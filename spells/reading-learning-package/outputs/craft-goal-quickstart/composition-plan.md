# Composition Plan — Craft + Goal Quickstart (learning_distill)

- **Spell:** whisper (composition authority) · packaged as a reading-learning-package output
- **Preset:** `learning_distill` (Feynman / Veritasium voice)
- **Transport:** learning_package (non-conversion)
- **Length target:** ~1,200–1,600 words, compact

## Narrative anchor

> AI coding agents are brilliant but amnesiac. **Craft** is the logbook that gives
> the project a memory. **Goal** is the autopilot that reads the logbook, does the
> safe work, and stops at the toll booth (your approval) for anything risky. A
> **controller agent** is the expedition leader who can run the whole thing for you.

One analogy — an **expedition** — carried from start to finish.

## Section plan

| # | Part | Job | Source anchors |
| - | ---- | --- | -------------- |
| 1 | The amnesia problem | Hook with the counterintuitive problem | craft/README.md (durable memory across sessions) |
| 2 | Craft = the logbook | Concrete mechanism: YAML ledger + human view, rows for blockers/decisions/gaps/next moves | craft/SKILL.md (storage, core methods), craft/README.md |
| 3 | Goal = the autopilot | Read frontier → classify risk → dispatch → **stop at approval** | goal/SKILL.md (control spine, gates, failure policy) |
| 4 | The pipeline | How log + autopilot compose into a hands-off-but-safe loop | goal/SKILL.md (shared state, phases) |
| 5 | The 5-minute recipe | Copy-pasteable first run: `craft start` → add a next move → run the goal loop | craft/SKILL.md (start_project, next), goal README |
| 6 | The conductor | Controller agent (Hermes / OpenClaw) directing Claude Code / Codex / itself | integration-spec OpenClaw RESULT.md |
| 7 | Honest limits | Fail-closed; stops on risk/unknown/approval; not magic | goal/SKILL.md (failure policy) |
| 8 | Source sheet | Where every claim came from | all of the above |

## Voice rules (from preset)

- Define every term on first use, in one clause, then use it.
- Exactly one running analogy. Mark analogies as the author's framing.
- Never say "fully automatic." The honest, memorable beat is: *the magic is that it knows when to stop.*
- End with the single smallest next command.

## Validation checklist

- [ ] One analogy, carried end to end
- [ ] No undefined jargon
- [ ] Recipe is ordered and copy-pasteable
- [ ] Fail-closed behavior stated honestly
- [ ] Controller framed as optional
- [ ] Source trace complete
