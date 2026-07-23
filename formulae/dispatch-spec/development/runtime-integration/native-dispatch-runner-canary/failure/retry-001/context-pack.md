# Context Pack — SWU-NDR-011 Retry 001

Evidence class: Task Session context; not canonical source

- Task: `TASK-NDR-005 / SWU-NDR-011`
- Attempt: append-only `retry-001`
- Mode: standard, strict
- Built: `2026-07-22T23:46:02Z`
- Selected files: 14
- Obligation coverage: 11/11 (100%)
- Runtime: current isolated installed Codex Orchestrate package
- Runtime write scope: this `failure/retry-001/` directory only
- Post-pass synchronization: central manifest/work-pack status only after all retry gates pass

## Controlling constraints

1. Preserve every file in failure attempt 1 byte-for-byte and link its receipt and hashes.
2. Generate a new isolated Orchestrate installation from current canonical source inside `retry-001/runtime/`.
3. Record one command entry: `orchestrate execute .../failure/retry-001/source.dispatch.json`.
4. Validate the retry source dispatch before any native action.
5. Persist exactly one first-wave action before invoking its mapped native host operation.
6. Use one bounded read-only helper; append attempt and host-result events around the real host call.
7. Register, wait, terminalize, close, and join that exact native identifier once.
8. Bind the intentional non-pass result to the expected action and reduce it to `gate_block`.
9. Emit zero dependent actions and perform zero dependent native spawns.
10. Validate the complete live event stream with the regenerated installed validator.
11. Keep SWU-NDR-012 locked unless every retry acceptance check passes.

## Selected evidence

- `work-pack/tasks/TASK-NDR-005.md` — retry behavior, scope, done criteria, and handoff — O1–O11.
- `work-pack/swu-manifest.json` — all dependency and attempt states — O1, O11.
- `work-pack/waves/W3.md` — failure-before-success ordering — O1, O11.
- `native-dispatch-runner.contract.json` — failure-withholding scenario and causal invariants — O3–O10.
- `EXECUTION-PACK.md` — G4 and evidence standard — O8–O11.
- `DESIGN.md` — failure sequence, native-driver boundary, and no post-hoc synthesis — O5–O10.
- SWU-NDR-007 receipt — generated-surface dependency PASS — O2.
- SWU-NDR-008 receipt — fail-closed admission dependency PASS — O8, O9.
- SWU-NDR-010 receipt — causal event dependency PASS — O6, O10.
- SWU-NDR-010R receipt — complete lifecycle dependency PASS — O7, O10.
- `runtime/orchestrate/generation-manifest.json` — selected installed support contract — O2.
- failure `source.dispatch.json` — immutable attempt-1 scenario template — O3–O9.
- failure `result.json` — exact attempt-1 blocker and satisfied assertions — O1, O10.
- failure `receipt.json` — attempt identity, helper closeout, hashes, and blocker fingerprint — O1, O7, O11.

## Decisions and assumptions

- Copy the scenario into retry scope and rewrite only retry-owned artifact references; do not reuse writable attempt-1 paths.
- Generate with the checked-in bootstrap script using selected `orchestrate` and required dependencies under the repo-codex profile.
- Execute the native Orchestrate skill in-process: deterministic preflight and compilation, then one host-native spawn from the persisted action.
- The helper returns bounded result data; Orchestrate owns receipt normalization, event persistence, reduction, and closeout.
- The existing helper exemption applies because this is one runtime-bound proof action, not analytical fan-out.

## Attempt-1 preservation anchors

- `source.dispatch.json`: `32e22bb972c2ae272b4255e3ebf9369dcf183c44ba879c480cc585ec7011d1f0`
- `result.json`: `f6213c0f9027b2f3848ac0e594b827dc6d2f5e6cad0e4b70ac675aada99552f1`
- `receipt.json`: `e62120db1388b0f67757ca0c41453b9605dd637d24eb3650cb210923286071e1`

## Gate verdict

PASS to execute. All four dependencies pass, the authorization is approved, the native host operations are available, the append-only scope is empty, and both canonical validators are available.
