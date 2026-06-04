# Multi-Account Repo Quality Signal Assessment

Generated after scanning public repositories for:

- [`paulkinlan`](https://github.com/paulkinlan)
- [`jakearchibald`](https://github.com/jakearchibald)
- [`pbakaus`](https://github.com/pbakaus)
- [`chrischabot`](https://github.com/chrischabot)
- [`timothyjordan`](https://github.com/timothyjordan)
- [`fayazara`](https://github.com/fayazara)
- [`yusukebe`](https://github.com/yusukebe)

The scan used `good-repo`-style heuristics plus extra owner/profile signals: followers, pinned repos, profile README, stars/forks, topic/license/description/homepage/CI/contributing coverage, wiki defaults, activity, and top-star vs top-score mismatch.

Treat scores as triage signals, not final quality judgments. These accounts contain many historical demos, experiments, forks, and educational artifacts where normal product-readiness scoring can understate value.

## Summary table

| Owner | Public repos | Active last year | Median score | Stars total | Topics | License | Description | Homepage | CI | Contributing | Wiki enabled | Profile README |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `PaulKinlan` | 293 | 75 | 33 | 3,166 | 8/293 | 153/293 | 184/293 | 137/293 | 21/293 | 19/293 | 264/293 | No |
| `jakearchibald` | 253 | 58 | 35 | 23,633 | 0/253 | 112/253 | 154/253 | 78/253 | 24/253 | 35/253 | 218/253 | No |
| `pbakaus` | 25 | 18 | 47 | 40,567 | 0/25 | 21/25 | 23/25 | 8/25 | 5/25 | 2/25 | 23/25 | No |
| `chrischabot` | 76 | 36 | 45.5 | 12 | 6/76 | 52/76 | 67/76 | 8/76 | 11/76 | 3/76 | 62/76 | No |
| `timothyjordan` | 8 | 8 | 68 | 10 | 0/8 | 7/8 | 7/8 | 6/8 | 6/8 | 5/8 | 1/8 | No |
| `fayazara` | 167 | 92 | 49 | 3,797 | 11/167 | 61/167 | 103/167 | 64/167 | 43/167 | 7/167 | 129/167 | Yes |
| `yusukebe` | 360 | 107 | 31 | 5,477 | 17/360 | 67/360 | 201/360 | 87/360 | 45/360 | 7/360 | 339/360 | Yes |

## Account-level observations

### `paulkinlan`

Strong web-platform lab profile: many demos, experiments, historical web APIs, and live/homepage links. Current `good-repo` scoring catches missing topics, wiki defaults, and uneven README/license/CI coverage, but it under-models **blog/article provenance** and **experimental demo intent**. A repo can be useful as source for an article or browser experiment even when it is not a maintained product.

### `jakearchibald`

Very high social proof and several globally influential repos despite almost no GitHub topics. Examples: `idb`, `svgomg`, `idb-keyval`, service worker demos/tutorials. `good-repo` should not treat missing topics/CONTRIBUTING/CI as equivalent to lack of impact. This account exposes the need for an **educational/demo artifact** class and for separating **adoption impact** from **current repo hygiene**.

### `pbakaus`

Small portfolio with extreme concentration of popularity in `impeccable` and several older high-star UI/web libraries. Topics are absent across the account, but popularity remains high. This reinforces that topics are discoverability hygiene, not a guaranteed popularity driver. It also shows that **launch momentum and external promotion** are not captured by file-based quality checks.

### `chrischabot`

Low stars but many recent repos and decent description/license coverage. This is the inverse of high-star legacy accounts: current activity and project velocity are visible even when social proof is low. `good-repo` should avoid over-penalizing low-star portfolios when repos are active and clearly described.

### `timothyjordan`

Small, structured portfolio with high license/CI/contributing coverage but no topics. This shows that a small account can have better repo hygiene than high-star portfolios. Profile-scale assessment should value **portfolio focus** and **small-repo completeness**, not just aggregate stars.

### `fayazara`

Active modern web/Cloudflare/Vue portfolio with profile README and useful pinned repos, including an org repo outside the account namespace. `good-repo` currently misses **pinned external/org repos** as part of an individual's public portfolio. Many high-star repos are product demos/tools where external homepages and live app proof matter more than traditional OSS governance.

### `yusukebe`

Large long-lived account with profile README and major ecosystem impact through pinned org repos like `honojs/hono` and `honojs/honox`, which are not counted as owned repos by a simple owner audit. This is the clearest evidence that owner audits need **contributor/ecosystem centrality** beyond repos directly owned by the user.

## Star-score mismatch examples

Some repos have high stars but relatively modest hygiene scores. These are not necessarily bad repos; they reveal missing audit dimensions.

| Repo | Stars | Heuristic score | Why this matters |
| --- | ---: | ---: | --- |
| `jakearchibald/svgomg` | 6,179 | 56 | Strong live/product impact can coexist with missing topics/changelog/contribution docs. |
| `jakearchibald/idb-keyval` | 3,189 | 59 | Small utility libraries can become widely adopted with minimal governance. |
| `jakearchibald/sprite-cow` | 1,324 | 41 | Historical/live tool value may outlast current maintenance signals. |
| `fayazara/onelink` | 1,023 | 49 | Product/demo popularity can exceed repo-hygiene score; homepage candidate detection must avoid sample/generated demo URLs. |
| `yusukebe/gh-markdown-preview` | 846 | 53 | Developer utility adoption may be better measured by usage/downloads than repo files alone. |
| `jakearchibald/offline-wikipedia` | 826 | 54 | Archived/historical demos can remain high-value reference artifacts. |
| `pbakaus/viewporter` | 589 | 45 | Older web libraries need legacy/context classification before normal launch scoring. |
| `PaulKinlan/WebIntents` | 479 | 58 | Deprecated or historical web-platform projects can be important despite stale hygiene. |

## Quality signals good-repo was missing or underweighting

### 1. Profile README and pinned repos

Pinned repositories are the user's self-curated public portfolio. Profile README indicates intentional profile presentation. Owner audits should inspect:

- profile README exists and is current,
- pinned repos are active/high-quality or intentionally historical,
- pinned repos can belong to organizations, not just the user namespace,
- pinned repos align with the owner's current identity and best work.

### 2. Educational/demo/artifact classification

Many repos in these accounts are not products or libraries; they are:

- article demos,
- browser API experiments,
- conference/tutorial code,
- bug reproductions,
- proof-of-concept playgrounds,
- historical references.

These should be judged on status, provenance, demo link health, and explanation—not on full OSS governance.

### 3. Blog/article/provenance links

For developer-relations and web-platform accounts, a repo often exists to support an article, talk, video, or standards discussion. Quality signals include:

- README links to the canonical article/talk/spec issue,
- repo date/status matches the article era,
- demo still works or is marked historical,
- successor/canonical repo is linked.

### 4. External/org ecosystem impact

For maintainers like `yusukebe`, important work may live under orgs (`honojs/*`) rather than personal repos. Owner audits should include:

- pinned external repos,
- contributed-to/org-owned repos where the user is a maintainer,
- package ecosystem impact,
- follower/network context only as social proof, not quality.

### 5. Popularity as outcome, not score

High-star repos can have weak hygiene, and low-star repos can be well maintained. `good-repo` should continue separating:

- repo effectiveness score,
- popularity/social proof,
- adoption evidence,
- maintenance health.

### 6. Package and usage adoption

Stars are incomplete. For libraries/tools, better adoption signals include:

- npm/PyPI/CPAN/package publication,
- downloads or reverse dependencies,
- GitHub dependency graph dependents,
- browser extension/app store listings,
- live demo usage where available.

### 7. Issue and PR responsiveness

The scan measured open issue counts but not responsiveness. Better contribution-health signals:

- time to first maintainer response,
- PR review latency,
- stale issue ratio,
- close/merge rate,
- recent maintainer comments,
- whether issue tracker is intentionally disabled or redirected.

### 8. Homepage health and candidate precision

Presence is not enough. Need to check:

- homepage returns 2xx/3xx,
- HTTPS and redirect canonicalization,
- page title/OG metadata,
- demo matches repo/README,
- sample/generated demo URLs are not mistaken for canonical homepage URLs.

### 9. Intentional archival and successor links

Old repos should not all be "poor." High-quality historical repos should say:

- archived or historical,
- why it exists,
- whether it still works,
- successor/current canonical project,
- dependency/browser/runtime caveats.

### 10. Portfolio signal-to-noise

Large accounts accumulate hundreds of experiments. Owner-wide audits should score profile hygiene:

- ratio of active maintained repos to stale experiments,
- archive/status-note coverage,
- pinned repo quality,
- duplicate/overlapping repo cleanup,
- whether high-value repos are easy to find.

### 11. Template/repro scope

Small reproduction repos should not be expected to have full license/CI/contributing suites. They should have:

- clear bug/repro statement,
- exact command or deployed repro,
- linked issue/upstream bug,
- expected vs actual result,
- status/resolution.

### 12. Non-English and legacy-content tolerance

Long-lived accounts may have older docs, non-English docs, or ecosystem-specific conventions. A regex-heavy audit can under-score them. Manual audits should avoid assuming English headings are the only quality signal.

## Changes recommended for good-repo

1. Add owner-audit support for profile README and pinned repositories.
2. Add repo classes: `demo/tutorial`, `bug reproduction`, `historical artifact`, `standards/web-platform experiment`.
3. Add provenance checks: article/talk/spec/upstream issue links.
4. Add external adoption checks: package registry, downloads, dependents, app/browser listings where relevant.
5. Add issue/PR responsiveness metrics for maintained projects.
6. Add homepage health checks, not only homepage presence/alignment.
7. Add status/successor-link credit for old/archived repos.
8. Add portfolio signal-to-noise scoring for owner/org audits.
9. Keep topics as discoverability hygiene, but do not overstate their relationship to popularity.
