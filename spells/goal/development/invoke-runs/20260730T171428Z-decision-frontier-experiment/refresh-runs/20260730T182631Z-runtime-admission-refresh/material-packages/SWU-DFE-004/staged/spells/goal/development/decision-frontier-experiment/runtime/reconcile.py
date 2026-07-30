"""Immutable, causal DFE reconciliation proposals."""

from __future__ import annotations

import copy
from typing import Any

from runtime.frontier import canonical_digest


TERMINAL = {"resolved", "invalidated", "superseded"}


def reconcile(document: dict[str, Any], claim: dict[str, Any], resolution: dict[str, Any]) -> dict[str, Any]:
    source_digest = canonical_digest(document)
    nodes = {item["id"]: item for item in document["nodes"]}
    decision = nodes.get(resolution["decision_id"])
    if (
        decision is None
        or claim["status"] != "active"
        or claim["decision_id"] != resolution["decision_id"]
        or claim["source_digest"] != source_digest
        or resolution["source_digest"] != source_digest
        or claim["owner"] != resolution["owner"]
        or decision["route"] != resolution["route"]
    ):
        raise ValueError("RESOLUTION_BINDING_MISMATCH")
    actions = sorted(resolution["actions"], key=lambda item: item["sequence"])
    if [item["sequence"] for item in actions] != list(range(len(actions))):
        raise ValueError("ACTION_SEQUENCE")
    if len({item["action_id"] for item in actions}) != len(actions):
        raise ValueError("DUPLICATE_ACTION")

    original_digest = canonical_digest(document)
    staged = copy.deepcopy(document)
    staged_nodes = {item["id"]: item for item in staged["nodes"]}
    for action in actions:
        kind = action["kind"]
        target = action["target"]
        payload = action["payload"]
        if kind == "add":
            new_node = copy.deepcopy(payload["node"])
            if new_node["id"] in staged_nodes or new_node["state"] != "open" or new_node["scope"] != "in_scope":
                raise ValueError("ADD_INVALID")
            staged["nodes"].append(new_node)
            staged_nodes[new_node["id"]] = new_node
        elif kind == "graduate_fog":
            if staged_nodes[target]["state"] != "fog" or not payload.get("question") or not payload.get("owner"):
                raise ValueError("FOG_GRADUATION_INVALID")
            staged_nodes[target]["state"] = "open"
            staged_nodes[target]["question"] = payload["question"]
            staged_nodes[target]["owner"] = payload["owner"]
        elif kind == "invalidate":
            if target not in staged_nodes or staged_nodes[target]["state"] in TERMINAL:
                raise ValueError("INVALIDATION_INVALID")
            staged_nodes[target]["state"] = "invalidated"
            staged_nodes[target]["disposition_reason"] = payload["reason"]
        elif kind == "supersede":
            replacement = payload["replacement_id"]
            if target not in staged_nodes or replacement not in staged_nodes:
                raise ValueError("SUPERSEDE_INVALID")
            staged_nodes[target]["state"] = "superseded"
            staged_nodes[target]["replacement_id"] = replacement
        elif kind == "unblock":
            pair = (payload["blocker_id"], payload["blocked_id"])
            if not any((edge["blocker_id"], edge["blocked_id"]) == pair for edge in staged["edges"]):
                raise ValueError("EDGE_MISSING")
            if staged_nodes[pair[0]]["state"] not in {"resolved", "invalidated"}:
                raise ValueError("BLOCKER_NOT_TERMINAL")
            staged["edges"] = [
                edge
                for edge in staged["edges"]
                if (edge["blocker_id"], edge["blocked_id"]) != pair
            ]
        else:
            raise ValueError("ACTION_KIND")
    staged["nodes"] = sorted(staged["nodes"], key=lambda item: item["id"])
    staged["edges"] = sorted(staged["edges"], key=lambda item: (item["blocker_id"], item["blocked_id"]))
    if canonical_digest(document) != original_digest:
        raise AssertionError("INPUT_MUTATED")
    return {
        "schema_version": "1.0.0",
        "kind": "reconciliation",
        "authority": "proposal",
        "source_digest": source_digest,
        "claim_id": claim["claim_id"],
        "resolution_id": resolution["resolution_id"],
        "actions": actions,
        "proposed_map_digest": canonical_digest(staged),
    }
