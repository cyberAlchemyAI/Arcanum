# Execution Pack: Deterministic Context Compiler

## Purpose

Schedule the medium-complexity work-pack without redefining its task or SWU
contracts. Every mutation unit is serial and requires a fresh explicit
selection.

## Planning Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| planningGateStatus | pass | Plan structure only. |
| executionAdmissionStatus | block-until-selection | No unit is selected. |
| complexity | medium | Split task and wave artifacts required. |
| baselineWave | [W0](work-pack/waves/W0.md) | Repeats before every selected SWU. |
| activePlanRef | [W1](work-pack/waves/W1.md) | First candidate wave, not active execution. |
| workPackManifest | [WORK-PACK.md](WORK-PACK.md) | Canonical plan. |
| layeringArtifact | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | L0 active window. |
| specRef | [SPEC.md](SPEC.md) | Define contract. |
| activeLayerWindow | L0 | Later layers are evidence-gated. |
| firstCandidateSwu | SWU-DCC-001 | Candidate only. |
| selectedSwu | none | No execution authority. |
| lastPlannedAt | 2026-07-27T00:00:00-03:00 | Plan date. |
| readinessProfile | pilot | Reusable behavior before broader lifecycle claims. |

## Task Board

| Task | Goal | Layer | Waves | Gate | Status |
| --- | --- | --- | --- | --- | --- |
| TASK-DCC-CONTRACT | schemas and early blockers | L0 | W0-W1 | selection-required | not-started |
| TASK-DCC-COMPILER | exact compile and selection | L0-L1 | W0-W2-W3 | serial dependencies | not-started |
| TASK-DCC-PAYLOAD | parity and one payload | L1 | W0-W3 | serial dependency | not-started |
| TASK-DCC-METRICS | measurement and reuse | L2 | W0-W4 | serial dependencies | not-started |
| TASK-DCC-EVIDENCE | paired live evidence | L3 | W0-W5 | reusable-evidence gate | not-started |
| TASK-DCC-INTEGRATE | canonical public integration | L3 | W0-W5 | lifecycle-owner gate | not-started |
| TASK-DCC-VERIFY | closure verification | L3 | W5 | closure exemption | not-started |

## Ordered Execution

```text
W0 -> SWU-DCC-001 -> owner receipt
W0 -> SWU-DCC-002 -> owner receipt
W0 -> SWU-DCC-003 -> owner receipt
W0 -> SWU-DCC-004 -> owner receipt
W0 -> SWU-DCC-005 -> owner receipt
W0 -> SWU-DCC-006 -> owner receipt
W0 -> SWU-DCC-007 -> owner receipt
W0 -> SWU-DCC-008 -> owner receipt
TASK-DCC-VERIFY -> closure receipt
```

The arrows express dependency eligibility, never automatic selection.

## Wave Promotion Evidence

| Wave | Decision | Required Evidence | Failure Route |
| --- | --- | --- | --- |
| W0 | is the selected unit safely bounded? | selection, context pack, baseline | block and return to Sigil Development |
| W1 | do structural inputs fail closed? | schema and negative receipts | repair SWU-DCC-001 |
| W2 | does one selector replay exactly? | deterministic and stale/escape receipts | repair or stop L0 |
| W3 | are selection and payload parity credible? | coverage, ordering, parity, adapter receipts | repair owning SWU |
| W4 | are measurement and reuse honest? | usage, cache, and base receipts | narrow claim or repair |
| W5 | is reusable behavior and integration supportable? | paired run, lifecycle diff, closure receipt | defer integration or retain residue |

## Parallelism

None. SWU-DCC-002 and 003 share the compiler, SWU-DCC-005 and 006 share
receipt semantics, and lifecycle evidence is strictly ordered. Serial execution
also preserves exact closeout baselines.

## Closure Task Exemption

TASK-DCC-VERIFY does not own an implementation behavior and is exempt from SWU
decomposition. It still has exact evidence targets and an owner receipt.

## Handoff

- Next lifecycle owner: Sigil Development
- First candidate: SWU-DCC-001
- Selected unit: none
- Task Session route: unavailable until one unit is explicitly selected
- Context pack timing: execution-time only, after selection
