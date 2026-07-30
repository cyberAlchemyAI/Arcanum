#!/usr/bin/env python3
"""Validate the SWU-TSGR-003 prepare/status runner family."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


OWNED = (
    "scripts/task-session-governance-runner.py",
    "development/fixtures/governance-runner-cases.json",
    "development/validate-governance-runner.py",
)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"top-level JSON must be an object: {path}")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_ref(root: Path, path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(root).as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "size_bytes": len(data),
    }


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def discover_canonical_task_session(source: Path) -> Path:
    if (source / "schemas/governance-run-request.schema.json").is_file():
        return source
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "arcanum/arcana/task-session"
        if (candidate / "schemas/governance-run-request.schema.json").is_file():
            return candidate
    raise ValueError("cannot discover canonical Task Session schemas")


def tree_manifest(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def runner_command(
    repo: Path, command: str, *, request: str | None = None
) -> list[str]:
    argv = [
        sys.executable,
        str(repo / "arcanum/arcana/task-session/scripts/task-session-governance-runner.py"),
        command,
        "--repo-root",
        str(repo),
    ]
    if request is not None:
        argv.extend(["--request", request])
    argv.extend(["--run-dir", "runs/run-1"])
    return argv


def invoke(argv: list[str]) -> tuple[int, dict[str, Any], str]:
    completed = subprocess.run(
        argv,
        check=False,
        capture_output=True,
        text=True,
        timeout=20,
    )
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise AssertionError(
            f"runner returned non-JSON stdout: {completed.stdout!r}"
        ) from error
    return completed.returncode, payload, completed.stderr


def scenario(
    root: Path,
    source_task_session: Path,
    canonical_task_session: Path,
    mutation: str | None = None,
) -> Path:
    repo = root / (mutation or "valid")
    runner_target = (
        repo / "arcanum/arcana/task-session/scripts/task-session-governance-runner.py"
    )
    runner_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(
        source_task_session / "scripts/task-session-governance-runner.py",
        runner_target,
    )
    schema_target = repo / "arcanum/arcana/task-session/schemas"
    schema_target.mkdir(parents=True, exist_ok=True)
    for name in (
        "governance-run-request.schema.json",
        "execution-ticket.schema.json",
        "governance-phase-receipt.schema.json",
        "executor-receipt.schema.json",
    ):
        shutil.copy2(canonical_task_session / "schemas" / name, schema_target / name)

    scenario_dir = repo / "scenario"
    scenario_dir.mkdir(parents=True)
    selected_rows = (
        "| `SWU-TSGR-003` | task | objective | deps | paths | checks | owner | selected |\n"
    )
    if mutation == "missing-selected-row":
        selected_rows = (
            "| `SWU-TSGR-003` | task | objective | deps | paths | checks | owner | blocked |\n"
        )
    elif mutation == "duplicate-selected-row":
        selected_rows += (
            "| `SWU-TSGR-004` | task | objective | deps | paths | checks | owner | selected |\n"
        )
    work_pack = scenario_dir / "WORK-PACK.md"
    work_pack.write_text(
        "# Synthetic Work Pack\n\n"
        "| SWU | Parent | Objective | Dependencies | Scope | Validation | Owner | Status |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
        + selected_rows,
        encoding="utf-8",
    )
    swu_contract = scenario_dir / "TASK.md"
    swu_contract.write_text(
        "# Synthetic Task\n\n## SWU-TSGR-003\n\nPrepare and status only.\n",
        encoding="utf-8",
    )

    controls_dir = scenario_dir / "controls"
    evaluation = controls_dir / "evaluation.json"
    admission = controls_dir / "admission.json"
    preflight = controls_dir / "preflight.json"
    write_json(
        evaluation,
        {
            "schema_version": "task-session.governance-evaluation-receipt.v1",
            "request_id": "evaluation-003",
            "evaluation_kind": "closeout-preflight",
            "outcome": "PROCEED",
        },
    )
    write_json(
        admission,
        {
            "schemaVersion": "1.2.0",
            "executionMode": "reusable-mutation",
            "writeProfile": "material-bound",
            "admissionVerdict": "admit",
            "mutationReady": True,
            "taskId": "TASK-TSGR-02",
            "swuId": "SWU-TSGR-003",
        },
    )
    write_json(
        preflight,
        {
            "schema_version": "task-session.closeout-preflight.v1",
            "task_id": "TASK-TSGR-02",
            "swu_id": "SWU-TSGR-003",
            "result": "PROCEED",
        },
    )

    request = {
        "schema_version": "task-session.governance-run-request.v1",
        "request_id": "request-003",
        "run_id": "synthetic-run-003",
        "work_pack_ref": exact_ref(repo, work_pack),
        "swu_ref": exact_ref(repo, swu_contract),
        "task_id": "TASK-TSGR-02",
        "swu_id": "SWU-TSGR-003",
        "control_refs": [
            exact_ref(repo, evaluation),
            exact_ref(repo, admission),
            exact_ref(repo, preflight),
        ],
        "execution_contract": {
            "allowed_writes": ["outputs/artifact.txt"],
            "declared_outputs": ["results/executor-result.json"],
            "validation_commands": [
                {
                    "command_id": "validate-artifact",
                    "argv": ["python3", "-m", "json.tool", "results/executor-result.json"],
                    "cwd": ".",
                    "timeout_seconds": 30,
                    "max_output_bytes": 4096,
                }
            ],
            "timeout_seconds": 60,
            "max_output_bytes": 8192,
        },
        "owner_identity": {
            "capability": "task-session",
            "subject": "synthetic-validator",
        },
        "idempotency_key": "synthetic.prepare.003",
        "closeout_contract": {
            "required_owner_capabilities": ["continuation-router", "invoke"],
            "continuation_policy": "emit-cursor-never-execute-successor",
            "terminal_receipt_path": "runs/run-1/terminal-receipt.json",
        },
    }
    if mutation == "stale-work-pack-digest":
        request["work_pack_ref"]["sha256"] = "0" * 64
    elif mutation == "stale-control-digest":
        request["control_refs"][0]["sha256"] = "0" * 64
    write_json(scenario_dir / "request.json", request)
    return repo


def assert_block_before_write(
    repo: Path, case_id: str
) -> tuple[bool, str]:
    code, payload, stderr = invoke(
        runner_command(repo, "prepare", request="scenario/request.json")
    )
    run_dir = repo / "runs/run-1"
    passed = (
        code == 2
        and payload.get("result") == "block"
        and payload.get("writes_performed") == 0
        and not run_dir.exists()
        and not stderr
    )
    return passed, f"{case_id}: code={code} run_exists={run_dir.exists()}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", choices=("prepare",), required=True)
    parser.add_argument("--task-session-dir")
    parser.add_argument("--material-inventory-manifest")
    args = parser.parse_args()

    source_task_session = (
        Path(args.task_session_dir).resolve()
        if args.task_session_dir
        else Path(__file__).resolve().parent.parent
    )
    canonical_task_session = discover_canonical_task_session(source_task_session)
    fixtures_path = (
        source_task_session / "development/fixtures/governance-runner-cases.json"
    )
    fixtures = load_json(fixtures_path)
    expected_ids = {case["case_id"] for case in fixtures["cases"]}
    results: list[tuple[str, bool, str]] = []

    with tempfile.TemporaryDirectory(prefix="task-session-runner-prepare-") as raw:
        temporary = Path(raw)
        valid = scenario(
            temporary, source_task_session, canonical_task_session, mutation=None
        )
        code, payload, stderr = invoke(
            runner_command(valid, "prepare", request="scenario/request.json")
        )
        run_dir = valid / "runs/run-1"
        expected_files = {
            "checkpoints/01-resolved.json",
            "checkpoints/02-governed.json",
            "checkpoints/03-admitted.json",
            "checkpoints/04-ticketed.json",
            "execution-ticket.json",
        }
        observed_files = {
            path.relative_to(run_dir).as_posix()
            for path in run_dir.rglob("*")
            if path.is_file()
        }
        passed = (
            code == 0
            and payload.get("result") == "pass"
            and payload.get("current_phase") == "ticketed"
            and payload.get("phase_index") == 4
            and observed_files == expected_files
            and not stderr
        )
        results.append(
            (
                "prepare-valid-ticketed-chain",
                passed,
                f"code={code} phase={payload.get('current_phase')} files={len(observed_files)}",
            )
        )

        before_replay = tree_manifest(run_dir)
        code, payload, stderr = invoke(
            runner_command(valid, "prepare", request="scenario/request.json")
        )
        after_replay = tree_manifest(run_dir)
        results.append(
            (
                "prepare-identical-replay-byte-stable",
                code == 0
                and payload.get("idempotent_replay") is True
                and payload.get("writes_performed") == 0
                and before_replay == after_replay
                and not stderr,
                f"code={code} stable={before_replay == after_replay}",
            )
        )

        before_status = tree_manifest(run_dir)
        code, payload, stderr = invoke(runner_command(valid, "status"))
        after_status = tree_manifest(run_dir)
        results.append(
            (
                "status-is-read-only",
                code == 0
                and payload.get("writes_performed") == 0
                and before_status == after_status
                and not stderr,
                f"code={code} stable={before_status == after_status}",
            )
        )

        for mutation, case_id in (
            ("missing-selected-row", "prepare-missing-selection-blocks-before-write"),
            ("duplicate-selected-row", "prepare-tied-selection-blocks-before-write"),
            ("stale-work-pack-digest", "prepare-stale-work-pack-blocks-before-write"),
            ("stale-control-digest", "prepare-stale-control-blocks-before-write"),
        ):
            repo = scenario(
                temporary, source_task_session, canonical_task_session, mutation
            )
            passed, details = assert_block_before_write(repo, case_id)
            results.append((case_id, passed, details))

        skipped = scenario(
            temporary, source_task_session, canonical_task_session, "skipped-checkpoint"
        )
        invoke(runner_command(skipped, "prepare", request="scenario/request.json"))
        (skipped / "runs/run-1/checkpoints/02-governed.json").unlink()
        before = tree_manifest(skipped / "runs/run-1")
        code, payload, stderr = invoke(runner_command(skipped, "status"))
        after = tree_manifest(skipped / "runs/run-1")
        results.append(
            (
                "status-rejects-skipped-checkpoint",
                code == 2
                and payload.get("result") == "block"
                and payload.get("writes_performed") == 0
                and before == after
                and not stderr,
                f"code={code} stable={before == after}",
            )
        )

        drift = scenario(
            temporary, source_task_session, canonical_task_session, "predecessor-drift"
        )
        invoke(runner_command(drift, "prepare", request="scenario/request.json"))
        admitted_path = drift / "runs/run-1/checkpoints/03-admitted.json"
        admitted = load_json(admitted_path)
        admitted["predecessor"]["receipt_ref"]["sha256"] = "0" * 64
        write_json(admitted_path, admitted)
        before = tree_manifest(drift / "runs/run-1")
        code, payload, stderr = invoke(runner_command(drift, "status"))
        after = tree_manifest(drift / "runs/run-1")
        results.append(
            (
                "status-rejects-predecessor-drift",
                code == 2
                and payload.get("result") == "block"
                and payload.get("writes_performed") == 0
                and before == after
                and not stderr,
                f"code={code} stable={before == after}",
            )
        )

    observed_ids = {case_id for case_id, _, _ in results}
    inventory_errors: list[str] = []
    for relative in OWNED:
        if not (source_task_session / relative).is_file():
            inventory_errors.append(f"missing owned output: {relative}")
    if args.material_inventory_manifest:
        manifest = load_json(Path(args.material_inventory_manifest))
        manifest_targets = {
            item["target_path"].split("arcana/task-session/", 1)[-1]
            for item in manifest.get("outputs", [])
            if isinstance(item, dict) and isinstance(item.get("target_path"), str)
        }
        if manifest_targets != set(OWNED):
            inventory_errors.append("producer manifest output inventory mismatch")

    combined_public_text = "\n".join(
        (source_task_session / relative).read_text(encoding="utf-8")
        for relative in OWNED
    ).casefold()
    private_slug = "body" + "-war"
    private_phrase = "suggested" + " track"
    for forbidden in (f"projects/{private_slug}", f"{private_slug}.", private_phrase):
        if forbidden in combined_public_text:
            inventory_errors.append(f"public boundary violation: {forbidden}")
    runner_text = (source_task_session / OWNED[0]).read_text(encoding="utf-8")
    if "shell=True" in runner_text or "os.system(" in runner_text:
        inventory_errors.append("runner contains shell execution surface")
    if expected_ids != observed_ids:
        inventory_errors.append(
            f"fixture/result id mismatch missing={sorted(expected_ids-observed_ids)} "
            f"extra={sorted(observed_ids-expected_ids)}"
        )

    positive = [item for item in results if "blocks" not in item[0] and "rejects" not in item[0]]
    negative = [item for item in results if item not in positive]
    failures = [item for item in results if not item[1]]
    failures.extend((error, False, error) for error in inventory_errors)
    manifest_digest = hashlib.sha256(
        json.dumps(
            {
                relative: {
                    "sha256": sha256(source_task_session / relative),
                    "size_bytes": (source_task_session / relative).stat().st_size,
                }
                for relative in OWNED
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()

    print(
        f"RESULT positive={sum(item[1] for item in positive)}/{len(positive)} "
        f"negative={sum(item[1] for item in negative)}/{len(negative)} "
        f"undeclared_outputs={len(inventory_errors)} inventory_mode="
        f"{'producer-manifest' if args.material_inventory_manifest else 'declared-targets'}"
    )
    for case_id, passed, details in results:
        print(f"{'PASS' if passed else 'FAIL'} {case_id} {details}")
    for error in inventory_errors:
        print(f"FAIL {error}")
    print(f"STAGED_MANIFEST_SHA256 {manifest_digest}")
    print("EXPERIMENT_HARNESS not_run owner=SWU-TSGR-010 reason=prepare-family-only")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
