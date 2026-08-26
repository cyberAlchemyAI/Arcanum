#!/usr/bin/env python3
"""List diagram bundles and resolve the latest active revision from manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_SCHEMA = ROOT / "schemas" / "diagram-bundle-manifest.schema.yml"
RECEIPT_SCHEMA = ROOT / "schemas" / "diagram-validation-receipt.schema.yml"
COMMIT_SCHEMA = ROOT / "schemas" / "diagram-commit-marker.schema.yml"
VALIDATOR = Path(__file__).with_name("validate_diagram_bundle.py")


def load_manifest(path: Path) -> dict[str, Any] | None:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError):
        return None
    return value if isinstance(value, dict) else None


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_resolvable(bundle: Path, manifest: dict[str, Any]) -> bool:
    """Reject any bundle that cannot pass full, non-mutating validation."""
    receipt = load_manifest(bundle / "validation.receipt.yml")
    manifest_path = bundle / "diagram.meta.yml"
    if not receipt or receipt.get("diagram_id") != manifest.get("diagram_id"):
        return False
    if receipt.get("revision") != manifest.get("revision"):
        return False
    try:
        manifest_schema = load_manifest(MANIFEST_SCHEMA)
        receipt_schema = load_manifest(RECEIPT_SCHEMA)
        commit_schema = load_manifest(COMMIT_SCHEMA)
        if not manifest_schema or not receipt_schema or not commit_schema:
            return False
        if list(Draft202012Validator(manifest_schema, format_checker=FormatChecker()).iter_errors(manifest)):
            return False
        if list(Draft202012Validator(receipt_schema, format_checker=FormatChecker()).iter_errors(receipt)):
            return False
        if receipt.get("observed_manifest_sha256") != sha256(manifest_path):
            return False
        output_root = bundle.parents[1]
        commit_path = (
            output_root / ".evidence-grounded-diagrams" / "commits"
            / str(manifest.get("diagram_id")) / f"{manifest.get('revision')}.yml"
        )
        commit = load_manifest(commit_path)
        if not commit or list(
            Draft202012Validator(commit_schema, format_checker=FormatChecker()).iter_errors(commit)
        ):
            return False
        if (
            commit.get("diagram_id") != manifest.get("diagram_id")
            or commit.get("revision") != manifest.get("revision")
            or Path(str(commit.get("bundle_path", ""))).resolve() != bundle.resolve()
            or commit.get("manifest_sha256") != sha256(manifest_path)
        ):
            return False
        records = receipt.get("observed_members", [])
        paths = [item.get("path") for item in records if isinstance(item, dict)]
        if len(paths) != len(records) or len(paths) != len(set(paths)):
            return False
        expected_records = {
            record["path"]: record["sha256"]
            for name, record in manifest.get("members", {}).items()
            if name != "validation_receipt" and isinstance(record, dict)
        }
        receipt_records = {item["path"]: item["sha256"] for item in records}
        if receipt_records != expected_records:
            return False
        for relative, digest in expected_records.items():
            candidate = Path(str(relative))
            if candidate.is_absolute() or ".." in candidate.parts:
                return False
            member = (bundle / candidate).resolve()
            member.relative_to(bundle.resolve())
            if not member.is_file() or sha256(member) != digest:
                return False
    except (OSError, TypeError, ValueError):
        return False
    checks = receipt.get("checks", {})
    for name in ("schema_shape", "referential_integrity", "persistence"):
        if checks.get(name, {}).get("status") != "PASS":
            return False
    if receipt.get("overall") not in {"PASS", "DRAFT"}:
        return False
    command = [sys.executable, str(VALIDATOR), str(bundle)]
    attestation = receipt.get("manual_attestation")
    if isinstance(attestation, dict):
        attestation_path = Path(str(attestation.get("path", "")))
        try:
            if not attestation_path.is_file() or sha256(attestation_path) != attestation.get("sha256"):
                return False
        except OSError:
            return False
        command.extend(["--manual-attestation", str(attestation_path)])
    try:
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return result.returncode == 0


def apply_effective_lifecycle(records: list[dict[str, Any]]) -> None:
    """Derive superseded state only from validated/published descendants."""
    by_revision = {
        (str(record["diagram_id"]), str(record["revision"])): record
        for record in records
    }
    superseded: set[tuple[str, str]] = set()
    for record in records:
        if record["declared_lifecycle"] not in {"validated", "published"}:
            continue
        diagram_id = str(record["diagram_id"])
        prior = record.get("supersedes_revision")
        seen: set[str] = set()
        while isinstance(prior, str) and prior not in seen:
            seen.add(prior)
            key = (diagram_id, prior)
            ancestor = by_revision.get(key)
            if ancestor is None:
                break
            superseded.add(key)
            prior = ancestor.get("supersedes_revision")
    for record in records:
        key = (str(record["diagram_id"]), str(record["revision"]))
        if record["declared_lifecycle"] == "rejected":
            record["lifecycle"] = "rejected"
        elif key in superseded:
            record["lifecycle"] = "superseded"


def resolve_current(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Prefer the newest validated/published revision over any newer draft."""
    grouped: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        if record["declared_lifecycle"] == "rejected":
            continue
        grouped.setdefault(str(record["diagram_id"]), []).append(record)

    current: list[dict[str, Any]] = []
    for diagram_records in grouped.values():
        governed = [
            record
            for record in diagram_records
            if record["declared_lifecycle"] in {"validated", "published"}
            and record["lifecycle"] != "superseded"
        ]
        candidates = governed or [
            record for record in diagram_records if record["lifecycle"] != "superseded"
        ]
        if candidates:
            current.append(max(candidates, key=lambda item: str(item["revision"])))
    return sorted(current, key=lambda item: str(item["diagram_id"]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_root", type=Path)
    parser.add_argument("--topic")
    parser.add_argument("--diagram-kind")
    parser.add_argument("--current", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    records: list[dict[str, Any]] = []
    for path in args.output_root.resolve().glob("*/*/diagram.meta.yml"):
        manifest = load_manifest(path)
        if not manifest or not is_resolvable(path.parent, manifest):
            continue
        tags = manifest.get("tags", {})
        if args.topic and args.topic not in tags.get("topics", []):
            continue
        if args.diagram_kind and args.diagram_kind != tags.get("diagram_kind"):
            continue
        records.append(
            {
                "diagram_id": manifest.get("diagram_id"),
                "revision": manifest.get("revision"),
                "lifecycle": manifest.get("lifecycle_status"),
                "declared_lifecycle": manifest.get("lifecycle_status"),
                "epistemic": manifest.get("aggregate_status"),
                "diagram_kind": tags.get("diagram_kind"),
                "topics": tags.get("topics", []),
                "validation_overall": (
                    load_manifest(path.parent / "validation.receipt.yml") or {}
                ).get("overall"),
                "supersedes_revision": (
                    manifest.get("supersedes", {}).get("revision")
                    if isinstance(manifest.get("supersedes"), dict)
                    else None
                ),
                "bundle": str(path.parent),
            }
        )
    records.sort(key=lambda item: (str(item["diagram_id"]), str(item["revision"])))
    apply_effective_lifecycle(records)
    selected_current = resolve_current(records) if args.current else records
    for record in records:
        record.pop("supersedes_revision", None)
    records = selected_current

    if args.json:
        print(json.dumps(records, indent=2, ensure_ascii=False))
    else:
        for record in records:
            print(
                f"{record['diagram_id']} {record['revision']} "
                f"{record['lifecycle']} {record['diagram_kind']} {record['bundle']}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
