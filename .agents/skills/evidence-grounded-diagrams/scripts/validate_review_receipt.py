#!/usr/bin/env python3
"""Validate the shape and decision consistency of a diagram review receipt."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "diagram-review-receipt.schema.yml"
MANIFEST_SCHEMA = ROOT / "schemas" / "diagram-bundle-manifest.schema.yml"


def load_mapping(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a mapping")
    return value


def validate(receipt: dict[str, Any]) -> list[str]:
    schema = load_mapping(SCHEMA)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [
        f"{'.'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(receipt), key=lambda item: list(item.absolute_path))
    ]
    findings = receipt.get("findings", [])
    ids = [item.get("finding_id") for item in findings if isinstance(item, dict)]
    if len(ids) != len(set(ids)):
        errors.append("finding_id values must be unique")
    first = receipt.get("first_blocker")
    material_blockers = [
        item for item in findings
        if isinstance(item, dict)
        and item.get("severity") == "blocker"
        and item.get("status") != "supported"
    ]
    if first is not None and first not in ids:
        errors.append("first_blocker must reference a finding_id in findings")
    elif first is not None:
        matched = next(item for item in findings if item.get("finding_id") == first)
        if matched not in material_blockers:
            errors.append("first_blocker must reference a material blocker-severity finding")
    verdict = receipt.get("verdict")
    if verdict == "FIX" and material_blockers:
        expected_first = material_blockers[0].get("finding_id")
        if first is None:
            errors.append("first_blocker is required when FIX retains a material blocker")
        elif first != expected_first:
            errors.append("first_blocker must reference the first material blocker in findings order")
    elif first is not None and (verdict != "FIX" or not material_blockers):
        errors.append("first_blocker must be null or omitted when FIX has no material blocker")
    if verdict == "PASS" and any(
        item.get("status") != "supported" for item in findings if isinstance(item, dict)
    ):
        errors.append("PASS cannot retain a non-supported finding")
    if verdict == "FIX" and not any(
        item.get("severity") in {"blocker", "major"}
        and item.get("status") in {"unsupported", "ambiguous", "inferred", "hypothetical", "unknown"}
        for item in findings
        if isinstance(item, dict)
    ):
        errors.append("FIX requires at least one material finding that is not supported")
    return errors


def normalized_source_digest_text(value: str, normalization: str) -> str:
    if normalization != "UTF-8, LF line endings, no trailing newline":
        raise ValueError(f"unsupported source normalization: {normalization}")
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(value.rstrip("\n").encode("utf-8")).hexdigest()


def normalized_source_digest(path: Path, normalization: str) -> str:
    return normalized_source_digest_text(path.read_text(encoding="utf-8"), normalization)


def validate_target(
    receipt: dict[str, Any], target_source: Path | None, target_stdin: str | None,
    bundle_root: Path | None
) -> list[str]:
    target = receipt.get("target", {})
    observed = target.get("observed_members", [])
    if target.get("kind") == "source":
        if target_source is None and target_stdin is None:
            return ["source receipt validation requires --target-source or --target-stdin"]
        source_records = [
            item for item in observed
            if isinstance(item, dict) and item.get("role") == "source"
        ]
        if len(source_records) != 1:
            return ["source receipt requires exactly one observed source member"]
        if len(observed) != 1 or target.get("render_inspected") is not False:
            return ["source receipt must observe only source bytes and cannot claim render inspection"]
        actual = (
            normalized_source_digest(target_source, target.get("normalization"))
            if target_source is not None
            else normalized_source_digest_text(target_stdin or "", target.get("normalization"))
        )
        return [] if source_records[0].get("sha256") == actual else ["reviewed source digest mismatch"]

    if target.get("kind") != "bundle":
        return ["target.kind must be bundle or source"]
    root_value = bundle_root or Path(str(target.get("bundle_path", "")))
    root = root_value.resolve()
    if not root.is_dir():
        return [f"reviewed bundle does not exist: {root}"]
    errors: list[str] = []
    declared_root = Path(str(target.get("bundle_path", ""))).resolve()
    if declared_root != root:
        errors.append("target.bundle_path does not identify the reviewed bundle")
    try:
        manifest = load_mapping(root / "diagram.meta.yml")
        manifest_schema = load_mapping(MANIFEST_SCHEMA)
        for error in Draft202012Validator(
            manifest_schema, format_checker=FormatChecker()
        ).iter_errors(manifest):
            errors.append(f"reviewed manifest: {error.message}")
    except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
        return errors + [f"cannot load reviewed manifest: {exc}"]
    if target.get("diagram_id") != manifest.get("diagram_id"):
        errors.append("target.diagram_id does not match reviewed manifest")
    if target.get("revision") != manifest.get("revision"):
        errors.append("target.revision does not match reviewed manifest")

    persisted_path = manifest.get("persistence", {}).get("bundle_path")
    if not isinstance(persisted_path, str) or Path(persisted_path).resolve() != root:
        errors.append("reviewed manifest persistence.bundle_path does not identify the reviewed bundle")

    members = manifest.get("members", {})
    role_to_member = {
        "manifest": {"path": "diagram.meta.yml"},
        "request": members.get("request", {}),
        "source": members.get("source", {}),
        "semantic-model": members.get("semantic_model", {}),
        "textual-equivalent": members.get("textual_equivalent", {}),
        "validation-receipt": members.get("validation_receipt", {}),
    }
    render = members.get("render")
    if isinstance(render, dict):
        role_to_member["render"] = render
    role_to_path = {
        role: member.get("path") if isinstance(member, dict) else None
        for role, member in role_to_member.items()
    }
    expected_roles = set(role_to_member)
    observed_records = [record for record in observed if isinstance(record, dict)]
    observed_roles = [record.get("role") for record in observed_records]
    observed_paths = [record.get("path") for record in observed_records]
    if len(observed_records) != len(observed):
        errors.append("every observed bundle member must be a mapping")
    if len(observed_roles) != len(set(observed_roles)):
        errors.append("observed bundle member roles must be unique")
    if len(observed_paths) != len(set(observed_paths)):
        errors.append("observed bundle member paths must be unique")
    expected_paths = list(role_to_path.values())
    if any(not isinstance(path, str) or not path for path in expected_paths):
        errors.append("reviewed manifest contains a missing review-relevant member path")
    if len(expected_paths) != len(set(expected_paths)):
        errors.append("reviewed manifest maps multiple review roles to the same member path")
    if set(observed_roles) != expected_roles:
        errors.append("review receipt does not cover the complete canonical bundle member set")
    if target.get("render_inspected") != ("render" in expected_roles):
        errors.append("render_inspected must match presence of an observed render member")

    for record in observed_records:
        role = record.get("role")
        relative = record.get("path")
        if not isinstance(relative, str):
            errors.append(f"observed {record.get('role')} member requires a path")
            continue
        if role_to_path.get(role) != relative:
            errors.append(f"observed {role} path differs from manifest")
            continue
        declared_digest = role_to_member.get(role, {}).get("sha256")
        if declared_digest is not None and declared_digest != record.get("sha256"):
            errors.append(f"observed {role} digest differs from manifest")
        candidate = Path(relative)
        if candidate.is_absolute() or ".." in candidate.parts:
            errors.append(f"unsafe observed member path: {relative}")
            continue
        member = (root / candidate).resolve()
        try:
            member.relative_to(root)
            actual = hashlib.sha256(member.read_bytes()).hexdigest()
        except (OSError, ValueError) as exc:
            errors.append(f"cannot read observed member {relative}: {exc}")
            continue
        if actual != record.get("sha256"):
            errors.append(f"reviewed member digest mismatch: {relative}")
        if declared_digest is not None and actual != declared_digest:
            errors.append(f"reviewed member bytes differ from manifest digest: {relative}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument("--target-source", type=Path)
    source_group.add_argument(
        "--target-stdin", action="store_true",
        help="read the exact inline source from standard input",
    )
    parser.add_argument("--bundle-root", type=Path)
    parser.add_argument("--shape-only", action="store_true")
    args = parser.parse_args()
    try:
        receipt = load_mapping(args.receipt)
        errors = validate(receipt)
        if not args.shape_only:
            inline_source = sys.stdin.read() if args.target_stdin else None
            errors.extend(
                validate_target(receipt, args.target_source, inline_source, args.bundle_root)
            )
    except (OSError, UnicodeError, TypeError, ValueError, yaml.YAMLError) as exc:
        errors = [str(exc)]
    if errors:
        print("REVIEW_RECEIPT_VALIDATION=fail")
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("REVIEW_RECEIPT_VALIDATION=pass")
    print(f"RECEIPT={args.receipt.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
