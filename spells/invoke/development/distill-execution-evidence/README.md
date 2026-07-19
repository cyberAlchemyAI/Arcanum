# Invoke Distill Execution Evidence

Governed Define, Design, and Plan package for the accepted change requests in
`ops/development/2026-07-17-invoke-distill-enforcement-review/`.

This package proposes an enforcement architecture; it does not revise Invoke or Distill,
approve the architecture, or make the Workbench mutation-ready.

## Navigation

1. [Define](DEFINE.md) and [glossary](GLOSSARY.md)
2. [Design](DESIGN.md) and [glossary consistency](GLOSSARY-CONSISTENCY.md)
3. [Distill run request](DISTILL-RUN-REQUEST.md) and design validation
4. [Implementation layering](IMPLEMENTATION-LAYERING.md) and
   [implementation plan](IMPLEMENTATION-PLAN.md)
5. [Execution pack](EXECUTION-PACK.md), [work-pack](WORK-PACK.md), and
   [gap ledger](GAP-LEDGER.md)
6. [Dispatch trace](DISPATCH-TECHNIQUE-TRACE.md) and validated
   [dispatch JSON](distill-execution-evidence.dispatch.json)
7. Plan Distill validation and [Invoke result](INVOKE-RESULT.md) when authored

Current selected unit: `SWU-DEE-001`. Current blocker: `DEC-DEE-001`. Accept or narrow
routes to one newly selected downstream SWU; reject preserves residue and selects none.

## Authority Boundary

- Invoke owns this intent-to-artifact package.
- Spellcraft owns acceptance and revision of the Invoke spell lifecycle.
- Sigil Development owns any Distill sigil lifecycle change.
- Task Session may execute one accepted SWU only after its owner gates pass.
- Existing Workbench evidence remains historical and unverified until replay.
