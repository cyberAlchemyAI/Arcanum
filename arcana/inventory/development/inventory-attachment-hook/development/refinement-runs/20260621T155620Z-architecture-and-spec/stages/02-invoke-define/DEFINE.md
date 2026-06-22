---
module: inventory-attachment-hook
runId: 20260621T155620Z-architecture-and-spec
stage: s2-invoke-define
status: pass
updatedAt: 2026-06-21
docType: invoke-define
---

# Define: Inventory Attachment Hook

## Definition

Inventory Attachment Hook is an opt-in post-run handoff contract that lets a
sigil, spell, or observed invocation envelope send selected durable outputs to
Inventory as candidate evidence and lookup indexes.

It is not a global always-on crawler, not a promotion mechanism, and not a
replacement for the capability that owns the source artifact.

## Core Terms

| Term | Definition |
| --- | --- |
| attachment policy | Author-declared configuration on a sigil, spell, or runtime envelope that states whether Inventory handoff is enabled and what can be captured. |
| handoff envelope | Post-run object assembled from invocation metadata, durable outputs, validation results, residue, and attachment policy. |
| candidate read model | Inventory-owned evidence, index, tag, log, or summary record that improves lookup but does not own canonical truth. |
| eligible output | Durable, source-referenced, public-boundary-safe artifact from a meaningful run. |
| exclusion class | Content that must not be inventorized, including secrets, credentials, private prompts, transient runtime files, and canonical promotion claims. |
| idempotency key | Stable key that prevents repeated observed invocations from creating duplicate Inventory records. |

## Owner Map

| Owner | Authority |
| --- | --- |
| Inventory | Policy vocabulary, request shape, candidate evidence writes, lookup indexes, lint/validate expectations. |
| Sigil Development | Sigil authoring guidance for attachment declaration and durable output exposure. |
| Spellcraft | Spell-level attachment guidance for composed outputs and cross-sigil evidence bundles. |
| Observed Invocation Loop | Runtime point that sees the invocation envelope and triggers the Inventory handoff. |
| Observability framework | Shared envelope fields, telemetry ordering, hook-operation ledgers, failure reporting. |
| Bootstrap/runtime generation | Generated package propagation and task-zero metadata, never source authority. |
| Downstream governance owners | Any later promotion into ontology, definitions, constitutions, axioms, disciplines, sigils, or spells. |

## Non-Goals

- no global capture of every sigil/spell run;
- no raw source mutation;
- no direct promotion from execution evidence to canonical authority;
- no private prompt or secret capture;
- no database/search UI in this architecture;
- no runtime implementation before contract and templates exist.

## Readiness Verdict

`pass`: the defined object is narrow enough to design. The remaining work is to
specify envelope shape, runtime order, failure behavior, state writes, and tests.
