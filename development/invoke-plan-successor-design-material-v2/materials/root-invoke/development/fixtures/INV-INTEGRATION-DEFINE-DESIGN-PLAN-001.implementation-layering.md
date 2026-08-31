# Implementation Layering: Mars Rover Maintenance Log

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 (POC) | After this layer, we know whether daily inspection notes can preserve component status. | planned record shape | daily inspection note and component status | governance and release packaging | fixture replay | continue when source terms are preserved |
| L1 | After this layer, we know whether operator decisions are repeatable. | planned review workflow | operator decision path | audit controls | expected output check | harden when workflow is repeatable |
| L2 | After this layer, we know whether governance holds. | validation policy | blocker and repair question tracking | release packaging | validation report | defer |
| L3 | After this layer, we know whether packaging is credible. | release checklist | package handoff | future rollout | release evidence | defer |

## Recommended Next Layer

- Next layer: L0
- Key decision unlocked: daily inspection note and component status planning works.
- Major deferred scope: governance and release packaging.
