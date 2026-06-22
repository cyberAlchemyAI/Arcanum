# Outcome: SWU-GOAL-001

## Selected Unit

- Source work-pack: `arcanum/spells/goal/development/invoke-runs/20260620T212656Z-goal-plan/WORK-PACK.md`
- Selected unit: `SWU-GOAL-001`
- Parent task: `TASK-GOAL-SPELLCRAFT-VALIDATE`
- Mode: single SWU, not one-shot stream
- Lifecycle owner: `spellcraft`

## Desired Result

Produce a Spellcraft lifecycle validation report for the `goal` spell
source/design/plan packet.

The report must return one of:

- `pass`: packet is coherent enough to proceed to later runtime SWUs.
- `flag`: packet can proceed only with named non-blocking gaps.
- `block`: packet must not proceed to runtime SWUs until named blockers are
  repaired.

## Completion Condition

The goal is complete when the validation report names evidence, verdict,
blockers or residue, and a next route. It must explicitly state whether runtime
SWUs remain blocked or can be selected next.
