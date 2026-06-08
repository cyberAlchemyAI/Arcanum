---
module: {module-name}
version: current
status: draft
updatedAt: {date}
docType: implementation-plan
---

# Implementation Plan: {Module Name}

Use this template to turn approved architecture into delivery slices and execution-ready sequencing.

## Objective

Describe what this implementation plan must deliver.

## Inputs

- [module-spec.md](module-spec.md)
- [architecture-bundle.md](architecture-bundle.md)
- [glossary-ontology.md](glossary-ontology.md)
- [../implementation-layering.md](../implementation-layering.md)
- [../work-pack.md](../work-pack.md)

## Delivery Slices

| Slice | Goal | Dependencies | Exit Condition |
| --- | --- | --- | --- |
| S1 | {goal} | {dependencies} | {evidence of completion} |
| S2 | {goal} | {dependencies} | {evidence of completion} |

## Layer Progression

| Layer | Purpose | Includes | Defers |
| --- | --- | --- | --- |
| L0 | Minimum working unit | {core contracts and one end-to-end path} | {advanced governance or scale concerns} |
| L1 | Deterministic hardening | {retry, consistency, validations} | {degraded-path governance} |
| L2 | Governance hardening | {fallback and closure controls} | {scale-fit concerns} |
| L3 | Scale fit | {repeatability, packaging, rollout fit} | {future scope} |

## Layer Boundary Decisions

| Layer | Decision Question | Evidence Needed To Promote | Deferred Scope |
| --- | --- | --- | --- |
| L0 | After this layer, we know whether {decision unlocked}. | {evidence links} | {deferred items} |
| L1 | After this layer, we know whether {decision unlocked}. | {evidence links} | {deferred items} |
| L2 | After this layer, we know whether {decision unlocked}. | {evidence links} | {deferred items} |
| L3 | After this layer, we know whether {decision unlocked}. | {evidence links} | {deferred items} |

## Task Decomposition

| Task ID | Description | Layer | Owner | Complexity | Depends On |
| --- | --- | --- | --- | --- | --- |
| T-001 | {task summary} | L0, L1, L2, or L3 | {owner} | low, medium, high | {task ids} |

## Work-Pack Mapping

| Implementation Plan Source | Work-Pack Target | Mapping Rule |
| --- | --- | --- |
| Delivery Slices | Task Status Board | Each slice must map to one or more task rows. |
| Layer Boundary Decisions | activeLayerWindow and task layer fields | Preserve layer ownership for every mapped task. |
| Task Decomposition | Task IDs and dependencies | Keep task IDs stable across artifacts. |
| Blockers And Risks | Blockers section | Carry blocker IDs and resolution paths unchanged. |
| Validation Strategy | Gate checks and evidence references | Keep validator intent and evidence commands aligned. |

## Validation Strategy

| Validation Type | Target | Method |
| --- | --- | --- |
| Contract validation | {contract ids} | {tests or checks} |
| Layer boundary validation | ../implementation-layering.md | confirm each layer includes an explicit decision question and promotion evidence |
| Link validation | all updated markdown files | check_markdown_links.sh per file |
| Gate validation | stage exits | explicit checklist and evidence |

## Blockers And Risks

| ID | Type | Description | Resolution Path |
| --- | --- | --- | --- |
| B-001 | blocker | {description} | {decision gate or follow-up action} |
| R-001 | risk | {description} | {mitigation} |

## Handoff To Work-Pack And Execution Pack

Use [../work-pack.md](../work-pack.md) as the stable manifest produced from this plan.

Use [execution-pack.md](execution-pack.md) to convert this plan into wave-by-wave gated execution.
Ensure each execution wave references at least one layer from [../implementation-layering.md](../implementation-layering.md).

For medium/high complexity scopes, update both work-pack and execution-pack together and preserve task/layer consistency.
