## Distill Result

- Target context: Arcanum shared runtime infrastructure for refine/task-session and future orchestrators.
- Objective and output artifact: Find the smallest coherent implementation unit; output a runtime contract design.
- Mode and budget: standard
- Proposal tracks: 1 track; Proposer/Balancer role simulation in one agent.
- Recursive rounds: 2 / 2
- Verdict: pass
- Role conversation trace: Proposer selected "Durable Runtime Run Contract"; Balancer rejected scheduler-first and refine-only variants; reconciliation chose tools-level runner plus file-backed schema.
- Current smallest coherent unit: Runtime Run Contract, responsible for durable execution state and adapter invocation.
- Optimization point: Smaller than a full scheduler, larger than a Codex wrapper; it fixes both refine and task-session without overbuilding.
- Concept layer map: Arcanum workflow orchestration -> durable runtime infrastructure -> runtime run contract -> adapter invocation.
- Technique pack trace: abstraction-level guard passed; recomposition proof passed; evolution profile passed; frame-expiry note recorded; premortem triggered; navigable result check passed.
- Closure and recomposition proof: The runtime run contract closes around handoff, status, events, result, artifacts, and children; it recomposes into refine as stage child runs and into task-session as bounded task execution.
- Evolution profile: likely adapters beyond Codex, nested loop execution, and scheduler later; smallest extension boundary is adapter registry plus parent/child run metadata.
- Deferred complexity: background scheduler, remote queue, retry policy, and UI dashboard are deferred.
- Tension ledger: resolved `Codex runtime vs generic runtime`; resolved `handoff vs status`; unresolved only historical docs cleanup order.
- Premortem: likely failure is over-migrating historical Codex Goal material; guardrail is update active runtime paths first.
- Frame-expiry note: This optimization point expires if Arcanum needs concurrent distributed scheduling rather than local durable handoff folders.
- Navigation guide: Start with `tools/arcanum-runtime-run` dry-run adapter, then route `tools/arcanum --exec`, then migrate refine/task-session active contracts.
- Next route: invoke design

### Proposer/Balancer Trace

| Role | Claim or Objection | Evidence or Category | Reconciliation |
| --- | --- | --- | --- |
| Proposer | Add a generic runtime run contract. | Current refine/task-session coupling. | accept |
| Balancer | Do not build a scheduler first. | Premature complexity. | accept; use file-backed async status folders. |
| Balancer | Do not patch refine only. | Same runtime need appears in task-session. | accept; tools-level runner. |
| Proposer | Keep Codex as `codex-exec`. | Existing CLI path is useful but fragile. | accept with isolated per-run state. |

### Observability Closeout

- OBSERVATION: skipped
- LEDGER: n/a
- REFLECTION_TRIGGER: none
- RECOMMENDATION: continue-to-invoke-design
- DEDUPE_KEY: local-skill-contract-distill-20260525T165111Z
