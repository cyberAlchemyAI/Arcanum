#!/usr/bin/env python3
"""Freeze only files selected by a Design boundary, preserving origin bindings."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--boundary-request", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    output = args.output.resolve()
    if output.exists() or output.is_symlink():
        raise ValueError("--output must be absent")
    if not output.parent.is_dir():
        raise ValueError("--output parent must exist")
    request = json.loads(args.boundary_request.read_text(encoding="utf-8"))
    document = request["document"]
    roots = {item["root_id"]: item for item in document["roots"]}
    entries: list[dict[str, Any]] = []
    seen: dict[str, str] = {}
    for rule in document["discovery_rules"]:
        if rule["root_id"] == "root:define-refresh":
            continue
        binding = roots[rule["root_id"]]
        root_path = (repo / binding["path"]).resolve()
        if repo not in root_path.parents:
            raise ValueError(f"root escapes repository: {binding['path']}")
        matched = 0
        for child in sorted(root_path.rglob("*")):
            if child.is_symlink():
                raise ValueError(f"symlink unsupported: {child}")
            if not child.is_file():
                continue
            relative = child.relative_to(root_path).as_posix()
            if not any(fnmatch.fnmatchcase(relative, pattern) for pattern in rule["include_globs"]):
                continue
            origin = f"{binding['path'].rstrip('/')}/{relative}"
            if origin in seen:
                raise ValueError(f"ambiguous selected file: {origin} ({seen[origin]}, {rule['rule_id']})")
            seen[origin] = rule["rule_id"]
            data = child.read_bytes()
            root_label = rule["root_id"].replace(":", "-")
            snapshot_relative = f"materials/{root_label}/{relative}"
            entries.append({
                "origin_path": origin,
                "snapshot_relative_path": snapshot_relative,
                "sha256": hashlib.sha256(data).hexdigest(),
                "size": len(data),
                "rule_id": rule["rule_id"],
                "input_class": rule["input_class"],
            })
            matched += 1
        if matched == 0:
            raise ValueError(f"discovery rule matched no files: {rule['rule_id']}")
    entries.sort(key=lambda item: (item["rule_id"], item["origin_path"]))

    stage = Path(tempfile.mkdtemp(prefix=f".{output.name}.", dir=output.parent))
    try:
        for entry in entries:
            source = repo / entry["origin_path"]
            data = source.read_bytes()
            if hashlib.sha256(data).hexdigest() != entry["sha256"] or len(data) != entry["size"]:
                raise ValueError(f"selected source changed during snapshot: {entry['origin_path']}")
            target = stage / entry["snapshot_relative_path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        manifest = {
            "schema_version": "invoke.design-selected-material-snapshot.v1",
            "snapshot_id": f"snapshot:{canonical_digest(entries)[:20]}",
            "observation_epoch": document["observation_epoch"],
            "source_boundary_request": args.boundary_request.resolve().relative_to(repo).as_posix(),
            "entries": entries,
            "entry_count": len(entries),
            "authority_effect": "none",
            "snapshot_digest": canonical_digest(entries),
        }
        (stage / "SOURCE-INVENTORY.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        for entry in entries:
            source = repo / entry["origin_path"]
            data = source.read_bytes()
            if hashlib.sha256(data).hexdigest() != entry["sha256"] or len(data) != entry["size"]:
                raise ValueError(f"selected source changed after snapshot: {entry['origin_path']}")
        os.replace(stage, output)
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise
    print(json.dumps({"output": output.as_posix(), "entry_count": len(entries), "snapshot_digest": canonical_digest(entries)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
