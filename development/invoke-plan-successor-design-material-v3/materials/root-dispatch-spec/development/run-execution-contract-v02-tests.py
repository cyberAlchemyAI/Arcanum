#!/usr/bin/env python3
"""Focused validator and no-effect rehearsal tests for execution contract v0.2."""

from __future__ import annotations

import copy
import json
import subprocess
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
ARCANUM = PACKAGE.parents[1]
VALIDATOR = PACKAGE / "scripts/validate-dispatch.py"
COORDINATOR = ARCANUM / "runtime/orchestrate/scripts/native_dispatch_coordinator.py"
BASE = PACKAGE / "examples/capability-bound-artifact-repair.json"
BRIEFINGS = PACKAGE / "examples/capability-bound-artifact-repair-briefings.json"


def strict_fixture() -> dict:
    doc = json.loads(BASE.read_text(encoding="utf-8"))
    strategy = doc["subagent_strategy"]
    strategy["execution_contract_version"] = "arcanum.capability-bound-execution.v0.2"
    strategy["execution_waves"][1]["gate_after"] = "g-artifact-scope"
    doc["gates"][0]["evaluation"] = {"mode": "receipt_status"}
    doc["gates"][1].update(
        {
            "applies_after_wave": "artifact-repair",
            "requires_role_receipts": ["receipts/artifact-repair.json"],
            "evaluation": {
                "mode": "domain_status",
                "source_role_id": "artifact-repair",
                "source_field": "domain_gate_status",
                "pass_values": ["valid"],
                "resolved_values": ["invalid"],
            },
        }
    )
    return doc


def run_validator(path: Path) -> dict:
    completed = subprocess.run([str(VALIDATOR), str(path), "--json"], check=False, capture_output=True, text=True)
    return json.loads(completed.stdout)


def main() -> int:
    failures: list[str] = []
    cases = []

    def case(name, mutate, expected):
        cases.append((name, mutate, expected))

    case("missing final gate", lambda doc: doc["subagent_strategy"]["execution_waves"][1].pop("gate_after"), "every v0.2 wave requires gate_after")
    case("incorrect wave binding", lambda doc: doc["gates"][1].update({"applies_after_wave": "lifecycle-updates"}), "must declare applies_after_wave='artifact-repair'")
    case("incomplete receipt coverage", lambda doc: doc["gates"][0].update({"requires_role_receipts": ["receipts/xray-iteration.json"]}), "missing role receipts")
    case("extra receipt coverage", lambda doc: doc["gates"][0]["requires_role_receipts"].append("receipts/artifact-repair.json"), "includes receipts outside the wave")
    case("missing typed evaluation", lambda doc: doc["gates"][0].pop("evaluation"), "requires typed evaluation under v0.2")
    case("ambiguous domain role", lambda doc: next(role for role in doc["subagent_strategy"]["roles"] if role["role_id"] == "artifact-repair").update({"agent_count": 2}), "domain_status source role must have agent_count=1")
    case("overlapping values", lambda doc: doc["gates"][1]["evaluation"]["resolved_values"].append("valid"), "pass_values and resolved_values overlap")
    case("wrong source field", lambda doc: doc["gates"][1]["evaluation"].update({"source_field": "task_status"}), "source_field must equal the source briefing domain_gate_status_field")
    case("non-final resolution", lambda doc: doc["gates"][0].update({"evaluation": {"mode": "domain_status", "source_role_id": "xray-lifecycle", "source_field": "domain_gate_status", "pass_values": ["valid"], "resolved_values": ["invalid"]}}), "resolved_values are permitted only on the final wave")

    with tempfile.TemporaryDirectory(prefix="execution-v02-") as temp_dir:
        root = Path(temp_dir)
        (root / BRIEFINGS.name).write_bytes(BRIEFINGS.read_bytes())
        baseline_path = root / "baseline.json"
        baseline_path.write_text(json.dumps(strict_fixture(), indent=2) + "\n", encoding="utf-8")
        baseline = run_validator(baseline_path)
        if baseline.get("validation") != "pass":
            print(json.dumps(baseline, indent=2))
            return 1
        print("EXECUTION_V02_BASELINE=pass")

        rehearsal = subprocess.run(
            ["python3", str(COORDINATOR), "rehearse", str(baseline_path), "--run-id", "v02-rehearsal"],
            check=False,
            capture_output=True,
            text=True,
        )
        try:
            rehearsal_result = json.loads(rehearsal.stdout)
        except json.JSONDecodeError:
            rehearsal_result = {}
        if not (
            rehearsal.returncode == 0
            and rehearsal_result.get("status") == "pass"
            and rehearsal_result.get("spawn_attempt_count") == 0
            and rehearsal_result.get("action_document_count") == 0
            and rehearsal_result.get("host_call_count") == 0
        ):
            failures.append(f"no-effect rehearsal: {rehearsal.stdout or rehearsal.stderr}")
        else:
            print("EXECUTION_V02_REHEARSAL=pass SPAWN_ATTEMPTS=0 ACTION_DOCUMENTS=0 HOST_CALLS=0")

        for index, (name, mutate, expected) in enumerate(cases, start=1):
            candidate = copy.deepcopy(strict_fixture())
            mutate(candidate)
            path = root / f"case-{index}.json"
            path.write_text(json.dumps(candidate, indent=2) + "\n", encoding="utf-8")
            result = run_validator(path)
            if result.get("validation") != "block" or not any(expected in block for block in result.get("blocks", [])):
                failures.append(f"{name}: expected {expected!r}, got {result}")
            else:
                print(f"EXECUTION_V02_MUTATION=pass CASE={name}")

    if failures:
        for failure in failures:
            print(f"EXECUTION_V02=block {failure}")
        return 1
    print("EXECUTION_V02=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
