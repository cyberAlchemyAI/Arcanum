# TASK-DEE-04: Invoke Mode Composition

Status: completed on 2026-07-17 after DEE-006 and DEE-007 evidence passed.

## Objective

Make every Invoke mode's evidence obligation explicit and prevent deferred modes from implying
operational readiness.

Selection gate: blocked until the Spellcraft receipt names exact canonical and fixture paths.

## SWU-DEE-006: Mode Capability Table

- Status: selected under
  [SPELLCRAFT-DEE-006-LIFECYCLE-RECEIPT.md](../SPELLCRAFT-DEE-006-LIFECYCLE-RECEIPT.md).
- Primary behavior: publish `implementation_status`, `dispatch_trace`, `distill`, and
  `mutation_handoff_allowed` rules per Invoke mode, with early `unsupported/deferred` for
  Invoke `full` and Invoke `validate`.
- Acceptance boundary: mode router tests stop deferred modes before lifecycle processing.
- Split analysis: table and fail-close router behavior form one decision; active-mode evidence
  projection is independently testable in DEE-007.
- Dependencies: DEE-002 and lifecycle receipt.
- Source anchors: review finding 5; Invoke root mode table.
- Write scope: canonical Invoke root/mode capability contract and tests.
- Done criteria: no validator infers absent mode obligations.
- Validation: deferred-mode fixture tests.
- Execution owner: Spellcraft.
- Completion evidence: `work-pack/results/SWU-DEE-006-RESULT.md`.

## SWU-DEE-007: Active Mode Evidence Projection

- Status: completed on 2026-07-17 under
  [SPELLCRAFT-DEE-007-LIFECYCLE-RECEIPT.md](../SPELLCRAFT-DEE-007-LIFECYCLE-RECEIPT.md).

- Primary behavior: project common execution-path/evidence/result fields and gates across
  define, design, plan, handoff, and refresh according to required/conditional applicability.
- Acceptance boundary: each active mode has a passing applicable/non-applicable case and blocks
  missing required evidence.
- Split analysis: per-mode edits share one common contract and integrated fixture boundary;
  deferred behavior remains DEE-006.
- Dependencies: DEE-005, DEE-006.
- Source anchors: accepted review mode findings and active mode contracts.
- Write scope: canonical active mode contracts, templates, runner checks, fixtures.
- Done criteria: plan never routes from authored label; conditional modes preserve bounded
  skip rationale.
- Validation: full Invoke fixture suite.
- Execution owner: Spellcraft; Distill changes, if any, route to Sigil Development.
