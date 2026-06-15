# Session Handoff: VS Code Zoo Code Conversion

## Identity

- Source session reference: current Codex thread, user request at `2026-06-12T16:31:22Z`
- Destination label: `vscode-zoo-code-conversion`
- Handoff type: `new-lifecycle-thread`
- Target project or lifecycle: `arcanum` runtime and host-surface lifecycle
- Created for: prepare a new thread that can define, design, and plan how to convert or expose Arcanum for Zoo Code, the VS Code AI coding extension at `https://www.zoocode.dev/`.

## New Session Prompt

```text
Continue from arcanum/development/session-handoffs/20260612T163122Z-vscode-zoo-code-conversion-handoff.md.

Goal: make it possible to convert or expose Arcanum for Zoo Code, the open-source VS Code AI coding extension.

Start from the external Zoo Code evidence in this handoff. Preserve current Arcanum boundaries and do not mutate canonical sigils, spells, registries, or bootstrap behavior until the target surface is defined.

Recommended route:
1. Run `invoke define` for the Zoo Code conversion surface.
2. Use the resulting definition to decide whether the owner is `arcanum-bootstrap`, `sigil-runtime-installer`, `spellcraft`, or a new host-surface capability.
3. Only after define/design approval, use `invoke plan` or `task-session` for implementation.
```

## Route Rationale

- Recommended next route: `invoke define`
- Rationale: the user clarified Zoo Code as `https://www.zoocode.dev/`. A define-stage artifact can now capture the target install surface, generated file shape, validation evidence, non-goals, and success criteria before implementation starts.
- Lifecycle owner: `invoke` for the next authoring step; likely downstream owners are `sigil-runtime-installer`, `arcanum-bootstrap`, `spellcraft`, or a new VS Code host-surface capability.

## Context Builder Selection

| Obligation | Coverage | Selected Source | Why It Matters |
| --- | --- | --- | --- |
| O-001 Preserve the user's split reason. | covered | Current user prompt: `invoke handoff so its possible to convert arcanum to vs code zoo code` | The handoff must keep this as a lifecycle split toward a new conversion capability, not as immediate implementation. |
| O-002 Identify Arcanum's current canonical model. | covered | `README.md`: capability model, sigils, spells, lifecycle work, Codex usage, install profiles | Shows that Arcanum canonical behavior lives in sigils/spells and that host surfaces are generated from those sources. |
| O-003 Identify existing host/runtime surfaces. | covered | `framework/runtime/README.md`; `tools/bootstrap_arcanum.sh`; `arcana/sigil-runtime-installer/README.md` | Existing surfaces include repo Codex skills, personal Codex skills, Claude Code skills, GitHub Copilot instructions/skills, repo-local tools, observability, and legacy `.codex/commands`. |
| O-004 Avoid treating legacy Codex commands as the desired target by default. | covered | `README.md`; `arcana/sigil-runtime-installer/README.md` | Current guidance says native skills are preferred, while `.codex/commands/` is legacy compatibility only. |
| O-005 Ground Zoo Code as the target runtime surface. | covered | `https://www.zoocode.dev/`; `https://docs.zoocode.dev/`; `https://github.com/Zoo-Code-Org/Zoo-Code` | Zoo Code is an open-source VS Code AI coding extension with modes, custom modes, MCP support, and a Roo-compatible settings/rules model. |
| O-006 Keep implementation deferred until the target surface is defined. | covered | `spells/invoke/handoff.md`; `spells/invoke/templates/session-handoff/session-handoff.md` | Handoff mode prepares context and a start prompt; it does not mutate downstream lifecycle artifacts. |
| O-007 Identify likely generated Zoo Code artifacts. | covered | Zoo Code custom modes and custom instructions docs | Candidate outputs include project `.roomodes`, `.roo/rules/`, `.roo/rules-{modeSlug}/`, and optional `.roo/mcp.json` if Arcanum exposes MCP tools. |

Strict coverage: `pass`

## Selected Session Context

- Current user request
  - Obligation refs: O-001, O-005
  - Context summary: The user wants an Invoke handoff so a future session can make Arcanum convertible to Zoo Code.
- Zoo Code public site and docs
  - Obligation refs: O-005, O-007
  - Context summary: Zoo Code is a VS Code AI coding extension and open-source Roo Code continuation. Relevant surfaces include built-in and custom modes, BYOK/model-agnostic operation, MCP integration, review-before-edit diffs, and headless/terminal operation.
- Zoo Code custom modes docs
  - Obligation refs: O-007
  - Context summary: Project custom modes can live in `.roomodes`; mode fields include `slug`, `name`, `description`, `roleDefinition`, `groups`, `whenToUse`, and `customInstructions`. Tool groups include read, edit, command, and MCP, with optional file restrictions.
- Zoo Code custom instructions docs
  - Obligation refs: O-007
  - Context summary: Workspace rules can live in `.roo/rules/` or `.roorules`; mode-specific rules can live in `.roo/rules-{modeSlug}/` or `.roorules-{modeSlug}`. This maps naturally to generated Arcanum per-capability instruction packages.
- Zoo Code MCP docs
  - Obligation refs: O-007
  - Context summary: Zoo Code can use MCP servers and project-level `.roo/mcp.json` configuration. This is a candidate route if Arcanum should expose deterministic tools or resources rather than only prompt/mode instructions.
- `README.md`
  - Obligation refs: O-002, O-004
  - Context summary: Arcanum is a governed capability framework. Canonical capability behavior lives in tiered sigil and spell folders, with generated host surfaces in consuming repositories. Codex discovery uses repo-scoped `.agents/skills/`, and old `.codex/commands/` are compatibility adapters rather than the canonical skill surface.
- `framework/runtime/README.md`
  - Obligation refs: O-003
  - Context summary: Arcanum's durable runtime model separates orchestrator meaning, runtime handoff, host-specific adapters, and evidence. Host tools such as Codex, Claude, and Copilot are not the runtime model; they are thin surfaces over canonical sigils and spells.
- `tools/bootstrap_arcanum.sh`
  - Obligation refs: O-003
  - Context summary: Bootstrap currently supports install profiles including `personal-codex`, `repo-codex`, `repo-local`, `github-copilot`, `claude`, and `observability`. It writes Codex repo skills, Claude Code skills/subagent support, GitHub Copilot skill/instruction surfaces, local runtime config, and optional legacy command files.
- `arcana/sigil-runtime-installer/README.md`
  - Obligation refs: O-003, O-004
  - Context summary: Sigil Runtime Installer is scoped to explicit legacy Codex command adapters. Native runtime skill surfaces are owned by bootstrap profiles, not by this legacy command installer.
- `registry/SIGILS.md` and `registry/SPELLS.md`
  - Obligation refs: O-002
  - Context summary: Existing likely lifecycle owners include `sigil-runtime-installer`, `skill-transcriptor`, `skill-decomposer`, `spellcraft`, `task-session`, and the `arcanum-bootstrap` spell.

## Excluded Context

| Candidate | Reason Excluded |
| --- | --- |
| Full current chat transcript | Too broad; the actionable evidence is the user prompt plus selected repository sources. |
| Existing dirty worktree details | Important for local git hygiene, but not part of the conversion concept unless implementation starts. The next session should inspect `git status` live. |
| Local parent VS Code workspace color launchers | They show existing VS Code workspace files, but they are not an Arcanum conversion target or runtime surface. |
| Legacy `.codex/commands/` cleanup reports | Interesting history, but they do not answer what "VS Code Zoo Code" means. |

## Target Boundary

- In scope for the new thread:
  - Define the Zoo Code target surface for Arcanum.
  - Decide whether the output should be project `.roomodes`, `.roo/rules/`, mode-specific `.roo/rules-{modeSlug}/`, optional `.roo/mcp.json`, bootstrap profile support, or a separate documentation/install recipe.
  - Map existing Arcanum surfaces and choose the smallest responsible extension boundary.
  - Preserve canonical Arcanum sources as the authority: sigils, spells, framework, registry, templates, and bootstrap generation.
  - Identify validation evidence: generated surface smoke test, install dry run, YAML/JSON validation, link checks, Zoo Code manual import/proof, or headless Zoo Code proof if stable enough.
- Out of scope for the new thread:
  - Directly rewriting canonical sigils or spells before the target is defined.
  - Treating `.codex/commands/` as the default output just because it is a code-oriented surface.
  - Copying private consuming-repository context into public Arcanum artifacts.
  - Committing or pushing without first inspecting local status and separating unrelated work.
- Prior decisions to preserve:
  - Native host skills are preferred over nested model-backed CLI execution.
  - Legacy Codex command generation is explicit compatibility, not the default.
  - Bootstrap owns native generated surfaces for Codex, Claude Code, GitHub Copilot, repo-local runtime config, and observability.
  - Sigil Runtime Installer owns only explicit legacy Codex command adapters.

## Gaps And Blockers

| Gap | Owner | Status | Next Action |
| --- | --- | --- | --- |
| Exact generated artifact shape is not selected. | `invoke define` | open | Choose between `.roomodes`, `.roo/rules-*`, `.roo/mcp.json`, bootstrap profile extension, or a staged combination. |
| Target host-surface owner is not yet selected. | `invoke define` | open | Define candidate ownership: bootstrap profile extension, sigil-runtime-installer update, new spell, or new sigil. |
| Validation surface is unknown. | `invoke define` then `invoke design` | open | Decide what evidence proves the generated VS Code target works. |
| Implementation write scope is not known. | downstream plan owner | deferred | Do not mutate bootstrap/runtime code until define/design selects scope. |

## Next-Session Start Prompt

```text
Read arcanum/development/session-handoffs/20260612T163122Z-vscode-zoo-code-conversion-handoff.md.

Task: start a governed lifecycle for making Arcanum convertible or exposable to Zoo Code, the open-source VS Code AI coding extension at https://www.zoocode.dev/.

First, inspect current repo state and preserve unrelated changes:
- git status --short --branch
- rg -n "zoo code|zoocode|zoo-code|roo|roomodes|roorules|VS Code|vscode|github-copilot|claude|repo-codex|bootstrap" README.md framework runtime arcana spells tools registry .github 2>/dev/null || true

Then run an `invoke define` style pass with this target:
"Define the Zoo Code conversion surface for Arcanum: target users, generated `.roomodes` or `.roo/rules-*` package shape, optional MCP route, canonical source authority, install path, lifecycle owner, validation evidence, non-goals, and next route."

Do not implement until the define artifact selects the generated artifact shape and validation surface.
```

## Provenance

- Source refs:
  - current Codex user prompt at `2026-06-12T16:31:22Z`
  - `https://www.zoocode.dev/`
  - `https://docs.zoocode.dev/`
  - `https://docs.zoocode.dev/features/custom-modes`
  - `https://docs.zoocode.dev/features/custom-instructions`
  - `https://docs.zoocode.dev/features/mcp/using-mcp-in-roo`
  - `https://github.com/Zoo-Code-Org/Zoo-Code`
  - `README.md`
  - `framework/runtime/README.md`
  - `tools/bootstrap_arcanum.sh`
  - `arcana/sigil-runtime-installer/README.md`
  - `registry/SIGILS.md`
  - `registry/SPELLS.md`
  - `spells/invoke/handoff.md`
  - `spells/invoke/templates/session-handoff/session-handoff.md`
- Context Builder mode: `standard`
- Evidence date: `2026-06-12`
- Output path: `development/session-handoffs/20260612T163122Z-vscode-zoo-code-conversion-handoff.md`
- Context index: `development/session-handoffs/20260612T163122Z-vscode-zoo-code-conversion-context-index.json`

## Gate Result

- Status: `pass`
- Reason: the handoff has enough local and external context to start a new lifecycle thread, preserves the correct next route, and records remaining non-blocker design gaps around generated artifact shape and validation surface.
