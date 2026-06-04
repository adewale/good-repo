# good-repo

A skill for making GitHub repositories easier to evaluate, adopt, contribute to, and trust.

`good-repo` audits a repository as a product surface: README, proof, examples, install path, repo structure, GitHub metadata, automation, maintenance signals, and community defaults. It is designed to pair with [`good-readme`](https://github.com/adewale/good-readme): let `good-readme` handle the README deeply; use `good-repo` for everything around it.

## Why this exists

Great code still loses users when the repo gives weak signals: no live demo, missing license, stale screenshots, vague GitHub description, no quick start, no contribution path, or no proof that the project actually works.

The first reference models are:

- [`nutlope/hallmark`](https://github.com/nutlope/hallmark) — a productized skill repo with a tight README, visible examples, live demo, install instructions, packaged skill entry point, modular references, quality gates, roadmap, license, and enough proof for a visitor to decide quickly.
- [`adewale/good-pr`](https://github.com/adewale/good-pr) — a small operational skill repo with real-pain origin, trigger-rich `SKILL.md`, PR templates, self-review checklist, readiness script, changelog, and evals.

## Install

```sh
npx skills add adewale/good-repo
```

Or copy `skills/good-repo/` into your agent skills directory.

For Pi package installs, the `package.json` includes `pi.skills`; for Claude/plugin installs, `.claude-plugin/marketplace.json` points to `./skills/good-repo`.

## Usage

Ask your coding agent from inside a repository:

```text
Audit this repo for GitHub effectiveness
```

```text
Configure this repo for maximum effectiveness
```

```text
Make this repo launch-ready; use good-readme for the README
```

```text
good-repo audit https://github.com/nutlope/hallmark
```

```text
good-repo explain https://github.com/adewale/good-pr
```

```text
good-repo owner-audit adewale
```

## What it checks

- **README/front door** — clarity, value proposition, install, usage, examples, honesty; delegated to `good-readme` when available.
- **Proof** — screenshots, live demos, examples, evals, tests, sample outputs, reproducible recipes.
- **Adoption path** — prerequisites, quick start, package metadata, release/download path, local dev setup.
- **Repository architecture** — docs split, examples, skill/package entry points, references, scripts, evals, generated assets, fixtures.
- **GitHub metadata** — description, homepage, topics, social preview, license, issue/discussion/wiki settings.
- **GitHub-official baseline** — README, Community Profile files, license, contribution guidelines, issue/PR templates, security policy, CI/workflows, and large-file hygiene.
- **Trust signals** — roadmap, changelog, maintenance status, contribution guidance, security policy, code owners.
- **Automation** — CI, release workflow, dependency updates, docs/examples validation.
- **Popularity/adoption context** — stars, forks, activity, contributor network, and quality signals without confusing popularity for quality.

## Example audit output

```markdown
## Repo Effectiveness Audit

**Project:** hallmark
**Class:** agent skill / design system
**Score:** 91 / 100
**Rating:** Exemplary

### Top strengths
1. Proof-first README — live demo, screenshots, examples, install command.
2. Skill packaging is clear — `package.json` points to `skills/hallmark/SKILL.md` and references.
3. Progressive disclosure — README stays short; detailed rules live in `references/` and docs.

### Priority improvements
1. Add GitHub topics — `skill`, `claude-code`, `cursor`, `codex`, `design-system`.
2. Add CONTRIBUTING.md or expand contributor workflow.
3. Add a lightweight CI check for skill metadata and internal links.
```

## What's included

| File | Purpose |
|------|---------|
| `skills/good-repo/SKILL.md` | Skill workflow, verbs, safety rails, output format |
| `skills/good-repo/scripts/check-repo-readiness.sh` | Mechanical repo readiness check |
| `skills/good-repo/scripts/audit-github-owner.py` | Owner/profile-wide GitHub audit script |
| `evals/evals.json` | Expected skill behaviors and regression cases |
| `evals/trigger-queries.json` | Trigger and near-miss cases for skill activation |
| `evals/run_eval.py` | Skill-creator-inspired eval schema validator, output grader, and benchmark generator |
| `evals/run_fixture_tests.py` | Fixture-level tests for mechanical repo readiness checks |
| `evals/fixtures/` | Tiny repos for homepage, license, and skill-layout regression checks |
| `evals/README.md` | Eval strategy for improving the skill |
| `docs/eval-results-2026-06-03.md` | First with-skill vs baseline smoke eval results |
| `docs/eval-results-2026-06-04.md` | Full behavior eval suite results with with-skill vs baseline comparison |
| `skills/good-repo/references/hallmark-exemplar.md` | What makes Hallmark an exemplary productized skill repo |
| `skills/good-repo/references/good-pr-exemplar.md` | What makes good-pr an exemplary small operational skill repo |
| `skills/good-repo/references/repo-anatomy.md` | Repo structure patterns by project type |
| `skills/good-repo/references/github-official-baseline.md` | GitHub's official docs baseline for healthy/discoverable repos |
| `skills/good-repo/references/popularity-signals.md` | Research-backed guidance on repo quality, popularity, stars, and adoption |
| `skills/good-repo/references/skill-repo-best-practices.md` | Agent Skill folder structure, packaging, eval, and marketplace guidance |
| `skills/good-repo/references/quality-checklist.md` | 100-point GitHub effectiveness rubric |
| `skills/good-repo/references/github-settings.md` | GitHub metadata, settings, and automation checklist |
| `skills/good-repo/references/anti-patterns.md` | Common repository smells and fixes |
| `docs/recipes.md` | Copy-paste prompts for audits, launch prep, and cleanup |
| `docs/sample-audits.md` | Scores and recommendations for a mixed GitHub sample |
| `docs/adewale-repos-assessment.md` | Owner-wide audit for `github.com/adewale` |
| `docs/adewale-recent-improvement-opportunities.md` | Recently modified `adewale` repos ranked by improvement opportunity |
| `docs/multi-account-signal-assessment.md` | Cross-account audit of public repo portfolios and missed quality signals |
| `docs/lessons-learned.md` | Lessons from owner-wide and cross-account audits |
| `docs/repo-quality-popularity.md` | Research brief on whether repo quality affects popularity/adoption |
| `CONTRIBUTING.md` | Lightweight contribution guidance |
| `.claude-plugin/marketplace.json` | Claude plugin / skills CLI metadata |
| `.github/PULL_REQUEST_TEMPLATE.md` | Minimal PR checklist |
| `.github/workflows/ci.yml` | JSON, shell, link, and readiness validation |

## What gets installed vs repo-only

```text
skills/good-repo/                     Installable runtime skill
├── SKILL.md
├── references/
└── scripts/

evals/                                Repo-only behavior checks
docs/                                 Repo-only reports, recipes, and lessons
.github/                              Repo-only CI and contribution surfaces
.claude-plugin/                       Marketplace/plugin metadata
package.json                          npm/Pi package metadata
```

The runtime skill stays self-contained under `skills/good-repo/`. Reports, evals, CI, and contribution process stay outside the installable folder.

## Relationship to good-readme

`good-readme` is the README specialist. `good-repo` should not reimplement it when it is available. The intended stack is:

1. Run `good-readme` to create or improve the README.
2. Run `good-repo` to configure the rest of the repository.
3. Re-run both before launch or release.

## License

MIT — see [LICENSE](LICENSE).
