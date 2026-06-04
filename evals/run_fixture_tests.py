#!/usr/bin/env python3
"""Run fixture-level mechanical tests for good-repo scripts.

These tests exercise file-scanning behavior without touching real GitHub
settings. The readiness script exposes GOOD_REPO_* environment overrides so
fixture repos can simulate GitHub metadata deterministically.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class FixtureCase:
    name: str
    slug: str
    github_homepage: str = ""
    contains: list[str] = field(default_factory=list)
    excludes: list[str] = field(default_factory=list)


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "evals" / "fixtures"
SCRIPT = ROOT / "skills" / "good-repo" / "scripts" / "check-repo-readiness.sh"

CASES = [
    FixtureCase(
        name="homepage-missing",
        slug="example/example-app",
        contains=[
            "Candidate homepage URL found (https://example-app.workers.dev/), but GitHub homepage is not configured for example/example-app",
        ],
        excludes=[
            "No candidate homepage URL found",
            "GitHub homepage matches candidate URL",
        ],
    ),
    FixtureCase(
        name="homepage-third-party-docs",
        slug="example/worker-notes",
        contains=[
            "No candidate homepage URL found and GitHub homepage is empty",
        ],
        excludes=[
            "Candidate homepage URL found",
            "developers.cloudflare.com/workers/), but GitHub homepage",
        ],
    ),
    FixtureCase(
        name="license-missing",
        slug="example/license-missing",
        contains=[
            "LICENSE missing or not in a standard root file",
        ],
    ),
    FixtureCase(
        name="skill-layout-bad",
        slug="example/repo-auditor",
        contains=[
            "Skill repo metadata found, but no skills/<name>/SKILL.md packaged skill files were found",
            "Found skill/SKILL.md; use skills/<skill-name>/SKILL.md",
            "Evals found inside an installable skill directory",
            "Marketplace metadata uses a flat skills list",
        ],
    ),
    FixtureCase(
        name="skill-name-mismatch",
        slug="example/repo-auditor",
        contains=[
            "Skill directory name (wrong-name) does not match SKILL.md frontmatter name (repo-auditor)",
        ],
    ),
]


def run_case(case: FixtureCase) -> tuple[bool, str]:
    source = FIXTURES / case.name
    if not source.exists():
        return False, f"fixture missing: {source}"

    with tempfile.TemporaryDirectory(prefix=f"good-repo-{case.name}-") as tmp:
        workdir = Path(tmp) / case.name
        shutil.copytree(source, workdir)
        env = os.environ.copy()
        env["GOOD_REPO_REPO_SLUG"] = case.slug
        env["GOOD_REPO_GITHUB_HOMEPAGE"] = case.github_homepage
        result = subprocess.run(
            ["bash", str(SCRIPT)],
            cwd=workdir,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        output = result.stdout
        problems: list[str] = []
        if result.returncode != 0:
            problems.append(f"script exited {result.returncode}")
        for expected in case.contains:
            if expected not in output:
                problems.append(f"missing expected text: {expected!r}")
        for forbidden in case.excludes:
            if forbidden in output:
                problems.append(f"found forbidden text: {forbidden!r}")
        if problems:
            return False, f"{case.name}: " + "; ".join(problems) + "\n--- output ---\n" + output
        return True, f"{case.name}: ok"


def main() -> int:
    failures: list[str] = []
    for case in CASES:
        ok, message = run_case(case)
        if ok:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}", file=sys.stderr)
            failures.append(message)
    if failures:
        print(f"\n{len(failures)} fixture test(s) failed", file=sys.stderr)
        return 1
    print(f"\n{len(CASES)} fixture tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
