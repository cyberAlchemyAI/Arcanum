# Sigilcraft Session Glossary

## Terms

| Term | Working Definition | Link Status | Notes |
| --- | --- | --- | --- |
| Sigilcraft | Proposed renamed lifecycle authority for creating, revising, validating, observing, reflecting on, and promoting sigils. | partial | Existing surface is `sigil-development`; rename is not approved yet. |
| Sigil Development | Current canonical sigil lifecycle authority at `arcana/sigil-development/`. | linked | Should remain as compatibility alias if `sigilcraft` becomes canonical. |
| Spellcraft | Arcana sigil for designing, installing, validating, observing, and revising spells. | linked | Parallel lifecycle authority for spells. |
| Craft session | A resumable process that carries an idea through refinement, artifacts, gates, validation, observation, and handoff. | no-match | Candidate concept introduced by this define run. |
| Stage | The current position in the craft lifecycle, such as start, refine, define, shape, validate, trial, observe, reflect, iterate, promote, or handoff. | partial | Related to existing lifecycle model but needs explicit state semantics. |
| Invoke | Spell that turns vague development intent into governed define, design, plan, full, validate, and handoff artifacts. | linked | Invoke prepares handoff context; it does not own sigil or spell lifecycle execution. |
| Task Session | Arcana sigil for executing one bounded task with scope, decisions, gates, validation, and evidence. | linked | Execution route after craft lifecycle gates make the work bounded. |
| Lifecycle authority | Capability that owns the rules for developing or maintaining a kind of artifact. | partial | Sigilcraft owns sigils; Spellcraft owns spells; Task Session owns bounded execution. |
| Session state | The resumable record of target, stage, artifacts, decisions, open gaps, validation, and next route. | no-match | Candidate state model for sigilcraft and possibly Spellcraft. |
| Artifact ledger | Stage-indexed record of artifacts produced, consumed, or updated during the session. | partial | Existing development artifacts use local paths; ledger semantics need design. |
| Decision ledger | Record of accepted assumptions, explicit choices, deferred gaps, and blockers. | partial | Could route blocker choices to decision-gate. |
| Compatibility alias | A retained old command or capability name that resolves to the new canonical capability during migration. | partial | Needed if `sigil-development` becomes `sigilcraft`. |
| Canonical id | Stable machine-facing identifier used in paths, registries, adapters, and telemetry. | linked | Changing it has runtime and compatibility consequences. |
| User-facing name | Human-facing label used in docs and explanations. | partial | Can change earlier than canonical ids if compatibility is preserved. |
| Handoff packet | A bounded artifact set prepared for another authority, such as invoke, spellcraft, decision-gate, or task-session. | partial | Existing invoke handoffs already follow this pattern. |
| Rename migration | Planned change from `sigil-development` to `sigilcraft` across docs, registry, commands, telemetry, and compatibility aliases. | no-match | Requires explicit approval and staged implementation. |

## Linking Summary

- linked: Sigil Development, Spellcraft, Invoke, Task Session, canonical id.
- partial: Sigilcraft, stage, lifecycle authority, artifact ledger, decision ledger, compatibility alias, user-facing name, handoff packet.
- no-match: craft session, session state, rename migration.

Candidate glossary promotion is not automatic. The no-match terms should remain local to this development session until the session model is validated.
