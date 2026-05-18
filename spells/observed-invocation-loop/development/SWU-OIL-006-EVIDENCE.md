# SWU-OIL-006 Evidence

## Scope

- Parent task: T-004
- Goal: document observed adapter contract and wrapper flow.
- Write scope:
  - `spells/observed-invocation-loop/README.md`
  - `.arcanum/runtimes/github-copilot/OBSERVED-INVOCATION.md`
  - `.arcanum/runtimes/github-copilot/skills/arcanum-orchestrate/SKILL.md`
  - `.arcanum/runtimes/github-copilot/skills/arcanum-sigil-signal-observer/SKILL.md`
  - `.arcanum/runtimes/github-copilot/skills/arcanum-spell-invoke/SKILL.md`

## Implemented Behavior

- Added an adapter contract section to the Observed Invocation Loop spell contract.
- Added runtime-local GitHub Copilot observed invocation contract.
- Added pilot metadata to the selected skill, sigil, and spell adapters.
- Locked pilot capability metadata:
  - skill: `arcanum-orchestrate`
  - sigil: `signal-observer`
  - spell: `invoke`
- Documented controls:
  - `OBSERVED_INVOCATION_STRICT=1`
  - `OBSERVED_REFLECT=off|auto|always`
- Documented that manual observer calls do not satisfy hook-enforcement evidence.

## Validation

Review checks:

- skill adapter declares `capability.kind = skill`,
- sigil adapter declares `capability.kind = sigil`,
- spell adapter declares `capability.kind = spell`,
- all three reference the runtime-local observed invocation contract,
- spell contract describes start, execute, envelope, observe, reflect, and closeout phases.

## Status

- SWU status: complete
- Parent task status: complete
- Next SWU: SWU-OIL-007
