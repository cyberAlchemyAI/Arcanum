#!/usr/bin/env python3
"""Validate Arcanum dispatch-spec documents.

This validator intentionally goes beyond JSON Schema. The schema checks the
shape; this script checks dispatch governance rules from SKILL.md and the
technique catalog.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover - environment guard
    print("VALIDATION=block")
    print(f"BLOCK: missing jsonschema dependency: {exc}", file=sys.stderr)
    raise SystemExit(2)

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment guard
    print("VALIDATION=block")
    print(f"BLOCK: missing PyYAML dependency: {exc}", file=sys.stderr)
    raise SystemExit(2)


SCRIPT_DIR = Path(__file__).resolve().parent
LOCAL_PACKAGE = SCRIPT_DIR.parent
ROOT = Path(__file__).resolve().parents[3]
REPO_PACKAGE = ROOT / "formulae" / "dispatch-spec"
PACKAGE = LOCAL_PACKAGE if (LOCAL_PACKAGE / "dispatch.schema.yml").exists() else REPO_PACKAGE
SCHEMA_PATH = PACKAGE / "dispatch.schema.yml"
CATALOG_PATH = PACKAGE / "TECHNIQUE-CATALOG.md"

NON_FIRST_INPUT_KINDS = {
    "frame",
    "handle",
    "decision",
    "ledger",
    "human_answer",
    "external_context",
    "artifact",
}
PROMOTION_AUTHORITY_TERMS = {
    "promote inventory",
    "promote ontology",
    "promote glossary",
    "promote sigil",
    "promote spell",
    "promotes inventory",
    "promotes ontology",
    "promotes glossary",
    "promotes sigil",
    "promotes spell",
}
BOUNDARY_EVIDENCE_TECHNIQUES = {
    "delegation_boundary",
    "authority_split_gate",
    "protected_action_mapping",
    "route_projection_boundary",
    "plan_import_preview_gate",
    "capability_projection_pack",
    "role_projection_boundary",
    "execution_receipt_handoff",
    "evidence_receipt_link",
    "evidence_summary_handoff",
    "concrete_path_evidence",
    "approval_semantics_map",
    "artifact_contract_bridge",
    "state_namespace_boundary",
    "memory_promotion_split",
}
CANONICAL_PROMOTION_TARGETS = {
    "inventory",
    "ontology",
    "glossary",
    "sigil",
    "spell",
}
EXECUTION_EVIDENCE_SOURCES = {
    "execution",
    "execution evidence",
    "task evidence",
    "delegated execution",
    "receipt",
    "runtime",
}
SUBAGENT_LIFECYCLE_RECEIPT_FIELDS = {
    "agent_id",
    "role_id",
    "spawn_status",
    "join_status",
    "close_status",
    "residue",
    "reroute",
}
SUBAGENT_TERMINAL_JOIN_STATUSES = {
    "completed",
    "timed_out",
    "blocked",
    "handed_off",
    "closed_without_result",
}
SUBAGENT_TERMINAL_CLOSE_STATUSES = {
    "closed",
    "already_closed",
    "handed_off",
    "blocked",
    "not_needed",
}
COMMAND_INTERFACE_TERMS = {
    ".codex/commands",
    "slash command",
    "slash-command",
    "command file",
    "command-backed",
    "tools/arcanum --resolve",
    "tools/arcanum --exec",
}
COMMAND_INTERFACE_NEGATIONS = {
    "must not require",
    "do not require",
    "does not require",
    "not require",
    "cannot satisfy",
    "not active",
    "deprecated",
    "outside the native",
}
NATIVE_RECEIPT_REQUIRED_FIELDS = {
    "dispatch_id",
    "step_id",
    "capability_ref",
    "status",
    "artifacts",
    "validation",
    "observer_status",
    "blockers",
    "residue",
    "handoff_note",
}
CANONICAL_CAPABILITY_IDS = {
    "context-builder",
    "invoke",
    "interrogation",
    "distill",
    "refine",
    "dispatch-spec",
    "task-session",
    "sigil-development",
    "spellcraft",
}
CAPABILITY_REF_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:[-_][a-z0-9]+)*(?:/[a-z][a-z0-9_.-]*)?$")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_schema(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        if path.suffix in {".yml", ".yaml"}:
            return yaml.safe_load(handle)
        return json.load(handle)


def catalog_ids(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    return set(re.findall(r"\|\s*`([^`]+)`\s*\|", text))


def technique_id(value: Any) -> tuple[str | None, str | None, str | None]:
    if isinstance(value, str):
        return value, None, None
    if isinstance(value, dict):
        return value.get("id"), value.get("source"), value.get("validation_note")
    return None, None, None


def iter_techniques(doc: dict[str, Any]) -> list[tuple[str, Any]]:
    found: list[tuple[str, Any]] = []
    for value in doc.get("techniques", []) or []:
        found.append(("dispatch", value))
    for overlay in doc.get("technique_overlays", []) or []:
        overlay_id = overlay.get("overlay_id", "<unknown-overlay>") if isinstance(overlay, dict) else "<unknown-overlay>"
        for value in overlay.get("techniques", []) or [] if isinstance(overlay, dict) else []:
            found.append((f"overlay:{overlay_id}", value))
    for step in doc.get("steps", []) or []:
        step_id = step.get("step_id", "<unknown-step>")
        for value in step.get("techniques", []) or []:
            found.append((f"step:{step_id}", value))
    return found


def technique_usage_haystack(doc: dict[str, Any]) -> str:
    doc_copy = copy.deepcopy(doc)
    doc_copy.pop("techniques", None)
    for step in doc_copy.get("steps", []) or []:
        if isinstance(step, dict):
            step.pop("techniques", None)
    return json.dumps(doc_copy, sort_keys=True).lower()


def validate_subagent_lifecycle(
    subagent_strategy: dict[str, Any],
    subagent_lifecycle: dict[str, Any],
    blocks: list[str],
    flags: list[str],
) -> None:
    """Validate runtime closeout receipts for delegated subagent execution."""

    strategy_status = subagent_strategy.get("status")
    if strategy_status in {"recommended", "required"}:
        receipt_requirements = {
            str(item)
            for item in subagent_strategy.get("receipt_requirements", []) or []
            if isinstance(item, str)
        }
        missing_receipts = sorted(SUBAGENT_LIFECYCLE_RECEIPT_FIELDS - receipt_requirements)
        if missing_receipts:
            blocks.append(
                "subagent_strategy.receipt_requirements missing lifecycle fields: "
                + ", ".join(missing_receipts)
            )

    if not subagent_lifecycle:
        return

    lifecycle_status = subagent_lifecycle.get("status")
    agents = subagent_lifecycle.get("agents", [])
    strategy_role_ids = {
        str(role.get("role_id"))
        for role in subagent_strategy.get("roles", []) or []
        if isinstance(role, dict) and role.get("role_id")
    }
    if lifecycle_status in {"pass", "flag", "block"} and not agents:
        blocks.append("subagent_lifecycle agents are required when lifecycle status is pass, flag, or block")

    for idx, agent in enumerate(agents if isinstance(agents, list) else []):
        if not isinstance(agent, dict):
            blocks.append("subagent_lifecycle.agents entries must be objects")
            continue
        agent_id = agent.get("agent_id", f"<agent-{idx + 1}>")
        role_id = agent.get("role_id")
        spawn_status = agent.get("spawn_status")
        join_status = agent.get("join_status")
        close_status = agent.get("close_status")
        residue = agent.get("residue")
        reroute = agent.get("reroute")

        if strategy_role_ids and role_id not in strategy_role_ids:
            blocks.append(f"subagent_lifecycle:{agent_id}: role_id '{role_id}' is not declared in subagent_strategy.roles")

        if spawn_status == "blocked":
            if not agent.get("spawn_error"):
                blocks.append(f"subagent_lifecycle:{agent_id}: blocked spawn requires spawn_error")
            if not residue or not reroute:
                blocks.append(f"subagent_lifecycle:{agent_id}: blocked spawn requires residue and reroute")
            continue

        if spawn_status == "spawned":
            if not join_status:
                blocks.append(f"subagent_lifecycle:{agent_id}: spawned agent requires join_status")
            if join_status == "pending":
                blocks.append(f"subagent_lifecycle:{agent_id}: pending join_status blocks closeout")
            if join_status == "completed" and not agent.get("receipt_artifact"):
                blocks.append(f"subagent_lifecycle:{agent_id}: completed join requires receipt_artifact")
            if join_status in {"timed_out", "blocked"} and (not residue or not reroute):
                blocks.append(f"subagent_lifecycle:{agent_id}: {join_status} join requires residue and reroute")
            if join_status == "handed_off" and not reroute:
                blocks.append(f"subagent_lifecycle:{agent_id}: handed_off join requires reroute")
            if join_status in SUBAGENT_TERMINAL_JOIN_STATUSES and not close_status:
                blocks.append(f"subagent_lifecycle:{agent_id}: terminal join requires close_status")
            if close_status == "pending":
                blocks.append(f"subagent_lifecycle:{agent_id}: pending close_status blocks closeout")
            if close_status not in SUBAGENT_TERMINAL_CLOSE_STATUSES and lifecycle_status == "pass":
                blocks.append(f"subagent_lifecycle:{agent_id}: pass lifecycle requires terminal close_status")

    if lifecycle_status == "pass":
        open_agents = [
            str(agent.get("agent_id", f"<agent-{idx + 1}>"))
            for idx, agent in enumerate(agents if isinstance(agents, list) else [])
            if isinstance(agent, dict)
            and (
                agent.get("spawn_status") == "spawned"
                and (
                    agent.get("join_status") not in SUBAGENT_TERMINAL_JOIN_STATUSES
                    or agent.get("close_status") not in SUBAGENT_TERMINAL_CLOSE_STATUSES
                )
            )
        ]
        if open_agents:
            blocks.append("subagent_lifecycle pass cannot include open agents: " + ", ".join(open_agents))
    elif lifecycle_status == "block":
        blocks.append("subagent_lifecycle status is block")
    elif lifecycle_status == "flag":
        flags.append("subagent_lifecycle status is flag; closeout residue requires operator review")


def validate_native_stage_receipts(
    doc: dict[str, Any],
    steps: list[Any],
    gates: list[Any],
    blocks: list[str],
    flags: list[str],
) -> None:
    """Validate commandless native receipt expectations for active routes."""

    native_receipt_gate = any(
        isinstance(gate, dict)
        and (
            str(gate.get("gate_id", "")) == "g03-native-capability-receipts"
            or "native receipt" in str(gate.get("condition", "")).lower()
            or "native stage receipt" in str(gate.get("condition", "")).lower()
        )
        for gate in gates
    )
    receipts = doc.get("native_stage_receipts", [])
    if native_receipt_gate and not receipts:
        blocks.append("native_stage_receipts are required when a native receipt gate is active")
        return
    if not receipts:
        return
    if not isinstance(receipts, list):
        blocks.append("native_stage_receipts must be an array")
        return

    step_by_id = {
        step.get("step_id"): step
        for step in steps
        if isinstance(step, dict) and step.get("step_id")
    }
    receipt_step_ids: set[str] = set()
    for idx, receipt in enumerate(receipts):
        if not isinstance(receipt, dict):
            blocks.append("native_stage_receipts entries must be objects")
            continue
        step_id = receipt.get("step_id", f"<receipt-{idx + 1}>")
        receipt_step_ids.add(str(step_id))
        capability_ref = str(receipt.get("capability_ref", ""))
        status = receipt.get("status")
        if step_id not in step_by_id:
            blocks.append(f"native_stage_receipts:{step_id}: references unknown step_id")
            continue
        step_capability = str(step_by_id[step_id].get("capability_ref", ""))
        if capability_ref != step_capability:
            blocks.append(f"native_stage_receipts:{step_id}: capability_ref does not match step capability_ref")
        if status == "pass" and not (receipt.get("artifacts") or receipt.get("validation")):
            blocks.append(f"native_stage_receipts:{step_id}: pass receipt requires artifacts or validation")
        if status in {"block", "flag"} and not (receipt.get("blockers") or receipt.get("residue")):
            flags.append(f"native_stage_receipts:{step_id}: {status} receipt should include blockers or residue")

    if native_receipt_gate:
        missing = sorted(set(step_by_id) - receipt_step_ids)
        if missing:
            blocks.append("native_stage_receipts missing step receipts: " + ", ".join(missing))


def validate_capability_refs(steps: list[Any], blocks: list[str], flags: list[str]) -> None:
    for idx, step in enumerate(steps):
        if not isinstance(step, dict):
            continue
        step_id = step.get("step_id", f"<step-{idx + 1}>")
        capability_ref = str(step.get("capability_ref", ""))
        if not CAPABILITY_REF_PATTERN.match(capability_ref):
            blocks.append(f"{step_id}: capability_ref '{capability_ref}' is not a valid native capability handle")
        elif capability_ref not in CANONICAL_CAPABILITY_IDS and not (
            isinstance(step.get("capability_metadata"), dict)
            or str(step.get("capability_status", "")) in {"candidate", "external", "local-extension"}
        ):
            flags.append(f"{step_id}: capability_ref '{capability_ref}' is not canonical and has no candidate metadata")


def validate_command_interface_gates(doc: dict[str, Any], gates: list[Any], blocks: list[str]) -> None:
    compatibility = str(doc.get("compatibility", "")).lower()
    route_class = str(doc.get("route_class", "")).lower()
    legacy_mode = compatibility == "legacy-compatibility" or route_class == "legacy-compatibility"
    for gate in gates:
        if not isinstance(gate, dict):
            continue
        gate_id = gate.get("gate_id", "<unknown-gate>")
        condition = str(gate.get("condition", "")).lower()
        on_fail = str(gate.get("on_fail", "")).lower()
        is_negative_boundary = any(phrase in condition for phrase in COMMAND_INTERFACE_NEGATIONS)
        if any(term in condition for term in COMMAND_INTERFACE_TERMS) and on_fail == "block" and not legacy_mode and not is_negative_boundary:
            blocks.append(f"{gate_id}: active dispatch gate requires deprecated command-interface proof")


def validate(doc: dict[str, Any], schema: dict[str, Any], known_techniques: set[str]) -> tuple[str, list[str], list[str]]:
    blocks: list[str] = []
    flags: list[str] = []

    schema_errors = sorted(Draft202012Validator(schema).iter_errors(doc), key=lambda err: list(err.path))
    for err in schema_errors:
        loc = "/".join(map(str, err.path)) or "<root>"
        blocks.append(f"schema:{loc}: {err.message}")

    steps = doc.get("steps", []) if isinstance(doc.get("steps"), list) else []
    gates = doc.get("gates", []) if isinstance(doc.get("gates"), list) else []
    obs = doc.get("observability", {}) if isinstance(doc.get("observability"), dict) else {}
    boundary_evidence = doc.get("boundary_evidence", {}) if isinstance(doc.get("boundary_evidence"), dict) else {}
    subagent_strategy = doc.get("subagent_strategy", {}) if isinstance(doc.get("subagent_strategy"), dict) else {}
    subagent_lifecycle = doc.get("subagent_lifecycle", {}) if isinstance(doc.get("subagent_lifecycle"), dict) else {}

    step_ids: set[str] = set()
    for idx, step in enumerate(steps):
        if not isinstance(step, dict):
            continue
        step_id = step.get("step_id", f"<step-{idx + 1}>")
        if step_id in step_ids:
            blocks.append(f"duplicate step_id: {step_id}")
        step_ids.add(step_id)

        inputs = step.get("inputs", []) if isinstance(step.get("inputs"), list) else []
        input_kinds = {item.get("kind") for item in inputs if isinstance(item, dict)}
        if idx > 0 and not (input_kinds & NON_FIRST_INPUT_KINDS):
            blocks.append(f"{step_id}: non-first step must consume a prior frame, handle, decision, ledger, artifact, human answer, or external context")

        pattern = step.get("pattern")
        step_techniques = {
            technique_id(value)[0]
            for value in step.get("techniques", []) or []
            if technique_id(value)[0]
        }
        if step.get("parallel") is True and not step.get("join_policy"):
            blocks.append(f"{step_id}: parallel step requires join_policy")
        technique_patterns = {pattern} | step_techniques
        for structured_pattern in {"dialectic", "tournament"} & technique_patterns:
            if not step.get("roles"):
                blocks.append(f"{step_id}: {structured_pattern} technique requires roles")
            if not step.get("convergence_criteria"):
                blocks.append(f"{step_id}: {structured_pattern} technique requires convergence_criteria")
        if {"validation", "toy_game"} & technique_patterns and not step.get("evidence_artifact"):
            blocks.append(f"{step_id}: validation or toy_game technique requires evidence_artifact")
        if "x_ray" in technique_patterns:
            outputs = step.get("outputs", []) if isinstance(step.get("outputs"), list) else []
            output_kinds = {item.get("kind") for item in outputs if isinstance(item, dict)}
            if not (output_kinds & {"handle", "artifact"}):
                blocks.append(f"{step_id}: x_ray technique requires a handle or artifact output")

    validate_capability_refs(steps, blocks, flags)

    if not any(isinstance(step, dict) and step.get("stop_conditions") for step in steps):
        flags.append("dispatch has no step stop_conditions")

    trace_events = obs.get("trace_events") if isinstance(obs, dict) else None
    if not trace_events:
        blocks.append("observability.trace_events must contain at least one event")
    if obs.get("dispatch_id_required") is not True:
        flags.append("observability.dispatch_id_required should be true")

    if subagent_strategy:
        strategy_status = subagent_strategy.get("status")
        strategy_roles = subagent_strategy.get("roles", []) if isinstance(subagent_strategy.get("roles"), list) else []
        strategy_authorization = subagent_strategy.get("authorization")
        strategy_join_policy = subagent_strategy.get("join_policy")
        if strategy_status in {"recommended", "required"}:
            if not subagent_strategy.get("trigger"):
                blocks.append("subagent_strategy trigger is required when status is recommended or required")
            if not subagent_strategy.get("parallelism") or subagent_strategy.get("parallelism") == "none":
                blocks.append("subagent_strategy parallelism is required when subagents are recommended or required")
            if not strategy_roles:
                blocks.append("subagent_strategy roles are required when status is recommended or required")
            if strategy_authorization not in {"requires_user_permission", "approved"}:
                blocks.append("subagent_strategy must require user permission or be approved before delegated execution")
            if not strategy_join_policy or strategy_join_policy == "none":
                blocks.append("subagent_strategy join_policy is required when subagents are recommended or required")
            if not subagent_strategy.get("permission_prompt"):
                blocks.append("subagent_strategy permission_prompt is required when subagents are recommended or required")
            receipt_requirements = {
                str(item)
                for item in subagent_strategy.get("receipt_requirements", []) or []
                if isinstance(item, str)
            }
            missing_native_receipts = sorted(NATIVE_RECEIPT_REQUIRED_FIELDS - receipt_requirements)
            if missing_native_receipts:
                blocks.append(
                    "subagent_strategy.receipt_requirements missing native receipt fields: "
                    + ", ".join(missing_native_receipts)
                )
            known_step_ids = {step.get("step_id") for step in steps if isinstance(step, dict)}
            for role in strategy_roles:
                if not isinstance(role, dict):
                    blocks.append("subagent_strategy.roles entries must be objects")
                    continue
                role_id = role.get("role_id", "<unknown-role>")
                for step_ref in role.get("applies_to_steps", []) or []:
                    if step_ref not in known_step_ids:
                        blocks.append(f"subagent_strategy:{role_id}: applies_to_steps references unknown step_id '{step_ref}'")
        if strategy_status == "blocked" and strategy_authorization != "blocked":
            flags.append("blocked subagent_strategy should use authorization=blocked")

    validate_subagent_lifecycle(subagent_strategy, subagent_lifecycle, blocks, flags)
    validate_command_interface_gates(doc, gates, blocks)
    validate_native_stage_receipts(doc, steps, gates, blocks, flags)

    all_technique_ids = {
        technique_id(value)[0]
        for _, value in iter_techniques(doc)
        if technique_id(value)[0]
    }
    if "route_menu" in all_technique_ids and not doc.get("route_menu"):
        flags.append("route_menu technique cited but dispatch.route_menu is missing")
    boundary_techniques = all_technique_ids & BOUNDARY_EVIDENCE_TECHNIQUES
    if boundary_techniques and not boundary_evidence:
        flags.append("boundary/evidence technique cited but dispatch.boundary_evidence is missing")

    gate_text = " ".join(
        str(gate.get("condition", "")) for gate in gates if isinstance(gate, dict)
    ).lower()
    guardrail_text = " ".join(str(item) for item in doc.get("promotion_guardrails", []) or []).lower()
    combined_guardrail_text = f"{gate_text} {guardrail_text}"
    for term in PROMOTION_AUTHORITY_TERMS:
        if term in combined_guardrail_text and "not " not in combined_guardrail_text[max(0, combined_guardrail_text.find(term) - 16):combined_guardrail_text.find(term)]:
            blocks.append(f"promotion authority appears to be claimed: {term}")

    if boundary_evidence:
        for boundary in boundary_evidence.get("boundaries", []) or []:
            if not isinstance(boundary, dict):
                blocks.append("boundary_evidence.boundaries entries must be objects")
                continue
            boundary_id = boundary.get("boundary_id", "<unknown-boundary>")
            for step_ref in boundary.get("applies_to_steps", []) or []:
                if step_ref not in step_ids:
                    blocks.append(f"boundary:{boundary_id}: applies_to_steps references unknown step_id '{step_ref}'")

        if "state_namespace_boundary" in boundary_techniques and not boundary_evidence.get("state_namespaces"):
            flags.append("state_namespace_boundary technique cited but boundary_evidence.state_namespaces is missing")
        if "memory_promotion_split" in boundary_techniques and not boundary_evidence.get("promotion_splits"):
            flags.append("memory_promotion_split technique cited but boundary_evidence.promotion_splits is missing")
        if "execution_receipt_handoff" in boundary_techniques and not boundary_evidence.get("receipts"):
            flags.append("execution_receipt_handoff technique cited but boundary_evidence.receipts is missing")

        for split in boundary_evidence.get("promotion_splits", []) or []:
            if not isinstance(split, dict):
                blocks.append("boundary_evidence.promotion_splits entries must be objects")
                continue
            source = str(split.get("source", "")).lower()
            target = str(split.get("target", "")).lower()
            rule = str(split.get("rule", "")).lower()
            on_violation = split.get("on_violation")
            source_claims_execution = any(term in source for term in EXECUTION_EVIDENCE_SOURCES)
            target_claims_canonical = any(term in target for term in CANONICAL_PROMOTION_TARGETS)
            rule_allows_direct_promotion = (
                ("direct" in rule or "without review" in rule or "automatically" in rule)
                and "requires" not in rule
                and "not " not in rule
            )
            if source_claims_execution and target_claims_canonical and rule_allows_direct_promotion:
                blocks.append("promotion split violation: execution evidence cannot directly promote canonical knowledge")
            if source_claims_execution and target_claims_canonical and on_violation != "block":
                flags.append("promotion split from execution evidence to canonical knowledge should block on violation")

    used_technique_ids: set[str] = set()
    step_technique_ids: set[str] = set()
    overlay_technique_ids: set[str] = set()
    haystack = technique_usage_haystack(doc)
    for location, value in iter_techniques(doc):
        tid, source, validation_note = technique_id(value)
        if not tid:
            blocks.append(f"{location}: invalid technique reference")
            continue
        used_technique_ids.add(tid)
        if location.startswith("step:"):
            step_technique_ids.add(tid)
        if location.startswith("overlay:"):
            overlay_technique_ids.add(tid)
        if tid not in known_techniques:
            if source != "local-extension":
                blocks.append(f"{location}: unknown technique '{tid}' must use source=local-extension")
            if not validation_note:
                blocks.append(f"{location}: local-extension technique '{tid}' requires validation_note")

    dispatch_level = [technique_id(value)[0] for value in doc.get("techniques", []) or []]
    for tid in filter(None, dispatch_level):
        reflected = (
            tid in haystack
            or tid.replace("_", " ") in haystack
            or tid.replace("_", "-") in haystack
            or tid in step_technique_ids
            or tid in overlay_technique_ids
        )
        if tid == doc.get("mode"):
            reflected = True
        if tid == "observability_grouping" and obs.get("signal_grouping"):
            reflected = True
        if tid in BOUNDARY_EVIDENCE_TECHNIQUES and boundary_evidence:
            reflected = True
        if tid == "role_projection_boundary" and subagent_strategy:
            reflected = True
        if not reflected and tid not in {"mandatory_component", "minimum_component_catalog", "data_quality_conformity"}:
            flags.append(f"dispatch-level technique '{tid}' is cited but not reflected in steps, gates, or observability")

    if not used_technique_ids:
        flags.append("dispatch cites no techniques")

    for overlay in doc.get("technique_overlays", []) or []:
        if not isinstance(overlay, dict):
            blocks.append("technique_overlays entries must be objects")
            continue
        overlay_id = overlay.get("overlay_id", "<unknown-overlay>")
        if not overlay.get("trigger"):
            flags.append(f"overlay:{overlay_id}: missing trigger")
        if not overlay.get("applies_to_steps"):
            flags.append(f"overlay:{overlay_id}: missing applies_to_steps")
        if not overlay.get("validation_expectation"):
            flags.append(f"overlay:{overlay_id}: missing validation_expectation")

    if blocks:
        return "block", blocks, flags
    if flags:
        return "flag", blocks, flags
    return "pass", blocks, flags


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an Arcanum dispatch document.")
    parser.add_argument("dispatch", type=Path, help="Path to dispatch JSON document")
    parser.add_argument("--schema", type=Path, default=SCHEMA_PATH)
    parser.add_argument("--catalog", type=Path, default=CATALOG_PATH)
    parser.add_argument("--json", action="store_true", help="Emit JSON result")
    args = parser.parse_args()

    doc = load_json(args.dispatch)
    schema = load_schema(args.schema)
    known = catalog_ids(args.catalog)
    status, blocks, flags = validate(doc, schema, known)

    if args.json:
        print(json.dumps({"validation": status, "blocks": blocks, "flags": flags}, indent=2))
    else:
        print(f"VALIDATION={status}")
        print(f"DISPATCH={args.dispatch}")
        for block in blocks:
            print(f"BLOCK: {block}")
        for flag in flags:
            print(f"FLAG: {flag}")

    return 0 if status in {"pass", "flag"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
