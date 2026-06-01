# Craft Runtime Command Surface Define

## Invoke Result

| Field | Value |
| --- | --- |
| Mode | define |
| Target | `development/craft/CRAFT-RUNTIME-001` |
| Phase status | pass |
| Mode contract | `spells/invoke/define.md` |
| Template selection | Module Formulae baseline plus standalone layering/work-pack companions |
| Next route | design |

## Objective

Create a local Craft runtime/command-surface artifact family that makes the Refine validation blocker executable.

The immediate problem is narrow:

```text
tools/arcanum --resolve dispatch-spec      # currently block
tools/arcanum --resolve runtime-handoff    # currently block
```

Craft validation needs these command routes because Refine requires dispatch route validation and runtime handoff readiness before command-backed stages can run.

## Scope

In scope:

- define the missing command-surface blocker,
- expose the source evidence and acceptance criteria,
- design an executable work-pack for command route availability,
- preserve observation and runtime handoff requirements,
- keep this under Craft development until task-session execution is approved.

Out of scope:

- executing the work-pack,
- mutating `.codex/commands`,
- mutating `tools/arcanum`,
- promoting Craft,
- changing canonical Refine behavior,
- implementing cross-runtime adapters for Claude or Copilot,
- scoring, generated indexes, or role delegation automation.

## Source Contracts

| Source | Use |
| --- | --- |
| `CRAFT-REFINE-RUNTIME-STRATEGY.md` | Runtime topology and failure evidence. |
| `ARCANUM-SKILL-RUNTIME-HANDOFF.md` | Runtime-agnostic skill invocation and observation envelope requirements. |
| `refinement-runs/20260529T164919Z-validate-craft/RESULT.md` | Current validation blocker and exact missing command routes. |
| `formulae/dispatch-spec/SKILL.md` | Existing dispatch-spec capability source. |
| `formulae/dispatch-spec/scripts/validate-dispatch.py` | Deterministic dispatch validation surface. |
| `arcana/task-session/runtime-adapters/runtime-handoff.md` | Existing runtime handoff adapter contract. |
| `.codex/commands/refine.md` | Refine command contract requiring dispatch validation and runtime handoff readiness. |
| `tools/arcanum` | Repository-local command surface that resolves `.codex/commands/<name>.md`. |

## Candidate Deliverables

| Deliverable | Purpose |
| --- | --- |
| Bare `dispatch-spec` command route | Let Refine resolve dispatch-spec through `tools/arcanum --resolve dispatch-spec`. |
| Bare `runtime-handoff` command route | Let Refine resolve runtime-handoff through `tools/arcanum --resolve runtime-handoff`. |
| Smoke validation task | Prove both routes resolve and the Craft Refine dispatch remains schema-valid. |
| Package sync task | Update Craft state after the command-surface blocker is cleared. |

## Decisions

| Decision | Selected | Rationale |
| --- | --- | --- |
| Treat missing commands as a Craft runtime blocker. | yes | The Refine validation route cannot execute without them. |
| Plan command aliases before implementation. | yes | The user asked for missing artifacts; Invoke should not execute Task Session work. |
| Keep runtime adapter implementation deferred. | yes | The immediate blocker is command route resolution, not full runtime adapter implementation. |

## Unresolved Gaps

| Gap | Treatment |
| --- | --- |
| Whether command aliases should call existing `arcanum-sigil-*` routes or direct capability sources. | Task-session decision in `CRAFT-RUNTIME-001`. |
| Whether runtime-handoff should be a sigil command, adapter command, or task-session adapter route. | Task-session decision in `CRAFT-RUNTIME-002`. |
| Whether this should later move to a runtime lifecycle thread. | Keep side-threaded; package sync records evidence only. |

## Gate Result

`pass`

This define artifact is stable enough for design and planning.
