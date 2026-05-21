---
template_id: invoke.implementation-plan
template_type: implementation-plan
canonical_source: WORK-PACK.md
retired: true
applies_to:
  - historical-reference
required_inputs:
  - implementation_objective
  - source_design_refs
  - delivery_boundary
optional_inputs:
  - architecture_refs
  - implementation_layering_ref
  - work_pack_ref
  - execution_pack_ref
output_files:
  - IMPLEMENTATION-PLAN.md
status: retired
authority_level: invoke-local
promotion_evidence: []
promotion_decision: pending
validation_rules:
  - source design refs present
  - delivery slices mapped
  - implementation details present for medium/high execution tasks
  - smallest working units present for medium/high work-packs
  - validation strategy present
  - standalone companion handoffs recorded
validation_examples:
  - examples/passing.md
  - examples/missing-input.md
created_at: 2026-05-16
updated_at: 2026-05-16
---

# Retired Implementation Plan: {capability-name}

This template is retained only as historical scaffolding. New invoke plan work must use `WORK-PACK.md` as the executable plan and `IMPLEMENTATION-LAYERING.md` as the governance lens.

## Implementation Objective

{what must be delivered and why}

## Source Design References

| Ref ID | Source | Required | Notes |
| --- | --- | --- | --- |
| SD-001 | {path or decision} | yes or no | {notes} |

## Delivery Boundary

- Included: {included delivery}
- Excluded: {excluded delivery}
- Deferral rules: {what may be deferred}

## Delivery Slices

| Slice ID | Outcome | Dependencies | Validation |
| --- | --- | --- | --- |
| S-001 | {outcome} | {dependencies} | {validation check} |

## Dependency Plan

| Dependency | Needed By | Readiness | Risk |
| --- | --- | --- | --- |
| {dependency} | {slice} | ready, partial, or missing | {risk} |

## Layer Window

- Layering companion: [../implementation-layering.md](../implementation-layering.md)
- Selected start layer: {layer}
- Selected stop layer: {layer}
- Layer deferrals: {deferrals}

## Task Decomposition

| Task ID | Slice ID | Task | Done When |
| --- | --- | --- | --- |
| T-001 | S-001 | {task} | {completion check} |

## Implementation Detail Specs

Required for medium/high complexity execution tasks. Low complexity plans may keep these details inline when the task is self-evident.

| Task ID | Detail Status | Inputs | Outputs | Implementation Notes | Edge Cases | Validation Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| T-001 | complete, gap, or n/a | {inputs} | {outputs} | {algorithm, pseudocode, state transition, data flow, or concrete implementation steps} | {edge cases or failure modes} | {checks proving the intended implementation} |

Algorithmic or domain-logic tasks must describe purpose, inputs, outputs, data model or state, step-by-step algorithm or pseudocode, precedence/scoring/classification/transition rules, edge cases, failure modes, and acceptance checks. A task that only says to implement a bundle, component, or outcome is not execution-ready.

## Smallest Working Units

Required for medium/high work-packs. SWUs sit below tasks and identify the smallest executable implementation step that can be assigned and verified independently.

Shared manifest:

| SWU ID | Parent Task | Goal | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Verification Command | Execution Owner | Handoff Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-{FEATURE-CODE}-001 | T-001 | {small executable goal} | {task ids, SWU ids, or none} | {files, modules, or docs this SWU may change} | {conditions that make this SWU done} | {evidence required to accept the SWU} | {command or reviewable check} | subagent, local-fallback, or manual | {context a worker/subagent needs and expected return shape} |

Task-local mapping:

```markdown
## Smallest Working Units

- SWU-{FEATURE-CODE}-001: {goal}
- SWU-{FEATURE-CODE}-002: {goal}
```

Closure-only task exemption:

```markdown
## Smallest Working Unit Exemption

- Reason: closure-only verification task
- Allowed because task ID contains: VERIFY, AUDIT, SIGNAL, or READINESS
```

Every SWU must map to exactly one parent task. Medium/high implementation handoff should target one SWU at a time; if a task has multiple SWUs and no SWU is selected, the execution route must ask for the SWU before mutation-capable work starts.

SWU handoff contract:

```yaml
swu_id: <id>
parent_task: <task id>
objective: <goal>
dependencies:
  - <task id, SWU id, or none>
write_scope:
  - <path or module>
done_criteria:
  - <criterion>
validation:
  - <command or reviewable check>
execution_owner: subagent | local-fallback | manual
expected_result:
  result: pass | flag | block | interrupted
  files_touched: []
  validation: []
  blockers: []
  handoff_note: <summary>
```

## Blocker Ledger

| Blocker ID | Blocker | Impact | Resolution |
| --- | --- | --- | --- |
| B-001 | {blocker} | {impact} | {resolution} |

## Validation Strategy

| Check ID | Check | Scope | Tool Or Evidence |
| --- | --- | --- | --- |
| V-001 | {check} | {scope} | {tool or evidence} |

## Work-Pack Handoff

- Work-pack companion: [../work-pack.md](../work-pack.md)
- Required manifest entries: {entries}
- Deferred entries: {entries and reasons}

## Execution-Pack Handoff

- Execution-pack template: [../module-formulae/execution-pack.md](../module-formulae/execution-pack.md)
- Wave grouping: {wave notes}
- Parallelization boundary: {boundary}

## Closure Criteria

| Criterion | Evidence |
| --- | --- |
| {criterion} | {evidence} |

## Gate Result

- Status: pass, flag, or block
- Reason: {gate result summary}
