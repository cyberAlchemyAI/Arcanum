#!/usr/bin/env python3
"""Stage-specific adapter that loads the exact canonical downstream consumer.

The adapter exists only for the two JSON-schema stages and the governance
prepare stage in the public integration fixture. The mapping is closed: schema
consumers are parsed and checked, while governance starts the exact runner's
generic prepare regression against the invocation-bound projection.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator


CONSUMERS = {
    "task_session_governance_runner": (
        "arcanum/arcana/task-session/scripts/prepare_live_execution_entry.py",
        ".agents/skills/task-session/scripts/prepare_live_execution_entry.py",
        ".claude/skills/task-session/scripts/prepare_live_execution_entry.py",
    ),
    "invoke_closeout": "arcanum/spells/invoke/schemas/precloseout-refresh-closeout-receipt.schema.json",
    "task_session_terminal": "arcanum/arcana/task-session/schemas/governance-terminal-receipt.schema.json",
}

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
LIVE_ENTRY_BUDGET_SCHEMA = (
    PACKAGE_ROOT / "schemas/preacceptance-live-entry-rehearsal-budget-v1.schema.json"
)
LIVE_ENTRY_REHEARSAL_HARD_MAXIMUM_SECONDS = 3600
LIVE_ENTRY_MAX_INVOCATIONS = 7
LIVE_ENTRY_MAX_INPUT_REF_OCCURRENCES = 16384
LIVE_ENTRY_MAX_UNIQUE_INPUT_REFS = 16384
LIVE_ENTRY_MAX_INPUT_SIZE_BYTES = 2147483648
LIVE_ENTRY_MAX_OUTPUT_PATHS = 1024
TERMINALIZATION_INVOCATION_COUNT = 3
TERMINALIZATION_INVOCATION_TIMEOUT_SECONDS = 60


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def ceiling_divide(value: int, divisor: int) -> int:
    return (value + divisor - 1) // divisor


def derive_live_entry_rehearsal_budget(
    request_ref: dict[str, Any],
    preparation_ref: dict[str, Any],
    preparation: dict[str, Any],
    failure_stop_after: str,
) -> dict[str, Any]:
    """Derive both outer deadlines from the exact sequential preparation graph."""
    steps = preparation.get("preparation_steps")
    if not isinstance(steps, list) or not steps:
        raise ValueError("live-entry budget requires preparation steps")
    step_ids = [step.get("step_id") for step in steps]
    if len(step_ids) != len(set(step_ids)) or failure_stop_after not in step_ids:
        raise ValueError("live-entry budget requires unique steps and an exact stop boundary")
    invocations = [
        preparation["owner_acceptance_validation"],
        *(step["invocation"] for step in steps),
        preparation["governance_runner"],
    ]
    if len(invocations) > LIVE_ENTRY_MAX_INVOCATIONS:
        raise ValueError("live-entry invocation count exceeds the hard maximum")

    references = [request_ref, preparation_ref]
    for invocation in invocations:
        references.extend(
            [invocation["input_closure_ref"], *invocation["input_refs"]]
        )
    if len(references) > LIVE_ENTRY_MAX_INPUT_REF_OCCURRENCES:
        raise ValueError("live-entry exact input occurrences exceed the hard maximum")
    unique_refs: dict[str, dict[str, Any]] = {}
    for reference in references:
        path = reference.get("path")
        if not isinstance(path, str):
            raise ValueError("live-entry workload contains a malformed exact input")
        prior = unique_refs.get(path)
        if prior is not None and prior != reference:
            raise ValueError(f"live-entry workload contains conflicting input refs: {path}")
        unique_refs[path] = reference
    unique_size = sum(reference["size_bytes"] for reference in unique_refs.values())
    if len(unique_refs) > LIVE_ENTRY_MAX_UNIQUE_INPUT_REFS:
        raise ValueError("live-entry unique exact inputs exceed the hard maximum")
    if unique_size > LIVE_ENTRY_MAX_INPUT_SIZE_BYTES:
        raise ValueError("live-entry exact input bytes exceed the hard maximum")

    output_paths = {
        preparation["preparation_receipt_path"],
        *(path for step in steps for path in step["output_paths"]),
        *preparation["governance_runner"]["output_paths"],
    }
    if len(output_paths) > LIVE_ENTRY_MAX_OUTPUT_PATHS:
        raise ValueError("live-entry exact outputs exceed the hard maximum")

    invocation_ceiling = sum(item["timeout_seconds"] for item in invocations)
    stop_index = step_ids.index(failure_stop_after)
    failure_stop_ceiling = preparation["owner_acceptance_validation"][
        "timeout_seconds"
    ] + sum(
        step["invocation"]["timeout_seconds"] for step in steps[: stop_index + 1]
    )
    workload_overhead = (
        30
        + 5 * ceiling_divide(len(references), 256)
        + 5 * ceiling_divide(unique_size, 67108864)
        + 5 * ceiling_divide(len(output_paths), 64)
    )
    success_timeout = invocation_ceiling + workload_overhead
    failure_stop_timeout = failure_stop_ceiling + workload_overhead
    stage_timeout = (
        success_timeout
        + failure_stop_timeout
        + TERMINALIZATION_INVOCATION_COUNT
        * TERMINALIZATION_INVOCATION_TIMEOUT_SECONDS
        + workload_overhead
    )
    if max(success_timeout, failure_stop_timeout, stage_timeout) > (
        LIVE_ENTRY_REHEARSAL_HARD_MAXIMUM_SECONDS
    ):
        raise ValueError(
            "derived live-entry rehearsal budget exceeds the 3600-second hard maximum"
        )
    budget = {
        "schema_version": "invoke.preacceptance-live-entry-rehearsal-budget.v1",
        "derivation_version": "task-session.sequential-live-entry-workload.v1",
        "invocation_count": len(invocations),
        "declared_invocation_timeout_seconds": invocation_ceiling,
        "failure_stop_after": failure_stop_after,
        "failure_stop_invocation_timeout_seconds": failure_stop_ceiling,
        "exact_input_ref_occurrence_count": len(references),
        "unique_input_ref_count": len(unique_refs),
        "unique_input_size_bytes": unique_size,
        "exact_output_path_count": len(output_paths),
        "workload_overhead_seconds": workload_overhead,
        "success_coordinator_timeout_seconds": success_timeout,
        "failure_stop_coordinator_timeout_seconds": failure_stop_timeout,
        "terminalization_invocation_count": TERMINALIZATION_INVOCATION_COUNT,
        "terminalization_invocation_timeout_seconds": (
            TERMINALIZATION_INVOCATION_TIMEOUT_SECONDS
        ),
        "stage_timeout_seconds": stage_timeout,
        "hard_maximum_seconds": LIVE_ENTRY_REHEARSAL_HARD_MAXIMUM_SECONDS,
    }
    budget["budget_digest"] = canonical_digest(budget)
    return budget


def validate_live_entry_rehearsal_budget(
    declared: Any, expected: dict[str, Any]
) -> dict[str, Any]:
    if not isinstance(declared, dict):
        raise ValueError("governance rehearsal lacks its live-entry workload budget")
    schema = json.loads(LIVE_ENTRY_BUDGET_SCHEMA.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(declared),
        key=lambda item: list(item.absolute_path),
    )
    if errors:
        first = errors[0]
        raise ValueError(
            "live-entry rehearsal budget schema invalid at "
            f"{'/'.join(map(str, first.absolute_path)) or '<root>'}: {first.message}"
        )
    digest_projection = dict(declared)
    observed_digest = digest_projection.pop("budget_digest")
    if observed_digest != canonical_digest(digest_projection):
        raise ValueError("live-entry rehearsal budget digest mismatch")
    if declared != expected:
        raise ValueError("live-entry rehearsal budget is stale or underspecified")
    return declared


def run_bounded(command: list[str], timeout_seconds: int, **kwargs: Any) -> Any:
    """Keep every real consumer under an explicit finite hard deadline."""
    return subprocess.run(command, timeout=timeout_seconds, **kwargs)


def safe_path(root: Path, raw_path: str) -> Path:
    relative = PurePosixPath(raw_path)
    if relative.is_absolute() or ".." in relative.parts or "\\" in raw_path:
        raise ValueError(f"unsafe consumer path: {raw_path}")
    candidate = (root / relative).resolve()
    candidate.relative_to(root.resolve())
    if not candidate.is_file():
        raise ValueError(f"missing consumer: {raw_path}")
    return candidate


def exact_ref(root: Path, path: Path) -> dict[str, Any]:
    content = path.read_bytes()
    return {
        "path": path.resolve().relative_to(root.resolve()).as_posix(),
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def exact_ref_document(root: Path, reference: dict[str, Any]) -> dict[str, Any]:
    source = safe_path(root, reference["path"])
    if exact_ref(root, source) != reference:
        raise ValueError(f"stale exact reference: {reference['path']}")
    document = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise ValueError(f"JSON object required: {reference['path']}")
    return document


def collect_exact_refs(value: Any) -> list[dict[str, Any]]:
    references: list[dict[str, Any]] = []
    if isinstance(value, dict):
        if (
            set(value) == {"path", "sha256", "size_bytes"}
            and isinstance(value["path"], str)
            and not PurePosixPath(value["path"]).is_absolute()
        ):
            references.append(value)
        else:
            for item in value.values():
                references.extend(collect_exact_refs(item))
    elif isinstance(value, list):
        for item in value:
            references.extend(collect_exact_refs(item))
    return references


def copy_exact_input(
    repository_root: Path,
    rehearsal_repository: Path,
    reference: dict[str, Any],
) -> None:
    source = safe_path(repository_root, reference["path"])
    if exact_ref(repository_root, source) != reference:
        raise ValueError(f"stale rehearsal input: {reference['path']}")
    target = rehearsal_repository / reference["path"]
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def path_state(root: Path, raw_path: str) -> dict[str, Any]:
    path = root / raw_path
    if not path.exists():
        return {"state": "absent"}
    if not path.is_file():
        return {"state": "non-file"}
    content = path.read_bytes()
    return {
        "state": "present",
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def canonical_partition(partition: dict[str, Any]) -> dict[str, Any]:
    result = {
        "schema_version": partition["schema_version"],
        "executor_write_scopes": sorted(partition["executor_write_scopes"]),
        "terminal_receipt_scope": partition["terminal_receipt_scope"],
        "lifecycle_owner_scopes": sorted(
            partition["lifecycle_owner_scopes"],
            key=lambda item: item["path"],
        ),
    }
    if "control_evidence_partition" in partition:
        result["control_evidence_partition"] = partition["control_evidence_partition"]
        result["exact_union_scope"] = sorted(partition["exact_union_scope"])
    return result


def repository_snapshot(root: Path) -> dict[str, dict[str, Any]]:
    return {
        path.relative_to(root).as_posix(): path_state(root, path.relative_to(root).as_posix())
        for path in sorted(root.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


def rehearse_governance(
    repository_root: Path,
    consumer: Path,
    projection_document: dict[str, Any],
    rehearsal_root: Path,
) -> tuple[int, dict[str, Any]]:
    contract = projection_document.get("governance_prepare_rehearsal")
    if not isinstance(contract, dict) or contract.get("schema_version") != (
        "invoke.preacceptance-governance-prepare-rehearsal.v2"
    ):
        raise ValueError("projection lacks the v2 governance rehearsal contract")
    request_ref = contract.get("request_ref")
    preparation_ref = contract.get("preparation_ref")
    selected_route = contract.get("selected_route")
    expected_partition = contract.get("route_scope_partition")
    run_dir = contract.get("run_dir")
    if not all(
        (
            isinstance(request_ref, dict),
            isinstance(preparation_ref, dict),
            isinstance(selected_route, dict),
            isinstance(expected_partition, dict),
            isinstance(run_dir, str),
        )
    ):
        raise ValueError("governance rehearsal contract is incomplete")
    safe_path_parent = PurePosixPath(run_dir)
    if (
        safe_path_parent.is_absolute()
        or ".." in safe_path_parent.parts
        or not safe_path_parent.parts
    ):
        raise ValueError("unsafe governance rehearsal run directory")

    request = exact_ref_document(repository_root, request_ref)
    preparation = exact_ref_document(repository_root, preparation_ref)
    failure_stop = contract.get("failure_stop_after")
    if failure_stop not in {
        "readiness", "selection", "fast-entry", "context", "admission"
    }:
        raise ValueError("live topology rehearsal lacks a typed failure stop boundary")
    expected_budget = derive_live_entry_rehearsal_budget(
        request_ref,
        preparation_ref,
        preparation,
        failure_stop,
    )
    rehearsal_budget = validate_live_entry_rehearsal_budget(
        contract.get("live_entry_rehearsal_budget"), expected_budget
    )
    if request.get("fast_execution_entry", {}).get(
        "route_scope_partition"
    ) != expected_partition:
        raise ValueError("projection partition differs from governance request")
    guard_ref = request["fast_execution_entry"]["request_ref"]
    guard_request = exact_ref_document(repository_root, guard_ref)
    actual_route = guard_request["execution_binding"]["current_route"]
    if actual_route != selected_route:
        raise ValueError("projection selected route differs from fast-entry binding")
    partition_paths = [
        *expected_partition["executor_write_scopes"],
        expected_partition["terminal_receipt_scope"],
        *(
            item["path"]
            for item in expected_partition["lifecycle_owner_scopes"]
        ),
        *expected_partition.get("control_evidence_partition", {}).get(
            "exact_union_scope", []
        ),
    ]
    if sorted(partition_paths) != sorted(actual_route["write_scope"]):
        raise ValueError("projection partition does not equal selected route scope")

    rehearsal_repository = rehearsal_root / "governance-repository"
    rehearsal_repository.mkdir(parents=True, exist_ok=False)
    consumer_relative = consumer.relative_to(repository_root)
    package_relative = consumer_relative.parent.parent
    shutil.copytree(
        repository_root / package_relative,
        rehearsal_repository / package_relative,
        dirs_exist_ok=True,
    )
    readiness_candidates = (
        package_relative.parent / "implementation-readiness",
        package_relative.parents[1] / "spells/implementation-readiness",
    )
    readiness_relative = next(
        (
            candidate
            for candidate in readiness_candidates
            if (repository_root / candidate).is_dir()
        ),
        None,
    )
    if readiness_relative is None:
        raise ValueError("missing Implementation Readiness consumer dependency")
    shutil.copytree(
        repository_root / readiness_relative,
        rehearsal_repository / readiness_relative,
        dirs_exist_ok=True,
    )
    all_refs = [
        request_ref,
        preparation_ref,
        *collect_exact_refs(request),
        *collect_exact_refs(preparation),
    ]
    unique_refs = {reference["path"]: reference for reference in all_refs}
    declared_future_postimages = {
        item["expected_postimage_ref"]["path"]: item["expected_postimage_ref"]
        for item in expected_partition.get("control_evidence_partition", {}).get("outputs", [])
        if isinstance(item.get("expected_postimage_ref"), dict)
    }
    for reference in unique_refs.values():
        if not (repository_root / reference["path"]).exists():
            if declared_future_postimages.get(reference["path"]) == reference:
                continue
            raise ValueError(f"missing exact rehearsal input: {reference['path']}")
        copy_exact_input(repository_root, rehearsal_repository, reference)

    control_partition = expected_partition.get("control_evidence_partition")
    failure_profile = request.get("failure_terminalization")
    if not isinstance(control_partition, dict) or not isinstance(failure_profile, dict):
        raise ValueError("live topology rehearsal requires control and failure profiles")
    if request.get("control_evidence_partition") != control_partition:
        raise ValueError("request and route live control partitions differ")
    if failure_profile.get("attempt_id") != request.get("run_id"):
        raise ValueError("failure terminalization attempt differs from governance run")
    if failure_profile.get("terminal_receipt_path") != expected_partition["terminal_receipt_scope"]:
        raise ValueError("failure terminal output differs from terminal partition")
    lifecycle_by_path = {
        item["path"]: (item["owner_capability"], item["write_class"])
        for item in expected_partition["lifecycle_owner_scopes"]
    }
    if lifecycle_by_path.get(failure_profile.get("invoke_owner_receipt_path")) != (
        "invoke", "owner-closeout-receipt"
    ):
        raise ValueError("failure Invoke block receipt is outside its lifecycle scope")
    if lifecycle_by_path.get(failure_profile.get("continuity_cursor_path")) != (
        "task-session", "continuity-cursor"
    ):
        raise ValueError("failure continuity cursor is outside its lifecycle scope")

    invoke_relative = Path("arcanum/spells/invoke")
    shutil.copytree(
        repository_root / invoke_relative,
        rehearsal_repository / invoke_relative,
        dirs_exist_ok=True,
    )
    failure_repository = rehearsal_root / "governance-failure-repository"
    shutil.copytree(rehearsal_repository, failure_repository)

    before = repository_snapshot(rehearsal_repository)
    environment = {"PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": "/tmp"}
    completed = run_bounded(
        [
            sys.executable,
            str(rehearsal_repository / consumer_relative),
            "--repo-root",
            str(rehearsal_repository),
            "--request",
            request_ref["path"],
            "--preparation",
            preparation_ref["path"],
            "--mode",
            "shadow",
            "--shadow-root",
            str(rehearsal_repository),
        ],
        cwd=rehearsal_repository,
        check=False,
        capture_output=True,
        timeout_seconds=rehearsal_budget["success_coordinator_timeout_seconds"],
        env=environment,
    )
    if completed.returncode != 0:
        return completed.returncode, {"runner_stderr_sha256": hashlib.sha256(completed.stderr).hexdigest()}
    status = json.loads(completed.stdout)
    ticket_path = rehearsal_repository / run_dir / "execution-ticket.json"
    ticket = json.loads(ticket_path.read_text(encoding="utf-8"))
    if status.get("result") != "pass" or status.get("mode") != "shadow":
        raise ValueError("live-entry coordinator did not pass the shadow success mode")
    if ticket.get("fast_execution_entry", {}).get(
        "route_scope_partition"
    ) != canonical_partition(expected_partition):
        raise ValueError("execution ticket lost the projection-bound route partition")
    if ticket.get("live_execution_entry_preparation_receipt_ref") != status.get(
        "preparation_receipt_ref"
    ):
        raise ValueError("execution ticket lost the exact live preparation receipt")
    ledger_path = request["plan_admission"]["consumption_ledger_path"]
    if (rehearsal_repository / ledger_path).exists():
        raise ValueError("governance prepare consumed the admission token")
    after = repository_snapshot(rehearsal_repository)
    observed_success_writes = sorted(
        path for path in set(before) | set(after) if before.get(path) != after.get(path)
    )
    declared_controls = set(control_partition["exact_union_scope"])
    if not set(observed_success_writes) <= declared_controls:
        raise ValueError(
            "governance prepare wrote outside live control authority: "
            + ", ".join(sorted(set(observed_success_writes) - declared_controls))
        )
    if observed_success_writes != sorted(status.get("observed_writes", [])):
        raise ValueError("live-entry coordinator receipt differs from observed topology")

    terminalizer = failure_repository / package_relative / "scripts/terminalize_pre_execution_failure.py"
    handler = failure_repository / invoke_relative / "scripts/handle_pre_execution_block.py"
    continuity = failure_repository / package_relative / "scripts/emit_pre_execution_failure_continuity.py"
    failure_before = repository_snapshot(failure_repository)
    coordinator_stop = run_bounded(
        [sys.executable, str(failure_repository / consumer_relative), "--repo-root", str(failure_repository), "--request", request_ref["path"], "--preparation", preparation_ref["path"], "--mode", "shadow", "--shadow-root", str(failure_repository), "--stop-after", failure_stop],
        cwd=failure_repository,
        check=False,
        capture_output=True,
        timeout_seconds=rehearsal_budget["failure_stop_coordinator_timeout_seconds"],
        env=environment,
    )
    if coordinator_stop.returncode != 0:
        return coordinator_stop.returncode, {"failure_stop_stderr_sha256": hashlib.sha256(coordinator_stop.stderr).hexdigest()}
    stopped = json.loads(coordinator_stop.stdout)
    if stopped.get("result") != "deliberate-pre-execution-stop":
        raise ValueError("coordinator did not reach the deliberate failure stop")
    commands = [
        [sys.executable, str(terminalizer), "--repo-root", str(failure_repository), "--request", request_ref["path"]],
        [sys.executable, str(handler), "--repo-root", str(failure_repository), "--request", request_ref["path"], "--terminal-receipt", failure_profile["terminal_receipt_path"]],
        [sys.executable, str(continuity), "--repo-root", str(failure_repository), "--request", request_ref["path"], "--terminal-receipt", failure_profile["terminal_receipt_path"], "--owner-receipt", failure_profile["invoke_owner_receipt_path"]],
    ]
    failure_results = []
    for command in commands:
        result = run_bounded(
            command,
            rehearsal_budget["terminalization_invocation_timeout_seconds"],
            cwd=failure_repository,
            check=False,
            capture_output=True,
            env=environment,
        )
        if result.returncode != 0:
            return result.returncode, {"failure_terminalization_stderr_sha256": hashlib.sha256(result.stderr).hexdigest()}
        failure_results.append(json.loads(result.stdout))
    failure_after = repository_snapshot(failure_repository)
    observed_failure_writes = sorted(
        path for path in set(failure_before) | set(failure_after) if failure_before.get(path) != failure_after.get(path)
    )
    expected_failure_writes = sorted([*stopped["observed_writes"], failure_profile["terminal_receipt_path"], failure_profile["invoke_owner_receipt_path"], failure_profile["continuity_cursor_path"]])
    if observed_failure_writes != expected_failure_writes:
        raise ValueError("pre-execution failure terminalization wrote outside its three exact outputs")
    if (failure_repository / run_dir).exists():
        raise ValueError("pre-execution failure path fabricated governance preparation phases")
    return 0, {
        "request_ref": request_ref,
        "selected_route_digest": hashlib.sha256(
            json.dumps(actual_route, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "route_scope_partition": canonical_partition(expected_partition),
        "ticket_ref": exact_ref(rehearsal_repository, ticket_path),
        "admission_consumed": False,
        "live_entry_rehearsal_budget": rehearsal_budget,
        "success_mode": {
            "result": "pass",
            "observed_control_writes": observed_success_writes,
            "material_lifecycle_terminal_writes": [],
        },
        "pre_execution_failure_mode": {
            "result": "block",
            "observed_outputs": observed_failure_writes,
            "blocker_fingerprint": failure_results[0]["blocker_fingerprint"],
            "admission_consumed": False,
            "successor_executed": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", required=True, choices=sorted(CONSUMERS))
    parser.add_argument("--consumer", required=True)
    parser.add_argument("--projection", required=True)
    parser.add_argument("--rehearsal-root", required=True)
    args = parser.parse_args()

    expected = CONSUMERS[args.stage]
    admitted_consumers = (expected,) if isinstance(expected, str) else expected
    if args.consumer not in admitted_consumers:
        raise ValueError(f"consumer mismatch for {args.stage}: {args.consumer}")
    repository_root = Path.cwd().resolve()
    consumer = safe_path(repository_root, args.consumer)
    projection = safe_path(repository_root, args.projection)
    projection_document = json.loads(projection.read_text(encoding="utf-8"))
    if not isinstance(projection_document, dict):
        raise ValueError("execution projection must be a JSON object")
    projection_digest = hashlib.sha256(projection.read_bytes()).hexdigest()
    rehearsal_root = Path(args.rehearsal_root).resolve()
    rehearsal_root.mkdir(parents=True, exist_ok=True)

    evidence: dict[str, Any] = {}
    if args.stage == "task_session_governance_runner":
        return_code, evidence = rehearse_governance(
            repository_root,
            consumer,
            projection_document,
            rehearsal_root,
        )
    else:
        schema = json.loads(consumer.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        return_code = 0

    if return_code == 0:
        output = rehearsal_root / f"{args.stage}.json"
        output.write_text(
            json.dumps(
                {
                    "consumer": args.consumer,
                    "projection": args.projection,
                    "projection_digest": projection_digest,
                    "result": "pass",
                    "stage": args.stage,
                    **evidence,
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
