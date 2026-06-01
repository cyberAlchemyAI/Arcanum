# Craft Runtime Command Surface Implementation Layering

## Purpose

Define the L0-L3 layer boundary for clearing the command-surface blocker that prevents Refine from validating Craft.

## Source Contract

| Source | Use |
| --- | --- |
| `CRAFT-RUNTIME-DEFINE.md` | Objective and scope. |
| `CRAFT-RUNTIME-DESIGN.md` | Six-view design and interface rules. |
| `CRAFT-VALIDATION.md` | Review surface and non-promotion guardrails. |
| `refinement-runs/20260529T164919Z-validate-craft/RESULT.md` | Exact blocked commands. |

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether `dispatch-spec` can be exposed as a bare command route. | Add or repair `dispatch-spec` command route. | Command route source review and route exposure. | Full Refine rerun. | `tools/arcanum --resolve dispatch-spec` passes. | Continue to runtime-handoff. |
| L1 | After this layer, we know whether `runtime-handoff` can be exposed as a bare command route. | Add or repair `runtime-handoff` command route. | Command route source review and route exposure. | Full runtime adapter implementation. | `tools/arcanum --resolve runtime-handoff` passes. | Continue to smoke validation. |
| L2 | After this layer, we know whether the command-surface blocker is actually cleared for Craft validation. | Command smoke and dispatch validation. | Resolve both routes and validate Craft dispatch. | Full Refine stage execution. | Resolve checks and dispatch validation pass. | Continue to package sync or remediate. |
| L3 | After this layer, we know whether Craft can reroute to Refine validation. | Package sync and next-route update. | README/session/work-pack sync. | Promotion. | Craft state names Refine rerun or task-session next route. | Defer promotion. |

## Non Regression Guardrails

- Do not promote Craft.
- Do not change Refine lifecycle semantics.
- Do not implement scoring, generated indexes, or role delegation automation.
- Do not claim full runtime-interface support after command smoke only.

## Recommended Next Layer

L0
