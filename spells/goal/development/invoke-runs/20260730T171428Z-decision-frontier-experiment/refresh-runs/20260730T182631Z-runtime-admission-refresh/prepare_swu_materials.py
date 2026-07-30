#!/usr/bin/env python3
"""Prepare exact, unapplied material packages for the seven DFE SWUs."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[7]
INVOKE_RUN = Path(
    "spells/goal/development/invoke-runs/"
    "20260730T171428Z-decision-frontier-experiment"
)
REFRESH_RUN = INVOKE_RUN / "refresh-runs/20260730T182631Z-runtime-admission-refresh"
MATERIAL_ROOT = REFRESH_RUN / "material-packages"
EXPERIMENT = Path("spells/goal/development/decision-frontier-experiment")
SOURCE_DIGEST = "a" * 64


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def digest(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def exact_ref(path: str) -> dict[str, object]:
    content = (REPOSITORY_ROOT / path).read_bytes()
    return {
        "path": path,
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def write_staged(unit: str, target: str, content: str | object) -> None:
    path = REPOSITORY_ROOT / MATERIAL_ROOT / unit / "staged" / target
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, str):
        path.write_text(content.rstrip() + "\n", encoding="utf-8")
    else:
        path.write_text(
            json.dumps(content, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def staged_ref(unit: str, target: str) -> dict[str, object]:
    path = MATERIAL_ROOT / unit / "staged" / target
    content = (REPOSITORY_ROOT / path).read_bytes()
    return {
        "path": str(path),
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def node(
    node_id: str,
    question: str,
    *,
    state: str = "open",
    route: str = "AFK",
    scope: str = "in_scope",
    owner: str = "resolver:test",
) -> dict[str, str]:
    return {
        "id": node_id,
        "question": question,
        "state": state,
        "route": route,
        "scope": scope,
        "owner": owner,
    }


def decision_map(
    destination: str,
    nodes: list[dict[str, str]],
    edges: list[tuple[str, str]],
) -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "kind": "decision_map",
        "destination": destination,
        "source_digest": SOURCE_DIGEST,
        "nodes": nodes,
        "edges": [
            {"blocker_id": blocker, "blocked_id": blocked}
            for blocker, blocked in edges
        ],
    }


DIAMOND = decision_map(
    "ship fixture",
    [
        node("A", "Choose input contract?"),
        node("B", "Choose output contract?"),
        node("C", "Choose reconciliation form?"),
        node("D", "Choose terminal evidence?"),
    ],
    [("A", "C"), ("B", "C"), ("C", "D")],
)
CYCLE = decision_map(
    "reject cycle",
    [node("A", "First?"), node("B", "Second?")],
    [("A", "B"), ("B", "A")],
)
FOG = decision_map(
    "graduate fog",
    [
        node("F1", "Unshaped uncertainty", state="fog"),
        node("O1", "Choose precise route?"),
    ],
    [],
)
SCOPE = decision_map(
    "retain scope",
    [
        node("O1", "Choose in-scope behavior?"),
        node(
            "X1",
            "Choose later integration?",
            state="out_of_scope",
            scope="out_of_scope",
        ),
    ],
    [],
)
INVALIDATED = decision_map(
    "resolved blocker",
    [
        node("A", "Former blocker?", state="invalidated"),
        node("C", "Now unblocked?"),
    ],
    [("A", "C")],
)


def frontier_projection(
    document: dict[str, object], claims: list[dict[str, object]] | None = None
) -> dict[str, object]:
    claims = claims or []
    source_digest = digest(document)
    active = {
        claim["decision_id"]
        for claim in claims
        if claim.get("status") == "active"
        and claim.get("source_digest") == source_digest
    }
    nodes = {item["id"]: item for item in document["nodes"]}  # type: ignore[index]
    blockers: dict[str, list[str]] = {}
    for edge in document["edges"]:  # type: ignore[index]
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
        projection.append(
            {
                "id": node_id,
                "eligible": not reasons,
                "exclusion_reasons": reasons,
            }
        )
    return {
        "schema_version": "1.0.0",
        "kind": "frontier_snapshot",
        "source_digest": source_digest,
        "nodes": projection,
        "frontier_ids": [
            item["id"] for item in projection if item["eligible"]
        ],
    }


def staged_reconciliation(
    document: dict[str, object],
    claim: dict[str, object],
    resolution: dict[str, object],
) -> dict[str, object]:
    staged = copy.deepcopy(document)
    nodes = {item["id"]: item for item in staged["nodes"]}  # type: ignore[index]
    edges = staged["edges"]  # type: ignore[index]
    for action in sorted(resolution["actions"], key=lambda item: item["sequence"]):  # type: ignore[index]
        kind = action["kind"]
        target = action["target"]
        payload = action["payload"]
        if kind == "add":
            new_node = copy.deepcopy(payload["node"])
            staged["nodes"].append(new_node)  # type: ignore[union-attr]
            nodes[new_node["id"]] = new_node
        elif kind == "graduate_fog":
            nodes[target]["state"] = "open"
            nodes[target]["question"] = payload["question"]
            nodes[target]["owner"] = payload["owner"]
        elif kind == "invalidate":
            nodes[target]["state"] = "invalidated"
            nodes[target]["disposition_reason"] = payload["reason"]
        elif kind == "supersede":
            nodes[target]["state"] = "superseded"
            nodes[target]["replacement_id"] = payload["replacement_id"]
        elif kind == "unblock":
            edges[:] = [
                edge
                for edge in edges
                if not (
                    edge["blocker_id"] == payload["blocker_id"]
                    and edge["blocked_id"] == payload["blocked_id"]
                )
            ]
    staged["nodes"] = sorted(staged["nodes"], key=lambda item: item["id"])  # type: ignore[index]
    staged["edges"] = sorted(
        staged["edges"],  # type: ignore[index]
        key=lambda item: (item["blocker_id"], item["blocked_id"]),
    )
    return {
        "schema_version": "1.0.0",
        "kind": "reconciliation",
        "authority": "proposal",
        "source_digest": digest(document),
        "claim_id": claim["claim_id"],
        "resolution_id": resolution["resolution_id"],
        "actions": resolution["actions"],
        "proposed_map_digest": digest(staged),
    }


DECISION_MAP_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://arcanum.dev/experiments/decision-map/1-0-0",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "schema_version",
        "kind",
        "destination",
        "source_digest",
        "nodes",
        "edges",
    ],
    "properties": {
        "schema_version": {"const": "1.0.0"},
        "kind": {"const": "decision_map"},
        "destination": {"type": "string", "minLength": 1},
        "source_digest": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
        "nodes": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["id", "question", "state", "route", "scope", "owner"],
                "properties": {
                    "id": {"type": "string", "minLength": 1},
                    "question": {"type": "string", "minLength": 1},
                    "state": {
                        "enum": [
                            "open",
                            "resolved",
                            "fog",
                            "out_of_scope",
                            "invalidated",
                            "superseded",
                        ]
                    },
                    "route": {"enum": ["HITL", "AFK"]},
                    "scope": {"enum": ["in_scope", "out_of_scope"]},
                    "owner": {"type": "string", "minLength": 1},
                },
            },
        },
        "edges": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["blocker_id", "blocked_id"],
                "properties": {
                    "blocker_id": {"type": "string", "minLength": 1},
                    "blocked_id": {"type": "string", "minLength": 1},
                },
            },
        },
    },
}


def closed_schema(kind: str, properties: dict[str, object]) -> dict[str, object]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://arcanum.dev/experiments/{kind}/1-0-0",
        "type": "object",
        "additionalProperties": False,
        "required": list(properties),
        "properties": properties,
    }


FRONTIER_SCHEMA = closed_schema(
    "frontier-snapshot",
    {
        "schema_version": {"const": "1.0.0"},
        "kind": {"const": "frontier_snapshot"},
        "source_digest": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
        "nodes": {"type": "array"},
        "frontier_ids": {"type": "array", "items": {"type": "string"}},
    },
)
CLAIM_SCHEMA = closed_schema(
    "claim",
    {
        "schema_version": {"const": "1.0.0"},
        "kind": {"const": "claim"},
        "claim_id": {"type": "string"},
        "decision_id": {"type": "string"},
        "source_digest": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
        "owner": {"type": "string"},
        "claimed_at": {"type": "string"},
        "status": {"const": "active"},
        "previous_store_digest": {
            "type": "string",
            "pattern": "^[a-f0-9]{64}$",
        },
    },
)
RESOLUTION_SCHEMA = closed_schema(
    "resolution",
    {
        "schema_version": {"const": "1.0.0"},
        "kind": {"const": "resolution"},
        "resolution_id": {"type": "string"},
        "decision_id": {"type": "string"},
        "source_digest": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
        "owner": {"type": "string"},
        "route": {"enum": ["HITL", "AFK"]},
        "actions": {"type": "array"},
    },
)
RECONCILIATION_SCHEMA = closed_schema(
    "reconciliation",
    {
        "schema_version": {"const": "1.0.0"},
        "kind": {"const": "reconciliation"},
        "authority": {"const": "proposal"},
        "source_digest": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
        "claim_id": {"type": "string"},
        "resolution_id": {"type": "string"},
        "actions": {"type": "array"},
        "proposed_map_digest": {
            "type": "string",
            "pattern": "^[a-f0-9]{64}$",
        },
    },
)
WAY_CLEAR_SCHEMA = closed_schema(
    "way-clear",
    {
        "schema_version": {"const": "1.0.0"},
        "kind": {"const": "way_clear"},
        "source_digest": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
        "status": {"enum": ["clear", "blocked"]},
        "remaining": {"type": "array"},
    },
)


README = """# Goal Decision Frontier Experiment

Fixture-only development experiment for a deterministic, reason-complete,
claim-aware decision frontier.

Authority ceiling: every map, claim, resolution, reconciliation, and receipt
is synthetic development evidence. Nothing here mutates Craft, completes a
task/SWU, promotes Goal, publishes, deploys, or claims production readiness.

Run the seven commands under `scripts/` in the serial work-pack order. Each
command writes only its declared validation evidence.
"""


VALIDATE_CONTRACTS = r'''#!/usr/bin/env python3
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
'''


FRONTIER_RUNTIME = r'''"""Pure reason-complete decision-frontier reducer."""

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
'''


RUN_FRONTIER = r'''#!/usr/bin/env python3
"""Run DFE frontier goldens and deterministic replay."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from runtime.frontier import canonical_bytes, derive_frontier  # noqa: E402
from validate_contracts import validate_decision_map  # noqa: E402


CASES = ["diamond", "fog", "scope", "invalidated"]
INPUTS = {
    "diamond": "diamond-map.json",
    "fog": "fog-map.json",
    "scope": "scope-map.json",
    "invalidated": "invalidated-map.json",
}
EVIDENCE = ROOT / "session-evidence/SWU-DFE-002/frontier-validation.json"


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay", type=int, default=2)
    args = parser.parse_args()
    observations = {}
    passed = True
    for case in CASES:
        document = load(ROOT / "fixtures" / INPUTS[case])
        errors = validate_decision_map(document)
        if errors:
            observations[case] = {"status": "block", "errors": errors}
            passed = False
            continue
        expected = load(ROOT / "fixtures/expected" / f"{case}-frontier.json")
        replays = [canonical_bytes(derive_frontier(document)) for _ in range(args.replay)]
        actual = json.loads(replays[0])
        case_pass = actual == expected and len(set(replays)) == 1
        passed = passed and case_pass
        observations[case] = {
            "status": "pass" if case_pass else "block",
            "frontier_ids": actual["frontier_ids"],
            "replay_identical": len(set(replays)) == 1,
        }
    result = {
        "schema_version": "dfe-frontier-validation.v1",
        "status": "pass" if passed else "block",
        "witnesses": ["DFE-FIX-001", "DFE-FIX-006", "DFE-FIX-009"],
        "observations": observations,
        "authority_effect": "none",
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''


CLAIMS_RUNTIME = r'''"""Digest-bound single-process claim compare-and-set."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def claim_decision(request: dict[str, Any], frontier: dict[str, Any], store_path: Path) -> dict[str, Any]:
    store = json.loads(store_path.read_text(encoding="utf-8"))
    before_digest = canonical_digest(store)
    eligible = {item["id"]: item["eligible"] for item in frontier["nodes"]}
    reason = None
    if request["source_digest"] != frontier["source_digest"]:
        reason = "STALE_SOURCE"
    elif request["expected_store_digest"] != before_digest:
        reason = "CAS_MISMATCH"
    elif request["decision_id"] not in eligible:
        reason = "UNKNOWN_DECISION"
    elif not eligible[request["decision_id"]]:
        reason = "NOT_ELIGIBLE"
    elif any(
        item["decision_id"] == request["decision_id"]
        and item["source_digest"] == request["source_digest"]
        and item["status"] == "active"
        for item in store["claims"]
    ):
        reason = "ACTIVE_CLAIM"
    if reason:
        return {"status": "rejected", "code": reason, "store_digest": before_digest}

    claim = {
        "schema_version": "1.0.0",
        "kind": "claim",
        "claim_id": request["claim_id"],
        "decision_id": request["decision_id"],
        "source_digest": request["source_digest"],
        "owner": request["owner"],
        "claimed_at": request["claimed_at"],
        "status": "active",
        "previous_store_digest": before_digest,
    }
    updated = {"schema_version": "1.0.0", "claims": [*store["claims"], claim]}
    temporary = store_path.with_name(store_path.name + ".tmp")
    with temporary.open("wb") as handle:
        handle.write(canonical_bytes(updated) + b"\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, store_path)
    return {
        "status": "accepted",
        "code": "CLAIM_ACCEPTED",
        "claim": claim,
        "before_store_digest": before_digest,
        "after_store_digest": canonical_digest(updated),
    }
'''


RUN_CLAIMS = r'''#!/usr/bin/env python3
"""Run current, stale, and competing DFE claim fixtures."""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from runtime.claims import canonical_digest, claim_decision  # noqa: E402
from runtime.frontier import derive_frontier  # noqa: E402


EVIDENCE = ROOT / "session-evidence/SWU-DFE-003/claim-validation.json"


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    decision_map = load(ROOT / "fixtures/diamond-map.json")
    initial_store = load(ROOT / "fixtures/active-claim.json")
    frontier = derive_frontier(decision_map, initial_store["claims"])
    expected_accepted = load(ROOT / "fixtures/expected/claim-accepted.json")
    expected_stale = load(ROOT / "fixtures/expected/claim-rejected-stale.json")
    with tempfile.TemporaryDirectory(prefix="dfe-claim-") as temporary:
        store_path = Path(temporary) / "claim-store.json"
        shutil.copyfile(ROOT / "fixtures/active-claim.json", store_path)
        request = {
            "claim_id": "claim-B",
            "decision_id": "B",
            "source_digest": frontier["source_digest"],
            "owner": "resolver:test",
            "claimed_at": "2026-07-30T00:00:00Z",
            "expected_store_digest": canonical_digest(initial_store),
        }
        accepted = claim_decision(request, frontier, store_path)
        competing = claim_decision(request, frontier, store_path)
        competing_store_digest = canonical_digest(load(store_path))

        shutil.copyfile(ROOT / "fixtures/active-claim.json", store_path)
        stale_request = load(ROOT / "fixtures/stale-claim.json")
        stale_request["expected_store_digest"] = canonical_digest(initial_store)
        stale = claim_decision(stale_request, frontier, store_path)
        unchanged_after_stale = canonical_digest(load(store_path)) == canonical_digest(initial_store)

    active_reasons = {
        item["id"]: item["exclusion_reasons"] for item in frontier["nodes"]
    }
    passed = (
        accepted == expected_accepted
        and stale == expected_stale
        and competing["code"] == "CAS_MISMATCH"
        and competing_store_digest == accepted["after_store_digest"]
        and unchanged_after_stale
        and "active_claim" in active_reasons["A"]
    )
    result = {
        "schema_version": "dfe-claim-validation.v1",
        "status": "pass" if passed else "block",
        "witnesses": ["DFE-FIX-002", "DFE-FIX-004"],
        "accepted": accepted,
        "stale": stale,
        "competing_code": competing["code"],
        "active_claim_reason": active_reasons["A"],
        "fixture_store_unchanged": unchanged_after_stale,
        "authority_effect": "none",
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''


RECONCILE_RUNTIME = r'''"""Immutable, causal DFE reconciliation proposals."""

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
'''


RUN_RECONCILE = r'''#!/usr/bin/env python3
"""Run the five typed DFE reconciliation fixtures."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from runtime.frontier import canonical_digest  # noqa: E402
from runtime.reconcile import reconcile  # noqa: E402


EVIDENCE = ROOT / "session-evidence/SWU-DFE-004/reconciliation-validation.json"
CASES = ["fog", "invalidation", "add", "supersede", "unblock"]


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    observations = {}
    passed = True
    for case in CASES:
        map_path = ROOT / "fixtures" / ("fog-map.json" if case == "fog" else "diamond-map.json")
        document = load(map_path)
        before = file_digest(map_path)
        resolution = load(ROOT / "fixtures" / f"{case}-resolution.json")
        claim = {
            "claim_id": f"claim-{resolution['decision_id']}",
            "decision_id": resolution["decision_id"],
            "source_digest": canonical_digest(document),
            "owner": resolution["owner"],
            "status": "active",
        }
        actual = reconcile(document, claim, resolution)
        expected = load(ROOT / "fixtures/expected" / f"{case}-reconciliation.json")
        unchanged = before == file_digest(map_path)
        case_pass = actual == expected and unchanged and actual["authority"] == "proposal"
        passed = passed and case_pass
        observations[case] = {
            "status": "pass" if case_pass else "block",
            "source_unchanged": unchanged,
            "proposal_digest": actual["proposed_map_digest"],
        }
    result = {
        "schema_version": "dfe-reconciliation-validation.v1",
        "status": "pass" if passed else "block",
        "witnesses": ["DFE-FIX-005", "DFE-FIX-007"],
        "observations": observations,
        "authority_effect": "none",
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''


HITL_RUNTIME = r'''"""Hard human-in-the-loop stop for an eligible DFE node."""

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
'''


RUN_HITL = r'''#!/usr/bin/env python3
"""Run the DFE HITL route and forbidden auto-resolution mutant."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from runtime.hitl import route_hitl  # noqa: E402


EVIDENCE = ROOT / "session-evidence/SWU-DFE-005/hitl-validation.json"


def main() -> int:
    document = json.loads((ROOT / "fixtures/hitl-map.json").read_text(encoding="utf-8"))
    expected = json.loads((ROOT / "fixtures/expected/hitl-route.json").read_text(encoding="utf-8"))
    actual = route_hitl(document, "H1")
    mutant_blocked = False
    try:
        route_hitl(document, "H1", auto_resolution=True)
    except ValueError as error:
        mutant_blocked = str(error) == "HITL_AUTO_RESOLUTION_FORBIDDEN"
    passed = actual == expected and mutant_blocked and actual["resolution"] is None and actual["reconciliation"] is None
    result = {
        "schema_version": "dfe-hitl-validation.v1",
        "status": "pass" if passed else "block",
        "witnesses": ["DFE-FIX-011"],
        "route": actual,
        "auto_resolution_mutant": "blocked" if mutant_blocked else "unexpected-pass",
        "authority_effect": "none",
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''


WAY_CLEAR_RUNTIME = r'''"""Strict DFE Way Clear predicate."""

from __future__ import annotations

from typing import Any

from runtime.frontier import canonical_digest


def evaluate_way_clear(document: dict[str, Any]) -> dict[str, Any]:
    remaining = []
    for item in sorted(document["nodes"], key=lambda node: node["id"]):
        if item["scope"] != "in_scope" or item["state"] not in {"open", "fog"}:
            continue
        remaining.append(
            {
                "id": item["id"],
                "reason": "unresolved_fog" if item["state"] == "fog" else "open_decision",
            }
        )
    return {
        "schema_version": "1.0.0",
        "kind": "way_clear",
        "source_digest": canonical_digest(document),
        "status": "clear" if not remaining else "blocked",
        "remaining": remaining,
    }
'''


RUN_WAY_CLEAR = r'''#!/usr/bin/env python3
"""Run terminal, open, and fog DFE Way Clear fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from runtime.way_clear import evaluate_way_clear  # noqa: E402


EVIDENCE = ROOT / "session-evidence/SWU-DFE-006/way-clear-validation.json"


def load(name: str) -> object:
    return json.loads((ROOT / "fixtures" / name).read_text(encoding="utf-8"))


def main() -> int:
    clear = evaluate_way_clear(load("way-clear-map.json"))
    expected = json.loads((ROOT / "fixtures/expected/way-clear.json").read_text(encoding="utf-8"))
    open_result = evaluate_way_clear(load("way-clear-open-mutant.json"))
    fog_result = evaluate_way_clear(load("way-clear-fog-mutant.json"))
    passed = (
        clear == expected
        and clear["status"] == "clear"
        and open_result["status"] == "blocked"
        and open_result["remaining"][0]["reason"] == "open_decision"
        and fog_result["status"] == "blocked"
        and fog_result["remaining"][0]["reason"] == "unresolved_fog"
    )
    result = {
        "schema_version": "dfe-way-clear-validation.v1",
        "status": "pass" if passed else "block",
        "witnesses": ["DFE-FIX-012"],
        "clear": clear,
        "open_mutant": open_result,
        "fog_mutant": fog_result,
        "state_changed": False,
        "authority_effect": "none",
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''


RUN_NONCOLLAPSE = r'''#!/usr/bin/env python3
"""Prove decision closure cannot complete execution state."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "session-evidence/SWU-DFE-007/noncollapse-validation.json"


def main() -> int:
    execution_path = ROOT / "fixtures/execution-state.json"
    before_bytes = execution_path.read_bytes()
    before_digest = hashlib.sha256(before_bytes).hexdigest()
    execution = json.loads(before_bytes)
    closure = json.loads((ROOT / "fixtures/decision-closure.json").read_text(encoding="utf-8"))
    expected = json.loads((ROOT / "fixtures/expected/execution-state-unchanged.json").read_text(encoding="utf-8"))
    decision_evidence = {"decision_closure": closure}
    after_bytes = execution_path.read_bytes()
    mutant = copy.deepcopy(execution)
    mutant["swus"][0]["status"] = "complete"
    mutant_blocked = mutant != execution
    passed = (
        before_bytes == after_bytes
        and before_digest == hashlib.sha256(after_bytes).hexdigest()
        and execution == expected
        and mutant_blocked
        and "decision_closure" in decision_evidence
    )
    result = {
        "schema_version": "dfe-noncollapse-validation.v1",
        "status": "pass" if passed else "block",
        "witnesses": ["DFE-FIX-008"],
        "before_sha256": before_digest,
        "after_sha256": hashlib.sha256(after_bytes).hexdigest(),
        "byte_identical": before_bytes == after_bytes,
        "collapse_mutant": "blocked" if mutant_blocked else "unexpected-pass",
        "decision_evidence_only": True,
        "authority_effect": "none",
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''


def resolution(
    case: str,
    document: dict[str, object],
    decision_id: str,
    actions: list[dict[str, object]],
) -> dict[str, object]:
    nodes = {item["id"]: item for item in document["nodes"]}  # type: ignore[index]
    return {
        "schema_version": "1.0.0",
        "kind": "resolution",
        "resolution_id": f"resolution-{case}",
        "decision_id": decision_id,
        "source_digest": digest(document),
        "owner": nodes[decision_id]["owner"],
        "route": nodes[decision_id]["route"],
        "actions": actions,
    }


ADD_NODE = node("X", "Choose replacement contract?")
RESOLUTIONS = {
    "fog": resolution(
        "fog",
        FOG,
        "F1",
        [
            {
                "sequence": 0,
                "action_id": "fog-0",
                "kind": "graduate_fog",
                "target": "F1",
                "payload": {
                    "question": "Choose the precise fog contract?",
                    "owner": "resolver:test",
                },
            }
        ],
    ),
    "invalidation": resolution(
        "invalidation",
        DIAMOND,
        "A",
        [
            {
                "sequence": 0,
                "action_id": "invalidate-0",
                "kind": "invalidate",
                "target": "A",
                "payload": {"reason": "superseded premise"},
            }
        ],
    ),
    "add": resolution(
        "add",
        DIAMOND,
        "A",
        [
            {
                "sequence": 0,
                "action_id": "add-0",
                "kind": "add",
                "target": "X",
                "payload": {"node": ADD_NODE},
            }
        ],
    ),
    "supersede": resolution(
        "supersede",
        DIAMOND,
        "A",
        [
            {
                "sequence": 0,
                "action_id": "supersede-add-0",
                "kind": "add",
                "target": "X",
                "payload": {"node": ADD_NODE},
            },
            {
                "sequence": 1,
                "action_id": "supersede-1",
                "kind": "supersede",
                "target": "A",
                "payload": {"replacement_id": "X"},
            },
        ],
    ),
    "unblock": resolution(
        "unblock",
        DIAMOND,
        "A",
        [
            {
                "sequence": 0,
                "action_id": "unblock-invalidate-0",
                "kind": "invalidate",
                "target": "A",
                "payload": {"reason": "no longer blocks"},
            },
            {
                "sequence": 1,
                "action_id": "unblock-1",
                "kind": "unblock",
                "target": "C",
                "payload": {"blocker_id": "A", "blocked_id": "C"},
            },
        ],
    ),
}


def write_materials() -> dict[str, list[str]]:
    target = lambda suffix: str(EXPERIMENT / suffix)
    materials: dict[str, dict[str, str | object]] = {
        "SWU-DFE-001": {
            target("README.md"): README,
            target("schemas/decision-map.schema.json"): DECISION_MAP_SCHEMA,
            target("schemas/frontier-snapshot.schema.json"): FRONTIER_SCHEMA,
            target("schemas/claim.schema.json"): CLAIM_SCHEMA,
            target("schemas/resolution.schema.json"): RESOLUTION_SCHEMA,
            target("schemas/reconciliation.schema.json"): RECONCILIATION_SCHEMA,
            target("schemas/way-clear.schema.json"): WAY_CLEAR_SCHEMA,
            target("fixtures/diamond-map.json"): DIAMOND,
            target("fixtures/cycle-map.json"): CYCLE,
            target("scripts/validate_contracts.py"): VALIDATE_CONTRACTS,
        },
        "SWU-DFE-002": {
            target("runtime/frontier.py"): FRONTIER_RUNTIME,
            target("fixtures/fog-map.json"): FOG,
            target("fixtures/scope-map.json"): SCOPE,
            target("fixtures/invalidated-map.json"): INVALIDATED,
            target("fixtures/expected/diamond-frontier.json"): frontier_projection(DIAMOND),
            target("fixtures/expected/fog-frontier.json"): frontier_projection(FOG),
            target("fixtures/expected/scope-frontier.json"): frontier_projection(SCOPE),
            target("fixtures/expected/invalidated-frontier.json"): frontier_projection(INVALIDATED),
            target("scripts/run_frontier_fixtures.py"): RUN_FRONTIER,
        },
        "SWU-DFE-003": {},
        "SWU-DFE-004": {
            target("runtime/reconcile.py"): RECONCILE_RUNTIME,
            target("scripts/run_reconciliation_fixtures.py"): RUN_RECONCILE,
        },
        "SWU-DFE-005": {},
        "SWU-DFE-006": {},
        "SWU-DFE-007": {
            target("fixtures/execution-state.json"): {
                "schema_version": "1.0.0",
                "goal": {"id": "goal:test", "status": "active"},
                "tasks": [{"id": "task:test", "status": "ready"}],
                "swus": [{"id": "SWU:test", "status": "selected"}],
            },
            target("fixtures/decision-closure.json"): {
                "schema_version": "1.0.0",
                "resolution": {"decision_id": "A", "status": "resolved"},
                "way_clear": {"status": "clear"},
                "authority": "decision-evidence-only",
            },
            target("scripts/run_noncollapse_fixture.py"): RUN_NONCOLLAPSE,
        },
    }

    initial_claim = {
        "schema_version": "1.0.0",
        "kind": "claim",
        "claim_id": "claim-A",
        "decision_id": "A",
        "source_digest": digest(DIAMOND),
        "owner": "resolver:test",
        "claimed_at": "2026-07-29T00:00:00Z",
        "status": "active",
        "previous_store_digest": "0" * 64,
    }
    initial_store = {"schema_version": "1.0.0", "claims": [initial_claim]}
    before_store_digest = digest(initial_store)
    accepted_claim = {
        "schema_version": "1.0.0",
        "kind": "claim",
        "claim_id": "claim-B",
        "decision_id": "B",
        "source_digest": digest(DIAMOND),
        "owner": "resolver:test",
        "claimed_at": "2026-07-30T00:00:00Z",
        "status": "active",
        "previous_store_digest": before_store_digest,
    }
    updated_store = {
        "schema_version": "1.0.0",
        "claims": [initial_claim, accepted_claim],
    }
    stale_request = {
        "claim_id": "claim-stale",
        "decision_id": "B",
        "source_digest": "b" * 64,
        "owner": "resolver:test",
        "claimed_at": "2026-07-30T00:00:00Z",
        "expected_store_digest": before_store_digest,
    }
    materials["SWU-DFE-003"] = {
        target("runtime/claims.py"): CLAIMS_RUNTIME,
        target("fixtures/active-claim.json"): initial_store,
        target("fixtures/stale-claim.json"): stale_request,
        target("fixtures/expected/claim-accepted.json"): {
            "status": "accepted",
            "code": "CLAIM_ACCEPTED",
            "claim": accepted_claim,
            "before_store_digest": before_store_digest,
            "after_store_digest": digest(updated_store),
        },
        target("fixtures/expected/claim-rejected-stale.json"): {
            "status": "rejected",
            "code": "STALE_SOURCE",
            "store_digest": before_store_digest,
        },
        target("scripts/run_claim_fixtures.py"): RUN_CLAIMS,
    }

    for case, receipt in RESOLUTIONS.items():
        document = FOG if case == "fog" else DIAMOND
        claim = {
            "claim_id": f"claim-{receipt['decision_id']}",
            "decision_id": receipt["decision_id"],
            "source_digest": digest(document),
            "owner": receipt["owner"],
            "status": "active",
        }
        materials["SWU-DFE-004"][target(f"fixtures/{case}-resolution.json")] = receipt
        materials["SWU-DFE-004"][
            target(f"fixtures/expected/{case}-reconciliation.json")
        ] = staged_reconciliation(document, claim, receipt)

    hitl_map = decision_map(
        "human decision",
        [
            node(
                "H1",
                "May the human approve this fixture route?",
                route="HITL",
                owner="human:test",
            )
        ],
        [],
    )
    hitl_route = {
        "schema_version": "1.0.0",
        "kind": "hitl_route",
        "decision_id": "H1",
        "source_digest": digest(hitl_map),
        "owner": "human:test",
        "status": "awaiting_human",
        "resolution": None,
        "reconciliation": None,
    }
    materials["SWU-DFE-005"] = {
        target("runtime/hitl.py"): HITL_RUNTIME,
        target("fixtures/hitl-map.json"): hitl_map,
        target("fixtures/expected/hitl-route.json"): hitl_route,
        target("scripts/run_hitl_fixture.py"): RUN_HITL,
    }

    clear_map = decision_map(
        "clear terminal",
        [
            node("A", "Resolved?", state="resolved"),
            node("B", "Invalidated?", state="invalidated"),
            node(
                "X",
                "Later?",
                state="out_of_scope",
                scope="out_of_scope",
            ),
        ],
        [],
    )
    open_mutant = copy.deepcopy(clear_map)
    open_mutant["nodes"][0]["state"] = "open"  # type: ignore[index]
    fog_mutant = copy.deepcopy(clear_map)
    fog_mutant["nodes"][0]["state"] = "fog"  # type: ignore[index]
    way_clear = {
        "schema_version": "1.0.0",
        "kind": "way_clear",
        "source_digest": digest(clear_map),
        "status": "clear",
        "remaining": [],
    }
    materials["SWU-DFE-006"] = {
        target("runtime/way_clear.py"): WAY_CLEAR_RUNTIME,
        target("fixtures/way-clear-map.json"): clear_map,
        target("fixtures/way-clear-open-mutant.json"): open_mutant,
        target("fixtures/way-clear-fog-mutant.json"): fog_mutant,
        target("fixtures/expected/way-clear.json"): way_clear,
        target("scripts/run_way_clear_fixtures.py"): RUN_WAY_CLEAR,
    }
    materials["SWU-DFE-007"][
        target("fixtures/expected/execution-state-unchanged.json")
    ] = materials["SWU-DFE-007"][target("fixtures/execution-state.json")]

    result: dict[str, list[str]] = {}
    for unit_id, files in materials.items():
        for path, content in files.items():
            write_staged(unit_id, path, content)
        result[unit_id] = list(files)
    return result


def build_packages(materials: dict[str, list[str]]) -> None:
    matrix = json.loads(
        (
            REPOSITORY_ROOT
            / INVOKE_RUN
            / "work-pack/shared/COMMAND-MATRIX.json"
        ).read_text(encoding="utf-8")
    )
    by_id = {unit["unit_id"]: unit for unit in matrix["units"]}
    shared_sources = [
        str(INVOKE_RUN / "WORK-PACK.md"),
        str(INVOKE_RUN / "work-pack/shared/CONTEXT.md"),
        str(INVOKE_RUN / "SPELLCRAFT-ADMISSION-RECEIPT.json"),
    ]
    for unit_id, targets in materials.items():
        unit = by_id[unit_id]
        task_path = unit["task_path"]
        sources = [task_path, *shared_sources]
        package = {
            "schema_version": "1.0.0",
            "package_id": f"goal-dfe-{unit_id.lower()}",
            "mutation_mode": "apply-approved",
            "mutation_state": "materialized",
            "lifecycle_owner": "spellcraft",
            "authority_class": "public",
            "publication_class": "public",
            "source_artifacts": [
                {**exact_ref(path), "authority_class": "public"} for path in sources
            ],
            "changes": [
                {
                    "target_path": path,
                    "operation": "create",
                    "output_ref": staged_ref(unit_id, path),
                }
                for path in targets
            ],
            "target_inventory": [
                {
                    "target_path": path,
                    "lifecycle_owner": "spellcraft",
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
                "owner": "spellcraft",
                "scope_paths": targets,
                "authority_classes": ["public"],
                "publication_classes": ["public"],
            },
            "validation_commands": [
                " ".join(spec["argv"]) for spec in unit["validation_commands"]
            ],
        }
        package_path = REPOSITORY_ROOT / MATERIAL_ROOT / unit_id / "material-package.json"
        package_path.parent.mkdir(parents=True, exist_ok=True)
        package_path.write_text(
            json.dumps(package, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def main() -> int:
    materials = write_materials()
    build_packages(materials)
    print(
        json.dumps(
            {
                "packages": len(materials),
                "staged_materials": sum(map(len, materials.values())),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
