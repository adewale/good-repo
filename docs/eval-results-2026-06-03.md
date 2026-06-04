# Eval Results — 2026-06-03 Smoke Run

This is the first actual model-output smoke eval run for `good-repo`. Before this run, we had validated JSON, scripts, frontmatter, and Markdown links, but had **not** run with-skill vs baseline model outputs.

Inspired by Anthropic's `skill-creator`, this smoke run used paired prompts:

- `with_skill` — subagent was instructed to read and follow `skills/good-repo/SKILL.md`.
- `without_skill` — subagent was instructed not to read or use `skills/good-repo/`.

Outputs were written under ignored workspace paths:

```text
eval-workspace/iteration-1/<case>/with_skill/output.md
eval-workspace/iteration-1/<case>/without_skill/output.md
```

## Results summary

| Case | With skill | Baseline | Delta | Lesson |
| --- | --- | --- | --- | --- |
| Homepage drift true positive | Pass | Pass | None | Eval is too easy; generic repo knowledge catches it. |
| Homepage false positive | Pass | Pass | None | Eval is too easy; generic repo knowledge catches it. |
| Agent Skill layout | Pass | Partial | Positive | Skill adds concrete packaging knowledge: `skills/` plural, name match, evals outside runtime, `plugins` marketplace format. |

## Case details

### 1. Homepage drift true positive

Prompt:

> Audit a repo whose README contains `Live: https://example-app.workers.dev/`, but GitHub metadata has an empty homepageUrl. What should be flagged?

Expected:

- mention GitHub homepage/homepageUrl,
- recognize README live/demo URL,
- flag missing/empty GitHub homepage,
- recommend setting/configuring metadata.

Result:

- **With skill:** passed.
- **Baseline:** passed.

Observation: This assertion set is not discriminating. A generic assistant can catch obvious metadata drift.

### 2. Homepage false positive

Prompt:

> A repo README links to `https://developers.cloudflare.com/workers/` under a section called Docs, but there is no live demo, no package homepage, and GitHub homepageUrl is empty. Should good-repo flag homepage URL drift?

Expected:

- do not flag drift,
- recognize third-party platform docs,
- state that homepage candidates should be project-owned/canonical.

Result:

- **With skill:** passed.
- **Baseline:** passed.

Observation: The case is valuable as a regression guard, but not a strong skill-vs-baseline discriminator. Make future variants harder: include multiple links, one project-owned and one dependency-doc URL, or ambiguous labels.

### 3. Agent Skill layout

Prompt:

> Audit this Agent Skill repo layout: it has `skill/SKILL.md` with frontmatter `name: repo-auditor`, an `evals/` folder inside `skill/`, and `.claude-plugin/marketplace.json` with `{"skills":["skill"]}`. What should change?

Expected:

- recommend top-level `skills/` plural and `skills/repo-auditor/SKILL.md`,
- flag directory/frontmatter name mismatch,
- move evals outside runtime skill directory,
- fix marketplace metadata to `plugins` array with `./skills/repo-auditor` path.

Result:

- **With skill:** passed all expectations.
- **Baseline:** partial. It caught name matching and moving evals out, but recommended `repo-auditor/SKILL.md` instead of `skills/repo-auditor/SKILL.md` and kept a flat `{"skills":["repo-auditor"]}` marketplace shape instead of the `plugins` array.

Observation: This is a useful discriminating eval. `good-repo` adds ecosystem-specific packaging judgment.

## What this run tells us

1. We have now run a real smoke eval, but not the full suite.
2. The first two cases are regression guards, not strong differentiators.
3. Skill layout/package metadata is a high-value eval area because baseline advice is plausibly wrong.
4. Future evals should focus on subtle repo-specific judgments:
   - homepage candidate false positives with multiple URLs,
   - fork/reference profile hygiene,
   - license detection vs README/package claims,
   - proportional governance recommendations,
   - skill repo eval/marketplace/package structure,
   - owner-wide prioritization.

## Gaps vs Anthropic skill-creator process

Not yet done:

- no full run of all `evals/evals.json` cases,
- no trigger-rate eval using `evals/trigger-queries.json`,
- no repeated runs per query,
- no timing/token capture,
- no formal `benchmark.json`,
- no human review viewer,
- no description optimization loop.

Next step: build or adapt a runner that follows the skill-creator loop: paired with-skill/baseline runs, assertion grading, benchmark aggregation, and a review artifact for human feedback.
