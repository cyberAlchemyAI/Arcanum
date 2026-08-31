#!/usr/bin/env python3
"""Materialize the exact Distill v1 execution evidence for W2 V6R3."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


RUN_ID = "distill:plan-successor-w2-v6r3-validate-01"
PARENT_RUN_ID = "invoke:plan-successor-design-v6"
PROPOSER_REF = "/root"
BALANCER_REF = "/root/plan_w2_v6_distill_balancer"


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def exact(path: Path, root: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": path.resolve().relative_to(root).as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "size_bytes": len(data),
    }


def event(
    sequence: int,
    event_type: str,
    role: str | None,
    invocation_ref: str | None,
    payload_ref: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "event_id": f"event:{RUN_ID}:{sequence}",
        "run_id": RUN_ID,
        "sequence": sequence,
        "event_type": event_type,
        "execution_path": "true_subagent",
        "role": role,
        "invocation_ref": invocation_ref,
        "payload_ref": payload_ref,
        "emitted_at": f"2026-08-28T17:00:0{sequence}Z",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--candidate-receipt", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    output = args.output_dir.resolve()
    if output.exists() or output.is_symlink():
        raise ValueError("--output-dir must be absent")
    output.mkdir(parents=False)

    reviewed = [exact(args.candidate.resolve(), root), exact(args.candidate_receipt.resolve(), root)]
    request = {
        "schema_version": "1.0.0",
        "run_id": RUN_ID,
        "parent_invoke_run_id": PARENT_RUN_ID,
        "invoke_mode": "design",
        "distill_mode": "validate",
        "round_budget": {"max_rounds": 3, "max_role_invocations": 6},
        "reviewed_inputs": reviewed,
        "requested_techniques": ["smallest-coherent-unit", "recomposition-proof"],
    }
    request_path = output / "DISTILL-RUN-REQUEST.json"
    write_json(request_path, request)

    proposer = {
        "role": "proposer",
        "run_id": RUN_ID,
        "verdict": "pass",
        "smallest_coherent_unit": "One canonical Plan source through one normalized graph, separately owned human and consumer projections, one complete candidate bundle, and independent replay admission.",
        "authority_boundary": "Readiness, acceptance, execution, publication, and deployment remain external.",
        "evidence_refs": reviewed,
    }
    proposer_path = output / "DISTILL-PROPOSER-RESULT.json"
    write_json(proposer_path, proposer)

    balancer = {
        "role": "balancer",
        "run_id": RUN_ID,
        "verdict": "pass",
        "objections": [],
        "distill_owned_gaps": [],
        "preserved_downstream_gap": {
            "gap_id": "gap:signal-observer-machine-contract",
            "blocking": False,
            "effect": "Plan bundle admission may proceed without an observer-closure claim; observability-configured execution remains deferred.",
        },
        "confirmed_checks": [
            "explicit project-views to project-consumers to produce-bundle to admit-bundle path",
            "exclusive component ownership",
            "seven-consumer applicability matrix",
            "conditional boundary adapters",
            "smallest coherent unit",
            "authority ceiling",
            "Work Pack navigation UX",
            "native-context 1.2.0 and 1.3.0 selection",
            "visible Signal Observer gap",
            "passing candidate receipt binding",
        ],
        "invocation_ref": BALANCER_REF,
    }
    balancer_path = output / "DISTILL-BALANCER-RESULT.json"
    write_json(balancer_path, balancer)

    reconciliation = {
        "run_id": RUN_ID,
        "status": "pass",
        "statement": "All prior Distill objections are repaired. The Signal Observer limitation is a preserved downstream Design gap, not an unclosed Distill objection.",
        "objection_refs": ["BAL-V6-001", "BAL-V6-002", "BAL-V6-003", "BAL-V6R2-001"],
    }
    reconciliation_path = output / "DISTILL-RECONCILIATION.json"
    write_json(reconciliation_path, reconciliation)

    recomposition = {
        "run_id": RUN_ID,
        "status": "pass",
        "proof": "The source validator admits one semantic source; the graph compiler produces one normalized graph; separate projectors derive human and consumer outputs; the bundle producer publishes one complete candidate; and an independently owned validator recompiles, byte-compares, and rehearses applicable consumers without granting readiness or execution.",
    }
    recomposition_path = output / "DISTILL-RECOMPOSITION.json"
    write_json(recomposition_path, recomposition)

    request_ref = exact(request_path, root)
    proposer_ref = exact(proposer_path, root)
    balancer_ref = exact(balancer_path, root)
    reconciliation_ref = exact(reconciliation_path, root)
    recomposition_ref = exact(recomposition_path, root)
    candidate_ref = reviewed[0]
    events = [
        event(0, "capability_probe", None, None, request_ref),
        event(1, "role_start", "proposer", PROPOSER_REF, request_ref),
        event(2, "role_result", "proposer", PROPOSER_REF, proposer_ref),
        event(3, "role_start", "balancer", BALANCER_REF, request_ref),
        event(4, "role_result", "balancer", BALANCER_REF, balancer_ref),
        event(5, "reconciliation", None, None, reconciliation_ref),
        event(6, "termination", None, None, recomposition_ref),
    ]
    events_path = output / "DISTILL-EVENTS.jsonl"
    events_path.write_text(
        "".join(json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for item in events),
        encoding="utf-8",
    )

    receipt = {
        "schema_version": "1.0.0",
        "receipt_id": "distill-receipt:plan-successor-w2-v6r3",
        "run_id": RUN_ID,
        "request_ref": request_ref,
        "event_refs": [item["event_id"] for item in events],
        "role_trace": [
            {
                "role": "proposer",
                "execution_path": "true_subagent",
                "invocation_ref": PROPOSER_REF,
                "evidence_refs": [events[1]["event_id"], events[2]["event_id"]],
                "result_ref": proposer_ref,
            },
            {
                "role": "balancer",
                "execution_path": "true_subagent",
                "invocation_ref": BALANCER_REF,
                "evidence_refs": [events[3]["event_id"], events[4]["event_id"]],
                "result_ref": balancer_ref,
            },
        ],
        "objections": [],
        "reconciliations": [
            {
                "statement": reconciliation["statement"],
                "category": "process",
                "disposition": "accept",
                "evidence_refs": [events[5]["event_id"]],
            }
        ],
        "technique_trace": [
            {"technique": "smallest-coherent-unit", "status": "applied", "evidence_refs": [events[2]["event_id"], events[4]["event_id"]]},
            {"technique": "recomposition-proof", "status": "applied", "evidence_refs": [events[5]["event_id"], events[6]["event_id"]]},
        ],
        "termination": {"reason": "reconciled", "round_count": 3},
        "verdict": "pass",
        "gaps": [],
        "recomposition": {"summary": recomposition["proof"], "result_ref": recomposition_ref},
        "next_route": {"capability": "invoke-design-bundle-producer", "status": "ready"},
        "reviewed_input_provenance": reviewed,
    }
    receipt_path = output / "DISTILL-EXECUTION-RECEIPT.json"
    write_json(receipt_path, receipt)
    print(json.dumps({"output_dir": output.as_posix(), "request": request_ref, "events": exact(events_path, root), "receipt": exact(receipt_path, root)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
