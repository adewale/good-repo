# Eval Results — 2026-06-04 Full Behavior Run

This run executed all prompt-level behavior evals in `evals/evals.json` using the skill-creator-inspired paired-output protocol.

Outputs and benchmark JSON were written under the ignored workspace:

```text
eval-workspace/iteration-4/behavior/<id>/{with_skill,without_skill}/output.md
eval-workspace/iteration-4/benchmark.json
```

## Protocol

- `with_skill`: subagent was instructed to read and follow `skills/good-repo/SKILL.md` plus relevant references.
- `without_skill`: subagent was instructed not to read or use `skills/good-repo/`.
- Both configurations were graded by `python3 evals/run_eval.py benchmark` against deterministic assertions in `evals/evals.json`.
- Fixture-level mechanical checks now run separately via `python3 evals/run_fixture_tests.py`.

## Results

| Configuration | Evals | Assertions | Passed | Failed | Mean eval pass rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| `with_skill` | 11 | 44 | 44 | 0 | 100.00% |
| `without_skill` | 11 | 44 | 39 | 5 | 89.07% |
| Delta | — | — | +5 | — | +10.93 pp |

## Baseline failures

The baseline missed five assertions:

1. **Eval 5 — Agent Skill layout**: did not recommend the standard `skills/repo-auditor` / `skills/` plural installable path.
2. **Eval 6 — Homepage false positive**: did not explicitly avoid flagging homepage drift for a third-party Cloudflare docs URL.
3. **Eval 6 — Third-party docs classification**: did not identify the link as dependency/platform/third-party docs.
4. **Eval 11 — Popularity metrics**: did not treat stars/forks/watchers as noisy outcome/social-proof signals.
5. **Eval 11 — Popularity confounders**: did not name major confounders such as age, ecosystem, language, domain, owner, or network effects.

## Non-discriminating evals

Several evals passed for both configurations. They remain useful as regression guards, but they are not evidence of skill lift in this run:

- Eval 1 — polished skill repo with no license/topics/evals/CI.
- Eval 2 — `good-pr` exemplar transfer.
- Eval 3 — avoid Hallmark cargo-culting.
- Eval 4 — homepage drift true positive.
- Eval 7 — owner profile with stale forks and active apps.
- Eval 8 — proportionate governance for tiny experiment repos.
- Eval 9 — README/package license claim with missing root `LICENSE`.
- Eval 10 — examples are not enough proof for skill behavior.

## Interpretation

The full behavior suite now passes with the skill. The strongest demonstrated lifts are ecosystem-specific judgments:

- Agent Skill packaging/layout conventions.
- Homepage-drift false-positive avoidance.
- Popularity/adoption causality caveats.

The suite still needs harder cases because the baseline passed most assertions. Future eval work should add more discriminating cases around ambiguous homepage candidates, package/adoption signals, org-owned pinned repos, historical demos, and issue/PR responsiveness.
