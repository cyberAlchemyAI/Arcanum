# Goal Folder: SWU-GOAL-001 Spellcraft Validate

This folder packages a compact native Codex `/goal` command plus sidecar
context for executing `SWU-GOAL-001` from the goal spell plan.

## Files

| File | Purpose |
| --- | --- |
| `00-goal-command.md` | Pasteable native Codex `/goal` command. |
| `01-outcome.md` | Selected unit and completion condition. |
| `02-verification.md` | Evidence and receipt requirements. |
| `03-constraints-boundaries.md` | Write scope, source scope, and capability policy. |
| `04-iteration-stop.md` | Iteration and blocked stop rules. |
| `05-reporting.md` | Final report and extra-source reporting requirements. |
| `handoff-pack.md` | Strict Markdown handoff pack for the selected SWU. |
| `handoff-index.json` | Structured index for source contracts and policy. |
| `CODEX-GOAL-PROFILE.md` | Full codex-goal-profile result. |

## Start Here

Use `00-goal-command.md` as the native command. The runtime should then read
`CODEX-GOAL-PROFILE.md`, `handoff-pack.md`, and `handoff-index.json` before any
broader context.
