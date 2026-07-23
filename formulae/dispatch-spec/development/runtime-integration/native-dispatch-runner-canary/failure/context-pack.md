# Context Pack — SWU-NDR-011

Task: `TASK-NDR-005 / SWU-NDR-011`

## Objective

Invoke a freshly generated installed Codex Orchestrate entrypoint on one two-wave dispatch. The real first-wave helper must return a bound non-pass receipt; the reducer must block the gate and emit zero dependent actions.

## Obligations

1. Preserve the failure-folder-only write boundary.
2. Generate the installed Orchestrate package from current canonical source inside that boundary.
3. Record the exact `orchestrate execute <dispatch.json>` entry command.
4. Validate the source dispatch before native execution.
5. Compile exactly one first-wave action and persist it before spawning.
6. Append the action attempt before the native host call and the host result immediately after return.
7. Bind the helper's intentional non-pass result to its action and native identifier.
8. Reduce the receipt to `gate_block` with zero dependent actions.
9. Validate the live causal event stream and close the helper with zero open residue.

## Selected evidence

- `TASK-NDR-005.md` — exact behavior, dependencies, write scope, and done criteria.
- SWU-NDR-007, SWU-NDR-008, and SWU-NDR-010 receipts — dependency PASS evidence.
- `native-dispatch-runner.contract.json` — failure-withholding acceptance scenario.
- `EXECUTION-PACK.md` — G4 and causal evidence standard.
- `DESIGN.md` — failure sequence and no post-hoc synthesis rule.
- `runtime/orchestrate/generation-manifest.json` — current generated support contract.
- `.agents/skills/orchestrate/SKILL.md` — installed execution protocol used to shape the isolated current package.

## Dispatch decision

This scenario uses one bounded helper. Under the Subagents Strategy helper rule it is not a multi-agent dispatch: no fan-out sheet, tension gate, or global ledger row applies. The Task Session receipt will record its spawn, join, terminal state, and closure.

## Write boundary

Every file produced by this session, including the isolated installed runtime and session receipt, remains below this `failure/` folder. The root installed packages, global telemetry, and central work-pack manifest are untouched.
