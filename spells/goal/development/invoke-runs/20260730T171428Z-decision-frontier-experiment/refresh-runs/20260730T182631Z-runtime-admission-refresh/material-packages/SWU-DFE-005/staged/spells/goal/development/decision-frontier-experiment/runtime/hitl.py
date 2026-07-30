"""Hard human-in-the-loop stop for an eligible DFE node."""

from __future__ import annotations

from typing import Any

from runtime.frontier import canonical_digest, derive_frontier


def route_hitl(document: dict[str, Any], decision_id: str, *, auto_resolution: bool = False) -> dict[str, Any]:
    frontier = derive_frontier(document)
    eligibility = {item["id"]: item["eligible"] for item in frontier["nodes"]}
    nodes = {item["id"]: item for item in document["nodes"]}
    decision = nodes.get(decision_id)
    if decision is None or not eligibility.get(decision_id):
        raise ValueError("NOT_ELIGIBLE")
    if decision["route"] != "HITL" or not decision["owner"]:
        raise ValueError("NOT_HITL")
    if auto_resolution:
        raise ValueError("HITL_AUTO_RESOLUTION_FORBIDDEN")
    return {
        "schema_version": "1.0.0",
        "kind": "hitl_route",
        "decision_id": decision_id,
        "source_digest": canonical_digest(document),
        "owner": decision["owner"],
        "status": "awaiting_human",
        "resolution": None,
        "reconciliation": None,
    }
