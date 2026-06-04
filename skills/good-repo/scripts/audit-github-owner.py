#!/usr/bin/env python3
"""Audit all public repos for a GitHub owner.

This is a lightweight triage tool for good-repo. It uses GitHub metadata,
root contents, README text, and package metadata to produce a heuristic
repo-effectiveness score plus recommendations. It is not a substitute for a
manual audit, but it is useful for owner/profile-wide cleanup passes.
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


LABEL_WORDS = re.compile(
    r"\b(live|demo|website|homepage|play now|try it|launch|open app)\b",
    re.I,
)
IGNORE_HOMEPAGE_HOSTS = (
    "github.com",
    "x.com",
    "twitter.com",
    "shields.io",
    "img.shields.io",
    "youtube.com",
    "youtu.be",
    "opencollective.com",
)


@dataclass
class RepoAudit:
    name: str
    html_url: str
    repo_class: str
    score: int
    rating: str
    fork: bool
    archived: bool
    stars: int
    updated_at: str
    homepage_status: str
    top_recommendations: list[str]
    strengths: list[str]


def gh_api(path: str) -> Any:
    if shutil.which("gh"):
        raw = subprocess.check_output(["gh", "api", path], text=True, stderr=subprocess.DEVNULL)
        return json.loads(raw)
    url = f"https://api.github.com/{path.lstrip('/')}"
    with urllib.request.urlopen(url, timeout=15) as response:
        return json.load(response)


def list_repos(owner: str) -> list[dict[str, Any]]:
    repos: list[dict[str, Any]] = []
    page = 1
    while True:
        data = gh_api(f"users/{owner}/repos?per_page=100&page={page}")
        if not data:
            return repos
        repos.extend(data)
        page += 1


def get_root_names(owner: str, repo: str) -> set[str]:
    try:
        data = gh_api(f"repos/{owner}/{repo}/contents")
    except Exception:
        return set()
    return {item.get("name", "") for item in data if item.get("name")}


def get_readme(owner: str, repo: str) -> str:
    try:
        data = gh_api(f"repos/{owner}/{repo}/readme")
        return base64.b64decode(data.get("content", "")).decode(errors="ignore")
    except Exception:
        return ""


def get_file_text(owner: str, repo: str, path: str) -> str:
    try:
        data = gh_api(f"repos/{owner}/{repo}/contents/{path}")
        if isinstance(data, dict) and data.get("content"):
            return base64.b64decode(data["content"]).decode(errors="ignore")
    except Exception:
        pass
    return ""


def package_homepage(owner: str, repo: str) -> str:
    text = get_file_text(owner, repo, "package.json")
    if not text:
        return ""
    try:
        data = json.loads(text)
    except Exception:
        return ""
    value = data.get("homepage")
    return value if isinstance(value, str) else ""


def looks_like_project_url(url: str, owner: str, repo: str, *, from_package: bool = False) -> bool:
    if from_package:
        return True
    try:
        parsed = urllib.parse.urlparse(url)
    except ValueError:
        return False
    haystack = f"{parsed.netloc}{parsed.path}".lower()
    repo_l = repo.lower()
    repo_compact = re.sub(r"[-_.]", "", repo_l)
    owner_l = owner.lower()
    owner_aliases = {owner_l, "oshineye" if owner_l == "adewale" else owner_l}
    if repo_l in haystack or repo_compact in re.sub(r"[-_.]", "", haystack):
        return True
    if any(alias in haystack for alias in owner_aliases):
        return True
    return False


def candidate_homepage(readme: str, package_home: str, owner: str, repo: str) -> str:
    candidates: list[str] = []

    def add(url: str, *, from_package: bool = False) -> None:
        url = url.strip().strip('"\'`.,;')
        if not url.startswith(("http://", "https://")):
            return
        if any(host in url for host in IGNORE_HOMEPAGE_HOSTS):
            return
        if not looks_like_project_url(url, owner, repo, from_package=from_package):
            return
        if url not in candidates:
            candidates.append(url)

    add(package_home, from_package=True)
    for label, url in re.findall(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", readme):
        if LABEL_WORDS.search(label):
            add(url)
    for match in re.finditer(r"https?://[^\s)>\"'`]+", readme):
        start = max(0, match.start() - 100)
        context = readme[start : match.start()]
        if LABEL_WORDS.search(context):
            add(match.group(0))
    return candidates[0] if candidates else ""


def normalize_url(url: str | None) -> str:
    return (url or "").strip().rstrip("/")


def rating(score: int) -> str:
    if score >= 90:
        return "Exemplary"
    if score >= 75:
        return "Strong"
    if score >= 60:
        return "Adequate"
    if score >= 40:
        return "Weak"
    return "Poor"


def classify(meta: dict[str, Any], root: set[str], readme: str) -> str:
    name = meta["name"].lower()
    desc = (meta.get("description") or "").lower()
    home = (meta.get("homepage") or "").lower()
    if meta.get("fork"):
        return "fork/reference"
    if "skills" in root or name.endswith("-skill") or "skill" in desc:
        return "agent skill"
    if "wrangler.jsonc" in root or "workers.dev" in home or "cloudflare" in desc:
        return "cloudflare app/tool"
    if name.endswith(".github.io") or "website" in desc or "site" in desc:
        return "website"
    if "package.json" in root and ("cli" in desc or "bin" in readme.lower()):
        return "cli/tool"
    if "package.json" in root or "pyproject.toml" in root or "Cargo.toml" in root or "go.mod" in root:
        return "library/app"
    if "docs" in root or "specs" in root:
        return "docs/project"
    return "project"


def days_since(iso: str) -> int:
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - dt).days
    except Exception:
        return 9999


def audit_repo(owner: str, meta: dict[str, Any]) -> RepoAudit:
    name = meta["name"]
    root = get_root_names(owner, name)
    readme = get_readme(owner, name)
    pkg_home = package_homepage(owner, name) if "package.json" in root else ""
    cand_home = candidate_homepage(readme, pkg_home, owner, name)
    gh_home = meta.get("homepage") or ""
    repo_class = classify(meta, root, readme)
    is_fork = bool(meta.get("fork"))
    is_old = days_since(meta.get("updated_at", "")) > 365 * 3

    score = 0
    strengths: list[str] = []
    recs: list[str] = []

    # Front door + README (20)
    if readme:
        score += 8
        if len(readme) > 800:
            score += 4
        if re.search(r"install|quick start|usage|play now|development|run", readme, re.I):
            score += 4
        if meta.get("description"):
            score += 3
        if re.search(r"limitation|non-goal|out of scope|requires|support", readme, re.I):
            score += 1
        strengths.append("README present")
    else:
        recs.append("Add a README that explains what/why/how to run")
    if not meta.get("description"):
        recs.append("Add a concise GitHub description")

    # Proof + examples (15)
    proof = 0
    if gh_home or cand_home:
        proof += 4
        strengths.append("live/demo/docs URL present")
    if any(x in root for x in ("docs", "examples", "site", "specs")):
        proof += 4
    if re.search(r"\.png|\.jpg|\.gif|screenshot|demo|terminal output|example", readme, re.I):
        proof += 3
    if any(x in root for x in ("test", "tests", "evals")) or re.search(r"test|vitest|pytest|playwright|fast-check", readme, re.I):
        proof += 3
    if re.search(r"changelog|release|version", readme, re.I) or "CHANGELOG.md" in root:
        proof += 1
    score += min(15, proof)

    # Adoption + DX (15)
    adoption = 0
    manifests = {"package.json", "pyproject.toml", "Cargo.toml", "go.mod", "requirements.txt", "wrangler.jsonc"}
    if root & manifests:
        adoption += 4
    if re.search(r"install|npm install|pip install|cargo install|bun install|go install|clone", readme, re.I):
        adoption += 4
    if re.search(r"requires|node|python|bun|rust|go|cloudflare|wrangler", readme, re.I):
        adoption += 3
    if re.search(r"npm test|bun test|pytest|cargo test|typecheck|lint|dev server|run", readme, re.I):
        adoption += 3
    if re.search(r"expected|open http|play now|live", readme, re.I):
        adoption += 1
    score += min(15, adoption)

    # Docs + architecture (15)
    docs = 0
    if any(x in root for x in ("docs", "specs", "examples")):
        docs += 5
    if re.search(r"architecture|further reading|docs|examples|api", readme, re.I):
        docs += 4
    if any(x in root for x in ("src", "client", "worker", "shared", "skills")):
        docs += 3
    if not re.search(r"TODO:|coming soon|describe your", readme, re.I):
        docs += 2
    if "CLAUDE.md" in root:
        docs += 1
    score += min(15, docs)

    # Metadata + discoverability (10)
    meta_score = 0
    if meta.get("description"):
        meta_score += 2
    if cand_home:
        if normalize_url(cand_home) == normalize_url(gh_home):
            meta_score += 2
        else:
            recs.append(f"Set GitHub homepage to {cand_home}")
    elif gh_home:
        meta_score += 2
    else:
        # blank can be fine for old forks or pure libraries with README as docs
        meta_score += 1 if repo_class in {"fork/reference", "library/app", "project"} else 0
    topics = meta.get("topics") or []
    if topics:
        meta_score += 2
    else:
        recs.append("Add 5–12 accurate GitHub topics")
    if not meta.get("has_wiki"):
        meta_score += 1
    elif "docs" in root or "specs" in root:
        recs.append("Disable GitHub wiki unless intentionally used; version docs in the repo")
    score += min(10, meta_score)

    # Trust + governance (15)
    trust = 0
    if meta.get("license") or any(x.lower().startswith("license") for x in root):
        trust += 4
    else:
        recs.append("Add a root LICENSE or explicitly mark the repo all-rights-reserved")
    if "CHANGELOG.md" in root or re.search(r"changelog|release", readme, re.I):
        trust += 3
    elif not is_fork and not is_old:
        recs.append("Add CHANGELOG.md or release notes for maintained/versioned work")
    if "CONTRIBUTING.md" in root:
        trust += 2
    elif not is_fork and not is_old:
        recs.append("Add CONTRIBUTING.md or clarify whether PRs are welcome")
    if "SECURITY.md" in root:
        trust += 1
    if not is_old:
        trust += 3
    elif not meta.get("archived"):
        recs.append("Archive stale legacy repo or add a status note")
    if meta.get("archived") or is_fork:
        trust += 1
    score += min(15, trust)

    # Automation + release hygiene (10)
    automation = 0
    if ".github" in root:
        automation += 2
    # Can't see nested workflows from root names alone; inspect .github contents cheaply.
    has_ci = False
    try:
        gh_dir = gh_api(f"repos/{owner}/{name}/contents/.github/workflows")
        has_ci = bool(gh_dir)
    except Exception:
        has_ci = False
    if has_ci:
        automation += 4
        strengths.append("CI/workflows present")
    elif not is_fork and not is_old:
        recs.append("Add lightweight CI/smoke validation")
    if any(x in root for x in ("test", "tests", "evals")) or re.search(r"test|vitest|pytest|playwright", readme, re.I):
        automation += 3
    if any(x in root for x in ("package-lock.json", "bun.lock", "uv.lock", "Cargo.lock")):
        automation += 1
    score += min(10, automation)

    # Fork profile hygiene adjustment: don't let upstream README alone make old forks look great.
    if is_fork:
        score = min(score, 68)
        if is_old:
            score = min(score, 45)
        recs.insert(0, "If this fork is not actively maintained, archive it or add a note explaining why it exists")

    score = max(0, min(100, score))
    if not recs:
        recs.append("Mostly healthy; keep docs, releases, and metadata current")
    homepage_status = "OK"
    if cand_home and not gh_home:
        homepage_status = f"Missing GitHub homepage; candidate {cand_home}"
    elif cand_home and normalize_url(cand_home) != normalize_url(gh_home):
        homepage_status = f"Mismatch: candidate {cand_home}; GitHub {gh_home}"
    elif gh_home:
        homepage_status = f"Configured: {gh_home}"
    elif not cand_home:
        homepage_status = "No candidate"

    return RepoAudit(
        name=name,
        html_url=meta.get("html_url", f"https://github.com/{owner}/{name}"),
        repo_class=repo_class,
        score=score,
        rating=rating(score),
        fork=is_fork,
        archived=bool(meta.get("archived")),
        stars=int(meta.get("stargazers_count") or 0),
        updated_at=meta.get("updated_at", ""),
        homepage_status=homepage_status,
        top_recommendations=recs[:3],
        strengths=strengths[:3],
    )


def markdown(owner: str, audits: list[RepoAudit]) -> str:
    lines: list[str] = []
    lines.append(f"# GitHub Owner Audit — `{owner}`")
    lines.append("")
    lines.append("Heuristic profile-wide audit generated by `good-repo`. Scores are triage signals: use them to prioritize cleanup, then manually audit high-value repos.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    public_count = len(audits)
    forks = sum(a.fork for a in audits)
    homepage_issues = [a for a in audits if a.homepage_status.startswith("Missing") or a.homepage_status.startswith("Mismatch")]
    no_topics = [a for a in audits if "Add 5–12 accurate GitHub topics" in a.top_recommendations]
    lines.append(f"- Public repos assessed: **{public_count}**")
    lines.append(f"- Forks/reference repos: **{forks}**")
    lines.append(f"- Homepage URL issues detected: **{len(homepage_issues)}**")
    lines.append(f"- Median-ish score: **{sorted(a.score for a in audits)[len(audits)//2]}**")
    lines.append("")
    lines.append("## Repo table")
    lines.append("")
    lines.append("| Repo | Class | Score | Rating | Homepage | Top recommendations |")
    lines.append("| --- | --- | ---: | --- | --- | --- |")
    for a in sorted(audits, key=lambda x: (x.fork, x.score, x.name.lower())):
        recs = "; ".join(a.top_recommendations).replace("|", "/")
        home = a.homepage_status.replace("|", "/")
        lines.append(f"| [`{a.name}`]({a.html_url}) | {a.repo_class} | {a.score} | {a.rating} | {home} | {recs} |")
    if homepage_issues:
        lines.append("")
        lines.append("## Homepage URL issues")
        lines.append("")
        for a in homepage_issues:
            lines.append(f"- [`{a.name}`]({a.html_url}) — {a.homepage_status}")
    lines.append("")
    lines.append("## Priority cleanup themes")
    lines.append("")
    lines.append("1. Add topics across active repos; many good projects are effectively undiscoverable from GitHub metadata.")
    lines.append("2. Add root LICENSE files where README/package metadata says MIT or the repo is public and reusable.")
    lines.append("3. Archive or add status notes to old forks and legacy App Engine/Buzz-era projects.")
    lines.append("4. Keep live/demo URLs aligned across README, package metadata, and GitHub homepage.")
    lines.append("5. Add small CI checks to active skill/tool/app repos rather than broad, expensive workflows.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("owner", help="GitHub owner/user/org")
    parser.add_argument("--output", "-o", help="Write Markdown report to this path")
    args = parser.parse_args()

    metas = list_repos(args.owner)
    audits = [audit_repo(args.owner, meta) for meta in metas]
    report = markdown(args.owner, audits)
    if args.output:
        from pathlib import Path

        Path(args.output).write_text(report)
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
