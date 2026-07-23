# TASK-NDR-VERIFY — Closure-only Recomposition

Owner: Task Session

Exemption: this task has no SWU because it adds no implementation behavior. It only verifies the completed SWU receipts against the existing contract.

- Dependencies: `SWU-NDR-013` pass receipt.
- Source anchors: `native-dispatch-runner.contract.json`; `work-pack/shared/traceability.md`; failure and success canary results.
- Related context: `EXECUTION-PACK.md` G6.
- Write scope: final closeout receipt and residue ledger inside the native dispatch runner integration evidence folder.
- Done criteria: every NDR requirement has concrete passing evidence; validator and run-evidence checks pass; deferred items remain explicit; no promotion or cross-host claim appears.
- Acceptance evidence: contract-to-path matrix, validator receipts, canary ordering proof, closeout receipt.
- Validation: JSON parse, Dispatch Spec closeout validation, run-evidence validation, concrete-path existence, public-boundary scan.
- Handoff: return implementation-complete evidence to the Orchestrate capability owner for a separate lifecycle decision.
