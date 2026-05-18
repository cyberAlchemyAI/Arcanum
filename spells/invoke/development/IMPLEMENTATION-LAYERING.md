---
title: Invoke Spell Implementation Layering
status: draft
updatedAt: 2026-05-16
owner: Arcanum maintainers
scope: workflow
---

# Invoke Spell Implementation Layering

This document defines a progressive implementation layering model for the `invoke` spell.

Scope note: Layer 0 is the minimum working unit POC that proves the concept with the smallest useful end-to-end slice. Every later layer must explicitly improve and preserve the guarantees from previous layers.

## Context

- Target: `invoke` reusable Arcanum library spell
- Current state: L0 define contract and L1 design contract are documented, with Module Formulae starter templates, dedicated candidate family scaffolds, and standalone implementation-layering/work-pack templates available
- Primary user/operator: a user or assistant with vague development intent that needs governed spec, design, and work-pack artifacts before implementation
- Primary constraint: governance and traceability without direct code implementation or a full local CLI runtime in the first pass
- Source references: [WAVE-PLAN.md](WAVE-PLAN.md), [spells/invoke/templates/module-formulae/bundle-profile.md](../templates/module-formulae/bundle-profile.md), [spells/invoke/templates/implementation-layering.md](../templates/implementation-layering.md), [spells/invoke/templates/work-pack.md](../templates/work-pack.md), [registry/SPELLS.md](../../../registry/SPELLS.md)

## Layering Method

- POC-first: prove that one vague goal can become a governed spec and glossary with traceable Necronomicon transport.
- Decision-first: each layer exists to answer one lifecycle-authoring question before widening the mode surface.
- Progressive hardening: each layer adds one bounded improvement theme: definition, design, planning, then release packaging.
- Non-regression: prior layer guarantees remain true in later layers.
- Evidence-gated promotion: the next layer starts only after current-layer exit evidence exists.

## Layer Boundary Heuristic

A layer ends at the smallest slice that changes what the team can responsibly decide next.

Use this sentence to define each boundary:

```text
After this layer, we know whether {decision unlocked}.
```

Use this value/cost heuristic when deciding whether to keep work in the current layer or move it later:

```text
Layer value = decision unlocked + user-visible outcome + risk reduced
Layer cost = implementation time + verification time + coordination burden

Stop the layer when the next unit of work has lower value-per-cost for the current decision than starting the next decision layer.
```

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | User/Operator Outcome | Risk Reduced | Main Cost Drivers | Promotion Decision |
| ----- | ----------------- | -------------------- | --------------------- | ------------ | ----------------- | ------------------ |
| L0 (POC) | After this layer, we know whether vague intent can become an approved spec and glossary through one governed `define` flow. | Author `arcanum/spells/invoke/README.md` with `define` mode, one local template eligibility path, glossary linking, candidate/conflict recording, and a define-stage transport report contract. | A user can turn a vague goal into a spec, glossary, decisions, unresolved gaps, and an auditable transport report. | Proves the central intent-to-artifact concept before design, planning, or registry release. | Spell contract authoring, template resolution checks, glossary rules, markdown validation. | Continue to L1 when define mode emits required artifacts and no-match terms without silent promotion. |
| L1 | After this layer, we know whether an approved spec and glossary can drive consistent architecture/design output. | Add `design` mode with six required views, glossary consistency checks, discovery-mode design brief behavior, and design-stage transport reports. | A user gets a design bundle that is traceable to the spec and terminology baseline. | Reduces architecture drift and terminology mismatch before work-pack planning. | Architecture view templates, glossary conflict checks, design validation examples. | Harden to L2 when design outputs preserve define-stage terminology and record gaps instead of editing upstream artifacts silently. |
| L2 | After this layer, we know whether approved spec/design artifacts can become executable work-packs with gates and adaptive complexity. | Add `plan` and `full` behavior, low/medium/high complexity thresholding, single versus split work-pack outputs, blocker routing, and stage transport reconciliation. | A user receives a bounded work-pack with traceability, gate checks, and clear next route. | Reduces implementation-readiness risk, hidden blocker risk, and inconsistent work-pack shape. | Complexity rubric, split-pack structure, gate handling, transport reconciliation. | Package to L3 when plan/full modes stop on blockers and produce auditable single or split work-packs. |
| L3 | After this layer, we know whether `invoke` is ready to be validated, registered, and used as the Necronomicon lifecycle route. | Add `validate` mode, validation examples, missing-`invoke` route gap behavior, registry entry, and examples for define/design/plan/full/validate. | Necronomicon and users can discover `invoke` as the baseline lifecycle authoring spell. | Reduces release drift, route ambiguity, and untested template behavior. | Example coverage, registry changes, scenario validation, link checks. | Release when validation examples pass and registry entry is added only after the release gate succeeds. |

## Capability or Scope Progression

| Capability / Scope Area | L0 (POC Proof) | L1 (First Hardening) | L2 (Reliability / Governance) | L3 (Scale / Packaging) |
| ----------------------- | -------------- | -------------------- | ----------------------------- | ---------------------- |
| Lifecycle mode | `define` only | `design` from approved spec or discovery brief | `plan` plus `full` with gates | `validate` and registry examples |
| Artifact outputs | Spec, glossary, decisions, gaps, define transport | Architecture bundle, six views, design gaps, design transport | Single/split work-pack, blockers, plan transport, reconciled reports | Validation report, examples, registry entry, route proof |
| Terminology governance | Exact-or-alias Necronomicon linking, no-match rationale | Glossary consistency and conflict reporting | Glossary-based task labels and traceability names | Validation enforces linking and conflict fields |
| Human gates | Template choice on ties, glossary promotion gate | Upstream design patch requests only by approval | Blockers route to decision-gate | Registry release blocked until examples pass |

## Layer Definitions

| Layer | Objective | Builds On | Included Scope | Explicitly Deferred | Exit Evidence | Value/Cost Notes |
| ----- | --------- | --------- | -------------- | ------------------- | ------------- | ---------------- |
| L0 (POC) | Prove governed intent-to-spec and glossary creation. | none | `invoke` identity, `define` mode, template eligibility, conservative glossary linking, candidate promotion gate, define transport report. | Design mode, plan mode, full orchestration, validation examples, registry entry. | Spell contract exists, markdown links pass, define scenario can be reviewed against spec and glossary contracts. | This is the smallest useful proof because the later modes depend on trusted spec and terminology output. |
| L1 | Add design from approved define outputs. | L0 | `design` mode, six architecture views, glossary consistency, discovery brief, spec gap requests, design transport. | Work-pack planning, full orchestration, registry release. | Design scenario emits all required views and records term conflicts without silent upstream edits. | Design belongs before planning because work-pack tasks should not precede architecture view and terminology alignment. |
| L2 | Add implementation-readiness planning. | L1 | `plan` mode, `full` sequencing, complexity rubric, blocker routing, single/split work-pack shape, transport reconciliation. | Public registry entry, final examples, consumer route release. | Low-complexity and medium/high scenarios produce expected work-pack shape; blocker scenario stops at gate. | The planning cost is justified once spec and design artifacts can be trusted as inputs. |
| L3 | Validate and package `invoke` for discovery and Necronomicon routing. | L2 | `validate` mode, per-template passing examples, per-profile negative examples, registry entry, lifecycle route examples. | Direct implementation execution and full local CLI runtime remain out of scope. | Validation matrix passes, markdown links pass, registry entry is added after release gate, missing-`invoke` route gap is documented. | Packaging has high value only after all lifecycle stages and gates are proven locally. |

## Layer 0 - Minimum Working Unit POC

### Goal

Prove that `invoke define` can convert a vague development goal into a governed spec and glossary artifact set with decisions, gaps, and a Necronomicon transport report.

### Included Scope

- Author the initial reusable spell contract at `arcanum/spells/invoke/README.md`.
- Implement or document `define` mode behavior for template eligibility, user choice on ties, spec generation, glossary generation, and decision snapshots.
- Apply conservative Necronomicon-first glossary linking: normalized exact canonical-label or alias matches become `linked`, evidence-backed non-exact matches become `partial`, and all others become `no-match` with rationale.
- Record candidate terms, conflicts, promotion gates, and define-stage transport report output.

### Explicitly Deferred Beyond L0

- Six-view architecture bundle generation.
- Work-pack planning and complexity-based split behavior.
- `full` orchestration across all stages.
- `validate` mode, registry entry, and public examples.
- Direct implementation or a full local CLI runtime.

### Exit Evidence

- `arcanum/spells/invoke/README.md` exists and includes identity, trigger conditions, modes, phases, gates, observability, and output contract.
- A representative define scenario maps to spec and glossary contract fields.
- Glossary entries include link status, promotion gate, conflict status, and no-match rationale when needed.
- Define-stage transport uses the session-scoped append plus summary-complement policy.
- Markdown link checks pass for changed docs.

### Promotion Decision

- Continue when: define mode can create auditable artifacts without silently promoting templates, glossary terms, or upstream context.
- Pivot when: template ambiguity or glossary ambiguity requires more explicit option-card behavior before artifact generation.
- Stop when: `define` cannot preserve traceability from goal to spec, glossary, decision, and gap outputs.

## Layer-by-Layer Improvement Model

### Layer 1 Improvements Over L0

- Added scope: `design` mode, six required architecture views, discovery-mode design brief, architecture gaps, and design-stage transport.
- Hardening delta: spec and glossary become enforceable design inputs rather than loose references.
- Verification delta: design scenarios prove view coverage, glossary consistency, and non-mutating upstream patch requests.
- Prior guarantees preserved: define artifacts remain auditable, glossary promotion stays gated, and Necronomicon transport remains append/complement by default.

### Layer 2 Improvements Over L1

- Added scope: `plan` mode, `full` orchestration, complexity factors, single/split work-pack output, blocker routing, and transport reconciliation.
- Hardening delta: implementation handoffs become bounded by complexity, gates, and traceability labels.
- Verification delta: low-complexity, medium/high-complexity, and blocked-full scenarios exercise stop conditions and output shape.
- Prior guarantees preserved: spec and design remain authoritative inputs, task labels use glossary terminology, and upstream mutations require approval.

### Layer 3 Improvements Over L2

- Added scope: `validate` mode, initial template validation examples, registry entry, and Necronomicon lifecycle route examples.
- Hardening delta: release readiness depends on examples and validation rather than contract text alone.
- Verification delta: one passing example per initial template, one missing-input negative example per profile family, representative scenarios, schema checks, and markdown links.
- Prior guarantees preserved: no direct implementation mutation, no full local CLI requirement, and registry entry only after validation passes.

## Implementation Wave Backbone

| Wave | Target Layer | Goal | Key Artifacts | Verification |
| ---- | ------------ | ---- | ------------- | ------------ |
| W0 | L0 | Inspect existing templates and overlaps. | Baseline notes, template inventory evidence. | Existing template and work-pack review. |
| W1-W2 | L0 | Finalize spell contract and define stage. | `invoke` spell file, spec/glossary contracts, template eligibility policy, define transport. | Markdown links, representative define scenario, Module Formulae profile resolution. |
| W3 | L1 | Add design stage. | Architecture bundle contract, six views, design brief, design transport. | Design from approved spec and vague-goal discovery scenario. |
| W4-W5 | L2 | Add planning, full orchestration, and validate behavior. | Work-pack outputs, complexity result, blockers, full-mode stop conditions, validation report. | Low/medium/high work-pack checks and blocker gate checks. |
| W6-W7 | L3 | Register and validate release surface. | Registry entry, examples, validation matrix evidence. | Per-template passing examples, per-profile negative examples, schema checks, markdown links. |

## Non-Regression Guardrails

- `invoke` never directly implements product code.
- Feature-spec authorship remains in dedicated feature-spec commands; `invoke` remains a generic Arcanum lifecycle spell.
- Candidate templates cannot auto-promote to canonical.
- Candidate glossary terms and conflicts require `decision-gate` or `ontology-vault` approval before canonical promotion.
- Approved stage transport appends reports under the active Necronomicon and complements summaries only when matching sections already exist.
- `full` mode stops on blocked gates and returns remediation guidance.
- Registry entry is added only after validation passes.

## Open Decisions

- Which concrete representative define/design/plan examples should become the first validation fixtures.
- Whether the first implementation should generate artifacts only as documentation contracts or also include a thin adapter prompt for `arcanum-spell-invoke`.
- How much of the Module Formulae starter bundle should be promoted from starter examples into local canonical inventory after validation.

## Recommended Next Layer

Continue with L1 validation. The next useful proof is `invoke design` from approved define outputs, because planning, full orchestration, validation, and registry release all depend on trustworthy six-view architecture output and glossary consistency checks.

Major deferred scope: adaptive work-packs, full orchestration, registry release, and any CLI-like runtime behavior remain outside the design layer until `design` proves the spec-to-architecture path.