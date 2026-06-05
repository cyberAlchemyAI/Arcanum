# Context Pack: SWU-CLEAN-004

Generated at: 2026-06-01T12:12:33Z

## Task Scope

- Work pack: `tools/development/CODEX-SKILL-SURFACE-CLEANUP-WORK-PACK.md`
- SWU: `SWU-CLEAN-004`
- Parent task: `TASK-CLEAN-004`
- User-selected decision route: `invoke refresh 1`, interpreted as final decision option 1 after evidence refresh.
- Runtime: local fallback.

## Controlling Sources

- `DECISIONS.md`
- `tools/development/CODEX-SKILL-SURFACE-CLEANUP-WORK-PACK.md`
- `tools/development/CODEX-SKILL-SURFACE-CLEANUP-DRY-RUN-20260601T115842Z.md`
- `tools/development/task-sessions/20260601T115930Z-swu-clean-004-option-2.md`
- `tools/arcanum-skill-surface-cleanup-report`

## Constraints

- Move generated personal duplicate packages to a timestamped backup, not hard-delete.
- Move generated legacy command files to a repository backup, not hard-delete.
- Preserve unknown entries:
  - `/mnt/c/Users/vlad_/.codex/skills/arcanum-orchestrate/SKILL.md`
  - `.codex/commands/arcanum-runtime-smoke.md`
- Keep short aliases and non-Arcanum skills.
- Validate by rerunning the cleanup inventory report after mutation.

## Cleanup Evidence

- Personal backup: `/mnt/c/Users/vlad_/.codex/skills/.cleanup-backups/20260601T120907Z/personal-skills/`
- Legacy command backup: `tools/development/cleanup-backups/20260601T120907Z/codex-commands/`
- Manifest: `tools/development/cleanup-backups/20260601T120907Z/manifest.txt`
- Post-cleanup report: `tools/development/CODEX-SKILL-SURFACE-CLEANUP-POST-CLEANUP-20260601T120907Z.md`

## Validation Summary

- Personal Codex skills: keep 44, remove candidates 0, unknown 1.
- Repository Codex skills: keep 0, remove candidates 0, unknown 0.
- Legacy Codex commands: keep 0, remove candidates 0, unknown 1.
- Backup counts: 40 personal generated packages and 84 generated legacy command files.

