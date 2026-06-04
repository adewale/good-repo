#!/usr/bin/env bash
# check-repo-readiness.sh
#
# Quick mechanical checks for GitHub repository launch/readiness.
# Run from the root of the repository you want to inspect.

set -euo pipefail

PASS="✓"
WARN="⚠"
FAIL="✗"

has_file() {
  [ -f "$1" ]
}

has_dir() {
  [ -d "$1" ]
}

has_readme() {
  find . -maxdepth 1 -type f -iname 'readme*' | grep -q .
}

count_matches() {
  find . -path ./.git -prune -o "$@" -print 2>/dev/null | wc -l | tr -d ' '
}

repo_slug_from_origin() {
  if [ -n "${GOOD_REPO_REPO_SLUG:-}" ]; then
    printf '%s\n' "$GOOD_REPO_REPO_SLUG"
    return 0
  fi
  local remote
  remote="$(git config --get remote.origin.url 2>/dev/null || true)"
  if [[ "$remote" =~ github.com[:/]([^/]+)/([^/.]+)(\.git)?$ ]]; then
    printf '%s/%s\n' "${BASH_REMATCH[1]}" "${BASH_REMATCH[2]}"
  fi
}

candidate_homepage_url() {
  local slug="${1:-}"
  OWNER_FOR_CANDIDATE="${slug%%/*}" REPO_FOR_CANDIDATE="${slug#*/}" python3 - <<'PY'
from pathlib import Path
import json
import os
import re
import urllib.parse

candidates = []
label_words = re.compile(r'\b(live|demo|website|homepage|play now|try it|launch|open app)\b', re.I)
ignore_hosts = ('github.com', 'x.com', 'twitter.com', 'shields.io', 'img.shields.io', 'youtube.com', 'youtu.be', 'opencollective.com')
owner = os.environ.get('OWNER_FOR_CANDIDATE', '')
repo = os.environ.get('REPO_FOR_CANDIDATE', '')
repo_l = repo.lower()
repo_compact = re.sub(r'[-_.]', '', repo_l)
owner_l = owner.lower()
owner_aliases = {owner_l}
if owner_l == 'adewale':
    owner_aliases.add('oshineye')

def looks_like_project_url(url, from_package=False):
    if from_package:
        return True
    try:
        parsed = urllib.parse.urlparse(url)
    except ValueError:
        return False
    haystack = f'{parsed.netloc}{parsed.path}'.lower()
    compact = re.sub(r'[-_.]', '', haystack)
    return bool(
        (repo_l and repo_l in haystack) or
        (repo_compact and repo_compact in compact) or
        any(alias and alias in haystack for alias in owner_aliases)
    )

def add(url, from_package=False):
    if not url:
        return
    url = url.strip().strip('"\'`.,;')
    if not url.startswith(('http://', 'https://')):
        return
    if any(host in url for host in ignore_hosts):
        return
    if not looks_like_project_url(url, from_package=from_package):
        return
    if url not in candidates:
        candidates.append(url)

# Manifest homepage is the strongest local signal.
p = Path('package.json')
if p.exists():
    try:
        data = json.loads(p.read_text())
        add(data.get('homepage'), from_package=True)
    except Exception:
        pass

# README links are candidates only when their label suggests live/demo/homepage.
for rp in Path('.').glob('*'):
    if not (rp.is_file() and rp.name.lower().startswith('readme')):
        continue
    text = rp.read_text(errors='ignore')
    for label, url in re.findall(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', text):
        if label_words.search(label):
            add(url)
    # Bare URLs are candidates only when nearby text carries a homepage signal.
    for m in re.finditer(r'https?://[^\s)>"\'`]+', text):
        url = m.group(0)
        start = max(0, m.start() - 80)
        context = text[start:m.start()]
        if label_words.search(context):
            add(url)

print(candidates[0] if candidates else '')
PY
}

github_homepage_url() {
  local slug="$1"
  if [ -n "${GOOD_REPO_GITHUB_HOMEPAGE+x}" ]; then
    printf '%s\n' "$GOOD_REPO_GITHUB_HOMEPAGE"
    return 0
  fi
  if [ -z "$slug" ]; then
    return 0
  fi
  if command -v gh >/dev/null 2>&1; then
    gh repo view "$slug" --json homepageUrl --jq '.homepageUrl // ""' 2>/dev/null || true
  else
    python3 - "$slug" <<'PY' 2>/dev/null || true
import json
import sys
import urllib.request
slug = sys.argv[1]
try:
    with urllib.request.urlopen(f'https://api.github.com/repos/{slug}', timeout=8) as response:
        data = json.load(response)
    print(data.get('homepage') or '')
except Exception:
    print('')
PY
  fi
}

normalize_url() {
  python3 - "$1" <<'PY'
import sys
u = (sys.argv[1] or '').strip()
while u.endswith('/'):
    u = u[:-1]
print(u)
PY
}

skill_name_from_file() {
  python3 - "$1" <<'PY'
from pathlib import Path
import sys
for line in Path(sys.argv[1]).read_text(errors='ignore').splitlines():
    if line.strip().startswith('name:'):
        print(line.split(':', 1)[1].strip().strip('"\''))
        break
PY
}

echo "Repo Readiness Check"
echo "===================="
echo ""

if has_readme; then
  echo "$PASS  README present"
else
  echo "$FAIL  README missing"
fi

if has_file LICENSE || has_file LICENSE.md; then
  echo "$PASS  LICENSE present"
else
  echo "$WARN  LICENSE missing or not in a standard root file"
fi

if has_file CHANGELOG.md; then
  echo "$PASS  CHANGELOG present"
else
  echo "$WARN  CHANGELOG missing (recommended for versioned packages/tools)"
fi

if has_file CONTRIBUTING.md; then
  echo "$PASS  CONTRIBUTING present"
else
  echo "$WARN  CONTRIBUTING missing (recommended for public OSS accepting PRs)"
fi

if has_file package.json; then
  if python3 -m json.tool package.json >/dev/null 2>&1; then
    echo "$PASS  package.json parses"
  else
    echo "$FAIL  package.json does not parse"
  fi
else
  echo "$WARN  package.json missing (fine for non-Node repos; expected for npm-distributed skills/packages)"
fi

PACKAGED_SKILL_COUNT=0
if has_dir skills; then
  PACKAGED_SKILL_COUNT=$(find skills -mindepth 2 -maxdepth 2 -name SKILL.md -type f 2>/dev/null | wc -l | tr -d ' ')
fi
IS_SKILL_REPO=0
if [ "$PACKAGED_SKILL_COUNT" -gt 0 ] || has_file .claude-plugin/marketplace.json; then
  IS_SKILL_REPO=1
fi
if [ "$PACKAGED_SKILL_COUNT" -gt 0 ]; then
  echo "$PASS  Packaged skill files found: $PACKAGED_SKILL_COUNT"
elif [ "$IS_SKILL_REPO" -eq 1 ]; then
  echo "$WARN  Skill repo metadata found, but no skills/<name>/SKILL.md packaged skill files were found"
else
  echo "$PASS  No packaged skill files found (normal for non-skill repos)"
fi

if has_file skill/SKILL.md; then
  echo "$WARN  Found skill/SKILL.md; use skills/<skill-name>/SKILL.md so the installable directory matches the skill name"
fi

if has_dir skills; then
  while IFS= read -r skill_file; do
    skill_dir="$(dirname "$skill_file")"
    skill_dir="$(basename "$skill_dir")"
    skill_name="$(skill_name_from_file "$skill_file")"
    if [ -n "$skill_name" ] && [ "$skill_name" != "$skill_dir" ]; then
      echo "$WARN  Skill directory name ($skill_dir) does not match SKILL.md frontmatter name ($skill_name)"
    fi
  done < <(find skills -mindepth 2 -maxdepth 2 -name SKILL.md -type f 2>/dev/null)
fi

RUNTIME_EVAL_COUNT=0
if has_dir skills; then
  RUNTIME_EVAL_COUNT=$(find skills -path '*/evals/*' -type f 2>/dev/null | wc -l | tr -d ' ')
fi
if has_dir skill/evals; then
  RUNTIME_EVAL_COUNT=$((RUNTIME_EVAL_COUNT + $(find skill/evals -type f 2>/dev/null | wc -l | tr -d ' ')))
fi
if [ "$RUNTIME_EVAL_COUNT" -gt 0 ]; then
  echo "$WARN  Evals found inside an installable skill directory; keep evals/ as a repo-only top-level directory"
fi

if has_file .claude-plugin/marketplace.json; then
  python3 - <<'PY'
from pathlib import Path
import json
try:
    data = json.loads(Path('.claude-plugin/marketplace.json').read_text())
except Exception:
    raise SystemExit(0)
if 'plugins' not in data and 'skills' in data:
    print('⚠  Marketplace metadata uses a flat skills list; prefer a plugins array with ./skills/<skill-name> paths')
PY
fi

REFERENCE_COUNT=0
if has_dir skills; then
  REFERENCE_COUNT=$(find skills -path '*/references/*.md' -type f 2>/dev/null | wc -l | tr -d ' ')
fi
if [ "$REFERENCE_COUNT" -gt 0 ]; then
  echo "$PASS  Skill reference docs found: $REFERENCE_COUNT"
elif [ "$IS_SKILL_REPO" -eq 1 ]; then
  echo "$WARN  No modular skill reference docs found"
else
  echo "$PASS  No skill reference docs expected"
fi

if has_dir docs || has_dir examples || has_dir site; then
  echo "$PASS  Proof/docs/example directory present"
else
  echo "$WARN  No docs/, examples/, or site/ directory found"
fi

if has_file evals/evals.json; then
  if python3 -m json.tool evals/evals.json >/dev/null 2>&1; then
    echo "$PASS  evals/evals.json parses"
  else
    echo "$FAIL  evals/evals.json does not parse"
  fi
elif [ "$IS_SKILL_REPO" -eq 1 ]; then
  echo "$WARN  evals/evals.json missing (strongly recommended for skill repos)"
else
  echo "$PASS  evals/evals.json not expected unless this repo defines an agent skill"
fi

if has_dir .github; then
  echo "$PASS  .github directory present"
else
  echo "$WARN  .github directory missing"
fi

if has_file .github/workflows/ci.yml || has_file .github/workflows/ci.yaml; then
  echo "$PASS  CI workflow present"
else
  echo "$WARN  CI workflow missing"
fi

REPO_SLUG="$(repo_slug_from_origin || true)"
CANDIDATE_HOMEPAGE="$(candidate_homepage_url "$REPO_SLUG")"
if [ -n "$REPO_SLUG" ]; then
  GH_HOMEPAGE="$(github_homepage_url "$REPO_SLUG")"
  if [ -n "$CANDIDATE_HOMEPAGE" ]; then
    if [ -z "$GH_HOMEPAGE" ]; then
      echo "$WARN  Candidate homepage URL found ($CANDIDATE_HOMEPAGE), but GitHub homepage is not configured for $REPO_SLUG"
    elif [ "$(normalize_url "$CANDIDATE_HOMEPAGE")" = "$(normalize_url "$GH_HOMEPAGE")" ]; then
      echo "$PASS  GitHub homepage matches candidate URL: $GH_HOMEPAGE"
    else
      echo "$WARN  Candidate homepage URL ($CANDIDATE_HOMEPAGE) differs from GitHub homepage ($GH_HOMEPAGE)"
    fi
  elif [ -n "$GH_HOMEPAGE" ]; then
    echo "$PASS  GitHub homepage configured: $GH_HOMEPAGE"
  else
    echo "$WARN  No candidate homepage URL found and GitHub homepage is empty"
  fi
else
  echo "$WARN  Could not infer GitHub repo from remote.origin.url; homepage configuration not checked"
fi

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  CHANGED=$(git status --short | wc -l | tr -d ' ')
  if [ "$CHANGED" -gt 0 ]; then
    echo "$WARN  Working tree has uncommitted changes: $CHANGED paths"
  else
    echo "$PASS  Working tree clean"
  fi
fi

echo ""
echo "Done. Treat $FAIL as blockers and $WARN as judgment calls, not automatic failures."
