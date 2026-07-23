# Context Pack — SWU-NDR-008

Status: pass

Mode: standard, strict obligation mapping

Session evidence: controls one local Task Session. It is not reusable design authority.

## Task

Prove through a deterministic parameterized matrix that every missing, malformed, identity-mismatched, timed-out, or non-pass required receipt produces `gate_block`, names the exact violation, and emits zero dependent actions.

## Obligations

| ID | Obligation | Status |
| --- | --- | --- |
| O1 | Cover a missing required receipt. | covered |
| O2 | Cover malformed receipt shape and schema fields. | covered |
| O3 | Cover each stable reducer identity binding: dispatch, run, wave, step, role, and capability. | covered |
| O4 | Cover host `agent_id` mismatch at the prior join-normalization boundary. | covered |
| O5 | Cover timed-out, fail, block, non-pass validation, and declared-blocker receipts. | covered |
| O6 | Every invalid class returns `gate_block`. | covered |
| O7 | Every invalid class returns empty next action identifiers and an empty action set. | covered |
| O8 | Each rejection includes the exact expected blocker text/field. | covered |
| O9 | Preserve generated-package drift by adding tests/evidence only when the implementation already satisfies the behavior. | covered |

## Selected Evidence

| Source | Selector | Obligations |
| --- | --- | --- |
| `work-pack/tasks/TASK-NDR-004.md` | SWU-NDR-008 | O1–O9 |
| `work-pack/session-evidence/SWU-NDR-005/receipt.json` | join normalization pass | O4, O5 |
| `native-dispatch-runner.contract.json` | invariants and receipt requirements | O1–O8 |
| `ARCHITECTURE.json` | failure rule and gate expression | O1–O8 |
| `work-pack/shared/traceability.md` | NDR-R5/R6 | O1–O8 |
| `runtime/orchestrate/scripts/native_dispatch_coordinator.py` | `_receipt_shape_blockers`, `_admit_receipts`, reducer | O1–O3, O5–O8 |
| `runtime/orchestrate/schemas/receipt.schema.json` | canonical receipt shape | O2, O5 |
| `runtime/orchestrate/tests/test_reduce_receipts.py` | baseline invalid cases | O1–O3, O5–O8 |
| `runtime/orchestrate/tests/native-join/test_native_join_contract.py` | agent identity normalization | O4 |

## Decisions

1. Add a dedicated parameterized admission matrix instead of rewriting already-correct reducer behavior.
2. Keep `agent_id` validation in join normalization because coordinator actions do not contain a native identifier until spawn returns; the reducer validates the remaining stable declared identities.
3. Require both `gate.next_action_ids=[]` and `action_set.actions=[]` for every rejection.
4. Assert exact blocker fragments rather than only checking that some blocker exists.
5. Restrict canonical additions to excluded authoring tests, preserving the zero-drift generated packages from SWU-NDR-007.

## Write Scope

- `runtime/orchestrate/tests/receipt-admission/`
- `formulae/dispatch-spec/development/native-dispatch-runner/work-pack/session-evidence/SWU-NDR-008/`
- `formulae/dispatch-spec/development/native-dispatch-runner/work-pack/swu-manifest.json` for evidence synchronization only

The task allows coordinator/schema changes, but none are needed after the evidence audit.

## Validation Surface

- deterministic parameterized receipt matrix;
- exact blocker assertion per class;
- gate-block and zero-dependent-action assertions per class;
- canonical gate/state/action-set schema validation;
- all earlier runtime and generation regressions;
- installed-package drift remains zero because selected runtime source is unchanged.

No blocker remains. Partial-wave reconciliation stays SWU-NDR-009.

## Provenance

- Built: `2026-07-22T15:31:55Z`
- Source digests: `context-pack.json`
