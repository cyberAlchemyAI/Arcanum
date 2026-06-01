# Runtime Glossary

## Terms

| Term | Status | Definition |
| --- | --- | --- |
| Orchestrator | linked | Arcanum capability that owns workflow meaning, stage order, safety gates, and final synthesis. |
| Async task handoff | linked | Immutable request artifact describing objective, inputs, scope, expected outputs, validation, blocked conditions, and adapter preference. |
| Runtime translator | linked | Component that transforms a generic handoff into an adapter-specific execution request. |
| Runtime executor | linked | Shared runner that owns durable run folders, status, events, adapter invocation, and result capture. |
| Adapter | linked | Concrete execution implementation, such as `dry-run` or `codex-exec`. |
| Runtime run | linked | Durable execution folder under `.arcanum/runtime/runs/<runtime-run-id>/`. |
| Loop topology | linked | Runtime metadata that represents root, stage, candidate, nested, repair, and continuation relationships. |
| Codex Goal | deprecated | Native `/goal` runtime concept; not part of the new Arcanum runtime core. |
| `codex-exec` | linked | Codex CLI adapter that runs `codex exec` with isolated per-run state. |
| `dry-run` | linked | Adapter that validates handoff and writes runtime artifacts without external execution. |
| `RUNTIME-HANDOFF.md` | linked | Generic runtime handoff artifact replacing active refine `GOAL-HANDOFF.md` requirements. |

## Glossary Consistency

- `Codex Goal`, `/goal`, and `codex-goal` are legacy terms for this project.
- Active runtime architecture should use `runtime handoff`, `runtime run`, `runtime executor`, and `adapter`.
- Historical references may remain in old development evidence when clearly marked as historical or deprecated.
