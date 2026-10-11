# Shared benchmark evals

This repo participates in the shared Skill Eval Harness:

- Repo: https://github.com/adewale/skill-eval-harness
- Version: `==0.6.0` (PyPI; the manifest's `harness.version` says the same)
- Manifest: `evals/shared-benchmark.json`

Install the pinned harness with [uv](https://docs.astral.sh/uv/):

```sh
uv tool install skill-eval-harness==0.6.0
```

CI runs the model-free gate against that pin on every push and pull request:

```sh
uvx --from skill-eval-harness==0.6.0 skill-benchmark validate --strict-leakage --check-ablations evals/shared-benchmark.json
uvx --from skill-eval-harness==0.6.0 skill-benchmark audit-manifest --fail-on-blockers evals/shared-benchmark.json
```

This manifest is the eval of record. `evals/evals.json` and `python3 evals/run_eval.py
grade|benchmark` are the frozen pre-harness suite behind
`docs/eval-results-2026-06-04.md`; see `evals/README.md` for why both still exist.

Splits:
- `tune` — visible iteration cases.
- `holdout` — hidden end-of-round / merge scoring cases.
- `holdback` — examples withheld from `SKILL.md`, references, docs, and public eval descriptions until after scoring.

Validate from this repo root:

```sh
skill-benchmark validate evals/shared-benchmark.json
```

Prepare paired run tasks:

```sh
skill-benchmark prepare evals/shared-benchmark.json --split tune --out /tmp/good-repo-tasks.jsonl
```

Include ablation variants when running a focused regression check:

```sh
skill-benchmark prepare evals/shared-benchmark.json --split tune --include-ablations --out /tmp/good-repo-ablation-tasks.jsonl
```

Run autonomous Pi trigger checks for trigger/no-trigger cases:

```sh
skill-pi-trigger-eval evals/shared-benchmark.json --split tune --out /tmp/good-repo-trigger-report.json
```

`old_skill` is optional and intentionally not emitted unless `old_skill_paths` is populated and `--include-old-skill` is passed. Hidden `holdout` / `holdback` prompt refs must be supplied privately before scoring; use `--allow-missing-prompts` only for dry-run planning.

Grade saved outputs:

```sh
skill-benchmark benchmark evals/shared-benchmark.json --runs eval-runs/latest --allow-scripts --out /tmp/good-repo-benchmark.json
```

Run optional qualitative judges through the shared `judge` backend:

```sh
skill-benchmark judge evals/shared-benchmark.json --runs eval-runs/latest --judge-cmd 'claude -p' --transcripts eval-runs/judge-transcripts --out /tmp/good-repo-judge-results.jsonl
skill-benchmark benchmark evals/shared-benchmark.json --runs eval-runs/latest --allow-scripts --judge-results /tmp/good-repo-judge-results.jsonl --out /tmp/good-repo-benchmark.json
```

Script assertions are deterministic repo-owned oracles and require `--allow-scripts` during grading.
