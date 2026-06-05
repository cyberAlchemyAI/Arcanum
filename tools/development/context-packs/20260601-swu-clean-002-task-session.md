# Context Pack: SWU-CLEAN-002

## Task

- Work-pack: `tools/development/CODEX-SKILL-SURFACE-CLEANUP-WORK-PACK.md`
- Task: `TASK-CLEAN-002`
- SWU: `SWU-CLEAN-002`

## Controlling Constraints

- Make short aliases the only default Codex discovery-surface packages.
- Do not delete personal Codex packages or repository command files.
- Preserve explicit compatibility through a flag.
- Alias packages must be self-sufficient; they cannot point at absent `arcanum-*` packages.
- `interrogation` should be the visible alias for `structured-interview-kits`.

## Source Anchors

- `tools/bootstrap_arcanum.sh`
- `tools/development/CODEX-SKILL-SURFACE-CLEANUP-WORK-PACK.md`
- `tools/development/CODEX-SKILL-SURFACE-CLEANUP-DRY-RUN.md`
- `README.md`
- `tools/install_arcanum.sh`

## Validation Surface

- `bash -n tools/bootstrap_arcanum.sh`
- `bash -n tools/install_arcanum.sh`
- staged `personal-codex` install under `/tmp/arcanum-alias-only-personal`
- staged `repo-codex,repo-local` install under `/tmp/arcanum-alias-only-repo`
- staged compatibility install under `/tmp/arcanum-prefixed-compat`

## Strict Coverage

Pass. The task is fully covered by generator behavior and `/tmp` staged install outputs.
