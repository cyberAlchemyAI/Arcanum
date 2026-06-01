# Invoke Refresh Report: Guide First Spellcraft Target

## Invoke Result

- Mode: `refresh`
- Spell: invoke
- Canonical ID: invoke
- Scope: `development/user-guide/packages/guide/`
- Phase status: `pass`
- Mode contract: `spells/invoke/refresh.md`
- Mutation mode: `apply-approved`
- Evidence date: `2026-05-29`
- Next route: `spellcraft`

## Refresh Signals

| ID | Type | Source | Claim | Confidence | Mutation Safety |
| --- | --- | --- | --- | --- | --- |
| RS-GUIDE-001 | blocker_resolved | user request `invoke refresh 1` | User selected option 1 from `GUIDE-B-003`: `guide-architecture`. | high | safe |
| RS-GUIDE-002 | status_changed | `DECISIONS.md` | Decision record should move from unresolved/block to selected/pass. | high | safe |
| RS-GUIDE-003 | route_changed | `SPELLCRAFT-HANDOFF.md` | Next spellcraft route should target `guide-architecture`, not generic `guide`. | high | safe |

## Applied Changes

| Artifact | Change |
| --- | --- |
| `DECISIONS.md` | Marked `GUIDE-B-003` as `pass`, selected `guide-architecture`, and recorded rationale. |
| `WORK-PACK.md` | Changed Guide work-pack gate to `pass`, marked `GUIDE-004` completed, and resolved `GUIDE-B-003`. |
| `SPELLCRAFT-HANDOFF.md` | Updated recommended route to `spellcraft` for `guide-architecture`. |
| `task-session-GUIDE-004.md` | Updated validation/gate verdict to `PASS`. |

## Skipped Changes

- No spellcraft artifacts were created.
- No runtime command or registry entry was installed.
- Deferred budget/callable-capability decisions remain for spellcraft design.

## Validation

| Check | Result |
| --- | --- |
| Decision record contains selected option `guide-architecture`. | pass |
| Guide work-pack gate is `pass`. | pass |
| Spellcraft handoff targets `guide-architecture`. | pass |

## Next Route

Run `spellcraft` for `guide-architecture`.
