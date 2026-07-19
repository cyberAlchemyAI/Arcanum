# TASK-DEE-06: Generated Runtime Mirrors

Status: completed on 2026-07-17 after DEE-011 parity evidence passed.

## Objective

Regenerate accepted public Invoke/Distill runtime surfaces and prove parity without private
authority prose.

Selection gate: blocked until canonical owners, generated targets, and generator command are
bound by the lifecycle receipt.

## SWU-DEE-011

- Status: completed under
  [SPELLCRAFT-DEE-011-LIFECYCLE-RECEIPT.md](../SPELLCRAFT-DEE-011-LIFECYCLE-RECEIPT.md).

- Primary behavior: regenerate and compare canonical/generated evidence contracts.
- Acceptance boundary: generated surfaces match their canonical owners; boundary scan passes.
- Split analysis: generation and parity are one atomic packaging behavior; canonical mutation
  is completed and validated before this unit starts.
- Dependencies: DEE-006, DEE-007, DEE-008, DEE-009, DEE-010.
- Source anchors: accepted lifecycle receipt and generated ownership metadata.
- Write scope: generated runtime surfaces only through repository generator.
- Done criteria: no hand-edited generated drift; no private authority prose.
- Acceptance evidence: generator command and parity/boundary reports.
- Validation: bootstrap/generation validation, fixture suite, `git diff --check`.
- Execution owner: Spellcraft/bootstrap owner.
