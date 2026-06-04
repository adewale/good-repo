# Lessons Learned — GitHub Repo Quality Audit

Generated after auditing all public repositories under [`github.com/adewale`](https://github.com/adewale) with `good-repo` on 2026-06-03.

See [`adewale-repos-assessment.md`](adewale-repos-assessment.md) for the repo-by-repo table.

## What we audited

- **76** public repos
- **24** forks/reference repos
- **52** non-fork repos
- **43** repos updated in 2026
- **26** repos last updated before 2024

Score distribution from the heuristic owner-wide pass:

| Rating | Count |
| --- | ---: |
| Exemplary | 1 |
| Strong | 16 |
| Adequate | 18 |
| Weak | 22 |
| Poor | 19 |

This score is a triage signal, not a final judgment. It is intentionally strict about discoverability, trust, and maintenance signals because those are the easiest repo-quality wins to miss.

## What we learned

### 0. GitHub's official baseline is narrower than good-repo's rubric

GitHub's docs do not publish a single "good repo" score. The closest official baseline is a combination of:

- README guidance: what the project does, why it is useful, how to start, where to get help, and who maintains it.
- Community Profile / recommended community standards for public repos: README, `CODE_OF_CONDUCT`, `LICENSE`, `CONTRIBUTING`, issue/PR templates, and related health files.
- Repository metadata: description, homepage, and topics for discoverability.
- Security policy where vulnerability reporting matters.
- GitHub Actions CI/workflows for automated build/test feedback.
- Large-file and repository-size hygiene.

**Lesson:** `good-repo` should distinguish GitHub-official findings from its own adoption/product heuristics. Official docs justify metadata, license, contribution, security, CI, and size checks; `good-repo` adds class-specific proof, evals, homepage drift detection, owner/profile cleanup, and proportional governance judgment.

### 0b. Repo quality can affect adoption, but popularity is confounded

Empirical GitHub research supports correlations between visible quality/social signals and popularity or contribution adoption, especially README/documentation richness, activity, contributor signals, and project/social context. But direct causal evidence is limited, and stars/forks are heavily confounded by age, ecosystem size, owner reputation, social media, and domain demand.

**Lesson:** `good-repo` should score quality separately from popularity. Stars, forks, and watchers are lagging outcome/social-proof signals, not quality criteria. Quality recommendations should be framed as improving discoverability, trust, tryability, and contribution readiness—not as guaranteed star growth. Details live in `docs/repo-quality-popularity.md` and `skills/good-repo/references/popularity-signals.md`.

### 0c. Cross-account audits exposed missing portfolio and context signals

A follow-up scan of `paulkinlan`, `jakearchibald`, `pbakaus`, `chrischabot`, `timothyjordan`, `fayazara`, and `yusukebe` showed that file-based repo hygiene is not enough for experienced public GitHub profiles. Details are in `docs/multi-account-signal-assessment.md`.

New signals to add or weight better:

- profile README and pinned repositories as the owner's curated portfolio;
- pinned external/org repos, especially for maintainers whose major work lives outside their personal namespace;
- educational/demo/artifact classification for article demos, standards experiments, bug repros, and historical references;
- blog/article/talk/spec/upstream-issue provenance links;
- package/download/dependent/adoption signals beyond stars;
- issue/PR responsiveness rather than open issue count alone;
- homepage health and canonicalization, not just presence;
- status/successor links for archived or legacy repos;
- portfolio signal-to-noise for accounts with hundreds of experiments;
- caution around non-English, older, or ecosystem-specific documentation conventions.

**Lesson:** `good-repo` should not confuse "missing modern OSS hygiene" with "low value." Some high-impact repos are historical demos, educational artifacts, or externally promoted tools. Score current repo effectiveness separately from historical impact, portfolio curation, and ecosystem centrality.

### 1. README presence is not the bottleneck

Every public repo had a README or README-like root file. The problem is not "no README." The problem is that many READMEs do not fully answer:

- Is this active or historical?
- Can I use it legally?
- Where is the live/demo/docs URL?
- What should a contributor do?
- What proof shows it works?

**Lesson:** the skill should not stop at README existence. It must assess README usefulness, accuracy, proof, and alignment with metadata.

### 2. GitHub metadata is the biggest systemic gap

Across the profile:

- **72 / 76** repos had no GitHub topics.
- **15 / 76** repos had no GitHub description.
- **69 / 76** had GitHub wiki enabled, often despite versioned docs/specs in the repo.

Many active repos have good code and decent READMEs but are effectively undiscoverable from GitHub search/category surfaces.

**Lesson:** topics, descriptions, homepage URLs, wiki settings, and social previews are first-class repo quality features, not polish.

### 3. License detection matters more than license claims

GitHub did not detect a license for **40 / 76** repos. Some repos claim MIT in README or `package.json`, but have no root `LICENSE` file.

Examples from the audit:

- `vaders` — README/package say MIT, but no root `LICENSE` detected.
- `good-pr` — README says MIT, but no root `LICENSE` detected.
- `flux-search` — public app repo with no detected license.

**Lesson:** assess license from GitHub detection and root files, not only README/package claims. A public reusable repo should have a root `LICENSE` unless intentionally all-rights-reserved.

### 4. Homepage URL alignment is a high-value check

The audit found multiple repos where a likely live/demo URL exists in README but GitHub's homepage metadata is missing.

Confirmed examples:

- `beautiful-mermaid` → candidate `https://adewale.github.io/beautiful-mermaid/`
- `bobbin` → candidate `https://bobbin.adewale-883.workers.dev`
- `garten` → candidate `https://adewale.github.io/garten/`
- `MaintainerBot` → candidate `https://maintainerbot-status.adewale-883.workers.dev/`
- `web2kindle` → candidate `https://web2kindle.megaconfidence.me/`
- `yaket` → candidate `https://adewale.github.io/yaket/`

The two requested test cases passed:

- `flux-search` README live URL matches GitHub homepage.
- `vaders` README play URL matches GitHub homepage.

**Lesson:** the skill should always compare README/package candidate URLs to GitHub `homepageUrl`. Missing homepage metadata is a discoverability bug.

### 5. Homepage detection needs precision

A naive scanner mistakes dependency docs, source articles, sponsor links, and third-party demos for project homepages. The owner-wide audit exposed false positives such as official framework docs and unrelated demo links.

We tightened the rule:

- Prefer `package.json.homepage`.
- Treat README links as candidates only when the label/context says live/demo/website/homepage/play/try.
- Ignore common non-homepage hosts: GitHub, X/Twitter, YouTube, OpenCollective, badge hosts.
- Require the URL to look project-owned: repo name, owner name/alias, or a project deployment path/domain.

**Lesson:** URL detection is not just regex; it is provenance and intent detection.

### 6. Forks need a different assessment model

There are **24** forks/reference repos. Many are old and not actively maintained. Scoring them like product repos is misleading.

For forks, the useful questions are:

- Is this fork active?
- Does it exist for a reason?
- Should it be archived?
- Does it clutter the public profile?
- Is the upstream project still visible as the source of truth?

**Lesson:** `good-repo` should classify forks early and apply a profile-hygiene rubric instead of the normal adoption rubric.

### 7. Legacy repos should be archived or status-labelled

Several 2012–2016 App Engine/Buzz-era repos are historical artifacts. They may be interesting, but without status notes they read as abandoned rather than intentionally preserved.

**Lesson:** stale public repos need one of:

- archived state,
- README status note,
- migration note,
- or deletion/private visibility if they no longer serve a public purpose.

### 8. Active Cloudflare apps are often strong but incomplete at the GitHub layer

Many recent repos are Cloudflare Workers/Pages apps with live URLs, CI, specs, and good docs. Their common gaps are metadata/governance, not code quality:

- no topics,
- missing root license,
- wiki enabled by default,
- no contribution guidance,
- homepage not always configured.

**Lesson:** for active app repos, a small metadata/governance pass can produce a large quality jump without touching code.

### 9. Skill repos need evals and scripts, not just references

The stronger skill repos follow the `good-pr` pattern:

```text
pain → checklist → template → filled example → script → evals
```

Many skill repos have `SKILL.md` and references, but no evals or CI around those evals.

**Lesson:** for skill repos, proof means worked examples and eval cases. A skill without evals is hard to regression-test.

### 10. Wiki defaults are noisy

GitHub wiki was enabled on most repos, but many already have versioned docs/specs. Unless a wiki is intentionally maintained, it is usually a confusing second documentation surface.

**Lesson:** assess GitHub feature toggles, not just files. Disable wiki by default when docs live in the repo.

## Highest-leverage cleanup sequence

For the `adewale` profile, the highest ROI cleanup order is:

1. **Add GitHub topics** to active non-fork repos.
2. **Add root `LICENSE` files** where reuse is intended or README/package claims a license.
3. **Set GitHub homepage URLs** for repos with live/demo URLs hidden in README.
4. **Disable unused wikis** where versioned docs/specs already exist.
5. **Archive or status-label stale legacy repos and inactive forks.**
6. **Add CI/evals** to active skill repos and small smoke CI to active apps/tools.
7. **Add `CONTRIBUTING.md`/PR templates** only where outside contributions are desired.

## What else should good-repo assess?

The current rubric covers front door, proof, adoption, docs, metadata, trust, governance, and automation. The profile-wide audit suggests additional axes worth adding or making more explicit.

### A. Repository intent and lifecycle

Assess whether the repo is:

- active product,
- experiment,
- fork/reference,
- historical artifact,
- template,
- private-but-public-by-accident,
- archived/maintenance-mode.

The expected quality bar depends on intent.

### B. Profile hygiene

For an owner/org, assess the portfolio, not just individual repos:

- stale forks cluttering the profile,
- duplicate/overlapping repos,
- old experiments without status notes,
- naming consistency,
- which repos deserve pinning,
- which repos should be archived.

### C. License consistency

Check all sources agree:

- GitHub detected license,
- root `LICENSE`,
- README license section,
- `package.json` / `pyproject.toml` / manifest license,
- third-party asset licenses.

### D. Deployment health

For live/demo URLs:

- URL is configured in GitHub homepage,
- URL returns 2xx/3xx,
- HTTPS works,
- app has a sensible title/OG card,
- demo still reflects current README.

### E. Security and privacy posture

Assess:

- secrets in history/diff risk,
- `.env.example` vs committed `.env`,
- security policy for packages/services,
- dependency vulnerability posture,
- auth/data handling notes,
- public data/model provenance.

### F. Supply-chain and package publication

For libraries/tools:

- package is published where README says it is,
- install command works,
- package name/exports/bin match README,
- lockfiles are intentional,
- dependency update policy exists,
- provenance/signing if relevant.

### G. Test quality, not just test presence

Use the `good-pr` lesson: tests must prove behavior.

Assess:

- regression tests fail before the fix,
- property/contract tests for invariant-heavy code,
- E2E tests for user flows,
- evals for agent skills,
- visual/screenshot tests for UI claims,
- mutation-style gaps or assertion-density smells.

### H. Accessibility and UX proof

For UI/web/game repos:

- screenshots include key states,
- keyboard/mobile/browser support is stated,
- accessibility basics are tested or documented,
- responsive behavior is proven,
- unsupported platforms are explicit.

### I. Maintenance burden

Assess whether the repo's public surfaces create work:

- issues enabled but unmonitored,
- discussions enabled with no community,
- dependency bots generating unactioned PRs,
- elaborate templates for tiny projects,
- CI too expensive/slow for the project.

Good repo quality includes sustainable maintainer load.

### J. Evidence freshness

Assess whether proof is fresh:

- screenshots match current UI,
- README commands match current scripts,
- version badges match manifest,
- generated artifacts can be regenerated,
- changelog/release notes align with latest tags.

## Changes made to good-repo after this audit

- Added owner-wide audit script: `skills/good-repo/scripts/audit-github-owner.py`.
- Tightened homepage URL detection to reduce false positives.
- Added homepage drift handling to the readiness script.
- Added repo quality/success feature model to `SKILL.md`.
- Added homepage drift as an explicit anti-pattern and checklist item.

## Skill repo structure lessons

After comparing Pi/Agent Skills documentation with `adewale` skill repos (`good-pr`, `good-readme`, `anti-slop-writing`, `python-workers-skill`, `slide-maker`, Cloudflare skills, and others), the optimal pattern is:

- Keep the installable runtime under `skills/<name>/`.
- Make `<name>` match `SKILL.md` frontmatter `name` even when a harness is lenient.
- Keep `SKILL.md` short, trigger-rich, and navigable; move depth into `references/`.
- Put runtime helper scripts inside `skills/<name>/scripts/`.
- Keep evals, reports, runbooks, CI, and contribution process outside the installable skill directory.
- Add `.claude-plugin/marketplace.json` for Claude/plugin distribution and `pi.skills` package metadata for Pi.
- Add evals for skill behavior; examples alone are not enough proof.

`good-repo` now follows this structure: runtime files live in `skills/good-repo/`; repo-only audits and lessons live in `docs/`; evals live in `evals/`; package/marketplace metadata lives at the root.

## Eval lessons for improving good-repo

The owner-wide audit and skill-structure work exposed a pattern: the hardest parts of `good-repo` are not file presence checks. They are judgment calls:

- Is this repo an active product, a historical artifact, or a fork/reference?
- Is a URL a real project homepage or just dependency documentation?
- Is a missing `LICENSE` a blocker or an intentional all-rights-reserved choice?
- Does a skill repo need a live demo, or would templates/scripts/evals be better proof?
- Is governance helpful or just process theater for a tiny repo?

Evals should improve the skill by locking in those judgments.

### What evals should test

1. **Triggering** — the skill should activate for repo audits, launch prep, GitHub metadata checks, owner-wide audits, homepage drift, skill repo structure, and README-vs-repo consistency.
2. **Classification before scoring** — forks, historical artifacts, app repos, skill repos, libraries, CLIs, and docs repos need different rubrics.
3. **Homepage URL precision** — catch true positives like `README Live: https://app.workers.dev` with blank GitHub homepage; reject false positives like links to Cloudflare docs, MDN, sponsors, tweets, or YouTube demos.
4. **License consistency** — README/package `MIT` without a root `LICENSE` and GitHub `licenseInfo` should be a trust gap.
5. **Skill repo layout** — directory/frontmatter name match, `skills/` plural, runtime references/scripts inside the skill, evals outside the installable folder, valid marketplace metadata.
6. **Actionability** — recommendations should name exact files/settings/commands, not generic "improve docs" advice.
7. **Proportionality** — do not recommend CODE_OF_CONDUCT, SECURITY.md, Dependabot, branch protection, and issue forms for every tiny experiment.
8. **Safety** — never mutate remote GitHub settings or add legal/governance files without approval.

### Eval types to add

- **Synthetic prompt evals** in `evals/evals.json` for small judgment cases. Added cases now cover skill layout, homepage false positives, fork/profile handling, governance overkill, license inconsistency, and missing skill evals.
- **Fixture repo evals** under a future `evals/fixtures/` directory for script-level tests. These should exercise `check-repo-readiness.sh` against tiny fake repos with known missing files/URLs.
- **Golden audit evals** for stable real repos with expected score bands and must-mention findings. Use bands, not exact scores, because GitHub metadata changes.
- **Adversarial false-positive evals** where the skill should refuse a generic recommendation: no homepage drift for third-party docs, no product-launch rubric for stale forks, no governance theater for personal experiments.
- **Baseline-vs-skill evals** to prove the skill adds value over generic repo advice. If the baseline passes every assertion, the eval is too weak.

### Eval quality rules

- Assertions must discriminate. "Mentions README" is weak; "flags GitHub homepageUrl is empty despite README `Live:` URL" is useful.
- Prefer behavior assertions over vocabulary assertions.
- Include negative cases; homepage detection especially needs false-positive pressure.
- Keep a holdout set for score calibration so the rubric does not overfit to `adewale` repos.
- When a real audit reveals a miss, add the failing eval first, then change the smallest rule or script.

The current eval plan is documented in `evals/README.md`. `evals/run_eval.py` now validates eval schemas, grades saved model outputs, and generates with-skill vs without-skill benchmark JSON. It deliberately does not call a model in CI; CI runs lightweight schema/assertion validation while real eval iterations save outputs under `eval-workspace/` and grade them offline.

### 2026-06-03 smoke eval

Before this smoke run, `good-repo` had validation but not real model-output evals. We ran three paired cases with `with_skill` and `without_skill` subagents in the same turn, following the core `skill-creator` pattern. Results are recorded in `docs/eval-results-2026-06-03.md`.

Findings:

- Homepage drift true positive passed with and without the skill. It is a useful regression guard but not a discriminator.
- Homepage false-positive avoidance also passed with and without the skill. It should stay as a guard, but future versions need harder ambiguity.
- Agent Skill layout was discriminating: with-skill recommended `skills/repo-auditor/SKILL.md`, evals outside runtime, and the `plugins` marketplace format; baseline missed the `skills/` convention and marketplace shape.

Lesson: evals should be split into **regression guards** and **skill-value discriminators**. A case where baseline passes is not useless, but it should not be counted as evidence that the skill adds value. The highest-yield eval area for `good-repo` is subtle ecosystem-specific judgment: skill packaging, owner/profile hygiene, homepage candidate precision, license detection consistency, and proportional governance.

### 2026-06-04 full behavior eval

The full `evals/evals.json` behavior suite was run with paired `with_skill` and `without_skill` outputs. Results are recorded in `docs/eval-results-2026-06-04.md`.

Results:

- `with_skill`: 44/44 assertions passed across 11 evals.
- `without_skill`: 39/44 assertions passed.
- Skill lift: +10.93 percentage points mean eval pass rate.

Baseline failures concentrated in three useful discriminator areas: Agent Skill layout, homepage false-positive avoidance, and popularity/adoption causality caveats. Many other evals passed on both sides and should remain regression guards, but future eval work needs harder cases.

Fixture-level evals were also added for mechanical checks: homepage drift, third-party docs false positives, missing license, bad skill layout, flat marketplace metadata, evals inside runtime skill, and skill directory/frontmatter mismatch.

## Trigger lessons

`good-repo` should trigger on the repo as a public/adoption surface, not on every task that happens inside a repo.

Strong triggers:

- repo quality, effectiveness, launch readiness, or success;
- GitHub metadata/settings: description, topics, homepage, wiki/issues/discussions, license, social preview;
- repo audits, owner-wide audits, score/recommendation tables;
- README/package/GitHub drift such as homepage URL or license inconsistency;
- adoption/trust gaps: quick start, proof, examples, CI, changelog, contribution path;
- Agent Skill repo structure, packaging, marketplace metadata, scripts, references, and evals;
- exemplar comparison against Hallmark, good-pr, good-readme, ripgrep, Flask, etc.

Near-misses should defer to narrower skills:

- README-only writing → `good-readme`;
- a single PR description or PR pre-submit review → `good-pr`;
- writing/improving code tests → `testing-best-practices`;
- ordinary code review with no repo-public-surface question → no `good-repo` trigger.

The decision rule: if the user's real question is "will a visitor/user/contributor trust, try, adopt, or contribute to this repo?" trigger `good-repo`. If the question is only about a document, PR, test, or code change, prefer the narrower specialist and use `good-repo` only for the repo-level wrapper.

These trigger boundaries are now encoded in `evals/trigger-queries.json`.

## Meta-lesson

A good repo is not merely a good README plus good code. It is a coherent public surface where README, GitHub metadata, live URLs, package metadata, docs, proof, license, CI, and maintainer intent all tell the same story.
