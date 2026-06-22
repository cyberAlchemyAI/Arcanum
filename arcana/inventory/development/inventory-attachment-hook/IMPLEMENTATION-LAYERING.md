---
module: inventory-attachment-hook
version: draft
status: plan-ready
updatedAt: 2026-06-21
docType: implementation-layering
---

# Implementation Layering: Inventory Attachment Hook

## Purpose

Define the smallest safe path from an opt-in attachment idea to a runtime-backed
Inventory handoff for sigils and spells.

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | Can authors declare an Inventory attachment without ambiguity? | Canonical contract updates in Inventory, Sigil Development, Spellcraft, and observability docs. | Attachment vocabulary, opt-in semantics, authority boundary, failure policy, owner split. | Automatic runtime execution and generated mirrors. | `rg` finds stable anchors for `inventoryAttachment`, `candidate-read-model`, and `onFailure`. | Continue to templates. |
| L1 | Can agents produce a valid attachment policy and handoff envelope? | Policy and handoff templates. | YAML/Markdown examples, include/exclude classes, source refs, output refs, validation result refs. | Runtime parser or Inventory mutation. | Template presence and sample parse/check. | Continue to runtime handoff. |
| L2 | Can the observed invocation path trigger Inventory from an attached run? | Observed invocation handoff contract and minimal executor design. | Hook sequence, idempotency key, failure semantics, telemetry event, Inventory mode routing. | Broad generated package rollout. | Dry-run or fixture shows envelope to Inventory request conversion. | Continue to generation/sync. |
| L3 | Are generated native surfaces synchronized and safe to use? | Bootstrap/regeneration and mirror validation. | `.agents/skills` mirrors for touched capabilities, runtime package notes, link/grep/diff checks. | Whole-repo inventorization and canonical promotion. | Generated files match canonical contract; validation commands pass. | Ready for pilot attached sigil/spell. |
| L4 | Does a real attached invocation shorten future search? | One pilot run with Inventory outputs. | Pilot attached capability, evidence card/index/log update, lookup check, observability signal. | Always-on inventory, ontology promotion, definition promotion. | Inventory lookup retrieves the pilot evidence by capability, output, and residue. | Consider defaulting selected high-value sigils/spells to attached mode. |

## Guardrails

- Attachment is opt-in and explicit.
- Inventory output is candidate evidence, not canonical authority.
- Raw source artifacts remain read-only unless the source owner explicitly
  mutates them.
- Hook failure warns by default; it blocks only when a sigil or spell declares
  attachment as required.
- Inventory records source refs, generated refs, validation refs, and residue.
- Runtime work must not hand-edit generated skill mirrors.
- Public Arcanum surfaces must not receive private parent-repo material.

## Recommended Layer Window

Execute L0-L1 first. L2 should begin only after the attachment vocabulary and
template shape are stable enough that runtime code is not guessing the contract.
