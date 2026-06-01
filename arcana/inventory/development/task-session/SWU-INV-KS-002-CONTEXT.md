# Task Session Context: SWU-INV-KS-002

## Selected Unit

- Work-pack: `arcana/inventory/development/WORK-PACK.md`
- Task: `TASK-001`
- SWU: `SWU-INV-KS-002`
- Goal: promote the evidence-card authoring template into `arcana/inventory/templates/evidence-card.md`.

## Source Artifacts

- `arcana/inventory/development/work-pack/tasks/TASK-001-templates.md`
- `arcana/inventory/development/templates/evidence-card.md`
- `arcana/inventory/templates/evidence-card-schema.md`
- `arcana/inventory/development/POC-VALIDATION.md`

## Controlling Constraints

- Dependency `SWU-INV-KS-001` must be complete.
- Keep the write scope to `arcana/inventory/templates/evidence-card.md` plus task-session synchronization.
- The template must support both full and minimal cards.
- The template must preserve source refs, captured metadata, trace, residue, and update date.

## Gate Verdict

Pass. The dependency is complete, the production schema exists, and the validation command is available.

## Decision Pack

| Decision | Selected Option | Rationale |
| --- | --- | --- |
| Template shape | Provide separate full and minimal examples. | This makes the profile distinction concrete for authors and later lint checks. |
| Default profile | Default to `profile: full`. | POC cards are expected to support retrieval, handoff review, and residue. |
| Runtime | Local fallback. | This SWU is static artifact promotion. |
