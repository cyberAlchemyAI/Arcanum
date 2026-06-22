---
module: inventory-attachment-hook
runId: 20260621T162713Z-runtime-integration
status: strategy-proposed
updatedAt: 2026-06-21
docType: refine-seed-proposal
observerRunId: arcanum-hook-019eeb01-bfb3-72a1-bc09-871666bb0eae
---

# Refine Seed Proposal: Runtime Integration Model And Design

## Operator Intent

```text
/refine we should model and design how this integrates with claude code, codex, and generic runtimes
```

## Scope Clarification

The immediate proof surface is native skill invocation through the current chat
surface, for example invoking `$refine`, `$inventory`, or another managed skill
from conversation. VS Code, Cursor, editor panels, and command-palette UX are
host-interface projections and are deferred unless separately requested.

## Target

`arcanum/arcana/inventory/development/inventory-attachment-hook/`

## Desired Outcome

Produce a runtime integration model and design for Inventory Attachment Hook
across three runtime surfaces:

- Codex;
- Claude Code;
- generic runtimes.

The model should prove integration by showing what happens when a chat-hosted
agent invokes a managed skill or spell, then closes the invocation with
observability and Inventory Attachment evidence.

Target final artifacts after confirmation:

- `arcanum/arcana/inventory/development/inventory-attachment-hook/RUNTIME-INTEGRATION-MODEL.md`
- `arcanum/arcana/inventory/development/inventory-attachment-hook/RUNTIME-INTEGRATION-DESIGN.md`

## Source Context

Primary local evidence:

- `ARCHITECTURE.md`
- `SPEC.md`
- `WORK-PACK.md`
- `arcanum/spells/observed-invocation-loop/README.md`
- `arcanum/framework/observability/SIGIL-OBSERVABILITY-HOOK.md`
- `arcanum/tools/bootstrap_arcanum.sh`
- `.agents/skills/observed-invocation-loop/README.md`
- `.claude/skills/observed-invocation-loop/README.md`
- `.claude/agents/arcanum-stage-worker.md`
- `.codex/hooks.json` and `.codex/hooks/` when present
- `.arcanum/runtime/config.json` when present

## Refinement Questions

1. What is the runtime-agnostic contract that all host runtimes must satisfy?
2. What is Codex-specific, and what should remain generic?
3. What is Claude Code-specific, including skill and subagent surfaces?
4. What does a generic runtime need to provide when it has no native hook API?
5. What must happen when a user invokes a skill from chat and the skill closes?
6. Where does Inventory Attachment run relative to observed invocation telemetry?
7. What generated package metadata or markers should be shared across runtimes?
8. What validation proves a runtime integration without relying on agent memory?

## Write Scope

Allowed after confirmation:

- this refinement run evidence folder;
- `RUNTIME-INTEGRATION-MODEL.md`;
- `RUNTIME-INTEGRATION-DESIGN.md`;
- optional stage drafts under `stages/`.

Not allowed in this refine run:

- canonical source mutation;
- generated mirror regeneration;
- hook script implementation;
- changes to `.agents/skills/`, `.claude/skills/`, `.codex/hooks/`, or
  `tools/arcanum`;
- pilot runtime execution;
- VS Code, Cursor, editor panel, or command-palette interface design.

## Preset And Research

| Field | Value |
| --- | --- |
| preset | standard |
| researchMode | research-if-gap-appears |
| externalResearch | not approved |
| subagentStrategy | recommended, requires user permission |

## Done Criteria

- The dispatch route validates before execution.
- The design separates host runtime duties from Arcanum capability duties.
- Codex, Claude Code, and generic runtime lanes are modeled with shared and
  runtime-specific requirements.
- The design names chat skill invocation as the first proof path.
- The design preserves canonical-source-first and generated-mirror discipline.
- The design makes Stop-hook/closeout, telemetry, Inventory handoff, and
  recursion prevention explicit.
- Editor UI behavior is explicitly deferred as a host-interface projection.
- Final synthesis recommends the next bounded route without executing it.
