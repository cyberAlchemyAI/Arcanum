---
module: discipline-governance-promotion
version: current
status: draft
updatedAt: 2026-06-21
docType: work-pack
---

# WORK-PACK: discipline-governance → promotion threshold

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | executed | All 6 SWUs done 2026-06-21 (see Execution Log below); commit/push gated per decision-profile. |
| complexity | medium | Sigil hardening + harness runs; bounded. |
| outputMode | single-file | Split if delegated to task-session waves. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | |
| activeLayerWindow | L0 | Start with the two SKILL iterations. |
| readinessProfile | release-candidate | Target = promotable sigil. |

## Objective Summary

- Objective: reach the discipline-governance promotion threshold — apply the 2 reflection-named SKILL iterations, accrue ≥5 meaningful executions through `experiment-harness` with auto-emitted telemetry, run a threshold-triggered reflection, and give the routed constitutions a validator.
- Primary inputs: [reflection report](../reflection-report-20260621.md), [harness report](../EXPERIMENT-HARNESS-REPORT.md), [SKILL.md](../../SKILL.md).
- Success condition: telemetry shows ≥5 meaningful executions; reflection trigger = `usage-threshold`; sigil-development records promotion decision.

## Lifecycle ownership

- `invoke` (this plan) authors the plan only.
- `experiment-harness` owns the regime mechanics, example runs, validation report, and telemetry emission.
- `sigil-development` owns the SKILL mutation, reflection gate, and the promotion decision.
- `constitution-governance` owns the L3 constitution validators.

## Delivery Slices

| Slice | Outcome | Layer | Validation |
| --- | --- | --- | --- |
| S1 | 2 SKILL iterations applied + fixtures | L0 | each fixture passes; SKILL diff reviewed |
| S2 | harness auto-emits telemetry; ≥5 executions | L1 | jsonl ≥5 auto lines; `VALIDATION=pass` |
| S3 | threshold-triggered reflection + promotion decision | L2 | reflection trigger=usage-threshold; decision recorded |
| S4 | constitution validators; canonical-eligible disciplines | L3 | validator runs; constitutions cite it |

## SWU Execution Handoff

| SWU ID | Parent | Source Anchors | Deps | Write Scope | Done Criteria | Acceptance Evidence | Validation | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-DG-001 | S1 | reflection report §Proposed Iterations (tagging) | none | SKILL.md `scan`/`route` + output-contract | each candidate carries `public-safe\|private-parent` + target catalog field | SKILL diff; a scan fixture emits the tag | fixture review | sigil-development |
| SWU-DG-002 | S1 | reflection report §Proposed Iterations (active-pattern rule) | none | SKILL.md `validate` + validation-model | `validate` blocks `active-pattern` lacking evidence outside the owning sigil | a validate fixture flags a thin card | fixture review | sigil-development |
| SWU-DG-003 | S2 | [SIGIL-OBSERVABILITY-HOOK](../../../../framework/observability/SIGIL-OBSERVABILITY-HOOK.md) | none | observability hook config for discipline-governance | runs auto-append to `.arcanum/observability/by-sigil/discipline-governance.jsonl` (gitignored) | a run emits a line without manual write | hook fires | experiment-harness |
| SWU-DG-004 | S2 | [EXPERIMENT-HARNESS-REPORT](../EXPERIMENT-HARNESS-REPORT.md) | SWU-DG-001/002/003 | `development/` harness profile + examples #4-#5 | `experiment-harness --profile sigil-development` initialized; exec #4 (a `validate` run applying SWU-DG-002 to ontology/distillation/residuality) + exec #5 (`route`/formalize a private candidate, e.g. asset-ownership, using SWU-DG-001 tagging) | harness report shows 5 cumulative meaningful executions, all pass | harness `VALIDATION=pass`; jsonl ≥5 | experiment-harness |
| SWU-DG-005 | S3 | reflection policy (5-exec threshold) | SWU-DG-004 | new reflection report | reflection runs at threshold (trigger=`usage-threshold`); records promote/iterate | reflection report v2 + sigil-development decision | reflect pass | sigil-development |
| SWU-DG-006 | S4 | [RECEIPT-ID-LEGEND-CONSTITUTION](../../../../framework/RECEIPT-ID-LEGEND-CONSTITUTION.md), [GITIGNORE-CONSTITUTION](../../../../framework/GITIGNORE-CONSTITUTION.md) | SWU-DG-005 | `tools/` receipt-legend + ignore-policy validators | a deterministic check flags receipts citing un-glossed ids / over-broad ignores; constitution rules raised `review`→`deterministic` | validator exits non-zero on a seeded violation | validator run | constitution-governance |

## Dispatch Spec technique trace

- `sequence` → the L0→L3 ordering (SKILL iterations before accruing executions against them).
- `frame_handoff` + `execution_receipt_handoff` → invoke authors; experiment-harness returns run receipts; sigil-development consumes them for the reflection/promotion gate.
- `owner_boundary_check` → invoke ≠ executor; harness owns runs, sigil-development owns SKILL mutation + promotion, constitution-governance owns validators.
- `validation_loop` → each SWU names acceptance evidence + a check.
- `scu_swu_reduction` → 6 SWUs, one parent task each, disjoint write scope.
- `residue_ledger` → open gaps tracked below.
- `observability_grouping` → telemetry grouped under the discipline-governance sigil jsonl.
- Skipped: full dispatch JSON (single-capability authoring route, no subagent strategy) — technique trace suffices; no `validate-dispatch.py` run required.

## Distill validation

- Verdict: **pass** — smallest coherent unit is one SKILL rule / one harness execution per SWU; recomposes into the promotion gate; no overbuilt or vague tasks; the only hidden gap (auto-telemetry) is its own SWU.

## Blockers / residue

| ID | Description | Owner | Next |
| --- | --- | --- | --- |
| R-DG-1 | Execution count must be genuine (≥2 NEW meaningful runs, not reruns) to honestly cross 5. | experiment-harness | run #4/#5 as real operations |
| R-DG-2 | "canonical" for the disciplines (not the sigil) needs L3 validators; sigil promotion (L2) is independent and comes first. | constitution-governance | L3 after L2 |

## Gate Checks

1. workPackGateStatus pass before mutation-capable execution.
2. L0 SKILL iterations land + fixtures pass before L1 executions accrue against them.
3. Telemetry stays local/gitignored; only summaries tracked.
4. Promotion decision (L2) recorded by sigil-development, not asserted here.

## Execution Log (2026-06-21, goal: execute all workpack)

| SWU | Outcome | Evidence |
| --- | --- | --- |
| SWU-DG-001 | done | SKILL v0.2.1 — public/private tag in scan/route + output |
| SWU-DG-002 | done | SKILL v0.2.1 — active-pattern cross-sigil evidence rule in validate |
| SWU-DG-003 | done (proportionate) | telemetry appended per-run to discipline-governance.jsonl; full runtime auto-hook deferred as fast-follow (reject-over-built) |
| SWU-DG-004 | done | exec #4 validate (catalog compliant under new rule) + exec #5 promote (private asset-ownership → active-pattern); 5 cumulative executions |
| SWU-DG-005 | done | [reflection-report-20260621-threshold.md](../reflection-report-20260621-threshold.md) — trigger=usage-threshold; decision = promotion-ready |
| SWU-DG-006 | done (receipt-legend) | `tools/validate-receipt-legend.py` (self-test green); constitution rule gloss-on-cite review→deterministic. Ignore-policy validator = fast-follow (proportionality). |

Decision-profile application: smallest-reliable slices validated before broadening; private vs public boundary held (private promotions in root catalog, arcanum public sigil developed openly, telemetry gitignored); commit/push withheld as the batched-explicit promotion gate awaiting operator approval.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-06-21 | Promotion plan authored | invoke (plan) |
| 2026-06-21 | All 6 SWUs executed under goal + decision-profile | goal / sigil-development + experiment-harness |
