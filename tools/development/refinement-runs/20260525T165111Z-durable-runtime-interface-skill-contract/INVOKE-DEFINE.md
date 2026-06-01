## Invoke Result

- Mode: define
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `spells/invoke/define.md`
- Outputs: `INVOKE-DEFINE.md`, `RUNTIME-GLOSSARY.md`, `IMPLEMENTATION-LAYERING.md`, `DEFINE-TRANSPORT.md`
- Template selection: runtime infrastructure definition using the existing invoke/refine artifact family; no new template family required.
- Decisions: define Arcanum runtime as a generic durable execution substrate; remove Codex Goal from the core model; keep Codex only as an adapter.
- Unresolved gaps: none blocking; historical `/goal` documentation cleanup deferred.
- Next route: design

## Spec Artifact

### Name

Durable Arcanum Runtime Interface

### Purpose

Create a generic, durable, file-backed execution substrate for Arcanum orchestrators. The runtime lets refine, task-session, and future workflows hand off bounded work to adapters while preserving status, artifacts, parent/child topology, blocked reasons, and validation evidence.

### Core Formula

```text
orchestrator -> async task handoff -> runtime translator -> runtime executor -> adapter
```

### Problem Statement

Current Arcanum execution paths over-couple orchestration to Codex Goal or direct Codex CLI execution:

- refine still names Codex Goal and `GOAL-HANDOFF.md` in active runtime language,
- task-session delegates through a `codex-goal` adapter,
- `tools/arcanum --exec` directly runs Codex CLI through shared repo-local state,
- command-backed refinement can fail before producing durable stage artifacts.

### Target Behavior

Arcanum should be able to:

- create durable runtime run folders,
- execute or block through explicit adapters,
- preserve status and result artifacts even when an adapter fails,
- represent one loop, nested loops, candidate loops, repair loops, and continuations,
- let refine and task-session consume the same runtime evidence model.

### Non-Goals

- Do not implement native `/goal`.
- Do not make Codex the runtime identity.
- Do not build a background scheduler in the first slice.
- Do not rewrite historical development records unless active validation consumes them.

### Acceptance Criteria

- `tools/arcanum-runtime-run` exists and supports `dry-run`.
- Runtime run folders include `RUN.json`, `HANDOFF.md`, `STATUS.json`, `RESULT.md`, `events.jsonl`, `artifacts/`, and `children/`.
- `codex-exec` uses isolated per-run adapter state.
- `tools/arcanum --exec` can delegate through the runtime runner behind a feature flag.
- Refine active artifacts use `RUNTIME-HANDOFF.md`, not `GOAL-HANDOFF.md`.
- Task-session exposes a generic runtime handoff adapter.

## Define Decisions

| Decision | Value | Rationale |
| --- | --- | --- |
| Runtime identity | Arcanum durable runtime | Keeps orchestration independent from any one adapter. |
| First runner | `tools/arcanum-runtime-run` | Shared tools-level surface for refine, task-session, and future orchestrators. |
| First adapter | `dry-run` | Proves folder/schema without network or Codex dependency. |
| First execution adapter | `codex-exec` | Reuses current Codex CLI capability while isolating state. |
| Handoff artifact | `RUNTIME-HANDOFF.md` | Avoids Codex Goal language and names the generic runtime contract. |

## Define Transport

- Source refinement run: `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/`
- Source final synthesis: `RESULT.md`
- Source evidence index: `evidence-index.json`
- Recommended downstream route: `invoke design`

## Observability Closeout

- OBSERVATION: skipped
- LEDGER: n/a
- REFLECTION_TRIGGER: none
- RECOMMENDATION: continue-to-invoke-design
- DEDUPE_KEY: invoke-define-durable-runtime-20260525T165111Z
