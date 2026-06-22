# Codex Goal Profile Design

Status: initial transmutation design.

## Design Intent

Create a small transmutation that turns one selected Arcanum task, SWU, or explicit one-shot stream into a compact native Codex Goal.

The retired Arcanum `goal` spell tried to own orchestration, checkpoints, resume, status, and closeout. That is redundant with native Codex Goals. The useful remaining capability is profile generation: a compact `/goal` line plus sidecar context when the execution frame is too dense for the native goal budget.

## Source Runtime

Codex native Goals are persistent, thread-scoped objectives with lifecycle controls and evidence-based completion. They are managed through `/goal`, `/goal pause`, `/goal resume`, and `/goal clear`.

Official reference: <https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex>

## Transformation

Input:

- one work-pack task, SWU, or explicit one-shot stream,
- source links,
- dependencies,
- write scope,
- done criteria,
- validation surface,
- blockers,
- optional decision profile,
- optional one-shot capability policy,
- native goal character budget.

Output:

- one native Codex `/goal` command,
- optional sidecar profile/handoff artifact,
- readiness verdict,
- audit notes.

## Field Mapping

| Work-Pack Field | Codex Goal Field |
| --- | --- |
| Done criteria | Outcome |
| Validation | Verification surface |
| Write scope | Boundaries |
| Source links | Allowed context |
| Dependencies and blockers | Stop condition |
| Handoff note | Iteration policy |
| Decision profile policy | Constraints, approval gates, stop conditions |
| One-shot stream | Ordered iteration policy and capability lanes |
| Goal budget | Compact goal or sidecar requirement |

## Non-Goals

- Do not implement `/goal`.
- Do not own pause, resume, clear, or continuation.
- Do not execute work.
- Do not create a second dashboard beside `WORK-PACK.md`.
- Do not generate a runnable Goal when dependencies or validation are missing.
- Do not copy private decision-profile contents into public reusable artifacts.
- Do not authorize subagents or sigils as ambient authority; they must be bounded lanes with receipts.

## Next Route

Use [WORK-PACK.md](WORK-PACK.md) for implementation sequencing.
