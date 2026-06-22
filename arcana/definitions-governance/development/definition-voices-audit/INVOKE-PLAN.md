# Invoke Plan: Definitions Governance Definition Voices Audit

## Intent

Plan the next lifecycle step for `definitions-governance`: audit
`definitions/DEFINITIONS.md` for actual three-voice completeness and prepare one
Task Session-ready SWU to perform the migration.

## Mode

- Spell: `invoke`
- Mode: `plan`
- Mode contract: `.agents/skills/invoke/plan.md`
- Target artifact owner: `definitions-governance`
- Next lifecycle owner: `task-session`

## Template And Profile Selection

| Template/Profile | Selected | Evidence |
| --- | --- | --- |
| `implementation-layering` companion | yes | Invoke plan requires a layering artifact; scope has a clear L0 migration and deferred L1-L3 hardening. |
| `work-pack` companion | yes | Task Session needs a bounded executable task/SWU with write scope and validation. |
| split execution pack | no | Low complexity: one canonical source, one index, one SWU, no cross-repo execution. |

## Planning Context Summary

| Source | Role |
| --- | --- |
| [../../SKILL.md](../../SKILL.md) | Defines required scientific/formal, plain-language, and domain-context voices. |
| [../../../../definitions/DEFINITIONS.md](../../../../definitions/DEFINITIONS.md) | Canonical definitions source to audit and update. |
| [../../../../definitions/DEFINITIONS-INDEX.md](../../../../definitions/DEFINITIONS-INDEX.md) | Indexed definition set and anchor stability reference. |
| [../../../../definitions/DEFINITION-DRIFT-AUDIT.md](../../../../definitions/DEFINITION-DRIFT-AUDIT.md) | Existing drift boundary and deferred downstream remediation. |
| [../../../../definitions/TAXONOMY.md](../../../../definitions/TAXONOMY.md) | DomainSpec meta-type explanatory layer. |
| [../../../../definitions/RELATIONSHIPS.md](../../../../definitions/RELATIONSHIPS.md) | DomainSpec relationship explanatory layer. |
| [../../../../development/user-guide/README.md](../../../../development/user-guide/README.md) | Arcanum reader-facing domain-context surface. |

## Outputs

- [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md)
- [WORK-PACK.md](WORK-PACK.md)
- [PLAN-TRANSPORT.md](PLAN-TRANSPORT.md)

## Decisions

| Decision | Selected Option | Rationale |
| --- | --- | --- |
| Definition voice shape | Use explicit voice headings or lines per definition. | Makes audits repeatable and reader-visible. |
| Scope | L0 canonical definitions migration only. | Downstream drift remediation is larger than the immediate next lifecycle step. |
| Execution boundary | One local Task Session SWU. | Write scopes overlap and should not be parallelized. |

## Validation Strategy

- Run `git -C arcanum diff --check`.
- Run local markdown link checks for `definitions/DEFINITIONS.md` and
  `definitions/DEFINITIONS-INDEX.md`.
- Run a voice-completeness check that verifies every indexed definition ID has
  scientific/formal, plain-language, and domain-context voice markers.

## Next Route

Run `task-session` on `SWU-DVA-001` in [WORK-PACK.md](WORK-PACK.md).
