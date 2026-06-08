#!/usr/bin/env python3
"""Generate a Refine dispatch document from seed fields.

The generator is intentionally deterministic and local. It materializes the
canonical Refine dispatch template, records selected technique overlays, and can
optionally validate the result through dispatch-spec.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
TEMPLATE = ROOT / "arcana" / "refine" / "templates" / "refine-dispatch.json"
VALIDATOR = ROOT / "formulae" / "dispatch-spec" / "scripts" / "validate-dispatch.py"
DEFAULT_OVERLAY = "baseline_sequence"
ROUTE_MENU_BY_OVERLAY = {
    "baseline_sequence": "baseline_sequence",
    "route_menu_for_ambiguity": "baseline_sequence",
    "dialectic_for_tension": "tension_or_alternative_overlay",
    "tournament_for_alternatives": "tension_or_alternative_overlay",
    "xray_for_hidden_structure": "structure_or_test_overlay",
    "toy_game_for_low_cost_falsification": "structure_or_test_overlay",
    "memory_residue_for_context_recovery": "structure_or_test_overlay",
    "protected_context_for_external_or_sensitive_evidence": "structure_or_test_overlay",
}
SUBAGENT_ROLES_BY_OVERLAY = {
    "route_menu_for_ambiguity": [
        {
            "role_id": "route-choice-reviewer",
            "purpose": "Check that the route menu is bounded and that the selected route follows the user's intent.",
            "owns": "route ambiguity, missing choices, and approval checkpoint risks",
            "applies_to_steps": ["s01-context-builder", "s04-research-decision"],
        }
    ],
    "dialectic_for_tension": [
        {
            "role_id": "dialectic-critic",
            "purpose": "Preserve competing principles and objections before Refine synthesizes the route.",
            "owns": "stable disagreements, counterarguments, and unresolved residue",
            "applies_to_steps": ["s03-interrogation-review", "s07-interrogation-design-review", "s10-final-synthesis"],
        }
    ],
    "tournament_for_alternatives": [
        {
            "role_id": "alternative-comparator",
            "purpose": "Compare candidate abstractions or routes with Pareto and recomposition criteria.",
            "owns": "candidate comparison, rejected alternatives, and convergence criteria",
            "applies_to_steps": ["s05-distill", "s08-distill-repair", "s10-final-synthesis"],
        }
    ],
    "xray_for_hidden_structure": [
        {
            "role_id": "structure-explorer",
            "purpose": "Expose hidden components, relationships, and workflow boundaries.",
            "owns": "structure map, relationship risks, and explanation handles",
            "applies_to_steps": ["s01-context-builder", "s06-invoke-design", "s10-final-synthesis"],
        }
    ],
    "toy_game_for_low_cost_falsification": [
        {
            "role_id": "falsification-reviewer",
            "purpose": "Design a low-cost failure test for the selected abstraction before planning hardens it.",
            "owns": "toy-game evidence expectations and failure-to-repair route",
            "applies_to_steps": ["s08-distill-repair", "s09-invoke-plan"],
        }
    ],
    "memory_residue_for_context_recovery": [
        {
            "role_id": "memory-residue-reviewer",
            "purpose": "Recover relevant prior context while separating evidence from canonical promotion.",
            "owns": "memory handles, duplicate claims, and residue ownership",
            "applies_to_steps": ["s01-context-builder", "s03-interrogation-review", "s10-final-synthesis"],
        }
    ],
    "protected_context_for_external_or_sensitive_evidence": [
        {
            "role_id": "protected-context-reviewer",
            "purpose": "Check that external or sensitive evidence remains bounded and non-canonical without owner review.",
            "owns": "protected context labels, source boundaries, and promotion split risks",
            "applies_to_steps": ["s04-research-decision", "s10-final-synthesis"],
        }
    ],
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a REFINE-DISPATCH.json document.")
    parser.add_argument("--seed", type=Path, help="Optional seed JSON file.")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--target", default=None)
    parser.add_argument("--operator-request", default=None)
    parser.add_argument("--preset", default="standard")
    parser.add_argument("--research-mode", default="research-if-gap-appears")
    parser.add_argument("--overlay", action="append", default=[])
    parser.add_argument("--output", type=Path, help="Write generated dispatch to this path.")
    parser.add_argument("--validate", action="store_true", help="Validate generated dispatch after writing/printing.")
    return parser.parse_args()


def merge_seed(args: argparse.Namespace) -> dict[str, Any]:
    seed: dict[str, Any] = {}
    if args.seed:
        seed = load_json(args.seed)
    for key, attr in [
        ("run_id", "run_id"),
        ("target", "target"),
        ("operator_request", "operator_request"),
        ("preset", "preset"),
        ("research_mode", "research_mode"),
    ]:
        value = getattr(args, attr)
        if value is not None:
            seed[key] = value
    if args.overlay:
        seed["overlays"] = args.overlay
    return seed


def generate(seed: dict[str, Any]) -> dict[str, Any]:
    doc = load_json(TEMPLATE)
    available = {item["overlay_id"] for item in doc.get("technique_overlays", [])}
    overlays = seed.get("overlays") or [DEFAULT_OVERLAY]
    unknown = sorted(set(overlays) - available)
    if unknown:
        raise ValueError(f"unknown overlay id(s): {', '.join(unknown)}")

    run_id = seed.get("run_id") or "<run-id>"
    target = seed.get("target") or "<target>"
    operator_request = seed.get("operator_request") or f"refine {target}"
    preset = seed.get("preset") or "standard"
    research_mode = seed.get("research_mode") or "research-if-gap-appears"

    doc["dispatch_id"] = run_id
    doc["selected_technique_overlays"] = overlays
    doc["intent"]["raw"] = operator_request
    doc["intent"]["objective"] = f"Run the canonical Refine loop for {target} and produce RESULT.md."
    doc["intent"]["target_artifact"] = f"{target}/development/refinement-runs/{run_id}/RESULT.md"
    doc["intent"]["operator_sentence"] = operator_request
    doc["intent"]["preset"] = preset
    doc["intent"]["research_mode"] = research_mode
    doc["intent"]["arcanum_vocabulary"] = sorted(
        set(doc["intent"].get("arcanum_vocabulary", [])) | {"refine", "dispatch-spec", *overlays}
    )
    for receipt in doc.get("native_stage_receipts", []) or []:
        if isinstance(receipt, dict):
            receipt["dispatch_id"] = run_id

    selected_menu = "baseline_sequence"
    for overlay in overlays:
        selected_menu = ROUTE_MENU_BY_OVERLAY.get(overlay, selected_menu)
        if selected_menu != "baseline_sequence":
            break
    if isinstance(doc.get("route_menu"), dict):
        doc["route_menu"]["selected_item_id"] = selected_menu

    selected_roles: list[dict[str, Any]] = []
    for overlay in overlays:
        selected_roles.extend(SUBAGENT_ROLES_BY_OVERLAY.get(overlay, []))
    if selected_roles and isinstance(doc.get("subagent_strategy"), dict):
        role_ids = ", ".join(role["role_id"] for role in selected_roles)
        doc["subagent_strategy"].update(
            {
                "status": "recommended",
                "trigger": f"Selected overlays imply delegated review: {', '.join(overlays)}.",
                "explanation": f"Dispatch Spec recommends role-bound reviewers ({role_ids}) because the target context selected overlays that benefit from independent critique before native runtime-backed stage execution.",
                "context": [
                    f"Target: {target}",
                    f"Preset: {preset}",
                    f"Research mode: {research_mode}",
                    f"Selected overlays: {', '.join(overlays)}",
                ],
                "roles": selected_roles,
                "parallelism": "fanout" if len(selected_roles) > 1 else "none",
                "join_policy": "parent_synthesis",
                "authorization": "requires_user_permission",
                "permission_prompt": "Dispatch Spec recommends the listed subagent strategy for this refinement. Run these delegated reviewers before native runtime-backed stages?",
            }
        )
    elif isinstance(doc.get("subagent_strategy"), dict):
        doc["subagent_strategy"].update(
            {
                "status": "none",
                "trigger": "Only the baseline sequence overlay was selected.",
                "explanation": "Dispatch Spec does not recommend subagents for this route because the problem shape does not currently show tension, competing alternatives, hidden structure, memory recovery, protected context, or falsification risk.",
                "context": [
                    f"Target: {target}",
                    f"Preset: {preset}",
                    f"Research mode: {research_mode}",
                    f"Selected overlays: {', '.join(overlays)}",
                ],
                "roles": [],
                "parallelism": "none",
                "join_policy": "none",
                "authorization": "not_needed",
                "permission_prompt": "Dispatch Spec does not recommend subagents. Run the validated Refine route now?",
            }
        )

    doc["generation"] = {
        "generator": "arcana/refine/scripts/generate-refine-dispatch.py",
        "template": "arcana/refine/templates/refine-dispatch.json",
        "preset": preset,
        "research_mode": research_mode,
        "selected_overlays": overlays,
    }
    return doc


def main() -> int:
    args = parse_args()
    seed = merge_seed(args)
    try:
        doc = generate(seed)
    except ValueError as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 1

    rendered = json.dumps(doc, indent=2, sort_keys=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        dispatch_path = args.output
    else:
        print(rendered, end="")
        dispatch_path = None

    if args.validate:
        if dispatch_path is None:
            print("BLOCK: --validate requires --output so the validator has a stable file path", file=sys.stderr)
            return 1
        result = subprocess.run([sys.executable, str(VALIDATOR), str(dispatch_path)], cwd=ROOT)
        return result.returncode

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
