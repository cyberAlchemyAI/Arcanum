---
name: MOGT Harness Pending-All Composite Codex Goal Pack
description: One native Codex goal profile for executing pending MOGT harness tasks in dependency order.
created: 2026-06-08
---

# MOGT Harness Pending-All Composite Codex Goal Pack

Paste the command in `00-goal-command.md` as the native Codex `/goal`.

The command intentionally stays compact. It requires the goal runner to read
these part files in order:

1. `01-outcome.md`
2. `02-verification.md`
3. `03-constraints-boundaries.md`
4. `04-iteration-stop.md`
5. `05-reporting.md`

Source work-pack:

- `research/mogt-agentic-conversation/development/WORK-PACK.md`

Selected unit:

- `SWU-MOGT-HARNESS-002+003+004+005`

Composite context pack:

- Markdown: `research/mogt-agentic-conversation/development/context-mogt-harness-pending-all.md`
- JSON index: `research/mogt-agentic-conversation/development/context-mogt-harness-pending-all.index.json`

Stage goal packs:

- `research/mogt-agentic-conversation/development/goals/mogt-harness-002/`
- `research/mogt-agentic-conversation/development/goals/mogt-harness-003/`
- `research/mogt-agentic-conversation/development/goals/mogt-harness-004/`
- `research/mogt-agentic-conversation/development/goals/mogt-harness-005/`
