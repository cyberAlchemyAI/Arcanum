#!/usr/bin/env python3
"""Materialize the bounded Invoke Refresh control-plane repair."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[7]
INVOKE_RUN = Path(
    "spells/goal/development/invoke-runs/"
    "20260730T171428Z-decision-frontier-experiment"
)
REFRESH_RUN = INVOKE_RUN / "refresh-runs/20260730T182631Z-runtime-admission-refresh"
STAGED_ROOT = REFRESH_RUN / "staged"
EXPERIMENT_ROOT = "spells/goal/development/decision-frontier-experiment"


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def exact_ref(path: str) -> dict[str, object]:
    content = (REPOSITORY_ROOT / path).read_bytes()
    return {
        "path": path,
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def staged_ref(path: str) -> dict[str, object]:
    staged_path = str(REFRESH_RUN / "staged" / path)
    content = (REPOSITORY_ROOT / staged_path).read_bytes()
    return {
        "path": staged_path,
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def write_text(relative: str, content: str) -> None:
    path = REPOSITORY_ROOT / STAGED_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_json(relative: str, value: object) -> None:
    path = REPOSITORY_ROOT / STAGED_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def command(argv: list[str], *, risk: str = "bounded-write") -> dict[str, object]:
    return {
        "cwd": "spells",
        "argv": argv,
        "expected_exit_code": 0,
        "timeout_seconds": 120,
        "environment": {"PYTHONDONTWRITEBYTECODE": "1"},
        "runtime_identity": {
            "executable": "python3",
            "version_policy": "exact version captured at Task Session preflight",
            "hash_policy": "resolve and SHA-256 the executable at Task Session preflight",
        },
        "risk_class": risk,
    }


def execution_paths(unit: str, validation_name: str) -> list[str]:
    prefix = f"{EXPERIMENT_ROOT}/session-evidence/{unit}"
    return [f"{prefix}/baseline.json", f"{prefix}/{validation_name}"]


def unit(
    unit_id: str,
    task: str,
    material_writes: list[str],
    validation_name: str,
    script: str,
    dependency: str | None,
    successor: str,
    extra_argv: list[str] | None = None,
) -> dict[str, object]:
    outputs = execution_paths(unit_id, validation_name)
    argv = [
        "python3",
        f"goal/development/decision-frontier-experiment/scripts/{script}",
    ]
    argv.extend(extra_argv or [])
    prefix = f"{EXPERIMENT_ROOT}/session-evidence/{unit_id}"
    return {
        "unit_id": unit_id,
        "task_path": str(INVOKE_RUN / f"work-pack/tasks/{task}"),
        "task_class": "material-mutation",
        "requested_execution_mode": "reusable-mutation",
        "dependencies": [dependency] if dependency else [],
        "successor": successor,
        "material_writes": material_writes,
        "execution_outputs": outputs,
        "allowed_writes": material_writes + outputs,
        "validation_commands": [command(argv)],
        "attempt": {
            "required": False,
            "id_algorithm": "",
            "collision_policy": "fail-if-exists",
            "retention_policy": "retain-receipt-only",
            "teardown_on_success": [],
            "teardown_on_failure": [],
        },
        "terminal_receipt": f"{prefix}/task-session-receipt.json",
        "closeout_receipt": f"{prefix}/owner-receipt.json",
        "dispatch_step": unit_id.lower(),
    }


def build_command_matrix() -> dict[str, object]:
    root = EXPERIMENT_ROOT
    units = [
        unit(
            "SWU-DFE-001",
            "TASK-DFE-CONTRACT.md",
            [
                f"{root}/README.md",
                *[
                    f"{root}/schemas/{name}.schema.json"
                    for name in (
                        "decision-map",
                        "frontier-snapshot",
                        "claim",
                        "resolution",
                        "reconciliation",
                        "way-clear",
                    )
                ],
                f"{root}/fixtures/diamond-map.json",
                f"{root}/fixtures/cycle-map.json",
                f"{root}/scripts/validate_contracts.py",
            ],
            "contract-validation.json",
            "validate_contracts.py",
            None,
            "SWU-DFE-002",
        ),
        unit(
            "SWU-DFE-002",
            "TASK-DFE-REDUCER.md",
            [
                f"{root}/runtime/frontier.py",
                f"{root}/fixtures/fog-map.json",
                f"{root}/fixtures/scope-map.json",
                f"{root}/fixtures/invalidated-map.json",
                f"{root}/fixtures/expected/diamond-frontier.json",
                f"{root}/fixtures/expected/fog-frontier.json",
                f"{root}/fixtures/expected/scope-frontier.json",
                f"{root}/fixtures/expected/invalidated-frontier.json",
                f"{root}/scripts/run_frontier_fixtures.py",
            ],
            "frontier-validation.json",
            "run_frontier_fixtures.py",
            "SWU-DFE-001",
            "SWU-DFE-003",
            ["--replay", "2"],
        ),
        unit(
            "SWU-DFE-003",
            "TASK-DFE-CLAIM.md",
            [
                f"{root}/runtime/claims.py",
                f"{root}/fixtures/active-claim.json",
                f"{root}/fixtures/stale-claim.json",
                f"{root}/fixtures/expected/claim-accepted.json",
                f"{root}/fixtures/expected/claim-rejected-stale.json",
                f"{root}/scripts/run_claim_fixtures.py",
            ],
            "claim-validation.json",
            "run_claim_fixtures.py",
            "SWU-DFE-002",
            "SWU-DFE-004",
        ),
        unit(
            "SWU-DFE-004",
            "TASK-DFE-RECONCILE.md",
            [
                f"{root}/runtime/reconcile.py",
                *[
                    f"{root}/fixtures/{name}-resolution.json"
                    for name in ("fog", "invalidation", "add", "supersede", "unblock")
                ],
                *[
                    f"{root}/fixtures/expected/{name}-reconciliation.json"
                    for name in ("fog", "invalidation", "add", "supersede", "unblock")
                ],
                f"{root}/scripts/run_reconciliation_fixtures.py",
            ],
            "reconciliation-validation.json",
            "run_reconciliation_fixtures.py",
            "SWU-DFE-003",
            "SWU-DFE-005",
        ),
        unit(
            "SWU-DFE-005",
            "TASK-DFE-BOUNDARY.md",
            [
                f"{root}/runtime/hitl.py",
                f"{root}/fixtures/hitl-map.json",
                f"{root}/fixtures/expected/hitl-route.json",
                f"{root}/scripts/run_hitl_fixture.py",
            ],
            "hitl-validation.json",
            "run_hitl_fixture.py",
            "SWU-DFE-004",
            "SWU-DFE-006",
        ),
        unit(
            "SWU-DFE-006",
            "TASK-DFE-BOUNDARY.md",
            [
                f"{root}/runtime/way_clear.py",
                f"{root}/fixtures/way-clear-map.json",
                f"{root}/fixtures/way-clear-open-mutant.json",
                f"{root}/fixtures/way-clear-fog-mutant.json",
                f"{root}/fixtures/expected/way-clear.json",
                f"{root}/scripts/run_way_clear_fixtures.py",
            ],
            "way-clear-validation.json",
            "run_way_clear_fixtures.py",
            "SWU-DFE-005",
            "SWU-DFE-007",
        ),
        unit(
            "SWU-DFE-007",
            "TASK-DFE-BOUNDARY.md",
            [
                f"{root}/fixtures/execution-state.json",
                f"{root}/fixtures/decision-closure.json",
                f"{root}/fixtures/expected/execution-state-unchanged.json",
                f"{root}/scripts/run_noncollapse_fixture.py",
            ],
            "noncollapse-validation.json",
            "run_noncollapse_fixture.py",
            "SWU-DFE-006",
            "VERIFY-DFE-001",
        ),
    ]
    control_root = str(INVOKE_RUN / "work-pack/shared").removeprefix("spells/")
    command_experiment_root = EXPERIMENT_ROOT.removeprefix("spells/")
    units.extend(
        [
            {
                "unit_id": "VERIFY-DFE-001",
                "task_path": str(
                    INVOKE_RUN / "work-pack/tasks/TASK-DFE-VERIFY.md"
                ),
                "task_class": "audit-only",
                "requested_execution_mode": "reusable-mutation",
                "dependencies": ["SWU-DFE-007"],
                "successor": "READINESS-DFE-001",
                "material_writes": [],
                "execution_outputs": [
                    f"{root}/session-evidence/VERIFY-DFE-001/authority-hashes.json"
                ],
                "allowed_writes": [
                    f"{root}/session-evidence/VERIFY-DFE-001/authority-hashes.json"
                ],
                "validation_commands": [
                    command(
                        [
                            "python3",
                            f"{control_root}/run_closure.py",
                            "--experiment-root",
                            command_experiment_root,
                            "--output",
                            f"{command_experiment_root}/session-evidence/VERIFY-DFE-001/authority-hashes.json",
                        ]
                    )
                ],
                "attempt": {
                    "required": False,
                    "id_algorithm": "",
                    "collision_policy": "fail-if-exists",
                    "retention_policy": "retain-receipt-only",
                    "teardown_on_success": [],
                    "teardown_on_failure": [],
                },
                "terminal_receipt": f"{root}/session-evidence/VERIFY-DFE-001/closure-receipt.json",
                "closeout_receipt": f"{root}/session-evidence/VERIFY-DFE-001/closure-receipt.json",
                "dispatch_step": "verify-dfe-001",
            },
            {
                "unit_id": "READINESS-DFE-001",
                "task_path": str(
                    INVOKE_RUN / "work-pack/tasks/TASK-DFE-READINESS.md"
                ),
                "task_class": "output-only",
                "requested_execution_mode": "reusable-mutation",
                "dependencies": ["VERIFY-DFE-001"],
                "successor": None,
                "material_writes": [],
                "execution_outputs": [
                    f"{root}/session-evidence/READINESS-DFE-001/lifecycle-decision.json"
                ],
                "allowed_writes": [
                    f"{root}/session-evidence/READINESS-DFE-001/lifecycle-decision.json"
                ],
                "validation_commands": [
                    command(
                        [
                            "python3",
                            f"{control_root}/record_lifecycle_decision.py",
                            "--closure",
                            f"{command_experiment_root}/session-evidence/VERIFY-DFE-001/closure-receipt.json",
                            "--output",
                            f"{command_experiment_root}/session-evidence/READINESS-DFE-001/lifecycle-decision.json",
                        ]
                    )
                ],
                "attempt": {
                    "required": False,
                    "id_algorithm": "",
                    "collision_policy": "fail-if-exists",
                    "retention_policy": "retain-receipt-only",
                    "teardown_on_success": [],
                    "teardown_on_failure": [],
                },
                "terminal_receipt": f"{root}/session-evidence/READINESS-DFE-001/lifecycle-decision.json",
                "closeout_receipt": f"{root}/session-evidence/READINESS-DFE-001/lifecycle-decision.json",
                "dispatch_step": "readiness-dfe-001",
            },
        ]
    )
    return {
        "schema_version": "1.0.0",
        "work_pack": str(INVOKE_RUN / "WORK-PACK.md"),
        "authority_class": "public",
        "publication_class": "public",
        "lifecycle_owner": "spellcraft",
        "closeout_owner": "invoke:refresh:apply-approved",
        "units": units,
    }


TERMINAL_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://arcanum.dev/experiments/goal-decision-frontier/task-session-receipt/1-0-0",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "schema_version",
        "unit_id",
        "step_id",
        "session_id",
        "status",
        "validation_result",
        "work_pack_sha256",
        "baseline_digest",
        "artifacts",
        "validation",
        "blockers",
        "material_writes",
        "execution_outputs",
        "allowed_writes",
        "undeclared_writes",
        "authority_effect",
        "successor",
        "experiment_harness",
    ],
    "properties": {
        "schema_version": {"const": "task-session-terminal-receipt.v1"},
        "unit_id": {"type": "string", "minLength": 1},
        "step_id": {"type": "string", "minLength": 1},
        "session_id": {"type": "string", "minLength": 1},
        "status": {"enum": ["pass", "flag", "block"]},
        "validation_result": {"enum": ["pass", "flag", "block"]},
        "work_pack_sha256": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
        "baseline_digest": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
        "artifacts": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["path", "sha256", "size_bytes", "delta"],
                "properties": {
                    "path": {"type": "string", "minLength": 1},
                    "sha256": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
                    "size_bytes": {"type": "integer", "minimum": 0},
                    "delta": {"enum": ["added", "changed", "unchanged"]},
                },
            },
        },
        "validation": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["argv", "exit_code", "evidence_path"],
                "properties": {
                    "argv": {
                        "type": "array",
                        "minItems": 1,
                        "items": {"type": "string", "minLength": 1},
                    },
                    "exit_code": {"type": "integer"},
                    "evidence_path": {"type": "string", "minLength": 1},
                },
            },
        },
        "blockers": {
            "type": "array",
            "items": {"type": "string", "minLength": 1},
        },
        "material_writes": {
            "type": "array",
            "uniqueItems": True,
            "items": {"type": "string", "minLength": 1},
        },
        "execution_outputs": {
            "type": "array",
            "uniqueItems": True,
            "items": {"type": "string", "minLength": 1},
        },
        "allowed_writes": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": {"type": "string", "minLength": 1},
        },
        "undeclared_writes": {
            "type": "array",
            "items": {"type": "string", "minLength": 1},
        },
        "authority_effect": {"const": "none"},
        "successor": {
            "type": "object",
            "additionalProperties": False,
            "required": ["unit_id", "eligible", "selected"],
            "properties": {
                "unit_id": {"type": ["string", "null"], "minLength": 1},
                "eligible": {"type": "boolean"},
                "selected": {"const": False},
            },
        },
        "experiment_harness": {
            "enum": ["updated", "pending", "blocked", "not_applicable"]
        },
    },
    "allOf": [
        {
            "if": {
                "properties": {"status": {"const": "pass"}},
                "required": ["status"],
            },
            "then": {
                "properties": {
                    "validation_result": {"const": "pass"},
                    "artifacts": {"minItems": 1},
                    "validation": {"minItems": 1},
                    "blockers": {"maxItems": 0},
                    "undeclared_writes": {"maxItems": 0},
                }
            },
        }
    ],
}


CLOSEOUT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://arcanum.dev/experiments/goal-decision-frontier/closeout-receipt/1-0-0",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "schema_version",
        "unit_id",
        "owner",
        "lifecycle_owner",
        "source_receipt",
        "validation_result",
        "validated_targets",
        "evidence",
        "delta_classes",
        "blockers",
        "successor",
        "lifecycle_effect",
        "authority_effect",
    ],
    "properties": {
        "schema_version": {"const": "invoke-refresh-closeout-receipt.v1"},
        "unit_id": {"type": "string", "minLength": 1},
        "owner": {"const": "invoke:refresh:apply-approved"},
        "lifecycle_owner": {"const": "spellcraft"},
        "source_receipt": {
            "type": "object",
            "additionalProperties": False,
            "required": ["path", "sha256", "size_bytes"],
            "properties": {
                "path": {"type": "string", "minLength": 1},
                "sha256": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
                "size_bytes": {"type": "integer", "minimum": 1},
            },
        },
        "validation_result": {"enum": ["pass", "block"]},
        "validated_targets": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": {"type": "string", "minLength": 1},
        },
        "evidence": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "string", "minLength": 1},
        },
        "delta_classes": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": {
                "enum": [
                    "evidence_added",
                    "blocker_opened",
                    "blocker_resolved",
                    "status_changed",
                    "route_changed",
                ]
            },
        },
        "blockers": {
            "type": "array",
            "items": {"type": "string", "minLength": 1},
        },
        "successor": {
            "type": "object",
            "additionalProperties": False,
            "required": ["unit_id", "eligible", "selected"],
            "properties": {
                "unit_id": {"type": ["string", "null"], "minLength": 1},
                "eligible": {"type": "boolean"},
                "selected": {"const": False},
            },
        },
        "lifecycle_effect": {"const": "none"},
        "authority_effect": {"const": "none"},
    },
    "allOf": [
        {
            "if": {
                "properties": {"validation_result": {"const": "pass"}},
                "required": ["validation_result"],
            },
            "then": {"properties": {"blockers": {"maxItems": 0}}},
        }
    ],
}


SEMANTIC_VALIDATOR = r'''#!/usr/bin/env python3
"""Validate receipt identity and semantic bindings after JSON Schema validation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--unit", required=True)
    parser.add_argument("--step", required=True)
    parser.add_argument("--work-pack-sha256", required=True)
    parser.add_argument("--successor", required=True)
    args = parser.parse_args()

    document = json.loads(args.receipt.read_text(encoding="utf-8"))
    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda error: list(error.absolute_path),
    )
    reasons = [
        f"schema:{'/'.join(map(str, error.absolute_path)) or '<root>'}:{error.message}"
        for error in errors
    ]
    expected_successor = None if args.successor == "none" else args.successor
    expected = {
        "unit_id": args.unit,
        "step_id": args.step,
        "work_pack_sha256": args.work_pack_sha256,
    }
    for key, value in expected.items():
        if document.get(key) != value:
            reasons.append(f"{key}:expected={value!r}:actual={document.get(key)!r}")
    successor = document.get("successor", {})
    if successor.get("unit_id") != expected_successor:
        reasons.append("successor unit mismatch")
    if successor.get("selected") is not False:
        reasons.append("successor must remain unselected")
    material = set(document.get("material_writes", []))
    outputs = set(document.get("execution_outputs", []))
    allowed = set(document.get("allowed_writes", []))
    if material & outputs or material | outputs != allowed:
        reasons.append("write partition mismatch")
    print(json.dumps({"status": "pass" if not reasons else "block", "reasons": reasons}, sort_keys=True))
    return 0 if not reasons else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''


CLOSEOUT_SYNC = r'''#!/usr/bin/env python3
"""Run the bounded Invoke Refresh closeout owner hop for one DFE unit."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", required=True, type=Path)
    parser.add_argument("--matrix", required=True, type=Path)
    parser.add_argument("--unit", required=True)
    parser.add_argument("--source-receipt", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    root = args.repository_root.resolve()
    matrix = json.loads(args.matrix.read_text(encoding="utf-8"))
    by_id = {unit["unit_id"]: unit for unit in matrix["units"]}
    unit = by_id[args.unit]
    source_path = root / args.source_receipt
    source = json.loads(source_path.read_text(encoding="utf-8"))
    blockers = []
    if source.get("status") != "pass" or source.get("validation_result") != "pass":
        blockers.append("source terminal receipt is not passing")

    evidence = []
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    for spec in unit["validation_commands"]:
        result = subprocess.run(
            spec["argv"],
            cwd=root / spec["cwd"],
            env={**env, **spec["environment"]},
            timeout=spec["timeout_seconds"],
            check=False,
            capture_output=True,
            text=True,
        )
        evidence.append(
            f"argv={json.dumps(spec['argv'], separators=(',', ':'))};exit={result.returncode}"
        )
        if result.returncode != spec["expected_exit_code"]:
            blockers.append(f"owner validation failed: {spec['argv']}")

    validated_targets = []
    for item in source.get("artifacts", []):
        target = root / item["path"]
        if not target.is_file() or digest(target) != item["sha256"]:
            blockers.append(f"target drift: {item['path']}")
        else:
            validated_targets.append(item["path"])

    source_ref = {
        "path": args.source_receipt,
        "sha256": digest(source_path),
        "size_bytes": source_path.stat().st_size,
    }
    successor = source.get("successor", {"unit_id": None, "eligible": False, "selected": False})
    receipt = {
        "schema_version": "invoke-refresh-closeout-receipt.v1",
        "unit_id": args.unit,
        "owner": "invoke:refresh:apply-approved",
        "lifecycle_owner": "spellcraft",
        "source_receipt": source_ref,
        "validation_result": "pass" if not blockers else "block",
        "validated_targets": sorted(validated_targets),
        "evidence": evidence or ["source receipt identity validated"],
        "delta_classes": ["evidence_added", "route_changed"],
        "blockers": blockers,
        "successor": successor,
        "lifecycle_effect": "none",
        "authority_effect": "none",
    }
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''


CLOSURE_RUNNER = r'''#!/usr/bin/env python3
"""Independently close the bounded DFE fixture experiment."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


CANONICAL_INPUTS = [
    "spells/goal/README.md",
    "spells/goal/runtime/goal_loop.py",
    "spells/goal/schemas/frontier-snapshot.schema.json",
    "spells/invoke/README.md",
    "arcana/craft/SKILL.md",
    "arcana/craft/templates/schemas/ledger-core.schema.yml",
]
DESIGN_MANIFEST = (
    "spells/goal/development/invoke-runs/"
    "20260730T171428Z-decision-frontier-experiment/"
    "DESIGN-SCOPE-MANIFEST.json"
)


def ref(root: Path, relative: str) -> dict[str, object]:
    path = root / relative
    content = path.read_bytes()
    return {"path": relative, "sha256": hashlib.sha256(content).hexdigest(), "size_bytes": len(content)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    spells_root = Path.cwd().resolve()
    arcanum_root = spells_root.parent
    experiment = spells_root / args.experiment_root
    missing = []
    owner_receipts = []
    for index in range(1, 8):
        unit = f"SWU-DFE-{index:03d}"
        owner = experiment / "session-evidence" / unit / "owner-receipt.json"
        if not owner.is_file():
            missing.append(str(owner.relative_to(arcanum_root)))
            continue
        document = json.loads(owner.read_text(encoding="utf-8"))
        if document.get("validation_result") != "pass":
            missing.append(f"{unit}:owner receipt not passing")
        owner_receipts.append(ref(arcanum_root, str(owner.relative_to(arcanum_root))))

    manifest = json.loads(
        (arcanum_root / DESIGN_MANIFEST).read_text(encoding="utf-8")
    )
    before_by_path = {
        item["path"]: item["digest"] for item in manifest["source_contracts"]
    }
    hashes = []
    for path in CANONICAL_INPUTS:
        after = ref(arcanum_root, path)
        before_sha256 = before_by_path.get(path)
        hashes.append(
            {
                "path": path,
                "before_sha256": before_sha256,
                "after_sha256": after["sha256"],
                "size_bytes": after["size_bytes"],
                "match": before_sha256 == after["sha256"],
            }
        )
        if before_sha256 is None or before_sha256 != after["sha256"]:
            missing.append(f"canonical hash drift: {path}")
    output = spells_root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    result = {
        "schema_version": "dfe-authority-hashes.v1",
        "status": "pass" if not missing else "block",
        "canonical_inputs": hashes,
        "owner_receipts": owner_receipts,
        "missing_or_blocked": missing,
        "authority_effect": "none",
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''


READINESS_RUNNER = r'''#!/usr/bin/env python3
"""Record the bounded post-fixture Spellcraft lifecycle decision."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--closure", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    spells_root = Path.cwd().resolve()
    closure_path = spells_root / args.closure
    closure = json.loads(closure_path.read_text(encoding="utf-8"))
    if closure.get("status") != "pass":
        return 1
    content = closure_path.read_bytes()
    decision = {
        "schema_version": "dfe-lifecycle-decision.v1",
        "unit_id": "READINESS-DFE-001",
        "status": "pass",
        "owner": "spellcraft",
        "source_closure": {
            "path": args.closure,
            "sha256": hashlib.sha256(content).hexdigest(),
            "size_bytes": len(content),
        },
        "decision": "authorize-paired-real-workflow-experiment-proposal",
        "rationale": "Synthetic fixtures can justify a paired workflow proposal, not canonical adoption.",
        "experiment_harness_status": "not_applicable",
        "experiment_harness_reason": "The fixture work pack is its own bounded deterministic harness; reusable real-workflow validation is the selected next proposal.",
        "selected_swu": None,
        "promotion": False,
        "publication": False,
        "authority_effect": "none",
        "successor": None,
    }
    output = spells_root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(decision, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


CLOSEOUT_CONTRACT = """# Task Session Closeout Contract

## Current Owner Route

Task Session execution and lifecycle ownership remain distinct:

- Task Session owns one selected SWU and its terminal source receipt.
- `invoke:refresh:apply-approved` is the only automatic closeout owner route.
- Spellcraft remains the experiment lifecycle owner and owns admission plus the
  final lifecycle decision.

The closeout hop is bookkeeping only. It cannot implement another unit,
select a successor, change authority, promote, publish, or deploy.

## Baseline Binding

Before mutation, the selected Task Session writes:

```text
spells/goal/development/decision-frontier-experiment/session-evidence/<SWU-ID>/baseline.json
```

It contains `swu_id`, `session_id`, exact task-local target inventory,
per-target existence/kind/SHA-256, scoped porcelain state, and a canonical
baseline digest. Missing future files are `exists: false`; globs are forbidden.

## Terminal Source Receipt

The executor writes:

```text
spells/goal/development/decision-frontier-experiment/session-evidence/<SWU-ID>/task-session-receipt.json
```

It must validate against `TASK-SESSION-RECEIPT.schema.json` and the semantic
validator in `work-pack/shared/validate-task-session-receipt.py`. A pass binds
the exact work-pack digest, unit/step identity, baseline, material/output
partition, artifacts, validation, empty blockers, empty undeclared writes,
authority effect `none`, and one eligible but unselected successor.

## Closeout Owner Receipt

The exact closeout route writes:

```text
spells/goal/development/decision-frontier-experiment/session-evidence/<SWU-ID>/owner-receipt.json
```

It validates against `CLOSEOUT-RECEIPT.schema.json` and records
`owner: invoke:refresh:apply-approved`, `lifecycle_owner: spellcraft`, the
source-receipt digest, re-run validation evidence, exact validated targets,
admitted delta classes, empty blockers, and one eligible but unselected
successor.

## Allowed Closeout Delta Classes

- `evidence_added`
- `blocker_opened`
- `blocker_resolved`
- `status_changed`
- `route_changed`

Implementation, deletion, canonical authority change, tracker mutation,
private export, successor selection, promotion, publication, and deployment
are forbidden.

## Successor Rule

A successor becomes eligible only when all predecessor closeout receipts pass
and no blocker affects its boundary. Eligibility never implies selection.
The outer `task-session-until-blocker` controller may select the unique
successor only under the user's explicit series authorization.
"""


def revised_markdown(path: str, replacements: list[tuple[str, str]]) -> str:
    value = (REPOSITORY_ROOT / path).read_text(encoding="utf-8")
    for old, new in replacements:
        value = value.replace(old, new)
    return value


def prepare() -> list[str]:
    command_matrix_path = str(INVOKE_RUN / "work-pack/shared/COMMAND-MATRIX.json")
    terminal_schema_path = str(INVOKE_RUN / "TASK-SESSION-RECEIPT.schema.json")
    closeout_schema_path = str(INVOKE_RUN / "CLOSEOUT-RECEIPT.schema.json")
    validator_path = str(
        INVOKE_RUN / "work-pack/shared/validate-task-session-receipt.py"
    )
    closeout_runner_path = str(INVOKE_RUN / "work-pack/shared/closeout_sync.py")
    closure_runner_path = str(INVOKE_RUN / "work-pack/shared/run_closure.py")
    readiness_runner_path = str(
        INVOKE_RUN / "work-pack/shared/record_lifecycle_decision.py"
    )
    continuation_path = str(INVOKE_RUN / "CONTINUATION.json")

    write_json(command_matrix_path, build_command_matrix())
    write_json(terminal_schema_path, TERMINAL_SCHEMA)
    write_json(closeout_schema_path, CLOSEOUT_SCHEMA)
    write_text(validator_path, SEMANTIC_VALIDATOR)
    write_text(closeout_runner_path, CLOSEOUT_SYNC)
    write_text(closure_runner_path, CLOSURE_RUNNER)
    write_text(readiness_runner_path, READINESS_RUNNER)
    write_json(
        continuation_path,
        {
            "schema_version": "1.0.0",
            "state": "ready-for-spellcraft-admission",
            "work_pack": str(INVOKE_RUN / "WORK-PACK.md"),
            "first_selectable_swu": "SWU-DFE-001",
            "selected_swu": None,
            "selection_allowed": False,
            "series_authorization": "execute-work-pack-until-blocker",
            "next_route": "spellcraft:validate",
            "authority_effect": "none",
        },
    )

    closeout_target = str(INVOKE_RUN / "work-pack/shared/CLOSEOUT-CONTRACT.md")
    write_text(closeout_target, CLOSEOUT_CONTRACT)

    work_pack_path = str(INVOKE_RUN / "WORK-PACK.md")
    work_pack_replacements = [
        (
            "| closeoutSyncStatus | pass |",
            "| closeoutSyncStatus | pass; current owner route `invoke:refresh:apply-approved` |",
        ),
        (
            "| SWU-DFE-001 | [inventory](work-pack/tasks/TASK-DFE-CONTRACT.md#exact-write-scope) | contract and graph mutants | Task Session -> Spellcraft | SWU-DFE-002 eligible |",
            "| SWU-DFE-001 | [inventory](work-pack/tasks/TASK-DFE-CONTRACT.md#exact-write-scope) | contract and graph mutants | Task Session -> Invoke Refresh under Spellcraft lifecycle | SWU-DFE-002 eligible |",
        ),
    ]
    current_work_pack = (REPOSITORY_ROOT / work_pack_path).read_text(
        encoding="utf-8"
    )
    if "- [command matrix]" not in current_work_pack:
        work_pack_replacements.append(
            (
                "- [closeout contract](work-pack/shared/CLOSEOUT-CONTRACT.md)",
                "- [closeout contract](work-pack/shared/CLOSEOUT-CONTRACT.md)\n"
                "- [command matrix](work-pack/shared/COMMAND-MATRIX.json)\n"
                "- [terminal receipt schema](TASK-SESSION-RECEIPT.schema.json)\n"
                "- [closeout receipt schema](CLOSEOUT-RECEIPT.schema.json)\n"
                "- [continuation state](CONTINUATION.json)",
            )
        )
    work_pack = revised_markdown(work_pack_path, work_pack_replacements)
    write_text(work_pack_path, work_pack)

    execution_pack_path = str(INVOKE_RUN / "EXECUTION-PACK.md")
    execution_pack = revised_markdown(
        execution_pack_path,
        [
            (
                "-> Spellcraft owner validation",
                "-> Invoke Refresh closeout under the Spellcraft lifecycle boundary",
            ),
            (
                "- predecessor owner receipts;",
                "- predecessor Invoke Refresh closeout receipts;",
            ),
        ],
    )
    write_text(execution_pack_path, execution_pack)

    task_paths = [
        str(INVOKE_RUN / "work-pack/tasks/TASK-DFE-CONTRACT.md"),
        str(INVOKE_RUN / "work-pack/tasks/TASK-DFE-REDUCER.md"),
        str(INVOKE_RUN / "work-pack/tasks/TASK-DFE-CLAIM.md"),
        str(INVOKE_RUN / "work-pack/tasks/TASK-DFE-RECONCILE.md"),
        str(INVOKE_RUN / "work-pack/tasks/TASK-DFE-BOUNDARY.md"),
    ]
    for path in task_paths:
        content = revised_markdown(
            path,
            [
                ("Spellcraft closeout", "Invoke Refresh closeout"),
                ("Spellcraft receipt", "Invoke Refresh closeout receipt"),
                ("Spellcraft replays", "The Invoke Refresh owner replays"),
                ("Spellcraft validates", "The Invoke Refresh owner validates"),
                ("terminal and owner receipts", "terminal and closeout receipts"),
                ("terminal and Spellcraft receipts", "terminal and closeout receipts"),
            ],
        )
        write_text(path, content)

    targets = [
        command_matrix_path,
        terminal_schema_path,
        closeout_schema_path,
        validator_path,
        closeout_runner_path,
        closure_runner_path,
        readiness_runner_path,
        continuation_path,
        closeout_target,
        work_pack_path,
        execution_pack_path,
        *task_paths,
    ]
    source_paths = [
        str(INVOKE_RUN / "WORK-PACK.md"),
        str(INVOKE_RUN / "EXECUTION-PACK.md"),
        str(INVOKE_RUN / "work-pack/shared/CLOSEOUT-CONTRACT.md"),
        "arcana/task-session/schemas/mutation-admission-request.schema.json",
    ]
    package = {
        "schema_version": "1.0.0",
        "package_id": "goal-dfe-runtime-admission-control-refresh",
        "mutation_mode": "apply-approved",
        "mutation_state": "materialized",
        "lifecycle_owner": "invoke",
        "authority_class": "public",
        "publication_class": "public",
        "source_artifacts": [
            {**exact_ref(path), "authority_class": "public"} for path in source_paths
        ],
        "changes": [
            {
                "target_path": path,
                "operation": "update"
                if (REPOSITORY_ROOT / path).exists()
                else "create",
                "output_ref": staged_ref(path),
            }
            for path in targets
        ],
        "target_inventory": [
            {
                "target_path": path,
                "lifecycle_owner": "invoke",
                "authority_class": "public",
                "publication_class": "public",
                "dependency_ids": [],
            }
            for path in targets
        ],
        "dependencies": [],
        "mirror_groups": [],
        "approval": {
            "class": "explicit-apply",
            "owner": "invoke",
            "scope_paths": targets,
            "authority_classes": ["public"],
            "publication_classes": ["public"],
        },
        "validation_commands": [
            f"python3 -m json.tool {command_matrix_path}",
            f"python3 -m json.tool {terminal_schema_path}",
            f"python3 -m json.tool {closeout_schema_path}",
            f"python3 -m json.tool {continuation_path}",
            f"python3 -m py_compile {validator_path} {closeout_runner_path} {closure_runner_path} {readiness_runner_path}",
        ],
    }
    package_path = REPOSITORY_ROOT / REFRESH_RUN / "material-package.json"
    package_path.parent.mkdir(parents=True, exist_ok=True)
    package_path.write_text(
        json.dumps(package, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return targets


def main() -> int:
    targets = prepare()
    print(
        json.dumps(
            {
                "package": str(REFRESH_RUN / "material-package.json"),
                "staged_targets": len(targets),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
