# Repo Effectiveness Checklist & Scoring Rubric

Score a GitHub repo out of 100. Use evidence from files, commands, and GitHub metadata.

## Rating scale

| Score | Rating | Meaning |
| --- | --- | --- |
| 90–100 | Exemplary | Could be used as a model for its repo class |
| 75–89 | Strong | Effective, with minor gaps |
| 60–74 | Adequate | Usable, but adoption/trust gaps remain |
| 40–59 | Weak | Important surfaces missing or misleading |
| 0–39 | Poor | Hard to evaluate, run, or trust |

## Core success features

The 100-point score is a structured way to inspect ten success features:

1. Clear front door.
2. Proof that it works.
3. Fast adoption path.
4. Accurate documentation.
5. Trust signals.
6. Repo architecture that matches project class.
7. Automation and validation.
8. Contribution readiness.
9. Discoverability.
10. Focus, scope, and positioning.

A repo can score well before it has many stars. Stars are lagging indicators; these features are leading indicators. Use [`popularity-signals.md`](popularity-signals.md) when interpreting stars, forks, watchers, adoption, or growth claims.

## GitHub-official baseline

GitHub's own docs do not define a single repo score, but they do define a baseline through README guidance, Community Profile files, repository metadata, contributor templates, security policy, CI/workflows, and large-file limits. Use [`github-official-baseline.md`](github-official-baseline.md) when a recommendation should be tied to official GitHub documentation. Use [`community-profile-repolinter.md`](community-profile-repolinter.md) when reporting GitHub's official Community Profile health percentage or translating Repolinter-style policy findings.

## Additional diagnostic axes

Use these when the basic score is not enough:

- **Repository intent/lifecycle** — active product, experiment, fork/reference, historical artifact, template, maintenance mode.
- **Owner/profile hygiene** — profile README, pinned repos, pinned external/org repos, stale forks, duplicate repos, pinning candidates, archive candidates, naming consistency.
- **Portfolio signal-to-noise** — ratio of maintained projects to experiments, status notes on old repos, whether the owner's best/current work is easy to find.
- **License consistency** — GitHub detected license, root `LICENSE`, README, manifest, and asset licenses agree.
- **Deployment health** — live URL returns, HTTPS works, title/OG card exists, demo matches current README, sample/demo URLs are not mistaken for canonical homepages.
- **Provenance/context** — links to canonical article, talk, spec issue, upstream bug, successor repo, or historical status when the repo is a demo/tutorial/repro/artifact.
- **Security/privacy posture** — secrets risk, `.env.example`, security policy, dependency vulnerabilities, data/model provenance.
- **Supply-chain/package publication** — package exists, install command works, exports/bin match README, downloads/dependents where available, provenance/signing when relevant.
- **Test quality** — tests/evals prove behavior, not just existence; regression guards fail before the fix.
- **Accessibility/UX proof** — screenshots/states, keyboard/mobile/browser support, responsive behavior, unsupported platforms.
- **Contribution responsiveness** — time to first maintainer response, PR review latency, stale issue ratio, close/merge rate, and whether trackers redirect elsewhere.
- **Maintenance burden** — issues/discussions/bots/CI are sustainable for the maintainer.
- **Evidence freshness** — screenshots, commands, versions, generated assets, releases, and docs are current.

## Category 1: Front door + README — 20 pts

Use `good-readme` for detailed README analysis when available. Otherwise score:

| Criterion | Points | Good evidence |
| --- | ---: | --- |
| Ten-second clarity | 4 | First screen explains what the repo does |
| Value proposition | 4 | States why it matters or what problem it solves |
| Install / quick start | 4 | Minimal steps from clone/install to first success |
| Usage examples | 4 | Real, copy-pasteable examples with output or result |
| Honesty + scope | 2 | Limits, maturity, non-goals, or caveats when relevant |
| Scannability | 2 | Standard headings, lists/tables/code blocks, no wall of text |

Deduct for: badge soup, ghost README, vague tagline, pseudocode examples, stale screenshots, no license mention.

## Category 2: Proof + examples — 15 pts

| Criterion | Points | Good evidence |
| --- | ---: | --- |
| Visual/executable proof | 4 | Screenshot, GIF, live demo, terminal output, notebook, or sample response |
| Examples cover common paths | 4 | `examples/`, recipes, fixtures, or docs for primary use cases |
| Reproducible proof | 3 | Commands or files let users recreate demo/output |
| Contrasting cases | 2 | More than one scenario when repo claims breadth/variety |
| Proof is current | 2 | Assets match current code/version and are referenced correctly |

Class-specific notes:

- Visual/UI projects need screenshots or live demos.
- CLI tools need command output.
- Libraries need runnable snippets/tests.
- Skills need worked prompt/output examples; strong skill repos also include eval cases for expected behavior.

## Category 3: Adoption path + developer experience — 15 pts

| Criterion | Points | Good evidence |
| --- | ---: | --- |
| Prerequisites | 3 | Runtime versions, OS/platform, system deps, accounts/API keys |
| Install path | 3 | Package manager, binary, clone/build, or harness-specific install |
| Local run/dev path | 3 | From clone to running tests/server/examples |
| Manifest/package metadata | 3 | Name, version, description, license, exports/bin/entry points |
| Verification step | 3 | `--version`, test command, expected output, smoke check |

Deduct for hidden environment variables, package name mismatch, no `.env.example` for apps, no supported version statement.

## Category 4: Docs + repo architecture — 15 pts

| Criterion | Points | Good evidence |
| --- | ---: | --- |
| Structure fits project class | 4 | Files/folders match library/CLI/app/skill/docs norms |
| README routes to depth | 3 | Links to docs, examples, API, recipes without duplicating everything |
| Reference docs are organized | 3 | `docs/` or `references/` split by concern with clear index |
| Generated/test artifacts explained | 2 | Examples/tests/screenshots have purpose/provenance |
| Naming is predictable | 2 | Conventional names: `examples`, `docs`, `src`, `tests`, `skills` |
| No template debris | 1 | No empty TODO sections or unused boilerplate files |

## Category 5: GitHub metadata + discoverability — 10 pts

| Criterion | Points | Good evidence |
| --- | ---: | --- |
| Description | 2 | Clear GitHub repo description |
| Homepage | 2 | GitHub homepage URL is configured to the demo/docs/package URL when such a URL exists |
| Topics | 2 | 5–12 accurate discovery topics |
| Social preview | 2 | Useful OG image/screenshot for public projects |
| Repo features configured | 2 | Issues/discussions/wiki/projects enabled/disabled intentionally |

Use `gh repo view --json` when possible. If metadata cannot be inspected, list it as unknown and ask the user or provide manual settings.

**Homepage URL drift check:** if `README.md`, `package.json.homepage`, docs, or marketplace metadata contain a likely live/demo/docs/site URL, but GitHub `homepageUrl` is empty or different, score the homepage criterion low and flag the exact candidate URL to set.

## Category 6: Trust + governance + maintenance — 15 pts

| Criterion | Points | Good evidence |
| --- | ---: | --- |
| License clarity | 3 | LICENSE file and README/package agree |
| Changelog/release notes | 3 | `CHANGELOG.md` or GitHub Releases for versioned projects |
| Contribution path | 3 | `CONTRIBUTING.md`, PR template, issue guidance, test commands |
| Security/support | 2 | `SECURITY.md` or support channel when relevant |
| Community expectations | 1 | `CODE_OF_CONDUCT.md` when the public repo seeks a contributor community |
| Maintenance status | 2 | Roadmap, active issues, explicit alpha/beta/stable/maintenance mode |
| Ownership | 1 | Maintainers, CODEOWNERS, or clear issue/PR response expectations for larger repos |

Do not penalize tiny personal experiments for missing enterprise governance if the README clearly labels them as experiments.

## Category 7: Automation + release hygiene — 10 pts

| Criterion | Points | Good evidence |
| --- | ---: | --- |
| CI smoke test | 3 | Install/build/test/lint workflow appropriate to stack |
| Docs/link/eval validation | 2 | Link checker, markdown lint, examples validation, skill eval validation, or equivalent |
| Dependency maintenance | 2 | Dependabot/Renovate or documented manual process |
| Release process | 2 | Tags/releases, versioning, build artifacts, publish workflow |
| Branch safety | 1 | Branch protection or clear maintainer-only flow once CI exists |

Award partial credit for documented manual processes when automation is intentionally absent.

## Audit procedure

1. Read README and manifests first.
2. Classify repo type and maturity.
3. Inspect proof/examples/docs and `.github/`.
4. Inspect GitHub metadata if possible.
5. Score each category with one-line evidence.
6. Identify top 3 strengths and top 3 priority fixes.
7. Propose the smallest safe implementation plan.

## Output template

```markdown
## Repo Effectiveness Audit

**Project:** <name>
**Class:** <class>
**Score:** <N> / 100
**Rating:** <rating>

### Scores by category
| Category | Score | Max | Evidence |
| --- | ---: | ---: | --- |
| Front door + README |  | 20 |  |
| Proof + examples |  | 15 |  |
| Adoption + DX |  | 15 |  |
| Docs + architecture |  | 15 |  |
| GitHub metadata |  | 10 |  |
| Trust + governance |  | 15 |  |
| Automation + release |  | 10 |  |
| **Total** |  | 100 |  |

### Strengths
1. ...

### Priority improvements
1. ...
```

## Applying N/A judgments

Some criteria genuinely do not apply. Examples:

- No changelog for a pre-release prototype with no versions.
- No security policy for a toy personal script.
- No social preview for a private internal repo.
- No visual demo for a pure math library.

When a criterion is N/A, reallocate judgment within the same category only if the repo explicitly communicates why the surface is unnecessary. Silence is not the same as N/A.
