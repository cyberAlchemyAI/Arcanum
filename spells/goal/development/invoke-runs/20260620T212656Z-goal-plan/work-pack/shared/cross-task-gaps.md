# Cross-Task Gaps: Goal Spell Plan

| Gap ID | Scope | Description | Owner | Repair Route | Blocks |
| --- | --- | --- | --- | --- | --- |
| G-GOAL-SCHEMA-HOME | schemas | Design schemas live in an Invoke run; stable public schema location is undecided. | spellcraft | Decide in SWU-GOAL-001. | Runtime schema imports. |
| G-GOAL-CRAFT-SYNC | Craft state | Craft ledger/view may lag the authored README and public schema. | craft/goal | Prepare staged proposal in SWU-GOAL-002. | Active source-state synchronization. |
| G-GOAL-RUNTIME-SOURCE | runtime | Exact runtime implementation files and installer path are not selected. | spellcraft | Select during W0 or first L1 Task Session. | Runtime write scope. |
| G-GOAL-FIXTURE-SET | validation | Low, medium, protected-mutation, and gap-discovery fixtures do not exist yet. | experiment-harness | Build in SWU-GOAL-009 after runtime behavior exists. | Registry readiness. |

## Gap Handling Rule

If a gap affects acceptance criteria for the selected SWU, stop or reroute. If
it affects a later layer, keep it visible and do not broaden the active SWU.
