# Sigil Runtime Installer

Sigil Runtime Installer installs explicit legacy Codex command adapters for Arcanum sigils and spells.

Arcanum now treats native runtime skills as the default installed runtime surface. `.codex/commands/` is legacy compatibility only. Generated command files are full executable command contracts with embedded canonical snapshots; there is no `.arcanum/runtimes/` indirection and no GitHub Copilot skill bridge.

For each explicit legacy command install, the installer creates one general `arcanum-orchestrate` command plus individual commands for every selected sigil and spell. Prefixed names use `arcanum-sigil-<id>` and `arcanum-spell-<id>` as stable compatibility names. Bare-id aliases such as `interrogation` or `invoke` are also full command files unless the alias would collide. When `ontology-harness` is selected, it creates `arcanum-ontology-harness`. When Necronomicon harness generation is enabled, it creates `arcanum-necronomicon`.

Generated Codex commands record their installed runtime with `arcanum:runtime codex`. Runtime-sensitive sigils may also declare adapter metadata. For example, `task-session` declares `arcanum:runtime-goal-adapter codex-goal` so it can translate a selected work-pack task or SWU into a native Codex `/goal` through the `codex-goal-profile` transmutation while preserving Task Session as the Arcanum coordinator.

## Problem It Solves

Arcanum stores canonical sigils and spells as framework artifacts, and current runtimes should discover them through generated native skill packages. Some repositories may still need Codex slash-command compatibility from `.codex/commands/`.

Sigil Runtime Installer bridges that legacy gap by generating Codex commands directly from canonical Arcanum artifacts, installing observer hooks, and validating that commands can run without generated `.arcanum/necronomicon/` registry files.

## Use When

- a repository explicitly still needs Arcanum sigils as Codex slash-command style commands,
- a consuming repository should install selected Arcanum capabilities without runtime adapter folders,
- installed commands need observer-envelope-first telemetry,
- command wrappers need validation.

Generated commands use their embedded canonical instruction snapshots and the observer envelope task-zero contract. Necronomicon is the persistent repository harness, not a generated definition-storage folder.

## Do Not Use When

- the user only wants to read the registry,
- the repository should not receive Codex command files,
- the requested install would make local generated commands authoritative over canonical sigils.

## Supported Targets

| Target | Command Surface | Generated Shape |
| --- | --- | --- |
| Codex commands | `.codex/commands/<command>.md` | Legacy command contract with observer task-zero block and embedded canonical snapshot |
| None | n/a | Observability and optional Necronomicon state only |

This sigil owns only the legacy `.codex/commands/` surface. Native runtime skill
surfaces are owned by `tools/bootstrap_arcanum.sh` profiles.

## Claude Code surface (owned by `bootstrap --profile claude`)

`tools/bootstrap_arcanum.sh --profile claude` generates `.claude/skills/<name>/SKILL.md`
for every sigil and spell plus `.claude/agents/arcanum-stage-worker.md`. At generation
time the canonical Arcanum tool vocabulary is mapped to real Claude Code tool names so
the generated `allowed-tools` are valid (sources are never edited):

| Canonical (source) | Claude (generated) |
| --- | --- |
| `Task` | `Agent` |
| `AskQuestions` | `AskUserQuestion` |
| all others (`Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep`) | unchanged |

The generated surface is validated by `tools/validate-claude-skills.sh`, which blocks an
install (and fails CI) if any package has a non-Claude tool name, a `name` that does not
match its directory, a missing description, or a dangling `skills:` reference. Regenerate
and validate with `make claude-skills` (optionally `TARGET=<repo>`).

## Output

The sigil can produce:

- target selection report,
- install manifest,
- Codex command files,
- Codex hook files,
- runtime metadata and runtime-goal adapter declarations,
- validation report.

## Why This Is Arcana

The sigil coordinates command generation, local path decisions, canonical snapshot embedding, observer hook installation, validation, and installation reporting across repository boundaries.
