# Codex Goal Profile Design

Status: initial transmutation design.

## Design Intent

Create a small transmutation that turns one selected Arcanum task or SWU into a native Codex Goal.

The retired Arcanum `goal` spell tried to own orchestration, checkpoints, resume, status, and closeout. That is redundant with native Codex Goals. The useful remaining capability is profile generation.

## Source Runtime

Codex native Goals are persistent, thread-scoped objectives with lifecycle controls and evidence-based completion. They are managed through `/goal`, `/goal pause`, `/goal resume`, and `/goal clear`.

Official reference: <https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex>

## Transformation

Input:

- one work-pack task or SWU,
- source links,
- dependencies,
- write scope,
- done criteria,
- validation surface,
- blockers.

Output:

- one native Codex `/goal` command,
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

## Non-Goals

- Do not implement `/goal`.
- Do not own pause, resume, clear, or continuation.
- Do not execute work.
- Do not create a second dashboard beside `WORK-PACK.md`.
- Do not generate a runnable Goal when dependencies or validation are missing.

## Next Route

Use [WORK-PACK.md](WORK-PACK.md) for implementation sequencing.
