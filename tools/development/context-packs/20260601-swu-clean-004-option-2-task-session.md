# Context Pack: SWU-CLEAN-004 Option 2

Generated at: 2026-06-01T11:59:30Z

## Task Scope

- Work pack: `tools/development/CODEX-SKILL-SURFACE-CLEANUP-WORK-PACK.md`
- Target: `SWU-CLEAN-004`
- User-selected decision option: 2, run another dry-run before live cleanup.
- Runtime: local fallback.

## Controlling Sources

- `DECISIONS.md`
- `tools/development/CODEX-SKILL-SURFACE-CLEANUP-WORK-PACK.md`
- `tools/arcanum-skill-surface-cleanup-report`
- `tools/development/CODEX-SKILL-SURFACE-CLEANUP-DRY-RUN.md`
- `tools/development/task-sessions/20260601T113112Z-swu-clean-003.md`

## Constraints

- Do not move, delete, or rewrite personal Codex-home packages in this option.
- Do not clean live repository `.codex/commands` in this option.
- Produce refreshed evidence only.
- Preserve unknown entries for manual review.
- Keep live cleanup blocked until final user approval.

## Decision Interpretation

The user selected option 2 from the recorded `SWU-CLEAN-004` decision gate. This resolves the preliminary evidence-refresh decision but does not approve destructive cleanup.

## Refreshed Evidence

- Report: `tools/development/CODEX-SKILL-SURFACE-CLEANUP-DRY-RUN-20260601T115842Z.md`
- Personal Codex skills: keep 44, remove candidates 40, unknown 1.
- Repository Codex skills: keep 0, remove candidates 0, unknown 0.
- Legacy Codex commands: keep 0, remove candidates 84, unknown 1.

## Remaining Gate

Final cleanup remains blocked until the user chooses one of:

1. backed-up full cleanup of generated personal duplicates plus generated repo legacy commands;
2. repository-only legacy command cleanup;
3. deferral/stop with compatibility debt accepted.

