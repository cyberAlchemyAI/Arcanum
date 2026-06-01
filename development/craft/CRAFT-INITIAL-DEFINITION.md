# Craft Initial Definition

Status: initial research product
Date: 2026-05-24
Scope: define Craft as a method primitive and candidate Arcanum/CyberAlchemy capability
Source frame: supplied multi-day conversation, local Arcanum/DomainSpec/CyberAlchemy artifacts, bounded external research

## Executive Definition

Craft is the recursive method for turning an intention into a stable artifact by moving between schema and data until the smallest coherent unit for the current objective is found, executed, validated, and recomposed into its upper context.

Craft treats building as a two-layer operation:

- Schema: the chosen representation of intent, domain structure, constraints, constitutions, axioms, specs, plans, architectures, and method rules.
- Data: the concrete artifact, observation, runtime behavior, implementation, validation output, or situated instance produced from that schema.

The working system is not the schema alone and not the data alone. The working system is the translation relation that binds them: the functor-like process made from human intent, LLM behavior, harnessing, local vocabulary, context, tools, validation, and governance.

Craft exists because this translation is never perfectly lossless in agentic work. Every attempt to turn schema into data produces residue: ambiguity, missing structure, drift, hidden assumptions, excess scope, brittle minimalism, or behavior that the current layer cannot explain. Craft names the discipline for detecting that residue, deciding whether it belongs in the current layer or a new one, and then creating the next responsible schema/data pair.

## Conversation Synthesis

The conversation converges on one central insight: DomainSpec and Arcanum are no longer only documentation or prompt frameworks. They are becoming a system for modeling the process by which intent becomes artifact under lossy translation.

The shared vocabulary that emerged:

- A domain is represented by schemas, but the schemas only become useful when populated, executed, or translated into data.
- An LLM is not a deterministic compiler. It behaves like a probabilistic, contextual, relational, attentive translator.
- Because the translator is probabilistic and attention-bounded, the output always leaves residue.
- Residue is not merely error. It is signal that the current layer may be missing a schema, boundary, taxonomy, axiom, constitution, or smaller unit of responsibility.
- Concept layering, now aligned with Distill, is the method for finding the smallest coherent unit that still carries meaning, inputs, outputs, responsibility, and a path back upward.
- Reflection tower is the recursive structure that appears when residue cannot be resolved inside the current schema/data layer. A new layer is created to explain the residue with its own schema and data.
- SWU is a domain-specific case of SCU: a Single Work Unit is the smallest coherent unit in planning and execution.
- Each repository, project, or bounded craft space can be understood as a tower: it contains layers of schema/data translation and residue handling.

The sharpest formulation from the conversation is:

```text
Craft is the recursive search for the next smallest coherent schema/data layer
needed to translate intent into artifact with acceptable residue.
```

## Research Grounding

This definition is grounded in local system evidence first.

Local evidence:

- `arcanum/framework/CYBERALCHEMY-METHOD.md` already defines governed synthesis through objective, artifact, discovery, tension, route, trace, and reflection.
- `arcanum/arcana/distill/README.md` already defines the search for the smallest coherent unit, reduction, recomposition, and deferred complexity.
- `cyberAlchemy/agentic-system-architecture.md` already defines translation residue as loss, ambiguity, contradiction, or unverified assumption when moving between schema and data.
- `implementation/domainspec/AXIOMS.md` and `implementation/domainspec/CONSTITUTION.md` already distinguish axioms as load-bearing behavior foundations and constitutions as enforceable structural rules.
- `arcanum/arcana/refine/REFINEMENT-LOOP.md` already defines a full refinement loop using context-builder, invoke, interrogation, research, distill, repair, plan, final interrogation, and synthesis.

External research used as analogy, not authority:

- David Spivak's Functorial Data Migration frames a database schema as a small category and an instance as a Set-valued functor on it. This supports the schema/data/functor reading, but Craft generalizes it operationally beyond databases.
- Lawvere's functorial semantics treats algebraic theories and models through functorial structure. This supports the intuition that a "theory" can be understood by the maps that preserve its structure.
- Mark Bedau's weak emergence supports the idea that some system-level properties are derivable only by simulation or composition, not by inspecting a single component. Craft should claim compositional emergence, not mystical strong emergence.

## Refine Trace

Requested mode: three `/refine` loops, max mode, with research.

Command-surface note: `arcanum/tools/arcanum --resolve /refine` currently returns `unknown Arcanum command: refine`, while `arcanum/arcana/refine` exists. This product therefore records three Refine-style loops using the installed Refine contract as the process model, rather than claiming a resolved slash-command execution.

### Loop 1: Define The Object

Question: What is Craft?

Result:

Craft is not just "building software." Craft is the recursive schema/data translation method for converting intention into artifact under probabilistic, contextual, relational, attentive translation.

Correction:

Avoid defining Craft as a universal theory of reality. The safer initial definition is operational and simulation-oriented: Craft models the structure a reality-like building process would need if intention, representation, translation, residue, and reflection were first-class.

### Loop 2: Stabilize The Formal Spine

Question: What are the primitives?

Result:

The minimum spine is:

```text
Intent
  -> chosen schema
  -> functor-like translator
  -> data/artifact
  -> residue
  -> decision: absorb, split, route, or promote
  -> next schema/data layer when residue cannot close locally
```

Correction:

Do not treat "fully faithful" or "isomorphism" as achievable by default with LLMs. In this system, the translator is PCRA: probabilistic, contextual, relational, attentive. The target is not zero residue; it is acceptable, named, governed residue.

### Loop 3: Turn Definition Into Method

Question: How does Craft operate?

Result:

Craft operates as a lifecycle:

```text
Define -> Design -> Plan -> Execute -> Validate -> Reflect
```

Each phase can use local constitutions, axioms, taxonomies, relationship maps, and phase-specific method contracts. Each phase may produce residue. When residue is load-bearing, Craft applies Distill, abstraction, interrogation, invoke, refine, x-ray, or another method to decide whether the current layer is too large, too small, missing a relation, missing a domain schema, or ready to execute.

Correction:

Reflection tower should not be only a concept. It should become the recursive residue-handling method inside Craft.

## Initial Vocabulary

### Craft Space

A bounded space where an intention is transformed into artifacts under a shared set of schemas, data types, tools, validators, constitutions, axioms, and lifecycle routes.

Examples:

- a repository,
- a product domain,
- a feature package,
- an Arcanum sigil,
- a DomainSpec project,
- a research/lifecycle packet.

### Schema

The chosen structure that makes an intention legible enough to translate. A schema can be a domain model, spec, architecture, plan, task, taxonomy, constitution, axiom set, interface, workflow, or method contract.

Schemas are observer-conditioned. A schema is not simply "in the world"; it is chosen by an observer for a purpose. Once chosen, it constrains valid instances.

### Data

The populated, produced, observed, or executed counterpart of a schema. Data can be code, documents, runtime behavior, validation evidence, telemetry, a generated artifact, a task result, or a concrete domain instance.

### Functor-Like Translator

The process that maps schema to data while attempting to preserve structure.

In Craft, this translator is usually not one thing. It is a composite:

```text
human intention
+ LLM behavior
+ prompt/schema/harness
+ tools
+ context
+ local vocabulary
+ validation and feedback
```

For LLM-centered work, the translator is PCRA:

- Probabilistic: output is distributional, not deterministic.
- Contextual: output depends on the selected context and conversation state.
- Relational: meaning depends on relations between concepts, artifacts, roles, and constraints.
- Attentive: fidelity is bounded by attention, context size, salience, and time.

### Residue

Residue is any meaningful mismatch, loss, ambiguity, contradiction, unexpressed structure, scope pressure, or validation gap left by a schema/data translation.

Residue is not automatically failure. It becomes actionable when it affects fidelity, safety, recomposition, execution, validation, or future understanding.

### Smallest Coherent Unit

An SCU is the smallest coherent unit that still has:

- meaning in the current craft space,
- one primary responsibility,
- inputs,
- outputs,
- validation or review surface,
- failure behavior,
- recomposition path into the upper layer.

The SCU is the current best point of low entropy for translation. It is small enough to reduce attention loss and large enough to avoid meaningless fragmentation.

### Entropy, SCU, And PCRA Translation

Entropy in Craft is the uncertainty introduced when a schema is translated into data by a PCRA functor-like process.

For LLM-centered work, entropy does not only mean randomness. It is the practical uncertainty produced by four coupled properties:

- Probabilistic spread: the model can produce many plausible continuations for the same schema.
- Contextual dependence: small changes in supplied context, conversation history, examples, or surrounding artifacts can shift the output.
- Relational load: the model must preserve relations between many concepts, constraints, files, roles, and downstream obligations.
- Attentional decay: as the unit grows, relevant details compete for salience and the model becomes more likely to drop, flatten, or overfit parts of the schema.

The PCRA translator therefore has a non-linear fidelity curve. Very small units can lose meaning because they no longer contain enough relation to recompose. Very large units can lose fidelity because they exceed the translator's practical attention and relation-preservation budget. The SCU is the local minimum between those failures.

```text
Too small:
  low context, low meaning, high recomposition ambiguity

SCU:
  enough context, one responsibility, low translation entropy,
  clear validation, clear recomposition

Too large:
  high context load, mixed responsibilities, attention loss,
  relation drift, rising residue
```

This is why SCU is not "the smallest possible unit." The smallest possible unit can be semantically underdetermined. SCU is the smallest coherent unit: the smallest unit that still gives the PCRA translator enough structure to preserve meaning while reducing the number of competing relations it must hold at once.

In practice, entropy rises when:

- one unit carries multiple responsibilities,
- inputs or outputs are implicit,
- validation is not local to the unit,
- the unit requires facts scattered across too many artifacts,
- the schema uses overloaded or unstable vocabulary,
- the task asks the translator to preserve too many cross-layer relations,
- the recomposition path is assumed rather than specified,
- attention is spent on broad context instead of load-bearing obligations.

Entropy decreases when:

- the unit has one primary responsibility,
- vocabulary is local and explicit,
- inputs, outputs, and failure behavior are named,
- validation can be run or reviewed at the unit boundary,
- relations are declared rather than implied,
- context is selected because it closes an obligation,
- recomposition is proven before execution,
- residue from previous runs is fed back into schema repair.

Residue is the observable trace of entropy after translation. Entropy is the uncertainty pressure before and during translation; residue is what remains after the artifact exists and validation compares it back to the schema.

```text
Schema + PCRA translator -> Data
translation entropy        -> Residue after validation
```

Craft uses SCU selection to minimize entropy before execution, and residue analysis to learn where entropy actually appeared.

### Single Work Unit

An SWU is an SCU in the context of planning and execution. It is the smallest executable unit that can be assigned, run, validated, and recomposed into a task, wave, plan, and larger artifact.

### Reflection Tower

Reflection tower is the recursive structure produced when residue from one schema/data translation becomes the data that demands a new schema.

```text
Layer N:
  Schema_N -> Translator_N -> Data_N -> Residue_N

If Residue_N cannot be explained or closed locally:
  Residue_N becomes the seed data for Schema_N+1
```

The tower stops when the current domain objective has acceptable residue, not when the system reaches universal completeness.

## Craft Cycle

Craft is always some configured form of:

```text
Define -> Design -> Plan -> Execute -> Validate -> Reflect
```

### 1. Define

Purpose: turn raw intent into a named schema candidate.

Inputs:

- user prompt,
- raw files,
- prior artifacts,
- examples,
- research,
- constraints,
- local vocabulary,
- existing schemas,
- conversation residue.

Outputs:

- objective,
- output artifact,
- scope boundary,
- initial definitions,
- candidate domain map,
- unknowns,
- residue ledger.

Closure condition:

The system can say what is being built, why, for whom or what, in what bounded craft space, and what artifact should exist next.

### 2. Design

Purpose: choose the structure that can hold the definition.

Outputs:

- architecture,
- domain model,
- taxonomy,
- relationships,
- capabilities,
- operations,
- entities,
- events,
- UI or interaction model,
- method contracts,
- validation shape.

Closure condition:

The structure has enough relations, responsibilities, and constraints to support planning without hidden glue.

### 3. Plan

Purpose: convert design into staged execution.

Canonical decomposition:

```text
Plan -> Waves -> Tasks -> SWUs
```

Closure condition:

The next SWU can be executed with clear inputs, outputs, done criteria, validation, and recomposition path.

### 4. Execute

Purpose: produce the data/artifact from the selected schema and plan.

Closure condition:

An artifact exists and can be inspected against the schema that produced it.

### 5. Validate

Purpose: compare data back to schema and measure residue.

Validation can include:

- tests,
- static checks,
- link checks,
- schema validation,
- ontology review,
- interrogation,
- x-ray,
- human review,
- runtime telemetry,
- domain metrics.

Closure condition:

Residue is classified as acceptable, repairable in current layer, requiring a new layer, or requiring a human decision.

### 6. Reflect

Purpose: decide whether repeated residue should update the method, schema, taxonomy, constitution, axiom, lifecycle route, or future context pack.

Closure condition:

The lesson is either discarded, recorded as candidate knowledge, promoted through governance, or routed to a new craft layer.

## Layer Families

Craft recognizes recurring schema/data ladders.

Domain ladder:

```text
Domain
  -> bounded contexts
  -> specs
  -> aspects, taxonomy, relationships, architecture, plan
```

Spec ladder:

```text
Spec
  -> capabilities
  -> operations
  -> entities
  -> events
```

Architecture ladder:

```text
Spec
  -> architecture
  -> infrastructure
  -> domain model
  -> UI / interaction surface
```

Planning ladder:

```text
Plan
  -> waves
  -> tasks
  -> SWUs
```

These ladders are not a fixed ontology of everything. They are common craft paths that should be overridden or composed by phase-specific definitions when the domain requires it.

## Residue Classification

Craft should distinguish at least five residue types.

| Residue Type | Description | Typical Response |
| --- | --- | --- |
| Translation residue | Output does not preserve enough of the schema's intended structure. | Refine prompt/schema, add validation, reduce unit size. |
| Domain residue | The schema lacks domain relations, terms, entities, constraints, or behavior. | Define/research domain, update taxonomy, relationships, specs. |
| Structural residue | The artifact shape cannot hold the required relations or lifecycle. | Redesign architecture, split layer, add interface or boundary. |
| Attention residue | The unit is too large or context too noisy for high-fidelity translation. | Distill to SCU/SWU, improve context pack, reduce scope. |
| Entropy residue | The PCRA translator had too many plausible paths, unstable terms, hidden obligations, or competing relations. | Reduce relation load, declare inputs/outputs, stabilize vocabulary, add examples or constraints. |
| Recomposition residue | The unit works locally but cannot be cleanly reattached to the upper schema. | Add recomposition proof, widen unit slightly, or define the missing bridge relation. |
| Governance residue | The system cannot determine authority, validation, promotion, or route. | Apply constitution, axiom, decision gate, task-session, or lifecycle owner. |

## Reflection Tower Method

Use reflection tower when a residue cannot be closed by local repair.

1. Name the residue.
2. Identify the schema/data pair that produced it.
3. Ask whether the residue is caused by missing information, excessive unit size, underspecified unit size, wrong abstraction level, missing relation, excessive entropy, missing validation, or wrong lifecycle owner.
4. If local repair is enough, repair the current layer.
5. If the residue implies a missing schema, promote the residue into a new layer seed.
6. Define the next layer's objective, schema, data target, validation, and recomposition path.
7. Stop when the domain's closure criteria are met or when further decomposition increases residue.

The key stop criterion:

```text
Do not keep splitting because splitting is possible.
Split only while residue decreases and recomposition remains meaningful.
```

The reflection tower is triggered when entropy cannot be reduced by merely shrinking the unit. Sometimes the SCU is already as small as it can responsibly be, but residue still appears because a higher schema is missing. In that case, the answer is not "make the task smaller." The answer is "name the missing layer that would make this task coherent."

```text
If unit too large:
  reduce toward SCU.

If unit already SCU but residue remains:
  inspect missing schema, relation, axiom, constitution, or domain layer.

If smaller unit increases residue:
  stop reduction and repair the upper layer.
```

## Constitutions And Axioms

Craft uses two governing rule families.

Constitutions enforce form and structure:

- artifact shape,
- lifecycle boundaries,
- required fields,
- source of truth,
- validation gates,
- promotion paths,
- allowed composition.

Axioms enforce behavior and load-bearing principles:

- semantic authority precedes implementation,
- governance must be computable,
- observation must be independent from execution,
- trace precedes promotion,
- reflection stays an outer loop.

In Craft terms:

```text
Constitution: what shape must the craft operation obey?
Axiom: what behavioral truth must remain invariant across craft operations?
```

## Method Routing

Craft does not replace existing Arcanum capabilities. It composes them.

| Situation | Route |
| --- | --- |
| Intent is vague or phase target unclear | `invoke define`, `scope-interview`, `definitions-governance` |
| Unit is too broad or residue increases with size | `distill` |
| Design may be brittle, oversized, misleading, or unsafe | `interrogation` |
| Existing artifact needs critique or method sharpening | `refine` |
| Need lifecycle define/design/plan/validate artifact | `invoke` |
| Need implementation-ready task/SWU execution | `task-session` |
| Need hidden failure, inconsistency, or artifact inspection | `x-ray` |
| Repeated usage residue should update capability | `workflow-reflect`, `signal-observer`, `sigil-maintenance-loop` |

Craft is the outer method that decides which route is responsible at each residue point.

## Stop Criteria

Craft should stop a layer when one of these is true:

1. The artifact validates against the current schema with acceptable residue.
2. Further decomposition removes meaning or creates hidden glue.
3. The next residue is a human decision, not a modeling problem.
4. The next residue belongs to another lifecycle owner.
5. Domain-specific metrics prove the current schema is stable enough.
6. The cost of the next layer exceeds the value of residue reduction.

Craft should continue upward or outward when:

1. residue repeats across runs,
2. validation fails for structural reasons,
3. the SCU becomes too large and entropy increases,
4. the current schema cannot express a necessary domain relation,
5. governance cannot tell who owns the next move,
6. recomposition is unclear.

## Initial Formal Model

Let a craft operation be:

```text
C = (I, S, F, E, D, R, G, V)
```

Where:

- `I` is intention.
- `S` is the chosen schema.
- `F` is the functor-like translator.
- `E` is translation entropy: uncertainty pressure created by PCRA properties, context load, relation load, and unit sizing.
- `D` is the produced data/artifact.
- `R` is residue.
- `G` is governance: constitutions, axioms, routes, ownership.
- `V` is validation: the comparison of data back to schema under domain closure criteria.

The basic operation:

```text
F_PCRA(I, S, context, tools) -> D
E = entropy(F_PCRA, S, context, relation_load, unit_size)
V(S, D, G) -> R
```

If `R` is acceptable, the layer closes.

If `R` is repairable, revise `S`, `F`, context, or `D` inside the same layer.

If `R` is structural, promote it:

```text
R_N -> I_N+1
```

That is the reflection tower step.

SCU selection is the pre-translation control on `E`:

```text
choose SCU such that:
  meaning(SCU) is sufficient
  responsibility(SCU) is singular
  relation_load(SCU) is bounded
  validation(SCU) is local
  recomposition(SCU -> upper schema) is explicit
```

Residue analysis is the post-translation evidence about `E`:

```text
if R shows missing details:
  repair schema or context

if R shows attention loss:
  reduce unit or improve context selection

if R shows relation drift:
  declare relationships or split responsibilities

if R shows recomposition failure:
  widen unit or add bridge schema

if R persists at SCU:
  climb the reflection tower
```

## Philosophical Horizon: Toward A Universal Physics Of Craft

Craft should not be reduced to a productivity tool. Its deeper thesis is that making is not an accidental human activity but a general transformation pattern: intention, constraint, structure, translation, manifestation, residue, and recursive repair.

In this lens, Craft asks:

```text
If reality had a "making process" built into its fabric,
what primitives would that process need?
```

The proposed answer is not "tasks" or "prompts." Those are local engineering forms. The deeper primitives are:

- difference: something is not yet in the form it could take,
- intention or attractor: a direction of possible becoming,
- schema: a chosen structure that makes the possible legible,
- functor-like translation: a structure-preserving transformation from one layer to another,
- data or artifact: the realized instance of that transformation,
- residue: what the transformation could not preserve, explain, or stabilize,
- reflection: the act of making residue into the seed of a new layer,
- recomposition: the return path by which the new layer changes the whole.

This is the sense in which Craft can become a "universal physics of craft": not a claim that every physical law has already been derived from Craft, but a research program for describing how coherent things come into being across domains.

The universal claim should therefore be staged:

1. Operational claim: Craft improves agentic artifact creation by governing schema/data translation and residue.
2. Formal claim: Craft can be modeled as recursive structure-preserving transformation with residue and recomposition.
3. Philosophical claim: all making can be understood as layered translation from potential structure into manifested instance under constraint.
4. Universal physics claim: reality itself may be intelligible as a recursive craft process where stable forms are the closure points of repeated schema/data/residue dynamics.

This gives Craft depth without pretending the deepest claim is already proven. The operational method becomes the laboratory where the philosophical claim earns or loses force.

### Craft As Simulation Of Making

The project can be framed as an attempt to simulate the act of making itself.

Not simulate one product. Not simulate one software lifecycle. Simulate the general process by which:

```text
possible form
  -> selected schema
  -> constrained translation
  -> manifested artifact
  -> measured residue
  -> next layer of explanation
```

In this reading, Arcanum's capabilities are not merely commands. They are instruments in a craft physics:

- `invoke` gives form to intention.
- `distill` searches for the smallest coherent unit of coherent transformation.
- `interrogation` applies tension so false closure breaks before it hardens.
- `refine` repeats the loop until the artifact can carry its responsibility.
- `x-ray` inspects hidden structure and failure surfaces.
- `task-session` turns selected units into governed execution.
- observability and reflection let the system learn from the residue it leaves behind.

The philosophical move is that residue is not waste. Residue is the evidence that reality, artifact, and schema are not yet in full relation. Craft advances by turning that remainder into the next object of thought.

### The Honesty Boundary

The universal physics lens is valuable only if Craft keeps an honesty boundary.

Craft may pursue universal structure, but each local use must still answer:

- What was the chosen schema?
- What data or artifact did it produce?
- What residue remained?
- What validation showed that residue?
- What layer, route, or stop criterion follows?

Without those questions, "universal physics" becomes aesthetic language. With them, it becomes a disciplined research direction: a way to let practical building generate philosophical evidence.

## Initial Definition For Arcanum

Craft is a candidate Arcana-level method for recursively governing artifact creation across DomainSpec, Arcanum, and CyberAlchemy.

It should provide:

- a vocabulary for schema/data/functor/residue in operational work,
- a residue classifier,
- a reflection tower method,
- SCU/SWU selection criteria,
- phase-specific define/design/plan/execute/validate/reflect contracts,
- routing rules to existing sigils and spells,
- promotion rules for repeated residue into taxonomy, constitution, axiom, or capability updates.

It should preserve two levels:

- philosophical horizon: Craft can pursue a universal physics of making,
- operational claim: each current artifact must prove only the local schema/data/residue transformation it actually ran.

It should not initially:

- present the universal physics lens as already proven,
- replace Distill, Invoke, Refine, Interrogation, Task Session, or X-Ray,
- claim perfect isomorphism with LLM-centered translation,
- promote conversation insight directly into global axiom without evidence.

## Open Questions

1. Is Craft a new top-level Arcana sigil, a spell that composes existing sigils, or the name of the outer CyberAlchemy method layer?
2. Should reflection tower be its own method under Craft or a shared primitive available to Refine, Distill, X-Ray, and Invoke?
3. What are the first domain-specific stability metrics for deciding "residue acceptable enough"?
4. How should SCU be measured beyond prose: information load, validation surface, recomposition proof, context size, or execution failure rate?
5. What is the minimum artifact shape for a `CRAFT-RUN.md`?
6. How should repeated residue promote into taxonomy, constitution, or axiom without bloating governance?
7. What would count as evidence for the universal physics claim: cross-domain recurrence, formal proof, simulation behavior, practical compression, or predictive power?
8. How can Craft talk about reality-level making without losing the local validation discipline that makes it useful?

## Proposed Next Product

Create a Craft development packet:

```text
arcanum/development/craft/
  CRAFT-INITIAL-DEFINITION.md
  CRAFT-GLOSSARY.md
  REFLECTION-TOWER-METHOD.md
  RESIDUE-TAXONOMY.md
  CRAFT-CYCLE.md
  CRAFT-RUN-TEMPLATE.md
  INTERROGATION-REVIEW.md
  SIGIL-HANDOFF.md
```

The next bounded work should not implement runtime behavior yet. It should first harden:

- definitions,
- residue taxonomy,
- reflection tower method,
- SCU/SWU criteria,
- route table,
- validation examples.

## Sources

Local:

- `arcanum/framework/CYBERALCHEMY-METHOD.md`
- `arcanum/arcana/distill/README.md`
- `arcanum/arcana/refine/README.md`
- `arcanum/arcana/refine/REFINEMENT-LOOP.md`
- `cyberAlchemy/agentic-system-architecture.md`
- `implementation/domainspec/AXIOMS.md`
- `implementation/domainspec/CONSTITUTION.md`

External:

- David I. Spivak, "Functorial Data Migration", arXiv:1009.1166, https://arxiv.org/abs/1009.1166
- F. William Lawvere, "Functorial Semantics of Algebraic Theories", 1963, https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/lawvere.pdf
- Mark A. Bedau, "Weak Emergence", 1997 abstract, https://people.reed.edu/~mab/papers/weak.emergence.ab.htm
