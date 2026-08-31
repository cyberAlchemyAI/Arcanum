#!/usr/bin/env python3
"""Create the W1 V6 author bound to the repaired evidence model."""

from __future__ import annotations

import argparse
from pathlib import Path


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise ValueError(f"expected one source fragment, found {count}: {old[:100]}")
    return text.replace(old, new)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists() or args.output.is_symlink():
        raise ValueError("--output must be absent")
    text = args.source.read_text(encoding="utf-8")

    replacements = [
        (
            'EPOCH = "2026-08-28-plan-successor-design-boundary-v5-snapshot"',
            'EPOCH = "2026-08-28-plan-successor-design-boundary-v6-evidence-repair"',
        ),
        (
            'PLAN-SUCCESSOR-DESIGN-OWNER-DECISION-V5.json',
            'PLAN-SUCCESSOR-DESIGN-OWNER-DECISION-V6.json',
        ),
        ('NO-PRIOR-DESIGN-V5.json', 'NO-PRIOR-DESIGN-V6.json'),
        (
            '    context_id, context_selector = pick("context-builder/README.md")\n',
            '    context_id, context_selector = pick("context-builder/README.md")\n'
            '    context_schema_id, context_schema_selector = pick("materials/root-context-builder/schemas/native-context-admission-projection-v1.schema.json")\n'
            '    task_version_id, task_version_selector = pick("materials/root-task-session/scripts/task-session-governance-runner.py")\n',
        ),
        (
            '("integration", True, "required", wpra_id, wpra_selector, "interface-owner", "architecture-owner", "The Design must close the interfaces to readiness, task execution, context, dispatch, goal, and observation consumers."),',
            '("integration", True, "required", wpra_id, wpra_selector, "interface-owner", "architecture-owner", "The Design must close every applicable machine-backed readiness and execution consumer while recording Signal Observer as a conditional machine-contract gap."),',
        ),
        (
            '("ux", False, "not-applicable-with-rationale", template_id, template_selector, "ux-plan-owner", "ux-plan-owner", "The generated Markdown is a coordinator view with no new interactive surface or changed human navigation contract."),',
            '("ux", True, "required", template_id, template_selector, "ux-plan-owner", "ux-plan-owner", "The generated WORK-PACK.md changes how a plan coordinator finds tasks, waves, gates, blockers, and the next eligible action, so its readable navigation contract requires design and validation."),',
        ),
        (
            '        "human_actors": [],\n        "rendered_surfaces": [],',
            '        "human_actors": [\n'
            '            {"signal_id": "signal:plan-coordinator", "source_input_id": template_id, "actor_id": "actor:plan-coordinator", "natural_person": True, "reads": True, "decides": True, "acts": True, "recovers": True, "navigates": True, "assistive_operation": False, "surfaces": ["surface:generated-work-pack"]}\n'
            '        ],\n'
            '        "rendered_surfaces": [\n'
            '            {"signal_id": "signal:generated-work-pack-surface", "source_input_id": template_id, "surface_id": "surface:generated-work-pack", "modality": "text", "semantic_contract_ref": "contract:generated-work-pack-navigation", "semantic_change": "changed"}\n'
            '        ],',
        ),
        (
            '{"signal_id": "signal:observer-interface", "source_input_id": observer_id, "interface_id": "interface:plan-to-observer", "kind": "observation-consumer", "peer": "Signal Observer", "direction": "outbound", "contract_ref": observer_selector},',
            '{"signal_id": "signal:observer-interface", "source_input_id": observer_id, "interface_id": "interface:plan-to-observer", "kind": "conditional-observation-gap", "peer": "Signal Observer", "direction": "outbound", "contract_ref": observer_selector},',
        ),
        (
            '{"signal_id": "signal:consumer-closure-rule", "source_input_id": wpra_id, "rule_id": "rule:all-plan-consumers", "verb": "validate", "subject": "Plan admission", "object": "every declared readiness and execution consumer", "enforcement_hint": "Run the exact consumer contracts against the staged bundle before PASS."}',
            '{"signal_id": "signal:consumer-closure-rule", "source_input_id": wpra_id, "rule_id": "rule:all-machine-backed-plan-consumers", "verb": "validate", "subject": "Plan admission", "object": "every applicable machine-contract-backed readiness and execution consumer", "enforcement_hint": "Run the exact consumer contracts against the staged bundle before PASS; report consumers without machine contracts as gaps."},\n'
            '            {"signal_id": "signal:native-context-version-rule", "source_input_id": context_schema_id, "rule_id": "rule:native-context-version-by-transients", "verb": "select version", "subject": "native-context admission projection", "object": "1.2.0 when transient outputs are absent and 1.3.0 when the declared transient-output set is nonempty", "enforcement_hint": "Derive the version from the exact execution contract and reject a mismatched projection."},\n'
            '            {"signal_id": "signal:observer-gap-rule", "source_input_id": observer_id, "rule_id": "rule:observer-machine-contract-required", "verb": "block closure claim", "subject": "Signal Observer integration", "object": "machine admission until a schema, deterministic projector or validator, and no-append fixture exist", "enforcement_hint": "Preserve the observer requirement as a conditional gap and never count README or skill prose as machine closure."}',
        ),
        (
            '{"obligation_id": "invariant:consumer-complete", "class": "invariant", "statement": "A new Plan PASS requires current evidence from every declared readiness, task, context, dispatch, goal, and observation consumer.", "source_input_ids": [wpra_id, readiness_id, task_id, context_id, dispatch_id, goal_id, observer_id], "owner": "invoke-plan-owner"}',
            '{"obligation_id": "invariant:machine-consumer-complete", "class": "invariant", "statement": "A new Plan PASS requires current machine-contract evidence from every applicable readiness, task, context, dispatch, and goal consumer.", "source_input_ids": [wpra_id, readiness_id, task_id, context_id, dispatch_id, goal_id], "owner": "invoke-plan-owner"},\n'
            '            {"obligation_id": "invariant:observer-gap-visible", "class": "invariant", "statement": "Signal Observer remains a conditional integration gap until a machine schema, deterministic projector or validator, and no-append fixture are admitted; prose alone cannot establish closure.", "source_input_ids": [observer_id], "owner": "signal-observer-owner"},\n'
            '            {"obligation_id": "invariant:native-context-version-selection", "class": "invariant", "statement": "Native-context version is 1.2.0 when no transient outputs are declared and 1.3.0 when the transient-output set is nonempty.", "source_input_ids": [context_schema_id, task_version_id], "owner": "context-builder-owner"}',
        ),
        (
            '{"witness_id": "witness:consumer-rehearsal", "claim_id": "claim:complete-consumer-closure", "concern_id": "authored:integration", "evidence_state": "planned-contract"},',
            '{"witness_id": "witness:consumer-rehearsal", "claim_id": "claim:machine-consumer-closure", "concern_id": "authored:integration", "evidence_state": "planned-contract"},\n'
            '                {"witness_id": "witness:work-pack-navigation", "claim_id": "claim:generated-work-pack-readable-navigation", "concern_id": "authored:ux", "evidence_state": "planned-contract"},\n'
            '                {"witness_id": "witness:native-context-version", "claim_id": "claim:native-context-version-derived-from-transients", "concern_id": "authored:validation", "evidence_state": "planned-contract"},',
        ),
        (
            '"objective": "Design the canonical JSON-first Plan source, deterministic generated views, exact admission boundary, and complete readiness and execution consumer contracts without revising the admitted definitions.",',
            '"objective": "Design the canonical JSON-first Plan source, deterministic generated views, exact admission boundary, complete machine-backed readiness and execution consumer contracts, and explicit gaps for consumers that lack machine contracts without revising the admitted definitions.",',
        ),
    ]
    for old, new in replacements:
        text = replace_once(text, old, new)

    # Ensure both exact machine-evidence selectors remain used by the generated source.
    text = replace_once(
        text,
        '    task_version_id, task_version_selector = pick("materials/root-task-session/scripts/task-session-governance-runner.py")\n',
        '    task_version_id, task_version_selector = pick("materials/root-task-session/scripts/task-session-governance-runner.py")\n'
        '    _ = (context_schema_selector, task_version_selector)\n',
    )
    args.output.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
