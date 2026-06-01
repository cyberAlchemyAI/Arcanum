# Stage 5: Distill

## Verdict

`pass`

## Selected Design Unit

**Runtime Run Contract**

This is the smallest coherent unit that fixes both refine and task-session without overbuilding a scheduler.

## Key Distillation

Do not start by creating a new high-level skill. Start by creating a durable runtime contract and a tools-level runner.

## What To Preserve

- Refine's ten-stage loop.
- Stage-owned artifacts.
- Target-local run manifests.
- Task-session's bounded task/SWU contract.
- Context Builder's strict evidence-pack idea.

## What To Remove From Active Runtime Path

- `GOAL-HANDOFF.md`
- native `/goal`
- `codex-goal` as canonical adapter
- shared `.arcanum/codex-home` for nested runtime executions

## Minimal V1

- `tools/arcanum-runtime-run`
- `.arcanum/runtime/runs/<run-id>/`
- `RUNTIME-HANDOFF.md`
- adapters: `dry-run`, `codex-exec`
- parent/child run ids
- runtime status artifacts
