# Plan Transport: Craft Feature Readiness Indexes

## Transport Status

- Status: `pass`
- Transport owner: `invoke`
- Target lifecycle owner: `arcana/craft`
- Transport mutation: none

## Transported Artifacts

- `INVOKE-DESIGN.md`
- `GLOSSARY-CONSISTENCY.md`
- `IMPLEMENTATION-LAYERING.md`
- `INVOKE-PLAN.md`
- `WORK-PACK.md`
- `work-pack/tasks/`
- `work-pack/waves/`

## Handoff Notes

- Future execution should start at `SWU-CFR-001`.
- The first execution owner should be `sigil-development --update craft` or a maintainer-approved `task-session`.
- Context Builder at execution time should select only the task-local files, canonical Craft sources, and the current git diff.
- No Necronomicon or canonical glossary mutation is requested by this transport.

## Residue

- Cross-sigil changes for Invoke and Refine remain open as separate lifecycle routes.
- A real Craft renderer/index generator remains deferred.
