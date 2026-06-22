---
artifact_id: GOAL-WORK-PACK-001
artifact_type: invoke-plan-work-pack
target: arcanum/spells/goal
invoke_mode: plan
status: draft
owner: spellcraft
created_at: 2026-06-20
---

# WORK-PACK: Goal Spell

## Purpose

Canonical executable plan and execution manifest for the `goal` spell planning
stage. This work-pack translates the accepted define/design baseline into
layered waves, task contracts, and SWUs while preserving the current lifecycle
boundary: Invoke authors the plan, Spellcraft validates the spell lifecycle, and
later Task Session work executes one selected SWU at a time.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Ready for next owner: Spellcraft validation. Runtime SWUs are dependency-gated by W0. |
| complexity | medium | More than two planning artifacts, split work-pack, multiple lifecycle owners, future runtime and evidence phases. |
| outputMode | split | Required for medium complexity. |
| executionPackRef | `EXECUTION-PACK.md` | Wave choreography only; task/SWU contracts stay here and in task files. |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | Source of truth for L0-L3 decisions and promotion evidence. |
| dispatchTechniqueTrace | `DISPATCH-TECHNIQUE-TRACE.json` | Plan technique trace. |
| fullDispatchRef | `PLAN-DISPATCH.json` | Full dispatch boundary for Invoke -> Spellcraft -> Task Session -> Experiment Harness. |
| distillValidationStatus | pass | Selected smallest coherent unit is `SWU-GOAL-001`. |
| activeLayerWindow | L0 | First execution route is lifecycle validation. |
| lastUpdatedAt | 2026-06-20T21:26:56Z | Authoring timestamp. |
| readinessProfile | pilot | Goal is draft; registry readiness remains evidence-gated. |

## Objective Summary

- Objective: make `arcanum/spells/goal` ready for lifecycle validation and later
  bounded runtime SWUs without bypassing public/private, source-authority,
  approval, or generated-surface boundaries.
- Primary inputs: source contract, public schema, define-stage spec, design
  architecture/rules/schemas/contracts, glossary consistency, and layering seed.
- Success condition: Spellcraft can validate the package from stable artifacts,
  and the next worker can select exactly one SWU with source anchors, write
  scope, done criteria, and verification evidence.

## Source Contracts

| Source | Role |
| --- | --- |
| `arcanum/spells/goal/README.md` | Public source contract for spell behavior and gates. |
| `arcanum/spells/goal/decision-profile.schema` | Public neutral decision-profile shape. |
| `../20260620T202601Z-goal-spec-definitions/SPEC.md` | Define-stage required behavior, state model, interfaces, and validation matrix. |
| `../20260620T202601Z-goal-spec-definitions/DEFINITIONS.md` | Local glossary and canonical term links. |
| `../20260620T205253Z-goal-architecture-rules-schemas-contracts/ARCHITECTURE.md` | Six-view design baseline. |
| `../20260620T205253Z-goal-architecture-rules-schemas-contracts/RULES.md` | Rule families and enforcement order. |
| `../20260620T205253Z-goal-architecture-rules-schemas-contracts/CONTRACTS.md` | Contract matrix and boundary contracts. |
| `../20260620T205253Z-goal-architecture-rules-schemas-contracts/SCHEMAS.md` | Schema inventory and schema promotion questions. |

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-001 | Spellcraft accepts or repairs the public source/design/plan packet. | L0 | [W0](work-pack/waves/W0.md) | Existing define/design artifacts. | Spellcraft validation report or named refinement block. |
| S-002 | Read-only runtime skeleton can bind, read, classify, and report without mutation. | L1 | [W1](work-pack/waves/W1.md) | S-001 pass. | Goal loop result fixture or reviewable dry-run evidence. |
| S-003 | Delegation, receipt closeout, audit, and staged deltas work without active apply. | L2 | [W2](work-pack/waves/W2.md) | S-002 pass. | Dispatch validation, terminal receipt, audit verdict, staged delta shape check. |
| S-004 | Approval, telemetry, gap discovery, and reusable evidence are ready for generated runtime packaging. | L3 | [W3](work-pack/waves/W3.md) | S-003 pass. | Approval-token scenario, telemetry signal, Experiment Harness report, installer dry run. |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [TASK-GOAL-SPELLCRAFT-VALIDATE](work-pack/tasks/TASK-GOAL-SPELLCRAFT-VALIDATE.md) | Validate lifecycle packet and stage source-state sync proposal. | L0 | medium | [W0](work-pack/waves/W0.md) | README, SPEC, ARCHITECTURE, RULES, CONTRACTS, SCHEMAS | ready | not-started |
| [TASK-GOAL-RUNTIME-SKELETON](work-pack/tasks/TASK-GOAL-RUNTIME-SKELETON.md) | Build read-only bind/frontier/risk/result skeleton. | L1 | medium | [W1](work-pack/waves/W1.md) | README phases, frontier/risk schemas, decision profile schema | blocked-after-W0 | not-started |
| [TASK-GOAL-DELEGATION-STAGING](work-pack/tasks/TASK-GOAL-DELEGATION-STAGING.md) | Add dispatch route, receipt closeout, audit, and staged delta behavior. | L2 | medium | [W2](work-pack/waves/W2.md) | RULES, CONTRACTS, dispatch schema, receipt and delta schemas | blocked-after-W1 | not-started |
| [TASK-GOAL-APPROVAL-PROMOTION](work-pack/tasks/TASK-GOAL-APPROVAL-PROMOTION.md) | Add approval token, Craft apply boundary, gap discovery, and proportionality controls. | L3 | medium | [W3](work-pack/waves/W3.md) | approval schema, telemetry schema, gap and budget rules | blocked-after-W2 | not-started |
| [TASK-GOAL-VERIFY-EVIDENCE](work-pack/tasks/TASK-GOAL-VERIFY-EVIDENCE.md) | Prove reusable behavior and generated-runtime readiness. | L3 | medium | [W3](work-pack/waves/W3.md) | validation matrix, Experiment Harness, runtime installer | ready-after-implementation | not-started |

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Related Context | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-GOAL-001 | [TASK-GOAL-SPELLCRAFT-VALIDATE](work-pack/tasks/TASK-GOAL-SPELLCRAFT-VALIDATE.md) | README, SPEC, ARCHITECTURE, RULES, CONTRACTS, SCHEMAS, this work-pack | spellcraft lifecycle authority | none | `arcanum/spells/goal/development/spellcraft-runs/` or equivalent validation report path | Validation accepts, flags, or blocks the packet with named evidence. | Spellcraft validation report. | `spellcraft validate arcanum/spells/goal` or reviewable Spellcraft run result. | manual | selected |
| SWU-GOAL-002 | [TASK-GOAL-SPELLCRAFT-VALIDATE](work-pack/tasks/TASK-GOAL-SPELLCRAFT-VALIDATE.md) | CRAFT view, ledger, README, decision-profile schema | source-state sync, public/private boundary | SWU-GOAL-001 | staged proposal artifact only; no active ledger mutation | Stale Craft rows are summarized as a staged proposal or explicitly deferred. | Staged sync proposal or deferral note. | Review staged proposal for no active ledger mutation. | local-fallback | blocked-after-SWU-GOAL-001 |
| SWU-GOAL-003 | [TASK-GOAL-RUNTIME-SKELETON](work-pack/tasks/TASK-GOAL-RUNTIME-SKELETON.md) | README Execution Phases, frontier snapshot schema, decision profile schema | L1 read-only proof | SWU-GOAL-001 | future runtime source contract or implementation files selected by Spellcraft | Goal bind and frontier read produce a snapshot or source-authority block. | Read-only fixture or dry-run result. | Frontier snapshot schema parse plus source-authority review. | task-session | blocked-after-W0 |
| SWU-GOAL-004 | [TASK-GOAL-RUNTIME-SKELETON](work-pack/tasks/TASK-GOAL-RUNTIME-SKELETON.md) | README Risk Classification, RULES risk rules, goal loop result schema | fail-closed risk behavior | SWU-GOAL-003 | future runtime source contract or implementation files selected by Spellcraft | Unknown and protected work stop before route or mutation. | Goal Loop Result with T3 stop case. | Goal loop result schema parse plus protected-operation scenario. | task-session | blocked-after-SWU-GOAL-003 |
| SWU-GOAL-005 | [TASK-GOAL-DELEGATION-STAGING](work-pack/tasks/TASK-GOAL-DELEGATION-STAGING.md) | dispatch schema, CONTRACTS Route and Execution contracts, execution receipt schema | owner-boundary routing | SWU-GOAL-004 | future runtime route adapter and receipt checks selected by Spellcraft | Eligible node route names owner, technique, receipt, gate, and fallback. | Valid dispatch route and terminal receipt. | dispatch-spec validator plus receipt shape review. | task-session | blocked-after-W1 |
| SWU-GOAL-006 | [TASK-GOAL-DELEGATION-STAGING](work-pack/tasks/TASK-GOAL-DELEGATION-STAGING.md) | RULES audit/staging rules, staged delta schema | proposal-before-apply guard | SWU-GOAL-005 | future audit/staging implementation selected by Spellcraft | Audit veto blocks close; accepted source-changing progress becomes staged delta only. | Audit verdict and staged delta artifact. | staged delta schema parse plus no-active-mutation review. | task-session | blocked-after-SWU-GOAL-005 |
| SWU-GOAL-007 | [TASK-GOAL-APPROVAL-PROMOTION](work-pack/tasks/TASK-GOAL-APPROVAL-PROMOTION.md) | approval token schema, approval contract, Craft apply boundary | explicit approval semantics | SWU-GOAL-006 | future approval and apply-boundary implementation selected by Spellcraft | Batch apply requires batch-specific approval token and durable decision record. | Approval-token scenario and rejected ambient-approval scenario. | approval-token schema parse plus decision-record link review. | task-session | blocked-after-W2 |
| SWU-GOAL-008 | [TASK-GOAL-APPROVAL-PROMOTION](work-pack/tasks/TASK-GOAL-APPROVAL-PROMOTION.md) | README Gap Discovery and Proportionality Guard, RULES budget rules | bounded discovery and budget ceiling | SWU-GOAL-007 | future gap/budget module implementation selected by Spellcraft | Gap discovery runs only after empty frontier and terminates by budget/dedupe rules. | Gap-discovery termination evidence and budget stop case. | reviewable fixture or Experiment Harness scenario. | task-session | blocked-after-SWU-GOAL-007 |
| SWU-GOAL-009 | [TASK-GOAL-VERIFY-EVIDENCE](work-pack/tasks/TASK-GOAL-VERIFY-EVIDENCE.md) | telemetry schema, validation matrix, registry readiness gate | reusable behavior proof | SWU-GOAL-008 | `arcanum/spells/goal/development/experiment-runs/` or equivalent evidence path | Low, medium, and protected-mutation scenarios prove fail-closed spine. | Experiment Harness report. | experiment-harness validation scenario set. | manual | blocked-after-W3-runtime |
| SWU-GOAL-010 | [TASK-GOAL-VERIFY-EVIDENCE](work-pack/tasks/TASK-GOAL-VERIFY-EVIDENCE.md) | README Local Customization, generated-surface rule, runtime installer contract | generated package readiness | SWU-GOAL-009 | generated runtime outputs through installer only | Runtime package generation is dry-run or applied by approved installer path, never hand-authored. | Installer dry-run/apply evidence and no hand-authored generated surface. | runtime installer validation plus diff hygiene. | manual | blocked-after-SWU-GOAL-009 |

## Blockers And Gaps

| Blocker ID | Scope | Description | Owner | Next Action | Target Date |
| --- | --- | --- | --- | --- | --- |
| B-GOAL-W0-VALIDATION | runtime SWUs | Runtime implementation depends on Spellcraft accepting or repairing the source/design/plan packet. | spellcraft | Execute SWU-GOAL-001. | n/a |
| G-GOAL-SCHEMA-HOME | schema promotion | Design schemas currently live in an Invoke run; stable public schema location is undecided. | spellcraft | Decide during SWU-GOAL-001 whether to keep, copy, or promote schemas. | n/a |
| G-GOAL-CRAFT-SYNC | source-state sync | Craft ledger/view still describe README/schema as planned even though authoring exists; active mutation requires a staged proposal and approval path. | craft/goal | Prepare staged proposal in SWU-GOAL-002. | n/a |
| B-GOAL-PROMOTION-EVIDENCE | registry readiness | Reusable behavior proof is absent. | experiment-harness | Execute SWU-GOAL-009 after runtime behavior exists. | n/a |

## Dispatch Technique Trace

| Technique ID | Applied To | Validation Expectation | Status |
| --- | --- | --- | --- |
| sequence | define/design refs -> plan artifacts -> lifecycle handoff | Downstream artifacts consume explicit inputs. | pass |
| scu_swu_reduction | SWU manifest and active layer window | First executable unit is `SWU-GOAL-001`. | pass |
| recomposition_proof | W0 through W3 | Each SWU recomposes into the approved goal design. | pass |
| validation_loop | slices, tasks, SWUs, dispatch file | Every delivery slice has validation evidence. | pass |
| owner_boundary_check | Invoke, Spellcraft, Task Session, Experiment Harness | Plan does not claim downstream lifecycle authority. | pass |
| handle_handoff | source refs and task files | Handoff uses artifact paths and handles. | pass |
| residue_ledger | blockers and gaps | Unresolved target gaps have owner and next action. | pass |
| execution_receipt_handoff | future delegated execution | Expected receipt fields are defined before execution begins. | pass |

## Distill Validation

| Check | Result | Evidence Or Gap |
| --- | --- | --- |
| Smallest coherent unit or SWU boundary | pass | `SWU-GOAL-001` is selected and executable without runtime mutation. |
| Recomposition proof | pass | W0 validates the packet, W1 proves read-only behavior, W2 adds staged delegation, W3 proves approval/evidence readiness. |
| Hidden acceptance-critical gaps | pass | Known gaps are named in Blockers And Gaps with owners and repair routes. |
| Deferred complexity | pass | Runtime implementation, generated surfaces, and registry readiness are deferred behind evidence gates. |
| Navigation to first executable unit | pass | Start at `TASK-GOAL-SPELLCRAFT-VALIDATE.md` and `SWU-GOAL-001`. |

## Gate Checks

1. Runtime implementation must not begin before SWU-GOAL-001 exits pass or a
   named repair path is accepted.
2. Active Craft ledger mutation must not occur through Invoke plan output.
3. Each future SWU must be selected one at a time before mutation-capable
   execution.
4. Generated host surfaces must be produced by installer paths only.
5. Filled decision profiles must remain outside the public spell package.
6. Experiment evidence is required before registry readiness advances.

## Next Implementation SWU

`SWU-GOAL-001` is the selected start point: run Spellcraft validation against
the goal source/design/plan packet.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-06-20 | Initial Invoke plan work-pack created. | Codex |
