#!/usr/bin/env python3
"""Closed-schema and graph-semantic admission for DFE documents."""

from __future__ import annotations

import copy
import hashlib
import json
from collections import deque
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
EVIDENCE = ROOT / "session-evidence/SWU-DFE-001/contract-validation.json"
STATES = {"open", "resolved", "fog", "out_of_scope", "invalidated", "superseded"}
ROUTES = {"HITL", "AFK"}
SCOPES = {"in_scope", "out_of_scope"}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def diagnostic(code: str, selector: str) -> dict[str, str]:
    return {"code": code, "selector": selector}


def validate_decision_map(document: Any) -> list[dict[str, str]]:
    if not isinstance(document, dict):
        return [diagnostic("SCHEMA_INVALID", "<root>")]
    expected = {"schema_version", "kind", "destination", "source_digest", "nodes", "edges"}
    if set(document) != expected or document.get("schema_version") != "1.0.0" or document.get("kind") != "decision_map":
        return [diagnostic("SCHEMA_INVALID", "<root>")]
    if not isinstance(document.get("destination"), str) or not document["destination"]:
        return [diagnostic("SCHEMA_INVALID", "destination")]
    source_digest = document.get("source_digest")
    if not isinstance(source_digest, str) or len(source_digest) != 64:
        return [diagnostic("SCHEMA_INVALID", "source_digest")]
    if not isinstance(document.get("nodes"), list) or not isinstance(document.get("edges"), list):
        return [diagnostic("SCHEMA_INVALID", "nodes|edges")]

    ids = []
    nodes = {}
    node_keys = {"id", "question", "state", "route", "scope", "owner"}
    for index, item in enumerate(document["nodes"]):
        if not isinstance(item, dict) or set(item) != node_keys:
            return [diagnostic("SCHEMA_INVALID", f"nodes/{index}")]
        if (
            not isinstance(item["id"], str)
            or not item["id"]
            or not isinstance(item["question"], str)
            or not item["question"]
            or not isinstance(item["owner"], str)
            or not item["owner"]
            or item["state"] not in STATES
            or item["route"] not in ROUTES
            or item["scope"] not in SCOPES
        ):
            return [diagnostic("SCHEMA_INVALID", f"nodes/{index}")]
        ids.append(item["id"])
        nodes[item["id"]] = item
    duplicates = sorted({node_id for node_id in ids if ids.count(node_id) > 1})
    if duplicates:
        return [diagnostic("DUPLICATE_ID", f"nodes/{duplicates[0]}")]

    pairs = []
    for index, edge in enumerate(document["edges"]):
        if not isinstance(edge, dict) or set(edge) != {"blocker_id", "blocked_id"}:
            return [diagnostic("SCHEMA_INVALID", f"edges/{index}")]
        pair = (edge["blocker_id"], edge["blocked_id"])
        if pair[0] == pair[1]:
            return [diagnostic("SELF_EDGE", f"edges/{pair[0]}->{pair[1]}")]
        if pair in pairs:
            return [diagnostic("DUPLICATE_EDGE", f"edges/{pair[0]}->{pair[1]}")]
        if pair[0] not in nodes or pair[1] not in nodes:
            return [diagnostic("UNKNOWN_ENDPOINT", f"edges/{pair[0]}->{pair[1]}")]
        pairs.append(pair)

    indegree = {node_id: 0 for node_id in nodes}
    children = {node_id: [] for node_id in nodes}
    for blocker, blocked in pairs:
        indegree[blocked] += 1
        children[blocker].append(blocked)
    ready = deque(sorted(node_id for node_id, count in indegree.items() if count == 0))
    visited = []
    while ready:
        current = ready.popleft()
        visited.append(current)
        for child in sorted(children[current]):
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)
    if len(visited) != len(nodes):
        return [diagnostic("GRAPH_CYCLE", "edges")]
    return []


def validate_document(document: Any, kind: str) -> list[dict[str, str]]:
    if kind == "decision_map":
        return validate_decision_map(document)
    schema_path = SCHEMAS / f"{kind.replace('_', '-')}.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        return [diagnostic("SCHEMA_INVALID", "<root>")]
    required = set(schema["required"])
    if set(document) != required:
        return [diagnostic("SCHEMA_INVALID", "<root>")]
    if document.get("schema_version") != "1.0.0":
        return [diagnostic("SCHEMA_INVALID", "schema_version")]
    return []


def load(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def main() -> int:
    diamond = load("fixtures/diamond-map.json")
    positive_errors = validate_decision_map(diamond)
    mutants = {}
    cycle = load("fixtures/cycle-map.json")
    mutants["cycle"] = validate_decision_map(cycle)
    duplicate = copy.deepcopy(diamond)
    duplicate["nodes"].append(copy.deepcopy(duplicate["nodes"][0]))
    mutants["duplicate_id"] = validate_decision_map(duplicate)
    unknown = copy.deepcopy(diamond)
    unknown["edges"].append({"blocker_id": "UNKNOWN", "blocked_id": "D"})
    mutants["unknown_endpoint"] = validate_decision_map(unknown)
    invalid_state = copy.deepcopy(diamond)
    invalid_state["nodes"][0]["state"] = "maybe"
    mutants["invalid_state"] = validate_decision_map(invalid_state)
    invalid_route = copy.deepcopy(diamond)
    invalid_route["nodes"][0]["route"] = "AUTO"
    mutants["invalid_route"] = validate_decision_map(invalid_route)
    expected_codes = {
        "cycle": "GRAPH_CYCLE",
        "duplicate_id": "DUPLICATE_ID",
        "unknown_endpoint": "UNKNOWN_ENDPOINT",
        "invalid_state": "SCHEMA_INVALID",
        "invalid_route": "SCHEMA_INVALID",
    }
    checks = {
        name: bool(errors) and errors[0]["code"] == expected_codes[name]
        for name, errors in mutants.items()
    }
    schema_files = sorted(path.name for path in SCHEMAS.glob("*.schema.json"))
    schema_parse = all(json.loads((SCHEMAS / name).read_text(encoding="utf-8")) for name in schema_files)
    passed = not positive_errors and all(checks.values()) and bool(schema_parse)
    result = {
        "schema_version": "dfe-contract-validation.v1",
        "status": "pass" if passed else "block",
        "witnesses": ["DFE-FIX-003"],
        "input_sha256": canonical_digest(diamond),
        "schema_files": schema_files,
        "positive": {"status": "pass" if not positive_errors else "block", "diagnostics": positive_errors},
        "mutants": {
            name: {"status": "block" if errors else "unexpected-pass", "diagnostics": errors}
            for name, errors in sorted(mutants.items())
        },
        "authority_effect": "none",
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
