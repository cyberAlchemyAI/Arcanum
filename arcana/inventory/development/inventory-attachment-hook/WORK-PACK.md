---
module: inventory-attachment-hook
version: draft
status: ready-for-task-session
updatedAt: 2026-06-21
docType: work-pack
---

# WORK-PACK: Inventory Attachment Hook

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Execution can start with `SWU-IAH-001`. |
| complexity | medium | Cross-capability contract plus runtime handoff. |
| outputMode | split | Execute one SWU at a time. |
| architectureRef | `IMPLEMENTATION-LAYERING.md` | Layered route for contract, templates, runtime, mirrors, pilot. |
| invokePlanRef | `INVOKE-PLAN.md` | Source plan. |
| activeLayerWindow | L0-L1 first | Runtime begins after contract/template stabilization. |
| readinessProfile | ready-for-task-session | Ready for bounded implementation, not feature-complete. |

## Objective Summary

Add an opt-in Inventory Attachment Hook so sigils and spells can inventory
durable outputs from meaningful runs into `.arcanum/inventory/` candidate
evidence.

Primary objective:

```text
When a sigil or spell declares inventoryAttachment.enabled, the post-run path can hand selected durable outputs to Inventory as candidate evidence and indexes.
```

## Active Scope

In scope:

- canonical attachment contract;
- sigil-level attachment declaration guidance;
- spell-level attachment declaration guidance;
- post-run/observed-invocation handoff semantics;
- policy and handoff templates;
- generated native skill mirror synchronization after canonical edits;
- one later pilot attached invocation.

Out of scope:

- always-on inventory for all sigils and spells;
- ontology promotion;
- definition, constitution, axiom, or discipline promotion;
- private material entering public Arcanum;
- database/vector/search UI;
- broad whole-repo inventorization.

## Delivery Slices

| Slice ID | Outcome | Layer | Dependencies | Validation |
| --- | --- | --- | --- | --- |
| S-IAH-001 | Canonical Inventory attachment contract exists. | L0 | none | grep anchors in Inventory docs |
| S-IAH-002 | Sigil and spell lifecycle docs can declare attachments. | L0 | S-IAH-001 | grep anchors in Sigil Development and Spellcraft docs |
| S-IAH-003 | Post-run handoff semantics exist. | L0-L2 | S-IAH-001 | observability/observed-invocation anchors |
| S-IAH-004 | Reusable policy and handoff templates exist. | L1 | S-IAH-001..003 | template presence and sample parse/check |
| S-IAH-005 | Generated runtime mirrors are synchronized. | L3 | S-IAH-001..004 | bootstrap/regeneration and diff checks |
| S-IAH-006 | Pilot attached invocation proves lookup value. | L4 | S-IAH-005 | Inventory lookup retrieves pilot evidence |

## SWU Execution Handoff

| SWU ID | Goal | Source Anchors | Write Scope | Done Criteria | Validation Surface | Status |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-IAH-001 | Add Inventory attachment contract and authority boundary. | `arcanum/arcana/inventory/SKILL.md`, this plan | `arcanum/arcana/inventory/SKILL.md`, optional `arcanum/arcana/inventory/README.md` | Inventory defines `inventoryAttachment`, candidate evidence semantics, include/exclude classes, and failure behavior. | `rg -n "inventoryAttachment|candidate-read-model|onFailure|authority boundary" arcanum/arcana/inventory` | ready |
| SWU-IAH-002 | Add sigil authoring guidance for attachment. | `arcanum/arcana/sigil-development/SKILL.md`, observability hook docs | `arcanum/arcana/sigil-development/SKILL.md` | Sigil lifecycle tells authors when/how to attach Inventory and expose durable outputs. | `rg -n "inventoryAttachment|durable outputs|Inventory" arcanum/arcana/sigil-development` | blocked-by-001 |
| SWU-IAH-003 | Add spell authoring guidance for attachment. | `arcanum/arcana/spellcraft/SKILL.md`, spellcraft README | `arcanum/arcana/spellcraft/SKILL.md`, optional spellcraft README | Spell lifecycle defines spell-level attachment, composed output bundles, and cross-sigil evidence handling. | `rg -n "inventoryAttachment|Inventory Attachment|durable outputs" arcanum/arcana/spellcraft` | blocked-by-001 |
| SWU-IAH-004 | Extend post-run handoff semantics. | `arcanum/framework/observability/SIGIL-OBSERVABILITY-HOOK.md`, `arcanum/spells/observed-invocation-loop/README.md` | observability hook docs and observed invocation docs | Hook sequence states when Inventory handoff happens, how failure is handled, and what telemetry records. | `rg -n "Inventory handoff|inventoryAttachment|onFailure|idempotency" arcanum/framework/observability arcanum/spells/observed-invocation-loop` | blocked-by-001 |
| SWU-IAH-005 | Add attachment policy and handoff templates. | this work-pack, Inventory templates | `arcanum/arcana/inventory/templates/` or `arcanum/arcana/inventory/development/templates/` | Templates exist for attachment policy and post-run handoff envelope. | file presence plus sample YAML/JSON check where applicable | blocked-by-004 |
| SWU-IAH-006 | Sync generated native skill surfaces. | bootstrap/runtime generation discipline | `.agents/skills/inventory/`, `.agents/skills/sigil-development/`, `.agents/skills/spellcraft/`, and observed-invocation mirror whenever OIL canonical docs change | Generated mirrors reflect canonical edits and no hand-edited drift remains. | bootstrap dry-run or targeted regeneration, schema/fixture checks, then `git diff --check` | blocked-by-005 |
| SWU-IAH-007 | Run one pilot attached invocation. | a selected low-risk sigil/spell | `.arcanum/inventory/`, `.arcanum/observability/` pilot outputs | A real attached run creates candidate evidence and future lookup can find it. | Inventory lookup/status plus observability signal review | blocked-by-006 |

## Open Decisions

| Decision ID | Question | Recommended Default | Gate |
| --- | --- | --- | --- |
| DEC-IAH-FAILURE | Should hook failure block the primary run? | Default `warn`; allow `block` only when a capability declares Inventory output as required. | Resolve in SWU-IAH-001. |
| DEC-IAH-MODE | Which Inventory mode should the hook call first? | `ingest` for new run outputs; `backfill` for older artifacts; `sync` for generated mirror refresh. | Resolve in SWU-IAH-001. |
| DEC-IAH-IDEMPOTENCY | What prevents duplicate inventory entries? | Use an idempotency key from capability id, invocation id, output path, and content hash when available. | Resolve in SWU-IAH-004. |
| DEC-IAH-PILOT | Which sigil or spell should prove the hook? | Prefer a low-risk local spell with durable docs and no private-to-public boundary risk. | Resolve before SWU-IAH-007. |

## Validation Bundle

Run after the relevant SWUs:

```bash
rg -n "inventoryAttachment|candidate-read-model|Inventory Attachment|onFailure" arcanum/arcana arcanum/framework arcanum/spells
git diff --check -- arcanum/arcana/inventory arcanum/arcana/sigil-development arcanum/arcana/spellcraft arcanum/framework/observability arcanum/spells/observed-invocation-loop .agents/skills
```

Add schema or fixture checks for controlled vocabulary, `source_refs`,
non-authority handoff language, per-output idempotency, public-boundary
resolution, and EvidenceSet references.

When generated mirrors are touched, validate through the repository bootstrap
path instead of manually editing generated packages.

## Gate Checks

1. Execute exactly one SWU at a time.
2. Patch canonical `arcanum` sources before generated skill mirrors.
3. Keep attachment opt-in and explicit.
4. Keep Inventory candidate-only; no ontology, definition, constitution, axiom,
   or discipline promotion.
5. Do not inventory secrets, credentials, private prompts, or public-boundary
   unsafe content.
6. Do not implement runtime automation until policy and handoff templates exist.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-06-21 | Created Invoke plan and task-session work-pack for Inventory Attachment Hook. | Codex |
