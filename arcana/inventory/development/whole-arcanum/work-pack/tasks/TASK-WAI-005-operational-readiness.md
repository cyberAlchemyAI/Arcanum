---
module: inventory-whole-arcanum
task: TASK-WAI-005
status: completed
layer: L3
---

# TASK-WAI-005: Operational Readiness

## Objective

Make the whole-Arcanum inventory repeatable: validate, refresh, query, and report
coverage without a human UI.

## Implementation Detail

Create or update operational docs and checks only after real cards and candidate
sets exist. The validator should remain shell plus `jq` oriented and should fail
on unresolved references, malformed card fields, and governance boundary drift.

## Smallest Working Units

| SWU | Goal | Write Scope | Done Criteria | Validation |
| --- | --- | --- | --- | --- |
| SWU-WAI-011 | Add refresh and lint validation contract. | whole-arcanum validator/docs paths | completed | pass: `validate-whole-arcanum-inventory.sh` |
| SWU-WAI-012 | Write readiness report and next promotion gate. | `READINESS.md` and task-session result | completed | pass: full validation suite |

## Source Anchors

- `arcana/inventory/scripts/validate-evidence-card-fixtures.sh`
- L2 coverage reports
- candidate EvidenceSet reuse evidence

## Completion Evidence

| SWU | Result | Evidence |
| --- | --- | --- |
| SWU-WAI-011 | PASS | `OPERATIONAL-COMMANDS.md` and `scripts/validate-whole-arcanum-inventory.sh` exist; full validation suite returns `RESULT: pass`. |
| SWU-WAI-012 | PASS | `READINESS.md` exists, records validation results and remaining gaps, and the full validation suite returns `RESULT: pass`. |

## Next Unit

No pending SWUs remain. Proceed to a real-task POC using `READINESS.md` and
`OPERATIONAL-COMMANDS.md`.
