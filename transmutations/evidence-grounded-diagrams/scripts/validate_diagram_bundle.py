#!/usr/bin/env python3
"""Validate an evidence-grounded diagram bundle without overstating the checks."""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = SKILL_ROOT / "schemas"
MANIFEST_SCHEMA = SCHEMA_ROOT / "diagram-bundle-manifest.schema.yml"
MODEL_SCHEMA = SCHEMA_ROOT / "diagram-semantic-model.schema.yml"
REQUEST_SCHEMA = SCHEMA_ROOT / "diagram-request.schema.yml"
RECEIPT_SCHEMA = SCHEMA_ROOT / "diagram-validation-receipt.schema.yml"
ATTESTATION_SCHEMA = SCHEMA_ROOT / "diagram-manual-attestation.schema.yml"
VALIDATOR_NAME = "evidence-grounded-diagram-bundle-validator"
VALIDATOR_VERSION = "0.4.0"

CHECK_NAMES = (
    "schema_shape",
    "referential_integrity",
    "evidence_adequacy",
    "source_validation",
    "render_inspection",
    "semantic_reconciliation",
    "accessibility",
    "persistence",
)
MANUAL_CHECKS = (
    "evidence_adequacy",
    "source_validation",
    "render_inspection",
    "semantic_reconciliation",
    "accessibility",
)


class BundleError(ValueError):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise BundleError(f"missing file: {path}") from exc
    except yaml.YAMLError as exc:
        raise BundleError(f"invalid YAML: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise BundleError(f"top-level YAML must be an object: {path}")
    return value


def write_yaml(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        yaml.safe_dump(value, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def schema_errors(instance: dict[str, Any], schema_path: Path) -> list[str]:
    schema = load_yaml(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors: list[str] = []
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path)):
        locator = ".".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"{schema_path.name}:{locator}: {error.message}")
    return errors


def member_path(bundle: Path, relative: str) -> Path:
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise BundleError(f"member path must be relative and confined: {relative}")
    resolved = (bundle / candidate).resolve()
    try:
        resolved.relative_to(bundle.resolve())
    except ValueError as exc:
        raise BundleError(f"member escapes bundle: {relative}") from exc
    return resolved


def normalized_member_path(bundle: Path, relative: str) -> tuple[Path, str, str]:
    """Return the confined path, canonical relative spelling, and path identity."""
    resolved = member_path(bundle, relative)
    normalized_relative = resolved.relative_to(bundle.resolve()).as_posix()
    identity = os.path.normcase(str(resolved))
    return resolved, normalized_relative, identity


def duplicate_ids(items: list[dict[str, Any]], key: str) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in items:
        value = item.get(key)
        if not isinstance(value, str):
            continue
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def aggregate_status(model: dict[str, Any]) -> str:
    statuses = {
        claim.get("status")
        for claim in model.get("claims", [])
        if claim.get("included") is True and claim.get("load_bearing") is True
    }
    statuses.discard(None)
    if not statuses:
        return "not-applicable"
    if statuses == {"evidence-backed"}:
        return "evidence-backed"
    if statuses <= {"evidence-backed", "inferred"}:
        return "inferred"
    if statuses == {"hypothesis"}:
        return "hypothesis"
    if statuses == {"unknown"}:
        return "unknown"
    return "mixed"


def normalized_sources(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    normalized: dict[str, dict[str, Any]] = {}
    for source in items:
        value = dict(source)
        value["locators"] = sorted(
            (dict(locator) for locator in source.get("locators", [])),
            key=lambda item: str(item.get("locator_id")),
        )
        normalized[str(source.get("source_id"))] = value
    return normalized


def validate_request_binding(
    request: dict[str, Any],
    model: dict[str, Any],
    manifest: dict[str, Any],
    request_digest: str,
) -> list[str]:
    errors: list[str] = []
    evidence_set = request.get("evidence_set", {})
    expected = {
        "request_id": request.get("request_id"),
        "evidence_set_id": evidence_set.get("evidence_set_id"),
        "request_sha256": request_digest,
        "evidence_snapshot_digest": evidence_set.get("snapshot_digest"),
    }
    if manifest.get("request_binding") != expected:
        errors.append("manifest request_binding does not match persisted request bytes")
    if model.get("request_binding") != expected:
        errors.append("model request_binding does not match persisted request bytes")
    if request.get("reader_question") != model.get("reader_question"):
        errors.append("request reader_question differs from semantic model")
    if request.get("reader_question") != manifest.get("reader_question"):
        errors.append("request reader_question differs from manifest")
    revision = str(manifest.get("revision", ""))
    if revision == "r0001" and request.get("mode") != "create":
        errors.append("r0001 requires a create request")
    if revision != "r0001" and request.get("mode") != "revise":
        errors.append("r0002+ requires an authorized revise request")
    if request.get("mode") == "revise":
        target = request.get("target", {})
        supersedes = manifest.get("supersedes", {})
        if target.get("kind") != "bundle":
            errors.append("revise request target must be a bundle")
        if target.get("diagram_id") != manifest.get("diagram_id"):
            errors.append("revise target diagram_id differs from new revision")
        if target.get("revision") != supersedes.get("revision"):
            errors.append("revise target revision differs from supersedes")
        if target.get("manifest_digest") != supersedes.get("manifest_digest"):
            errors.append("revise target digest differs from supersedes")
    permitted = normalized_sources(evidence_set.get("sources", []))
    modeled = normalized_sources(model.get("sources", []))
    if modeled != permitted:
        errors.append("semantic model sources/locators differ from permitted evidence set")
    return errors


def validate_references(model: dict[str, Any], manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if model.get("diagram_id") != manifest.get("diagram_id"):
        errors.append("model diagram_id differs from manifest")
    if model.get("revision") != manifest.get("revision"):
        errors.append("model revision differs from manifest")

    for items, key, label in (
        (model.get("sources", []), "source_id", "source"),
        (model.get("claims", []), "claim_id", "claim"),
        (model.get("elements", []), "element_id", "element"),
        (model.get("encodings", []), "encoding_id", "encoding"),
    ):
        duplicates = duplicate_ids(items, key)
        if duplicates:
            errors.append(f"duplicate {label} IDs: {', '.join(sorted(duplicates))}")

    sources = {item["source_id"]: item for item in model.get("sources", [])}
    locator_pairs: set[tuple[str, str]] = set()
    for source_id, source in sources.items():
        locator_ids: set[str] = set()
        for locator in source.get("locators", []):
            locator_id = locator.get("locator_id")
            if locator_id in locator_ids:
                errors.append(f"duplicate locator ID in {source_id}: {locator_id}")
            locator_ids.add(locator_id)
            locator_pairs.add((source_id, locator_id))

    claims = {item["claim_id"]: item for item in model.get("claims", [])}
    elements = {item["element_id"]: item for item in model.get("elements", [])}
    represented_claims: set[str] = set()
    for claim_id, claim in claims.items():
        support = claim.get("support", [])
        for reference in support:
            pair = (reference.get("source_id"), reference.get("locator_id"))
            if pair not in locator_pairs:
                errors.append(f"{claim_id}: support does not resolve: {pair[0]}/{pair[1]}")
        if claim.get("status") == "evidence-backed" and not any(
            item.get("support_kind") == "direct" for item in support
        ):
            errors.append(f"{claim_id}: evidence-backed requires direct support")
        if claim.get("status") == "inferred":
            if not support:
                errors.append(f"{claim_id}: inferred claim requires cited support")
            qualification = str(claim.get("qualification", "")).strip().lower()
            if qualification in {"", "none", "n/a", "not applicable"}:
                errors.append(f"{claim_id}: inferred claim requires explicit synthesis")

    for element_id, element in elements.items():
        for claim_id in element.get("claim_ids", []):
            if claim_id not in claims:
                errors.append(f"{element_id}: unknown claim reference: {claim_id}")
            else:
                represented_claims.add(claim_id)

    for encoding in model.get("encodings", []):
        encoding_id = encoding.get("encoding_id", "<unknown>")
        for element_id in encoding.get("element_ids", []):
            if element_id not in elements:
                errors.append(f"{encoding_id}: unknown element reference: {element_id}")
        for claim_id in encoding.get("claim_ids", []):
            if claim_id not in claims:
                errors.append(f"{encoding_id}: unknown claim reference: {claim_id}")
            else:
                represented_claims.add(claim_id)

    covered = set(model.get("textual_equivalent_coverage", []))
    for claim_id in covered - set(claims):
        errors.append(f"textual equivalent covers unknown claim: {claim_id}")
    for claim_id, claim in claims.items():
        if claim.get("included") is True and claim.get("load_bearing") is True:
            if claim_id not in represented_claims:
                errors.append(f"{claim_id}: included load-bearing claim has no visual element")
            if claim_id not in covered:
                errors.append(f"{claim_id}: missing textual-equivalent coverage")

    computed = aggregate_status(model)
    if model.get("aggregate_status") != computed:
        errors.append(
            f"model aggregate_status is {model.get('aggregate_status')}; computed {computed}"
        )
    if manifest.get("aggregate_status") != computed:
        errors.append(
            f"manifest aggregate_status is {manifest.get('aggregate_status')}; computed {computed}"
        )
    tags = manifest.get("tags", {})
    if tags.get("epistemic") != computed:
        errors.append("tags.epistemic differs from computed aggregate status")
    if tags.get("lifecycle") != manifest.get("lifecycle_status"):
        errors.append("tags.lifecycle differs from lifecycle_status")
    completeness = model.get("scope", {}).get("completeness")
    if tags.get("scope") != completeness:
        errors.append("tags.scope differs from model scope completeness")
    return errors


def validate_lineage(bundle: Path, manifest: dict[str, Any]) -> list[str]:
    """Close revision lineage without mutating any earlier revision."""
    errors: list[str] = []
    revision = manifest.get("revision")
    supersedes = manifest.get("supersedes")
    if not isinstance(revision, str) or not revision.startswith("r"):
        return errors
    try:
        number = int(revision[1:])
    except ValueError:
        return errors
    if number == 1:
        if supersedes is not None:
            errors.append("r0001 must not declare supersedes")
        return errors
    if not isinstance(supersedes, dict):
        errors.append(f"{revision} requires supersedes lineage")
        return errors
    expected_revision = f"r{number - 1:04d}"
    prior_revision = supersedes.get("revision")
    if prior_revision != expected_revision:
        errors.append(
            f"{revision} must supersede immediate predecessor {expected_revision}"
        )
        return errors
    prior_manifest_path = bundle.parent / expected_revision / "diagram.meta.yml"
    if not prior_manifest_path.is_file():
        errors.append(f"superseded manifest does not exist: {prior_manifest_path}")
        return errors
    try:
        prior_manifest = load_yaml(prior_manifest_path)
    except BundleError as exc:
        errors.append(str(exc))
        return errors
    if prior_manifest.get("diagram_id") != manifest.get("diagram_id"):
        errors.append("superseded revision belongs to a different diagram_id")
    if prior_manifest.get("revision") != expected_revision:
        errors.append("superseded manifest revision does not match its path")
    expected_digest = supersedes.get("manifest_digest")
    actual_digest = sha256(prior_manifest_path)
    if expected_digest != actual_digest:
        errors.append("supersedes.manifest_digest does not match prior manifest bytes")
    return errors


def validate_members(bundle: Path, manifest: dict[str, Any]) -> tuple[list[str], dict[str, str]]:
    errors: list[str] = []
    observed: dict[str, str] = {}
    members = manifest.get("members", {})
    if not isinstance(members, dict):
        return ["manifest members must be an object"], observed

    member_names = (
        "request",
        "source",
        "render",
        "semantic_model",
        "textual_equivalent",
        "validation_receipt",
    )
    identities: dict[str, tuple[str, str]] = {}
    role_paths: dict[str, tuple[Path, str]] = {}
    for member_name in member_names:
        record = members.get(member_name)
        if record is None:
            continue
        if not isinstance(record, dict):
            errors.append(f"members.{member_name} must be an object")
            continue
        relative = record.get("path")
        if not isinstance(relative, str):
            errors.append(f"members.{member_name}.path is invalid")
            continue
        try:
            path, normalized_relative, identity = normalized_member_path(bundle, relative)
        except BundleError as exc:
            errors.append(str(exc))
            continue
        if relative.replace("\\", "/") != normalized_relative:
            errors.append(
                f"members.{member_name}.path must use normalized bundle-relative spelling: "
                f"{normalized_relative}"
            )
        prior = identities.get(identity)
        if prior is not None:
            errors.append(
                f"member path alias: roles {prior[0]} and {member_name} both resolve to "
                f"{normalized_relative}"
            )
        else:
            identities[identity] = (member_name, normalized_relative)
        role_paths[member_name] = (path, normalized_relative)

    for member_name in ("request", "source", "render", "semantic_model", "textual_equivalent"):
        record = members.get(member_name)
        if record is None or not isinstance(record, dict) or member_name not in role_paths:
            continue
        path, normalized_relative = role_paths[member_name]
        if not path.is_file():
            errors.append(f"missing bundle member for role {member_name}: {normalized_relative}")
            continue
        actual = sha256(path)
        observed[normalized_relative] = actual
        expected = record.get("sha256")
        if expected != actual:
            errors.append(f"digest mismatch for role {member_name}: {normalized_relative}")

    receipt_record = members.get("validation_receipt")
    if not isinstance(receipt_record, dict):
        errors.append("members.validation_receipt must be an object")
    elif "validation_receipt" in role_paths:
        receipt_path, receipt_relative = role_paths["validation_receipt"]
        if not receipt_path.is_file():
            errors.append(f"missing bundle member for role validation_receipt: {receipt_relative}")
    elif not isinstance(receipt_record.get("path"), str):
        errors.append("members.validation_receipt.path is invalid")

    text_record = members.get("textual_equivalent", {})
    text_relative = text_record.get("path")
    if isinstance(text_relative, str):
        try:
            if not member_path(bundle, text_relative).read_text(encoding="utf-8").strip():
                errors.append("textual equivalent is empty")
        except (BundleError, FileNotFoundError, UnicodeDecodeError) as exc:
            errors.append(f"cannot read textual equivalent: {exc}")
    return errors, observed


def validate_persistence(bundle: Path, manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    persistence = manifest.get("persistence", {})
    if persistence.get("state") != "saved":
        errors.append("persistence state is not saved")
    declared_bundle = persistence.get("bundle_path")
    if not isinstance(declared_bundle, str) or Path(declared_bundle).resolve() != bundle.resolve():
        errors.append("persistence.bundle_path does not identify this bundle")
    index_path = persistence.get("index_path")
    if not isinstance(index_path, str) or not Path(index_path).is_file():
        errors.append("persistence index does not exist")
        return errors
    try:
        index = load_yaml(Path(index_path))
    except BundleError as exc:
        errors.append(str(exc))
        return errors
    matching = [
        entry
        for entry in index.get("entries", [])
        if entry.get("diagram_id") == manifest.get("diagram_id")
        and entry.get("revision") == manifest.get("revision")
        and Path(str(entry.get("bundle_path", ""))).resolve() == bundle.resolve()
    ]
    if len(matching) != 1:
        errors.append("resolver index does not contain exactly one matching bundle entry")
    return errors


def validate_promotion_evidence(bundle: Path, manifest: dict[str, Any]) -> list[str]:
    """Verify recorded promotion provenance without treating it as trusted authority."""
    if manifest.get("promotion_status") != "promoted":
        return []
    errors: list[str] = []
    evidence = manifest.get("promotion_evidence")
    if not isinstance(evidence, dict):
        return ["promoted bundle requires structured promotion_evidence"]
    subject = evidence.get("subject", {})
    if not isinstance(subject, dict):
        errors.append("promotion_evidence.subject must be an object")
    else:
        if subject.get("diagram_id") != manifest.get("diagram_id"):
            errors.append("promotion evidence subject diagram_id differs from manifest")
        if subject.get("revision") != manifest.get("revision"):
            errors.append("promotion evidence subject revision differs from manifest")

    attestation = evidence.get("attestation", {})
    if not isinstance(attestation, dict):
        errors.append("promotion_evidence.attestation must be an object")
        return errors
    declared_path = attestation.get("path")
    expected_digest = attestation.get("sha256")
    if not isinstance(declared_path, str) or not declared_path:
        errors.append("promotion attestation path is invalid")
        return errors
    candidate = Path(declared_path)
    if not candidate.is_absolute():
        candidate = bundle / candidate
    try:
        resolved = candidate.resolve(strict=True)
    except (OSError, RuntimeError):
        errors.append(f"promotion attestation does not exist: {declared_path}")
        return errors
    if not resolved.is_file():
        errors.append(f"promotion attestation is not a regular file: {declared_path}")
        return errors
    try:
        actual_digest = sha256(resolved)
    except OSError as exc:
        errors.append(f"cannot read promotion attestation {declared_path}: {exc}")
        return errors
    if actual_digest != expected_digest:
        errors.append(f"promotion attestation digest mismatch: {declared_path}")
    return errors


def check(status: str, evidence: str, limitations: list[str] | None = None) -> dict[str, Any]:
    return {
        "status": status,
        "assessor": VALIDATOR_NAME,
        "evidence": evidence,
        "limitations": limitations or [],
    }


def reset_manual_check(name: str) -> dict[str, Any]:
    return check(
        "NOT_RUN",
        "",
        [f"{name} requires a source-aware or visual assessor for the current bytes."],
    )


def validate_manual_attestation(
    path: Path | None,
    manifest_digest: str,
    observed: dict[str, str],
    has_render: bool,
) -> tuple[list[str], dict[str, Any] | None, dict[str, Any] | None]:
    if path is None:
        return [], None, None
    try:
        attestation = load_yaml(path.resolve())
    except BundleError as exc:
        return [str(exc)], None, None
    errors = schema_errors(attestation, ATTESTATION_SCHEMA)
    records = attestation.get("observed_members", [])
    record_paths = [item.get("path") for item in records if isinstance(item, dict)]
    if len(record_paths) != len(records) or len(record_paths) != len(set(record_paths)):
        errors.append("manual attestation observed member paths must be unique")
    attested = {item.get("path"): item.get("sha256") for item in records}
    if attestation.get("observed_manifest_sha256") != manifest_digest:
        errors.append("manual attestation manifest digest is stale")
    if attested != observed:
        errors.append("manual attestation does not cover the exact current member set")
    assessor = attestation.get("assessor", {})
    record = {
        "path": str(path.resolve()),
        "sha256": sha256(path.resolve()),
        "assessor_identity": assessor.get("identity"),
        "provenance": assessor.get("provenance"),
    }
    checks: dict[str, Any] = {}
    for name in MANUAL_CHECKS:
        candidate = attestation.get("checks", {}).get(name, {})
        limitations = list(candidate.get("limitations", []))
        limitations.append(
            "Advisory assessment only: this package has no configured attestor trust anchor."
        )
        checks[name] = {
            "status": candidate.get("status"),
            "assessor": assessor.get("identity"),
            "evidence": candidate.get("evidence", ""),
            "limitations": limitations,
        }
    if not has_render and checks.get("render_inspection", {}).get("status") == "PASS":
        errors.append("manual attestation cannot PASS render_inspection without a render member")
    return errors, checks, record


def receipt_is_current(
    receipt: dict[str, Any], manifest_digest: str, observed: dict[str, str]
) -> bool:
    if receipt.get("observed_manifest_sha256") != manifest_digest:
        return False
    records = receipt.get("observed_members", [])
    if not isinstance(records, list):
        return False
    paths = [item.get("path") for item in records if isinstance(item, dict)]
    if len(paths) != len(records) or len(paths) != len(set(paths)):
        return False
    receipt_members = {item.get("path"): item.get("sha256") for item in records}
    return receipt_members == observed


def build_receipt(
    manifest: dict[str, Any],
    manifest_digest: str,
    observed: dict[str, str],
    schema_failures: list[str],
    reference_failures: list[str],
    persistence_failures: list[str],
    manual_checks: dict[str, Any] | None = None,
    attestation_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    checks: dict[str, Any] = {}
    checks["schema_shape"] = check(
        "FAIL" if schema_failures else "PASS",
        "; ".join(schema_failures) if schema_failures else "Manifest and semantic model match canonical schemas.",
    )
    checks["referential_integrity"] = check(
        "FAIL" if reference_failures else "PASS",
        "; ".join(reference_failures) if reference_failures else "IDs, references, aggregate status, and coverage close.",
    )
    checks["persistence"] = check(
        "FAIL" if persistence_failures else "PASS",
        "; ".join(persistence_failures) if persistence_failures else "Members, digests, bundle path, and resolver index close.",
    )
    for name in MANUAL_CHECKS:
        checks[name] = (
            manual_checks[name]
            if manual_checks is not None and name in manual_checks
            else reset_manual_check(name)
        )

    deterministic_failures = schema_failures + reference_failures + persistence_failures
    blockers = list(deterministic_failures)
    official_ready = (
        manifest.get("publication", {}).get("official") is True
        and manifest.get("publication", {}).get("readiness") == "ready"
    )
    if official_ready:
        for name in CHECK_NAMES:
            if checks[name]["status"] != "PASS":
                blockers.append(f"official readiness requires {name}: PASS")
        if attestation_record is not None:
            blockers.append(
                "official readiness requires an externally governed attestor trust anchor; "
                "package-local manual attestations are advisory"
            )
    if deterministic_failures:
        overall = "FAIL"
    elif blockers:
        overall = "BLOCKED"
    elif all(item["status"] == "PASS" for item in checks.values()) and attestation_record is None:
        overall = "PASS"
    else:
        overall = "DRAFT"

    return {
        "contract_version": "2.0.0",
        "diagram_id": manifest.get("diagram_id"),
        "revision": manifest.get("revision"),
        "validated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "validator": {"name": VALIDATOR_NAME, "version": VALIDATOR_VERSION},
        "observed_manifest_sha256": manifest_digest,
        "observed_members": [
            {"path": path, "sha256": digest} for path, digest in sorted(observed.items())
        ],
        "manual_attestation": attestation_record,
        "checks": checks,
        "overall": overall,
        "blockers": blockers,
    }


def validate_publication(manifest: dict[str, Any], receipt: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    lifecycle = manifest.get("lifecycle_status")
    publication = manifest.get("publication", {})
    official_ready = publication.get("official") is True and publication.get("readiness") == "ready"
    if official_ready or lifecycle == "published":
        if manifest.get("members", {}).get("render") is None:
            errors.append("published/official-ready bundle requires a render member")
        for name in CHECK_NAMES:
            if receipt.get("checks", {}).get(name, {}).get("status") != "PASS":
                errors.append(f"published/official-ready bundle requires {name}: PASS")
        if receipt.get("overall") != "PASS":
            errors.append("published/official-ready bundle requires overall receipt PASS")
    if lifecycle == "validated":
        for name in CHECK_NAMES:
            if receipt.get("checks", {}).get(name, {}).get("status") != "PASS":
                errors.append(f"validated bundle requires {name}: PASS")
        if receipt.get("overall") != "PASS":
            errors.append("validated bundle requires overall receipt PASS from a trusted validation path")
    return errors


def validate_receipt_consistency(
    manifest: dict[str, Any],
    receipt: dict[str, Any],
    computed: dict[str, Any],
) -> list[str]:
    """Reject a current-looking receipt whose verdict contradicts its checks."""
    errors: list[str] = []
    for field in ("diagram_id", "revision"):
        if receipt.get(field) != manifest.get(field):
            errors.append(f"validation receipt {field} does not match manifest")

    for name in ("schema_shape", "referential_integrity", "persistence"):
        actual = receipt.get("checks", {}).get(name, {}).get("status")
        expected = computed.get("checks", {}).get(name, {}).get("status")
        if actual != expected:
            errors.append(
                f"validation receipt {name} status is {actual!r}; current bytes require {expected!r}"
            )
    for name in MANUAL_CHECKS:
        actual = receipt.get("checks", {}).get(name, {}).get("status")
        expected = computed.get("checks", {}).get(name, {}).get("status")
        if actual != expected:
            errors.append(
                f"validation receipt {name} status is {actual!r}; trusted inputs require {expected!r}"
            )
    if receipt.get("manual_attestation") != computed.get("manual_attestation"):
        errors.append("validation receipt manual_attestation differs from trusted validation input")

    statuses = [
        receipt.get("checks", {}).get(name, {}).get("status") for name in CHECK_NAMES
    ]
    official_ready = (
        manifest.get("publication", {}).get("official") is True
        and manifest.get("publication", {}).get("readiness") == "ready"
    )
    if any(status == "FAIL" for status in statuses):
        expected_overall = "FAIL"
    elif official_ready and (
        any(status != "PASS" for status in statuses)
        or receipt.get("manual_attestation") is not None
    ):
        expected_overall = "BLOCKED"
    elif all(status == "PASS" for status in statuses) and receipt.get("manual_attestation") is None:
        expected_overall = "PASS"
    else:
        expected_overall = "DRAFT"
    if receipt.get("overall") != expected_overall:
        errors.append(
            f"validation receipt overall is {receipt.get('overall')!r}; checks require {expected_overall!r}"
        )
    if expected_overall in {"FAIL", "BLOCKED"} and not receipt.get("blockers"):
        errors.append(f"validation receipt overall {expected_overall} requires at least one blocker")
    if expected_overall == "PASS" and receipt.get("blockers"):
        errors.append("validation receipt overall PASS cannot retain blockers")
    return errors


def preflight(bundle: Path) -> list[str]:
    """Validate staged bytes before they can enter the resolver index."""
    bundle = bundle.resolve()
    manifest_path = bundle / "diagram.meta.yml"
    try:
        manifest = load_yaml(manifest_path)
        request_record = manifest.get("members", {}).get("request", {})
        request_path = member_path(bundle, request_record.get("path", "diagram.request.yml"))
        request = load_yaml(request_path)
        model_record = manifest.get("members", {}).get("semantic_model", {})
        model = load_yaml(member_path(bundle, model_record.get("path", "diagram.model.yml")))
    except (BundleError, OSError) as exc:
        return [str(exc)]
    member_errors, _ = validate_members(bundle, manifest)
    return (
        schema_errors(manifest, MANIFEST_SCHEMA)
        + schema_errors(request, REQUEST_SCHEMA)
        + schema_errors(model, MODEL_SCHEMA)
        + validate_request_binding(request, model, manifest, sha256(request_path))
        + validate_references(model, manifest)
        + validate_lineage(bundle, manifest)
        + member_errors
        + validate_promotion_evidence(bundle, manifest)
    )


def run(
    bundle: Path,
    write_receipt_flag: bool,
    manual_attestation_path: Path | None = None,
) -> tuple[list[str], dict[str, Any] | None]:
    bundle = bundle.resolve()
    manifest_path = bundle / "diagram.meta.yml"
    try:
        manifest = load_yaml(manifest_path)
    except BundleError as exc:
        return [str(exc)], None
    model_record = manifest.get("members", {}).get("semantic_model", {})
    request_record = manifest.get("members", {}).get("request", {})
    model_relative = model_record.get("path", "diagram.model.yml")
    request_relative = request_record.get("path", "diagram.request.yml")
    try:
        request_path = member_path(bundle, request_relative)
        request = load_yaml(request_path)
        model = load_yaml(member_path(bundle, model_relative))
    except BundleError as exc:
        return [str(exc)], None

    manifest_schema_errors = schema_errors(manifest, MANIFEST_SCHEMA)
    request_schema_errors = schema_errors(request, REQUEST_SCHEMA)
    model_schema_errors = schema_errors(model, MODEL_SCHEMA)
    shape_errors = manifest_schema_errors + request_schema_errors + model_schema_errors
    reference_errors = (
        validate_request_binding(request, model, manifest, sha256(request_path))
        + validate_references(model, manifest)
        + validate_lineage(bundle, manifest)
    )
    member_errors, observed = validate_members(bundle, manifest)
    persistence_errors = (
        validate_persistence(bundle, manifest)
        + validate_promotion_evidence(bundle, manifest)
    )
    persistence_group = member_errors + persistence_errors
    manifest_digest = sha256(manifest_path)
    attestation_errors, manual_checks, attestation_record = validate_manual_attestation(
        manual_attestation_path,
        manifest_digest,
        observed,
        isinstance(manifest.get("members", {}).get("render"), dict),
    )

    receipt_record = manifest.get("members", {}).get("validation_receipt", {})
    receipt_relative = receipt_record.get("path", "validation.receipt.yml")
    receipt_path = member_path(bundle, receipt_relative)
    old_receipt: dict[str, Any] | None = None
    if receipt_path.is_file():
        try:
            old_receipt = load_yaml(receipt_path)
        except BundleError:
            old_receipt = None

    computed_receipt = build_receipt(
        manifest,
        manifest_digest,
        observed,
        shape_errors,
        reference_errors,
        persistence_group + attestation_errors,
        manual_checks,
        attestation_record,
    )
    receipt = computed_receipt
    if write_receipt_flag:
        write_yaml(receipt_path, receipt)
    elif old_receipt is not None:
        receipt = old_receipt

    receipt_shape_errors = schema_errors(receipt, RECEIPT_SCHEMA)
    current_errors: list[str] = []
    if not receipt_is_current(receipt, manifest_digest, observed):
        current_errors.append("validation receipt is stale for current manifest/member bytes")
    consistency_errors = validate_receipt_consistency(manifest, receipt, computed_receipt)
    publication_errors = validate_publication(manifest, receipt)
    all_errors = (
        shape_errors
        + reference_errors
        + persistence_group
        + receipt_shape_errors
        + current_errors
        + consistency_errors
        + publication_errors
        + attestation_errors
    )
    return all_errors, receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--write-receipt", action="store_true")
    parser.add_argument(
        "--manual-attestation",
        type=Path,
        help="advisory external assessment bound to exact bytes; never a trust anchor",
    )
    parser.add_argument(
        "--preflight",
        action="store_true",
        help="validate staged shape, references, lineage, members, and digests before persistence",
    )
    args = parser.parse_args()
    if not args.bundle.is_dir():
        print(f"BUNDLE_VALIDATION=fail\nERROR: not a bundle directory: {args.bundle}")
        return 1
    if args.preflight:
        errors = preflight(args.bundle)
        if errors:
            print("BUNDLE_PREFLIGHT=fail")
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print("BUNDLE_PREFLIGHT=pass")
        print(f"BUNDLE={args.bundle.resolve()}")
        return 0
    try:
        errors, receipt = run(args.bundle, args.write_receipt, args.manual_attestation)
    except (BundleError, OSError) as exc:
        errors, receipt = [str(exc)], None
    if errors:
        print("BUNDLE_VALIDATION=fail")
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    overall = receipt.get("overall", "DRAFT") if receipt else "DRAFT"
    print(f"BUNDLE_VALIDATION={overall.lower()}")
    print(f"BUNDLE={args.bundle.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
