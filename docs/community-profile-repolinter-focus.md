# Focus: GitHub Community Profile and Repolinter

This note narrows the similar-tool comparison to two practical baselines:

1. **GitHub Community Profile** — official GitHub health-file baseline exposed in the UI and REST API.
2. **Repolinter** — configurable repo policy linter from TODO Group. Important caveat: the project is currently archived, so treat it as a useful ruleset pattern, not a strategic dependency.

## Why these two matter

`good-repo` should not invent every repo-quality rule. GitHub Community Profile gives us an official minimum public-OSS baseline. Repolinter shows how to make repo hygiene policy-as-code.

But both are mostly mechanical. They do not answer the central `good-repo` question:

> Can the right visitor understand, trust, try, adopt, and contribute to this repo?

## GitHub Community Profile

Inspect with:

```sh
gh api repos/OWNER/REPO/community/profile
```

Useful fields:

- `health_percentage`
- `description`
- `documentation`
- `files.readme`
- `files.license`
- `files.contributing`
- `files.code_of_conduct`
- `files.issue_template`
- `files.pull_request_template`

### What it gets right

- Official GitHub baseline.
- Easy to explain to maintainers.
- Excellent for detecting missing README/license/contribution/template files.
- Good minimum for public repos seeking contributors.

### What it misses

- GitHub topics.
- Wiki/discussions/issues feature intent.
- CI/workflow quality.
- README usefulness, not just presence.
- Install path correctness.
- Demo/proof quality.
- Homepage drift.
- Agent Skill packaging/evals.
- Whether governance is proportionate.

### How `good-repo` should use it

- Add Community Profile health as an **official baseline signal**, not the whole score.
- Show it early in audits when GitHub API access exists.
- Treat missing license/contributing/templates as stronger findings when GitHub itself reports them missing.
- Avoid blindly chasing 100% health for tiny experiments, personal repos, or historical artifacts.

## Repolinter

Run with:

```sh
npx -y repolinter@0.12.0 lint . --format json
```

Caveat: Repolinter's GitHub repo currently starts with an **Archived** notice. It is still instructive, but `good-repo` should not depend on it as a required CI tool without a project decision.

### What it gets right

- Repo hygiene as machine-checkable policy.
- Configurable rule sets for organizations.
- CI-friendly JSON output.
- Checks beyond GitHub Community Profile, including CI integration and large files.
- Good model for enterprise/OSPO compliance.

### What it gets wrong or overstates

The default ruleset is intentionally broad and can over-prescribe:

- `CODE_OF_CONDUCT` as an error even for tiny/personal repos.
- `SECURITY.md` and `SUPPORT` as errors even for non-sensitive experiments.
- `test-directory-exists` while missing agent-skill `evals/` as test evidence.
- Source license headers as a warning where project-level license is enough.
- Uniform policy over project-class judgment.

### How `good-repo` should use it

- Borrow its policy-as-code model.
- Optionally emit or recommend a Repolinter config for orgs that want enforcement.
- Do not treat default Repolinter pass/fail as the `good-repo` score.
- Map Repolinter failures into `good-repo` categories with proportionality.

## Six-repo check

Repos checked:

- `adewale/oshineye-dev`
- `adewale/swiss-poster-skill`
- `adewale/pi-comfort`
- `adewale/good-pr`
- `adewale/testing-best-practices`
- `adewale/skill_scanner`

### GitHub Community Profile

| Repo | Health % | GitHub sees | Main official-profile gaps |
| --- | ---: | --- | --- |
| `oshineye-dev` | 14 | README, docs URL | missing license, contributing, issue/PR templates, code of conduct |
| `swiss-poster-skill` | 42 | README, license, description, docs URL | missing contributing, issue/PR templates, code of conduct |
| `pi-comfort` | 14 | README, docs URL | missing license, contributing, issue/PR templates, code of conduct |
| `good-pr` | 28 | README, description | missing detected license, contributing, issue/PR templates, code of conduct |
| `testing-best-practices` | 28 | README, description | missing detected license, contributing, issue/PR templates, code of conduct |
| `skill_scanner` | 28 | README, description | missing detected license, contributing, issue/PR templates, code of conduct |

### Repolinter default results

All six fail default Repolinter. Common default failures:

- missing `LICENSE` where applicable,
- missing `CONTRIBUTING`,
- missing `CODE_OF_CONDUCT`,
- missing `SECURITY.md`,
- missing `SUPPORT`,
- missing issue template,
- missing PR template,
- missing CI for some repos,
- missing test directory for some skill repos even when evals exist.

Per repo:

| Repo | Default Repolinter failures worth acting on | Default failures to treat cautiously |
| --- | --- | --- |
| `oshineye-dev` | license decision, README license note, PR/issue template if accepting contributions | code of conduct, security, support, changelog may be overkill for personal site |
| `swiss-poster-skill` | contributing, changelog, CI, issue/PR templates, eval/test evidence | code of conduct, security, support may be optional |
| `pi-comfort` | license decision, README license note, CI if package is meant to install, PR/issue template if accepting PRs | code of conduct, security, support, changelog may conflict with personal-use positioning |
| `good-pr` | root `LICENSE`, CI, issue/PR template, contributing | test-directory failure is misleading because skill evals exist; code of conduct/security/support optional |
| `testing-best-practices` | root `LICENSE`, CI, issue/PR template, contributing | code of conduct/security/support optional; default does not understand skill evals/research proof |
| `skill_scanner` | root `LICENSE`, README license note, issue/PR template, contributing | security/support may be useful later, but do not block current early status; source headers optional |

## What should change in `good-repo`

1. **Integrate Community Profile API** in owner/repo audits and report `health_percentage` as an official baseline.
2. **Keep Community Profile separate from effectiveness score** so tiny/personal/historical repos are not pushed into governance theater.
3. **Add Repolinter as optional evidence**: "if installed or requested, run it and translate findings." Do not add it as a required dependency yet.
4. **Add a project-class-aware Repolinter mapping**:
   - universal: README, license decision, no large files, package metadata, CI if maintained;
   - public OSS: contributing, issue/PR templates;
   - security-sensitive: `SECURITY.md`, support channel;
   - mature/community project: code of conduct;
   - agent skill: evals count as test/proof evidence.
5. **Teach the skill the archived-state caveat** for Repolinter so it does not recommend relying on an unmaintained tool without context.
6. **Use GitHub Community Profile before Repolinter** for most audits: it is official, supported, and directly maps to GitHub UI.

## Positioning

`good-repo` should position around these two like this:

> GitHub Community Profile tells you whether the public OSS basics exist. Repolinter tells you whether a configurable policy passes. `good-repo` tells you whether the repo is effective for the actual visitor, user, contributor, and maintainer — and what to fix first.
