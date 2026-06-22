---
module: inventory-attachment-hook
runId: 20260621T162713Z-runtime-integration
stage: s5-distill
status: pass
updatedAt: 2026-06-21
docType: distill
---

# Distill: Smallest Coherent Runtime Unit

## Selected Unit

`ChatSkillAttachmentCloseout`

Responsibility: close one managed chat-invoked skill or spell with enough
privacy-safe evidence to observe the run and, when explicitly enabled, attach
selected durable outputs to Inventory as candidate evidence.

## Why This Unit

This is smaller than a full runtime framework and larger than a hook script. It
contains the behavior that must be preserved across Codex, Claude Code, and
generic runtimes:

- capability identity resolution;
- primary result preservation;
- observed envelope creation;
- telemetry append or explicit skip;
- attachment policy evaluation;
- candidate evidence handoff;
- non-recursive closeout receipt.

## Layer Map

| Layer | Concept | Role |
| --- | --- | --- |
| Repository learning system | Arcanum learns from governed evidence. | Parent context |
| Observed invocation envelope pipeline | One run becomes one telemetry event. | Existing base |
| Inventory Attachment Hook | Selected durable outputs become candidate Inventory evidence. | Target feature |
| ChatSkillAttachmentCloseout | One chat-invoked managed run closes with observation and optional attachment. | Selected SCU |

## Recomposition Proof

`ChatSkillAttachmentCloseout` recomposes into the larger architecture by
becoming the common lifecycle each runtime lane projects:

```text
Codex lane          -> skill-aware hook/wrapper closeout
Claude Code lane    -> native skill/stage-worker receipt closeout
Generic runtime lane -> deterministic wrapper/manual observer closeout
```

Each lane can vary in enforcement strength, but all must emit the same logical
closeout fields.

## Deferred Complexity

| Deferred Item | Reason |
| --- | --- |
| Full editor UI integration | Host-interface projection, not runtime proof. |
| Implicit skill selection telemetry | Needs platform metadata or wrapper conventions. |
| Continuation feedback attachment | Important later, but not required for first Inventory Attachment proof. |
| Ledger migration of legacy unknown kinds | Adjacent observability work, not attachment contract. |

## Verdict

`pass`: design should proceed with `ChatSkillAttachmentCloseout` as the shared
unit and three runtime projections.
