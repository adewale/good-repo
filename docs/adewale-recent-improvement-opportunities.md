# `github.com/adewale` — Recently Modified Repo Improvement Opportunities

Generated with `good-repo` after the 2026-06-04 eval/fixture updates.

Scope: public, non-fork repositories updated in the last 365 days.

## Summary

- Recently modified non-fork repos: **43**
- Below 60 / Weak-or-worse: **12**
- Below 75 / not yet Strong: **25**
- Missing GitHub topics: **38 / 43**
- Missing detected GitHub license: **21 / 43**
- Missing GitHub description: **10 / 43**
- Wiki enabled: **39 / 43**
- Homepage URL drift issues: **5**

## Highest-priority improvements

These are recently touched repos where small repo-surface work should produce the biggest quality lift.

| Priority | Repo | Score | Updated | Class | Main improvements |
| ---: | --- | ---: | --- | --- | --- |
| 1 | [`wwwoshineye`](https://github.com/adewale/wwwoshineye) | 24 | 2025-10-20 | website | Add topics; add root `LICENSE` or mark all-rights-reserved; add status/changelog note |
| 2 | [`fibonacci_durable_object`](https://github.com/adewale/fibonacci_durable_object) | 33 | 2025-12-04 | Cloudflare app/tool | Add topics; add changelog/status; clarify contribution policy |
| 3 | [`oshineye-dev`](https://github.com/adewale/oshineye-dev) | 42 | 2026-05-30 | Cloudflare app/tool | Add GitHub description; add topics; add root `LICENSE` or mark all-rights-reserved |
| 4 | [`swiss-poster-skill`](https://github.com/adewale/swiss-poster-skill) | 46 | 2026-06-01 | agent skill | Add topics; add changelog/status; clarify contribution policy |
| 5 | [`next-starter-template`](https://github.com/adewale/next-starter-template) | 50 | 2025-11-28 | Cloudflare app/tool | Add GitHub description; add topics; add root `LICENSE` |
| 6 | [`pi-comfort`](https://github.com/adewale/pi-comfort) | 50 | 2026-05-09 | agent skill | Add GitHub description; add topics; disable wiki if unused |
| 7 | [`good-pr`](https://github.com/adewale/good-pr) | 52 | 2026-03-18 | agent skill | Add topics; add root `LICENSE`; add `CONTRIBUTING.md` |
| 8 | [`testing-best-practices`](https://github.com/adewale/testing-best-practices) | 53 | 2026-06-01 | agent skill | Add topics; add root `LICENSE`; add `CONTRIBUTING.md` |
| 9 | [`skill_scanner`](https://github.com/adewale/skill_scanner) | 54 | 2026-05-21 | agent skill | Add topics; add root `LICENSE`; add `CONTRIBUTING.md` |
| 10 | [`cf-advisor-skill`](https://github.com/adewale/cf-advisor-skill) | 55 | 2025-12-18 | agent skill | Add GitHub description; add topics; disable wiki if unused |
| 11 | [`python-workers-skill`](https://github.com/adewale/python-workers-skill) | 57 | 2026-05-20 | agent skill | Add topics; add changelog/status; clarify contribution policy |
| 12 | [`good-readme`](https://github.com/adewale/good-readme) | 58 | 2026-03-21 | agent skill | Add topics; add `CONTRIBUTING.md`; add lightweight CI/smoke validation |

## Homepage drift quick wins

These should be fast GitHub settings fixes after confirming the URLs are canonical and live.

| Repo | Candidate homepage |
| --- | --- |
| [`web2kindle`](https://github.com/adewale/web2kindle) | `https://web2kindle.megaconfidence.me/` |
| [`MaintainerBot`](https://github.com/adewale/MaintainerBot) | `https://maintainerbot-status.adewale-883.workers.dev/` |
| [`garten`](https://github.com/adewale/garten) | `https://adewale.github.io/garten/` |
| [`bobbin`](https://github.com/adewale/bobbin) | `https://bobbin.adewale-883.workers.dev` |
| [`yaket`](https://github.com/adewale/yaket) | `https://adewale.github.io/yaket/` |

Example command pattern, after approval:

```sh
gh repo edit OWNER/REPO --homepage URL
```

## Profile-wide cleanup sequence

1. **Add topics to active repos** — 38 of 43 recently modified non-forks have no topics.
2. **Add/confirm root licenses** — 21 of 43 lack GitHub-detected licenses.
3. **Disable unused wikis** — 39 of 43 still have wiki enabled; prefer versioned docs in repo unless a wiki is intentionally maintained.
4. **Fix homepage drift** — set GitHub homepage for the 5 repos above.
5. **Patch active skill repos** — add root license, topics, `CONTRIBUTING.md`, CI/eval validation where missing.
6. **Add descriptions** — 10 active repos lack a concise GitHub description.

## Current `good-repo` status

`adewale/good-repo` now scores **85 / 100 — Strong** under the heuristic owner-audit script. The public repo has CI, fixture tests, eval schema validation, full behavior eval results, topics, license, and wiki disabled. The score is conservative because the heuristic does not yet award extra points for documented full behavior eval results or fixture coverage.
