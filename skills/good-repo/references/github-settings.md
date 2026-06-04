# GitHub Settings, Metadata, and Automation

Use this reference for `good-repo configure` and `good-repo launch`. Prefer inspecting first, then proposing changes. Do not mutate remote settings without user approval.

## Table of Contents

- [Inspecting repo metadata](#inspecting-repo-metadata)
- [High-leverage metadata](#high-leverage-metadata)
- [Feature toggles](#feature-toggles)
- [Recommended `.github/` files](#recommended-github-files)
- [CI patterns](#ci-patterns)
- [Dependency updates](#dependency-updates)
- [Branch protection](#branch-protection)
- [Labels](#labels)
- [Manual launch checklist](#manual-launch-checklist)

## Inspecting repo metadata

If GitHub CLI is available:

```sh
gh repo view --json \
  nameWithOwner,description,homepageUrl,repositoryTopics,licenseInfo,defaultBranchRef,\
  hasIssuesEnabled,hasDiscussionsEnabled,hasWikiEnabled,isTemplate,visibility,\
  pushedAt,latestRelease,url
```

For a specific repo:

```sh
gh repo view OWNER/REPO --json nameWithOwner,description,homepageUrl,repositoryTopics,licenseInfo,url
```

Public API fallback:

```sh
curl -s https://api.github.com/repos/OWNER/REPO
```

## High-leverage metadata

### Description

Good descriptions are 80–140 characters, plain language, and searchable.

Pattern:

```text
A <project class> that <does primary job> for <audience>.
```

Examples:

- `A design skill for AI coding agents that makes generated UIs look intentional.`
- `A CLI for filtering and transforming newline-delimited event streams.`
- `A README quality skill that writes and audits project documentation.`

### Homepage

Set to the most useful next click:

1. Live demo for apps/design/visual projects.
2. Documentation site for frameworks/platforms.
3. Package registry for libraries.
4. Marketplace/listing page for skills/plugins.
5. Leave blank only if no stable destination exists.

**Detection rule:** if the README, package manifest, marketplace metadata, or docs contain a likely live/demo/docs/homepage URL, GitHub's `homepageUrl` should point to it. A common repo smell is a README with `Live: https://...` while GitHub's sidebar homepage is blank.

Candidate homepage signals:

- `package.json.homepage`
- README links with text like `Live`, `Demo`, `Docs`, `Website`, `Play now`, `Try it`, `Homepage`
- framework deploy URLs for the project (`workers.dev`, `vercel.app`, `netlify.app`, project docs domains)
- marketplace/plugin listing URLs

Do not treat every external link as a homepage candidate. Credits, dependency docs, tweets, licenses, badges, and source articles are usually not homepage URLs.

### Topics

Use 5–12 accurate topics. Include:

- Project class: `cli`, `library`, `template`, `skill`, `docs`.
- Ecosystem: `nodejs`, `typescript`, `python`, `rust`, `go`, `claude-code`, `cursor`.
- Domain: `design-system`, `readme`, `github`, `observability`, etc.
- Avoid spammy or aspirational topics.

Example for this repo:

```text
github, repository, repo-health, documentation, readme, open-source, skill, claude-code, cursor, codex
```

Set topics with approval:

```sh
gh repo edit OWNER/REPO \
  --description "..." \
  --homepage "https://..." \
  --add-topic github \
  --add-topic repo-health
```

`gh repo edit` may not support every setting on every CLI version. Use `gh repo edit --help` before proposing exact commands.

### Social preview

GitHub's social preview is often manual through Settings → Social preview. Recommend an image when:

- Repo is public.
- Links will be shared externally.
- Project has visual output or strong branding.

Good preview images:

- 1280×640 or close.
- Readable project name and one-line promise.
- Actual screenshot/output if visual.
- No tiny text, no badge soup.

## Feature toggles

| Feature | Enable when | Disable when |
| --- | --- | --- |
| Issues | Maintainer will triage bugs/requests | Repo is archive/demo-only or uses external tracker |
| Discussions | Community Q&A matters | Maintainer cannot monitor it |
| Wiki | Existing team uses GitHub Wiki | Prefer versioned docs in repo |
| Projects | Active public planning | No one maintains project board |
| Sponsorship | Maintainer has funding channel | Not applicable |

## Recommended `.github/` files

### Pull request template

`.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## Summary

- 

## Validation

- [ ] Tests pass / not applicable
- [ ] Docs updated / not applicable
- [ ] README examples still accurate / not applicable

## Notes

- 
```

### Bug report issue form

`.github/ISSUE_TEMPLATE/bug_report.yml`:

```yaml
name: Bug report
description: Report something broken or incorrect
title: "bug: "
labels: [bug]
body:
  - type: textarea
    id: what-happened
    attributes:
      label: What happened?
      description: Describe the bug and expected behavior.
    validations:
      required: true
  - type: textarea
    id: reproduce
    attributes:
      label: Reproduction
      description: Commands, repo, URL, or steps to reproduce.
    validations:
      required: true
  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: OS, runtime version, package version, browser, or harness.
```

### Feature request issue form

`.github/ISSUE_TEMPLATE/feature_request.yml`:

```yaml
name: Feature request
description: Suggest an improvement
title: "feat: "
labels: [enhancement]
body:
  - type: textarea
    id: problem
    attributes:
      label: Problem
      description: What are you trying to do that is hard today?
    validations:
      required: true
  - type: textarea
    id: proposal
    attributes:
      label: Proposed solution
      description: What should change?
  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives considered
```

### Security policy

`SECURITY.md`:

```markdown
# Security Policy

## Reporting a vulnerability

Please do not open public issues for vulnerabilities. Email <security contact> with:

- affected version or commit
- reproduction steps
- impact
- suggested fix, if known

We aim to acknowledge reports within <timeframe>.
```

Ask the user for contact/timeframe before creating this.

### CODEOWNERS

Use only when there are clear owners:

```text
# Default owners
* @owner

# Documentation
/docs/ @docs-owner
```

## CI patterns

Add the smallest workflow that validates the repo's actual promise.

### Node/package smoke CI

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm test --if-present
      - run: npm run build --if-present
```

Do not add `npm ci` if there is no lockfile or dependency install path. Adjust to the ecosystem.

### Docs/link check

Prefer a lightweight checker only if the repo can maintain it. At minimum, validate internal links manually during audits:

```sh
python3 - <<'PY'
from pathlib import Path
for p in Path('.').rglob('*.md'):
    print(p)
PY
```

For serious docs repos, recommend a real link-check workflow.

## Dependency updates

`.github/dependabot.yml` for npm:

```yaml
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
    open-pull-requests-limit: 5
```

Only add dependabot when there is an active maintainer. Dependency bots create work.

## Branch protection

Recommend after CI exists:

- Require PR before merge.
- Require status checks to pass.
- Require branch up to date for larger teams.
- Restrict force pushes.

Do not attempt to configure branch protection without explicit permission and repo admin access.

## Labels

Useful default labels:

- `bug`
- `enhancement`
- `documentation`
- `good first issue`
- `help wanted`
- `question`
- `security`
- `needs reproduction`

Avoid elaborate taxonomies until the issue volume justifies them.

## Manual launch checklist

Before public launch:

- [ ] GitHub description set.
- [ ] Homepage set to demo/docs/package.
- [ ] Topics set.
- [ ] Social preview uploaded.
- [ ] License detected by GitHub.
- [ ] README first screen works.
- [ ] Install/quick-start tested on a clean checkout.
- [ ] Issues/discussions/wiki intentionally configured.
- [ ] Release/tag exists if install command references a version.
- [ ] CI status passing if badges show CI.
