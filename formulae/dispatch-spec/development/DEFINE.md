# Dispatch Spec Define

## Invoke Define Result

- Mode: `define`
- Spell: `invoke`
- Target artifact: `dispatch-spec`
- Target type: draft Formulae sigil package
- Phase status: `pass`
- Mode contract: `spells/invoke/define.md`
- Template selection: Formulae validation package with schema, skill contract, glossary, and design companion artifacts.
- Next route: `spellcraft` when a reusable spell should consume dispatch documents; `experiment-harness` when validation examples are ready.

## Purpose

`dispatch-spec` defines a deterministic contract for describing a governed route through Arcanum sigils and spells. It validates the structure of a proposed composition without deciding the route itself and without executing any step.

The first target is a route graph that lets an operator write Arcanum-fluent sentences such as:

```text
Use dialectics to explore/exploit, then distill, x-ray the architecture, run toy games, and use a Pareto-aware decision process to find the best abstraction for this problem.
```

The dispatch document should preserve:

- operator intent,
- extracted Arcanum vocabulary,
- candidate capability menu,
- selected ordered steps,
- pattern per step,
- handoff artifacts,
- gates and stop conditions,
- observability grouping,
- promotion guardrails.

## Source Evidence

| Source | Contribution |
| --- | --- |
| `/tmp/weaver-spec/README.md` | Weaver is a contract layer, not a runtime; useful precedent for interface-first interoperability. |
| `/tmp/weaver-spec/docs/ARCHITECTURE.md` | Routing, execution, and orchestration should remain separate. |
| `/tmp/weaver-spec/docs/LIFECYCLE.md` | Route -> call -> interpret -> answer -> execute lifecycle inspires Arcanum dispatch stages. |
| `/tmp/weaver-spec/docs/GLOSSARY.md` | `ChoiceCard`, `SelectableItem`, `RoutingDecision`, `Frame`, `Handle`, and `TraceEvent` map cleanly to Arcanum routing. |
| `spells/necronomicon/README.md` | Necronomicon owns memory, route choice, no-promotion guardrails, and handoffs. |
| `arcana/spellcraft/README.md` | Spellcraft owns reusable spell composition from referenced sigils. |
| `spells/invoke/README.md` | Invoke owns define/design/plan/handoff authoring and routes lifecycle ownership onward. |
| `development/craft/CRAFT-INITIAL-DEFINITION.md` | SCU/SWU, residue, validation surface, and recomposition vocabulary define honest step boundaries. |
| `spells/whisper/README.md` | Existing spell example of substrate extraction, SCU tournament, composition, validation, and residue. |

## Scope

In scope:

- Draft Formulae package under `formulae/dispatch-spec/`.
- JSON schema for dispatch documents.
- Formulae skill contract for validation behavior.
- Weaver extraction note.
- Arcanum synthesis with taxonomy, sentence grammar, and examples.
- Invoke define/design development artifacts.

Out of scope:

- Runtime execution engine.
- Registry promotion.
- Automatic Necronomicon mutation.
- Spellcraft lifecycle completion.
- Full telemetry schema migration.
- Actual implementation of a validator CLI.

## Core Definitions

| Term | Definition |
| --- | --- |
| Dispatch document | A schema-valid object describing a sigil/spell route, including intent, steps, gates, handoffs, and observability. |
| Route pattern | The structural execution shape of a step, such as sequence, fanout, dialectic, tournament, x-ray, validation, toy game, synthesis, or handoff. |
| Capability reference | A stable pointer to a sigil, spell, mode, or runtime adapter without copying its internals. |
| Frame handoff | A safe step output summary consumed by a later step. |
| Handle handoff | A controlled reference to a larger artifact such as a report, HTML explanation, work-pack, or validation run. |
| Promotion guardrail | A rule preventing candidate knowledge, glossary terms, ontology concepts, sigils, or spells from becoming canonical without the owning lifecycle. |

## Decisions

| Decision | Selected Path | Rationale |
| --- | --- | --- |
| Tier | Formulae | The package validates known document structure rather than synthesizing routes. |
| First schema shape | JSON Schema | Matches Weaver contract style and is easy to validate locally. |
| Route pattern values | Starter enum | Gives validation teeth while remaining draft; future extension can loosen or add patterns. |
| Execution ownership | External owners | Dispatch Spec validates; Necronomicon, Spellcraft, Invoke, Task Session, and Experiment Harness own their respective work. |
| Promotion | Explicitly deferred | Draft package should not update registries or claim canonical status until validated. |

## Output Artifacts

| Artifact | Path | Status |
| --- | --- | --- |
| Package README | `formulae/dispatch-spec/README.md` | created |
| Skill contract | `formulae/dispatch-spec/SKILL.md` | created |
| Schema | `formulae/dispatch-spec/dispatch.schema.yml` | created |
| Weaver extraction | `formulae/dispatch-spec/WEAVER-EXTRACTION.md` | created |
| Synthesis | `formulae/dispatch-spec/ARCANUM-DISPATCH-SYNTHESIS.md` | created |
| Define artifact | `formulae/dispatch-spec/development/DEFINE.md` | this file |
| Glossary | `formulae/dispatch-spec/development/GLOSSARY.md` | created |
| Layering seed | `formulae/dispatch-spec/development/IMPLEMENTATION-LAYERING-SEED.md` | created |
| Define transport | `formulae/dispatch-spec/development/DEFINE-TRANSPORT.md` | created |

## Unresolved Gaps

| Gap | Status | Recommended Route |
| --- | --- | --- |
| No executable validator script yet. | non-blocker for define/design | `task-session` after design approval |
| Not registered in `registry/SIGILS.md`. | deliberate | `sigil-development` or explicit promotion task |
| No experiment harness examples. | expected draft gap | `experiment-harness` after SKILL stabilizes |
| Telemetry fields are proposed but not wired. | future integration | observed invocation loop / signal observer task |

