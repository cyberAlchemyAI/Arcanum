#!/usr/bin/env python3
"""Validate an authored semantic-intent artifact against a hidden target oracle.

This is a deterministic development validator, not an Invoke lifecycle entrypoint.
It independently matches authored concepts, relationships, boundaries, evidence
dispositions, facets, probes, and consumer topology to a checked fixture oracle.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Any


FACETS = (
    "subject",
    "parts",
    "relationships",
    "evidence-state",
    "validation-gates",
    "execution-handoff",
    "authority-boundary",
)


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold().replace("\u00a0", " ")
    value = re.sub(r"[^\w]+", " ", value, flags=re.UNICODE)
    return re.sub(r"\s+", " ", value).strip()


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def labels(item: dict[str, Any]) -> set[str]:
    return {normalize(item["label"]), *(normalize(alias) for alias in item.get("aliases", []))}


def artifact_labels(item: dict[str, Any]) -> set[str]:
    return {normalize(item["term"]), *(normalize(alias) for alias in item.get("aliases", []))}


def matches_semantic_label(item: dict[str, Any], expected: dict[str, Any]) -> bool:
    """Match source vocabulary without reducing validation to raw keywords.

    Exact normalized labels remain preferred.  A multi-token oracle label may
    also occur as a complete phrase inside a more qualified authored term (for
    example, ``Invoke Plan successor`` or ``execution-entry state``).  Single
    generic aliases such as ``plan`` or ``task`` never receive substring
    matching, which keeps the match bounded before structural relation and
    boundary checks run.
    """

    authored = artifact_labels(item)
    accepted = labels(expected)
    if authored & accepted:
        return True
    return any(
        len(candidate.split()) >= 2 and candidate in authored_label
        for candidate in accepted
        for authored_label in authored
    )


def matching_semantic_items(
    items: list[dict[str, Any]], expected: dict[str, Any]
) -> list[dict[str, Any]]:
    """Prefer an exact semantic label before accepting a qualified phrase."""

    accepted = labels(expected)
    primary = normalize(expected["label"])
    primary_exact = [item for item in items if normalize(item["term"]) == primary]
    if primary_exact:
        return primary_exact
    exact = [item for item in items if artifact_labels(item) & accepted]
    if exact:
        return exact
    return [item for item in items if matches_semantic_label(item, expected)]


def diagnostic(code: str, obligation_id: str | None, detail: str) -> dict[str, Any]:
    return {"code": code, "obligation_id": obligation_id, "detail": detail}


def evaluate_artifact(oracle: dict[str, Any], artifact: dict[str, Any]) -> dict[str, Any]:
    diagnostics: list[dict[str, Any]] = []
    definitions = artifact.get("definitions", [])
    bindings = artifact.get("authority_bindings", [])
    probes = artifact.get("probes", [])
    declared_uncovered = set(artifact.get("declared_uncovered", []))
    matched: dict[str, dict[str, Any]] = {}
    definition_to_obligation: dict[str, str] = {}
    binding_to_external: dict[str, str] = {}

    for concept in oracle["concepts"]:
        obligation_id = concept["obligation_id"]
        definition_candidates = matching_semantic_items(definitions, concept)
        binding_candidates = []
        if concept.get("materialization") == "definition-or-binding":
            binding_candidates = [
                item
                for item in matching_semantic_items(bindings, concept)
                if any(
                    probe.get("authority_binding_id") == item.get("binding_id")
                    and probe.get("definition_id") is None
                    for probe in probes
                )
            ]
        candidates = [*definition_candidates, *binding_candidates]
        if obligation_id in declared_uncovered:
            diagnostics.append(
                diagnostic(
                    "OBLIGATION_UNCOVERED",
                    obligation_id,
                    "The author explicitly left this independently enumerated obligation uncovered.",
                )
            )
        if len(candidates) != 1:
            diagnostics.append(
                diagnostic(
                    "MISSING_CONCEPT" if not candidates else "AMBIGUOUS_CONCEPT",
                    obligation_id,
                    f"Expected one semantic definition; observed {len(candidates)}.",
                )
            )
            continue
        matched[obligation_id] = candidates[0]
        if candidates[0].get("definition_id") is not None:
            definition_to_obligation[candidates[0]["definition_id"]] = obligation_id
        else:
            binding_to_external[candidates[0]["binding_id"]] = obligation_id

    for external in oracle.get("external_concepts", []):
        candidates = matching_semantic_items(bindings, external)
        if len(candidates) == 1:
            binding_to_external[candidates[0]["binding_id"]] = external["external_id"]
            matched[external["external_id"]] = candidates[0]
        else:
            diagnostics.append(
                diagnostic(
                    "MISSING_EXTERNAL_BINDING",
                    external["external_id"],
                    f"Expected one exact external authority binding; observed {len(candidates)}.",
                )
            )

    probe_targets: dict[str, list[dict[str, Any]]] = {}
    known_definition_ids = set(definition_to_obligation)
    known_binding_ids = set(binding_to_external)
    all_definition_ids = {item.get("definition_id") for item in definitions}
    all_binding_ids = {item.get("binding_id") for item in bindings}
    for probe in probes:
        definition_id = probe.get("definition_id")
        binding_id = probe.get("authority_binding_id")
        definition_declared = definition_id is not None
        binding_declared = binding_id is not None
        definition_bound = definition_id in all_definition_ids
        binding_bound = binding_id in all_binding_ids
        structurally_bound = (
            (definition_declared or binding_declared)
            and (not definition_declared or definition_bound)
            and (not binding_declared or binding_bound)
        )
        if not structurally_bound:
            diagnostics.append(
                diagnostic(
                    "ORPHAN_PROBE",
                    None,
                    f"Probe {probe.get('probe_id', '<missing>')} contains an unresolved semantic target.",
                )
            )
            continue
        # A specialization probe may bind both its candidate definition and the
        # unchanged authority basis. The candidate is its primary obligation;
        # the authority binding remains independently checked below.
        if definition_id in known_definition_ids:
            key = definition_to_obligation[definition_id]
        elif binding_id in known_binding_ids:
            key = binding_to_external[binding_id]
        else:
            # The hidden oracle is a minimum required semantic denominator, not
            # a claim that no other source-backed target meaning may exist.
            # Extra authored items remain subject to structural probe integrity.
            continue
        probe_targets.setdefault(key, []).append(probe)

    for item in definitions:
        definition_id = item.get("definition_id")
        item_probes = [probe for probe in probes if probe.get("definition_id") == definition_id]
        if len(item_probes) != 1:
            diagnostics.append(
                diagnostic(
                    "PROBE_MAPPING_MISSING",
                    definition_to_obligation.get(definition_id),
                    f"Expected one probe for semantic item {definition_id}; observed {len(item_probes)}.",
                )
            )
    for item in bindings:
        binding_id = item.get("binding_id")
        item_probes = [
            probe for probe in probes if probe.get("authority_binding_id") == binding_id
        ]
        if len(item_probes) != 1:
            diagnostics.append(
                diagnostic(
                    "PROBE_MAPPING_MISSING",
                    binding_to_external.get(binding_id),
                    f"Expected one probe for semantic item {binding_id}; observed {len(item_probes)}.",
                )
            )

    chain: list[dict[str, Any]] = []
    for concept in oracle["concepts"]:
        obligation_id = concept["obligation_id"]
        definition = matched.get(obligation_id)
        probe_ids = [item["probe_id"] for item in probe_targets.get(obligation_id, [])]
        status = (
            "materialized"
            if definition is not None
            and len(probe_ids) == 1
            and obligation_id not in declared_uncovered
            else "missing"
        )
        chain.append(
            {
                "obligation_id": obligation_id,
                "kind": "concept",
                "probe_ids": probe_ids,
                "material_ids": [
                    definition.get("definition_id") or definition.get("binding_id")
                ] if definition else [],
                "status": status,
            }
        )

    def semantic_id(key: str) -> str | None:
        item = matched.get(key)
        if item is None:
            return None
        return item.get("definition_id") or item.get("semantic_id")

    for relationship in oracle.get("relationships", []):
        subject = matched.get(relationship["subject"])
        object_id = semantic_id(relationship["object"])
        allowed_types = set(relationship.get("types", [relationship["type"]]))
        found = bool(subject and subject.get("definition_id") and object_id) and any(
            relation.get("type") in allowed_types
            and relation.get("target_id") == object_id
            for relation in subject.get("relations", [])
        )
        if not found:
            diagnostics.append(
                diagnostic(
                    "MISSING_RELATIONSHIP",
                    relationship["obligation_id"],
                    relationship["statement"],
                )
            )
        chain.append(
            {
                "obligation_id": relationship["obligation_id"],
                "kind": "relationship",
                "probe_ids": [
                    item["probe_id"]
                    for endpoint in (relationship["subject"], relationship["object"])
                    for item in probe_targets.get(endpoint, [])
                ],
                "material_ids": [
                    item
                    for item in (
                        subject.get("definition_id") if subject else None,
                        object_id,
                    )
                    if item is not None
                ],
                "status": "materialized" if found else "missing",
            }
        )

    for boundary in oracle.get("boundaries", []):
        subject = matched.get(boundary["subject"])
        expected_phrases = [
            normalize(boundary["match"]),
            *(normalize(value) for value in boundary.get("matches", [])),
        ]
        found = bool(subject and subject.get("definition_id")) and any(
            expected in normalize(value)
            for value in subject.get("boundary", {}).get(boundary["field"], [])
            for expected in expected_phrases
        )
        if not found:
            diagnostics.append(
                diagnostic(
                    "MISSING_BOUNDARY",
                    boundary["obligation_id"],
                    boundary["statement"],
                )
            )
        chain.append(
            {
                "obligation_id": boundary["obligation_id"],
                "kind": "boundary",
                "probe_ids": [
                    item["probe_id"] for item in probe_targets.get(boundary["subject"], [])
                ],
                "material_ids": [subject["definition_id"]] if subject else [],
                "status": "materialized" if found else "missing",
            }
        )

    facet_map = {item.get("facet_id"): item for item in artifact.get("facets", [])}
    if set(facet_map) != set(FACETS) or len(artifact.get("facets", [])) != len(FACETS):
        diagnostics.append(
            diagnostic(
                "FACET_SET_INCOMPLETE",
                None,
                "All seven intent facets must be assessed exactly once.",
            )
        )
    required_facets = {
        item["facet"]
        for item in [
            *oracle["concepts"],
            *oracle.get("relationships", []),
            *oracle.get("boundaries", []),
        ]
    }
    for facet_id in FACETS:
        facet = facet_map.get(facet_id)
        if facet is None:
            continue
        if facet.get("status") == "unassessed":
            diagnostics.append(
                diagnostic("FACET_UNASSESSED", None, f"Facet {facet_id} is unassessed.")
            )
        elif facet_id in required_facets and facet.get("status") != "represented":
            diagnostics.append(
                diagnostic(
                    "FACET_REQUIRED_BUT_EXCLUDED",
                    None,
                    f"Facet {facet_id} contains oracle obligations but is not represented.",
                )
            )
        elif facet_id not in required_facets and facet.get("status") == "not-applicable":
            if not str(facet.get("rationale", "")).strip() or not facet.get("evidence_source_ids"):
                diagnostics.append(
                    diagnostic(
                        "FACET_NA_UNEVIDENCED",
                        None,
                        f"Facet {facet_id} lacks evidence-backed non-applicability.",
                    )
                )

    historical = [
        item for item in artifact.get("evidence_sources", []) if item.get("source_class") == "historical"
    ]
    if oracle.get("requires_historical_semantics"):
        retained = any(
            item.get("semantic_disposition") == "retain-and-reassess"
            and item.get("authority_disposition") in {"historical-only", "none"}
            for item in historical
        )
        if not retained:
            diagnostics.append(
                diagnostic(
                    "HISTORICAL_SEMANTICS_DISCARDED",
                    None,
                    "Historical authority may be discarded, but its domain semantics must be retained and reassessed.",
                )
            )

    topology = artifact.get("consumer_topology", {})
    roots = topology.get("configured_roots", [])
    enumerated = topology.get("enumerated_consumers", [])
    declared = topology.get("declared_consumers", [])
    rationale = str(topology.get("no_consumers_evidence", "")).strip()
    if not roots:
        diagnostics.append(
            diagnostic(
                "EMPTY_CIRCULAR_CONSUMER_DENOMINATOR",
                None,
                "No configured consumer root exists from which zero consumers could be independently enumerated.",
            )
        )
    elif set(enumerated) != set(declared):
        diagnostics.append(
            diagnostic(
                "CONSUMER_TOPOLOGY_MISMATCH",
                None,
                "Declared consumers do not equal independently enumerated consumers.",
            )
        )
    elif not enumerated and not rationale:
        diagnostics.append(
            diagnostic(
                "NO_CONSUMERS_UNEVIDENCED",
                None,
                "Zero enumerated consumers requires an evidence-backed rationale.",
            )
        )

    diagnostics = sorted(
        diagnostics,
        key=lambda item: (item["code"], item["obligation_id"] or "", item["detail"]),
    )
    coverage_material = {
        "target_id": oracle["target_id"],
        "chain": chain,
        "diagnostic_codes": [item["code"] for item in diagnostics],
    }
    coverage_digest = digest(coverage_material)
    snapshot = artifact.get("closure_snapshot")
    if snapshot is not None and snapshot.get("coverage_digest") != coverage_digest:
        diagnostics.append(
            diagnostic(
                "ADMISSION_CLOSURE_DRIFT",
                None,
                "The admitted artifact no longer equals the semantic state closed before mutation.",
            )
        )
        diagnostics = sorted(
            diagnostics,
            key=lambda item: (item["code"], item["obligation_id"] or "", item["detail"]),
        )

    receipt = {
        "schema_version": "invoke.define-intent-fixture-receipt.v1",
        "target_id": oracle["target_id"],
        "claim_ceiling": "independently-enumerated-semantic-obligations",
        "obligation_count": len(chain),
        "materialized_count": sum(item["status"] == "materialized" for item in chain),
        "missing_obligation_ids": [
            item["obligation_id"] for item in chain if item["status"] != "materialized"
        ],
        "chain": chain,
        "diagnostics": diagnostics,
        "coverage_digest": coverage_digest,
        "result": "pass" if not diagnostics else "block",
        "receipt_digest": "0" * 64,
    }
    receipt["receipt_digest"] = digest(
        {key: value for key, value in receipt.items() if key != "receipt_digest"}
    )
    return receipt


def build_complete_artifact(
    oracle: dict[str, Any], include_concepts: set[str] | None = None
) -> dict[str, Any]:
    included = include_concepts or {item["obligation_id"] for item in oracle["concepts"]}
    definitions = []
    authority_bindings = []
    probes = []
    semantic_ids: dict[str, str] = {}
    for concept in oracle["concepts"]:
        if concept["obligation_id"] not in included:
            continue
        suffix = concept["obligation_id"].split(":", 1)[-1]
        if concept.get("materialization") == "definition-or-binding":
            binding_id = f"binding:{suffix}"
            semantic_id = f"authority-definition:{suffix}"
            semantic_ids[concept["obligation_id"]] = semantic_id
            authority_bindings.append(
                {
                    "binding_id": binding_id,
                    "semantic_id": semantic_id,
                    "term": concept["label"],
                    "aliases": copy.deepcopy(concept.get("aliases", [])),
                }
            )
            probes.append(
                {
                    "probe_id": f"probe:{suffix}",
                    "term": concept["label"],
                    "definition_id": None,
                    "authority_binding_id": binding_id,
                }
            )
            continue
        definition_id = f"definition:{suffix}"
        semantic_ids[concept["obligation_id"]] = definition_id
        definitions.append(
            {
                "definition_id": definition_id,
                "term": concept["label"],
                "aliases": copy.deepcopy(concept.get("aliases", [])),
                "relations": [],
                "boundary": {"includes": [], "excludes": [], "conditions": []},
            }
        )
        probes.append(
            {
                "probe_id": f"probe:{suffix}",
                "term": concept["label"],
                "definition_id": definition_id,
                "authority_binding_id": None,
            }
        )

    for external in oracle.get("external_concepts", []):
        suffix = external["external_id"].split(":", 1)[-1]
        binding_id = f"binding:{suffix}"
        semantic_id = f"authority-definition:{suffix}"
        semantic_ids[external["external_id"]] = semantic_id
        authority_bindings.append(
            {
                "binding_id": binding_id,
                "semantic_id": semantic_id,
                "term": external["label"],
                "aliases": copy.deepcopy(external.get("aliases", [])),
            }
        )
        probes.append(
            {
                "probe_id": f"probe:{suffix}",
                "term": external["label"],
                "definition_id": None,
                "authority_binding_id": binding_id,
            }
        )

    definitions_by_id = {item["definition_id"]: item for item in definitions}
    for relationship in oracle.get("relationships", []):
        subject_id = semantic_ids.get(relationship["subject"])
        object_id = semantic_ids.get(relationship["object"])
        if subject_id in definitions_by_id and object_id is not None:
            definitions_by_id[subject_id]["relations"].append(
                {"type": relationship["type"], "target_id": object_id}
            )
    for boundary in oracle.get("boundaries", []):
        subject_id = semantic_ids.get(boundary["subject"])
        if subject_id in definitions_by_id:
            definitions_by_id[subject_id]["boundary"][boundary["field"]].append(
                boundary["match"]
            )

    required_facets = {
        item["facet"]
        for item in [
            *oracle["concepts"],
            *oracle.get("relationships", []),
            *oracle.get("boundaries", []),
        ]
    }
    evidence_sources = [
        {
            "source_id": "source:current-objective",
            "source_class": "current-intent",
            "semantic_disposition": "retain",
            "authority_disposition": "none",
            "rationale": "The bounded current objective is retained as intent evidence.",
        }
    ]
    if oracle.get("requires_historical_semantics"):
        evidence_sources.append(
            {
                "source_id": "source:historical-plan",
                "source_class": "historical",
                "semantic_disposition": "retain-and-reassess",
                "authority_disposition": "historical-only",
                "rationale": "Prior authority is historical while its domain concepts remain evidence.",
            }
        )
    source_ids = [item["source_id"] for item in evidence_sources]
    return {
        "schema_version": "invoke.define-intent-authored-artifact.v1",
        "target_id": oracle["target_id"],
        "evidence_sources": evidence_sources,
        "facets": [
            {
                "facet_id": facet_id,
                "status": "represented" if facet_id in required_facets else "not-applicable",
                "evidence_source_ids": source_ids,
                "rationale": (
                    "The oracle has independently enumerated obligations for this facet."
                    if facet_id in required_facets
                    else "The configured evidence has no obligation for this bounded facet."
                ),
            }
            for facet_id in FACETS
        ],
        "definitions": definitions,
        "authority_bindings": authority_bindings,
        "probes": probes,
        "declared_uncovered": [],
        "consumer_topology": {
            "configured_roots": ["fixture://configured-consumers"],
            "enumerated_consumers": [],
            "declared_consumers": [],
            "no_consumers_evidence": "The configured fixture root enumerated zero current consumers.",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", required=True, type=Path)
    parser.add_argument("--target")
    parser.add_argument("--artifact", required=True, type=Path)
    args = parser.parse_args()
    matrix = load_object(args.matrix)
    artifact = load_object(args.artifact)
    target_key = args.target
    if target_key is None:
        matches = [
            key
            for key, value in matrix["targets"].items()
            if value["target_id"] == artifact.get("target_id")
        ]
        if len(matches) != 1:
            raise SystemExit(
                f"artifact target_id resolves to {len(matches)} fixture oracles"
            )
        target_key = matches[0]
    try:
        oracle = matrix["targets"][target_key]
    except KeyError as exc:
        raise SystemExit(f"unknown target oracle: {target_key}") from exc
    receipt = evaluate_artifact(oracle, artifact)
    print(canonical_bytes(receipt).decode("utf-8"), end="")
    return 0 if receipt["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
