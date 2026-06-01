# Refine Seed Proposal: Durable Runtime Interface

## Target

Design a generic Arcanum runtime system where refine and task-session no longer depend on Codex Goal or native `/goal`.

## Primary Question

Can Arcanum have a durable execution run model that can execute loops like refinement, including multiple or nested refinement loops, while keeping Codex as just one adapter?

## Model To Refine

```text
orchestrator -> async task handoff -> runtime translator -> runtime executor
```

## Constraints

- Codex is only a runtime adapter, probably `codex-exec`.
- The runtime must be generic enough for refine, task-session, and future Arcanum workflows.
- Native `/goal` and Codex Goal state must not be the core model.
- Durable runs must support parent/child relationships.
- Multiple refinement loops must be represented as sibling, nested, candidate, or repair loops.
- Each run must have durable artifacts, status, evidence, and blocked reasons.
- The Codex adapter must avoid shared database/state collisions through isolated per-run adapter state.
- Async execution can start as durable handoff/status folders; a scheduler can be future work.

## Canonical Loop

1. Context Builder evidence baseline.
2. Invoke Define.
3. Interrogation using `refine-review`.
4. Research decision / bounded research only if a named gap requires it.
5. Distill.
6. Invoke Redefine / Design.
7. Interrogation using `refine-design-review`.
8. Distill Repair.
9. Invoke Plan.
10. Final Interrogation and Synthesis.

## Desired Final Output

A handoff-quality implementation plan with:

- Summary
- Proposed runtime architecture
- Durable run folder contract
- Refine integration
- Task-session integration
- Multiple-loop model
- Adapter model, including Codex adapter boundaries
- Validation plan
- First implementation slice
- Open decisions only if genuinely unresolved
