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
        "arcanum/arcana/task-session/scripts/task-session-governance-runner.py",
        ".agents/skills/task-session/scripts/task-session-governance-runner.py",
        ".claude/skills/task-session/scripts/task-session-governance-runner.py",
    ),
    "invoke_closeout": "arcanum/spells/invoke/schemas/precloseout-refresh-closeout-receipt.schema.json",
    "task_session_terminal": "arcanum/arcana/task-session/schemas/governance-terminal-receipt.schema.json",
}


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
        if set(value) == {"path", "sha256", "size_bytes"}:
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
    return {
        "schema_version": partition["schema_version"],
        "executor_write_scopes": sorted(partition["executor_write_scopes"]),
        "terminal_receipt_scope": partition["terminal_receipt_scope"],
        "lifecycle_owner_scopes": sorted(
            partition["lifecycle_owner_scopes"],
            key=lambda item: item["path"],
        ),
    }


def rehearse_governance(
    repository_root: Path,
    consumer: Path,
    projection_document: dict[str, Any],
    rehearsal_root: Path,
) -> tuple[int, dict[str, Any]]:
    contract = projection_document.get("governance_prepare_rehearsal")
    if not isinstance(contract, dict) or contract.get("schema_version") != (
        "invoke.preacceptance-governance-prepare-rehearsal.v1"
    ):
        raise ValueError("projection lacks the versioned governance rehearsal contract")
    request_ref = contract.get("request_ref")
    selected_route = contract.get("selected_route")
    expected_partition = contract.get("route_scope_partition")
    run_dir = contract.get("run_dir")
    if not all(
        (
            isinstance(request_ref, dict),
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
    all_refs = [request_ref, *collect_exact_refs(request)]
    unique_refs = {reference["path"]: reference for reference in all_refs}
    for reference in unique_refs.values():
        copy_exact_input(repository_root, rehearsal_repository, reference)

    before = {
        path: path_state(rehearsal_repository, path)
        for path in actual_route["write_scope"]
    }
    completed = subprocess.run(
        [
            sys.executable,
            str(rehearsal_repository / consumer_relative),
            "prepare",
            "--repo-root",
            str(rehearsal_repository),
            "--request",
            request_ref["path"],
            "--run-dir",
            run_dir,
        ],
        cwd=rehearsal_repository,
        check=False,
        capture_output=True,
        timeout=60,
    )
    if completed.returncode != 0:
        return completed.returncode, {"runner_stderr_sha256": hashlib.sha256(completed.stderr).hexdigest()}
    status = json.loads(completed.stdout)
    ticket_path = rehearsal_repository / run_dir / "execution-ticket.json"
    ticket = json.loads(ticket_path.read_text(encoding="utf-8"))
    if status.get("current_phase") != "ticketed" or status.get("writes_performed") != 0:
        raise ValueError("governance rehearsal did not stop at no-effect ticketed phase")
    if ticket.get("fast_execution_entry", {}).get(
        "route_scope_partition"
    ) != canonical_partition(expected_partition):
        raise ValueError("execution ticket lost the projection-bound route partition")
    ledger_path = request["plan_admission"]["consumption_ledger_path"]
    if (rehearsal_repository / ledger_path).exists():
        raise ValueError("governance prepare consumed the admission token")
    after = {
        path: path_state(rehearsal_repository, path)
        for path in actual_route["write_scope"]
    }
    if before != after:
        raise ValueError("governance prepare changed a selected-route path")
    return 0, {
        "request_ref": request_ref,
        "selected_route_digest": hashlib.sha256(
            json.dumps(actual_route, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "route_scope_partition": canonical_partition(expected_partition),
        "ticket_ref": exact_ref(rehearsal_repository, ticket_path),
        "admission_consumed": False,
        "route_paths_unchanged": True,
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
