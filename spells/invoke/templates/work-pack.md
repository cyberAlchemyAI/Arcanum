---
module: {module-name}
version: current
status: draft
updatedAt: {date}
docType: work-pack
---

# WORK-PACK: {module-name}

## Purpose

Canonical executable plan and execution manifest for invoke planning outputs.

This artifact is the planning entrypoint and source of truth for executable planning. It contains the objective, delivery slices, tasks, SWUs, validation strategy, blockers, gates, current state, and links to waves/task files when split.
It can stay single-file for low complexity or link split waves, task files, and execution-pack artifacts for medium/high complexity.
This template is standalone at invoke scope and is composed by the DomainSpec implementation and full profiles.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass or block | Must be pass before mutation-capable execution. |
| complexity | low, medium, or high | Current complexity level. |
| outputMode | single-file or split | Split is required when scope exceeds low complexity. |
| executionPackRef | {path or n/a} | Required for medium/high complexity execution. |
| layeringArtifactRef | {path or n/a} | Should reference implementation-layering.md. |
| dispatchTechniqueTrace | {technique ids or path} | Required Invoke plan technique trace; cite only techniques that affect gates, evidence, handoff, or gaps. |
| distillValidationStatus | pass, flag, block, or skipped | Required for Invoke plan/full/validate before mutation-capable handoff. |
| swuAtomicityStatus | pass, flag, block, or n/a | Required for medium/high plans; task-shaped SWUs block handoff. |
| firstUnitNarrownessStatus | pass, flag, block, or n/a | Required before selecting the first mutation-capable SWU. |
| closeoutSyncStatus | pass or block | Pass only when every mutation-capable SWU has a complete Task Session closeout contract. |
| admissionTiming | selected-unit-at-task-session or full-frontier | New plans default to selected-unit timing; full-frontier requires a named reason. |
| executionEntryState | selection-ready, owner-prerequisite, task-ready, or blocked | Must name exactly one truthful current state. |
| allowedRoutesDigest | {sha256} | Canonical digest of the exact internal route projection. |
| activeLayerWindow | L0, L1, L2, L3, or n/a | Primary layer focus for current execution slice. |
| lastUpdatedAt | {iso-timestamp} | Last update time for this work-pack. |
| readinessProfile | pilot, release-candidate, production | Completion target profile. |

## Work-Pack Execution Policy

```yaml
executionPolicy:
  routePolicy: automatic-in-scope
  allowedRoutes:
    - routeId: <stable route id>
      frontierSwu: <exact SWU id>
      capability: <installed owner id>
      mode: <owner mode>
      target: <exact target>
      writeScope: [<normalized repository-local paths>]
      effectClass: repository-local-reversible
      requiredInputs: [<typed input refs>]
      expectedReceipt: <exact receipt contract>
  allowedRoutesDigest: <canonical sha256>
  automaticDecisions:
    - internal-tool-selection
    - capability-owner-routing
    - reversible-local-default
    - declared-fallback
    - declared-retry
    - fresh-task-session-resumption
  stopDecisions:
    - product-or-semantic-choice
    - scope-expansion
    - destructive-or-irreversible-effect
    - credentials-or-secret-access
    - external-message-or-network-effect
    - cost-policy-or-risk-acceptance
    - authority-promotion-publication-deployment
    - failed-acceptance-critical-validation
  scopeSource: exact-work-pack-and-captured-frontier
  validationPolicy: owner-gates-remain-mandatory

executionEntry:
  state: selection-ready
  selectedUnit: null
  routeId: null
  nextOwner: implementation-readiness:execute

# Null unless the selected SWU has a genuine owner prerequisite that must be
# resolved inside the already-running Task Session attempt.
preExecutionOwnerPrerequisite:
  sourcePhase: pre-execution-prerequisite
  recordSchema: arcanum/arcana/task-session/schemas/pre-execution-owner-prerequisite.schema.json
  recordRef: <exact path, sha256, and size of the instantiated typed record>
  authorizationEvidenceSelector: <current direct request or exact durable approval>
  returnControl: same-task-session-attempt
  resumePoint: task-session:context-build
  maxOwnerHops: 1
```

The operator's direct request to run or finish this Work Pack is the execution
intent. Matched internal routes do not require a second authorization prompt.
Undeclared routes and protected effects still stop before mutation.

`effectClass` is a closed shared vocabulary, not a place to encode route
purpose. A closeout route uses `repository-local-reversible`; its closeout-only
boundary is expressed by the Invoke Refresh mode, exact target and write scope,
the Closeout Contract, expected receipt, and derived authorization. Validate
the machine-readable execution-entry projection with the installed
Implementation Readiness validator before marking this Work Pack pass-ready.

When `declared-retry` is present, it authorizes only one retry after the same
owner route returns `REPAIRABLE_OWNER_CONDITION` for the unchanged entry,
binding, and selected unit. The retry consumes the ordinary step budget and
does not release replay history. A second retry stops before another dispatch.

The pre-execution record must conform to the referenced schema and bind the
route, task, SWU, attempt, target inventory, structured validation contracts,
expected owner receipt, satisfaction predicate, authorization requirement,
allowed effect, and complete fingerprint inputs. A generic readiness
`owner-prerequisite` may join before a fresh Task Session starts. A route with
`sourcePhase: pre-execution-prerequisite` instead returns its exact control
handle to the same active attempt and resumes Context Builder once; it must not
be converted into a fresh Task Session action.

## Objective Summary

- Objective: {what this work-pack must deliver}
- Primary inputs: approved design outputs, layering decisions, architecture references
- Success condition: {evidence-based completion condition}

## Planning Mapping

| Planning Source | Work-Pack Target | Mapping Rule |
| --- | --- | --- |
| Delivery Boundary | Objective Summary and Slices | Preserve included/excluded scope. |
| Delivery Slices | Task Status Board and Waves | Each slice produces one or more tasks with explicit dependencies. |
| Layer Boundary Decisions | activeLayerWindow and task layer fields | Every task and wave maps to at least one layer decision. |
| Task Decomposition | Task Status Board and task files | Preserve task IDs, dependencies, and owners. |
| Blockers And Risks | Blockers section | Carry blocker IDs and resolution paths forward unchanged. |
| Validation Strategy | Gate checks and evidence references | Reuse validation targets and expected evidence commands. |
| Dispatch Technique Trace | Gate checks, handoff notes, and gap ledger | Preserve selected Dispatch Spec techniques and the validation expectation they enforce. |
| Distill Validation | Gate checks and blockers | Carry pass/flag/block verdict, recomposition proof status, and named gaps. |
| SWU Manifest | Task files and traceability | Every non-exempt SWU keeps dependencies, write scope, done criteria, validation, and execution-owner recommendation. |
| Source Contracts | Task board, SWU manifest, and task files | Link existing source context so workers can navigate without repository search. |
| Context Builder Readiness | SWU handoff notes | Preserve source anchors, validation surfaces, and write scope so Context Builder can generate execution-time packs. Do not pre-generate context packs in Invoke planning. |
| Task Session Closeout | Task Session Closeout Sync Contract | Declare exact post-execution targets, baselines, admitted deltas, validation, owner receipt, and successor policy before mutation handoff. |

## Task Session Closeout Sync Contract

Every mutation-capable SWU must have one complete closeout row before Task
Session admission. Shared values may be referenced from a stable common
contract, but target inventory and successor policy must remain exact.

| SWU ID | Lifecycle Owner Route | Terminal Source Receipt Contract | Declared Target Inventory | Baseline Binding | Allowed Delta Classes | Owner Validation | Expected Owner Receipt | Successor Policy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-{FEATURE-CODE}-001 | `invoke:refresh:apply-approved` | {receipt schema or exact result shape} | {exact planning/evidence paths} | {live digest or deterministic baseline rule} | {evidence_added, blocker_opened, blocker_resolved, status_changed, route_changed} | {commands or review checks} | {exact receipt path and schema} | {unique declared dependency-ready same-work-pack successor or none} |

The contract is closeout-only. It cannot admit implementation, another SWU,
authority changes, promotion, publication, deployment, destructive cleanup,
policy or cost/risk acceptance, or unrelated targets. Missing inventory,
baseline binding, owner validation, expected receipt, or deterministic
successor policy sets `closeoutSyncStatus = block`. Invoke Refresh must not
infer undeclared targets after implementation.

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-001 | {outcome} | L0, L1, L2, or L3 | W0, W1, W2 | {dependencies} | {validation check} |

## Navigability Rule

The work-pack is the coordinator control panel. Link IDs to their contracts when files exist:

- task IDs link to `work-pack/tasks/TASK-*.md`,
- wave IDs link to `work-pack/waves/W*.md` when practical,
- SWU parent tasks link to their task contract,
- source contracts link to existing design, architecture, run-contract, or shared context files.

Keep future write-scope paths as plain text unless the files already exist and linking them improves readability.

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [TASK-A](work-pack/tasks/TASK-A.md) | {goal summary} | L0, L1, L2, or L3 | low, medium, high | [W1](work-pack/waves/W1.md), [W2](work-pack/waves/W2.md) | {source contract links} | ready or blocked | not-started, in-progress, completed |
| TASK-VERIFY | Completion verification | L2 or L3 | medium or high | W3+ | {source contract links} | ready-after-implementation | not-started, in-progress, completed |

## Split Task File Contract

When `outputMode = split`, each `work-pack/tasks/TASK-*.md` file must include:

- task objective,
- layer and slice mapping,
- source contracts with links to existing files,
- dependencies,
- blocker/gap state,
- Smallest Working Units,
- for each SWU: primary behavior, independent acceptance boundary, split analysis, dependencies, source anchors, related context hints, write scope, done criteria, acceptance evidence, validation surface, execution owner, and handoff note,
- synchronization rules,
- completion evidence.

Placeholder task files are not execution-ready. If task files exist but do not include the task-local SWU execution contract, set `workPackGateStatus = block`.

## SWU Atomicity Review

| SWU ID | Primary Behavior Or Decision | Independent Acceptance Boundary | Candidate Child Units | Retained-Boundary Rationale | Verdict |
| --- | --- | --- | --- | --- | --- |
| SWU-{FEATURE-CODE}-001 | {one behavior or decision} | {evidence that can pass without sibling behavior} | {plausible splits considered} | {why further split breaks executable semantic closure} | pass, flag, or block |

If candidate child units can pass independently, split the SWU. Shared files, one parent task, or sequential convenience do not prove atomicity. The first selected SWU must also be the narrowest reversible trust-building step.

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Related Context | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-{FEATURE-CODE}-001 | [TASK-A](work-pack/tasks/TASK-A.md) | {source contract links, headings, symbols, or selectors} | {related architecture/feature/context links or none} | {dependencies or none} | {paths/modules} | {done criteria} | {evidence required to mark complete} | {command or review check} | subagent, local-fallback, or manual | ready, blocked, or selected |

For SWUs intended for Task Session or runtime-goal handoff, `Source Anchors` and `Related Context` must include enough selectors for Context Builder to produce a strict handoff pack at execution time. Invoke plans should not pre-generate context packs; Task Session/Context Builder stores generated handoff packs as session evidence.

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action | Target Date |
| --- | --- | --- | --- | --- | --- |
| B-001 | task or cross-task | {blocked item} | {owner} | {unblock action} | {date} |

## Dispatch Technique Trace

| Technique ID | Applied To | Validation Expectation | Status |
| --- | --- | --- | --- |
| sequence | design refs -> plan artifacts -> handoff | downstream artifacts consume explicit inputs | pass, flag, or block |
| scu_swu_reduction | task/SWU boundary | selected unit is executable and meaningful | pass, flag, or block |
| recomposition_proof | selected unit -> approved design | unit recomposes into delivery boundary | pass, flag, or block |
| validation_loop | slices, tasks, SWUs | every delivery slice has evidence | pass, flag, or block |
| owner_boundary_check | Invoke -> next lifecycle owner | plan does not claim execution or promotion authority | pass, flag, or block |

## Distill Validation

| Check | Result | Evidence Or Gap |
| --- | --- | --- |
| Smallest coherent unit or SWU boundary | pass, flag, or block | {evidence or named gap} |
| SWU atomicity and split analysis | pass, flag, or block | {task-shaped count, candidate splits, and retained-boundary rationale} |
| First-unit narrowness | pass, flag, or block | {first selected SWU and why it is the narrowest reversible step} |
| Recomposition proof | pass, flag, or block | {evidence or named gap} |
| Hidden acceptance-critical gaps | pass, flag, or block | {none or named gaps} |
| Deferred complexity | pass, flag, or block | {what was deferred and why} |
| Navigation to first executable unit | pass, flag, or block | {first SWU/task or gap} |

## Required Links

Single-file mode:

- Keep this file as the only planning artifact when scope remains low complexity and reviewable.

Split mode:

- domainspec-spec/execution-pack.md
- work-pack/shared/context.md
- work-pack/shared/cross-task-gaps.md
- work-pack/shared/cross-task-decisions.md
- work-pack/shared/traceability.md
- work-pack/tasks/TASK-A.md
- work-pack/waves/W0.md
- work-pack/waves/W1.md

## Gate Checks

1. `workPackGateStatus` must be pass before mutation-capable execution.
2. Medium/high complexity requires `executionPackRef` and baseline wave W0.
3. Layer mappings must be consistent with `layeringArtifactRef` deferred scope and promotion decisions.
4. Any unresolved blocker that affects acceptance criteria keeps gate status at block.
5. Missing Dispatch Technique Trace or unused technique citations keep gate status at block or flag respectively.
6. Distill validation must be pass for mutation-capable execution; flag requires named gaps and repair paths, and block prevents handoff.
7. Any non-exempt SWU missing dependencies, source anchors, write scope, done criteria, acceptance evidence, validation surface, or execution-owner recommendation keeps gate status at block.
8. Any runtime-goal SWU missing source anchors or related-context hints needed for Context Builder handoff-pack generation keeps gate status at block.
9. Any task with multiple SWUs must select one SWU before mutation-capable execution.
10. Parallel SWUs must have disjoint write scopes or an explicit merge plan.
11. Medium/high SWUs must own one primary behavior, have an independently reviewable acceptance boundary, and include split analysis; task-shaped SWUs keep the gate blocked.
12. The first selected SWU must pass the narrow-first-unit gate.
13. Every mutation-capable SWU must have a complete Task Session Closeout Sync
    Contract and `closeoutSyncStatus = pass`; missing closeout prerequisites
    block execution before source mutation.

## Handoff To Execution Pack

Use [domainspec-spec/execution-pack.md](domainspec-spec/execution-pack.md) for wave-by-wave execution details.

- Low complexity: execution details may remain in this file with `executionPackRef = n/a`.
- Medium/high complexity: generate or update execution-pack and set `executionPackRef`.
- Keep task IDs and layer assignments consistent between work-pack and execution-pack.
- Execution-pack schedules waves and SWUs; it does not redefine task or SWU contracts.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| {date} | Initial work-pack created | {name} |
