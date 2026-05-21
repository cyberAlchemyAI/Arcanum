# Sigil Runtime Installer

Sigil Runtime Installer installs Arcanum sigils and spells into the Codex command surface.

Arcanum now treats `.codex/commands/` as the installed runtime surface. Generated command files are full executable command contracts with embedded canonical snapshots; there is no `.arcanum/runtimes/` indirection and no GitHub Copilot skill bridge.

For each selected install, the installer creates one general `arcanum-orchestrate` command plus individual commands for every selected sigil and spell. Prefixed names use `arcanum-sigil-<id>` and `arcanum-spell-<id>` as stable compatibility names. Bare-id aliases such as `interrogation` or `invoke` are also full command files unless the alias would collide. When `ontology-harness` is selected, it creates `arcanum-ontology-harness`. When Necronomicon harness generation is enabled, it creates `arcanum-necronomicon`.

Generated Codex commands record their installed runtime with `arcanum:runtime codex`. Runtime-sensitive sigils may also declare adapter metadata. For example, `task-session` declares `arcanum:runtime-goal-adapter codex-goal` so it can translate a selected work-pack task or SWU into a native Codex `/goal` through the `codex-goal-profile` transmutation while preserving Task Session as the Arcanum coordinator.

## Problem It Solves

Arcanum stores canonical sigils and spells as framework artifacts, but Codex discovers repository slash commands from `.codex/commands/`. A registry is useful only when the selected capabilities are invokable from that local command surface.

Sigil Runtime Installer bridges that gap by generating Codex commands directly from canonical Arcanum artifacts, installing observer hooks, and validating that commands can run without generated `.arcanum/necronomicon/` registry files.

## Use When

- a repository should expose Arcanum sigils as Codex slash-command style commands,
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
| Codex | `.codex/commands/<command>.md` | Full command contract with observer task-zero block and embedded canonical snapshot |
| None | n/a | Observability and optional Necronomicon state only |

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
