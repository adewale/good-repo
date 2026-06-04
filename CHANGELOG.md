# Changelog

All notable changes to `good-repo` will be documented here.

## 0.1.0 — 2026-06-03

- Initial skill scaffold.
- Added Hallmark-derived exemplar analysis.
- Added good-pr-derived exemplar analysis for small operational skill repos.
- Added repo readiness check script and skill eval cases, applying the good-pr pattern.
- Added CI validation for JSON, shell scripts, internal Markdown links, and readiness checks.
- Added owner-wide GitHub audit script and `github.com/adewale` assessment report.
- Added lessons learned document with additional repo assessment axes.
- Added skill repo best-practices reference and optimized package/marketplace structure.
- Added GitHub-official baseline reference covering README guidance, Community Profile files, metadata/topics/homepage, license, contribution templates, security policy, CI/workflows, and large-file hygiene.
- Added repo quality vs popularity/adoption research brief and runtime reference; stars/forks are now framed as noisy outcomes rather than intrinsic quality.
- Added multi-account signal assessment for high-activity GitHub profiles; expanded checklist axes for profile README, pinned/external repos, demo/tutorial/repro artifacts, provenance links, package adoption, responsiveness, homepage health, and portfolio signal-to-noise.
- Added focused GitHub Community Profile and Repolinter guidance; owner audits now include GitHub Community Profile health percentages when available.
- Added eval strategy documentation and expanded behavior eval cases for skill layout, homepage precision, forks, governance, license consistency, and skill-eval gaps.
- Added trigger policy to `SKILL.md` plus `evals/trigger-queries.json` for positive and near-negative activation cases.
- Ran first paired with-skill vs baseline smoke eval and documented results in `docs/eval-results-2026-06-03.md`.
- Updated eval strategy from Anthropic `skill-creator`: paired runs, assertion grading, non-discriminating assertion detection, benchmark/report loop.
- Added `evals/run_eval.py` for eval schema validation, saved-output assertion grading, and with-skill vs baseline benchmark generation; wired lightweight eval validation into CI.
- Added fixture repo tests for homepage drift, third-party docs false positives, missing license, singular skill layout, marketplace shape, runtime eval placement, and skill frontmatter/directory mismatch.
- Ran the full paired behavior eval suite; `with_skill` passed 44/44 assertions vs baseline 39/44, documented in `docs/eval-results-2026-06-04.md`.
- Added `.claude-plugin/marketplace.json` and Pi package metadata.
- Added 100-point repo effectiveness rubric.
- Added GitHub settings and automation checklist.
- Added repo anti-pattern reference and usage recipes.
