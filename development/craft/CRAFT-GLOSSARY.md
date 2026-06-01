# Craft Glossary

## Purpose

This glossary stabilizes the candidate vocabulary needed before Craft method architecture planning.

Terms are local to `development/craft/` unless a later promotion route explicitly moves them into a canonical registry, ontology, sigil, spell, command, or runtime surface.

## Status Legend

| Status | Meaning |
| --- | --- |
| `candidate` | Stable enough for architecture planning, but not yet canonically promoted. |
| `validated-by-mvp` | Exercised or checked by the recursive-ledger MVP fixture and validation report. |
| `deferred` | Named for continuity, but intentionally outside the current closure wave. |

## Core Method Terms

| Term | Definition | Status | Source Anchors |
| --- | --- | --- | --- |
| Craft | The recursive method for turning intention into stable artifacts by moving between schema and data, finding the smallest coherent unit, validating it, and recomposing it into its upper context. | candidate | `CRAFT-INITIAL-DEFINITION.md#executive-definition` |
| Craft Space | A bounded development space where intention is transformed into artifacts under shared schemas, data types, tools, validators, constitutions, axioms, and lifecycle routes. | candidate | `CRAFT-INITIAL-DEFINITION.md#craft-space` |
| Schema | The chosen representation that makes an intention legible enough to translate into an artifact, behavior, plan, validation surface, or method rule. | candidate | `CRAFT-INITIAL-DEFINITION.md#schema` |
| Data | The produced, populated, observed, executed, or validated counterpart of a schema. | candidate | `CRAFT-INITIAL-DEFINITION.md#data` |
| Functor-Like Translator | The composite translation process made from human intent, LLM behavior, context, tools, local vocabulary, validation, and governance. | candidate | `CRAFT-INITIAL-DEFINITION.md#functor-like-translator` |
| PCRA Translation | The probabilistic, contextual, relational, and attentive behavior of LLM-centered translation. | candidate | `CRAFT-INITIAL-DEFINITION.md#functor-like-translator`, `CRAFT-INITIAL-DEFINITION.md#entropy-scu-and-pcra-translation` |
| Residue | Meaningful mismatch, loss, ambiguity, contradiction, unexpressed structure, scope pressure, or validation gap left by schema/data translation. | candidate | `CRAFT-INITIAL-DEFINITION.md#residue` |
| Entropy | The uncertainty pressure introduced when a schema is translated into data by a PCRA translator. | candidate | `CRAFT-INITIAL-DEFINITION.md#entropy-scu-and-pcra-translation` |
| Smallest Coherent Unit | The smallest unit that still has meaning, one primary responsibility, inputs, outputs, validation or review surface, failure behavior, and a recomposition path. | candidate | `CRAFT-INITIAL-DEFINITION.md#smallest-coherent-unit` |
| SCU | Abbreviation for Smallest Coherent Unit. It is the general Craft unit boundary used to reduce translation entropy without losing recomposition meaning. | candidate | `CRAFT-INITIAL-DEFINITION.md#smallest-coherent-unit` |
| SWU | Smallest Working Unit: a planning and execution-specific form of SCU with write scope, acceptance evidence, and validation. | candidate | `CRAFT-INITIAL-DEFINITION.md#conversation-synthesis`, `CRAFT-GAP-CLOSURE-WORK-PACK.md#task-contracts` |
| Reflection | The review step that inspects residue, validation evidence, and recomposition fitness after an artifact or unit is produced. | candidate | `CRAFT-INITIAL-DEFINITION.md#conversation-synthesis`, `CRAFT-INITIAL-DEFINITION.md#loop-3-turn-definition-into-method` |
| Reflection Tower | The recursive structure created when residue cannot close inside the current schema/data layer and needs a new layer with its own schema and data. | candidate | `CRAFT-INITIAL-DEFINITION.md#conversation-synthesis` |
| Recomposition | The act of reconnecting a completed lower-level unit to its parent context or downstream consumer without losing meaning, evidence, or responsibility. | candidate | `CRAFT-INITIAL-DEFINITION.md#smallest-coherent-unit`, `CRAFT-LEDGER-TYPE-SYSTEM.md#base-blocker-types` |
| Validation | The review, test, checklist, or evidence comparison that proves a claim enough for the current layer and records pass, flag, or block. | validated-by-mvp | `LEDGER-VALIDATION.md#summary-verdict`, `LEDGER-VALIDATION.md#validation-checklist` |
| Promotion | A later authority decision that moves a candidate definition, artifact, route, or method into a more canonical surface. It is not automatic from local validation. | candidate | `SESSION-LEDGER.md#decision-ledger`, `CRAFT-GAP-CLOSURE-WORK-PACK.md#gate-checks` |
| Route | A selected next capability or lifecycle path, such as invoke, refine, task-session, decision-gate, architecture planning, or deferred side thread. | candidate | `CRAFT-RECURSIVE-LEDGER-GLOSSARY.md#terms`, `SESSION-LEDGER.md#current-next-move` |
| Handoff | A selective transfer artifact that gives another thread, route, or runtime the context, obligations, boundaries, and expected next work without dumping unrelated session state. | candidate | `ARCANUM-SKILL-RUNTIME-HANDOFF.md`, `CRAFT-GAP-CLOSURE-WORK-PACK.md#task-contracts` |

## Recursive Ledger Terms

| Term | Definition | Status | Source Anchors |
| --- | --- | --- | --- |
| Context | A bounded development space with its own purpose, lifecycle stage, artifacts, relationships, gate, and next move. | validated-by-mvp | `CRAFT-RECURSIVE-LEDGER-GLOSSARY.md#terms`, `LEDGER.md#context-rows`, `LEDGER-VALIDATION.md#validation-checklist` |
| Craft Context | A context inside the Craft package or recursive ledger that may represent a project, subproject, method slice, experiment, or work area. | validated-by-mvp | `CRAFT-RECURSIVE-LEDGER-GLOSSARY.md#terms`, `LEDGER.md#context-rows` |
| Artifact | A file, decision, output, work-pack, validation result, handoff, generated product, or other produced object owned by a context. | validated-by-mvp | `CRAFT-RECURSIVE-LEDGER-GLOSSARY.md#terms`, `LEDGER.md#artifact-rows`, `LEDGER-VALIDATION.md#validation-checklist` |
| Owned Artifact | An artifact for which one context is the primary development or maintenance owner, even if other contexts reference it. | validated-by-mvp | `CRAFT-RECURSIVE-LEDGER-GLOSSARY.md#terms`, `LEDGER.md#artifact-rows` |
| Recursive Ledger | A ledger where contexts can contain child contexts while also relating across branches through blockers, enablers, dependencies, evidence, and decisions. | validated-by-mvp | `CRAFT-RECURSIVE-LEDGER-GLOSSARY.md#terms`, `LEDGER.md#purpose`, `LEDGER-VALIDATION.md#summary-verdict` |
| Context Tree | The parent/child containment structure of contexts. It captures nesting but not every cross-context relation. | validated-by-mvp | `CRAFT-RECURSIVE-LEDGER-GLOSSARY.md#terms`, `LEDGER.md#context-rows` |
| Cross-Context Relation | A blocker, enabler, dependency, informing relation, or supersession between contexts or artifacts that may not share the same parent. | validated-by-mvp | `CRAFT-RECURSIVE-LEDGER-GLOSSARY.md#terms`, `LEDGER.md#relation-rows` |
| Ledger Row | A structured entry describing one context, artifact, relation, typed item, gate, enabler, blocker, decision, or event. | validated-by-mvp | `CRAFT-RECURSIVE-LEDGER-GLOSSARY.md#terms`, `LEDGER.md#context-rows`, `LEDGER.md#typed-item-rows` |
| Work-Pack | A task-execution artifact that decomposes work into tasks, gates, blockers, validation, and sometimes SWUs. In Craft ledger terms, it is an artifact owned by a context, not the whole context. | validated-by-mvp | `CRAFT-RECURSIVE-LEDGER-GLOSSARY.md#terms`, `LEDGER.md#artifact-rows`, `LEDGER-VALIDATION.md#validation-checklist` |
| Next Responsible Move | The concrete next action for a context after considering stage, gate, blockers, enablers, and route boundaries. | validated-by-mvp | `CRAFT-RECURSIVE-LEDGER-GLOSSARY.md#terms`, `LEDGER.md#context-rows` |
| Context Stage | The lifecycle state of a context, such as idea, define, design, plan, execute, validate, reflect, blocked, or closed. | validated-by-mvp | `CRAFT-RECURSIVE-LEDGER-GLOSSARY.md#terms`, `LEDGER.md#context-rows` |

## Condition And Routing Terms

| Term | Definition | Status | Source Anchors |
| --- | --- | --- | --- |
| Blocker | A condition or relation where a context, artifact, decision, missing requirement, failed validation, or unresolved authority question prevents progress. | validated-by-mvp | `CRAFT-RECURSIVE-LEDGER-GLOSSARY.md#terms`, `CRAFT-LEDGER-TYPE-SYSTEM.md#base-blocker-types`, `LEDGER.md#typed-item-rows` |
| Gate | A pass, flag, or block check that must be satisfied before a context, artifact, or task can move forward. | validated-by-mvp | `CRAFT-RECURSIVE-LEDGER-GLOSSARY.md#terms`, `CRAFT-LEDGER-TYPE-SYSTEM.md#base-gate-types`, `LEDGER.md#typed-item-rows` |
| Enabler | A condition or relation where a context, artifact, decision, or evidence item makes another context able to progress. | validated-by-mvp | `CRAFT-RECURSIVE-LEDGER-GLOSSARY.md#terms`, `CRAFT-LEDGER-TYPE-SYSTEM.md#base-enabler-types`, `LEDGER.md#typed-item-rows` |
| Condition Type | A shared or context-specific type that explains what kind of blocker, gate, or enabler is present. | validated-by-mvp | `CRAFT-LEDGER-TYPE-SYSTEM.md#type-model`, `LEDGER.md#typed-item-rows` |
| Base Type | A condition type shared across Craft contexts, such as `decision_blocker`, `validation_gate`, or `artifact_enabler`. | validated-by-mvp | `CRAFT-LEDGER-TYPE-SYSTEM.md#base-type-principles`, `CRAFT-LEDGER-TYPE-SYSTEM.md#base-blocker-types` |
| Context-Specific Type | A local subtype that extends a base condition type inside one context family, such as `ledger.cross_context_relation_blocker`. | validated-by-mvp | `CRAFT-LEDGER-TYPE-SYSTEM.md#context-specific-types`, `LEDGER.md#typed-item-rows` |
| Lane | An operational responsibility lane that names the expertise needed for a condition, such as business, tech, qa, validator, auditor, governance, planner, operations, integrator, or blocker_refiner. | validated-by-mvp | `CRAFT-LEDGER-TYPE-SYSTEM.md#operational-lanes`, `LEDGER-VALIDATION.md#conflict-and-lane-review` |
| Operational Lane | Same as lane; emphasizes that the lane is a responsibility category, not a person, agent, tool, or final delegation route. | validated-by-mvp | `CRAFT-LEDGER-TYPE-SYSTEM.md#operational-lanes` |
| Role Hint | A non-binding suggested future role or responsibility target derived from a condition type and lane. | validated-by-mvp | `CRAFT-LEDGER-TYPE-SYSTEM.md#role-mapping-model`, `LEDGER.md#typed-item-rows` |
| Role Mapping | A future mapping from condition type plus lane to a local role or route. It is modeled now but automation is deferred. | deferred | `CRAFT-LEDGER-TYPE-SYSTEM.md#role-mapping-model`, `LEDGER-VALIDATION.md#open-flags` |
| Blocker Refiner | The responsibility lane or role that turns a raw blocker into a typed, lane-owned, evidence-backed blocker with a closure condition before resolution is allowed. | validated-by-mvp | `CRAFT-LEDGER-TYPE-SYSTEM.md#blocker-refinement-rule`, `LEDGER-VALIDATION.md#blocker-lifecycle-review` |
| Blocker Refinement Gate | The gate that prevents raw or merely typed blockers from being marked resolved until they are refined or explicitly waived. | validated-by-mvp | `CRAFT-LEDGER-TYPE-SYSTEM.md#base-gate-types`, `CRAFT-LEDGER-TYPE-SYSTEM.md#blocker-refinement-rule`, `LEDGER-VALIDATION.md#blocker-lifecycle-review` |
| Waiver | An explicit decision that allows a blocker or strict requirement to close without the normal refinement or validation path, while preserving decision evidence and rationale. | validated-by-mvp | `LEDGER.md#typed-item-rows`, `LEDGER.md#decision-rows`, `LEDGER-VALIDATION.md#blocker-lifecycle-review` |

## Deferred Terms

| Term | Definition | Status | Source Anchors |
| --- | --- | --- | --- |
| Priority Scoring | A future mechanism for ranking contexts or next moves using blockers, enablers, readiness, importance, confidence, lane load, and downstream impact. | deferred | `CRAFT-RECURSIVE-LEDGER-GLOSSARY.md#terms`, `LEDGER-VALIDATION.md#open-flags` |
| Generated Index | A future machine-readable index over ledger rows for repeated query, automation, or runtime use. | deferred | `LEDGER.md#deferred-index`, `LEDGER-VALIDATION.md#generated-index-decision` |
| Role Delegation Automation | A future automation layer that assigns or routes work using type, lane, role hints, evidence, and confidence. | deferred | `CRAFT-LEDGER-TYPE-SYSTEM.md#role-mapping-model`, `LEDGER-VALIDATION.md#open-flags` |
| Runtime Interface | The command, adapter, observation envelope, or skill execution surface that may later run or observe Craft-related work. | deferred | `CRAFT-REFINE-RUNTIME-STRATEGY.md`, `ARCANUM-SKILL-RUNTIME-HANDOFF.md` |

## Architecture Planning Boundary

This glossary closes the vocabulary blocker for the next architecture pass. It does not solve architecture-owned inputs such as route integration, validation example-suite shape, promotion policy, scoring, generated indexes, or role delegation automation.

Those belong to later tasks in [CRAFT-GAP-CLOSURE-WORK-PACK.md](CRAFT-GAP-CLOSURE-WORK-PACK.md) or the broader Craft method architecture package.
