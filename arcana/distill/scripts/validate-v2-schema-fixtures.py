#!/usr/bin/env python3
"""Validate Distill v2 schema fixture manifests without lifecycle sidecars."""
from __future__ import annotations

import argparse
import copy
from datetime import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any

from jsonschema import Draft202012Validator, RefResolver


COMMON_ID = "https://arcanum.dev/schemas/distill/common/2-0-0"
TECHNIQUE_ID = "https://arcanum.dev/schemas/distill/technique-spec/2-0-0"
COMMON_PATH = Path("arcana/distill/schemas/distill-common-v2.schema.json")
TECHNIQUE_PATH = Path("arcana/distill/schemas/distill-technique-spec-v2.schema.json")
CANONICAL_PATH = Path("arcana/distill/profiles/v2/techniques/abstraction_level_guard.json")
DEFAULT_MANIFEST = Path(
    "arcana/distill/development/fixtures/v2/schema/technique-spec/cases.json"
)

COMMON_DEFINITIONS = {
    "authority_effect_none",
    "bounded_count",
    "canonical_identifier",
    "exact_artifact_reference",
    "json_scalar",
    "non_negative_integer",
    "non_empty_string",
    "positive_integer",
    "repository_relative_path",
    "sha256",
    "state_field_reference",
    "structured_value_level_1",
    "structured_value_level_2",
    "unique_canonical_identifier_array",
    "unique_non_empty_string_array",
    "utc_timestamp",
}

COMMON_REF_EDGES = {
    "technique_id": f"{COMMON_ID}#/$defs/canonical_identifier",
    "display_name": f"{COMMON_ID}#/$defs/non_empty_string",
    "phases": f"{COMMON_ID}#/$defs/unique_non_empty_string_array",
    "hooks": f"{COMMON_ID}#/$defs/unique_non_empty_string_array",
    "allowed_inputs": f"{COMMON_ID}#/$defs/unique_non_empty_string_array",
    "emits": f"{COMMON_ID}#/$defs/unique_non_empty_string_array",
    "pass_condition": f"{COMMON_ID}#/$defs/non_empty_string",
    "flag_condition": f"{COMMON_ID}#/$defs/non_empty_string",
    "block_condition": f"{COMMON_ID}#/$defs/non_empty_string",
}

REF_EDGE_BLOCKERS = {
    "technique_id": "E_COMMON_REF_EDGE_TECHNIQUE_ID",
    "display_name": "E_COMMON_REF_EDGE_DISPLAY_NAME",
    "phases": "E_COMMON_REF_EDGE_PHASES",
    "hooks": "E_COMMON_REF_EDGE_HOOKS",
    "allowed_inputs": "E_COMMON_REF_EDGE_ALLOWED_INPUTS",
    "emits": "E_COMMON_REF_EDGE_EMITS",
    "pass_condition": "E_COMMON_REF_EDGE_PASS_CONDITION",
    "flag_condition": "E_COMMON_REF_EDGE_FLAG_CONDITION",
    "block_condition": "E_COMMON_REF_EDGE_BLOCK_CONDITION",
}

REF_EDGE_MUTATIONS = {
    "MUT-REF-EDGE-TECHNIQUE-ID-001": "technique_id",
    "MUT-REF-EDGE-DISPLAY-NAME-001": "display_name",
    "MUT-REF-EDGE-PHASES-001": "phases",
    "MUT-REF-EDGE-HOOKS-001": "hooks",
    "MUT-REF-EDGE-ALLOWED-INPUTS-001": "allowed_inputs",
    "MUT-REF-EDGE-EMITS-001": "emits",
    "MUT-REF-EDGE-PASS-CONDITION-001": "pass_condition",
    "MUT-REF-EDGE-FLAG-CONDITION-001": "flag_condition",
    "MUT-REF-EDGE-BLOCK-CONDITION-001": "block_condition",
}

PHASE_ORDER = [
    "setup",
    "concept_mapping",
    "proposal",
    "balance",
    "closure",
    "pitch_off",
    "final_synthesis",
    "handoff",
]

HOOK_ORDER = [
    "after_intent_confirmation",
    "before_layer_split",
    "after_proposer_pass",
    "after_balancer_pass",
    "before_accept_split",
    "before_pitch_off",
    "before_verdict",
    "after_verdict",
]

UTC_TIMESTAMP_RE = re.compile(
    r"[0-9]{4}-(0[1-9]|1[0-2])-([0-2][0-9]|3[0-1])"
    r"T([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]Z"
)
CANONICAL_IDENTIFIER_RE = re.compile(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*")
STATE_FIELD_RE = re.compile(
    r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*(?:\.[a-z][a-z0-9]*(?:_[a-z0-9]+)*)+"
)

OBJECTION_CATEGORIES = {
    "lost_recomposition",
    "missing_input_or_output",
    "wrong_abstraction_level",
    "unconfirmed_evolution_profile",
    "excessive_cognitive_load",
    "external_variety_not_handled",
    "internal_complexity_greater_than_needed",
    "stakeholder_boundary_ambiguity",
    "concept_claim_treated_as_knowledge",
    "validation_burden",
    "hidden_glue",
    "premature_complexity",
    "brittle_minimalism",
}

PERSISTED_IDS = {
    "valid-abstraction-level-guard",
    "invalid-hyphen-id",
    "invalid-forbidden-hook",
    "invalid-missing-emits",
    "invalid-unknown-field",
}

POSITIVE_IDS = {
    "POS-CANONICAL-IDENTIFIER-001",
    "POS-NON-EMPTY-STRING-001",
    "POS-UNIQUE-ARRAY-001",
    "POS-SHA256-001",
    "POS-REPOSITORY-PATH-001",
    "POS-EXACT-REF-001",
    "POS-POSITIVE-INTEGER-001",
    "POS-BOUNDED-COUNT-001",
    "POS-AUTHORITY-EFFECT-001",
    "POS-UTC-TIMESTAMP-001",
}

MUTATION_IDS = {
    "MUT-COMMON-SEMANTIC-DEF-001",
    "MUT-TECH-DUPLICATE-HOOK-001",
    "MUT-REF-ABSOLUTE-001",
    "MUT-REF-TRAVERSAL-001",
    "MUT-REF-URI-001",
    "MUT-REF-NUL-001",
    "MUT-REF-EMPTY-SEGMENT-001",
    "MUT-REF-DOT-SEGMENT-001",
    "MUT-TECH-TYPE-001",
    "MUT-TECH-PHASE-001",
    "MUT-TECH-ACTIVATION-001",
    "MUT-TECH-FAILURE-001",
    "MUT-ID-TRAILING-LF-001",
    "MUT-ID-UPPERCASE-001",
    "MUT-ID-LEADING-UNDERSCORE-001",
    "MUT-STRING-EMPTY-001",
    "MUT-ARRAY-EMPTY-001",
    "MUT-ARRAY-EMPTY-ITEM-001",
    "MUT-SHA256-UPPERCASE-001",
    "MUT-SHA256-SHORT-001",
    "MUT-REF-MISSING-SIZE-001",
    "MUT-REF-SIZE-TYPE-001",
    "MUT-POSITIVE-ZERO-001",
    "MUT-POSITIVE-NEGATIVE-001",
    "MUT-BOUNDED-MISSING-MAX-001",
    "MUT-BOUNDED-MIN-OVER-DEFAULT-001",
    "MUT-BOUNDED-DEFAULT-OVER-MAX-001",
    "MUT-AUTHORITY-EFFECT-001",
    "MUT-TIMESTAMP-OFFSET-001",
    "MUT-TIMESTAMP-FRACTION-001",
    "MUT-TIMESTAMP-CALENDAR-001",
    "MUT-TIMESTAMP-YEAR-ZERO-001",
    "MUT-TIMESTAMP-TRAILING-LF-001",
    "MUT-REF-EDGE-TECHNIQUE-ID-001",
    "MUT-REF-EDGE-DISPLAY-NAME-001",
    "MUT-REF-EDGE-PHASES-001",
    "MUT-PHASE-ORDER-001",
    "MUT-HOOK-ORDER-001",
    "MUT-CONFUSION-PROSE-001",
    "MUT-EMITTED-CONSTRAINT-MISSING-001",
    "MUT-MANIFEST-ORACLE-001",
    "MUT-SCHEMA-VERSION-001",
    "MUT-SCHEMA-ID-001",
    "MUT-REF-EDGE-HOOKS-001",
    "MUT-REF-EDGE-ALLOWED-INPUTS-001",
    "MUT-REF-EDGE-EMITS-001",
    "MUT-REF-EDGE-PASS-CONDITION-001",
    "MUT-REF-EDGE-FLAG-CONDITION-001",
    "MUT-REF-EDGE-BLOCK-CONDITION-001",
}


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def repository_path_blocker(value: Any) -> str | None:
    if not isinstance(value, str) or not value:
        return "E_PATH_EMPTY_SEGMENT"
    if value.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:[/\\]", value):
        return "E_PATH_ABSOLUTE"
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", value):
        return "E_PATH_URI"
    if "\x00" in value:
        return "E_PATH_NUL"
    parts = value.split("/")
    if "" in parts:
        return "E_PATH_EMPTY_SEGMENT"
    if ".." in parts:
        return "E_PATH_TRAVERSAL"
    if "." in parts:
        return "E_PATH_DOT_SEGMENT"
    if PurePosixPath(value).is_absolute():
        return "E_PATH_ABSOLUTE"
    return None


def bounded_count_blocker(value: Any) -> str | None:
    if not isinstance(value, dict):
        return None
    if not all(isinstance(value.get(key), int) for key in ("minimum", "default", "maximum")):
        return None
    if not value["minimum"] <= value["default"] <= value["maximum"]:
        return "E_BOUNDED_COUNT_ORDER"
    return None


def utc_calendar_blocker(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except (TypeError, ValueError):
        return "E_UTC_TIMESTAMP_CALENDAR"
    return None


def utc_timestamp_blocker(value: Any) -> str | None:
    if not isinstance(value, str) or UTC_TIMESTAMP_RE.fullmatch(value) is None:
        return "E_UTC_TIMESTAMP_PATTERN"
    return utc_calendar_blocker(value)


def store_for(common: dict[str, Any], technique: dict[str, Any]) -> dict[str, Any]:
    return {COMMON_ID: common, TECHNIQUE_ID: technique}


def errors_for(
    instance: Any,
    schema: dict[str, Any],
    store: dict[str, Any],
) -> list[Any]:
    resolver = RefResolver.from_schema(schema, store=store)
    validator = Draft202012Validator(schema, resolver=resolver)
    return sorted(
        validator.iter_errors(instance),
        key=lambda error: (
            tuple(str(part) for part in error.absolute_path),
            tuple(str(part) for part in error.absolute_schema_path),
            str(error.validator),
        ),
    )


def direct_definition_errors(
    name: str,
    value: Any,
    common: dict[str, Any],
    technique: dict[str, Any],
) -> list[Any]:
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$ref": f"{COMMON_ID}#/$defs/{name}",
    }
    return errors_for(value, schema, store_for(common, technique))


def classify_json_error(error: Any, context: str) -> str:
    path = tuple(str(part) for part in error.absolute_path)
    validator = str(error.validator)

    if context == "technique":
        first = path[0] if path else ""
        if validator == "pattern" and first == "technique_id":
            return "E_TECHNIQUE_ID_PATTERN"
        if validator == "enum" and first == "type":
            return "E_TECHNIQUE_TYPE_UNKNOWN"
        if validator == "enum" and first == "phases":
            return "E_PHASE_UNKNOWN"
        if validator == "enum" and first == "hooks":
            return "E_HOOK_UNKNOWN"
        if validator == "enum" and first == "activation":
            return "E_ACTIVATION_UNKNOWN"
        if validator == "enum" and first == "failure_behavior":
            return "E_FAILURE_BEHAVIOR_UNKNOWN"
        if validator == "uniqueItems":
            return "E_ARRAY_NOT_UNIQUE"
        if validator == "const" and first == "schema_version":
            return "E_SCHEMA_VERSION_CONST"
        if validator == "required" and "emits" not in error.instance:
            return "E_REQUIRED_PROPERTY_EMITS"
        if validator == "additionalProperties":
            return "E_UNKNOWN_PROPERTY"

    definition = context.removeprefix("definition:")
    if definition == "canonical_identifier" and validator == "pattern":
        return "E_CANONICAL_IDENTIFIER_PATTERN"
    if definition == "non_empty_string" and validator == "minLength":
        return "E_NON_EMPTY_STRING"
    if definition == "unique_non_empty_string_array":
        if validator == "minItems":
            return "E_ARRAY_EMPTY"
        if validator == "minLength":
            return "E_ARRAY_ITEM_EMPTY"
        if validator == "uniqueItems":
            return "E_ARRAY_NOT_UNIQUE"
    if definition == "sha256" and validator == "pattern":
        return "E_SHA256_PATTERN"
    if definition == "exact_artifact_reference":
        if validator == "required" and "size_bytes" not in error.instance:
            return "E_EXACT_REF_REQUIRED_SIZE"
        if validator == "type" and path == ("size_bytes",):
            return "E_EXACT_REF_SIZE_TYPE"
    if definition == "positive_integer" and validator == "minimum":
        return "E_POSITIVE_INTEGER_MINIMUM"
    if definition == "bounded_count" and validator == "required" and "maximum" not in error.instance:
        return "E_BOUNDED_COUNT_REQUIRED_MAXIMUM"
    if definition == "authority_effect_none" and validator == "const":
        return "E_AUTHORITY_EFFECT_NOT_NONE"
    if definition == "utc_timestamp" and validator == "pattern":
        return "E_UTC_TIMESTAMP_PATTERN"
    raise AssertionError(
        f"unclassified validation error: context={context}, validator={validator}, path={path}"
    )


def relative_order_ok(values: Any, canonical: list[str]) -> bool:
    if not isinstance(values, list) or any(value not in canonical for value in values):
        return False
    positions = [canonical.index(value) for value in values]
    return positions == sorted(positions)


def schema_policy_blocker(
    common: dict[str, Any],
    technique: dict[str, Any],
) -> str | None:
    if common.get("$id") != COMMON_ID or common.get("schema_version") != "distill.common.v2":
        return "E_SCHEMA_IDENTITY"
    if technique.get("$id") != TECHNIQUE_ID:
        return "E_SCHEMA_IDENTITY"
    if set(common.get("$defs", {})) != COMMON_DEFINITIONS:
        return "E_COMMON_SEMANTIC_COUPLING"
    for field, expected in COMMON_REF_EDGES.items():
        observed = technique.get("properties", {}).get(field, {}).get("$ref")
        if observed != expected:
            return REF_EDGE_BLOCKERS[field]
    return None


def canonical_policy_blocker(
    instance: dict[str, Any],
    canonical: dict[str, Any],
) -> str | None:
    if not relative_order_ok(instance.get("phases"), PHASE_ORDER):
        return "E_PHASE_ORDER"
    if not relative_order_ok(instance.get("hooks"), HOOK_ORDER):
        return "E_HOOK_ORDER"
    emits = instance.get("emits")
    constraints = instance.get("emitted_field_constraints")
    if not isinstance(emits, list) or not isinstance(constraints, dict) or set(emits) != set(constraints):
        return "E_EMITTED_FIELD_CONSTRAINT_MISSING"
    confusion = constraints.get("cross_level_confusion")
    if not isinstance(confusion, dict) or confusion.get("value_kind") != "boolean":
        return "E_CROSS_LEVEL_CONFUSION_TYPE"
    if instance.get("hooks") != canonical.get("hooks"):
        return "E_CANONICAL_HOOK_MISMATCH"
    return None


def validate_technique(
    instance: dict[str, Any],
    common: dict[str, Any],
    technique: dict[str, Any],
    canonical: dict[str, Any],
) -> list[str]:
    blockers = [
        classify_json_error(error, "technique")
        for error in errors_for(instance, technique, store_for(common, technique))
    ]
    policy = canonical_policy_blocker(instance, canonical)
    if policy is not None:
        blockers.append(policy)
    return list(dict.fromkeys(blockers))


def evaluate_positive(
    probe: dict[str, Any],
    common: dict[str, Any],
    technique: dict[str, Any],
) -> str | None:
    name = probe["definition"]
    value = probe["value"]
    errors = direct_definition_errors(name, value, common, technique)
    if errors:
        return classify_json_error(errors[0], f"definition:{name}")
    if name == "repository_relative_path":
        return repository_path_blocker(value)
    if name == "exact_artifact_reference":
        return repository_path_blocker(value["path"])
    if name == "bounded_count":
        return bounded_count_blocker(value)
    if name == "utc_timestamp":
        return utc_timestamp_blocker(value)
    return None


def inline_schema_for(field: str) -> dict[str, Any]:
    if field == "technique_id":
        return {"type": "string", "pattern": "^[a-z][a-z0-9]*(?:_[a-z0-9]+)*(?![\\s\\S])"}
    if field in {"display_name", "pass_condition", "flag_condition", "block_condition"}:
        return {"type": "string", "minLength": 1}
    return {
        "type": "array",
        "minItems": 1,
        "uniqueItems": True,
        "items": {"type": "string", "minLength": 1},
    }


def _definition_blocker(
    name: str,
    value: Any,
    common: dict[str, Any],
    technique: dict[str, Any],
) -> str | None:
    errors = direct_definition_errors(name, value, common, technique)
    if errors:
        return classify_json_error(errors[0], f"definition:{name}")
    if name == "bounded_count":
        return bounded_count_blocker(value)
    if name == "utc_timestamp":
        return utc_timestamp_blocker(value)
    return None


def evaluate_mutation(
    mutation_id: str,
    common: dict[str, Any],
    technique: dict[str, Any],
    canonical: dict[str, Any],
    manifest: dict[str, Any],
    fixture_dir: Path,
) -> tuple[str | None, dict[str, Any]]:
    if mutation_id == "MUT-COMMON-SEMANTIC-DEF-001":
        changed = copy.deepcopy(common)
        changed["$defs"]["verdict"] = {"enum": ["pass", "flag", "block"]}
        return schema_policy_blocker(changed, technique), {}

    if mutation_id == "MUT-SCHEMA-ID-001":
        changed = copy.deepcopy(technique)
        changed["$id"] = "https://example.invalid/technique"
        return schema_policy_blocker(common, changed), {}

    if mutation_id in REF_EDGE_MUTATIONS:
        field = REF_EDGE_MUTATIONS[mutation_id]
        changed = copy.deepcopy(technique)
        changed["properties"][field] = inline_schema_for(field)
        return schema_policy_blocker(common, changed), {}

    if mutation_id == "MUT-MANIFEST-ORACLE-001":
        invalid = read_json(fixture_dir / "invalid-hyphen-id.json")
        underlying = validate_technique(invalid, common, technique, canonical)[0]
        tampered_expected = "E_UNKNOWN_PROPERTY"
        blocker = None if underlying == tampered_expected else "E_EXPECTED_BLOCKER_MISMATCH"
        return blocker, {
            "underlying_observed_blocker": underlying,
            "tampered_expected_blocker": tampered_expected,
        }

    path_values = {
        "MUT-REF-ABSOLUTE-001": "/tmp/distill.json",
        "MUT-REF-TRAVERSAL-001": "../distill.json",
        "MUT-REF-URI-001": "https://example.invalid/distill.json",
        "MUT-REF-NUL-001": "arcana/\x00/distill.json",
        "MUT-REF-EMPTY-SEGMENT-001": "arcana//distill.json",
        "MUT-REF-DOT-SEGMENT-001": "arcana/./distill.json",
    }
    if mutation_id in path_values:
        return repository_path_blocker(path_values[mutation_id]), {}

    definition_values: dict[str, tuple[str, Any]] = {
        "MUT-ID-TRAILING-LF-001": ("canonical_identifier", "abstraction_level_guard\n"),
        "MUT-ID-UPPERCASE-001": ("canonical_identifier", "Abstraction_level_guard"),
        "MUT-ID-LEADING-UNDERSCORE-001": ("canonical_identifier", "_abstraction_level_guard"),
        "MUT-STRING-EMPTY-001": ("non_empty_string", ""),
        "MUT-ARRAY-EMPTY-001": ("unique_non_empty_string_array", []),
        "MUT-ARRAY-EMPTY-ITEM-001": ("unique_non_empty_string_array", ["a", ""]),
        "MUT-SHA256-UPPERCASE-001": ("sha256", "A" + "0" * 63),
        "MUT-SHA256-SHORT-001": ("sha256", "0" * 63),
        "MUT-REF-MISSING-SIZE-001": (
            "exact_artifact_reference",
            {"path": "arcana/a", "sha256": "0" * 64},
        ),
        "MUT-REF-SIZE-TYPE-001": (
            "exact_artifact_reference",
            {"path": "arcana/a", "sha256": "0" * 64, "size_bytes": "0"},
        ),
        "MUT-POSITIVE-ZERO-001": ("positive_integer", 0),
        "MUT-POSITIVE-NEGATIVE-001": ("positive_integer", -1),
        "MUT-BOUNDED-MISSING-MAX-001": ("bounded_count", {"minimum": 1, "default": 2}),
        "MUT-BOUNDED-MIN-OVER-DEFAULT-001": (
            "bounded_count",
            {"minimum": 3, "default": 2, "maximum": 4},
        ),
        "MUT-BOUNDED-DEFAULT-OVER-MAX-001": (
            "bounded_count",
            {"minimum": 1, "default": 4, "maximum": 3},
        ),
        "MUT-AUTHORITY-EFFECT-001": ("authority_effect_none", "implementation"),
        "MUT-TIMESTAMP-OFFSET-001": ("utc_timestamp", "2025-01-01T00:00:00+00:00"),
        "MUT-TIMESTAMP-FRACTION-001": ("utc_timestamp", "2025-01-01T00:00:00.000Z"),
        "MUT-TIMESTAMP-CALENDAR-001": ("utc_timestamp", "2025-02-29T00:00:00Z"),
        "MUT-TIMESTAMP-YEAR-ZERO-001": ("utc_timestamp", "0000-01-01T00:00:00Z"),
        "MUT-TIMESTAMP-TRAILING-LF-001": ("utc_timestamp", "2025-01-01T00:00:00Z\n"),
    }
    if mutation_id in definition_values:
        name, value = definition_values[mutation_id]
        return _definition_blocker(name, value, common, technique), {}

    changed = copy.deepcopy(canonical)
    if mutation_id == "MUT-TECH-DUPLICATE-HOOK-001":
        changed["hooks"].append("before_layer_split")
    elif mutation_id == "MUT-TECH-TYPE-001":
        changed["type"] = "mode mechanic"
    elif mutation_id == "MUT-TECH-PHASE-001":
        changed["phases"][0] = "concept mapping"
    elif mutation_id == "MUT-TECH-ACTIVATION-001":
        changed["activation"] = "mode-required"
    elif mutation_id == "MUT-TECH-FAILURE-001":
        changed["failure_behavior"] = "skip-with-reason"
    elif mutation_id == "MUT-PHASE-ORDER-001":
        changed["phases"].reverse()
    elif mutation_id == "MUT-HOOK-ORDER-001":
        changed["hooks"].reverse()
    elif mutation_id == "MUT-CONFUSION-PROSE-001":
        changed["emitted_field_constraints"]["cross_level_confusion"] = {
            "value_kind": "enum",
            "values": ["yes", "no"],
        }
    elif mutation_id == "MUT-EMITTED-CONSTRAINT-MISSING-001":
        del changed["emitted_field_constraints"]["unit_or_layer_id"]
    elif mutation_id == "MUT-SCHEMA-VERSION-001":
        changed["schema_version"] = "distill.technique_spec.v1"
    else:
        raise ValueError(f"unimplemented mutation {mutation_id}")

    blockers = validate_technique(changed, common, technique, canonical)
    return (blockers[0] if blockers else None), {}


def load_bundle(root: Path, manifest_path: Path) -> dict[str, Any]:
    resolved_manifest = manifest_path if manifest_path.is_absolute() else root / manifest_path
    fixture_dir = resolved_manifest.parent
    return {
        "common": read_json(root / COMMON_PATH),
        "technique": read_json(root / TECHNIQUE_PATH),
        "canonical": read_json(root / CANONICAL_PATH),
        "manifest": read_json(resolved_manifest),
        "fixture_dir": fixture_dir,
    }


def _id_set(records: Any) -> set[str]:
    if not isinstance(records, list):
        return set()
    return {record.get("id") for record in records if isinstance(record, dict) and isinstance(record.get("id"), str)}


def run_technique_manifest(root: Path, manifest_path: Path) -> dict[str, Any]:
    bundle = load_bundle(root, manifest_path)
    common = bundle["common"]
    technique = bundle["technique"]
    canonical = bundle["canonical"]
    manifest = bundle["manifest"]
    fixture_dir = bundle["fixture_dir"]

    blockers: list[str] = []
    results: list[dict[str, Any]] = []

    for schema in (common, technique):
        try:
            Draft202012Validator.check_schema(schema)
        except Exception:
            blockers.append("E_SCHEMA_META_INVALID")

    policy = schema_policy_blocker(common, technique)
    if policy is not None:
        blockers.append(policy)

    groups = {
        "persisted_cases": PERSISTED_IDS,
        "generated_positive_probes": POSITIVE_IDS,
        "generated_mutations": MUTATION_IDS,
    }
    for key, required_ids in groups.items():
        records = manifest.get(key)
        ids = _id_set(records)
        if ids != required_ids or not isinstance(records, list) or len(records) != len(required_ids):
            blockers.append("E_FIXTURE_ID_SET_MISMATCH")

    for case in manifest.get("persisted_cases", []):
        instance = read_json(fixture_dir / case["path"])
        observed_blockers = validate_technique(instance, common, technique, canonical)
        observed = "block" if observed_blockers else "pass"
        observed_blocker = observed_blockers[0] if observed_blockers else None
        expected_blocker = case.get("expected_blocker")
        success = observed == case["expected"] and observed_blocker == expected_blocker
        results.append({
            "id": case["id"],
            "kind": "persisted",
            "expected": case["expected"],
            "expected_blocker": expected_blocker,
            "observed": observed,
            "observed_blocker": observed_blocker,
            "success": success,
        })
        if not success:
            blockers.append("E_PERSISTED_CASE_MISMATCH")

    for probe in manifest.get("generated_positive_probes", []):
        observed_blocker = evaluate_positive(probe, common, technique)
        success = observed_blocker is None
        results.append({
            "id": probe["id"],
            "kind": "generated_positive",
            "expected": "pass",
            "observed": "pass" if success else "block",
            "observed_blocker": observed_blocker,
            "success": success,
        })
        if not success:
            blockers.append("E_GENERATED_POSITIVE_MISMATCH")

    for mutation in manifest.get("generated_mutations", []):
        observed_blocker, detail = evaluate_mutation(
            mutation["id"], common, technique, canonical, manifest, fixture_dir
        )
        success = observed_blocker == mutation["expected_blocker"]
        results.append({
            "id": mutation["id"],
            "kind": "generated_mutation",
            "expected": "block",
            "expected_blocker": mutation["expected_blocker"],
            "observed": "block" if observed_blocker else "pass",
            "observed_blocker": observed_blocker,
            "success": success,
            "detail": detail,
        })
        if not success:
            blockers.append("E_GENERATED_MUTATION_MISMATCH")

    blockers = list(dict.fromkeys(blockers))
    passed = sum(1 for result in results if result["success"])
    status = "pass" if not blockers and passed == 64 and len(results) == 64 else "block"
    return {
        "schema_version": "distill.technique_spec_fixture_validation.v2",
        "status": status,
        "passed": passed,
        "total": len(results),
        "counts": {
            "persisted": sum(result["kind"] == "persisted" for result in results),
            "generated_positive": sum(result["kind"] == "generated_positive" for result in results),
            "generated_mutation": sum(result["kind"] == "generated_mutation" for result in results),
        },
        "blockers": blockers,
        "results": results,
        "authority_effect": "none",
    }


GENERIC_GROUP_KINDS = (
    "canonical_positive",
    "generated_missing_required",
    "generated_unknown_field",
    "generated_wrong_type",
    "generated_invalid_enum_or_const",
    "generated_common_ref_edges",
    "generated_policy_mutations",
)

LEAF_CONTRACTS: dict[str, dict[str, Any]] = {
    "common": {
        "manifest_id": "distill.common.schema_fixtures.v2",
        "schema_path": "arcana/distill/schemas/distill-common-v2.schema.json",
        "schema_id": COMMON_ID,
        "expected_count": 27,
        "group_kinds": ("canonical_positive", "generated_policy_mutations"),
        "policy_ids": (
            "common-wrong-type", "common-identifier-pattern", "common-state-field-pattern",
            "common-array-empty", "common-canonical-array-pattern", "common-canonical-array-duplicate",
            "common-sha-pattern", "common-ref-missing-size", "common-positive-zero",
            "common-non-negative-negative",
            "common-bounded-missing-maximum", "common-bounded-order",
            "common-authority-const", "common-timestamp-pattern",
            "common-timestamp-calendar", "common-json-scalar-object",
            "common-structured-level-one-depth", "common-structured-level-two-depth",
            "common-path-absolute",
            "common-path-traversal", "common-path-uri", "common-path-nul",
            "common-path-empty-segment", "common-path-dot-segment",
            "common-semantic-coupling", "common-schema-identity",
        ),
        "policy_spec_digest": "ad5e1fee0303a29daec5c24f6909bd54189ab16e7609dbb072c7d010b09e8b99",
    },
    "mode_spec": {
        "manifest_id": "distill.mode_spec.schema_fixtures.v2",
        "schema_path": "arcana/distill/schemas/distill-mode-spec-v2.schema.json",
        "schema_id": "https://arcanum.dev/schemas/distill/mode-spec/2-0-0",
        "instance_schema_version": "distill.mode_spec.v2",
        "required": ("schema_version", "mode_id", "display_name", "tracks", "rounds_per_track", "role_program", "technique_policy", "skipped_reason_required", "pitch_off_policy", "human_gates", "cycle_policy", "closeout_policy"),
        "probe_surfaces": {"required": (67, "793979258133c095adaf0153c6712916b5c145350ee0289ba017811de71f6fcf"), "wrong_type": (56, "764fd160ad595c92479e28ae91b6fc95da8498836886e26c59827b80e1bba755"), "invalid_enum": (34, "02dc508ec1cac5424b6a530de8f4a54836a2f58cc9bfbf4c1376da771355a5f2")},
        "common_ref_count": 11,
        "common_ref_digest": "c7c7b8002b2ca0a7f605847e88e55291a01839e9d418ec62d4200904f0073748",
        "expected_count": 184,
        "policy_ids": (
            "mode-missing-track-maximum", "mode-unbounded-round-maximum",
            "mode-zero-track-maximum", "mode-budget-order", "mode-closure-owned",
            "mode-verdict-owner", "mode-role-program-order",
            "mode-role-program-missing-reconciliation", "mode-technique-policy-duplicate",
            "mode-pitch-prohibited-payload", "mode-pitch-conditional-missing-condition",
            "mode-periodic-gate-missing-interval", "mode-nonperiodic-gate-with-interval",
            "mode-human-gate-duplicate-id",
        ),
        "policy_spec_digest": "e0e6de36f046bd7f335ab6d9034f3050b323b82d0daa509eb328fcd8bf8b2c8d",
    },
    "technique_spec": {
        "manifest_id": "distill.technique_spec.schema_fixtures.v2",
        "schema_path": "arcana/distill/schemas/distill-technique-spec-v2.schema.json",
        "schema_id": TECHNIQUE_ID,
        "instance_schema_version": "distill.technique_spec.v2",
        "required": (
            "schema_version", "technique_id", "display_name", "type", "phases",
            "hooks", "activation", "allowed_inputs", "emits",
            "emitted_field_constraints", "failure_responses",
        ),
        "probe_surfaces": {"required": (44, "e05979cf0a5863e10e39f28e8add493153a733cbc8e91f20da1244b33b9d36fc"), "wrong_type": (48, "f6214278616526ea19b1ce1b5964b1b15063b6681d69022fa78367940721a52c"), "invalid_enum": (29, "03c3dd78d18c9d91dca31402d6a7bc25283a15aa58bcffebf2df35a63ecb1eb2")},
        "common_ref_count": 17,
        "common_ref_digest": "166e90fa35aeb8cb0722cad061f5d154a15b85e94d5808eafc9e7a813a606b36",
        "expected_count": 164,
        "policy_ids": (
            "technique-activation-always-with-predicates",
            "technique-activation-group-missing-predicates",
            "technique-activation-predicate-missing-id",
            "technique-activation-predicate-invalid-id",
            "technique-activation-predicate-duplicate-id",
            "technique-activation-undeclared-input",
            "technique-activation-recursive-predicate",
            "technique-emitted-constraint-missing",
            "technique-list-descriptor-unbounded",
            "technique-list-descriptor-order",
            "technique-scalar-descriptor-ref-type",
            "technique-scalar-descriptor-order",
            "technique-record-required-field-unknown",
            "technique-union-duplicate-tag",
            "technique-failure-response-order",
            "technique-failure-response-missing-actions",
            "technique-route-action-missing-target",
            "technique-non-route-action-with-target",
            "technique-phase-order", "technique-hook-order",
            "technique-forbidden-canonical-hook",
            "technique-legacy-activation-string",
            "technique-legacy-pass-condition",
            "technique-legacy-failure-behavior",
        ),
        "policy_spec_digest": "633d4cf6b61b60ee0eeb4d02c8bd360877d19c16a0183a3ded076e1ebddaa624",
    },
    "profile": {
        "manifest_id": "distill.profile.schema_fixtures.v2",
        "schema_path": "arcana/distill/schemas/distill-profile-v2.schema.json",
        "schema_id": "https://arcanum.dev/schemas/distill/profile/2-0-0",
        "instance_schema_version": "distill.profile.v2",
        "required": ("schema_version", "profile_id", "display_name", "mode_refs", "technique_refs", "objection_categories", "output_contract_version", "override_policy"),
        "probe_surfaces": {"required": (16, "753de1490554c6b05e3255830429676e71f36b9f364a7ad2e05512acd02f1113"), "wrong_type": (16, "bb4af2a4469e1b38a0d9cc8f362be5b833a7366e8ddd7ab0eb28a884b0f9b125"), "invalid_enum": (17, "83b70e21a989496c352284e3b77ad86eaa5f1cea2a87d2da5def5afd6c560600")},
        "common_ref_count": 5,
        "common_ref_digest": "b71778308f619d572c80cfbb5b3b02e7766e438bb95e5a3e7530b5e0c0028bc9",
        "expected_count": 60,
        "policy_ids": (
            "profile-embedded-mode-spec", "profile-embedded-technique-spec",
            "profile-unsafe-mode-ref", "profile-coarse-objection-category",
        ),
        "policy_spec_digest": "6d3ac979eabe50df7277381d463d9e0ea5e5f82c3f9bd1037ea19688548f3f3b",
    },
    "source": {
        "manifest_id": "distill.source.schema_fixtures.v2",
        "schema_path": "arcana/distill/schemas/distill-source-v2.schema.json",
        "schema_id": "https://arcanum.dev/schemas/distill/source/2-0-0",
        "instance_schema_version": "distill.source.v2",
        "required": ("schema_version", "identity", "intent", "policy", "discovery", "constraints", "artifacts", "lineage"),
        "probe_surfaces": {"required": (43, "a5b7f71cead86a805a41e41d1edc1ec27ae1334969a87569fa39c4789996e8d0"), "wrong_type": (52, "449af04da6313f71a66f3fc3ed27ef8beed515aa11e21b33df68071e42fafd3c"), "invalid_enum": (4, "873736d17d5435016285dfe2ee909a522e4ecd0e301f3e2df0d4b981c32742d6")},
        "common_ref_count": 24,
        "common_ref_digest": "d2ebe31d1a4aa48409211e70d216481235d5c47ff512e5f42c321c1870aad5cb",
        "expected_count": 132,
        "policy_ids": (
            "source-unsafe-artifact-path", "source-invalid-exact-ref",
            "source-revision-without-reason", "source-preauthored-verdict",
            "source-invoke-shaped", "source-artifacts-require-member",
            "source-requested-techniques-require-member",
        ),
        "policy_spec_digest": "41f297692054b5d7b5ce2896e1e33ee07e8817ee8bc5c01eb4cb867296b99112",
    },
    "trace_event": {
        "manifest_id": "distill.trace_event.schema_fixtures.v2",
        "schema_path": "arcana/distill/schemas/distill-trace-event-v2.schema.json",
        "schema_id": "https://arcanum.dev/schemas/distill/trace-event/2-0-0",
        "instance_schema_version": "distill.trace_event.v2",
        "required": ("schema_version", "event_id", "run_id", "sequence", "previous_event_sha256", "created_at", "event_type", "payload", "authority_effect"),
        "probe_surfaces": {"required": (43, "430b02e9f11bdbde83e564638cf8b35481fb714c0fe470958d23b514e497f410"), "wrong_type": (33, "ea521f064b58a47fc2e9ffa9c03e042c38a99980fe6adde2f35c7ca2da23014f"), "invalid_enum": (13, "a58be3bcd408a3f38bf448d0c07c32d6e69aa981eb003b394479988452650b19")},
        "common_ref_count": 39,
        "common_ref_digest": "6b4e7821db9d82090a0132562b967bcfdcf4f559baf6358fb89ee8320ca744f4",
        "expected_count": 144,
        "policy_ids": (
            "trace-authority-event", "trace-mutable-summary",
            "trace-sequence-zero-with-predecessor", "trace-sequence-one-without-predecessor",
            "trace-skipped-without-reason", "trace-activated-without-output",
            "trace-skipped-with-output", "trace-route-without-target",
            "trace-nonroute-with-target", "trace-invalid-state-field",
            "trace-untagged-emitted-value", "trace-not-applicable-activated",
            "trace-coarse-objection-category",
            "trace-duplicate-emitted-field",
        ),
        "policy_spec_digest": "63760fc08fb4bac14eef0b519ba641dd4fc5224e67ac352b02fcdd520e6323bb",
    },
    "result": {
        "manifest_id": "distill.result.schema_fixtures.v2",
        "schema_path": "arcana/distill/schemas/distill-result-v2.schema.json",
        "schema_id": "https://arcanum.dev/schemas/distill/result/2-0-0",
        "instance_schema_version": "distill.result.v2",
        "required": ("schema_version", "run_id", "source_ref", "target_context", "objective", "output_artifact", "mode_id", "mode_budget", "proposal_tracks", "recursive_rounds", "verdict", "role_conversation_trace", "selected_unit_id", "current_smallest_coherent_unit", "optimization_point", "concept_layer_map", "technique_pack_trace", "closure_and_recomposition_proof", "evolution_profile", "deferred_complexity", "tension_ledger", "readiness_effects", "premortem", "frame_expiry_note", "navigation_guide", "evidence_emission", "telemetry", "next_route", "authority_effect"),
        "probe_surfaces": {"required": (74, "a6b8c610d1407e34c084b4519f10906bde9a79c2ced0b7e4d02df257dfeec9a3"), "wrong_type": (72, "c2a87e82f186248f52f9143e3c373e7c2fe9d9c3635e60fbcaa835c28afafe98"), "invalid_enum": (14, "8a6db892221d3ea3f60bb79a36c8f714fde61913db4875176ce65ec9f928e40a")},
        "common_ref_count": 44,
        "common_ref_digest": "e9bac05d41a0843e115fc5acc9cc16313dc1a848872c903ee584240ab4e46db1",
        "expected_count": 219,
        "policy_ids": (
            "result-pass-without-selected-unit", "result-pass-with-blocker-tension",
            "result-flag-without-readiness-effects", "result-block-with-selected-unit",
            "result-block-implementation-route", "result-technique-event-link-missing",
            "result-technique-event-link-pattern", "result-technique-skipped-without-reason",
            "result-technique-activated-with-skip-reason",
            "result-technique-route-without-target",
            "result-technique-nonroute-with-target",
            "result-technique-not-applicable-activated",
            "result-authority-effect",
        ),
        "policy_spec_digest": "3d9cebeeec421e3ecef5ec0d4b3ccb4f4d679500aa4857d7d1e6b25cb9d40e0a",
    },
    "stage_receipt": {
        "manifest_id": "distill.stage_receipt.schema_fixtures.v2",
        "schema_path": "arcana/distill/schemas/distill-stage-receipt-v2.schema.json",
        "schema_id": "https://arcanum.dev/schemas/distill/stage-receipt/2-0-0",
        "instance_schema_version": "distill.stage_receipt.v2",
        "required": ("schema_version", "run_id", "created_at", "producer_id", "producer_sha256", "finalizer_id", "finalizer_sha256", "schema_inventory", "artifact_inventory", "validation_state", "publication", "receipt_digest", "receipt_digest_method", "authority_effect"),
        "probe_surfaces": {"required": (83, "7ad72886cfadbad8f673d901b78749c4a343706f4c0a59b6d2d9e08393c39e95"), "wrong_type": (79, "6abcc7a748ba1030628a1ec5ea56c424911003838e923a55e05f0b6feba5b5c8"), "invalid_enum": (20, "e3c00ea578bb47f195b60fcd7b236b632276cac3244bb2bbae2f7eee3cf28eb4")},
        "common_ref_count": 13,
        "common_ref_digest": "e31ac29f967c057d25a64f92119c7f3b6e0f690754a78a062616cfe88b607d48",
        "expected_count": 204,
        "policy_ids": ("receipt-incomplete-role-inventory", "receipt-incomplete-schema-inventory", "receipt-duplicate-schema-kind", "receipt-duplicate-role-inventory", "receipt-self-referential-role", "receipt-self-referential-digest-law", "receipt-non-atomic-publication"),
        "policy_spec_digest": "24081156a64e010afdec5cdaa73fd02d45f65de07416740874acbb2987d3dcf3",
    },
}

FAMILY_MEMBERS = (
    ("common", "arcana/distill/development/fixtures/v2/schema/common/cases.json", 27),
    ("mode_spec", "arcana/distill/development/fixtures/v2/schema/mode-spec/cases.json", 184),
    ("technique_spec", "arcana/distill/development/fixtures/v2/schema/technique-spec/cases.json", 164),
    ("profile", "arcana/distill/development/fixtures/v2/schema/profile/cases.json", 60),
    ("source", "arcana/distill/development/fixtures/v2/schema/source/cases.json", 132),
    ("trace_event", "arcana/distill/development/fixtures/v2/schema/trace-event/cases.json", 144),
    ("result", "arcana/distill/development/fixtures/v2/schema/result/cases.json", 219),
    ("stage_receipt", "arcana/distill/development/fixtures/v2/schema/stage-receipt/cases.json", 204),
)
FAMILY_TOTAL = 1134


def _escape_pointer(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def _pointer_parts(pointer: str) -> list[str]:
    if not pointer.startswith("/"):
        raise ValueError(f"invalid JSON pointer: {pointer}")
    return [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]


def _pointer_parent(document: Any, pointer: str) -> tuple[Any, str]:
    parts = _pointer_parts(pointer)
    if not parts:
        raise ValueError("root pointer is not mutable")
    current = document
    for part in parts[:-1]:
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current, parts[-1]


def _pointer_set(document: Any, pointer: str, value: Any) -> None:
    parent, key = _pointer_parent(document, pointer)
    if isinstance(parent, list):
        parent[int(key)] = copy.deepcopy(value)
    else:
        parent[key] = copy.deepcopy(value)


def _pointer_remove(document: Any, pointer: str) -> None:
    parent, key = _pointer_parent(document, pointer)
    if isinstance(parent, list):
        del parent[int(key)]
    else:
        del parent[key]


def _common_ref_entries(schema: Any) -> list[list[str]]:
    entries: list[list[str]] = []

    def walk(value: Any, pointer: str) -> None:
        if isinstance(value, dict):
            ref = value.get("$ref")
            if isinstance(ref, str) and ref.startswith(f"{COMMON_ID}#/"):
                entries.append([f"{pointer}/$ref", ref])
            for key, child in value.items():
                walk(child, f"{pointer}/{_escape_pointer(key)}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f"{pointer}/{index}")

    walk(schema, "")
    return entries


def _canonical_digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _schema_paths() -> tuple[Path, ...]:
    return tuple(Path(contract["schema_path"]) for contract in LEAF_CONTRACTS.values()) + (TECHNIQUE_PATH,)


def _schema_store(root: Path) -> dict[str, Any]:
    schemas = [read_json(root / path) for path in _schema_paths()]
    return {schema["$id"]: schema for schema in schemas}


def _generic_errors(instance: Any, schema: dict[str, Any], store: dict[str, Any]) -> list[Any]:
    resolver = RefResolver.from_schema(schema, store=store)
    validator = Draft202012Validator(schema, resolver=resolver)
    return list(validator.iter_errors(instance))


def _error_tree(errors: list[Any]) -> list[Any]:
    flattened: list[Any] = []
    pending = list(errors)
    while pending:
        error = pending.pop(0)
        flattened.append(error)
        pending[0:0] = list(error.context)
    return flattened


def _instance_pointers(value: Any, pointer: str = "") -> list[str]:
    pointers: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_pointer = f"{pointer}/{_escape_pointer(key)}"
            pointers.append(child_pointer)
            pointers.extend(_instance_pointers(child, child_pointer))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_pointer = f"{pointer}/{index}"
            pointers.append(child_pointer)
            pointers.extend(_instance_pointers(child, child_pointer))
    return pointers


def _pointer_get(document: Any, pointer: str) -> Any:
    current = document
    for part in _pointer_parts(pointer):
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current


def _wrong_type_value(value: Any) -> Any:
    if isinstance(value, bool):
        return "wrong_type"
    if isinstance(value, str):
        return 7
    if isinstance(value, int):
        return "wrong_type"
    if isinstance(value, list):
        return {}
    if isinstance(value, dict):
        return []
    if value is None:
        return {}
    raise TypeError(f"unsupported fixture type: {type(value)!r}")


def _invalid_same_type_value(value: Any) -> Any:
    if isinstance(value, bool):
        return not value
    if isinstance(value, str):
        return "__invalid_enum_or_const__"
    if isinstance(value, int):
        return value + 999999
    return value


def _probe_surfaces(positive: Any, schema: dict[str, Any], store: dict[str, Any]) -> dict[str, list[str]]:
    required: list[str] = []
    wrong_type: list[str] = []
    invalid_enum: list[str] = []
    for pointer in _instance_pointers(positive):
        parent, key = _pointer_parent(positive, pointer)
        if isinstance(parent, dict):
            changed = copy.deepcopy(positive)
            _pointer_remove(changed, pointer)
            if _probe_blocker(_generic_errors(changed, schema, store), "required", pointer):
                required.append(pointer)
        value = _pointer_get(positive, pointer)
        changed = copy.deepcopy(positive)
        _pointer_set(changed, pointer, _wrong_type_value(value))
        if _probe_blocker(_generic_errors(changed, schema, store), "wrong_type", pointer):
            wrong_type.append(pointer)
        alternate = _invalid_same_type_value(value)
        if alternate != value:
            changed = copy.deepcopy(positive)
            _pointer_set(changed, pointer, alternate)
            if _probe_blocker(_generic_errors(changed, schema, store), "invalid_enum", pointer):
                invalid_enum.append(pointer)
    return {
        "required": sorted(set(required)),
        "wrong_type": sorted(set(wrong_type)),
        "invalid_enum": sorted(set(invalid_enum)),
    }


def _classify_generic_errors(errors: list[Any]) -> str | None:
    if not errors:
        return None
    validators = {str(error.validator) for error in _error_tree(errors)}
    priorities = (
        ("required", "E_REQUIRED_PROPERTY"),
        ("additionalProperties", "E_UNKNOWN_PROPERTY"),
        ("type", "E_WRONG_TYPE"),
        ("enum", "E_ENUM_OR_CONST"),
        ("const", "E_ENUM_OR_CONST"),
        ("pattern", "E_PATTERN"),
        ("minItems", "E_MIN_ITEMS"),
        ("maxItems", "E_MAX_ITEMS"),
        ("minimum", "E_MINIMUM"),
        ("maximum", "E_MAXIMUM"),
        ("uniqueItems", "E_NOT_UNIQUE"),
        ("oneOf", "E_ONE_OF"),
        ("not", "E_CONDITIONAL"),
    )
    for validator, blocker in priorities:
        if validator in validators:
            return blocker
    return "E_SCHEMA_VALIDATION"


def _probe_blocker(errors: list[Any], kind: str, pointer: str) -> str | None:
    parts = _pointer_parts(pointer)
    target_path = tuple(parts)
    parent_path = tuple(parts[:-1])
    leaf = parts[-1]
    for error in _error_tree(errors):
        path = tuple(str(part) for part in error.absolute_path)
        validator = str(error.validator)
        if kind == "required" and validator == "required" and path == parent_path and leaf in error.validator_value:
            return "E_REQUIRED_PROPERTY"
        if kind == "wrong_type" and validator == "type" and path == target_path:
            return "E_WRONG_TYPE"
        if kind == "invalid_enum" and validator in {"enum", "const"} and path == target_path:
            return "E_ENUM_OR_CONST"
    return None


def _generic_schema_policy(artifact: str, schema: dict[str, Any]) -> str | None:
    contract = LEAF_CONTRACTS[artifact]
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        return "E_SCHEMA_META_IDENTITY"
    if schema.get("$id") != contract["schema_id"]:
        return "E_SCHEMA_IDENTITY"
    if artifact == "common":
        if schema.get("schema_version") != "distill.common.v2":
            return "E_SCHEMA_IDENTITY"
        if set(schema.get("$defs", {})) != COMMON_DEFINITIONS:
            return "E_COMMON_SEMANTIC_COUPLING"
        return None
    if tuple(schema.get("required", ())) != contract["required"]:
        return "E_SCHEMA_REQUIRED_SURFACE"
    if schema.get("properties", {}).get("schema_version", {}).get("const") != contract["instance_schema_version"]:
        return "E_SCHEMA_IDENTITY"
    if artifact == "source":
        artifacts_schema = schema.get("properties", {}).get("artifacts", {})
        requested_schema = (
            schema.get("$defs", {})
            .get("policy", {})
            .get("properties", {})
            .get("requested_technique_refs", {})
        )
        if "minItems" in artifacts_schema or "minItems" in requested_schema:
            return "E_SOURCE_EMPTY_COLLECTION_CLOSURE"
    refs = _common_ref_entries(schema)
    if len(refs) != contract["common_ref_count"] or _canonical_digest(refs) != contract["common_ref_digest"]:
        return "E_COMMON_REF_EDGE"
    return None


def _walk_exact_ref_paths(value: Any) -> list[str]:
    blockers: list[str] = []
    if isinstance(value, dict):
        if {"path", "sha256", "size_bytes"}.issubset(value) and isinstance(value.get("path"), str):
            blocker = repository_path_blocker(value.get("path"))
            if blocker:
                blockers.append(blocker)
        for child in value.values():
            blockers.extend(_walk_exact_ref_paths(child))
    elif isinstance(value, list):
        for child in value:
            blockers.extend(_walk_exact_ref_paths(child))
    return blockers


FAILURE_ACTION_ORDER = (
    "revise_candidate",
    "merge_candidates",
    "add_guardrail",
    "defer_complexity",
    "preserve_alternatives",
    "ask_human_gate",
    "reject_candidate",
    "route",
)


def _descriptor_policy_blocker(descriptor: Any) -> str | None:
    if not isinstance(descriptor, dict):
        return None
    kind = descriptor.get("value_kind")
    if kind == "scalar":
        schema_ref = descriptor.get("schema_ref")
        scalar_type = descriptor.get("scalar_type")
        string_refs = {
            f"{COMMON_ID}#/$defs/canonical_identifier",
            f"{COMMON_ID}#/$defs/non_empty_string",
            f"{COMMON_ID}#/$defs/sha256",
        }
        integer_refs = {
            f"{COMMON_ID}#/$defs/positive_integer",
            f"{COMMON_ID}#/$defs/non_negative_integer",
        }
        if (schema_ref in string_refs and scalar_type != "string") or (
            schema_ref in integer_refs and scalar_type != "integer"
        ):
            return "E_DESCRIPTOR_SCALAR_REF"
        for lower, upper in (("minimum", "maximum"), ("min_length", "max_length")):
            if isinstance(descriptor.get(lower), (int, float)) and isinstance(descriptor.get(upper), (int, float)):
                if descriptor[lower] > descriptor[upper]:
                    return "E_DESCRIPTOR_BOUNDS"
    elif kind == "list":
        if isinstance(descriptor.get("maximum_items"), int) and descriptor["maximum_items"] > 32:
            return "E_DESCRIPTOR_BOUNDS"
        if isinstance(descriptor.get("minimum_items"), int) and isinstance(descriptor.get("maximum_items"), int):
            if descriptor["minimum_items"] > descriptor["maximum_items"]:
                return "E_DESCRIPTOR_BOUNDS"
        return _descriptor_policy_blocker(descriptor.get("items"))
    elif kind == "record":
        fields = descriptor.get("fields")
        required = descriptor.get("required_fields")
        if isinstance(fields, dict) and isinstance(required, list) and not set(required).issubset(fields):
            return "E_DESCRIPTOR_REQUIRED_FIELD"
        if isinstance(fields, dict):
            for child in fields.values():
                blocker = _descriptor_policy_blocker(child)
                if blocker:
                    return blocker
    elif kind == "union":
        variants = descriptor.get("variants")
        if isinstance(variants, list):
            tags = [item.get("tag") for item in variants if isinstance(item, dict)]
            if len(tags) != len(variants) or len(tags) != len(set(tags)):
                return "E_DESCRIPTOR_UNION_TAG"
            for item in variants:
                blocker = _descriptor_policy_blocker(item.get("descriptor"))
                if blocker:
                    return blocker
    return None


def _instance_policy_blocker(artifact: str, instance: Any) -> str | None:
    if not isinstance(instance, dict):
        return None
    if artifact == "technique_spec":
        if not relative_order_ok(instance.get("phases"), PHASE_ORDER):
            return "E_PHASE_ORDER"
        if not relative_order_ok(instance.get("hooks"), HOOK_ORDER):
            return "E_HOOK_ORDER"
        emits = instance.get("emits")
        constraints = instance.get("emitted_field_constraints")
        if isinstance(emits, list) and isinstance(constraints, dict) and set(emits) != set(constraints):
            return "E_EMITTED_FIELD_CONSTRAINT_MISSING"
        activation = instance.get("activation")
        allowed = instance.get("allowed_inputs")
        if isinstance(activation, dict) and isinstance(activation.get("predicates"), list) and isinstance(allowed, list):
            predicate_ids = [
                item.get("predicate_id")
                for item in activation["predicates"]
                if isinstance(item, dict) and isinstance(item.get("predicate_id"), str)
            ]
            if any(
                CANONICAL_IDENTIFIER_RE.fullmatch(predicate_id) is None
                for predicate_id in predicate_ids
            ):
                return "E_PATTERN"
            if len(predicate_ids) != len(set(predicate_ids)):
                return "E_ACTIVATION_PREDICATE_ID_DUPLICATE"
            for item in activation["predicates"]:
                if isinstance(item, dict):
                    permitted = {"predicate_id", "input", "comparison"}
                    if item.get("comparison") not in {"exists", "not_exists"}:
                        permitted.add("value")
                    if set(item) - permitted:
                        return "E_ACTIVATION_NOT_FLAT"
            if any(item.get("input") not in allowed for item in activation["predicates"] if isinstance(item, dict)):
                return "E_ACTIVATION_INPUT_UNDECLARED"
        if isinstance(constraints, dict):
            for descriptor in constraints.values():
                blocker = _descriptor_policy_blocker(descriptor)
                if blocker:
                    return blocker
        responses = instance.get("failure_responses")
        if isinstance(responses, list):
            if [item.get("decision") for item in responses if isinstance(item, dict)] != ["pass", "flag", "block"]:
                return "E_FAILURE_RESPONSE_ORDER"
            for response in responses:
                actions = response.get("responses") if isinstance(response, dict) else None
                if isinstance(actions, list):
                    names = [item.get("action") for item in actions if isinstance(item, dict)]
                    complete = all(
                        isinstance(item, dict)
                        and ((item.get("action") == "route" and "route_target" in item) or
                             (item.get("action") != "route" and "route_target" not in item))
                        for item in actions
                    )
                    if complete and len(names) == len(actions) and all(name in FAILURE_ACTION_ORDER for name in names):
                        positions = [FAILURE_ACTION_ORDER.index(name) for name in names]
                        if positions != sorted(positions):
                            return "E_FAILURE_ACTION_ORDER"
        if instance.get("technique_id") == "abstraction_level_guard" and instance.get("hooks") != ["before_layer_split", "before_accept_split"]:
            return "E_CANONICAL_HOOK_MISMATCH"
    if artifact == "mode_spec":
        if "closure_rule" in instance or "verdict_policy" in instance:
            return "E_MODE_OWNS_CLOSURE"
        closeout = instance.get("closeout_policy")
        if isinstance(closeout, dict) and closeout.get("verdict_owner") not in (None, "core_engine"):
            return "E_MODE_OWNS_CLOSURE"
        for field in ("tracks", "rounds_per_track"):
            count = instance.get(field)
            blocker = bounded_count_blocker(count) if isinstance(count, dict) and all(isinstance(count.get(key), int) and count.get(key) >= 1 for key in ("minimum", "default", "maximum")) else None
            if blocker:
                return blocker
        role_program = instance.get("role_program")
        if isinstance(role_program, list):
            steps = [item.get("step") for item in role_program if isinstance(item, dict)]
            if steps != list(range(1, len(role_program) + 1)):
                return "E_ROLE_PROGRAM_ORDER"
            if not role_program or not isinstance(role_program[-1], dict) or role_program[-1].get("actor") != "core_engine" or role_program[-1].get("action") != "reconcile":
                return "E_ROLE_PROGRAM_RECONCILIATION"
        technique_policy = instance.get("technique_policy")
        if isinstance(technique_policy, list):
            technique_ids = [item.get("technique_id") for item in technique_policy if isinstance(item, dict)]
            if len(technique_ids) != len(technique_policy) or len(technique_ids) != len(set(technique_ids)):
                return "E_TECHNIQUE_POLICY_DUPLICATE"
        human_gates = instance.get("human_gates")
        if isinstance(human_gates, list):
            gate_ids = [item.get("gate_id") for item in human_gates if isinstance(item, dict)]
            if len(gate_ids) != len(human_gates) or len(gate_ids) != len(set(gate_ids)):
                return "E_HUMAN_GATE_DUPLICATE"
    if artifact == "profile":
        if "mode_spec" in instance or "technique_specs" in instance:
            return "E_PROFILE_EMBEDDED_DEFINITION"
    if artifact == "source":
        if "verdict" in instance or "selected_unit_id" in instance:
            return "E_SOURCE_PREAUTHORED_VERDICT"
        lineage = instance.get("lineage")
        if isinstance(lineage, dict) and isinstance(lineage.get("objective_output_revision"), dict):
            revision = lineage["objective_output_revision"]
            if not isinstance(revision.get("reason"), str) or not revision.get("reason"):
                return "E_REVISION_REASON_REQUIRED"
    if artifact == "trace_event":
        if instance.get("event_type") in {"owner_decision", "authorization", "implementation_authority"}:
            return "E_TRACE_AUTHORITY_EVENT"
        if "mutable_summary" in instance:
            return "E_TRACE_MUTABLE_SUMMARY"
        sequence = instance.get("sequence")
        predecessor = instance.get("previous_event_sha256")
        if sequence == 0 and predecessor is not None:
            return "E_TRACE_PREDECESSOR"
        if isinstance(sequence, int) and sequence > 0 and predecessor is None:
            return "E_TRACE_PREDECESSOR"
        payload = instance.get("payload")
        if instance.get("event_type") == "technique" and isinstance(payload, dict):
            emitted = payload.get("emitted_output")
            status = payload.get("activation_status")
            decision = payload.get("decision")
            if status == "activated" and isinstance(emitted, list) and not emitted:
                return "E_TRACE_ACTIVATED_OUTPUT_REQUIRED"
            if status == "skipped" and isinstance(emitted, list) and emitted:
                return "E_TRACE_SKIPPED_OUTPUT_FORBIDDEN"
            if status == "skipped" and not payload.get("skip_reason"):
                return "E_TRACE_SKIP_REASON_REQUIRED"
            if status == "activated" and "skip_reason" in payload:
                return "E_TRACE_SKIP_REASON_FORBIDDEN"
            if (decision == "route") != ("route_target" in payload):
                return "E_TRACE_ROUTE_TARGET"
            if payload.get("policy_status") == "not_applicable" and status != "skipped":
                return "E_TRACE_ACTIVATION_STATUS"
            inspected = payload.get("inspected_state")
            if isinstance(inspected, list) and any(
                not isinstance(item, str) or STATE_FIELD_RE.fullmatch(item) is None
                for item in inspected
            ):
                return "E_TRACE_STATE_FIELD_REFERENCE"
            if isinstance(emitted, list):
                if any(
                    not isinstance(item, dict)
                    or not isinstance(item.get("value"), dict)
                    or item["value"].get("value_kind") not in {"scalar", "enum", "list", "record", "union"}
                    for item in emitted
                ):
                    return "E_TRACE_EMITTED_VALUE_TAG"
                field_ids = [item.get("field_id") for item in emitted if isinstance(item, dict)]
                if len(field_ids) == len(emitted) and len(field_ids) != len(set(field_ids)):
                    return "E_TRACE_EMITTED_FIELD_DUPLICATE"
        if instance.get("event_type") == "objection" and isinstance(payload, dict):
            if payload.get("category") not in OBJECTION_CATEGORIES:
                return "E_OBJECTION_CATEGORY"
    if artifact == "result":
        verdict = instance.get("verdict")
        selected = instance.get("selected_unit_id")
        unit = instance.get("current_smallest_coherent_unit")
        effects = instance.get("readiness_effects")
        tensions = instance.get("tension_ledger")
        route = instance.get("next_route")
        if verdict == "pass":
            if selected is None or unit is None or effects:
                return "E_RESULT_VERDICT_CONTRADICTION"
            if isinstance(tensions, list) and any(isinstance(item, dict) and item.get("effect") == "block" for item in tensions):
                return "E_RESULT_VERDICT_CONTRADICTION"
        if verdict == "flag" and (selected is None or unit is None or ("readiness_effects" in instance and not effects)):
            return "E_RESULT_VERDICT_CONTRADICTION"
        if verdict == "block" and (("selected_unit_id" in instance and selected is not None) or ("current_smallest_coherent_unit" in instance and unit is not None) or route in {"implementation_layering", "invoke_design", "invoke_plan", "task_session"}):
            return "E_RESULT_VERDICT_CONTRADICTION"
        technique_trace = instance.get("technique_pack_trace")
        if isinstance(technique_trace, list):
            event_ids = [item.get("event_id") for item in technique_trace if isinstance(item, dict)]
            if len(event_ids) == len(technique_trace) and len(event_ids) != len(set(event_ids)):
                return "E_RESULT_TECHNIQUE_EVENT_DUPLICATE"
    if artifact == "stage_receipt":
        inventory = instance.get("artifact_inventory")
        roles = [item.get("role") for item in inventory if isinstance(item, dict)] if isinstance(inventory, list) else []
        if isinstance(inventory, list) and all(isinstance(role, str) for role in roles) and (sorted(roles) != ["markdown", "result", "source", "trace"] or len(set(roles)) != 4):
            return "E_RECEIPT_INVENTORY_ROLES"
        schema_inventory = instance.get("schema_inventory")
        if isinstance(schema_inventory, list):
            schema_kinds = [item.get("schema_kind") for item in schema_inventory if isinstance(item, dict)]
            expected_schema_kinds = {"common", "mode_spec", "technique_spec", "profile", "source", "trace_event", "result", "stage_receipt"}
            if len(schema_inventory) != 8 or len(schema_kinds) != 8 or set(schema_kinds) != expected_schema_kinds:
                return "E_RECEIPT_SCHEMA_INVENTORY"
        validation = instance.get("validation_state")
        if isinstance(validation, dict):
            status, blockers = validation.get("status"), validation.get("blockers")
            if (status == "pass" and blockers) or (status == "block" and not blockers):
                return "E_RECEIPT_VALIDATION_STATE"
        method = instance.get("receipt_digest_method")
        if isinstance(method, dict) and method != {"algorithm": "sha256", "canonicalization": "canonical_utf8_json", "excluded_fields": ["receipt_digest"]}:
            return "E_RECEIPT_DIGEST_METHOD"
        publication = instance.get("publication")
        if isinstance(publication, dict) and isinstance(publication.get("method"), str) and publication.get("method") != "atomic_directory_rename":
            return "E_RECEIPT_PUBLICATION_METHOD"
    path_blockers = _walk_exact_ref_paths(instance)
    return path_blockers[0] if path_blockers else None


def _generic_observed(artifact: str, instance: Any, schema: dict[str, Any], store: dict[str, Any]) -> str | None:
    policy = _instance_policy_blocker(artifact, instance)
    if policy:
        return policy
    return _classify_generic_errors(_generic_errors(instance, schema, store))


def _apply_mutation(document: Any, mutation: dict[str, Any]) -> Any:
    operation = mutation["operation"]
    if operation == "replace_document":
        return copy.deepcopy(mutation["value"])
    changed = copy.deepcopy(document)
    if operation in {"set", "add", "set_schema", "add_schema_definition"}:
        _pointer_set(changed, mutation["pointer"], mutation.get("value"))
    elif operation == "remove":
        _pointer_remove(changed, mutation["pointer"])
    elif operation == "multi_set":
        for item in mutation["changes"]:
            _pointer_set(changed, item["pointer"], item.get("value"))
    else:
        raise ValueError(f"unknown mutation operation: {operation}")
    return changed


def _manifest_policy_mutations(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    for group in manifest.get("groups", []):
        if group.get("kind") == "generated_policy_mutations":
            return group.get("mutations", [])
    return []


def _manifest_contract_blockers(manifest: dict[str, Any], artifact: str) -> list[str]:
    contract = LEAF_CONTRACTS[artifact]
    blockers: list[str] = []
    if manifest.get("manifest_id") != contract["manifest_id"]:
        blockers.append("E_MANIFEST_IDENTITY")
    if manifest.get("schema_path") != contract["schema_path"] or manifest.get("schema_id") != contract["schema_id"]:
        blockers.append("E_MANIFEST_SCHEMA_BINDING")
    observed_kinds = tuple(group.get("kind") for group in manifest.get("groups", []))
    expected_kinds = contract.get("group_kinds", GENERIC_GROUP_KINDS)
    if observed_kinds != expected_kinds or len(set(observed_kinds)) != len(expected_kinds):
        blockers.append("E_FIXTURE_GROUP_SET_MISMATCH")
    policy_ids = tuple(item.get("id") for item in _manifest_policy_mutations(manifest))
    if policy_ids != contract["policy_ids"]:
        blockers.append("E_FIXTURE_ID_SET_MISMATCH")
    policy_specs = [{key: value for key, value in item.items() if key != "expected_blocker"} for item in _manifest_policy_mutations(manifest)]
    if _canonical_digest(policy_specs) != contract["policy_spec_digest"]:
        blockers.append("E_MUTATION_SPEC_MISMATCH")
    if manifest.get("expected_case_count") != contract["expected_count"]:
        blockers.append("E_FIXTURE_DENOMINATOR_MISMATCH")
    return blockers


def _common_value_blocker(name: str, value: Any, common: dict[str, Any], technique: dict[str, Any]) -> str | None:
    errors = direct_definition_errors(name, value, common, technique)
    blocker = _classify_generic_errors(errors)
    if blocker:
        return blocker
    if name == "repository_relative_path":
        return repository_path_blocker(value)
    if name == "exact_artifact_reference":
        return repository_path_blocker(value.get("path")) if isinstance(value, dict) else None
    if name == "bounded_count":
        return bounded_count_blocker(value)
    if name == "utc_timestamp":
        return utc_timestamp_blocker(value)
    return None


def run_generic_leaf(root: Path, manifest_path: Path) -> dict[str, Any]:
    resolved = manifest_path if manifest_path.is_absolute() else root / manifest_path
    manifest = read_json(resolved)
    artifact = manifest.get("artifact")
    if artifact not in LEAF_CONTRACTS:
        raise ValueError(f"unknown generic artifact: {artifact}")
    contract = LEAF_CONTRACTS[artifact]
    schema = read_json(root / Path(contract["schema_path"]))
    common = read_json(root / COMMON_PATH)
    technique = read_json(root / TECHNIQUE_PATH)
    positive = read_json(resolved.parent / manifest["positive_fixture"])
    store = _schema_store(root)
    blockers = _manifest_contract_blockers(manifest, artifact)
    results: list[dict[str, Any]] = []
    surfaces = _probe_surfaces(positive, schema, store) if artifact != "common" else None
    if surfaces is not None:
        for name, (expected_count, expected_digest) in contract["probe_surfaces"].items():
            observed_surface = surfaces[name]
            if len(observed_surface) != expected_count or _canonical_digest(observed_surface) != expected_digest:
                blockers.append("E_FIXTURE_PROBE_SURFACE_MISMATCH")

    try:
        Draft202012Validator.check_schema(schema)
    except Exception:
        blockers.append("E_SCHEMA_META_INVALID")
    schema_policy = _generic_schema_policy(artifact, schema)
    if schema_policy:
        blockers.append(schema_policy)

    positive_group = manifest["groups"][0]
    if artifact == "common":
        if set(positive) != COMMON_DEFINITIONS:
            observed_positive = "E_COMMON_POSITIVE_SURFACE"
        else:
            observed_positive = next((_common_value_blocker(name, positive[name], common, technique) for name in sorted(COMMON_DEFINITIONS) if _common_value_blocker(name, positive[name], common, technique)), None)
    else:
        observed_positive = _generic_observed(artifact, positive, schema, store)
    results.append({"id": positive_group["id"], "kind": "canonical_positive", "expected": "pass", "observed": "pass" if observed_positive is None else "block", "observed_blocker": observed_positive, "success": observed_positive is None})

    if artifact != "common":
        groups = {group["kind"]: group for group in manifest["groups"]}
        assert surfaces is not None
        group = groups["generated_missing_required"]
        for index, pointer in enumerate(surfaces["required"], start=1):
            changed = copy.deepcopy(positive)
            _pointer_remove(changed, pointer)
            observed = _probe_blocker(_generic_errors(changed, schema, store), "required", pointer)
            expected = group.get("expected_blocker")
            results.append({"id": f"{group['id']}:{index:03d}", "kind": group["kind"], "expected": "block", "expected_blocker": expected, "observed": "block" if observed else "pass", "observed_blocker": observed, "success": observed == expected, "detail": {"instance_pointer": pointer}})

        group = groups["generated_unknown_field"]
        changed = copy.deepcopy(positive)
        changed["unexpected_field"] = True
        observed = _generic_observed(artifact, changed, schema, store)
        expected = group.get("expected_blocker")
        results.append({"id": group["id"], "kind": group["kind"], "expected": "block", "expected_blocker": expected, "observed": "block" if observed else "pass", "observed_blocker": observed, "success": observed == expected})

        group = groups["generated_wrong_type"]
        for index, pointer in enumerate(surfaces["wrong_type"], start=1):
            changed = copy.deepcopy(positive)
            _pointer_set(changed, pointer, _wrong_type_value(_pointer_get(positive, pointer)))
            observed = _probe_blocker(_generic_errors(changed, schema, store), "wrong_type", pointer)
            expected = group.get("expected_blocker")
            results.append({"id": f"{group['id']}:{index:03d}", "kind": group["kind"], "expected": "block", "expected_blocker": expected, "observed": "block" if observed else "pass", "observed_blocker": observed, "success": observed == expected, "detail": {"instance_pointer": pointer}})

        group = groups["generated_invalid_enum_or_const"]
        for index, pointer in enumerate(surfaces["invalid_enum"], start=1):
            changed = copy.deepcopy(positive)
            _pointer_set(changed, pointer, _invalid_same_type_value(_pointer_get(positive, pointer)))
            observed = _probe_blocker(_generic_errors(changed, schema, store), "invalid_enum", pointer)
            expected = group.get("expected_blocker")
            results.append({"id": f"{group['id']}:{index:03d}", "kind": group["kind"], "expected": "block", "expected_blocker": expected, "observed": "block" if observed else "pass", "observed_blocker": observed, "success": observed == expected, "detail": {"instance_pointer": pointer}})

        group = groups["generated_common_ref_edges"]
        for index, (pointer, _) in enumerate(_common_ref_entries(schema), start=1):
            changed_schema = copy.deepcopy(schema)
            _pointer_set(changed_schema, pointer, "https://example.invalid/inline-substitution")
            observed = _generic_schema_policy(artifact, changed_schema)
            expected = group.get("expected_blocker")
            results.append({"id": f"{group['id']}:{index:03d}", "kind": group["kind"], "expected": "block", "expected_blocker": expected, "observed": "block" if observed else "pass", "observed_blocker": observed, "success": observed == expected, "detail": {"schema_pointer": pointer}})

    for mutation in _manifest_policy_mutations(manifest):
        if mutation["operation"] in {"set_schema", "add_schema_definition"}:
            changed_schema = _apply_mutation(schema, mutation)
            observed = _generic_schema_policy(artifact, changed_schema)
        else:
            changed = _apply_mutation(positive, mutation)
            if artifact == "common":
                first = _pointer_parts(mutation.get("pointer", "/canonical_identifier"))[0] if mutation["operation"] != "replace_document" else "canonical_identifier"
                observed = _common_value_blocker(first, changed[first], common, technique)
            else:
                observed = _generic_observed(artifact, changed, schema, store)
        expected = mutation.get("expected_blocker")
        results.append({"id": mutation["id"], "kind": "generated_policy_mutations", "expected": "block", "expected_blocker": expected, "observed": "block" if observed else "pass", "observed_blocker": observed, "success": observed == expected})

    if any(not result["success"] for result in results):
        blockers.append("E_FIXTURE_OUTCOME_MISMATCH")
    ids = [result["id"] for result in results]
    if len(ids) != len(set(ids)) or len(ids) != contract["expected_count"]:
        blockers.append("E_FIXTURE_DENOMINATOR_MISMATCH")
    blockers = list(dict.fromkeys(blockers))
    return {
        "schema_version": "distill.schema_fixture_validation.v2",
        "artifact": artifact,
        "status": "pass" if not blockers else "block",
        "passed": sum(result["success"] for result in results),
        "total": len(results),
        "counts": {kind: sum(result["kind"] == kind for result in results) for kind in set(result["kind"] for result in results)},
        "blockers": blockers,
        "results": results,
        "authority_effect": "none",
    }


def run_schema_family(root: Path, manifest_path: Path) -> dict[str, Any]:
    resolved = manifest_path if manifest_path.is_absolute() else root / manifest_path
    manifest = read_json(resolved)
    blockers: list[str] = []
    observed_members = tuple((item.get("artifact"), item.get("manifest_path"), item.get("expected_case_count")) for item in manifest.get("members", []))
    if observed_members != FAMILY_MEMBERS or manifest.get("expected_member_count") != 8 or manifest.get("expected_case_count") != FAMILY_TOTAL:
        blockers.append("E_FAMILY_MEMBER_SET_MISMATCH")
    member_results: list[dict[str, Any]] = []
    all_results: list[dict[str, Any]] = []
    for artifact, path, expected_count in FAMILY_MEMBERS:
        result = run_all(root, Path(path))
        member_results.append({"artifact": artifact, "status": result["status"], "passed": result["passed"], "total": result["total"], "expected_total": expected_count, "blockers": result["blockers"]})
        if result["status"] != "pass" or result["total"] != expected_count:
            blockers.append("E_FAMILY_MEMBER_FAILED")
        for item in result["results"]:
            copied = copy.deepcopy(item)
            copied["id"] = f"{artifact}:{item['id']}"
            all_results.append(copied)
    ids = [item["id"] for item in all_results]
    if len(ids) != FAMILY_TOTAL or len(ids) != len(set(ids)):
        blockers.append("E_FAMILY_DENOMINATOR_MISMATCH")
    blockers = list(dict.fromkeys(blockers))
    return {
        "schema_version": "distill.schema_family_fixture_validation.v2",
        "status": "pass" if not blockers else "block",
        "passed": sum(item["success"] for item in all_results),
        "total": len(all_results),
        "member_count": len(member_results),
        "members": member_results,
        "blockers": blockers,
        "results": all_results,
        "authority_effect": "none",
    }


def run_all(root: Path, manifest_path: Path) -> dict[str, Any]:
    resolved = manifest_path if manifest_path.is_absolute() else root / manifest_path
    manifest = read_json(resolved)
    version = manifest.get("schema_version")
    if version == "distill.schema_fixture_manifest.v2":
        return run_generic_leaf(root, manifest_path)
    if version == "distill.schema_family_fixture_manifest.v2":
        return run_schema_family(root, manifest_path)
    raise ValueError(f"unknown fixture manifest schema_version: {version}")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--root", type=Path, required=True)
    result.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    result.add_argument("--output-format", choices=("json",), default="json")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        result = run_all(args.root.resolve(), args.manifest)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        result = {
            "schema_version": "distill.schema_fixture_validation.v2",
            "status": "block",
            "passed": 0,
            "total": 0,
            "blockers": ["E_FIXTURE_INPUT_INVALID"],
            "detail": str(error),
            "authority_effect": "none",
        }
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        return 2
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
