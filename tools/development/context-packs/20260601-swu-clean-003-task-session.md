# Context Pack: SWU-CLEAN-003

Generated at: 2026-06-01T11:31:12Z

## Task Scope

- Work pack: `tools/development/CODEX-SKILL-SURFACE-CLEANUP-WORK-PACK.md`
- SWU: `SWU-CLEAN-003`
- Parent task: `TASK-CLEAN-003`
- Objective: add a recoverable repository legacy `.codex/commands` cleanup path.
- Runtime: local fallback.

## Controlling Sources

- `tools/development/CODEX-SKILL-SURFACE-CLEANUP-WORK-PACK.md`
- `tools/development/CODEX-SKILL-SURFACE-CLEANUP-DRY-RUN.md`
- `tools/bootstrap_arcanum.sh`
- `tools/install_arcanum.sh`
- `README.md`

## Constraints

- Preserve native Codex skills as the normal Codex surface.
- Keep legacy `.codex/commands` generation explicit through `--legacy-codex-commands`.
- Cleanup must be recoverable by reinstalling with `--legacy-codex-commands`.
- Cleanup must only remove generated Arcanum command files and preserve unknown local command files.
- Do not mutate personal Codex home during this SWU.

## Decisions

- Add an explicit `--clean-legacy-codex-commands` flag instead of overloading `--force`.
- Use generated command marker `<!-- arcanum:command ... -->` as the deletion authority.
- Preserve unknown `.codex/commands/*.md` files and report them on stderr.
- Validate in staged `/tmp` repositories before any real cleanup.

## Validation Surface

- `bash -n tools/bootstrap_arcanum.sh`
- `bash -n tools/install_arcanum.sh`
- `bash -n tools/arcanum-skill-surface-cleanup-report`
- staged no-legacy install has no `.codex/commands`
- staged legacy install writes `refine.md`
- staged cleanup removes generated commands
- staged reinstall restores `refine.md`
- staged cleanup preserves an unknown local command file

