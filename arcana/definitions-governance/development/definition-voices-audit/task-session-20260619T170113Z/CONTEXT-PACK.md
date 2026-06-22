# Context Pack: SWU-DVA-001

## Context Pack Summary

- Task: `SWU-DVA-001`
- Mode: lean
- Files selected: 7
- Snippets selected: 12
- Obligation coverage: 100%
- Noise ratio: low
- Output markdown: this file
- Output index: none
- Handoff pack: none
- Session evidence path: `arcana/definitions-governance/development/definition-voices-audit/task-session-20260619T170113Z/`
- Strict coverage: n/a
- Blockers: 0

## Obligations

| ID | Obligation | Evidence |
| --- | --- | --- |
| O1 | Preserve canonical definition authority and stable IDs. | `definitions/DEFINITIONS.md` authority rule and indexed headings. |
| O2 | Ensure every current definition has scientific/formal, plain-language, and domain-context voices. | `arcana/definitions-governance/SKILL.md` definition-voice-model. |
| O3 | Keep DomainSpec explanatory layers non-authoritative. | `definitions/TAXONOMY.md` and `definitions/RELATIONSHIPS.md` explanatory-layer notices. |
| O4 | Keep domain context local to Arcanum and optionally tied to `development/user-guide/`. | `definitions-governance` contract and `development/user-guide/README.md`. |
| O5 | Keep execution bounded to the SWU write scope and validate with diff/link/voice checks. | `WORK-PACK.md` SWU handoff. |

## Included Context

- `arcana/definitions-governance/SKILL.md`
  - Why included: controlling sigil contract for the three-voice migration.
  - Selectors: `<definition-voice-model>`, `<process>` steps 5 and 9, `<quality-bar>`.
  - Obligations: O2, O4.

- `definitions/DEFINITIONS.md`
  - Why included: canonical source to mutate.
  - Selectors: Authority Rule; headings `DEF-ARC-CONTRACT`, `DEF-ARC-SCHEMA`, `DS-D1`, `DS-D2`, `DS-D3`, `DS-D7`, `DS-D8`, `DS-D10`, `DS-P1`, `DS-P2`, `DS-P3`.
  - Obligations: O1, O2.

- `definitions/DEFINITIONS-INDEX.md`
  - Why included: indexed definition set and anchor stability reference.
  - Selectors: Terms table and Governance Notes.
  - Obligations: O1, O5.

- `definitions/DEFINITION-DRIFT-AUDIT.md`
  - Why included: existing downstream drift boundary and place to record this audit result.
  - Selectors: Result table, Boundary.
  - Obligations: O3, O5.

- `definitions/TAXONOMY.md`
  - Why included: DomainSpec meta-type explanatory layer for DS-D1 domain context.
  - Selectors: opening explanatory-layer notice and overview.
  - Obligations: O3, O4.

- `definitions/RELATIONSHIPS.md`
  - Why included: DomainSpec edge explanatory layer for DS-D2, DS-D7, and DS-D8 domain context.
  - Selectors: opening explanatory-layer notice and overview.
  - Obligations: O3, O4.

- `development/user-guide/README.md`
  - Why included: Arcanum reader-facing domain-context surface.
  - Selectors: three-part model, translation meaning, current local artifacts, boundary rules.
  - Obligations: O4.

## Execution Constraints

- Do not mutate generated runtime skill packages.
- Do not rename definition IDs or heading anchors.
- Do not promote local glossary terms.
- Do not remediate downstream drift outside `definitions/` in this SWU.
- Plain-language and domain-context voices must remain non-normative.

## Next Actions

1. Add or normalize three voice markers for every indexed definition.
2. Sync index governance notes.
3. Append audit result to `DEFINITION-DRIFT-AUDIT.md`.
4. Run validation checks and write the task-session report.
