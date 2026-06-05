# Context Pack: SWU-CLEAN-001

## Task

- Work-pack: `tools/development/CODEX-SKILL-SURFACE-CLEANUP-WORK-PACK.md`
- Task: `TASK-CLEAN-001`
- SWU: `SWU-CLEAN-001`

## Controlling Constraints

- Do not delete or move personal Codex packages.
- Do not delete or move repository `.codex/commands`.
- Classify keep/remove/unknown paths only.
- Preserve non-Arcanum personal skills such as `playwright`.
- Personal cleanup remains blocked until explicit user approval.

## Source Anchors

- `tools/development/CODEX-SKILL-SURFACE-CLEANUP-REFINE.md`
- `tools/development/CODEX-SKILL-SURFACE-CLEANUP-IMPLEMENTATION-LAYERING.md`
- `tools/development/CODEX-SKILL-SURFACE-CLEANUP-WORK-PACK.md`
- `/mnt/c/Users/vlad_/.codex/skills`
- `.agents/skills`
- `.codex/commands`

## Validation Surface

- `bash -n tools/arcanum-skill-surface-cleanup-report`
- `tools/arcanum-skill-surface-cleanup-report > tools/development/CODEX-SKILL-SURFACE-CLEANUP-DRY-RUN.md`

## Strict Coverage

Pass. The selected SWU only needs generated-provenance classification and a dry-run report; all required surfaces were inspected without deletion.
