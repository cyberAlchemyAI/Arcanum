# WORK-PACK: Distill Runtime-Event Emission

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | planning package is complete; lifecycle/mutation authority remains with Sigil Development |
| complexity | medium | runtime, evidence, observability, generated profiles |
| outputMode | split | task and wave contracts are separate |
| executionPackRef | [EXECUTION-PACK.md](EXECUTION-PACK.md) | required companion |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | L0-L3 decisions |
| dispatchTechniqueTrace | [DISPATCH-TECHNIQUE-TRACE.md](DISPATCH-TECHNIQUE-TRACE.md) | full dispatch validates before handoff |
| distillValidationStatus | pass | role-simulated Validate result; recomposition and atomicity pass |
| swuAtomicityStatus | pass | seven units, no task-shaped unit |
| firstUnitNarrownessStatus | pass | DRE-001 proves one event before role wiring |
| closeoutSyncStatus | pass | exact target/receipt/successor contract below |
| activeLayerWindow | complete | L0-L3 execution and closeout passed |
| readinessProfile | pilot | first live producer closeout |
| selectedSWU | none | DRE-001 through DRE-007 and VERIFY passed sequentially |

## Objective Summary

- Objective: close `GAP-DEE-002` with a live Distill producer and truthful
  direct/invoked observation boundaries.
- Primary inputs: [DEFINE.md](DEFINE.md), [DESIGN.md](DESIGN.md), accepted DEE
  schema/resolver, and current Distill contract.
- Success: both execution paths emit resolvable evidence, direct telemetry
  dedupes, emission status is truthful, readiness closes only after integrated
  evidence, and generated profiles match canonical sources.

## Task Status Board

| Task | Goal | Layer | Gate | Status |
| --- | --- | --- | --- | --- |
| [TASK-DRE-01](work-pack/tasks/TASK-DRE-01-RUNTIME-EMISSION.md) | runtime producer and both role paths | L0-L1 | complete | completed |
| [TASK-DRE-02](work-pack/tasks/TASK-DRE-02-DIRECT-TELEMETRY.md) | direct telemetry and emission status | L2 | complete | completed |
| [TASK-DRE-03](work-pack/tasks/TASK-DRE-03-READINESS.md) | canonical validation/readiness truth | L2 | complete | completed |
| [TASK-DRE-04](work-pack/tasks/TASK-DRE-04-MIRRORS.md) | regenerate runtime profiles | L3 | complete | completed |
| [TASK-DRE-VERIFY](work-pack/tasks/TASK-DRE-VERIFY.md) | integrated closeout | L3 | complete | completed |

## SWU Manifest

| SWU | Parent | Primary Behavior | Independent Acceptance Boundary | Dependencies | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-DRE-001 | TASK-DRE-01 | append one consumer-accepted Distill runtime event | one event persists; schema/digest negatives do not write | none | manual / Sigil Development | completed |
| SWU-DRE-002 | TASK-DRE-01 | emit a complete true-subagent boundary sequence | sequence resolves with stable distinct role IDs | DRE-001 | manual / Sigil Development | completed |
| SWU-DRE-003 | TASK-DRE-01 | emit a complete role-simulation boundary sequence | sequence resolves with null native IDs | DRE-002 | manual / Sigil Development | completed |
| SWU-DRE-004 | TASK-DRE-02 | append exactly one direct Distill usage signal | direct row records once; lineage/invoked misuse blocks | DRE-003 | manual / Sigil Development | completed |
| SWU-DRE-005 | TASK-DRE-02 | expose evidence-emission status at Distill closeout | complete/partial/failed/not-required/not-configured fixtures agree | DRE-004 | manual / Sigil Development | completed |
| SWU-DRE-006 | TASK-DRE-03 | make canonical validation/readiness and gap state evidence-derived | docs close gap only when integrated runtime checks pass | DRE-005 | manual / Sigil Development | completed |
| SWU-DRE-007 | TASK-DRE-04 | regenerate selected runtime profiles from canonical Distill | Codex/Claude mirrors equal bootstrap projection | DRE-006 | local-fallback / bootstrap | completed |

## SWU Atomicity

| SWU | Candidate Children | Retained Boundary | Verdict |
| --- | --- | --- | --- |
| DRE-001 | schema validation; append; digest guard | one append transaction is the minimum executable producer proof | pass |
| DRE-002 | Proposer events; Balancer events; reconciliation | partial role sequences cannot satisfy true-subagent evidence closure | pass |
| DRE-003 | simulated role events; reconciliation | partial simulation sequences cannot satisfy fallback evidence closure | pass |
| DRE-004 | envelope validation; append; dedupe | one direct-observation transaction owns all three | pass |
| DRE-005 | status vocabulary; closeout projection | vocabulary without projection has no observable behavior | pass |
| DRE-006 | validation doc; readiness doc; gap row | these are one readiness claim and must change atomically | pass |
| DRE-007 | Codex mirror; Claude mirror; parity check | one canonical projection decision must cover all generated profiles | pass |

DRE-001 is the narrowest reversible trust-building step: it adds no role wiring,
telemetry semantics, readiness claim, or generated output.

## Task Session Closeout Sync Contract

All baselines are captured immediately before an SWU as SHA-256 values for
existing files and explicit `absent` markers for new files.

| SWU | Lifecycle Owner Route | Terminal Source Receipt | Declared Target Inventory | Allowed Deltas | Owner Validation | Expected Receipt | Successor |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DRE-001 | `sigil-development --update distill` | execution-pack result shape | emitter, single-event fixtures/runner, this work-pack | artifact/evidence/status only | focused emitter suite; accepted schema validation | `work-pack/results/SWU-DRE-001-RESULT.md` | DRE-002 iff pass |
| DRE-002 | `sigil-development --update distill` | execution-pack result shape | emitter, true-subagent fixtures/runner, this work-pack | artifact/evidence/status only | true-subagent resolver suite | `work-pack/results/SWU-DRE-002-RESULT.md` | DRE-003 iff pass |
| DRE-003 | `sigil-development --update distill` | execution-pack result shape | emitter, role-simulation fixtures/runner, this work-pack | artifact/evidence/status only | simulation and cross-path suites | `work-pack/results/SWU-DRE-003-RESULT.md` | DRE-004 iff pass |
| DRE-004 | `sigil-development --update distill` | execution-pack result shape | direct observer, direct telemetry fixtures/runner, this work-pack | artifact/evidence/status only | record/dedupe/misuse suite | `work-pack/results/SWU-DRE-004-RESULT.md` | DRE-005 iff pass |
| DRE-005 | `sigil-development --update distill` | execution-pack result shape | Distill SKILL, telemetry template, status fixtures, this work-pack | contract/evidence/status only | status matrix plus semantic non-regression | `work-pack/results/SWU-DRE-005-RESULT.md` | DRE-006 iff pass |
| DRE-006 | `sigil-development --update distill` | execution-pack result shape | Distill validation/readiness, DEE gap/validation, this work-pack | evidence/status/route only | canonical suite and claim audit | `work-pack/results/SWU-DRE-006-RESULT.md` | DRE-007 iff pass |
| DRE-007 | bootstrap regeneration | execution-pack result shape | selected `.agents`/`.claude` Distill mirrors, parity runner, this work-pack | generated/evidence/status only | isolated bootstrap and exact parity | `work-pack/results/SWU-DRE-007-RESULT.md` | VERIFY iff pass |

Closeout cannot infer extra targets, authorize another SWU, publish, promote, or
rewrite historical evidence.

## Blockers And Gaps

| ID | Scope | State | Owner | Repair |
| --- | --- | --- | --- | --- |
| GAP-DEE-002 | runtime producer | resolved | Sigil Development + runtime integration | DRE-001 through DRE-007 and integrated closeout passed |
| GAP-DRE-001 | lifecycle acceptance | resolved | Sigil Development | accepted in `SIGIL-DEVELOPMENT-LIFECYCLE-RECEIPT.md` |

## Distill Validation

See [PLAN-DISTILL-VALIDATION.md](PLAN-DISTILL-VALIDATION.md).

| Check | Result |
| --- | --- |
| smallest unit | pass: DRE-001 |
| atomicity/split analysis | pass |
| first-unit narrowness | pass |
| recomposition | pass |
| hidden acceptance-critical gaps | pass: lifecycle acceptance is explicit |
| deferred complexity | pass |
| navigation | pass |

## Closeout Checks

1. DRE-001 through DRE-007 each have a passing terminal receipt.
2. Every mutation unit stayed within its declared scope and successor policy.
3. Distill plan validation and semantic-preservation checks pass.
4. Sigil Development accepted DEC-DRE-001 before mutation.
5. Generated profiles were regenerated only after canonical validation.
6. Integrated closeout passed before `GAP-DEE-002` resolved.

## Next Route

Observe meaningful direct and invoked Distill runs. Route to
`workflow-reflect` only if the configured reflection thresholds fire.
