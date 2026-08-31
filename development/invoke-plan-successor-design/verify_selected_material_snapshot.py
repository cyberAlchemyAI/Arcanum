#!/usr/bin/env python3
"""Independently verify a Design selected-material snapshot against live origins."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
from pathlib import Path
from typing import Any


IDENTITY = "invoke.verify-design-selected-material-snapshot.v1"


def digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def enumerate_origins(repo: Path, request: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    document = request["document"]
    roots = {item["root_id"]: item for item in document["roots"]}
    entries: list[dict[str, Any]] = []
    blockers: list[str] = []
    seen: dict[str, str] = {}
    for rule in document["discovery_rules"]:
        if rule["root_id"] == "root:define-refresh":
            continue
        binding = roots[rule["root_id"]]
        root_path = (repo / binding["path"]).resolve()
        matched = 0
        for child in sorted(root_path.rglob("*")):
            if child.is_symlink():
                blockers.append(f"symlink:{child.relative_to(repo).as_posix()}")
                continue
            if not child.is_file():
                continue
            relative = child.relative_to(root_path).as_posix()
            if not any(fnmatch.fnmatchcase(relative, pattern) for pattern in rule["include_globs"]):
                continue
            origin = f"{binding['path'].rstrip('/')}/{relative}"
            if origin in seen:
                blockers.append(f"ambiguous:{origin}:{seen[origin]}:{rule['rule_id']}")
                continue
            seen[origin] = rule["rule_id"]
            data = child.read_bytes()
            entries.append({
                "origin_path": origin,
                "snapshot_relative_path": f"materials/{rule['root_id'].replace(':', '-')}/{relative}",
                "sha256": hashlib.sha256(data).hexdigest(),
                "size": len(data),
                "rule_id": rule["rule_id"],
                "input_class": rule["input_class"],
            })
            matched += 1
        if matched == 0:
            blockers.append(f"empty-rule:{rule['rule_id']}")
    entries.sort(key=lambda item: (item["rule_id"], item["origin_path"]))
    return entries, sorted(blockers)


def build_receipt(repo: Path, request_path: Path, snapshot_root: Path) -> dict[str, Any]:
    request = load(request_path)
    manifest_path = snapshot_root / "SOURCE-INVENTORY.json"
    manifest = load(manifest_path)
    live_entries, blockers = enumerate_origins(repo, request)
    declared = manifest.get("entries", [])
    if manifest.get("entry_count") != len(declared):
        blockers.append("manifest-entry-count-mismatch")
    if manifest.get("snapshot_digest") != digest(declared):
        blockers.append("manifest-digest-mismatch")
    if live_entries != declared:
        live_by_origin = {item["origin_path"]: item for item in live_entries}
        declared_by_origin = {item["origin_path"]: item for item in declared}
        for path in sorted(set(live_by_origin) - set(declared_by_origin)):
            blockers.append(f"origin-added:{path}")
        for path in sorted(set(declared_by_origin) - set(live_by_origin)):
            blockers.append(f"origin-removed:{path}")
        for path in sorted(set(live_by_origin) & set(declared_by_origin)):
            if live_by_origin[path] != declared_by_origin[path]:
                blockers.append(f"origin-modified:{path}")
    declared_snapshot_paths = {item["snapshot_relative_path"] for item in declared}
    actual_snapshot_paths = {
        child.relative_to(snapshot_root).as_posix()
        for child in snapshot_root.rglob("*")
        if child.is_file() and child.name != "SOURCE-INVENTORY.json"
    }
    for path in sorted(actual_snapshot_paths - declared_snapshot_paths):
        blockers.append(f"snapshot-extra:{path}")
    for path in sorted(declared_snapshot_paths - actual_snapshot_paths):
        blockers.append(f"snapshot-missing:{path}")
    for entry in declared:
        target = snapshot_root / entry["snapshot_relative_path"]
        if not target.is_file() or target.is_symlink():
            continue
        data = target.read_bytes()
        if hashlib.sha256(data).hexdigest() != entry["sha256"] or len(data) != entry["size"]:
            blockers.append(f"snapshot-mismatch:{entry['snapshot_relative_path']}")
    blockers = sorted(set(blockers))
    script = Path(__file__).resolve()
    request_data = request_path.read_bytes()
    manifest_data = manifest_path.read_bytes()
    receipt = {
        "schema_version": "invoke.design-selected-material-verification.v1",
        "verification_id": f"verification:{digest(declared)[:20]}",
        "validator": {
            "identity": IDENTITY,
            "path": script.relative_to(repo).as_posix(),
            "sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        },
        "bindings": {
            "boundary_request": {
                "path": request_path.relative_to(repo).as_posix(),
                "sha256": hashlib.sha256(request_data).hexdigest(),
                "size": len(request_data),
            },
            "snapshot_manifest": {
                "path": manifest_path.relative_to(repo).as_posix(),
                "sha256": hashlib.sha256(manifest_data).hexdigest(),
                "size": len(manifest_data),
            },
            "snapshot_digest": manifest.get("snapshot_digest"),
        },
        "checks": {
            "origin_inventory_equal": live_entries == declared,
            "snapshot_inventory_equal": actual_snapshot_paths == declared_snapshot_paths,
            "snapshot_bytes_equal": not any(item.startswith("snapshot-mismatch:") for item in blockers),
            "rule_enumeration_complete": not any(item.startswith(("empty-rule:", "ambiguous:")) for item in blockers),
        },
        "entry_count": len(declared),
        "result": "pass" if not blockers else "block",
        "blockers": blockers,
        "claim_ceiling": "Proves origin fidelity and completeness only for the exact selected rules, repository bytes, and snapshot bound by this receipt.",
        "authority_effect": "none",
        "receipt_digest": "0" * 64,
    }
    receipt["receipt_digest"] = digest({key: value for key, value in receipt.items() if key != "receipt_digest"})
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--boundary-request", required=True, type=Path)
    parser.add_argument("--snapshot-root", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expected-receipt", type=Path)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    receipt = build_receipt(
        repo,
        args.boundary_request.resolve(),
        args.snapshot_root.resolve(),
    )
    if args.expected_receipt is not None:
        expected = load(args.expected_receipt)
        if receipt != expected:
            receipt["result"] = "block"
            receipt["blockers"] = sorted(set(receipt["blockers"] + ["expected-receipt-mismatch"]))
    if args.output is not None:
        if args.output.exists() or args.output.is_symlink():
            raise ValueError("--output must be absent")
        args.output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True))
    return 0 if receipt["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
