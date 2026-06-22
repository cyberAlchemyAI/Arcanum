---
module: inventory-attachment-hook
runId: 20260621T155620Z-architecture-and-spec
status: strategy-proposed
updatedAt: 2026-06-21
docType: refine-seed-proposal
---

# Refine Seed Proposal: Inventory Attachment Hook Architecture And Spec

## Operator Intent

```text
$refine architecture and spec for the Inventory Attachment Hook
```

## Target

`arcanum/arcana/inventory/development/inventory-attachment-hook/`

## Desired Outcome

Produce architecture and specification artifacts for the opt-in Inventory
Attachment Hook so implementation can proceed without guessing cross-capability
authority boundaries.

Target final artifacts after confirmation:

- `arcanum/arcana/inventory/development/inventory-attachment-hook/ARCHITECTURE.md`
- `arcanum/arcana/inventory/development/inventory-attachment-hook/SPEC.md`

## Source Context

Primary local evidence:

- `INVOKE-PLAN.md`
- `IMPLEMENTATION-LAYERING.md`
- `WORK-PACK.md`
- `arcanum/arcana/inventory/SKILL.md`
- `arcanum/arcana/sigil-development/SKILL.md`
- `arcanum/arcana/spellcraft/SKILL.md`
- `arcanum/framework/observability/SIGIL-OBSERVABILITY-HOOK.md`
- `arcanum/spells/observed-invocation-loop/README.md`
- `arcanum/formulae/dispatch-spec/dispatch.schema.yml`
- `arcanum/formulae/dispatch-spec/TECHNIQUE-CATALOG.md`

## Refinement Questions

1. What is the minimal architecture for an attached Inventory handoff that does
   not become a global always-on hook?
2. What exact policy envelope should sigils and spells declare?
3. What runtime sequence should convert an observed invocation into an
   Inventory request?
4. What idempotency, failure, privacy, and public-boundary rules are required?
5. Which writes are canonical source changes, generated mirrors, read-model
   updates, or observability records?
6. What acceptance tests prove the hook shortens future search without granting
   promotion authority?

## Write Scope

Allowed after confirmation:

- refinement run evidence under this folder;
- target architecture/spec artifacts under
  `arcanum/arcana/inventory/development/inventory-attachment-hook/`;
- optional stage drafts under `stages/`.

Not allowed in this refine run:

- mutation of canonical skill docs;
- generated skill mirror regeneration;
- implementation of the runtime hook;
- pilot invocation outputs;
- public/private boundary unsafe material;
- lifecycle promotion into definitions, ontology, constitutions, axioms, or
  disciplines.

## Preset And Research

| Field | Value |
| --- | --- |
| preset | standard |
| researchMode | research-if-gap-appears |
| externalResearch | not approved |
| subagentStrategy | recommended, requires user permission |

## Planned Stage Configuration

The run uses the canonical ten-stage Refine loop:

1. Context Builder evidence baseline.
2. Invoke Define.
3. Interrogation `refine-review`.
4. Refine research decision.
5. Distill coherent unit.
6. Invoke Design for architecture/spec.
7. Interrogation `refine-design-review`.
8. Distill Repair.
9. Invoke Plan refresh.
10. Final Interrogation and Refine-owned synthesis.

## Done Criteria

- `REFINE-DISPATCH.json` validates through Dispatch Spec before execution.
- The strategy preview is confirmed before runtime-backed stages or subagents
  run.
- `ARCHITECTURE.md` defines components, owners, data flow, state namespaces,
  failure handling, and authority boundaries.
- `SPEC.md` defines the policy envelope, handoff envelope, validation rules,
  idempotency key, acceptance tests, and non-goals.
- Final synthesis cites stage receipts or blocked reasons.
