# Runtime Handoff: Validate Craft Refine Run

## Status

`blocked-before-execution`

## Objective

Run the canonical Refine loop for validating Craft only after dispatch route shape and runtime handoff surfaces are available.

## Dispatch Reference

`development/craft/refinement-runs/20260529T164919Z-validate-craft/REFINE-DISPATCH.json`

## Strategy Preview

| Item | Value |
| --- | --- |
| Preset | standard |
| Research | no-research |
| Selected overlays | `baseline_sequence`, `craft_validation_loop` |
| Subagent strategy | none |
| Join policy | none |
| Authorization | not_needed for subagents; command-backed execution blocked by route availability |

## Overlay Rationale

| Overlay | Why It Applies |
| --- | --- |
| `baseline_sequence` | Refine requires the canonical ten-stage loop and every stage must pass evidence to the next. |
| `craft_validation_loop` | Craft needs repeatable local validation and recomposition evidence before promotion. |

## Command Resolution

| Command | Status |
| --- | --- |
| `context-builder` | resolves |
| `invoke` | resolves |
| `interrogation` | resolves |
| `distill` | resolves |
| `dispatch-spec` | missing command route |
| `runtime-handoff` | missing command route |

## Blocked Fields

| Field | Reason |
| --- | --- |
| Dispatch Spec command-backed validation | `tools/arcanum --resolve dispatch-spec` fails. |
| Runtime handoff command route | `tools/arcanum --resolve runtime-handoff` fails. |
| Canonical Refine stage execution | Refine contract requires dispatch validation and runtime handoff readiness before command-backed stages. |

## Runtime Status

No command-backed stage execution was performed.

## Exact Unblock Action

Install or expose the missing command routes, then rerun this Refine dispatch:

```text
tools/arcanum --resolve dispatch-spec
tools/arcanum --resolve runtime-handoff
```

If the command-surface work is intentionally side-threaded, the safe next route is:

```text
invoke plan development/craft/CRAFT-RUNTIME-001
```
