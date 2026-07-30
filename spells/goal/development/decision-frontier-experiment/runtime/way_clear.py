"""Strict DFE Way Clear predicate."""

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
