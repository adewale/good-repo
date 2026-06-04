# Sample Repo Effectiveness Audits

Small sample generated on 2026-06-03 using the `good-repo` rubric. This is a mixed/stratified sample rather than a statistically rigorous random sample: two user-provided test cases, two skill exemplars, two mature OSS tools/frameworks, one library, and one code-search-found repo used to exercise homepage URL drift detection.

## Summary table

| Repo | Class | Score | Rating | Homepage URL check | Top recommendation |
| --- | --- | ---: | --- | --- | --- |
| [`adewale/flux-search`](https://github.com/adewale/flux-search) | Cloudflare search app | 84 | Strong | README live URL matches GitHub homepage | Add root `LICENSE` + GitHub topics |
| [`adewale/vaders`](https://github.com/adewale/vaders) | TUI/web game | 87 | Strong | README play URL matches GitHub homepage | Add root `LICENSE`; fix README/package version drift |
| [`e3ntity/nonescape`](https://github.com/e3ntity/nonescape) | JS/Python ML library | 58 | Weak | **Live URL exists; GitHub homepage missing** | Set homepage to `https://www.nonescape.com` and add CI |
| [`nutlope/hallmark`](https://github.com/nutlope/hallmark) | Productized agent skill | 91 | Exemplary | Live demo matches GitHub homepage | Add topics + lightweight CI/contribution flow |
| [`adewale/good-pr`](https://github.com/adewale/good-pr) | Small operational agent skill | 82 | Strong | No homepage candidate; blank acceptable | Add root `LICENSE`, topics, CI for script/evals |
| [`BurntSushi/ripgrep`](https://github.com/BurntSushi/ripgrep) | CLI tool | 96 | Exemplary | No external homepage needed; blank acceptable | Minor: social preview / first-run quick path polish |
| [`pallets/flask`](https://github.com/pallets/flask) | Python web framework | 95 | Exemplary | Docs homepage configured | Minor: keep README routing aligned with docs |
| [`sindresorhus/ky`](https://github.com/sindresorhus/ky) | JS HTTP client library | 81 | Strong | No clear homepage candidate; blank acceptable | Move sponsor block below project pitch / install path |

## Detailed findings

### adewale/flux-search — 84 / 100 · Strong

**Evidence:** clear README, live app link, Cloudflare deploy button, detailed search language, quick start, architecture docs, CI, changelog, many scripts/specs.

**Category sketch:** Front door 18/20 · Proof 13/15 · Adoption 14/15 · Docs/architecture 14/15 · Metadata 6/10 · Trust 9/15 · Automation 10/10.

**Strengths**

1. Strong first-screen value: search every issue of The FLUX Review with hybrid lexical + semantic search.
2. Adoption path is concrete: prerequisites, D1/Vectorize setup, migrations, local dev, bootstrap, corpus pipeline.
3. CI validates corpus processing, tests, and typecheck.

**Recommendations**

1. Add a root `LICENSE` and align README/package metadata.
2. Add GitHub topics: `cloudflare-workers`, `search`, `newsletter`, `semantic-search`, `d1`, `vectorize`, `hono`, `typescript`.
3. Add `CONTRIBUTING.md` or a short contributor section if outside PRs are welcome.
4. Add `.dev.vars.example` and a Cloudflare services/free-tier table.
5. Add a screenshot/social preview so the search UI is visible before clicking through.

**Homepage URL check:** pass. README exposes `https://flux-search.adewale-883.workers.dev/`; GitHub homepage is configured to the same URL.

---

### adewale/vaders — 87 / 100 · Strong

**Evidence:** strong README, screenshots, live browser link, terminal run path, controls table, architecture summary, specs/docs, changelog, extensive CI including unit, contracts, E2E, build, spritesheet generation.

**Category sketch:** Front door 19/20 · Proof 15/15 · Adoption 14/15 · Docs/architecture 14/15 · Metadata 6/10 · Trust 9/15 · Automation 10/10.

**Strengths**

1. Excellent proof: launch/gameplay screenshots, live app, TUI and browser paths.
2. Clear project scope: keyboard-only, desktop browser support, mobile/touch out of scope.
3. Exceptional validation stack: workspace tests, platform-boundary grep checks, E2E tests, deployment coherence, spritesheet freshness.

**Recommendations**

1. Add root `LICENSE`; README/package claim MIT but GitHub does not detect a license.
2. Fix README/package version drift: README badge says `1.1.0`, `package.json` says `1.1.1`.
3. Add GitHub topics: `opentui`, `cloudflare-workers`, `durable-objects`, `multiplayer`, `space-invaders`, `bun`, `typescript`, `game`.
4. Disable GitHub wiki unless intentionally used; repo already has versioned docs/specs.
5. Add `CONTRIBUTING.md` and issue/PR templates if public contributions are desired.

**Homepage URL check:** pass. README exposes `https://vaders.adewale-883.workers.dev`; GitHub homepage is configured to the same URL.

---

### e3ntity/nonescape — 58 / 100 · Weak

**Evidence:** root README is concise and links JS/Python APIs, live demo, model weights, and license. Has `LICENSE`, package-specific READMEs, examples. Missing GitHub homepage, topics, CI, changelog, contribution guidance, and a stronger root adoption path.

**Category sketch:** Front door 13/20 · Proof 8/15 · Adoption 10/15 · Docs/architecture 9/15 · Metadata 3/10 · Trust 7/15 · Automation 0/10.

**Strengths**

1. Clear project idea: AI-generated image detection for JavaScript and Python.
2. Live demo exists and model weights are linked.
3. Separate JS and Python README files provide API examples.

**Recommendations**

1. **Configure GitHub homepage:** README says live demo is `https://www.nonescape.com`, but GitHub `homepageUrl` is empty.
2. Add GitHub topics: `ai-detection`, `deepfake-detection`, `computer-vision`, `javascript`, `python`, `onnx`, `image-classification`.
3. Add CI for JS build/tests and Python import/example smoke tests.
4. Expand root README with a two-path quick start: JavaScript and Python.
5. Add `CHANGELOG.md`, `CONTRIBUTING.md`, and package publication/version notes.

**Homepage URL check:** fail. Candidate homepage URL found in README (`https://www.nonescape.com`), but GitHub homepage is not configured.

---

### nutlope/hallmark — 91 / 100 · Exemplary

**Evidence:** concise README, live demo, screenshot grid, install command, four verbs, package skill metadata, modular references, docs/recipes/study examples, site tests, roadmap, license.

**Category sketch:** Front door 20/20 · Proof 15/15 · Adoption 14/15 · Docs/architecture 15/15 · Metadata 6/10 · Trust 13/15 · Automation 7/10.

**Strengths**

1. Proof-first presentation: live site, screenshots, generated pages, recipes.
2. Skill architecture is excellent: `SKILL.md` plus modular references and examples.
3. Strong product language: 22 themes, four verbs, slop gates, project memory, roadmap.

**Recommendations**

1. Add GitHub topics: `skill`, `claude-code`, `cursor`, `codex`, `design-system`, `frontend`, `ai-agents`.
2. Add lightweight CI for skill metadata, package JSON, internal links, and deploy/static-site sanity.
3. Add `CONTRIBUTING.md` and PR template for outside improvements.
4. Consider `CHANGELOG.md` or GitHub Releases for versioned skill changes.

**Homepage URL check:** pass. README live demo and GitHub homepage both point to `https://www.usehallmark.com/`.

---

### adewale/good-pr — 82 / 100 · Strong

**Evidence:** strong README origin story, tight scope, install/usage, `SKILL.md`, references for PR template/checklist/example, readiness script, evals, changelog. Missing detected license, topics, CI, contribution path.

**Category sketch:** Front door 18/20 · Proof 12/15 · Adoption 12/15 · Docs/architecture 13/15 · Metadata 4/10 · Trust 8/15 · Automation 7/10.

**Strengths**

1. Narrow and memorable job: help contributors craft PRs maintainers want to merge.
2. Excellent operational artifacts: template, filled example, checklist, script.
3. Evals encode non-obvious skill behavior such as regression-test quality and visual evidence requirements.

**Recommendations**

1. Add root `LICENSE`; README says MIT but GitHub does not detect one.
2. Add GitHub topics: `pull-requests`, `open-source`, `claude-code`, `skill`, `code-review`, `contributing`.
3. Add CI to validate `evals/evals.json` and shell syntax for `check-pr-readiness.sh`.
4. Add minimal `CONTRIBUTING.md` and PR template — especially fitting for this repo's subject.
5. Add package/marketplace metadata if distribution beyond Claude plugin is desired.

**Homepage URL check:** no candidate homepage URL; blank GitHub homepage is acceptable.

---

### BurntSushi/ripgrep — 96 / 100 · Exemplary

**Evidence:** clear README, release downloads, install instructions across platforms, guide/FAQ/changelog, license files, contributing, CI, tests/benches/fuzzing, excellent topics.

**Category sketch:** Front door 19/20 · Proof 14/15 · Adoption 15/15 · Docs/architecture 15/15 · Metadata 9/10 · Trust 15/15 · Automation 10/10.

**Strengths**

1. Ten-second clarity: recursively searches directories while respecting gitignore.
2. Mature adoption path: release binaries, install docs, guide, FAQ, shell completion docs.
3. Deep trust signals: changelog, contributing, dual license, CI, tests, fuzz/bench infrastructure.

**Recommendations**

1. Optional social preview or first-screen visual/terminal example for link shares.
2. Keep README from becoming too long by continuing to route depth to `GUIDE.md` and `FAQ.md`.

**Homepage URL check:** no external homepage candidate; blank GitHub homepage is acceptable.

---

### pallets/flask — 95 / 100 · Exemplary

**Evidence:** GitHub description and homepage configured, focused README, simple example, docs site, examples, tests, license, changes, pyproject, strong topics.

**Category sketch:** Front door 18/20 · Proof 13/15 · Adoption 15/15 · Docs/architecture 15/15 · Metadata 10/10 · Trust 15/15 · Automation 9/10.

**Strengths**

1. Clear positioning: lightweight WSGI web application framework.
2. Good progressive path: simple example in README, deep docs at configured homepage.
3. Mature repo structure: docs, examples, tests, changelog, license, pyproject.

**Recommendations**

1. Keep README routing crisp; avoid duplicating the docs site.
2. Ensure social preview and docs homepage stay current as docs branding evolves.

**Homepage URL check:** pass. GitHub homepage is `https://flask.palletsprojects.com`.

---

### sindresorhus/ky — 81 / 100 · Strong

**Evidence:** strong package metadata, license, tests, topics, code examples, mature maintainer conventions. First-screen README is dominated by sponsor/logo content before the product pitch and install path.

**Category sketch:** Front door 13/20 · Proof 10/15 · Adoption 14/15 · Docs/architecture 13/15 · Metadata 8/10 · Trust 14/15 · Automation 9/10.

**Strengths**

1. Strong ecosystem fit: tiny Fetch-based HTTP client with npm/package metadata and topics.
2. Long README covers usage in depth.
3. Tests, license, source layout, and package conventions are mature.

**Recommendations**

1. Move sponsor block below the project pitch/install path; the first screen should answer what/why/how before sponsorship.
2. Add a short top-level quick start before the long advanced usage sections.
3. If there is a canonical docs/package URL, configure GitHub homepage; otherwise blank is acceptable because README is the docs.

**Homepage URL check:** no clear homepage candidate; blank GitHub homepage is acceptable.
