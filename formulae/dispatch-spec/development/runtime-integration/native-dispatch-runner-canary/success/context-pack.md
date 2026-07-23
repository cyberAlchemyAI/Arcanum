# Context Pack — SWU-NDR-012

Evidence class: Task Session context; not canonical source

- Task: `TASK-NDR-005 / SWU-NDR-012`
- Mode: standard, strict
- Built: `2026-07-22T23:54:59Z`
- Selected files: 12
- Obligation coverage: 12/12 (100%)
- Runtime: fresh isolated installed Codex Orchestrate package
- Runtime write scope: this `success/` directory only
- Post-pass synchronization: central manifest/work-pack status only after all success gates pass

## Controlling constraints

1. The passing SWU-NDR-011 retry receipt is the only unlock for this run.
2. Create every runtime and evidence artifact under the success folder.
3. Record one command entry: `orchestrate execute .../success/source.dispatch.json`.
4. Validate the dispatch and generate an isolated current Orchestrate package before native action.
5. Persist and spawn exactly one first-wave pass action.
6. Join its pass receipt through the complete terminal-close lifecycle.
7. Persist `gate_pass` before the dependent action is compiled or attempted.
8. Consume the reducer-emitted dependent action; do not invent it.
9. Spawn the dependent role exactly once and bind its native identifier.
10. Require the dependent artifact and pass receipt, then close its lifecycle.
11. Reduce the dependent wave to complete and validate the full event stream.
12. Preserve all failure evidence and avoid lifecycle-promotion or cross-host claims.

## Selected evidence

- `work-pack/tasks/TASK-NDR-005.md` — success behavior, scope, dependencies, done criteria — O1–O12.
- `work-pack/swu-manifest.json` — SWU-NDR-011 PASS and SWU-NDR-012 pending — O1, O12.
- `work-pack/waves/W3.md` — failure-before-success order — O1.
- `native-dispatch-runner.contract.json` — success-progression scenario and invariants — O3–O11.
- `EXECUTION-PACK.md` — G5 dependent-spawn gate — O7–O11.
- `DESIGN.md` — successful sequence and immediate causal evidence rule — O5–O11.
- failure retry `receipt.json` — exact passing prerequisite and immutable evidence — O1, O12.
- failure retry `source.dispatch.json` — matching two-wave topology and bounded roles — O5–O9.
- `runtime/orchestrate/SKILL.md` — canonical execute, spawn, and join contracts — O3–O11.
- `runtime/orchestrate/generation-manifest.json` — installed support contract — O4.
- `runtime/orchestrate/scripts/native_dispatch_coordinator.py` — reducer-emitted second wave and completion semantics — O7, O8, O11.
- `runtime/orchestrate/scripts/validate_run_evidence.py` — live causal closeout contract — O6, O7, O9–O11.

## Decisions and assumptions

- Use two sequential capability-bound host actions; this is runtime execution, not analytical fan-out.
- The first helper is read-only and returns a bound PASS from the success sentinel.
- The dependent helper owns only `dependent/output.json`; Orchestrate owns both normalized receipts.
- Build the dependent run plan only from the first reducer's `next-actions.json` and `state.json`.
- The final dependent wave has no gate; its passing reduction reaches `complete`, while the event stream ends at its joined receipt.

## Gate verdict

PASS to execute. The prerequisite retry is PASS, the success folder was absent before this session, authorization is approved, native host operations are available, and all deterministic validators are present.
