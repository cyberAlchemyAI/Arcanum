"""Pure reason-complete decision-frontier reducer."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def derive_frontier(document: dict[str, Any], claims: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    claims = claims or []
    source_digest = canonical_digest(document)
    for claim in claims:
        if claim.get("status") == "active" and claim.get("source_digest") != source_digest:
            raise ValueError("STALE_CLAIM")
    active = {
        claim["decision_id"]
        for claim in claims
        if claim.get("status") == "active"
    }
    nodes = {item["id"]: item for item in document["nodes"]}
    blockers: dict[str, list[str]] = {}
    for edge in document["edges"]:
        blockers.setdefault(edge["blocked_id"], []).append(edge["blocker_id"])
    projection = []
    for node_id in sorted(nodes):
        item = nodes[node_id]
        reasons = []
        if item["state"] != "open":
            reasons.append(f"state:{item['state']}")
        if item["state"] == "fog":
            reasons.append("imprecise")
        if item["scope"] != "in_scope":
            reasons.append("out_of_scope")
        if node_id in active:
            reasons.append("active_claim")
        for blocker_id in sorted(blockers.get(node_id, [])):
            if nodes[blocker_id]["state"] not in {"resolved", "invalidated"}:
                reasons.append(f"unresolved_blocker:{blocker_id}")
        reasons = sorted(set(reasons))
        projection.append({"id": node_id, "eligible": not reasons, "exclusion_reasons": reasons})
    return {
        "schema_version": "1.0.0",
        "kind": "frontier_snapshot",
        "source_digest": source_digest,
        "nodes": projection,
        "frontier_ids": [item["id"] for item in projection if item["eligible"]],
    }
