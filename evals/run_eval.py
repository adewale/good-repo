#!/usr/bin/env python3
"""Validate and grade good-repo evals.

This runner borrows the useful mechanics from Anthropic's skill-creator loop
without requiring model access in CI:

- validate eval/trigger schemas and skill-name alignment;
- grade saved model outputs against concrete assertions;
- compare paired with-skill vs without-skill outputs into a benchmark JSON.

It intentionally does not call an LLM. Generate outputs with your agent harness,
save them under eval-workspace, then use this script to grade and summarize.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SUPPORTED_ASSERTIONS = {
    "content_includes_any",
    "content_includes_all",
    "content_excludes_any",
    "regex_includes",
    "regex_excludes",
}
CONFIGURATIONS = ("with_skill", "without_skill")


@dataclass
class ValidationResult:
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


@dataclass
class AssertionResult:
    description: str
    assertion_type: str
    passed: bool
    evidence: str


@dataclass
class EvalGrade:
    eval_id: str
    configuration: str
    output_path: str | None
    passed: int
    failed: int
    total: int
    pass_rate: float
    assertions: list[AssertionResult]


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{path}: invalid JSON: {exc}") from exc


def read_skill_name(skill_path: Path) -> str | None:
    if not skill_path.exists():
        return None
    text = skill_path.read_text()
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    for line in parts[1].splitlines():
        if line.strip().startswith("name:"):
            return line.split(":", 1)[1].strip().strip('"\'')
    return None


def add_error(errors: list[str], path: str, message: str) -> None:
    errors.append(f"{path}: {message}")


def assert_nonempty_string(errors: list[str], path: str, value: Any) -> None:
    if not isinstance(value, str) or not value.strip():
        add_error(errors, path, "must be a non-empty string")


def validate_behavior_evals(evals_path: Path, skill_name: str | None) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    data = load_json(evals_path)

    if not isinstance(data, dict):
        add_error(errors, str(evals_path), "top-level value must be an object")
        return ValidationResult(errors, warnings)

    assert_nonempty_string(errors, "skill_name", data.get("skill_name"))
    if skill_name and data.get("skill_name") != skill_name:
        add_error(errors, "skill_name", f"must match SKILL.md name {skill_name!r}")

    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        add_error(errors, "evals", "must be a non-empty list")
        return ValidationResult(errors, warnings)

    seen_ids: set[str] = set()
    for index, item in enumerate(evals):
        prefix = f"evals[{index}]"
        if not isinstance(item, dict):
            add_error(errors, prefix, "must be an object")
            continue
        raw_id = item.get("id")
        eval_id = str(raw_id)
        if raw_id is None or not eval_id.strip():
            add_error(errors, f"{prefix}.id", "is required")
        elif eval_id in seen_ids:
            add_error(errors, f"{prefix}.id", f"duplicate id {eval_id!r}")
        else:
            seen_ids.add(eval_id)

        assert_nonempty_string(errors, f"{prefix}.prompt", item.get("prompt"))
        assert_nonempty_string(errors, f"{prefix}.expected_output", item.get("expected_output"))

        files = item.get("files", [])
        if not isinstance(files, list):
            add_error(errors, f"{prefix}.files", "must be a list when present")
        else:
            for file_index, rel in enumerate(files):
                if not isinstance(rel, str) or not rel.strip():
                    add_error(errors, f"{prefix}.files[{file_index}]", "must be a non-empty path string")
                    continue
                if rel.startswith("/"):
                    add_error(errors, f"{prefix}.files[{file_index}]", "must be relative, not absolute")
                    continue
                if not (evals_path.parent / rel).exists() and not Path(rel).exists():
                    add_error(errors, f"{prefix}.files[{file_index}]", f"referenced file does not exist: {rel}")

        assertions = item.get("assertions")
        if not isinstance(assertions, list) or not assertions:
            add_error(errors, f"{prefix}.assertions", "must be a non-empty list")
            continue
        if len(assertions) < 2:
            warnings.append(f"{prefix}: has only one assertion; weak evals often pass by accident")

        for assertion_index, assertion in enumerate(assertions):
            ap = f"{prefix}.assertions[{assertion_index}]"
            if not isinstance(assertion, dict):
                add_error(errors, ap, "must be an object")
                continue
            atype = assertion.get("type")
            if atype not in SUPPORTED_ASSERTIONS:
                add_error(errors, f"{ap}.type", f"unsupported assertion type {atype!r}")
            value = assertion.get("value")
            if atype in {"content_includes_any", "content_includes_all", "content_excludes_any"}:
                if not isinstance(value, list) or not value or not all(isinstance(v, str) and v for v in value):
                    add_error(errors, f"{ap}.value", "must be a non-empty list of non-empty strings")
            elif atype in {"regex_includes", "regex_excludes"}:
                if not isinstance(value, str) or not value:
                    add_error(errors, f"{ap}.value", "must be a non-empty regex string")
                else:
                    try:
                        re.compile(value)
                    except re.error as exc:
                        add_error(errors, f"{ap}.value", f"invalid regex: {exc}")
            assert_nonempty_string(errors, f"{ap}.description", assertion.get("description"))

            if isinstance(assertion.get("description"), str):
                desc_words = assertion["description"].split()
                if len(desc_words) < 4:
                    warnings.append(f"{ap}.description: very short descriptions are hard to review")

    return ValidationResult(errors, warnings)


def validate_trigger_queries(trigger_path: Path, skill_name: str | None) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    data = load_json(trigger_path)

    if not isinstance(data, dict):
        add_error(errors, str(trigger_path), "top-level value must be an object")
        return ValidationResult(errors, warnings)

    assert_nonempty_string(errors, "skill_name", data.get("skill_name"))
    if skill_name and data.get("skill_name") != skill_name:
        add_error(errors, "skill_name", f"must match SKILL.md name {skill_name!r}")
    assert_nonempty_string(errors, "description", data.get("description"))

    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        add_error(errors, "cases", "must be a non-empty list")
        return ValidationResult(errors, warnings)

    seen_ids: set[str] = set()
    positives = 0
    negatives = 0
    for index, item in enumerate(cases):
        prefix = f"cases[{index}]"
        if not isinstance(item, dict):
            add_error(errors, prefix, "must be an object")
            continue
        case_id = item.get("id")
        assert_nonempty_string(errors, f"{prefix}.id", case_id)
        if isinstance(case_id, str):
            if case_id in seen_ids:
                add_error(errors, f"{prefix}.id", f"duplicate id {case_id!r}")
            seen_ids.add(case_id)
        assert_nonempty_string(errors, f"{prefix}.prompt", item.get("prompt"))
        assert_nonempty_string(errors, f"{prefix}.reason", item.get("reason"))
        should_trigger = item.get("should_trigger")
        if not isinstance(should_trigger, bool):
            add_error(errors, f"{prefix}.should_trigger", "must be boolean")
        elif should_trigger:
            positives += 1
        else:
            negatives += 1
            preferred = item.get("preferred_skill")
            if preferred is not None and (not isinstance(preferred, str) or not preferred.strip()):
                add_error(errors, f"{prefix}.preferred_skill", "must be a non-empty string when present")

    if positives == 0:
        add_error(errors, "cases", "must include at least one positive trigger case")
    if negatives == 0:
        add_error(errors, "cases", "must include at least one negative trigger case")
    if positives and negatives and min(positives, negatives) / max(positives, negatives) < 0.4:
        warnings.append(f"trigger set is imbalanced: {positives} positive vs {negatives} negative cases")

    return ValidationResult(errors, warnings)


def normalize_text(text: str, *, case_sensitive: bool) -> str:
    return text if case_sensitive else text.lower()


def evaluate_assertion(output: str, assertion: dict[str, Any]) -> AssertionResult:
    atype = assertion["type"]
    value = assertion["value"]
    description = assertion["description"]
    case_sensitive = bool(assertion.get("case_sensitive", False))
    haystack = normalize_text(output, case_sensitive=case_sensitive)

    def norm(v: str) -> str:
        return normalize_text(v, case_sensitive=case_sensitive)

    if atype == "content_includes_any":
        matched = [v for v in value if norm(v) in haystack]
        return AssertionResult(
            description=description,
            assertion_type=atype,
            passed=bool(matched),
            evidence=f"matched any: {matched}" if matched else f"none of {value!r} found",
        )
    if atype == "content_includes_all":
        missing = [v for v in value if norm(v) not in haystack]
        return AssertionResult(
            description=description,
            assertion_type=atype,
            passed=not missing,
            evidence=f"all terms found: {value}" if not missing else f"missing: {missing}",
        )
    if atype == "content_excludes_any":
        found = [v for v in value if norm(v) in haystack]
        return AssertionResult(
            description=description,
            assertion_type=atype,
            passed=not found,
            evidence=f"excluded terms absent: {value}" if not found else f"unexpected terms found: {found}",
        )
    if atype == "regex_includes":
        flags = 0 if case_sensitive else re.IGNORECASE
        match = re.search(value, output, flags)
        return AssertionResult(
            description=description,
            assertion_type=atype,
            passed=bool(match),
            evidence=f"matched regex: {match.group(0)!r}" if match else f"regex not found: {value}",
        )
    if atype == "regex_excludes":
        flags = 0 if case_sensitive else re.IGNORECASE
        match = re.search(value, output, flags)
        return AssertionResult(
            description=description,
            assertion_type=atype,
            passed=not match,
            evidence=f"regex absent: {value}" if not match else f"unexpected regex match: {match.group(0)!r}",
        )
    raise ValueError(f"unsupported assertion type: {atype}")


def output_candidates(
    outputs_dir: Path,
    eval_id: str,
    configuration: str,
    *,
    include_unconfigured: bool,
) -> list[Path]:
    padded = eval_id.zfill(3) if eval_id.isdigit() else eval_id
    names = [eval_id]
    if padded not in names:
        names.append(padded)
    candidates: list[Path] = []
    for name in names:
        candidates.extend(
            [
                outputs_dir / name / configuration / "output.md",
                outputs_dir / name / configuration / "outputs" / "output.md",
                outputs_dir / name / configuration / "outputs" / "final.md",
            ]
        )
        if include_unconfigured:
            candidates.extend(
                [
                    outputs_dir / name / "output.md",
                    outputs_dir / name / "outputs" / "output.md",
                    outputs_dir / f"{name}.md",
                ]
            )
    return candidates


def find_output(
    outputs_dir: Path,
    eval_id: str,
    configuration: str,
    *,
    include_unconfigured: bool = True,
) -> Path | None:
    for candidate in output_candidates(
        outputs_dir,
        eval_id,
        configuration,
        include_unconfigured=include_unconfigured,
    ):
        if candidate.exists():
            return candidate
    return None


def grade_eval(item: dict[str, Any], output: str, output_path: Path | None, configuration: str) -> EvalGrade:
    assertion_results = [evaluate_assertion(output, assertion) for assertion in item["assertions"]]
    passed = sum(1 for result in assertion_results if result.passed)
    total = len(assertion_results)
    failed = total - passed
    return EvalGrade(
        eval_id=str(item["id"]),
        configuration=configuration,
        output_path=str(output_path) if output_path else None,
        passed=passed,
        failed=failed,
        total=total,
        pass_rate=passed / total if total else 0.0,
        assertions=assertion_results,
    )


def grade_outputs(
    evals_path: Path,
    outputs_dir: Path,
    configuration: str,
    allow_missing: bool,
    *,
    include_unconfigured: bool = True,
) -> list[EvalGrade]:
    data = load_json(evals_path)
    grades: list[EvalGrade] = []
    for item in data["evals"]:
        eval_id = str(item["id"])
        output_path = find_output(outputs_dir, eval_id, configuration, include_unconfigured=include_unconfigured)
        if output_path is None:
            if allow_missing:
                continue
            assertions = [
                AssertionResult(
                    description=a.get("description", "<missing description>"),
                    assertion_type=a.get("type", "<missing type>"),
                    passed=False,
                    evidence=f"missing output for eval {eval_id} under {outputs_dir}",
                )
                for a in item.get("assertions", [])
            ]
            total = len(assertions)
            grades.append(
                EvalGrade(
                    eval_id=eval_id,
                    configuration=configuration,
                    output_path=None,
                    passed=0,
                    failed=total,
                    total=total,
                    pass_rate=0.0,
                    assertions=assertions,
                )
            )
            continue
        grades.append(grade_eval(item, output_path.read_text(errors="replace"), output_path, configuration))
    return grades


def summarize_grades(grades: list[EvalGrade]) -> dict[str, Any]:
    total_assertions = sum(g.total for g in grades)
    passed = sum(g.passed for g in grades)
    failed = sum(g.failed for g in grades)
    return {
        "evals": len(grades),
        "assertions": total_assertions,
        "passed": passed,
        "failed": failed,
        "pass_rate": passed / total_assertions if total_assertions else 0.0,
    }


def print_grade_table(grades: list[EvalGrade]) -> None:
    print("| Eval | Config | Pass rate | Passed | Failed | Output |")
    print("| --- | --- | ---: | ---: | ---: | --- |")
    for grade in grades:
        output = grade.output_path or "missing"
        print(
            f"| {grade.eval_id} | {grade.configuration} | {grade.pass_rate:.2%} | "
            f"{grade.passed} | {grade.failed} | {output} |"
        )
    summary = summarize_grades(grades)
    print()
    print(
        f"Summary: {summary['passed']}/{summary['assertions']} assertions passed "
        f"({summary['pass_rate']:.2%}) across {summary['evals']} eval outputs."
    )


def mean(values: list[float]) -> float:
    return statistics.mean(values) if values else 0.0


def stddev(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    return statistics.pstdev(values)


def stat_block(values: list[float]) -> dict[str, float]:
    if not values:
        return {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0}
    return {"mean": mean(values), "stddev": stddev(values), "min": min(values), "max": max(values)}


def benchmark(evals_path: Path, outputs_dir: Path, allow_missing: bool) -> dict[str, Any]:
    data = load_json(evals_path)
    eval_ids = [str(item["id"]) for item in data["evals"]]
    runs: list[dict[str, Any]] = []
    by_config: dict[str, list[EvalGrade]] = {}

    for configuration in CONFIGURATIONS:
        grades = grade_outputs(
            evals_path,
            outputs_dir,
            configuration,
            allow_missing=allow_missing,
            include_unconfigured=False,
        )
        by_config[configuration] = grades
        for grade in grades:
            runs.append(
                {
                    "eval_id": grade.eval_id,
                    "configuration": configuration,
                    "run_number": 1,
                    "result": {
                        "pass_rate": grade.pass_rate,
                        "passed": grade.passed,
                        "failed": grade.failed,
                        "total": grade.total,
                        "errors": 0 if grade.output_path else 1,
                    },
                    "expectations": [
                        {
                            "text": assertion.description,
                            "type": assertion.assertion_type,
                            "passed": assertion.passed,
                            "evidence": assertion.evidence,
                        }
                        for assertion in grade.assertions
                    ],
                }
            )

    run_summary: dict[str, Any] = {}
    for configuration, grades in by_config.items():
        pass_rates = [g.pass_rate for g in grades]
        run_summary[configuration] = {
            "pass_rate": stat_block(pass_rates),
            "evals": len(grades),
            "assertions": sum(g.total for g in grades),
            "passed": sum(g.passed for g in grades),
            "failed": sum(g.failed for g in grades),
        }

    with_mean = run_summary.get("with_skill", {}).get("pass_rate", {}).get("mean", 0.0)
    without_mean = run_summary.get("without_skill", {}).get("pass_rate", {}).get("mean", 0.0)
    run_summary["delta"] = {"pass_rate": with_mean - without_mean}

    notes: list[str] = []
    with_by_id = {g.eval_id: g for g in by_config.get("with_skill", [])}
    without_by_id = {g.eval_id: g for g in by_config.get("without_skill", [])}
    for eval_id in eval_ids:
        with_grade = with_by_id.get(eval_id)
        without_grade = without_by_id.get(eval_id)
        if not with_grade or not without_grade:
            notes.append(f"Eval {eval_id} is missing one side of the with_skill/without_skill comparison.")
            continue
        if math.isclose(with_grade.pass_rate, 1.0) and math.isclose(without_grade.pass_rate, 1.0):
            notes.append(f"Eval {eval_id} passes 100% for both configurations; useful regression guard but not a discriminator.")
        elif with_grade.pass_rate <= without_grade.pass_rate:
            notes.append(
                f"Eval {eval_id} does not show a with-skill lift "
                f"({with_grade.pass_rate:.2%} vs {without_grade.pass_rate:.2%}); inspect assertion quality or skill behavior."
            )

    return {
        "metadata": {
            "skill_name": data.get("skill_name"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "evals_run": eval_ids,
            "runs_per_configuration": 1,
            "outputs_dir": str(outputs_dir),
        },
        "runs": runs,
        "run_summary": run_summary,
        "notes": notes,
    }


def command_validate(args: argparse.Namespace) -> int:
    skill_name = read_skill_name(args.skill)
    behavior = validate_behavior_evals(args.evals, skill_name)
    triggers = validate_trigger_queries(args.triggers, skill_name)
    errors = behavior.errors + triggers.errors
    warnings = behavior.warnings + triggers.warnings

    if warnings and not args.quiet:
        print("Warnings:", file=sys.stderr)
        for warning in warnings:
            print(f"  - {warning}", file=sys.stderr)
    if errors:
        print("Errors:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    if not args.quiet:
        print("Eval schemas OK")
        if skill_name:
            print(f"Skill name: {skill_name}")
    return 0


def command_grade(args: argparse.Namespace) -> int:
    grades = grade_outputs(args.evals, args.outputs_dir, args.configuration, allow_missing=args.allow_missing)
    if args.json:
        payload = {
            "summary": summarize_grades(grades),
            "grades": [
                {
                    "eval_id": g.eval_id,
                    "configuration": g.configuration,
                    "output_path": g.output_path,
                    "passed": g.passed,
                    "failed": g.failed,
                    "total": g.total,
                    "pass_rate": g.pass_rate,
                    "assertions": [a.__dict__ for a in g.assertions],
                }
                for g in grades
            ],
        }
        print(json.dumps(payload, indent=2))
    else:
        print_grade_table(grades)
    return 0 if all(g.failed == 0 for g in grades) else 1


def command_benchmark(args: argparse.Namespace) -> int:
    payload = benchmark(args.evals, args.outputs_dir, allow_missing=args.allow_missing)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2) + "\n")
        print(f"Wrote {args.output}")
    else:
        print(json.dumps(payload, indent=2))
    missing_errors = sum(run["result"].get("errors", 0) for run in payload["runs"])
    if missing_errors and not args.allow_missing:
        return 1
    failed = sum(run["result"]["failed"] for run in payload["runs"])
    return 0 if failed == 0 or args.allow_failures else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate and grade good-repo evals")
    parser.set_defaults(func=None)
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Validate eval and trigger schema")
    validate.add_argument("--evals", type=Path, default=Path("evals/evals.json"))
    validate.add_argument("--triggers", type=Path, default=Path("evals/trigger-queries.json"))
    validate.add_argument("--skill", type=Path, default=Path("skills/good-repo/SKILL.md"))
    validate.add_argument("--quiet", action="store_true")
    validate.set_defaults(func=command_validate)

    grade = sub.add_parser("grade", help="Grade saved outputs for one configuration")
    grade.add_argument("--evals", type=Path, default=Path("evals/evals.json"))
    grade.add_argument("--outputs-dir", type=Path, required=True)
    grade.add_argument("--configuration", choices=CONFIGURATIONS, default="with_skill")
    grade.add_argument("--allow-missing", action="store_true", help="Skip evals with no saved output instead of failing them")
    grade.add_argument("--json", action="store_true", help="Print JSON instead of Markdown table")
    grade.set_defaults(func=command_grade)

    bench = sub.add_parser("benchmark", help="Compare with_skill and without_skill saved outputs")
    bench.add_argument("--evals", type=Path, default=Path("evals/evals.json"))
    bench.add_argument("--outputs-dir", type=Path, required=True)
    bench.add_argument("--output", type=Path, help="Write benchmark JSON to this path")
    bench.add_argument("--allow-missing", action="store_true", help="Skip missing outputs")
    bench.add_argument("--allow-failures", action="store_true", help="Return success even if graded assertions fail")
    bench.set_defaults(func=command_benchmark)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
