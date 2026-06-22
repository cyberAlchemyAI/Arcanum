---
module: inventory-attachment-hook
runId: 20260621T155620Z-architecture-and-spec
stage: s5-distill
status: pass
updatedAt: 2026-06-21
docType: distill-result
---

# Distill: Smallest Coherent Unit

## Target Context

The target is a cross-capability hook architecture that must be specific enough
for SWU execution while staying short of implementation.

## Selected Unit

`AttachedInventoryHandoff`

## Responsibility

Represent the contract and runtime boundary for converting one meaningful
attached sigil/spell invocation into one Inventory candidate-evidence request.

## Closure

The unit closes when it defines:

- attachment policy;
- observed invocation inputs;
- handoff envelope;
- eligibility and exclusion rules;
- idempotency key;
- Inventory request mode;
- failure behavior;
- state writes;
- validation and acceptance tests.

## Recomposition Proof

`AttachedInventoryHandoff` recomposes into the whole hook by becoming:

- the Inventory contract for `SWU-IAH-001`;
- the sigil authoring guidance for `SWU-IAH-002`;
- the spell authoring guidance for `SWU-IAH-003`;
- the observed invocation handoff contract for `SWU-IAH-004`;
- the template substrate for `SWU-IAH-005`;
- the generated mirror sync target for `SWU-IAH-006`;
- the pilot proof target for `SWU-IAH-007`.

## Deferred Complexity

- automatic execution code;
- search UI or database substrate;
- full Inventory lint rule implementation;
- broad default-on attachment;
- ontology/definition promotion routes.

## Tension Ledger

| Tension | Resolution |
| --- | --- |
| Lookup optimization wants automatic capture. | Keep attachment explicit and default `enabled: false` unless declared. |
| Governance wants reusable evidence. | Store candidate evidence with source refs and non-authority notices. |
| Runtime wants reliable hooks. | Put triggering in Observed Invocation Loop after observability envelope assembly. |
| Avoid duplicates. | Require idempotency key and dedupe behavior before Inventory write. |
| Public Arcanum cannot receive private material. | Run exclusion/public-boundary checks before handoff. |

## Verdict

`pass`: design `AttachedInventoryHandoff` as the architecture/spec core.
