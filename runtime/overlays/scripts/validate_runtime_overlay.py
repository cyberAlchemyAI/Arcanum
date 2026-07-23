#!/usr/bin/env python3
"""Validate canonical-base plus declared additive runtime overlays."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any


SCHEMA_VERSION = "arcanum.runtime-overlay-manifest.v1"
TOP_LEVEL_FIELDS = {
    "schema_version",
    "target",
    "canonical",
    "generator",
    "payload_root",
    "runtime_targets",
    "allowed_metadata",
    "fragments",
    "presets",
    "protected_controls",
    "validation_command",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(text: str, label: str) -> tuple[dict[str, str], str]:
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        raise ValueError(f"{label}: missing generated frontmatter")
    end = normalized.find("\n---\n", 4)
    if end < 0:
        raise ValueError(f"{label}: unterminated generated frontmatter")
    fields: dict[str, str] = {}
    for line in normalized[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            raise ValueError(f"{label}: unsupported frontmatter line: {line}")
        fields[match.group(1)] = strip_quotes(match.group(2))
    return fields, normalized[end + 5 :]


def contained_path(
    repo_root: Path,
    raw_path: Any,
    label: str,
    errors: list[str],
    *,
    require_exists: bool = True,
) -> Path | None:
    if not isinstance(raw_path, str) or not raw_path.strip():
        errors.append(f"{label}: path must be a non-empty string")
        return None
    portable = raw_path.replace("\\", "/")
    candidate_parts = PurePosixPath(portable)
    if candidate_parts.is_absolute() or ".." in candidate_parts.parts:
        errors.append(f"{label}: path escapes repository: {raw_path}")
        return None
    if re.match(r"^[A-Za-z]:/", portable):
        errors.append(f"{label}: absolute drive path is forbidden: {raw_path}")
        return None

    repo_real = repo_root.resolve()
    candidate = repo_root.joinpath(*candidate_parts.parts)
    existing = candidate
    while not existing.exists() and existing != repo_root:
        existing = existing.parent
    try:
        existing_real = existing.resolve()
        existing_real.relative_to(repo_real)
    except (OSError, ValueError):
        errors.append(f"{label}: existing parent escapes repository: {raw_path}")
        return None

    if candidate.exists():
        try:
            candidate.resolve().relative_to(repo_real)
        except (OSError, ValueError):
            errors.append(f"{label}: resolved path escapes repository: {raw_path}")
            return None
    elif require_exists:
        errors.append(f"{label}: missing path: {raw_path}")
        return None
    return candidate


def require_object(
    value: Any,
    required: set[str],
    allowed: set[str],
    label: str,
    errors: list[str],
) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        errors.append(f"{label}: must be an object")
        return None
    missing = sorted(required - set(value))
    extra = sorted(set(value) - allowed)
    if missing:
        errors.append(f"{label}: missing fields: {', '.join(missing)}")
    if extra:
        errors.append(f"{label}: undeclared fields: {', '.join(extra)}")
    return value


def unique_ids(items: Any, label: str, errors: list[str]) -> set[str]:
    if not isinstance(items, list):
        errors.append(f"{label}: must be an array")
        return set()
    seen: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            errors.append(f"{label}[{index}]: missing string id")
            continue
        item_id = item["id"]
        if item_id in seen:
            errors.append(f"{label}: duplicate id {item_id}")
        seen.add(item_id)
    return seen


def apply_fragments(
    canonical_text: str,
    manifest: dict[str, Any],
    repo_root: Path,
    preset_ids: set[str],
    errors: list[str],
) -> tuple[str, list[dict[str, Any]]]:
    composed = canonical_text
    fragment_report: list[dict[str, Any]] = []
    fragments = manifest.get("fragments", [])
    unique_ids(fragments, "fragments", errors)
    if not isinstance(fragments, list):
        return composed, fragment_report

    for index, fragment in enumerate(fragments):
        label = f"fragments[{index}]"
        obj = require_object(
            fragment,
            {"id", "preset_ids", "source", "sha256", "mode", "anchor"},
            {"id", "preset_ids", "source", "sha256", "mode", "anchor"},
            label,
            errors,
        )
        if obj is None:
            continue
        if obj.get("mode") != "insert_after_exact":
            errors.append(f"{label}: only insert_after_exact is additive")
            continue
        linked_presets = obj.get("preset_ids")
        if not isinstance(linked_presets, list) or not linked_presets:
            errors.append(f"{label}: preset_ids must be a non-empty array")
            linked_presets = []
        for preset_id in linked_presets:
            if preset_id not in preset_ids:
                errors.append(f"{label}: undeclared preset id {preset_id}")

        source = contained_path(repo_root, obj.get("source"), f"{label}.source", errors)
        if source is None:
            continue
        payload_bytes = source.read_bytes()
        actual_digest = sha256_bytes(payload_bytes)
        if obj.get("sha256") != actual_digest:
            errors.append(f"{label}: fragment digest mismatch")
            continue
        anchor = obj.get("anchor")
        if not isinstance(anchor, str) or not anchor:
            errors.append(f"{label}: anchor must be non-empty")
            continue
        occurrences = composed.count(anchor)
        if occurrences != 1:
            errors.append(f"{label}: anchor occurrence count is {occurrences}, expected 1")
            continue
        payload = payload_bytes.decode("utf-8").rstrip("\n")
        composed = composed.replace(anchor, f"{anchor}\n{payload}", 1)
        fragment_report.append(
            {
                "id": obj.get("id"),
                "source": obj.get("source"),
                "sha256": actual_digest,
                "mode": obj.get("mode"),
            }
        )
    return composed, fragment_report


def validate_presets(
    manifest: dict[str, Any], repo_root: Path, errors: list[str]
) -> tuple[set[str], list[dict[str, Any]]]:
    presets = manifest.get("presets", [])
    preset_ids = unique_ids(presets, "presets", errors)
    copied_report: list[dict[str, Any]] = []
    if not isinstance(presets, list):
        return preset_ids, copied_report

    declared_source_dirs: set[str] = set()
    for index, preset in enumerate(presets):
        label = f"presets[{index}]"
        obj = require_object(
            preset,
            {"id", "source_dir", "copied_files"},
            {"id", "source_dir", "copied_files"},
            label,
            errors,
        )
        if obj is None:
            continue
        source_dir = contained_path(
            repo_root, obj.get("source_dir"), f"{label}.source_dir", errors
        )
        if source_dir is not None:
            if not source_dir.is_dir():
                errors.append(f"{label}.source_dir: must be a directory")
            declared_source_dirs.add(source_dir.name)
        copied_files = obj.get("copied_files")
        if not isinstance(copied_files, list) or not copied_files:
            errors.append(f"{label}.copied_files: must be a non-empty array")
            continue
        destinations: set[str] = set()
        for file_index, copied_file in enumerate(copied_files):
            file_label = f"{label}.copied_files[{file_index}]"
            file_obj = require_object(
                copied_file,
                {"source", "destination", "sha256"},
                {"source", "destination", "sha256"},
                file_label,
                errors,
            )
            if file_obj is None:
                continue
            source = contained_path(
                repo_root, file_obj.get("source"), f"{file_label}.source", errors
            )
            destination_raw = file_obj.get("destination")
            destination = PurePosixPath(
                destination_raw.replace("\\", "/")
                if isinstance(destination_raw, str)
                else ""
            )
            if (
                not isinstance(destination_raw, str)
                or destination.is_absolute()
                or ".." in destination.parts
                or not destination.parts
                or destination.parts[0] in {"SKILL.md", "README.md"}
            ):
                errors.append(f"{file_label}: unsafe package destination")
                continue
            destination_key = destination.as_posix()
            if destination_key in destinations:
                errors.append(f"{label}: duplicate destination {destination_key}")
            destinations.add(destination_key)
            if source is None:
                continue
            if source_dir is not None:
                try:
                    source.resolve().relative_to(source_dir.resolve())
                except ValueError:
                    errors.append(f"{file_label}: source is outside preset source_dir")
            actual_digest = sha256_bytes(source.read_bytes())
            if file_obj.get("sha256") != actual_digest:
                errors.append(f"{file_label}: payload digest mismatch")
            copied_report.append(
                {
                    "preset_id": obj.get("id"),
                    "source": file_obj.get("source"),
                    "destination": destination_key,
                    "sha256": actual_digest,
                }
            )

    payload_root = contained_path(
        repo_root, manifest.get("payload_root"), "payload_root", errors
    )
    if payload_root is not None and payload_root.is_dir():
        discovered = {path.name for path in payload_root.iterdir() if path.is_dir()}
        undeclared = sorted(discovered - declared_source_dirs)
        missing = sorted(declared_source_dirs - discovered)
        if undeclared:
            errors.append(f"payload_root: undeclared preset directories: {', '.join(undeclared)}")
        if missing:
            errors.append(f"payload_root: missing declared preset directories: {', '.join(missing)}")
    return preset_ids, copied_report


def validate_runtime_targets(
    manifest: dict[str, Any], repo_root: Path, errors: list[str]
) -> list[dict[str, Any]]:
    targets = manifest.get("runtime_targets", [])
    unique_ids(targets, "runtime_targets", errors)
    allowed_metadata = manifest.get("allowed_metadata")
    if (
        not isinstance(allowed_metadata, list)
        or not allowed_metadata
        or not all(isinstance(field, str) and field for field in allowed_metadata)
    ):
        errors.append("allowed_metadata: must be a non-empty string array")
        allowed_set: set[str] = set()
    else:
        allowed_set = set(allowed_metadata)
        if len(allowed_set) != len(allowed_metadata):
            errors.append("allowed_metadata: duplicate field")

    reports: list[dict[str, Any]] = []
    if not isinstance(targets, list) or not targets:
        errors.append("runtime_targets: must be a non-empty array")
        return reports
    for index, target in enumerate(targets):
        label = f"runtime_targets[{index}]"
        obj = require_object(
            target,
            {"id", "package_root", "skill_path", "metadata"},
            {"id", "package_root", "skill_path", "metadata"},
            label,
            errors,
        )
        if obj is None:
            continue
        package_root = contained_path(
            repo_root,
            obj.get("package_root"),
            f"{label}.package_root",
            errors,
            require_exists=False,
        )
        skill_path = contained_path(
            repo_root,
            obj.get("skill_path"),
            f"{label}.skill_path",
            errors,
            require_exists=False,
        )
        if package_root is not None and skill_path is not None:
            try:
                skill_path.relative_to(package_root)
            except ValueError:
                errors.append(f"{label}: skill_path is outside package_root")
        metadata = obj.get("metadata")
        if not isinstance(metadata, dict) or not metadata:
            errors.append(f"{label}.metadata: must be a non-empty object")
            metadata = {}
        unknown = sorted(set(metadata) - allowed_set)
        if unknown:
            errors.append(f"{label}.metadata: fields not allowed: {', '.join(unknown)}")
        if metadata.get("runtime") != obj.get("id"):
            errors.append(f"{label}.metadata.runtime: must equal target id")
        if any(not isinstance(value, str) for value in metadata.values()):
            errors.append(f"{label}.metadata: values must be strings")
        reports.append(
            {
                "id": obj.get("id"),
                "package_root": obj.get("package_root"),
                "skill_path": obj.get("skill_path"),
            }
        )
    return reports


def validate_generated(
    manifest: dict[str, Any],
    repo_root: Path,
    composed_text: str,
    copied_files: list[dict[str, Any]],
    errors: list[str],
) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    allowed_metadata = set(manifest.get("allowed_metadata", []))
    canonical_preset_root = repo_root / manifest["canonical"]["package_root"] / "presets"
    canonical_preset_dirs = (
        {path.name for path in canonical_preset_root.iterdir() if path.is_dir()}
        if canonical_preset_root.is_dir()
        else set()
    )
    declared_overlay_dirs = {
        PurePosixPath(item["destination"]).parts[1]
        for item in copied_files
        if len(PurePosixPath(item["destination"]).parts) >= 2
        and PurePosixPath(item["destination"]).parts[0] == "presets"
    }

    for index, target in enumerate(manifest.get("runtime_targets", [])):
        label = f"generated[{target.get('id', index)}]"
        skill_path = contained_path(
            repo_root, target.get("skill_path"), f"{label}.skill_path", errors
        )
        package_root = contained_path(
            repo_root, target.get("package_root"), f"{label}.package_root", errors
        )
        if skill_path is None or package_root is None:
            continue
        try:
            metadata, body = parse_frontmatter(skill_path.read_text("utf-8"), label)
        except (OSError, UnicodeDecodeError, ValueError) as error:
            errors.append(str(error))
            continue
        unknown = sorted(set(metadata) - allowed_metadata)
        if unknown:
            errors.append(f"{label}: undeclared generated metadata: {', '.join(unknown)}")
        for key, expected in target.get("metadata", {}).items():
            if metadata.get(key) != expected:
                errors.append(f"{label}: metadata mismatch for {key}")
        if normalize_text(body) != normalize_text(composed_text):
            errors.append(f"{label}: generated semantic body differs from admitted composition")
        for control in manifest.get("protected_controls", []):
            if normalize_text(control.get("text", "")) not in normalize_text(body):
                errors.append(
                    f"{label}: missing protected {control.get('class')} "
                    f"{control.get('id')}"
                )
        for copied_file in copied_files:
            destination = package_root / PurePosixPath(copied_file["destination"])
            if not destination.is_file():
                errors.append(
                    f"{label}: missing copied payload {copied_file['destination']}"
                )
            elif sha256_bytes(destination.read_bytes()) != copied_file["sha256"]:
                errors.append(
                    f"{label}: copied payload digest mismatch "
                    f"{copied_file['destination']}"
                )
        runtime_preset_root = package_root / "presets"
        if runtime_preset_root.is_dir():
            runtime_dirs = {
                path.name for path in runtime_preset_root.iterdir() if path.is_dir()
            }
            undeclared = sorted(
                runtime_dirs - canonical_preset_dirs - declared_overlay_dirs
            )
            if undeclared:
                errors.append(
                    f"{label}: undeclared generated preset directories: "
                    f"{', '.join(undeclared)}"
                )
        reports.append(
            {
                "id": target.get("id"),
                "skill_path": target.get("skill_path"),
                "body_sha256": sha256_bytes(normalize_text(body).encode("utf-8")),
            }
        )
    return reports


def validate_manifest(
    manifest_path: Path,
    repo_root: Path,
    target: str,
    *,
    check_generated: bool = False,
) -> dict[str, Any]:
    errors: list[str] = []
    try:
        manifest = json.loads(manifest_path.read_text("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        return {"status": "fail", "errors": [f"manifest: {error}"]}

    if not isinstance(manifest, dict):
        return {"status": "fail", "errors": ["manifest: root must be an object"]}
    missing = sorted(TOP_LEVEL_FIELDS - set(manifest))
    extra = sorted(set(manifest) - TOP_LEVEL_FIELDS)
    if missing:
        errors.append(f"manifest: missing fields: {', '.join(missing)}")
    if extra:
        errors.append(f"manifest: undeclared fields: {', '.join(extra)}")
    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"manifest: unsupported schema_version {manifest.get('schema_version')}")
    if manifest.get("target") != target:
        errors.append(
            f"manifest: target mismatch expected {target}, got {manifest.get('target')}"
        )

    canonical = require_object(
        manifest.get("canonical"),
        {"source", "sha256", "package_root"},
        {"source", "sha256", "package_root"},
        "canonical",
        errors,
    )
    canonical_text = ""
    if canonical is not None:
        canonical_path = contained_path(
            repo_root, canonical.get("source"), "canonical.source", errors
        )
        package_root = contained_path(
            repo_root, canonical.get("package_root"), "canonical.package_root", errors
        )
        if canonical_path is not None:
            canonical_bytes = canonical_path.read_bytes()
            if canonical.get("sha256") != sha256_bytes(canonical_bytes):
                errors.append("canonical: base digest mismatch")
            try:
                canonical_text = canonical_bytes.decode("utf-8")
            except UnicodeDecodeError:
                errors.append("canonical.source: must be UTF-8")
        if canonical_path is not None and package_root is not None:
            try:
                canonical_path.resolve().relative_to(package_root.resolve())
            except ValueError:
                errors.append("canonical.source: must be inside canonical.package_root")

    generator = require_object(
        manifest.get("generator"),
        {"path", "version", "version_marker", "overlay_protocol"},
        {"path", "version", "version_marker", "overlay_protocol"},
        "generator",
        errors,
    )
    if generator is not None:
        generator_path = contained_path(
            repo_root, generator.get("path"), "generator.path", errors
        )
        if generator.get("overlay_protocol") != SCHEMA_VERSION:
            errors.append("generator.overlay_protocol: schema mismatch")
        if not isinstance(generator.get("version"), str) or not generator.get("version"):
            errors.append("generator.version: must be non-empty")
        marker = generator.get("version_marker")
        if not isinstance(marker, str) or not marker:
            errors.append("generator.version_marker: must be non-empty")
        elif generator_path is not None and marker not in generator_path.read_text("utf-8"):
            errors.append("generator: version marker not found")

    runtime_report = validate_runtime_targets(manifest, repo_root, errors)
    preset_ids, copied_report = validate_presets(manifest, repo_root, errors)
    composed_text, fragment_report = apply_fragments(
        canonical_text, manifest, repo_root, preset_ids, errors
    )

    referenced_presets = {
        preset_id
        for fragment in manifest.get("fragments", [])
        if isinstance(fragment, dict)
        for preset_id in fragment.get("preset_ids", [])
        if isinstance(preset_id, str)
    }
    unreferenced = sorted(preset_ids - referenced_presets)
    if unreferenced:
        errors.append(f"presets: no declared fragment references: {', '.join(unreferenced)}")

    controls = manifest.get("protected_controls")
    unique_ids(controls, "protected_controls", errors)
    control_report: list[dict[str, str]] = []
    if not isinstance(controls, list) or not controls:
        errors.append("protected_controls: must be a non-empty array")
    else:
        for index, control in enumerate(controls):
            label = f"protected_controls[{index}]"
            obj = require_object(
                control,
                {"id", "class", "text"},
                {"id", "class", "text"},
                label,
                errors,
            )
            if obj is None:
                continue
            if obj.get("class") not in {"gate", "status", "authority", "state"}:
                errors.append(f"{label}: unsupported class {obj.get('class')}")
            protected_text = obj.get("text")
            if not isinstance(protected_text, str) or not protected_text:
                errors.append(f"{label}: text must be non-empty")
                continue
            if normalize_text(protected_text) not in normalize_text(canonical_text):
                errors.append(
                    f"canonical: missing protected {obj.get('class')} {obj.get('id')}"
                )
            if normalize_text(protected_text) not in normalize_text(composed_text):
                errors.append(
                    f"composition: removed protected {obj.get('class')} {obj.get('id')}"
                )
            control_report.append(
                {"id": obj.get("id"), "class": obj.get("class"), "status": "present"}
            )

    validation_command = manifest.get("validation_command")
    if (
        not isinstance(validation_command, str)
        or "validate_runtime_overlay.py" not in validation_command
        or str(manifest_path.relative_to(repo_root)) not in validation_command
    ):
        errors.append("validation_command: must name validator and this manifest")

    generated_report: list[dict[str, Any]] = []
    if check_generated:
        generated_report = validate_generated(
            manifest, repo_root, composed_text, copied_report, errors
        )

    return {
        "schema_version": "arcanum.runtime-overlay-validation.v1",
        "status": "pass" if not errors else "fail",
        "target": target,
        "manifest": str(manifest_path.relative_to(repo_root)),
        "canonical_sha256": (
            sha256_bytes(canonical_text.encode("utf-8")) if canonical_text else None
        ),
        "composed_semantic_sha256": (
            sha256_bytes(normalize_text(composed_text).encode("utf-8"))
            if composed_text
            else None
        ),
        "runtime_targets": runtime_report,
        "fragments": fragment_report,
        "copied_files": copied_report,
        "protected_controls": control_report,
        "generated_checked": check_generated,
        "generated": generated_report,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate an additive canonical-base runtime overlay manifest."
    )
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--target", required=True)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--check-generated", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    manifest_path = (
        args.manifest.resolve()
        if args.manifest.is_absolute()
        else (repo_root / args.manifest).resolve()
    )
    try:
        manifest_path.relative_to(repo_root)
    except ValueError:
        print("FAIL: manifest path escapes repository", file=sys.stderr)
        return 2

    report = validate_manifest(
        manifest_path,
        repo_root,
        args.target,
        check_generated=args.check_generated,
    )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    elif report["status"] == "pass":
        mode = "manifest+generated" if args.check_generated else "manifest"
        print(
            f"PASS runtime overlay {mode}: {report['target']} "
            f"({len(report['fragments'])} fragments, "
            f"{len(report['copied_files'])} copied files, "
            f"{len(report['protected_controls'])} protected controls)"
        )
    else:
        for error in report["errors"]:
            print(f"FAIL: {error}", file=sys.stderr)
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
