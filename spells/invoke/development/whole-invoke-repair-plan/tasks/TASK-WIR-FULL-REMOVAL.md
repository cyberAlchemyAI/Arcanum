# TASK-WIR-FULL-REMOVAL — Compatibility-Closed Deferred Full Removal

## SWU-WIR-010

- Primary behavior: remove new `invoke full` routing while preserving historical readability.
- Split analysis: router, capability tables/schemas, Handoff choices, templates, fixtures, docs, generated mirrors, and compatibility diagnostics must change together; splitting would expose contradictory public states.
- Dependencies: SWU-WIR-012.
- Write scope: complete exact inventory discovered from canonical references to `full`, plus generated Invoke mirrors.
- Done: no new route advertises or accepts `full`; historical receipts receive a stable unsupported/removed diagnostic; `define|design|plan` replacements are explicit; no dangling links.
- Validation: repository reference inventory before/after, request-schema negatives, historical fixture reads, Handoff route tests, generated parity, aggregate Invoke suite.
- Compatibility: additive reader compatibility precedes deletion; rollback restores the complete inventory as one unit.
- Closeout: owner `invoke-router`; admitted deltas `update|delete`; expected `SWU-WIR-010-RESULT.json`; successor SWU-WIR-013 only on PASS.
