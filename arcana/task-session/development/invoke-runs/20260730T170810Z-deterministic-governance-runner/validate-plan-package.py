#!/usr/bin/env python3
"""Validate the deterministic governance runner Invoke planning package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


REQUIRED_ROOT = {
    "SPEC.md",
    "GLOSSARY.md",
    "ARCHITECTURE.md",
    "UX-PLAN.md",
    "VALIDATION-CONTRACTS.md",
    "IMPLEMENTATION-LAYERING.md",
    "IMPLEMENTATION-PLAN.md",
    "WORK-PACK.md",
    "EXECUTION-PACK.md",
    "DESIGN-SCOPE-MANIFEST.json",
    "DESIGN-DENOMINATOR-RECEIPT.json",
    "DESIGN-SELECTION-RESULT.json",
    "CONTINUATION.json",
    "OWNER-READINESS.md",
    "PLAN-DISTILL-VALIDATION.md",
    "PLAN-TRANSPORT.md",
    "INVOKE-REPORT.md",
    "INVOKE-RESULT.json",
    "DISPATCH-VALIDATION.json",
    "PLAN-VALIDATION.md",
    "OBSERVABILITY-RECEIPT.md",
}

TASK_FILES = {
    "TASK-TSGR-00-LIFECYCLE.md",
    "TASK-TSGR-01-CONTRACTS.md",
    "TASK-TSGR-02-RUNNER.md",
    "TASK-TSGR-03-HOOKS.md",
    "TASK-TSGR-04-OPERATIONS.md",
}

WAVE_FILES = {
    "W0-LIFECYCLE-CONTRACT.md",
    "W1-RUNNER-MECHANISM.md",
    "W2-OWNER-INTEGRATION.md",
    "W3-OPERATIONS-INTEGRATION.md",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors: list[str] = []

    for name in sorted(REQUIRED_ROOT):
        if not (root / name).is_file():
            fail(errors, f"missing root artifact: {name}")
    for name in sorted(TASK_FILES):
        if not (root / "work-pack" / "tasks" / name).is_file():
            fail(errors, f"missing task artifact: {name}")
    for name in sorted(WAVE_FILES):
        if not (root / "work-pack" / "waves" / name).is_file():
            fail(errors, f"missing wave artifact: {name}")
    if not (root / "work-pack" / "shared" / "EXECUTION-CONTROL.md").is_file():
        fail(errors, "missing shared execution control")
    for name in (
        "task-session-swu-result.schema.json",
        "continuation-closeout-receipt.schema.json",
        "invoke-refresh-owner-receipt.schema.json",
    ):
        schema_path = root / "schemas" / name
        if not schema_path.is_file():
            fail(errors, f"missing planning receipt schema: {name}")
            continue
        try:
            Draft202012Validator.check_schema(json.loads(schema_path.read_text()))
        except Exception as error:
            fail(errors, f"invalid planning receipt schema {name}: {error}")
    for name in ("distill-child-envelope.json", "invoke-envelope.json"):
        if not (root / "observability" / name).is_file():
            fail(errors, f"missing observability envelope: {name}")

    work_pack = (root / "WORK-PACK.md").read_text(encoding="utf-8")
    expected_swus = {f"SWU-TSGR-{index:03d}" for index in range(11)}
    observed_swus = set(re.findall(r"SWU-TSGR-\d{3}", work_pack))
    missing_swus = sorted(expected_swus - observed_swus)
    if missing_swus:
        fail(errors, f"work-pack missing SWUs: {', '.join(missing_swus)}")
    if work_pack.count("| selected |") != 1:
        fail(errors, "work-pack must select exactly one SWU")
    ordered_phrases = (
        "emit `execution-received`",
        "without applying",
        "atomically commit admitted staged outputs",
        "append-only Signal Observer",
        "paired Experiment Harness",
    )
    cursor = -1
    for phrase in ordered_phrases:
        next_cursor = work_pack.find(phrase, cursor + 1)
        if next_cursor < 0:
            fail(errors, f"work-pack missing reduced-order phrase: {phrase}")
            break
        cursor = next_cursor

    joined_tasks = "\n".join(
        (root / "work-pack" / "tasks" / name).read_text(encoding="utf-8")
        for name in sorted(TASK_FILES)
    )
    for swu in sorted(expected_swus):
        if swu not in joined_tasks:
            fail(errors, f"task contracts missing {swu}")

    control = (
        root / "work-pack" / "shared" / "EXECUTION-CONTROL.md"
    ).read_text(encoding="utf-8")
    for required in (
        "invoke:refresh:apply-approved",
        "terminal source receipt",
        "declared planning target inventory",
        "baseline",
        "allowed planning delta classes",
        "expected continuation router join receipt",
        "never execute",
    ):
        if required.lower() not in control.lower():
            fail(errors, f"execution control missing phrase: {required}")

    try:
        continuation = json.loads((root / "CONTINUATION.json").read_text())
    except (OSError, json.JSONDecodeError) as error:
        fail(errors, f"invalid continuation JSON: {error}")
    else:
        if continuation.get("selected_swu") != "SWU-TSGR-000":
            fail(errors, "continuation must select SWU-TSGR-000")
        if continuation.get("execution_authorized") is not False:
            fail(errors, "continuation must not authorize implementation")

    try:
        selection = json.loads(
            (root / "DESIGN-SELECTION-RESULT.json").read_text()
        )
    except (OSError, json.JSONDecodeError) as error:
        fail(errors, f"invalid design selection JSON: {error}")
    else:
        if selection.get("verdict") != "pass" or selection.get("fixed_point") is not True:
            fail(errors, "design selection must be fixed-point pass")

    public_text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in root.rglob("*")
        if path.is_file() and path.name != Path(__file__).name
    )
    private_project_slug = "body" + "-war"
    private_feature_phrase = "suggested" + " track"
    for forbidden in (
        f"projects/{private_project_slug}",
        f"{private_project_slug}.",
        private_feature_phrase,
    ):
        if forbidden.lower() in public_text.lower():
            fail(errors, f"public package contains forbidden consumer selector: {forbidden}")

    if errors:
        print("VALIDATION=block")
        for error in errors:
            print(f"ERROR={error}")
        return 1
    print("VALIDATION=pass")
    print("SWU_COUNT=11")
    print("SELECTED_SWU=SWU-TSGR-000")
    print("AUTHORITY=planning-only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
