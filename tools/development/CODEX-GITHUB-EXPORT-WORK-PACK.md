---
module: codex-github-export
version: current
status: draft
updatedAt: 2026-06-01
docType: work-pack
---

# Work Pack: Codex/GitHub Export

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | L0/L1 mutation scope is local and validated by `/tmp` installs. |
| complexity | medium | Cross-surface installer and resolver behavior. |
| outputMode | single-file | Task files are not needed for the current two-SWU slice. |
| executionPackRef | n/a | Single-file work-pack is sufficient for this slice. |
| layeringArtifactRef | `tools/development/CODEX-GITHUB-EXPORT-IMPLEMENTATION-LAYERING.md` | Global layer model. |
| activeLayerWindow | L0-L1 | Export profile and resolver proof. |
| lastUpdatedAt | 2026-06-01 | Initial invoke plan. |
| readinessProfile | release-candidate | Target is easy export to fresh projects. |

## Objective Summary

- Objective: make Arcanum export cleanly to a new Codex and GitHub project.
- Primary inputs: export review, bootstrap profile contract, Codex `.agents/skills` guidance, native runtime package completeness result.
- Success condition: a fresh repository can install `.agents/skills`, `.github/skills`, repo-local runtime config, and resolve `refine` through `tools/arcanum` without legacy commands.

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-001 | Bootstrap writes repo-scoped Codex skill packages. | L0 | W0 | native package writer exists | staged `repo-codex` install contains canonical and alias skill packages |
| S-002 | Repo-local resolver recognizes native skill packages. | L1 | W0 | S-001 | staged `repo-local,repo-codex` install resolves `refine` without `.codex/commands` |
| S-003 | Export smoke covers GitHub/Copilot, personal Codex, Claude, and legacy compatibility. | L2 | W1 | S-001, S-002 | shell smoke commands pass |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TASK-EXPORT-001 | Add `repo-codex` install profile for `.agents/skills`. | L0 | medium | W0 | `tools/bootstrap_arcanum.sh` | ready | completed |
| TASK-EXPORT-002 | Resolve native skills in `tools/arcanum`. | L1 | medium | W0 | `tools/arcanum` | ready-after-TASK-EXPORT-001 | completed |
| TASK-EXPORT-VERIFY | Validate staged export surfaces. | L2 | medium | W1 | `/tmp` staged installs | ready-after-implementation | completed |

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Related Context | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-EXPORT-001 | TASK-EXPORT-001 | `tools/bootstrap_arcanum.sh` profile parsing and writer functions | README `.agents/skills` guidance | none | `tools/bootstrap_arcanum.sh` | `repo-codex` profile writes `.agents/skills` packages | `/tmp` install has `.agents/skills/refine/SKILL.md`; prefixed packages require `--prefixed-skill-packages` | `bash tools/bootstrap_arcanum.sh --target /tmp/... --profile repo-codex --sigils refine --spells none --force` | local-fallback | completed |
| SWU-EXPORT-002 | TASK-EXPORT-002 | `tools/arcanum` `--list`, `--resolve`, metadata detection | `.codex/commands` compatibility | SWU-EXPORT-001 | `tools/arcanum` | resolver returns `.agents/skills/refine/SKILL.md` when no legacy command exists | `tools/arcanum --resolve refine` passes in staged install without `.codex/commands` | staged resolver smoke | local-fallback | completed |
| SWU-EXPORT-003 | TASK-EXPORT-VERIFY | installer smoke commands | native package completeness result | SWU-EXPORT-001, SWU-EXPORT-002 | `/tmp/arcanum-export-*` only | profile matrix passes syntax and staged output checks | command transcript summarized in task result | `bash -n`; staged bootstrap commands; resolver commands | local-fallback | completed |

## Implementation Detail

### TASK-EXPORT-001

Add a profile name `repo-codex` accepted anywhere profiles are parsed. It writes generated native packages into `.agents/skills` using the existing generated package writer, with `arcanum-` canonical package names plus thin aliases such as `refine`.

The profile should create or preserve `AGENTS.md` with Codex guidance when missing. It must not require `--legacy-codex-commands`.

### TASK-EXPORT-002

Extend `tools/arcanum` so deterministic resolution can return either:

- `.codex/commands/<name>.md` for legacy commands, or
- `.agents/skills/<name>/SKILL.md` for native repo-scoped skills.

Resolution should prefer exact legacy commands when present for backward compatibility, then exact native skill packages. `--list` should include both surfaces without duplicates.

## Blockers

None for L0/L1. L3 remote GitHub proof is deferred until export-critical local changes are committed and pushed.

## Validation Strategy

```bash
bash -n tools/bootstrap_arcanum.sh
bash -n tools/arcanum
rm -rf /tmp/arcanum-export-codex-repo
bash tools/bootstrap_arcanum.sh --target /tmp/arcanum-export-codex-repo --profile repo-codex,repo-local,github-copilot,observability --sigils refine,context-builder --spells none --force
test -f /tmp/arcanum-export-codex-repo/.agents/skills/refine/SKILL.md
test -f /tmp/arcanum-export-codex-repo/.github/skills/arcanum-sigil-refine/SKILL.md
/tmp/arcanum-export-codex-repo/tools/arcanum --resolve refine
/tmp/arcanum-export-codex-repo/tools/arcanum --list
```

Validated on 2026-06-01 with staged `/tmp` installs:

- `bash -n tools/bootstrap_arcanum.sh`
- `bash -n tools/install_arcanum.sh`
- `bash -n tools/arcanum`
- `repo-codex,repo-local,github-copilot,observability` install with `refine,context-builder`
- alias-only repo Codex install with `tools/arcanum --resolve refine` returning `.agents/skills/refine/SKILL.md`
- `personal-codex` install compatibility
- legacy `.codex/commands` compatibility with `--legacy-codex-commands`

## Next Route

After L0/L1 validation passes, run `task-session` or a direct follow-up for L2/L3: export smoke script, README install recipe refresh, and remote GitHub archive proof.
