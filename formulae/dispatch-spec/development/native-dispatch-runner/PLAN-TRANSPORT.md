# Plan Transport

- Next capability: Task Session
- First selection: `work-pack/tasks/TASK-NDR-001.md`, `SWU-NDR-001`
- Execution authorization: required
- Canonical machine inputs: `native-dispatch-runner.contract.json`, `ARCHITECTURE.json`, `execution.dispatch.json`
- Layer gate: do not start the native driver until the L0 deterministic gate passes
- Final proof order: failure canary, then success canary, then closeout
