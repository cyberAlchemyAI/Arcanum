#!/usr/bin/env python3
"""Extract a deterministic Invoke Design concern denominator from exact inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Iterable

from jsonschema import Draft202012Validator


DETECTOR_ID = "invoke-design-scope-extractor"
DETECTOR_VERSION = "1.0.0"
DETECTOR_OWNER = "spellcraft"
VALIDATOR_OWNER = "invoke-design-selection-validator"

FIELD_CLASSES = (
    "human_actors",
    "rendered_surfaces",
    "interfaces",
    "stores",
    "queues",
    "writers",
    "normative_rules",
    "effects",
    "data_and_log_sinks",
    "deployment_targets",
    "compatibility_boundaries",
    "quality_claims",
    "acceptance_and_readiness_claims",
)

SIGNAL_CLASS = {
    "human_actors": "human-actor",
    "rendered_surfaces": "rendered-surface",
    "interfaces": "interface",
    "stores": "store",
    "queues": "queue",
    "writers": "writer",
    "normative_rules": "normative-rule",
    "effects": "effect",
    "data_and_log_sinks": "data-log-sink",
    "deployment_targets": "deployment",
    "compatibility_boundaries": "compatibility",
    "quality_claims": "quality-claim",
    "acceptance_and_readiness_claims": "acceptance-readiness-claim",
}

ID_FIELD = {
    "human_actors": "actor_id",
    "rendered_surfaces": "surface_id",
    "interfaces": "interface_id",
    "stores": "store_id",
    "queues": "queue_id",
    "writers": "writer_id",
    "normative_rules": "rule_id",
    "effects": "effect_id",
    "data_and_log_sinks": "sink_id",
    "deployment_targets": "deployment_id",
    "compatibility_boundaries": "boundary_id",
    "quality_claims": "claim_id",
    "acceptance_and_readiness_claims": "claim_id",
}


class ExtractionFailure(ValueError):
    def __init__(self, code: str, message: str, selector: str | None = None):
        super().__init__(message)
        self.code = code
        self.selector = selector

    def diagnostic(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": str(self),
            "selector": self.selector,
            "repair": {
                "MANIFEST_NOT_CLOSED": "close the manifest and recompute input_digest",
                "MISSING_DETECTOR_INPUT": "restore the missing readable selector",
                "SELF_ISSUED_RECEIPT": "use an author identity distinct from the detector",
                "UNBOUND_SIGNAL": "assign a supported manifest field class and stable id",
            }.get(self.code, "repair the declared input and rerun extraction"),
        }


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ExtractionFailure("MANIFEST_NOT_CLOSED", "manifest must be a JSON object")
    return value


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def manifest_digest(manifest: dict[str, Any]) -> str:
    material = {key: value for key, value in manifest.items() if key != "input_digest"}
    return canonical_digest(material)


def receipt_digest(receipt: dict[str, Any]) -> str:
    material = {key: value for key, value in receipt.items() if key != "receipt_digest"}
    return canonical_digest(material)


def normalized_relative_path(raw: str) -> str:
    normalized = raw.replace("\\", "/")
    path = PurePosixPath(normalized)
    if (
        not normalized
        or path.is_absolute()
        or PureWindowsPath(raw).is_absolute()
        or ".." in path.parts
        or str(path) in ("", ".")
    ):
        raise ExtractionFailure(
            "MISSING_DETECTOR_INPUT", f"selector escapes repository root: {raw}", raw
        )
    return str(path)


def digest_path(path: Path) -> str:
    if path.is_file():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    if path.is_dir():
        members = []
        for child in sorted(item for item in path.rglob("*") if item.is_file()):
            members.append(
                {
                    "path": str(child.relative_to(path)).replace("\\", "/"),
                    "sha256": hashlib.sha256(child.read_bytes()).hexdigest(),
                }
            )
        return canonical_digest(members)
    raise ExtractionFailure(
        "MISSING_DETECTOR_INPUT", f"selector is not a readable file or directory: {path}"
    )


def resolve_exact(
    repository_root: Path, raw_path: str, expected_digest: str
) -> tuple[str, str]:
    relative = normalized_relative_path(raw_path)
    root = repository_root.resolve()
    candidate = (root / relative).resolve(strict=False)
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise ExtractionFailure(
            "MISSING_DETECTOR_INPUT",
            f"selector resolves outside repository root: {raw_path}",
            raw_path,
        ) from error
    if not candidate.exists():
        raise ExtractionFailure(
            "MISSING_DETECTOR_INPUT", f"missing selector: {raw_path}", raw_path
        )
    actual = digest_path(candidate)
    if actual != expected_digest:
        raise ExtractionFailure(
            "MISSING_DETECTOR_INPUT",
            f"selector digest mismatch: {raw_path}",
            raw_path,
        )
    return relative, actual


def unique_bindings(
    bindings: Iterable[dict[str, Any]], path_key: str, label: str
) -> list[dict[str, Any]]:
    seen: set[str] = set()
    ordered = []
    for binding in bindings:
        normalized = normalized_relative_path(binding[path_key])
        if normalized in seen:
            raise ExtractionFailure(
                "MANIFEST_NOT_CLOSED",
                f"duplicate normalized {label}: {normalized}",
                normalized,
            )
        seen.add(normalized)
        ordered.append(binding)
    return ordered


def schema_failures(manifest: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    return [
        f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(manifest),
            key=lambda item: list(item.path),
        )
    ]


def extract_denominator(
    manifest: dict[str, Any],
    repository_root: Path,
    manifest_schema: dict[str, Any],
    authored_concern_ids: list[str] | None = None,
) -> dict[str, Any]:
    if manifest.get("authored_by") == DETECTOR_ID:
        raise ExtractionFailure(
            "SELF_ISSUED_RECEIPT", "manifest author equals denominator detector"
        )
    errors = schema_failures(manifest, manifest_schema)
    if errors:
        missing = any(
            f"'{field}' is a required property" in message
            for field in FIELD_CLASSES
            for message in errors
        )
        code = "MISSING_DETECTOR_INPUT" if missing else "MANIFEST_NOT_CLOSED"
        raise ExtractionFailure(code, "; ".join(errors))

    actual_manifest_digest = manifest_digest(manifest)
    if actual_manifest_digest != manifest["input_digest"]:
        raise ExtractionFailure(
            "MANIFEST_NOT_CLOSED", "manifest input_digest does not match canonical input"
        )

    inspected: dict[str, dict[str, Any]] = {}

    def inspect(path: str, digest: str) -> None:
        relative, actual = resolve_exact(repository_root, path, digest)
        previous = inspected.get(relative)
        if previous is not None and previous["source_digest"] != actual:
            raise ExtractionFailure(
                "MANIFEST_NOT_CLOSED",
                f"selector has conflicting digests: {relative}",
                relative,
            )
        inspected[relative] = {
            "selector": relative,
            "path": relative,
            "source_digest": actual,
        }

    footprint = manifest["target_footprint"]
    for binding in unique_bindings(footprint["roots"], "path", "root"):
        inspect(binding["path"], binding["digest"])
    for binding in unique_bindings(
        footprint["inclusions"], "path", "inclusion"
    ):
        inspect(binding["path"], binding["digest"])
    unique_bindings(
        [{"path": item["selector"]} for item in footprint["exclusions"]],
        "path",
        "exclusion",
    )
    for binding in unique_bindings(manifest["source_contracts"], "path", "source"):
        inspect(binding["path"], binding["digest"])

    signals: list[dict[str, Any]] = []
    signal_ids: set[str] = set()
    for field in FIELD_CLASSES:
        if field not in manifest:
            raise ExtractionFailure(
                "MISSING_DETECTOR_INPUT", f"manifest field class missing: {field}", field
            )
        for item in manifest[field]:
            item_id = item.get(ID_FIELD[field])
            if not isinstance(item_id, str) or not item_id:
                raise ExtractionFailure(
                    "UNBOUND_SIGNAL", f"stable id missing for {field}", field
                )
            signal_id = f"signal:{SIGNAL_CLASS[field]}:{item_id}"
            if signal_id in signal_ids:
                raise ExtractionFailure(
                    "UNBOUND_SIGNAL", f"duplicate signal id: {signal_id}", item_id
                )
            signal_ids.add(signal_id)
            inspect(item["source_selector"], item["source_digest"])
            attributes = {
                key: value
                for key, value in item.items()
                if key
                not in {
                    ID_FIELD[field],
                    "source_selector",
                    "source_digest",
                }
            }
            signals.append(
                {
                    "signal_id": signal_id,
                    "signal_class": SIGNAL_CLASS[field],
                    "source_selector": normalized_relative_path(item["source_selector"]),
                    "source_digest": item["source_digest"],
                    "attributes": attributes,
                }
            )

    concerns = sorted(set(authored_concern_ids or []))
    signals.sort(key=lambda item: item["signal_id"])
    denominator_ids = sorted(set(concerns) | signal_ids)
    receipt: dict[str, Any] = {
        "schema_version": "1.0.0",
        "manifest_id": manifest["manifest_id"],
        "manifest_input_digest": manifest["input_digest"],
        "manifest_authored_by": manifest["authored_by"],
        "detector_id": DETECTOR_ID,
        "detector_version": DETECTOR_VERSION,
        "detector_owner": DETECTOR_OWNER,
        "inspected_selectors": sorted(
            inspected.values(), key=lambda item: item["selector"]
        ),
        "extracted_signals": signals,
        "authored_concern_ids": concerns,
        "denominator_signal_ids": denominator_ids,
        "unbound_signal_ids": [],
        "missing_detector_inputs": [],
        "verdict": "pass",
        "diagnostics": [],
        "receipt_digest": "0" * 64,
        "validator_owner": VALIDATOR_OWNER,
    }
    receipt["receipt_digest"] = receipt_digest(receipt)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    parser.add_argument("--repository-root", required=True)
    parser.add_argument("--manifest-schema")
    parser.add_argument("--authored-concern-id", action="append", default=[])
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    schema_path = (
        Path(args.manifest_schema)
        if args.manifest_schema
        else script_dir.parent / "schemas/design-scope-manifest.schema.json"
    )
    try:
        result = extract_denominator(
            load_json(Path(args.manifest)),
            Path(args.repository_root),
            load_json(schema_path),
            args.authored_concern_id,
        )
        status = 0
    except ExtractionFailure as error:
        result = {"verdict": "block", "diagnostics": [error.diagnostic()]}
        status = 1
    Path(args.output).write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return status


if __name__ == "__main__":
    raise SystemExit(main())
