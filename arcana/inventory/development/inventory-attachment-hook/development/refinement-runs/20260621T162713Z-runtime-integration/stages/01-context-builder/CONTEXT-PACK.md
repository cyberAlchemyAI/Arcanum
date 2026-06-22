---
module: inventory-attachment-hook
runId: 20260621T162713Z-runtime-integration
stage: s1-context-builder
status: pass
updatedAt: 2026-06-21
docType: context-pack
---

# Context Pack: Runtime Integration For Chat Skill Invocation

## Task

Design how Inventory Attachment Hook integrates with Codex, Claude Code, and
generic runtimes when a managed Arcanum skill or spell is invoked through chat.

Editor UI surfaces, including VS Code and Cursor panels, are deferred.

## Obligation Coverage

| Obligation | Status | Evidence |
| --- | --- | --- |
| Model the shared runtime contract. | covered | `ARCHITECTURE.md`, `SPEC.md`, `observed-invocation-loop/README.md` |
| Make chat-invoked skills the proof surface. | covered | `REFINE-SEED-PROPOSAL.md`, `ARCHITECTURE-OVERVIEW.md` direct skill gap |
| Preserve Codex, Claude Code, and generic runtime lanes. | covered | `bootstrap_arcanum.sh`, `.agents/skills/`, `.claude/skills/`, `.arcanum/runtime/config.json` |
| Keep generated mirrors non-authoritative. | covered | `ARCHITECTURE.md`, `WORK-PACK.md`, generated package frontmatter |
| Attach only candidate Inventory evidence. | covered | `SPEC.md` policy and handoff envelope |
| Preserve observability before Inventory attachment. | covered | `ARCHITECTURE.md` runtime order, OIL execution phases |
| Avoid VS Code interface scope. | resolved | operator clarification and dispatch guardrail |

## Selected Evidence

| Source | Selected Reason |
| --- | --- |
| `arcanum/arcana/inventory/development/inventory-attachment-hook/ARCHITECTURE.md` | Defines `AttachedInventoryHandoff`, runtime order, authority split, failure semantics, recursion guard, and generated mirror strategy. |
| `arcanum/arcana/inventory/development/inventory-attachment-hook/SPEC.md` | Defines `inventoryAttachment`, handoff envelope, validation, idempotency, public-boundary resolution, and OIL insertion point. |
| `arcanum/arcana/inventory/development/inventory-attachment-hook/WORK-PACK.md` | Names implementation slices and gates; runtime automation waits until contract/template stabilization. |
| `arcanum/spells/observed-invocation-loop/README.md` | Defines managed invocation closeout, hook-first observability, native runtime contract, and generated markers. |
| `arcanum/framework/observability/ARCHITECTURE-OVERVIEW.md` | Identifies the current direct `$skill-name` observation gap and recommends a skill-aware observation bridge. |
| `.codex/hooks/arcanum-user-prompt-submit.sh` | Shows current hook detection is command-oriented through `.codex/commands`. |
| `.codex/hooks/arcanum-stop.sh` | Shows closeout envelope finalization and observer append path for hook-managed runs. |
| `.claude/agents/arcanum-stage-worker.md` | Shows Claude Code stage worker receipt expectations for bounded dispatch stages. |
| `.arcanum/runtime/config.json` | Shows enabled native-skill, codex-skill, claude-skill, local-skill, and dry-run adapters. |

## Key Inference

The existing architecture already defines where Inventory Attachment belongs:
after observed invocation envelope assembly and primary telemetry handling, before
final closeout. The missing runtime design detail is how a chat-hosted `$skill`
invocation reliably creates its own envelope and closeout evidence.

## Strict Coverage

`pass`: all obligations are covered by local repository evidence. No external
research is needed for this design pass.
