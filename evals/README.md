# good-repo Eval Strategy

`good-repo` evals should prove the skill adds repo-quality judgment that a generic assistant often misses. They are repo-only development artifacts, not part of the runtime skill package.

This strategy follows the useful parts of Anthropic's `skill-creator` workflow: run paired with-skill and baseline outputs, grade assertions, aggregate results, inspect qualitative output, then revise the skill based on observed failures rather than vibes.

## Current status

- Static validation runs via `npm run validate`.
- A first smoke eval was run on 2026-06-03; see `docs/eval-results-2026-06-03.md`.
- The full model-output eval suite has **not** been run yet.
- Trigger-rate evals for `evals/trigger-queries.json` have **not** been run yet.

## What to evaluate

Use evals to improve five behaviors:

1. **Triggering** — the skill should load for repo audits, launch prep, GitHub metadata checks, skill repo structure, owner-wide audits, homepage URL drift, and README-vs-repo consistency.
2. **Classification** — the skill should classify repo type before scoring: skill, CLI, app, library, docs repo, fork/reference, historical artifact.
3. **Rubric judgment** — scores should be calibrated against known exemplars (`hallmark`, `good-pr`, `ripgrep`, `flask`) and weak/misaligned repos.
4. **Actionability** — recommendations should name the smallest concrete file, setting, command, or GitHub metadata change.
5. **Safety** — the skill must not mutate GitHub settings, add legal/governance files, or invent claims without approval/evidence.

## Eval types

### 1. Trigger evals

Prompt-only positive and near-negative cases in `evals/trigger-queries.json`. These define when the skill should load and when a narrower skill should win.

Important positives:

- repo quality / launch readiness,
- GitHub metadata configuration,
- homepage URL drift,
- owner-wide audits,
- Agent Skill repo layout,
- exemplar comparison,
- README plus repo-level launch gaps.

Important negatives:

- README-only rewriting → `good-readme`,
- one PR description/review → `good-pr`,
- test implementation/quality → `testing-best-practices`,
- code review without repo-public-surface concern.

### 2. Synthetic behavior evals

Small prompt-only cases in `evals/evals.json`. These catch recurring judgment errors:

- homepage URL missing vs false-positive homepage candidate,
- license claimed in README/package but missing root `LICENSE`,
- skill directory/frontmatter mismatch,
- over-prescribing governance for tiny repos,
- treating forks like active product repos,
- scoring README polish while missing repo-level trust gaps.

### 3. Fixture repo evals

Create tiny fake repos under `evals/fixtures/` when scripts or file scanning need real files. Each fixture should target one behavior:

```text
evals/fixtures/homepage-missing/
├── README.md        # Live URL present
└── .git/config      # origin points to test repo or script override

evals/fixtures/skill-layout-bad/
├── skill/SKILL.md   # wrong location/name mismatch
└── evals-in-runtime/
```

Run `skills/good-repo/scripts/check-repo-readiness.sh` or a future fixture-aware validator and assert exact warnings.

### 4. Golden audit evals

For a small stable set of real repos, keep expected score bands and must-mention findings:

| Repo | Expected band | Must mention |
| --- | ---: | --- |
| `nutlope/hallmark` | 88–95 | proof-first, topics/CI/contributing gaps |
| `adewale/good-pr` | 78–86 | templates/script/evals, missing license/topics/CI |
| `BurntSushi/ripgrep` | 93–98 | mature CLI, docs/releases/license/CI |
| `e3ntity/nonescape` | 50–65 | homepage URL drift, CI/docs gaps |

Use bands, not exact scores; GitHub metadata changes over time.

### 5. Adversarial false-positive evals

Add negative cases where the skill should **not** recommend the obvious generic fix:

- README links to framework docs; do not set GitHub homepage to dependency docs.
- Tiny personal experiment; do not add full governance suite.
- Fork/reference repo; do not demand product-level launch readiness.
- Pure library with README-as-docs; blank homepage can be acceptable.
- Private/internal repo; public OSS discoverability criteria may not apply.

### 6. Baseline comparison

Periodically run with and without the skill. A useful eval is one where `good-repo` adds specific judgment:

- names homepage URL drift,
- catches license inconsistency,
- distinguishes runtime skill files from repo-only evals,
- recommends archive/status for stale forks,
- avoids cargo-culting Hallmark into tiny operational skills.

If a no-skill baseline passes every assertion, strengthen the eval.

## Assertion quality

Good assertions are discriminating and concrete:

- Good: "mentions GitHub `homepageUrl` is empty even though README has a `Live:` URL."
- Good: "does not recommend setting homepage to Cloudflare docs when the docs link is only a dependency reference."
- Weak: "mentions README."
- Weak: "says improve docs."

Prefer assertions on decisions and evidence, not vocabulary alone.

## Skill-creator-inspired run protocol

For a real eval iteration:

1. **Pick eval cases** — start with 3–5 cases, not the whole suite.
2. **Run paired outputs in the same turn**:
   - `with_skill`: explicitly read/follow `skills/good-repo/SKILL.md`.
   - `without_skill`: explicitly do not read/use `skills/good-repo/`.
3. **Save outputs** under `eval-workspace/iteration-N/<case>/{with_skill,without_skill}/outputs/`.
4. **Grade assertions** against both outputs. For programmatic assertions, use scripts; for judgment assertions, record quoted evidence.
5. **Mark non-discriminating assertions** where baseline and with-skill both pass.
6. **Aggregate** pass rates and qualitative findings into a benchmark/report file.
7. **Revise the skill** only when a failure generalizes beyond one case.
8. **Record lessons** in `docs/lessons-learned.md` when doctrine, scripts, or trigger policy changes.

The most important skill-creator lesson: if baseline passes every assertion, the eval may still be useful as a regression guard, but it does not prove the skill adds value.

## Improvement loop

1. Capture a failure from a real audit.
2. Add or update an eval that fails for that failure.
3. Change the smallest skill reference or script rule.
4. Re-run validation and the affected eval manually.
5. Record the lesson in `docs/lessons-learned.md` when the rule changes.

## Current gaps

- No automated runner yet for `evals/evals.json`.
- No fixture repos yet for script-level homepage detection.
- No baseline-vs-skill comparison harness yet.
- No score-calibration suite with hand-reviewed expected bands yet.
