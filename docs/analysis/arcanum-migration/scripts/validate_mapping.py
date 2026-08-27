#!/usr/bin/env python3
"""Validate an Arcanum current-system mapping package without mutating it."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ModuleNotFoundError:
    print(
        "BLOCK: missing dependency 'jsonschema'; install "
        "docs/analysis/arcanum-migration/requirements.txt",
        file=sys.stderr,
    )
    raise SystemExit(2)


SCRIPT = Path(__file__).resolve()
AREA = SCRIPT.parent.parent
DEFAULT_SCHEMA = AREA / "contracts" / "current-system-map.schema.json"
DEFAULT_MAP = AREA / "mapping" / "current-system-map.json"
DEFAULT_PROJECT_ROOT = SCRIPT.parents[4]


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"missing file: {path}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON at {path}:{exc.lineno}:{exc.colno}: {exc.msg}") from None


def duplicate_values(values: list[str]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def find_untyped_unknowns(value: Any, path: str = "") -> list[str]:
    """Reject the exact sentinel 'unknown' outside the governed unknowns collection."""
    if isinstance(value, str):
        return [path or "/"] if value.strip().lower() == "unknown" else []
    if isinstance(value, list):
        return [
            found
            for index, item in enumerate(value)
            for found in find_untyped_unknowns(item, f"{path}/{index}")
        ]
    if isinstance(value, dict):
        return [
            found
            for key, item in value.items()
            if key != "unknowns"
            for found in find_untyped_unknowns(item, f"{path}/{key}")
        ]
    return []


def validate_baseline(baseline: dict[str, Any], project_root: Path) -> list[str]:
    errors: list[str] = []
    if baseline["kind"] == "clean-git":
        result = subprocess.run(
            ["git", "rev-parse", "--verify", f"{baseline['git_ref']}^{{commit}}"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            errors.append(f"baseline git_ref is not resolvable: {baseline['git_ref']}")
        elif result.stdout.strip().lower() != baseline["repository_head"]:
            errors.append("baseline git_ref does not resolve to baseline.repository_head")
    else:
        locator = Path(baseline["bundle_locator"])
        bundle = locator if locator.is_absolute() else project_root / locator
        if not bundle.is_file():
            errors.append(f"baseline bundle is not retrievable: {baseline['bundle_locator']}")
        else:
            digest = hashlib.sha256(bundle.read_bytes()).hexdigest()
            if digest != baseline["bundle_sha256"]:
                errors.append("baseline bundle_sha256 does not match the retrievable bundle")
    return errors


def validate_semantics(document: dict[str, Any], project_root: Path) -> list[str]:
    errors = validate_baseline(document["baseline"], project_root)
    for path in find_untyped_unknowns(document):
        errors.append(f"untyped 'unknown' sentinel at {path}; use a governed unknowns entry")
    inventory_ids = set(document["inventory_ids"])
    relation_ids = [record["relation_id"] for record in document["relation_records"]]
    relation_id_set = set(relation_ids)
    open_item_ids = [item["open_item_id"] for item in document["open_items"]]
    open_item_id_set = set(open_item_ids)
    edge_ids = [edge["edge_id"] for edge in document["discovery"]["edges"]]

    for label, values in (
        ("relation_id", relation_ids),
        ("open_item_id", open_item_ids),
        ("edge_id", edge_ids),
    ):
        for duplicate in sorted(duplicate_values(values)):
            errors.append(f"duplicate {label}: {duplicate}")

    covered_inventory: set[str] = set()
    blocking_unknowns = False
    for record in document["relation_records"]:
        inventory_id = record["inventory_id"]
        if inventory_id not in inventory_ids:
            errors.append(f"{record['relation_id']} references undeclared inventory_id {inventory_id}")
        if not record["relation_id"].startswith(f"REL-{inventory_id}-"):
            errors.append(
                f"{record['relation_id']} must begin with REL-{inventory_id}- to preserve deterministic identity"
            )
        covered_inventory.add(inventory_id)
        blocking_unknowns = blocking_unknowns or any(item["blocking"] for item in record["unknowns"])

        for evidence in record["evidence"]:
            locator = evidence["locator"].split("#", 1)[0]
            locator_path = Path(locator)
            if locator_path.is_absolute() or ".." in locator_path.parts:
                errors.append(f"{record['relation_id']} has a non-repository-relative evidence locator: {locator}")
                continue
            if document["baseline"]["kind"] == "clean-git":
                result = subprocess.run(
                    ["git", "show", f"{document['baseline']['repository_head']}:{locator}"],
                    cwd=project_root,
                    capture_output=True,
                    check=False,
                )
                if result.returncode != 0:
                    errors.append(
                        f"{record['relation_id']} evidence is not retrievable from the clean baseline: {locator}"
                    )
                elif hashlib.sha256(result.stdout).hexdigest() != evidence["source_sha256"]:
                    errors.append(
                        f"{record['relation_id']} evidence hash does not match clean baseline bytes: {locator}"
                    )
            elif locator not in document["baseline"]["included_paths"]:
                errors.append(
                    f"{record['relation_id']} evidence is absent from baseline.included_paths: {locator}"
                )

    for inventory_id in sorted(inventory_ids - covered_inventory):
        errors.append(f"inventory_id has no relation record: {inventory_id}")

    for edge in document["discovery"]["edges"]:
        if edge["status"] == "mapped":
            for relation_id in edge["relation_ids"]:
                if relation_id not in relation_id_set:
                    errors.append(f"{edge['edge_id']} references missing relation_id {relation_id}")
        elif edge["status"] == "blocked" and edge["open_item_id"] not in open_item_id_set:
            errors.append(f"{edge['edge_id']} references missing open_item_id {edge['open_item_id']}")

    blocking_open = any(
        item["blocking"] and item["status"] != "resolved" for item in document["open_items"]
    )
    derived_structural = not errors
    derived_decision_ready = derived_structural and not blocking_unknowns and not blocking_open
    completion = document["completion"]
    if completion["structurally_complete"] != derived_structural:
        errors.append(
            "completion.structurally_complete does not match inventory, relation, edge, and baseline closure"
        )
    if completion["decision_ready"] != derived_decision_ready:
        errors.append(
            "completion.decision_ready must be false while a blocking unknown/open item remains"
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mapping", nargs="?", type=Path, default=DEFAULT_MAP)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--project-root", type=Path, default=DEFAULT_PROJECT_ROOT)
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args()

    try:
        schema = load_json(args.schema.resolve())
        document = load_json(args.mapping.resolve())
    except ValueError as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 2

    Draft202012Validator.check_schema(schema)
    shape_errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda error: list(error.absolute_path),
    )
    errors = [
        f"/{'/'.join(str(part) for part in error.absolute_path)}: {error.message}"
        for error in shape_errors
    ]
    if not errors:
        errors.extend(validate_semantics(document, args.project_root.resolve()))
    if args.require_ready and not errors and not document["completion"]["decision_ready"]:
        errors.append("mapping is structurally valid but not decision-ready")

    if errors:
        for error in errors:
            print(f"BLOCK: {error}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "status": "pass",
                "mapping": str(args.mapping),
                "relation_count": len(document["relation_records"]),
                "edge_count": len(document["discovery"]["edges"]),
                "decision_ready": document["completion"]["decision_ready"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
