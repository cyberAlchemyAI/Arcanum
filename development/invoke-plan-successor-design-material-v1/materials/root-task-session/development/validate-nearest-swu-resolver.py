#!/usr/bin/env python3
"""Exercise the generated nearest-SWU resolver against filesystem fixtures."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


def write_fixture(root: Path, fixture: dict[str, Any]) -> None:
    target = root / fixture["path"]
    target.parent.mkdir(parents=True, exist_ok=True)
    if "json" in fixture:
        target.write_text(
            json.dumps(fixture["json"], indent=2) + "\n",
            encoding="utf-8",
        )
    else:
        target.write_text(str(fixture.get("content", "")) + "\n", encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "usage: validate-nearest-swu-resolver.py <canonical-task-session-dir>",
            file=sys.stderr,
        )
        return 2

    canonical_dir = Path(sys.argv[1]).resolve()
    resolver = canonical_dir / "scripts/resolve-nearest-swu.py"
    fixture_path = (
        canonical_dir
        / "development/fixtures/nearest-swu-resolution-cases.json"
    )
    fixtures = json.loads(fixture_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    passed = 0

    for case in fixtures["cases"]:
        with tempfile.TemporaryDirectory(prefix="task-session-nearest-") as temp:
            repo_root = Path(temp)
            for fixture in case.get("files", []):
                write_fixture(repo_root, fixture)
            cwd = repo_root / case.get("cwd", ".")
            cwd.mkdir(parents=True, exist_ok=True)

            command = [
                sys.executable,
                str(resolver),
                "--repo-root",
                str(repo_root),
                "--cwd",
                str(cwd),
                *case.get("args", []),
            ]
            environment = os.environ.copy()
            for variable in (
                "ARCANUM_TASK_SESSION_ID",
                "CODEX_THREAD_ID",
                "CLAUDE_SESSION_ID",
            ):
                environment.pop(variable, None)
            environment.update(case.get("env", {}))
            completed = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                env=environment,
            )

            try:
                actual = json.loads(completed.stdout)
            except json.JSONDecodeError:
                errors.append(
                    f"{case['id']}: resolver did not emit JSON: {completed.stdout!r}"
                )
                continue

            expected = case["expected"]
            mismatches: list[str] = []
            for key in ("status", "reason"):
                if actual.get(key) != expected.get(key):
                    mismatches.append(
                        f"{key} expected={expected.get(key)!r} "
                        f"actual={actual.get(key)!r}"
                    )

            if (
                "session_id_source" in expected
                and actual.get("session_id_source")
                != expected["session_id_source"]
            ):
                mismatches.append(
                    "session_id_source "
                    f"expected={expected['session_id_source']!r} "
                    f"actual={actual.get('session_id_source')!r}"
                )

            if "candidate_count" in expected and len(actual["candidates"]) != expected[
                "candidate_count"
            ]:
                mismatches.append(
                    f"candidate_count expected={expected['candidate_count']} "
                    f"actual={len(actual['candidates'])}"
                )

            if "source" in expected:
                selected = actual.get("selected") or {}
                for key in ("source", "work_pack", "swu"):
                    if selected.get(key) != expected.get(key):
                        mismatches.append(
                            f"selected.{key} expected={expected.get(key)!r} "
                            f"actual={selected.get(key)!r}"
                        )

            if "rejection_reason" in expected:
                reasons = {item.get("reason") for item in actual.get("rejected", [])}
                if expected["rejection_reason"] not in reasons:
                    mismatches.append(
                        f"rejection_reason {expected['rejection_reason']!r} "
                        f"not in {sorted(str(item) for item in reasons)}"
                    )

            if actual.get("execution_limit") not in {None, 1}:
                mismatches.append(
                    f"execution_limit expected=1 actual={actual.get('execution_limit')}"
                )

            if mismatches:
                errors.append(f"{case['id']}: {'; '.join(mismatches)}")
            else:
                passed += 1

    if errors:
        for error in errors:
            print(f"FAIL {error}")
        print(f"RESULT nearest-resolution passed={passed} failed={len(errors)}")
        return 1

    print(f"RESULT nearest-resolution passed={passed} failed=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
