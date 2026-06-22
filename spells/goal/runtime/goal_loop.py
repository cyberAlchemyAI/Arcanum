#!/usr/bin/env python3
"""Read-only runtime skeleton for the goal spell.

This module is intentionally generic: it reads a public-safe JSON fixture or
caller payload, emits a frontier snapshot, classifies risk fail-closed, and
returns a non-mutating Goal Loop Result. It never loads filled private profile
content and never writes Craft source state.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RISK_TIERS = ("T0", "T1", "T2", "T3")
PROTECTED_TERMS = (
    "apply",
    "ci",
    "commit",
    "generate",
    "gitlink",
    "mutation",
    "network",
    "pr",
    "promotion",
    "publication",
    "publish",
    "push",
    "shell",
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected object fixture: {path}")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _public_node(node: dict[str, Any]) -> dict[str, str]:
    public = {
        "node_id": str(node.get("node_id", "")),
        "kind": str(node.get("kind", "")),
        "status": str(node.get("status", "")),
        "summary": str(node.get("summary", "")),
    }
    if node.get("evidence_ref"):
        public["evidence_ref"] = str(node["evidence_ref"])
    return public


def bind_source(payload: dict[str, Any]) -> tuple[bool, str, str, str]:
    goal = str(payload.get("goal") or "unspecified-goal")
    context_id = str(payload.get("goal_context_id") or "")
    source_ref = str(payload.get("source_ref") or "")
    if not context_id or not source_ref:
        return False, goal, context_id, source_ref
    return True, goal, context_id, source_ref


def read_frontier(payload: dict[str, Any], context_id: str, source_ref: str) -> dict[str, Any]:
    nodes = [_public_node(node) for node in payload.get("nodes", [])]
    return {
        "snapshot_id": str(payload.get("snapshot_id") or f"frontier-{context_id}"),
        "goal_context_id": context_id,
        "source_ref": source_ref,
        "captured_at": _utc_now(),
        "nodes": nodes,
        "active_blockers": [str(item) for item in payload.get("active_blockers", [])],
        "active_gaps": [str(item) for item in payload.get("active_gaps", [])],
    }


def classify_node(node: dict[str, Any]) -> tuple[str, str]:
    explicit = str(node.get("risk_tier") or node.get("risk") or "").upper()
    if explicit in RISK_TIERS:
        return explicit, "explicit"
    if explicit:
        return "T3", "unknown-risk"

    text = " ".join(
        str(node.get(field, "")).lower()
        for field in ("node_id", "kind", "status", "summary")
    )
    if any(term in text for term in PROTECTED_TERMS):
        return "T3", "protected-operation"
    if str(node.get("status", "")).lower() in {"blocked", "protected"}:
        return "T3", "protected-status"
    if str(node.get("kind", "")).lower() in {"gap", "blocker", "decision"}:
        return "T2", "review-required"
    return "T1", "read-only-default"


def classify_risk(payload: dict[str, Any]) -> tuple[dict[str, int], list[str]]:
    counts = {tier: 0 for tier in RISK_TIERS}
    reasons: list[str] = []
    for node in payload.get("nodes", []):
        tier, reason = classify_node(node)
        counts[tier] += 1
        if tier == "T3":
            reasons.append(reason)
    return counts, reasons


def first_routable_node(payload: dict[str, Any]) -> dict[str, Any] | None:
    for node in payload.get("nodes", []):
        tier, _reason = classify_node(node)
        if tier != "T3":
            return node
    return None


def build_dispatch_route(payload: dict[str, Any]) -> dict[str, Any] | None:
    node = first_routable_node(payload)
    if node is None:
        return None

    node_id = str(node.get("node_id", "node"))
    route_id = str(payload.get("route_id") or f"goal-route-{node_id}")
    owner = str(node.get("owner") or payload.get("owner") or "task-session")
    receipt_ref = f"{route_id}.execution-receipt.json"
    result_ref = f"{route_id}.result.md"
    return {
        "dispatch_id": route_id,
        "intent": {
            "raw": str(node.get("summary") or payload.get("goal") or "route goal node"),
            "objective": f"Route {node_id} through {owner} with terminal receipt evidence.",
            "target_artifact": node_id,
            "arcanum_vocabulary": ["goal", "dispatch route", "execution receipt"],
        },
        "mode": "sequence",
        "techniques": [
            "sequence",
            "delegation_boundary",
            "execution_receipt_handoff",
            "validation_loop",
        ],
        "boundary_evidence": {
            "boundaries": [
                {
                    "boundary_id": "goal-w2-owner-boundary",
                    "kind": "capability_handoff",
                    "from_owner": "goal",
                    "to_owner": owner,
                    "applies_to_steps": ["execute-node"],
                    "contract": "Goal routes eligible work and receives terminal receipt evidence without redefining owner internals.",
                    "on_violation": "block",
                }
            ],
            "authority": {
                "lifecycle": "goal",
                "execution": owner,
                "validation": "dispatch-spec",
                "evidence": "task-session",
                "promotion": "craft-after-approval",
            },
            "receipts": [
                {
                    "receipt_id": "goal-w2-terminal-receipt",
                    "producer": owner,
                    "required_fields": ["dispatch_id", "step_id", "capability_ref", "status", "validation", "residue"],
                    "stores": [receipt_ref],
                    "on_missing": "block",
                }
            ],
            "state_namespaces": [
                {
                    "namespace": "craft-source",
                    "owner": "arcana/craft",
                    "write_policy": "Goal may stage deltas, but active apply requires approval.",
                }
            ],
        },
        "steps": [
            {
                "step_id": "execute-node",
                "name": "Execute eligible goal node",
                "capability_ref": owner,
                "pattern": "handoff",
                "techniques": ["delegation_boundary", "execution_receipt_handoff", "validation_loop"],
                "inputs": [{"kind": "intent", "ref": "intent.raw"}],
                "outputs": [{"kind": "artifact", "ref": receipt_ref}],
                "evidence_artifact": receipt_ref,
                "stop_conditions": ["block if receipt is not terminal"],
            }
        ],
        "gates": [
            {
                "gate_id": "goal-w2-terminal-receipt",
                "kind": "validation",
                "owner": "goal",
                "condition": "Delegated lane returns terminal receipt before audit.",
                "on_fail": "block",
            }
        ],
        "native_stage_receipts": [
            {
                "dispatch_id": route_id,
                "step_id": "execute-node",
                "capability_ref": owner,
                "receipt_kind": "native-stage",
                "status": "pass",
                "artifacts": [receipt_ref, result_ref],
                "validation": ["terminal receipt shape checked"],
                "observer_status": "not_run",
                "blockers": [],
                "residue": "",
                "handoff_note": "route evidence fixture",
            }
        ],
        "observability": {
            "dispatch_id_required": True,
            "trace_events": ["dispatch_validated", "terminal_receipt_recorded"],
            "signal_grouping": "dispatch_id",
        },
    }


def build_execution_receipt(payload: dict[str, Any], route: dict[str, Any]) -> dict[str, Any]:
    route_id = str(route["dispatch_id"])
    owner = str(route["steps"][0]["capability_ref"])
    return {
        "receipt_id": f"{route_id}-receipt",
        "route_id": route_id,
        "owner": owner,
        "status": "closed",
        "terminal": True,
        "evidence": [str(payload.get("evidence_ref") or "fixture:terminal-receipt")],
        "files_touched": [],
        "validation": ["receipt is terminal", "owner boundary preserved"],
        "residue": [],
        "reroute": "audit-gate",
    }


def audit_receipt(payload: dict[str, Any], receipt: dict[str, Any]) -> dict[str, Any]:
    veto = bool(payload.get("audit_veto"))
    return {
        "audit_id": f"audit-{receipt['receipt_id']}",
        "receipt_id": receipt["receipt_id"],
        "verdict": "block" if veto else "pass",
        "veto": veto,
        "evidence": receipt["evidence"],
        "reason": "audit-veto" if veto else "done-criteria-satisfied",
    }


def build_staged_delta(payload: dict[str, Any], receipt: dict[str, Any], audit: dict[str, Any]) -> dict[str, Any] | None:
    source_change = payload.get("source_change")
    if audit["verdict"] != "pass" or not isinstance(source_change, dict):
        return None
    return {
        "delta_id": str(source_change.get("delta_id") or f"delta-{receipt['receipt_id']}"),
        "source_authority": str(source_change.get("source_authority") or "arcana/craft"),
        "target": str(source_change.get("target") or "fixture:craft-ledger"),
        "operation": str(source_change.get("operation") or "annotate"),
        "framed_diff": str(source_change.get("framed_diff") or "Stage public-safe progress evidence without applying it."),
        "validation_expectation": [
            str(item)
            for item in source_change.get(
                "validation_expectation",
                ["staged delta schema validates", "promotion_state remains staged"],
            )
        ],
        "promotion_state": "staged",
        "created_by_receipt": str(receipt["receipt_id"]),
    }


def evaluate_approval_boundary(payload: dict[str, Any]) -> dict[str, Any]:
    batch_id = str(payload.get("batch_id") or "")
    token = payload.get("approval_token")
    if payload.get("ambient_approval") and not isinstance(token, dict):
        return {
            "batch_id": batch_id,
            "state": "blocked",
            "stop_reason": "ambient-approval",
            "apply_owner": "arcana/craft",
            "craft_apply_request": False,
            "direct_apply_performed": False,
        }
    if not isinstance(token, dict):
        return {
            "batch_id": batch_id,
            "state": "held",
            "stop_reason": "approval-required",
            "apply_owner": "arcana/craft",
            "craft_apply_request": False,
            "direct_apply_performed": False,
        }
    if token.get("batch_id") != batch_id:
        return {
            "batch_id": batch_id,
            "state": "blocked",
            "stop_reason": "approval-token-mismatch",
            "apply_owner": "arcana/craft",
            "craft_apply_request": False,
            "direct_apply_performed": False,
        }
    if token.get("approval_state") != "approved" or not token.get("decision_record_ref"):
        return {
            "batch_id": batch_id,
            "state": "held",
            "stop_reason": "approval-required",
            "apply_owner": "arcana/craft",
            "craft_apply_request": False,
            "direct_apply_performed": False,
        }
    return {
        "batch_id": batch_id,
        "state": "ready-for-craft-apply",
        "stop_reason": "none",
        "apply_owner": "arcana/craft",
        "craft_apply_request": True,
        "direct_apply_performed": False,
        "decision_record_ref": str(token["decision_record_ref"]),
        "approval_token_id": str(token.get("token_id", "")),
    }


def run_gap_discovery(payload: dict[str, Any]) -> dict[str, Any]:
    if not payload.get("frontier_empty", False):
        return {
            "result": "BLOCK",
            "stop_reason": "frontier-not-empty",
            "rounds": 0,
            "proposals": [],
            "duplicates": [],
        }

    max_rounds = int(payload.get("max_rounds", 1))
    current_round = int(payload.get("current_round", 0))
    if current_round >= max_rounds:
        return {
            "result": "STOP",
            "stop_reason": "budget-ceiling",
            "rounds": current_round,
            "proposals": [],
            "duplicates": [],
        }

    seen: set[tuple[str, str]] = set()
    proposals: list[dict[str, str]] = []
    duplicates: list[dict[str, str]] = []
    for gap in payload.get("candidate_gaps", []):
        key = (str(gap.get("kind", "")), str(gap.get("target", "")))
        public_gap = {
            "kind": key[0],
            "target": key[1],
            "summary": str(gap.get("summary", "")),
        }
        if key in seen:
            duplicates.append(public_gap)
            continue
        seen.add(key)
        proposals.append(public_gap)

    return {
        "result": "PASS",
        "stop_reason": "dedupe-complete",
        "rounds": current_round + 1,
        "proposals": proposals,
        "duplicates": duplicates,
    }


def build_telemetry_signal(
    goal_context_id: str,
    round_index: int,
    frontier_size: int,
    risk_counts: dict[str, int],
    stop_reason: str,
    nodes_dispatched: int = 0,
    staged_deltas: int = 0,
) -> dict[str, Any]:
    return {
        "spell": "goal",
        "goal_context_id": goal_context_id,
        "round_index": round_index,
        "frontier_size": frontier_size,
        "nodes_classified": {tier: int(risk_counts.get(tier, 0)) for tier in RISK_TIERS},
        "nodes_dispatched": nodes_dispatched,
        "staged_deltas": staged_deltas,
        "stop_reason": stop_reason,
    }


def build_result(payload: dict[str, Any], frontier: dict[str, Any] | None) -> dict[str, Any]:
    bound, goal, _context_id, _source_ref = bind_source(payload)
    if not bound:
        return {
            "spell": "goal",
            "goal": goal,
            "result": "BLOCK",
            "rounds": 0,
            "decision_profile": "neutral-default",
            "frontier": {"start": 0, "end": 0},
            "risk_tiers_seen": {tier: 0 for tier in RISK_TIERS},
            "stop_reason": "source-authority",
            "extra_sources": [],
            "next_route": "decision-gate",
        }

    counts, t3_reasons = classify_risk(payload)
    frontier_size = len(frontier["nodes"] if frontier else payload.get("nodes", []))
    if t3_reasons:
        result = "STOP"
        stop_reason = "t3-node"
        next_route = "operator-approval"
    else:
        result = "PASS"
        stop_reason = "none"
        next_route = "task-session"

    return {
        "spell": "goal",
        "goal": goal,
        "result": result,
        "rounds": 1,
        "decision_profile": "neutral-default",
        "frontier": {"start": frontier_size, "end": frontier_size},
        "risk_tiers_seen": counts,
        "stop_reason": stop_reason,
        "extra_sources": [],
        "next_route": next_route,
    }


def run_goal_loop(payload: dict[str, Any]) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    bound, _goal, context_id, source_ref = bind_source(payload)
    frontier = read_frontier(payload, context_id, source_ref) if bound else None
    return frontier, build_result(payload, frontier)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the read-only goal skeleton.")
    parser.add_argument("--fixture", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()

    payload = _read_json(args.fixture)
    frontier, result = run_goal_loop(payload)

    stem = args.fixture.stem
    if frontier is not None:
        _write_json(args.out_dir / f"{stem}.frontier-snapshot.json", frontier)
    _write_json(args.out_dir / f"{stem}.goal-loop-result.json", result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
