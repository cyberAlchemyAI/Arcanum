# TASK-DEE-01: Lifecycle Acceptance

## Objective

Resolve `DEC-DEE-001` through Spellcraft without mutating canonical Invoke/Distill source.

## SWU-DEE-001

- Primary behavior: render one accept, narrow, or reject lifecycle decision for the proposed
  receipt/event architecture.
- Independent acceptance boundary: accept/narrow names the executable contract, provenance
  policy, owners, downstream changes, and next selectable SWU; reject names the rationale,
  rejected proposal, preserved residue, blocked route, and selects no downstream SWU.
- Split analysis: schema, runtime, and validator implementation are plausible children and
  are deliberately excluded; this unit closes on the decision alone.
- Dependencies: accepted review findings.
- Source anchors: `DEFINE.md#Acceptance-Critical-Decision`, `DESIGN.md#Design-Decisions`,
  `GAP-LEDGER.md` row `GAP-DEE-001`.
- Related context: `work-pack/shared/context.md`.
- Write scope:
  `arcanum/spells/invoke/development/distill-execution-evidence/SPELLCRAFT-LIFECYCLE-RECEIPT.md`,
  `arcanum/spells/invoke/development/distill-execution-evidence/GAP-LEDGER.md`, and
  `arcanum/spells/invoke/development/distill-execution-evidence/WORK-PACK.md` only; no canonical
  contract mutation.
- Done criteria: DEC-DEE-001 resolved; GAP-DEE-001 updated; downstream contract changes and
  owners identified.
- Acceptance evidence: conditional receipt fields appropriate to accept/narrow/reject.
- Validation: review receipt contains decision, rationale, scope, owners, and residue.
- Execution owner: `spellcraft` with human approval where required.
- Handoff: if accepted/narrowed, select exactly one next SWU; if rejected, block and preserve
  residue.
