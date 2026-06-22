---
module: inventory-attachment-hook
version: draft
status: plan-ready
updatedAt: 2026-06-21
docType: invoke-plan
invokeMode: plan
---

# Invoke Plan: Inventory Attachment Hook

## Result

| Field | Value |
| --- | --- |
| planGateStatus | pass |
| target | Inventory Attachment Hook for sigils and spells |
| recommendedNextRoute | `task-session` on `SWU-IAH-001` |
| outputMode | split |
| layeringRef | `IMPLEMENTATION-LAYERING.md` |
| workPackRef | `WORK-PACK.md` |

## Objective

Implement an opt-in attachment hook so a sigil or spell can declare that a
meaningful run should hand selected durable outputs to Inventory after the run.

The hook must make later searches shorter by producing Inventory read-model
evidence, without promoting facts into definitions, ontology, constitutions,
axioms, disciplines, or any other canonical authority surface.

## Core Design Decision

The hook should be attached, not global.

An invocation is eligible only when a sigil, spell, or runtime envelope declares
an inventory attachment policy. The policy tells the post-run hook what kinds of
outputs can be inventorized, what must be excluded, whether failure blocks the
run, and which Inventory mode should receive the handoff.

Minimal policy shape:

```yaml
inventoryAttachment:
  enabled: true
  mode: ingest
  authority: candidate-read-model
  attachWhen:
    - meaningful-run
    - durable-output-present
  include:
    - changed-files
    - output-artifacts
    - durable-decisions
    - source-backed-claims
    - residues
    - validation-reports
  exclude:
    - secrets
    - credentials
    - private-user-prompts
    - transient-runtime-files
    - canonical-promotion-claims
  onFailure: warn
```

## Ownership Split

| Owner | Responsibility |
| --- | --- |
| `inventory` | Attachment policy vocabulary, ingest/backfill/sync handoff contract, candidate-only authority boundary, templates, validation expectations. |
| `sigil-development` | Sigil lifecycle guidance for declaring attachment and exposing durable outputs to the post-run hook. |
| `spellcraft` | Spell lifecycle guidance for spell-level attachment, composition outputs, and cross-sigil evidence bundles. |
| `observed-invocation-loop` | Runtime handoff point that detects attachment policy and calls Inventory after observability capture. |
| observability framework | Shared post-run envelope fields, failure semantics, and telemetry for hook execution. |
| bootstrap/runtime generation | Propagate canonical contract changes into generated native skill/spell surfaces. |

## Authority Boundary

Inventory Attachment creates candidate evidence and lookup projections only.

It may:

- append or refresh Inventory generated pages, evidence cards, indexes, tags,
  and logs;
- reference the source artifact and invocation envelope;
- mark uncertainty, gaps, residue, and validation status;
- shorten future retrieval paths for agents.

It must not:

- promote a definition;
- create or mutate ontology meaning as authoritative truth;
- create or mutate constitutions, axioms, or disciplines;
- treat generated Inventory projections as the source of truth;
- inventory private or unsafe material into public Arcanum surfaces.

## Execution Shape

1. Add the attachment contract to canonical Inventory docs.
2. Add sigil-level and spell-level authoring guidance.
3. Extend the post-run/observed invocation contract with an Inventory handoff.
4. Add reusable attachment policy and handoff templates.
5. Regenerate generated runtime skill surfaces from canonical Arcanum sources.
6. Validate links, grep anchors, generated mirrors, and authority-boundary text.

## Readiness

This plan is ready for execution as a sequence of small SWUs. Start with
`SWU-IAH-001`; do not implement runtime automation before the contract and
policy template are explicit.
