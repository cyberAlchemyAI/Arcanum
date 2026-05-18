# Necronomicon Glossary Consistency

## Summary

| Check | Result | Notes |
| --- | --- | --- |
| Define glossary terms appear in design | pass | Core terms are used consistently in `DESIGN.md`. |
| Necronomicon vs ontology-harness boundary | pass | Design keeps Necronomicon as harness and ontology governance downstream. |
| Inventory ownership | pass | Design treats inventory as retrieval/durable knowledge owner. |
| Invoke ownership | pass | Design treats invoke as lifecycle authoring owner. |
| Side note and unblocker distinction | pass | Design separates generic side notes from bounded blocking tasks. |

## Term Mapping

| Glossary Term | Design Usage | Status |
| --- | --- | --- |
| Necronomicon | Repository-local stateful harness. | linked |
| Session Memory Router | MVP structure and workflow. | linked |
| Workbench State Manager | Continuation lanes and queues. | linked |
| Active Interaction | Primary session state object. | linked |
| Turn Classification | Ordered decision flow. | linked |
| Side Note | Non-derailing queue input. | linked |
| Unblocker Task | Small bounded side task. | linked |
| Inventory Candidate | Durable knowledge candidate. | linked |
| Ontology Candidate | Governance candidate, not promoted. | linked |
| Checkpoint | Durable distillation and queue closeout. | linked |
| Gap | Explicit unresolved item. | linked |
| Handoff | Transfer to owning capability. | linked |

## Conflicts

None found.

## Gaps

- Exact state schemas remain plan-layer work.
- Fixture coverage is not yet implemented.
