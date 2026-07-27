---
module: deterministic-context-compiler
version: current
status: plan-validated
updatedAt: 2026-07-27
docType: work-pack
lifecycle_owner: sigil-development
selected_swu: none
---

# WORK-PACK: Deterministic Context Compiler

## Purpose

Provide the canonical executable plan for implementing and evidencing the
deterministic Context Builder compiler without conflating plan completeness,
SWU selection, implementation, reusable behavior, or lifecycle promotion.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Structural planning gate; not execution authorization. |
| executionAdmissionStatus | block-until-selection | Sigil Development must accept the route and exactly one SWU must be selected. |
| complexity | medium | Eight mutation SWUs, one closure task, multiple schemas, scripts, fixtures, and lifecycle boundaries. |
| outputMode | split | Tasks, waves, and shared contracts are separate files. |
| executionPackRef | [EXECUTION-PACK.md](EXECUTION-PACK.md) | Required medium-complexity companion. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | L0 is the active window. |
| dispatchTechniqueTrace | [DISPATCH-TRACE.md](DISPATCH-TRACE.md) | Full Dispatch Spec trace. |
| distillValidationStatus | pass | [DISTILL-VALIDATION.md](DISTILL-VALIDATION.md) |
| swuAtomicityStatus | pass | All eight units have one behavior and independent acceptance. |
| firstUnitNarrownessStatus | pass | SWU-DCC-001 is the narrowest reversible candidate; it is not selected. |
| closeoutSyncStatus | pass | Every mutation SWU has exact targets, baseline, receipt, validation, and successor. |
| activeLayerWindow | L0 | Later layers require predecessor evidence. |
| firstCandidateSwu | SWU-DCC-001 | Candidate only. |
| selectedSwu | none | Invoke does not select or execute. |
| lastUpdatedAt | 2026-07-27T00:00:00-03:00 | Date-bound authoring timestamp; receipts bind exact bytes. |
| readinessProfile | pilot | Target is reusable-behavior proof, not production readiness. |

## Objective Summary

- Objective: deterministically validate, snapshot, deduplicate, select, render,
  reuse, and receipt already-authored Context Builder evidence candidates.
- Primary inputs:
  [SPEC.md](SPEC.md), [ARCHITECTURE.md](ARCHITECTURE.md),
  [WITNESS-CONTRACTS.md](WITNESS-CONTRACTS.md), and
  [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md).
- Success condition: deterministic fixtures and paired live evidence pass,
  then Sigil Development integrates only the supported public contract.
- Evidence ceiling: this work-pack is Plan evidence; no implementation witness
  has run.

## Delivery Slices

| Slice | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-001 | structural request/receipt boundary | L0 | [W1](work-pack/waves/W1.md) | W0 | schema and negative fixtures |
| S-002 | exact single-selector compile and replay | L0 | [W2](work-pack/waves/W2.md) | SWU-DCC-001 | DCC-FIX-001, 003, 006 |
| S-003 | deterministic deduplication and covering set | L1 | [W3](work-pack/waves/W3.md) | SWU-DCC-002 | DCC-FIX-002, 004, 005, 007, 008 |
| S-004 | output parity and one-payload handoff | L1 | [W3](work-pack/waves/W3.md) | SWU-DCC-003 | DCC-FIX-011, 012 |
| S-005 | evidence-separated measurement | L2 | [W4](work-pack/waves/W4.md) | SWU-DCC-004 | DCC-FIX-009 |
| S-006 | cache invalidation and base/delta proof | L2 | [W4](work-pack/waves/W4.md) | SWU-DCC-005 | DCC-FIX-010 and cache mutants |
| S-007 | paired baseline/candidate evidence | L3 | [W5](work-pack/waves/W5.md) | SWU-DCC-006 | Experiment Harness receipt |
| S-008 | lifecycle-owned canonical integration | L3 | [W5](work-pack/waves/W5.md) | SWU-DCC-007 | full regression and public hygiene |
| S-009 | independent closure verification | L3 | [W5](work-pack/waves/W5.md) | all SWUs | full receipt reconciliation |

## Task Status Board

| Task | Goal | Layer | Complexity | Waves | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- |
| [TASK-DCC-CONTRACT](work-pack/tasks/TASK-DCC-CONTRACT.md) | freeze structural contracts | L0 | medium | W1 | ready-after-selection | not-started |
| [TASK-DCC-COMPILER](work-pack/tasks/TASK-DCC-COMPILER.md) | exact compile and covering selection | L0-L1 | medium | W2-W3 | dependency-bound | not-started |
| [TASK-DCC-PAYLOAD](work-pack/tasks/TASK-DCC-PAYLOAD.md) | parity and one-payload handoff | L1 | medium | W3 | dependency-bound | not-started |
| [TASK-DCC-METRICS](work-pack/tasks/TASK-DCC-METRICS.md) | measurement and safe reuse | L2 | medium | W4 | dependency-bound | not-started |
| [TASK-DCC-EVIDENCE](work-pack/tasks/TASK-DCC-EVIDENCE.md) | paired reusable-behavior evidence | L3 | medium | W5 | dependency-bound | not-started |
| [TASK-DCC-INTEGRATE](work-pack/tasks/TASK-DCC-INTEGRATE.md) | bounded canonical integration | L3 | medium | W5 | lifecycle-bound | not-started |
| [TASK-DCC-VERIFY](work-pack/tasks/TASK-DCC-VERIFY.md) | closure verification | L3 | medium | W5 | ready-after-implementation | not-started |

## SWU Atomicity Review

| SWU | Primary Behavior | Independent Acceptance Boundary | Candidate Child Units | Retained-Boundary Rationale | Verdict |
| --- | --- | --- | --- | --- | --- |
| SWU-DCC-001 | validate typed request/receipt structure | positive and negative schemas pass before writes | schemas; negative fixtures | contracts and fail-closed proof are one trust boundary | pass |
| SWU-DCC-002 | compile one exact selector end to end | byte-identical replay and stale/escape negatives | snapshot; object; payload; replay | each child alone loses end-to-end utility or proof | pass |
| SWU-DCC-003 | deterministic dedupe and covering selection | stable selected set, coverage, exclusions, blockers | dedupe; greedy selection | dedupe changes selection inputs; one decision boundary | pass |
| SWU-DCC-004 | maintain output parity and one runtime payload | all projections agree and one payload is named | renderer; adapter | the acceptance-critical boundary is persistence versus injection | pass |
| SWU-DCC-005 | keep measurement sources distinct | unavailable evidence remains unknown | bytes; tokenizer; runtime usage | one schema must prevent claim collapse | pass |
| SWU-DCC-006 | admit reuse only with current proof | corrupt/stale/base mutants fail closed | cache; delta | both control reused bytes entering the payload | pass |
| SWU-DCC-007 | produce paired reusable-behavior evidence | comparable runs and honest comparison receipt | profile; live run | neither supports a claim without the other | pass |
| SWU-DCC-008 | integrate the proved public contract | canonical files agree and regressions pass | skill; README; templates | partial public contract would be incoherent | pass |

## SWU Execution Handoff

| SWU | Parent Task | Source Anchors | Related Context | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-DCC-001 | [Contract](work-pack/tasks/TASK-DCC-CONTRACT.md) | FR-01, FR-07; Request Validator | shared context and decisions | W0 | exact task-local ten targets | structural pass/fail boundary | schema and negative receipts | three request fixtures | Sigil Development + selected Task Session | candidate |
| SWU-DCC-002 | [Compiler](work-pack/tasks/TASK-DCC-COMPILER.md) | FR-02, 03, 08; Snapshotter/CAS | schemas and single source fixture | 001 | exact task-local eight targets | exact object/payload/receipt replay | DCC-FIX-001, 003, 006 | compile replay and mutants | Sigil Development + selected Task Session | dependency-bound |
| SWU-DCC-003 | [Compiler](work-pack/tasks/TASK-DCC-COMPILER.md) | FR-05, 06, 07; Selector | traceability and compiler contract | 002 | exact task-local ten targets | stable complete selected set | DCC-FIX-002, 004, 005, 007, 008 | five selection fixtures | Sigil Development + selected Task Session | dependency-bound |
| SWU-DCC-004 | [Payload](work-pack/tasks/TASK-DCC-PAYLOAD.md) | FR-08, 09; Renderer/Adapter | current templates and selected set | 003 | exact task-local nine targets | output parity and one payload | DCC-FIX-011, 012 | parity and adapter mutants | Sigil Development + selected Task Session | dependency-bound |
| SWU-DCC-005 | [Metrics](work-pack/tasks/TASK-DCC-METRICS.md) | FR-11; usage interface | validation strategy | 004 | exact task-local eight targets | honest evidence labels | DCC-FIX-009 | three usage fixtures | Sigil Development + selected Task Session | dependency-bound |
| SWU-DCC-006 | [Metrics](work-pack/tasks/TASK-DCC-METRICS.md) | FR-04, 10; CAS/runtime | cache and usage schemas | 005 | exact task-local ten targets | safe stale/corrupt/base handling | DCC-FIX-010 and mutants | cache/base replay | Sigil Development + selected Task Session | dependency-bound |
| SWU-DCC-007 | [Evidence](work-pack/tasks/TASK-DCC-EVIDENCE.md) | acceptance and live evidence contracts | prior owner receipts | 006 | exact task-local eight targets | comparable paired receipt | baseline/candidate and review | Experiment Harness validation | Sigil Development + selected Task Session | dependency-bound |
| SWU-DCC-008 | [Integrate](work-pack/tasks/TASK-DCC-INTEGRATE.md) | full spec; versioning; R-007 | lifecycle receipts | 007 | exact task-local seven targets | smallest supported canonical diff | regressions, hygiene, owner receipt | full suite and parity disposition | Sigil Development | lifecycle-bound |

Each task file includes the full objective, split analysis, exact inventory,
done criteria, evidence, commands, owner, expected result, and closeout contract.
Context Builder generates a strict execution-time pack only after selection.

## Task Session Closeout Sync Contract

Shared receipt fields and rules are fixed in
[CLOSEOUT-CONTRACT.md](work-pack/shared/CLOSEOUT-CONTRACT.md). The exact target
inventory is the numbered `Exact Write Scope` in each linked task/SWU section.

| SWU | Lifecycle Owner Route | Terminal Source Receipt | Exact Target Inventory | Baseline | Allowed Deltas | Owner Validation | Expected Owner Receipt | Successor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-DCC-001 | Sigil Development -> selected Task Session -> Sigil Development | shared task-session receipt contract | [001 inventory](work-pack/tasks/TASK-DCC-CONTRACT.md#exact-write-scope) | exact inventory digest | added evidence/artifacts | schema and three fixture replay | `session-evidence/SWU-DCC-001/owner-receipt.json` | 002 eligible; not selected |
| SWU-DCC-002 | same bounded route | shared contract | [002 inventory](work-pack/tasks/TASK-DCC-COMPILER.md#exact-write-scope) | exact inventory digest | added/changed artifacts; evidence | compile replay and two mutants | `session-evidence/SWU-DCC-002/owner-receipt.json` | 003 eligible; not selected |
| SWU-DCC-003 | same bounded route | shared contract | [003 inventory](work-pack/tasks/TASK-DCC-COMPILER.md#exact-write-scope-1) | exact inventory digest | added/changed artifacts; evidence | five selection fixture replay | `session-evidence/SWU-DCC-003/owner-receipt.json` | 004 eligible; not selected |
| SWU-DCC-004 | same bounded route | shared contract | [004 inventory](work-pack/tasks/TASK-DCC-PAYLOAD.md#exact-write-scope) | exact inventory digest | added artifacts/evidence | parity and adapter replay | `session-evidence/SWU-DCC-004/owner-receipt.json` | 005 eligible; not selected |
| SWU-DCC-005 | same bounded route | shared contract | [005 inventory](work-pack/tasks/TASK-DCC-METRICS.md#exact-write-scope) | exact inventory digest | added artifacts/evidence | usage fixture replay | `session-evidence/SWU-DCC-005/owner-receipt.json` | 006 eligible; not selected |
| SWU-DCC-006 | same bounded route | shared contract | [006 inventory](work-pack/tasks/TASK-DCC-METRICS.md#exact-write-scope-1) | exact inventory digest | added/changed artifacts; evidence | stale/corrupt/base replay | `session-evidence/SWU-DCC-006/owner-receipt.json` | 007 eligible; not selected |
| SWU-DCC-007 | same bounded route with Experiment Harness | shared contract | [007 inventory](work-pack/tasks/TASK-DCC-EVIDENCE.md#exact-write-scope) | exact inventory digest | added evidence; status | paired-run validation/review | `session-evidence/SWU-DCC-007/owner-receipt.json` | 008 eligible only on reusable pass; not selected |
| SWU-DCC-008 | Sigil Development-owned integration | shared contract | [008 inventory](work-pack/tasks/TASK-DCC-INTEGRATE.md#exact-write-scope) | exact inventory digest | changed artifacts; evidence/status/route | full regression, hygiene, parity disposition | `session-evidence/SWU-DCC-008/owner-receipt.json` | none |

Receipt paths in the table are relative to
`transmutations/context-builder/development/deterministic-context-compiler/`.
No row authorizes its successor.

## Blockers And Admission Conditions

| ID | Scope | Description | Owner | Next Action |
| --- | --- | --- | --- | --- |
| A-001 | execution admission | No SWU is selected. | user and Sigil Development | accept lifecycle handoff and select exactly one SWU |
| A-002 | later layers | Implementation and witnesses are unexecuted. | per-SWU Task Session | proceed serially only after predecessor owner receipt |
| A-003 | integration | Reusable behavior and savings are unproven. | Sigil Development | require SWU-DCC-007 evidence before 008 |

These conditions block mutation, not Plan completeness.

## Dispatch Technique Trace

| Technique | Applied To | Validation Expectation | Status |
| --- | --- | --- | --- |
| sequence | Define -> Design -> Plan -> lifecycle handoff | every non-first step consumes a prior artifact or receipt | pass |
| frame_handoff | stage transports | each stage names the bounded incoming frame | pass |
| handle_handoff | design and plan artifacts | artifacts are referenced, not copied into another authority owner | pass |
| residue_ledger | decisions, gaps, admission conditions | unresolved claims retain owner and route | pass |
| scu_swu_reduction | task decomposition | every SWU has one primary behavior and split analysis | pass |
| recomposition_proof | SWUs -> spec/architecture | traceability covers every requirement and layer | pass |
| validation_loop | fixtures, Distill, Dispatch, closure | every slice names evidence and failure route | pass |
| concrete_path_evidence | exact targets and receipts | no glob or inferred target admits mutation | pass |
| artifact_contract_bridge | design -> work-pack -> owner receipts | checks prove artifact behavior, not promotion | pass |
| execution_receipt_handoff | Task Session closeout | source and owner receipts are exact and bounded | pass |
| authority_split_gate | Invoke / Task Session / Sigil Development | planning, execution, evidence, and lifecycle claims remain separate | pass |
| owner_boundary_check | final handoff | Invoke stops before lifecycle mutation | pass |
| observability_grouping | Invoke and Distill signals | child and parent share one dispatch reference | pass; central ledger lines 401-402 |

Full route: [INVOKE-DISPATCH.json](INVOKE-DISPATCH.json).

## Distill Validation

| Check | Result | Evidence |
| --- | --- | --- |
| Smallest coherent first unit | pass | SWU-DCC-001 freezes schema and fail-closed validation only. |
| SWU atomicity and split analysis | pass | Eight primary behaviors; candidate children assessed in each task. |
| First-unit narrowness | pass | 001 is reversible and precedes compiler/cache mutation; not selected. |
| Recomposition proof | pass | [TRACEABILITY.md](work-pack/shared/TRACEABILITY.md) maps all requirements. |
| Hidden acceptance-critical gaps | pass | runtime usage and reusable behavior stay later, explicit, and blocking. |
| Deferred complexity | pass | provider cache, cleanup, selector breadth, publication, production are excluded. |
| Navigation | pass | first candidate resolves directly to TASK-DCC-CONTRACT and W1. |

See [DISTILL-VALIDATION.md](DISTILL-VALIDATION.md).

## Required Links

- [Execution pack](EXECUTION-PACK.md)
- [Shared context](work-pack/shared/CONTEXT.md)
- [Cross-task gaps](work-pack/shared/GAPS.md)
- [Cross-task decisions](work-pack/shared/DECISIONS.md)
- [Traceability](work-pack/shared/TRACEABILITY.md)
- [Closeout contract](work-pack/shared/CLOSEOUT-CONTRACT.md)
- [W0 baseline](work-pack/waves/W0.md)
- [W1 structural contract](work-pack/waves/W1.md)
- [W2 exact compile](work-pack/waves/W2.md)
- [W3 selection/parity](work-pack/waves/W3.md)
- [W4 measurement/reuse](work-pack/waves/W4.md)
- [W5 evidence/integration](work-pack/waves/W5.md)

## Gate Checks

1. Plan shape, links, layers, atomicity, Distill, Dispatch, and closeout
   contracts pass.
2. `selectedSwu = none`; therefore mutation admission remains blocked.
3. Every SWU is serial; no shared write scope is concurrently assigned.
4. A successor owner receipt makes only one next unit eligible and never
   selected.
5. Any failed negative fixture, undeclared mutation, private/public violation,
   or authority overclaim blocks its unit.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-07-27 | Initial Invoke Plan work-pack | Invoke |
