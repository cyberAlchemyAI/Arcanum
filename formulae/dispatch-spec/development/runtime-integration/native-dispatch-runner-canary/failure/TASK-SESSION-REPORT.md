# Task Session Result

- Task: `TASK-NDR-005 / SWU-NDR-011`
- Result: BLOCK
- Command: `orchestrate execute formulae/dispatch-spec/development/runtime-integration/native-dispatch-runner-canary/failure/source.dispatch.json`
- Context pack: 9 sources, 9/9 obligations covered
- Strict coverage: pass
- Runtime: current isolated installed Codex Orchestrate package
- Dispatch validation: pass
- Native execution: one first-wave helper spawned, returned `/root/ndr011_failure_nonpass`, and completed read-only
- Failure withholding: pass — the non-pass receipt produced `gate_block`, zero next actions, and zero dependent native spawns
- Causal evidence validation: block — required lifecycle events at sequences 3, 4, and 6 are unsupported by the canonical run-event schema
- Blocker fingerprint: `canonical-event-vocabulary-misses-required-join-lifecycle-events`
- Success canary: forbidden by G4
- Subagent closeout: spawned 1, joined 1, completed 1, logically closed 1, interrupted 0, open 0
- Write boundary: pass — every SWU-011 write remains inside the failure folder
- Central manifest: intentionally untouched under the strict runtime-integration-only boundary
- Claim limit: failure withholding occurred, but the scenario is not accepted as causal integration proof because its full live lifecycle stream does not validate

## Next required decision

Authorize a bounded repair outside the canary folder to add all five missing join-lifecycle kinds—`agent_wait_registered`, `wait_attempted`, `agent_closed`, `wait_timed_out`, and `agent_interrupted`—to the canonical event schema and define both successful-close and timeout/interrupt ordering rules in `validate_run_evidence.py`. Then regenerate the isolated runtime and rerun SWU-NDR-011. Do not run SWU-NDR-012 first.
