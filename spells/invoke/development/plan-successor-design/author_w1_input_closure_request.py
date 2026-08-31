#!/usr/bin/env python3
"""Author the complete Plan-successor Design W1 closure request from Boundary V2."""

from __future__ import annotations

import argparse
import copy
import fnmatch
import hashlib
import json
import re
from pathlib import Path
from typing import Any


EPOCH = "2026-08-28-plan-successor-design-boundary-v2"
TARGET = "invoke:plan-successor:definition-target"
OWNER = "owner:user"
BASE = "arcanum/spells/invoke/development/plan-successor-design"


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def slug(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return normalized[-72:] or "input"


def file_ref(path: str, schema_id: str | None = None, version: str | None = None) -> dict[str, Any]:
    return {
        "path": path,
        "visibility": "public",
        "expected_schema_id": schema_id,
        "expected_schema_version": version,
    }


def owner_for(path: str) -> str:
    routes = (
        ("arcanum/transmutations/implementation-layering/", "implementation-layering-owner"),
        ("arcanum/spells/work-pack-readiness-audit/", "work-pack-readiness-audit-owner"),
        ("arcanum/spells/implementation-readiness/", "implementation-readiness-owner"),
        ("arcanum/arcana/task-session/", "task-session-owner"),
        ("arcanum/transmutations/context-builder/", "context-builder-owner"),
        ("arcanum/formulae/dispatch-spec/", "dispatch-spec-owner"),
        ("arcanum/spells/goal/", "goal-owner"),
        ("arcanum/arcana/signal-observer/", "signal-observer-owner"),
    )
    for prefix, owner in routes:
        if path.startswith(prefix):
            return owner
    return "invoke-plan-owner"


def authority_class(kind: str) -> str:
    return {
        "current-implementation": "observed-current-state",
        "quality-constraint": "observed-current-state",
        "architecture-pattern": "advisory",
    }.get(kind, "normative")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--boundary", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    output = args.output.resolve()
    if output.exists() or output.is_symlink():
        raise ValueError("--output must be absent")
    boundary = load(args.boundary)
    if boundary["target_id"] != TARGET or boundary["approved_by"] != OWNER:
        raise ValueError("boundary does not bind the approved Plan-successor target and owner")

    roots = {item["root_id"]: item for item in boundary["roots"]}
    matches: dict[str, tuple[str, str]] = {}
    for rule in boundary["discovery_rules"]:
        root_binding = roots[rule["root_id"]]
        root_path = root / root_binding["path"]
        matched: list[str] = []
        for child in sorted(root_path.rglob("*")):
            if child.is_symlink():
                raise ValueError(f"symlink inside boundary: {child}")
            if not child.is_file():
                continue
            relative = child.relative_to(root_path).as_posix()
            if any(fnmatch.fnmatchcase(relative, pattern) for pattern in rule["include_globs"]):
                matched.append(f"{root_binding['path'].rstrip('/')}/{relative}")
        if not matched:
            raise ValueError(f"empty discovery rule: {rule['rule_id']}")
        for path in matched:
            if path in matches:
                raise ValueError(f"ambiguous discovery path: {path}")
            matches[path] = (rule["rule_id"], rule["input_class"])

    input_catalog: list[dict[str, Any]] = []
    path_to_id: dict[str, str] = {}
    evidence_paths: list[dict[str, str]] = []
    for index, (path, (rule_id, kind)) in enumerate(sorted(matches.items())):
        input_id = f"input:{index:03d}:{slug(path)}"
        path_to_id[path] = input_id
        input_catalog.append({
            "input_id": input_id,
            "kind": kind,
            "authority_class": authority_class(kind),
            "authority_owner": owner_for(path),
            "applicability_owner": OWNER,
            "classification": "required",
            "selector": f"file:{path}",
            "source_ref": file_ref(path),
            "freshness": {"status": "current", "observed_epoch": EPOCH},
            "applies_to": ["invoke-plan-successor-design"],
            "exclusion_evidence_ref": None,
        })
        evidence_paths.append({"pointer": f"/input_catalog/{index}/source_ref", "path": path})

    def pick(*suffixes: str) -> tuple[str, str]:
        candidates = [path for path in path_to_id if any(path.endswith(suffix) for suffix in suffixes)]
        if not candidates:
            raise ValueError(f"missing representative input for {suffixes}")
        selected = sorted(candidates)[0]
        return path_to_id[selected], f"file:{selected}"

    define_id, define_selector = pick("plan-successor-define/bundle-v4/DEFINITIONS.json")
    plan_md_id, plan_md_selector = pick("spells/invoke/plan.md")
    boundary_doc_id, boundary_doc_selector = pick("PLAN-ARTIFACT-BOUNDARIES.md")
    plan_schema_id, plan_schema_selector = pick("plan-execution-source-v1.schema.json")
    compiler_id, compiler_selector = pick("compile_plan_execution_source.py")
    wpra_id, wpra_selector = pick("work-pack-readiness-audit/README.md")
    readiness_id, readiness_selector = pick("implementation-readiness/README.md")
    task_id, task_selector = pick("task-session/README.md")
    context_id, context_selector = pick("context-builder/README.md")
    dispatch_id, dispatch_selector = pick("dispatch-spec/README.md")
    goal_id, goal_selector = pick("spells/goal/README.md")
    observer_id, observer_selector = pick("signal-observer/README.md")
    distill_id, distill_selector = pick("distill-execution-receipt-v1.schema.json")
    test_id, test_selector = pick("test_plan_execution_source.py")
    template_id, template_selector = pick("templates/work-pack.md")

    decision_path = f"{BASE}/PLAN-SUCCESSOR-DESIGN-OWNER-DECISION.json"
    no_prior_path = f"{BASE}/NO-PRIOR-DESIGN.json"
    approval_path = root.joinpath(args.boundary.resolve().relative_to(root)).as_posix()
    if approval_path.startswith(root.as_posix() + "/"):
        approval_path = approval_path[len(root.as_posix()) + 1:]
    stage_path = "arcanum/spells/invoke/development/plan-successor-define/bundle-v4/INVOKE-DEFINE-STAGE-RECEIPT.json"
    admission_path = "arcanum/spells/invoke/development/plan-successor-define/DEFINE-BUNDLE-ADMISSION-RECEIPT-4.json"
    manifest_schema_path = "arcanum/spells/invoke/schemas/design-scope-manifest.schema.json"

    discovery_boundary = {
        "observation_epoch": boundary["observation_epoch"],
        "roots": [{"root_id": item["root_id"], "path": item["path"]} for item in boundary["roots"]],
        "discovery_rules": copy.deepcopy(boundary["discovery_rules"]),
        "required_input_classes": copy.deepcopy(boundary["required_input_classes"]),
        "permitted_exclusions": copy.deepcopy(boundary["permitted_exclusions"]),
        "boundary_digest": boundary["boundary_digest"],
    }
    for index, item in enumerate(discovery_boundary["roots"]):
        evidence_paths.append({"pointer": f"/discovery_boundary/roots/{index}", "path": item["path"], "kind": "directory"})

    all_concerns = [
        ("authority", True, "required", define_id, define_selector, "authority-owner", "architecture-owner", "The successor changes which artifact owns Plan meaning and must preserve the owner decision and authority ceiling."),
        ("security", False, "not-applicable-with-rationale", define_id, define_selector, "security-risk-owner", "architecture-owner", "No authentication, authorization transport, credential, or security boundary is introduced by this local authoring contract."),
        ("state-event", True, "required", task_id, task_selector, "workflow-owner", "architecture-owner", "Plan tasks, waves, gates, blockers, and terminal handoff states require explicit transition rules."),
        ("persistence", True, "required", compiler_id, compiler_selector, "persistence-owner", "architecture-owner", "The compiler and admission steps create exact absent outputs and must define writer ownership and collision behavior."),
        ("failure", True, "required", readiness_id, readiness_selector, "workflow-owner", "architecture-owner", "Blocked prerequisites and failed validation must stop before implementation authority is inferred."),
        ("reliability", True, "required", test_id, test_selector, "service-owner", "architecture-owner", "The source-to-view chain must replay deterministically and expose stale or incomplete consumer evidence."),
        ("integration", True, "required", wpra_id, wpra_selector, "interface-owner", "architecture-owner", "The Design must close the interfaces to readiness, task execution, context, dispatch, goal, and observation consumers."),
        ("migration", True, "required", boundary_doc_id, boundary_doc_selector, "migration-owner", "architecture-owner", "The successor must replace Work-Pack-as-source wording without rewriting historical artifacts or hiding the compatibility boundary."),
        ("rollout", False, "not-applicable-with-rationale", define_id, define_selector, "release-owner", "architecture-owner", "This Design authors local governed artifacts and performs no runtime activation, publication, deployment, or release."),
        ("privacy-data", False, "not-applicable-with-rationale", define_id, define_selector, "data-owner", "architecture-owner", "The bounded source contains repository planning evidence and introduces no personal-data collection or retention sink."),
        ("performance", False, "not-applicable-with-rationale", test_id, test_selector, "service-owner", "architecture-owner", "No runtime latency or throughput claim is made; deterministic correctness is the required quality property."),
        ("ux", False, "not-applicable-with-rationale", template_id, template_selector, "ux-plan-owner", "ux-plan-owner", "The generated Markdown is a coordinator view with no new interactive surface or changed human navigation contract."),
        ("validation", True, "required", plan_schema_id, plan_schema_selector, "design-owner", "plan-work-pack-owner", "Every source, generated view, predecessor binding, and downstream readiness claim requires machine validation."),
    ]
    authored_concerns = []
    predicate_inputs = []
    for primary, required, disposition, source_id, selector, accountable, artifact_owner, rationale in all_concerns:
        concern_id = f"authored:{primary}"
        authored_concerns.append({
            "concern_id": concern_id,
            "primary_class": primary,
            "disposition": disposition,
            "required_predicate": required,
            "evidence_selectors": [selector],
            "ownership": {
                "accountable_owner": accountable,
                "contributing_owners": ["architecture-owner", "plan-work-pack-owner"],
                "artifact_owner": artifact_owner,
                "validator_owner": "invoke-design-selection-validator",
            },
            "selected": required,
            "rationale": rationale,
            "revisit_condition": None,
        })
        predicate_inputs.append({
            "predicate_id": f"predicate:{primary}",
            "concern_id": concern_id,
            "source_input_ids": [source_id],
            "expected": required,
        })

    scope_signals = {
        "human_actors": [],
        "rendered_surfaces": [],
        "interfaces": [
            {"signal_id": "signal:define-admission-interface", "source_input_id": define_id, "interface_id": "interface:define-to-design", "kind": "admitted-artifact", "peer": "Invoke Define v3", "direction": "inbound", "contract_ref": stage_path},
            {"signal_id": "signal:wpra-interface", "source_input_id": wpra_id, "interface_id": "interface:plan-to-wpra", "kind": "readiness-consumer", "peer": "Work Pack Readiness Audit", "direction": "outbound", "contract_ref": wpra_selector},
            {"signal_id": "signal:readiness-interface", "source_input_id": readiness_id, "interface_id": "interface:plan-to-readiness", "kind": "readiness-consumer", "peer": "Implementation Readiness", "direction": "outbound", "contract_ref": readiness_selector},
            {"signal_id": "signal:task-interface", "source_input_id": task_id, "interface_id": "interface:plan-to-task-session", "kind": "execution-consumer", "peer": "Task Session", "direction": "outbound", "contract_ref": task_selector},
            {"signal_id": "signal:context-interface", "source_input_id": context_id, "interface_id": "interface:plan-to-context-builder", "kind": "context-consumer", "peer": "Context Builder", "direction": "outbound", "contract_ref": context_selector},
            {"signal_id": "signal:dispatch-interface", "source_input_id": dispatch_id, "interface_id": "interface:plan-to-dispatch", "kind": "dispatch-consumer", "peer": "Dispatch Spec", "direction": "outbound", "contract_ref": dispatch_selector},
            {"signal_id": "signal:goal-interface", "source_input_id": goal_id, "interface_id": "interface:plan-to-goal", "kind": "execution-consumer", "peer": "Goal", "direction": "outbound", "contract_ref": goal_selector},
            {"signal_id": "signal:observer-interface", "source_input_id": observer_id, "interface_id": "interface:plan-to-observer", "kind": "observation-consumer", "peer": "Signal Observer", "direction": "outbound", "contract_ref": observer_selector},
            {"signal_id": "signal:distill-v1-interface", "source_input_id": distill_id, "interface_id": "interface:design-to-distill-v1", "kind": "evidence-contract", "peer": "Distill v1", "direction": "outbound", "contract_ref": distill_selector},
        ],
        "stores": [],
        "queues": [],
        "writers": [
            {"signal_id": "signal:plan-bundle-writer", "source_input_id": compiler_id, "writer_id": "writer:plan-bundle", "targets": ["canonical Plan JSON bundle", "generated WORK-PACK.md view"], "concurrency": "Absent outputs only; refuse overwrite or concurrent publication."}
        ],
        "normative_rules": [
            {"signal_id": "signal:source-authority-rule", "source_input_id": define_id, "rule_id": "rule:single-plan-source", "verb": "admit", "subject": "Plan successor", "object": "one canonical JSON source as the sole meaning-bearing Plan source", "enforcement_hint": "Reject generated views or lifecycle receipts as authored source fields."},
            {"signal_id": "signal:terminal-state-rule", "source_input_id": task_id, "rule_id": "rule:terminal-plan-handoff", "verb": "preserve terminal state", "subject": "Plan handoff", "object": "typed blockers, gates, and one selected execution-entry boundary", "enforcement_hint": "Block execution when required readiness evidence is absent or stale."},
            {"signal_id": "signal:consumer-closure-rule", "source_input_id": wpra_id, "rule_id": "rule:all-plan-consumers", "verb": "validate", "subject": "Plan admission", "object": "every declared readiness and execution consumer", "enforcement_hint": "Run the exact consumer contracts against the staged bundle before PASS."}
        ],
        "effects": [
            {"signal_id": "signal:no-product-effect", "source_input_id": define_id, "effect_id": "effect:author-plan-artifacts", "reversible": True, "external": False, "privileged": False},
            {"signal_id": "signal:no-execution-effect", "source_input_id": readiness_id, "effect_id": "effect:implementation-execution", "reversible": False, "external": False, "privileged": False}
        ],
        "data_and_log_sinks": [],
        "deployment_targets": [],
        "compatibility_boundaries": [
            {"signal_id": "signal:plan-source-migration", "source_input_id": boundary_doc_id, "boundary_id": "compatibility:work-pack-source", "old_contract": "stored WORK-PACK.md is described as the Plan source of truth", "new_contract": "stored canonical JSON Plan source owns meaning and WORK-PACK.md is generated"}
        ],
        "quality_claims": [],
        "acceptance_and_readiness_claims": [
            {"signal_id": "signal:w1-closure-claim", "source_input_id": test_id, "claim_id": "claim:w1-input-closure", "selector": test_selector, "evidence_state": "authored-complete"}
        ],
    }

    document = {
        "authored_by": OWNER,
        "target": {
            "id": TARGET,
            "title": "Invoke Plan successor architecture",
            "objective": "Design the canonical JSON-first Plan source, deterministic generated views, exact admission boundary, and complete readiness and execution consumer contracts without revising the admitted definitions.",
            "owner": OWNER,
            "visibility": "public",
        },
        "activation": {
            "kind": "normal",
            "define_stage_receipt_ref": file_ref(stage_path),
            "define_admission_receipt_ref": file_ref(admission_path),
            "approval_ref": file_ref(approval_path, "https://arcanum.dev/schemas/invoke/design-input-boundary-approval/v1", "invoke.design-input-boundary-approval.v1"),
        },
        "discovery_boundary": discovery_boundary,
        "scope_manifest_contract_ref": file_ref(manifest_schema_path, "https://arcanum.dev/schemas/invoke/design-scope-manifest/1-0-0", "1.0.0"),
        "input_catalog": input_catalog,
        "conditional_input_resolutions": [],
        "constraints": [
            {"obligation_id": "constraint:preserve-admitted-define", "class": "constraint", "statement": "Design must bind the exact admitted Define v4 stage and admission and must not revise its meanings.", "source_input_ids": [define_id], "owner": "invoke-plan-owner"},
            {"obligation_id": "constraint:distill-v1-only", "class": "constraint", "statement": "Design evidence must use the four pinned Distill v1 schemas and must not consume concurrent Distill v2 material.", "source_input_ids": [distill_id], "owner": "invoke-design-owner"},
            {"obligation_id": "constraint:no-execution-authority", "class": "constraint", "statement": "Design outputs may describe implementation work but cannot select, accept, execute, publish, or deploy it.", "source_input_ids": [readiness_id, task_id], "owner": "authority-owner"}
        ],
        "invariants": [
            {"obligation_id": "invariant:single-json-source", "class": "invariant", "statement": "Exactly one canonical JSON Plan source owns meaning; every Markdown coordinator artifact is derived.", "source_input_ids": [define_id, plan_schema_id], "owner": "invoke-plan-owner"},
            {"obligation_id": "invariant:deterministic-atomic-bundle", "class": "invariant", "statement": "Compilation is deterministic, writes only to absent outputs, and admission independently replays and byte-compares the bundle.", "source_input_ids": [compiler_id, test_id], "owner": "invoke-plan-owner"},
            {"obligation_id": "invariant:consumer-complete", "class": "invariant", "statement": "A new Plan PASS requires current evidence from every declared readiness, task, context, dispatch, goal, and observation consumer.", "source_input_ids": [wpra_id, readiness_id, task_id, context_id, dispatch_id, goal_id, observer_id], "owner": "invoke-plan-owner"}
        ],
        "prior_decisions": [
            {"decision_id": "decision:plan-successor-json-source", "status": "preserved", "owner": OWNER, "decision_ref": file_ref(decision_path)},
            {"decision_id": "decision:legacy-work-pack-source-wording", "status": "eligible-for-supersession", "owner": OWNER, "decision_ref": file_ref(decision_path)}
        ],
        "exclusions": [],
        "design_kind": {"kind": "greenfield", "no_prior_design_determination_ref": file_ref(no_prior_path)},
        "selection_inputs": {
            "authored_concerns": authored_concerns,
            "predicate_inputs": predicate_inputs,
            "planned_witness_requirements": [
                {"witness_id": "witness:deterministic-replay", "claim_id": "claim:deterministic-plan-bundle", "concern_id": "authored:reliability", "evidence_state": "planned-contract"},
                {"witness_id": "witness:consumer-rehearsal", "claim_id": "claim:complete-consumer-closure", "concern_id": "authored:integration", "evidence_state": "planned-contract"},
                {"witness_id": "witness:migration-compatibility", "claim_id": "claim:work-pack-generated-view", "concern_id": "authored:migration", "evidence_state": "planned-contract"},
                {"witness_id": "witness:distill-v1", "claim_id": "claim:distill-v1-evidence", "concern_id": "authored:validation", "evidence_state": "planned-contract"}
            ],
        },
        "input_conflicts": [
            {"conflict_id": "conflict:plan-source-authority", "input_ids": [define_id, plan_md_id, boundary_doc_id], "resolution_status": "resolved", "decision_ref": file_ref(decision_path)}
        ],
        "scope_signals": scope_signals,
    }

    for pointer, path in (
        ("/activation/define_stage_receipt_ref", stage_path),
        ("/activation/define_admission_receipt_ref", admission_path),
        ("/activation/approval_ref", approval_path),
        ("/scope_manifest_contract_ref", manifest_schema_path),
        ("/prior_decisions/0/decision_ref", decision_path),
        ("/prior_decisions/1/decision_ref", decision_path),
        ("/design_kind/no_prior_design_determination_ref", no_prior_path),
        ("/input_conflicts/0/decision_ref", decision_path),
    ):
        evidence_paths.append({"pointer": pointer, "path": path})

    request = {
        "$schema": "https://arcanum.dev/schemas/invoke/design-input-closure-v2-authoring-request/v1",
        "schema_version": "invoke.cli-authoring-request.v1",
        "mode": "design",
        "stage": "input-closure",
        "document": document,
        "evidence_paths": evidence_paths,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": output.as_posix(), "discovered_files": len(input_catalog), "evidence_bindings": len(evidence_paths)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
