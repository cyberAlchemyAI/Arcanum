#!/usr/bin/env python3
"""Pure deterministic projections for one coherent Invoke Design candidate."""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any


VIEW_ORDER = (
    ("context", "Context View"),
    ("high_level_structure", "High-Level Structure View"),
    ("low_level_components", "Low-Level Components View"),
    ("workflow_process", "Workflow Process View"),
    ("decision_flow", "Decision Flow View"),
    ("dependency_interface", "Dependency Interface View"),
)


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def compact(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def with_digest(document: dict[str, Any], field: str) -> dict[str, Any]:
    """Return a copy carrying the canonical digest of every field except itself."""
    result = copy.deepcopy(document)
    result[field] = hashlib.sha256(compact(result).encode("utf-8")).hexdigest()
    return result


def cell(value: Any) -> str:
    text = value if isinstance(value, str) else compact(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


def render_architecture(artifact: dict[str, Any]) -> bytes:
    facts = {item["fact_id"]: item for item in artifact["facts"]}
    lines = [
        f"# Architecture: {artifact['target_id']}",
        "",
        "This file is a deterministic human view of `DESIGN.json`. The machine artifact and its exact receipts remain authoritative.",
        "",
        "## Design Boundary",
        "",
        f"- Target: `{artifact['target_id']}`",
        f"- Profile: `{artifact['profile_id']}`",
        f"- Design kind: `{artifact['design_kind']['kind']}`",
        f"- Selection evidence: `{artifact['selection_evidence_state']}`",
        f"- Plan evidence: `{artifact['plan_evidence_state']}`",
    ]
    for key, title in VIEW_ORDER:
        view = artifact["views"][key]
        lines.extend(["", f"## {title}", "", f"- View ID: `{view['view_id']}`", f"- Applicability: `{view['applicability']}`", ""])
        if view["applicability"] == "not-applicable-with-evidence":
            lines.append("No facts are projected. Evidence:")
            lines.append("")
            for ref in sorted(view["na_evidence_refs"], key=lambda item: item["path"]):
                lines.append(f"- `{ref['path']}` (`{ref['sha256']}`, {ref['size']} bytes)")
            continue
        lines.extend([
            "| Fact ID | Kind | Name | Owner | Typed attributes |",
            "| --- | --- | --- | --- | --- |",
        ])
        for fact_id in sorted(view["fact_ids"]):
            fact = facts[fact_id]
            lines.append(
                f"| `{cell(fact_id)}` | `{cell(fact['fact_kind'])}` | {cell(fact['name'])} | "
                f"`{cell(fact['owner'])}` | `{cell(fact['attributes'])}` |"
            )
    lines.extend([
        "",
        "## Concern Trace",
        "",
        "| Concern ID | Class | Disposition | Facts | Selected output |",
        "| --- | --- | --- | --- | --- |",
    ])
    for concern in sorted(artifact["concern_trace"], key=lambda item: item["concern_id"]):
        lines.append(
            f"| `{cell(concern['concern_id'])}` | `{cell(concern['primary_class'])}` | "
            f"`{cell(concern['disposition'])}` | `{cell(concern['fact_ids'])}` | "
            f"`{cell(concern['selected_output_id'])}` |"
        )
    lines.extend(["", "## Evidence Ceiling", "", "- Architecture facts are authored and independently coherent within the exact W1 denominator.", "- Planned witnesses remain unexecuted Plan contracts.", "- This view grants no registry, runtime, acceptance, execution, publication, deployment, or external-effect authority.", ""])
    return "\n".join(lines).encode("utf-8")


def render_selected_companions(artifact: dict[str, Any]) -> bytes:
    facts = {item["fact_id"]: item for item in artifact["facts"]}
    lines = [
        f"# Selected Design Companions: {artifact['target_id']}",
        "",
        "This aggregate is a deterministic view of the selected companion records in `DESIGN.json`.",
    ]
    companions = sorted(artifact["selected_companions"], key=lambda item: item["output_id"])
    if not companions:
        lines.extend(["", "No companion output was selected.", ""])
        return "\n".join(lines).encode("utf-8")
    for companion in companions:
        lines.extend(["", f"## `{companion['output_id']}`", "", "| Fact ID | Kind | Name | Owner |", "| --- | --- | --- | --- |"])
        for fact_id in sorted(companion["fact_ids"]):
            fact = facts[fact_id]
            lines.append(f"| `{cell(fact_id)}` | `{cell(fact['fact_kind'])}` | {cell(fact['name'])} | `{cell(fact['owner'])}` |")
        lines.extend(["", "Requirement references:"])
        for ref in sorted(companion["requirement_refs"], key=lambda item: (item["subject_kind"], item["subject_id"])):
            lines.append(f"- `{ref['subject_kind']}:{ref['subject_id']}`")
    lines.extend(["", "These companions do not promote templates or complete Spellcraft, Sigil Development, UX, research, or Plan lifecycles.", ""])
    return "\n".join(lines).encode("utf-8")


def render_layering(artifact: dict[str, Any]) -> bytes:
    layering = artifact["layering"]
    lines = [f"# Implementation Layering Seed: {artifact['target_id']}", "", "This is a Design-stage projection, not a complete Plan layering artifact.", ""]
    if layering["kind"] == "seed":
        lines.extend(["## Seed", "", f"- Decision: {layering['decision']}", f"- Minimum unit: {layering['minimum_unit']}"])
    else:
        lines.extend(["## Gap", "", f"- Rationale: {layering['rationale']}"])
    lines.extend(["", "Plan evidence remains `plan-evidence-pending`.", ""])
    return "\n".join(lines).encode("utf-8")


def derive_next_route(artifact: dict[str, Any]) -> str:
    outputs = set(artifact["selected_outputs"])
    spell = any(item == "spell" or item.startswith("spell:") or item.startswith("spell-") for item in outputs)
    sigil = any(item == "sigil" or item.startswith("sigil:") or item.startswith("sigil-") for item in outputs)
    if spell and sigil:
        raise ValueError("selected outputs cross Spellcraft and Sigil Development owner routes")
    if artifact["unresolved_gaps"]:
        return "deferred"
    if spell:
        return "spellcraft"
    if sigil:
        return "sigil-development"
    return "plan"


def project_json_views(
    artifact: dict[str, Any],
    coherence_ref: dict[str, Any],
    artifact_ref: dict[str, Any],
    next_route: str,
) -> dict[str, dict[str, Any]]:
    glossary = {
        "$schema": "https://arcanum.dev/schemas/invoke/design-glossary-consistency-report/v1",
        "schema_version": "invoke.design-glossary-consistency-report.v1",
        "report_id": f"{artifact['artifact_id']}:glossary-report:v1",
        "target_id": artifact["target_id"],
        "design_artifact_ref": copy.deepcopy(artifact_ref),
        "source_glossary_ref": copy.deepcopy(artifact["glossary_application"]["source_glossary_ref"]),
        "mappings": sorted(copy.deepcopy(artifact["glossary_application"]["mappings"]), key=lambda item: item["term"]),
        "unmapped_terms": sorted(artifact["glossary_application"]["unmapped_terms"]),
        "conflicts": [],
        "result": "pass",
        "evidence_state": "authored-complete",
        "plan_evidence_state": "plan-evidence-pending",
        "promotion_state": "not-promoted",
        "authority_effect": "none",
    }
    glossary = with_digest(glossary, "report_digest")
    witnesses = {
        "$schema": "https://arcanum.dev/schemas/invoke/design-planned-witness-contracts/v1",
        "schema_version": "invoke.design-planned-witness-contracts.v1",
        "contract_set_id": f"{artifact['artifact_id']}:planned-witnesses:v1",
        "target_id": artifact["target_id"],
        "design_artifact_ref": copy.deepcopy(artifact_ref),
        "witnesses": sorted(copy.deepcopy(artifact["planned_witnesses"]), key=lambda item: item["witness_id"]),
        "evidence_state": "authored-complete",
        "execution_state": "not-executed",
        "plan_evidence_state": "plan-evidence-pending",
        "promotion_state": "not-promoted",
        "authority_effect": "none",
    }
    witnesses = with_digest(witnesses, "contract_set_digest")
    template = {
        "$schema": "https://arcanum.dev/schemas/invoke/design-template-selection-receipt/v1",
        "schema_version": "invoke.design-template-selection-receipt.v1",
        "receipt_id": f"{artifact['artifact_id']}:template-selection:v1",
        "target_id": artifact["target_id"],
        "design_artifact_ref": copy.deepcopy(artifact_ref),
        "selected_profile_id": artifact["template_selection"]["selected_profile_id"],
        "selection_evidence_ref": copy.deepcopy(artifact["template_selection"]["evidence_ref"]),
        "selected_companion_ids": sorted(item["output_id"] for item in artifact["selected_companions"]),
        "selection_state": "authored-complete",
        "promotion_state": "not-promoted",
        "plan_evidence_state": "plan-evidence-pending",
        "authority_effect": "none",
    }
    template = with_digest(template, "receipt_digest")
    dispatch = {
        "$schema": "https://arcanum.dev/schemas/invoke/design-dispatch-trace/v1",
        "schema_version": "invoke.design-dispatch-trace.v1",
        "trace_id": f"{artifact['artifact_id']}:dispatch-trace:v1",
        "target_id": artifact["target_id"],
        "design_artifact_ref": copy.deepcopy(artifact_ref),
        "techniques": sorted(artifact["dispatch_trace"]["techniques"]),
        "trace_evidence_ref": copy.deepcopy(artifact["dispatch_trace"]["evidence_ref"]),
        "trace_state": "authored-complete",
        "execution_state": "not-executed",
        "plan_evidence_state": "plan-evidence-pending",
        "authority_effect": "none",
    }
    dispatch = with_digest(dispatch, "trace_digest")
    transport = {
        "$schema": "https://arcanum.dev/schemas/invoke/design-transport-report/v1",
        "schema_version": "invoke.design-transport-report.v1",
        "report_id": f"{artifact['artifact_id']}:transport-report:v1",
        "target_id": artifact["target_id"],
        "design_artifact_ref": copy.deepcopy(artifact_ref),
        "policy": {
            "append_existing_only": artifact["transport_policy"]["append_existing_only"],
            "upstream_mutation": artifact["transport_policy"]["upstream_mutation"],
            "targets": sorted(artifact["transport_policy"]["targets"]),
        },
        "transport_state": "no-op",
        "mutation_performed": False,
        "promotion_state": "not-promoted",
        "plan_evidence_state": artifact["plan_evidence_state"],
        "authority_effect": "none",
    }
    transport = with_digest(transport, "report_digest")
    return {
        "GLOSSARY-CONSISTENCY-REPORT.json": glossary,
        "PLANNED-WITNESS-CONTRACTS.json": witnesses,
        "TEMPLATE-SELECTION-RECEIPT.json": template,
        "DISPATCH-TRACE.json": dispatch,
        "DESIGN-TRANSPORT-REPORT.json": transport,
    }


def project_bundle(
    artifact: dict[str, Any],
    coherence_ref: dict[str, Any],
    artifact_ref: dict[str, Any],
) -> tuple[str, dict[str, bytes]]:
    next_route = derive_next_route(artifact)
    result = {
        "ARCHITECTURE.md": render_architecture(artifact),
        "SELECTED-COMPANIONS.md": render_selected_companions(artifact),
        "IMPLEMENTATION-LAYERING.md": render_layering(artifact),
    }
    result.update({name: pretty_bytes(document) for name, document in project_json_views(artifact, coherence_ref, artifact_ref, next_route).items()})
    return next_route, result
