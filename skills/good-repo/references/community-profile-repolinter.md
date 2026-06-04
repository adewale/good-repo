# GitHub Community Profile and Repolinter

Use this reference when grounding `good-repo` in official GitHub community-health signals or when a user asks about Repolinter-style policy checks.

## GitHub Community Profile

GitHub Community Profile is the closest official machine-readable health baseline for public repositories.

Inspect it with:

```sh
gh api repos/OWNER/REPO/community/profile
```

Important fields:

- `health_percentage`
- `description`
- `documentation`
- `files.readme`
- `files.license`
- `files.contributing`
- `files.code_of_conduct`
- `files.issue_template`
- `files.pull_request_template`

### How to use it

- Treat it as an **official baseline**, not the whole `good-repo` score.
- Cite it when recommending README, license, contributing guidance, issue templates, PR templates, code of conduct, or support/security files.
- Apply proportionality: a tiny personal experiment or historical artifact does not need to chase 100% Community Profile health.
- For public reusable repos, missing license is a high-severity trust/adoption issue.
- For repos inviting outside contribution, missing contributing guidance and PR/issue templates are concrete contribution-readiness gaps.

### What it misses

Community Profile does not judge:

- README quality beyond existence,
- GitHub topics,
- homepage drift,
- wiki/discussions/issues intent,
- CI quality,
- install path accuracy,
- proof/demo/examples,
- skill packaging/evals,
- package registry health,
- issue/PR responsiveness.

Use it as the GitHub-official floor; use `good-repo` for class-aware readiness.

## Repolinter

Repolinter is a configurable repository policy linter from TODO Group.

Run it manually with:

```sh
npx -y repolinter@0.12.0 lint . --format json
```

Important caveat: Repolinter's upstream repository is currently archived. Treat it as a useful policy-checking pattern and optional evidence, not a default dependency unless the user explicitly wants it.

### What it is good for

- OSPO/organization policy enforcement.
- CI-friendly mechanical checks.
- Required file/path/content rules.
- Detecting missing license/README/contributing/templates/CI/large-file patterns.

### What to be careful about

The default ruleset can over-prescribe:

- `CODE_OF_CONDUCT` for tiny or personal repos,
- `SECURITY.md`/`SUPPORT` for non-sensitive experiments,
- `test-directory-exists` while ignoring agent-skill `evals/`,
- source license headers where a project-level license is sufficient,
- uniform policy for all repo classes.

Never map default Repolinter failure directly to `good-repo` failure. Translate findings through repo class, maturity, and maintainer intent.

## Suggested mapping

| Repolinter / Community signal | good-repo interpretation |
| --- | --- |
| README missing | Launch blocker for almost every public repo |
| LICENSE missing | Trust/legal blocker for public reusable repos; ask if all-rights-reserved is intentional |
| CONTRIBUTING missing | Gap only if public PRs are welcome or expected |
| Issue/PR template missing | Useful for repos with issue/PR traffic; optional for tiny personal repos |
| CODE_OF_CONDUCT missing | Community-readiness gap for mature public communities; not default for experiments |
| SECURITY.md missing | Important for packages/services/security-sensitive repos; optional for toy/demo repos |
| SUPPORT missing | Useful when support channels exist; avoid fake support contracts |
| CI missing | High-value if repo has tests/build/evals/docs checks; not mandatory for one-off historical artifacts |
| Test directory missing | For agent skills, evals may be the right proof; for docs repos, link checks may be better |
| Large files present | Usually a repo-health issue; consider Git LFS/artifact storage |

## Recommended `good-repo` behavior

1. Check GitHub Community Profile when `gh` or GitHub API access is available.
2. Report the health percentage as an official baseline.
3. Explain missing files in context, not as universal blockers.
4. If the user asks for policy enforcement, suggest Repolinter or a Repolinter-style config.
5. If using Repolinter, prefer a custom class-aware ruleset over the default ruleset.
6. Keep `good-repo` focused on effectiveness: front door, proof, adoption path, metadata coherence, trust, automation, and contribution readiness.

## Sources

- GitHub Community Profile docs: https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories
- GitHub Community Profile REST API: https://docs.github.com/en/rest/metrics/community?apiVersion=2022-11-28#get-community-profile-metrics
- Repolinter: https://github.com/todogroup/repolinter
- Repolinter rules: https://github.com/todogroup/repolinter/blob/main/docs/rules.md
