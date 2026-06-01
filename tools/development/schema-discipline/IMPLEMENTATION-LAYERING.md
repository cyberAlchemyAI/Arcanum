---
title: Schema Discipline Implementation Layering
status: draft
updatedAt: 2026-05-25
owner: local-fallback
scope: governance-practice
---

# Schema Discipline Implementation Layering

This document defines a progressive implementation layering model for lightweight schema discipline across Arcanum and CyberAlchemy.

## Context

- Target: Schema discipline for Arcanum and CyberAlchemy.
- Current state: partially implemented locally in runtime artifacts and candidate CyberAlchemy ontology lifecycle designs.
- Primary user/operator: agents and human reviewers consuming runtime evidence, sigils, spells, work-packs, context packs, and ontology promotion records.
- Primary constraint: avoid unnecessary dependencies or framework overhead.
- Source references: see `DEFINE.md` and `DESIGN.md`.

## Layering Method

- Layer 0 is a contract and one-family proof, not a platform migration.
- Each layer answers one decision question.
- Later layers preserve earlier guarantees.
- Promotion requires evidence, not intent.

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Operator Outcome | Risk Reduced | Main Cost Drivers | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether a shared schema discipline contract can improve one artifact family without new dependencies. | `SCHEMA-DISCIPLINE-CONTRACT.md` applied to `framework/runtime/`. | Runtime reviewers can check status, field tiers, enums, provenance, and validation grade consistently. | Over-modeling and hidden runtime evidence gaps. | Contract writing, doc alignment, `jq` checks. | Continue if runtime remains simple and validation is reviewable. |
| L1 | After this layer, we know whether the pattern is repeatable for handoffs and work-packs. | Context-pack/task-session handoff schema plus one work-pack/SWU validation profile. | Delegation blocks incomplete handoffs before runtime work begins. | Weak context or write-scope evidence masquerading as task readiness. | Template updates, fixture handoff, strict coverage checks. | Harden if handoff reuse is clear; narrow if templates become noisy. |
| L2 | After this layer, we know whether schema discipline can govern capability contracts without flattening sigils and spells into one model. | Sigil/spell template updates for frontmatter, quality bar, output contract, field tiers, and enum docs. | Capability authors have a predictable source schema without losing tier-specific differences. | Capability drift and soft quality bars. | Template migration, examples, stale language checks. | Expand only after new/revised sigils use the contract cleanly. |
| L3 | After this layer, we know whether CyberAlchemy promotion can consume schema-disciplined evidence without false authority. | `PromotionRecord` template and validator/checklist for candidate ontology promotion. | Ontology work keeps candidate/promoted status, confidence split, owner, use scope, contradiction, and rollback visible. | Telemetry or generated evidence becoming canonical truth. | Owner review, bridge-validation examples, candidate schema review. | Promote only with owner-approved use scope and bridge validation. |
| L4 | After this layer, we know whether stronger schema tooling is justified for repeated structured consumers. | Optional JSON Schema or library-backed validator for one high-drift, machine-consumed family. | Frequent consumers get stronger compatibility checks. | Validator drift and consumer breakage. | Dependency review, maintenance cost, migration support. | Adopt only for selected families with repeated drift; otherwise stay with `jq`/shell. |

## Capability Progression

| Area | L0 | L1 | L2 | L3 | L4 |
| --- | --- | --- | --- | --- | --- |
| Runtime | Contract proof for `RUN.json`, `STATUS.json`, adapter profile, validation grade. | Runtime handoff compatibility with task-session/context-builder. | Capability templates cite runtime evidence where needed. | Runtime signals feed PromotionRecord only as review input. | Optional schema validator if runtime consumers multiply. |
| Context and task handoff | Referenced as future consumer. | Strict Markdown plus JSON/index handoff schema. | Capability contracts can require context handoff evidence. | Handoff evidence can support ontology candidate records. | Optional structured validator for handoff indexes. |
| Sigils and spells | No broad migration. | Handoff consumers only. | Template contract and quality bar discipline. | Capability changes can create promotion candidates. | Optional registry/schema validator if registry consumers require it. |
| CyberAlchemy ontology | Candidate boundary named. | Context evidence remains candidate. | Capability claims remain lifecycle-owned. | PromotionRecord schema proof. | Optional schema only after ontology owner accepts branch/use model. |

## Layer Definitions

| Layer | Objective | Builds On | Included Scope | Explicitly Deferred | Exit Evidence |
| --- | --- | --- | --- | --- | --- |
| L0 | Prove lightweight contract on runtime. | none | Contract doc, runtime family map, small validation commands. | Handoff migration, sigil migration, ontology schema implementation. | Contract file, runtime validation checks, no dependency change. |
| L1 | Make delegation handoffs schema-disciplined. | L0 | Context pack/task-session handoff fields, strict coverage, source selectors, gaps, provenance. | Capability-template migration and ontology promotion. | One handoff fixture or reviewed template with Markdown and JSON/index expectations. |
| L2 | Normalize capability authoring surfaces. | L1 | Sigil/spell template rules, quality bar schema, output contract discipline. | Canonical ontology mutation. | Template review and at least one updated example. |
| L3 | Bound ontology promotion schemas. | L2 | PromotionRecord template, confidence split, review owner, bridge validation checklist. | Permanent Operational Ontology acceptance. | Candidate-only promotion fixture and review checklist. |
| L4 | Add stronger tooling only where proven necessary. | L3 | One selected high-drift structured family. | Universal schema platform. | Drift evidence and approved dependency decision. |

## Recommended Next Layer

Start with L0.

Minimum working unit:

- Create `SCHEMA-DISCIPLINE-CONTRACT.md`.
- Review `framework/runtime/README.md`, runtime templates, and runtime runner validation against that contract.
- Add only doc/template changes and small `jq`/shell checks if gaps are found.

## Non-Regression Guardrails

- Do not add new dependencies in L0 through L3.
- Do not treat candidate CyberAlchemy design artifacts as canonical ontology authority.
- Do not let observability or telemetry promote meaning without review.
- Do not make runtime state a universal ontology.
- Do not replace human-readable templates with machine-only schemas where review is the primary use.

## Major Deferred Scope

- JSON Schema adoption.
- Full sigil/spell migration.
- Canonical CyberAlchemy ontology mutation.
- Permanent Operational Ontology branch decision.
- Graph database or taxonomy dependency adoption.
