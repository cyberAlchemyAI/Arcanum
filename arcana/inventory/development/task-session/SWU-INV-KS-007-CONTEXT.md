# Task Session Context: SWU-INV-KS-007

## Selected Unit

- Work-pack: `arcana/inventory/development/WORK-PACK.md`
- Task: `TASK-004`
- SWU: `SWU-INV-KS-007`
- Goal: add ontology and definitions handoff JSON examples.

## Source Artifacts

- `arcana/inventory/development/work-pack/tasks/TASK-004-handoff-examples.md`
- `arcana/inventory/development/INTERFACES.md`
- `arcana/inventory/development/FLOWS-POLICIES.md`
- `arcana/inventory/development/pilot/evidence-card/pilot-cards.json`
- `arcana/inventory/development/pilot/evidence-card/pilot-retrieval.json`

## Controlling Constraints

- Dependency `SWU-INV-KS-005` must be complete.
- Both packets must parse as JSON.
- Both packets must include source refs.
- Both packets must include explicit non-authority notices.
- Handoff examples must not imply downstream promotion.

## Gate Verdict

Pass. Pilot cards exist, the interface contract defines packet shape, and validation is available.

## Decision Pack

| Decision | Selected Option | Rationale |
| --- | --- | --- |
| Ontology packet | Use boundary and promotion-owner cards. | These stress ontology authority without promoting relations. |
| Definitions packet | Use EvidenceCard, EvidenceSet, retrieval, and authority terms. | These are likely shared terms but still need Definitions Governance. |
| Runtime | Local fallback. | This SWU is static JSON fixture authoring. |
