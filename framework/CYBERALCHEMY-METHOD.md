# CyberAlchemy Method

## Purpose

The CyberAlchemy Method is the working method behind Arcanum: a way to create, refine, validate, and evolve agent capabilities through governed synthesis.

It treats agent work as more than prompt execution. A useful agent capability is grown through intent, research, discovery, decomposition, tension, evidence, design, validation, observation, and reflection. The goal is not to make an agent sound clever; the goal is to make its reasoning reusable, inspectable, and improvable.

This document defines the baseline method so future sigils, spells, techniques, and agent collaborations can share the same operating model.

## At A Glance

CyberAlchemy is for work where the answer should become a reusable artifact, not just a momentary response.

The method keeps five things visible:

| Anchor | Question |
| --- | --- |
| Objective | What are we trying to solve? |
| Output artifact | What should exist when this work is done? |
| Discovery | What must we learn before the artifact can responsibly close? |
| Tension | What could make the artifact brittle, oversized, misleading, or unsafe? |
| Route | Who or what owns the next lifecycle step? |

The objective and output artifact are guiding stars, not chains. They help the user and agent understand the middle of the work, but they should be renamed when discovery proves that another output shape would solve the objective better.

## Core Thesis

Good agent systems are built by turning vague intent and discovered evidence into governed artifacts.

The method works by repeatedly moving between:

- **human intent**: what the user is trying to make possible,
- **objective and output artifact**: what the work is trying to solve and what form the result should take,
- **research and discovery**: what must be found, learned, compared, or tested before synthesis can responsibly close,
- **concept synthesis**: what the work means and how its parts fit,
- **structured tension**: what could be wrong, oversized, brittle, or premature,
- **artifact creation**: what stable document, spec, interface, or contract now exists,
- **ergonomic navigation**: how humans and agents can understand, traverse, and continue the work,
- **observability**: what the run teaches future maintenance,
- **lifecycle routing**: what authority should own the next step.

The agent is not a passive executor. It is a collaborator that helps shape the problem, preserves decisions, and makes the path forward more legible.

## Method Loop

The CyberAlchemy Method follows this loop. The loop is recursive: later discovery, tension, or validation may send the work back to an earlier step.

| Phase | Steps | Purpose |
| --- | --- | --- |
| Orient | 1-3 | Name the seed, bound the context, and state the current target result. |
| Discover | 4 | Find the evidence, gaps, unknowns, and alternative frames that matter. |
| Shape | 5-8 | Choose the route, draft the artifact, test it with tension, and revise toward closure. |
| Stabilize | 9-12 | Make the work navigable, preserve openness, record trace, and route ownership. |
| Evolve | 13 | Reflect after use so repeated work improves the method. |

1. **Name the seed**
   Capture the user's starting point in plain language. Do not rush to implementation before the intent has a stable name.

2. **Bound the context**
   Identify the working context, constraints, existing artifacts, target owner, and current lifecycle stage.

3. **Name the target result**
   State the current objective and expected output artifact: data model, architecture design, implemented code structure, plan, decision record, research map, technique spec, or another concrete result. Treat this as an orientation point that discovery may revise.

4. **Discover the unknowns**
   Search, inspect, interview, compare, and research enough to reveal the real terrain. Name what was discovered, what remains unknown, and which unknowns are blockers.

5. **Choose the governing route**
   Decide whether the work needs define, design, plan, validation, interrogation, lifecycle authoring, or execution. Use the smallest governing route that can responsibly hold the work.

6. **Create a draft artifact**
   Turn the intent into a concrete artifact: handoff, glossary, design, plan, technique spec, work-pack, or review record.

7. **Introduce structured tension**
   Use critique, Balancer roles, interrogation, premortems, or alternative tracks to find weak boundaries, hidden assumptions, premature complexity, and missing evidence.

8. **Revise toward closure**
   Do not merely add more detail. Revise until the artifact has enough closure for the current context: purpose, boundary, inputs, outputs, failure behavior, and next route.

9. **Make the work navigable**
   Organize the artifact so a human or future agent can quickly understand where to start, what matters, what changed, what is unresolved, and what action comes next.

10. **Preserve open-endedness**
   Closure is contextual, not final. Record what evolution pressure is likely, what should remain open, and what context change would invalidate the current artifact.

11. **Record the trace**
   Preserve decisions, rejected alternatives, unresolved tensions, validation status, and observability signals. The trace is part of the work, not administrative residue.

12. **Route the next owner**
   Hand the result to the correct lifecycle authority: sigil-development, spellcraft, implementation-layering, task-session, robot-talks, decision-gate, or deferred follow-up.

13. **Reflect after use**
   Repeated use should change the system. Observability and reflection turn agent behavior into maintainable capability.

## Synthesis Pattern

CyberAlchemy synthesis is not summarization. It is a transformation from scattered intent into a structured object that can survive handoff.

The synthesis pattern is:

```text
seed intent
  -> bounded context
  -> objective and output artifact
  -> research and discovery
  -> local vocabulary
  -> candidate structure
  -> tension and critique
  -> revised artifact
  -> validation evidence
  -> lifecycle route
```

A synthesis is successful when a future agent or human can understand:

- what was asked,
- what was produced,
- why this shape was chosen,
- what was rejected,
- what remains unresolved,
- where to start and how to continue,
- what should happen next.

## Agent Collaboration Model

The method treats agents as role-bearing collaborators.

| Role | Responsibility |
| --- | --- |
| Human | Provides intent, taste, constraints, approval, and blocker decisions. |
| Primary agent | Owns the run, integrates evidence, edits artifacts, and preserves the final account. |
| Researcher | Finds source evidence, outside patterns, missing context, and alternative frames. |
| Proposer | Builds candidate structures, options, reductions, or plans. |
| Balancer | Challenges scope, closure, hidden complexity, brittle minimalism, and unsupported assumptions. |
| Observer | Records telemetry and detects when reflection is needed. |
| Lifecycle authority | Owns promotion, validation, implementation, or maintenance for the target artifact. |

Subagents are useful when their work is bounded, parallel, and traceable. They should not replace the primary agent's responsibility for integration.

## Governing Principles

### Intent Before Machinery

Do not build systems before the intent is clear enough to carry through a lifecycle artifact.

### Discovery Feeds Synthesis

Do not only rearrange the context already in front of the agent. Research, inspect, compare, and interview until the current synthesis is fed by enough discovered evidence to stand on its own.

### Objective And Artifact Guide The Work

Keep two guiding references visible: the objective being solved and the output artifact or final product the work is currently trying to produce. Seeing the intended result helps the agent and user understand what discovery must find, what structure must be designed, and what middle steps matter.

The target artifact is not immutable. It is a working orientation point that should be revised when research, tension, or implementation reveals that another output shape would solve the objective more responsibly.

### Artifact Over Vibes

A good run leaves something reviewable behind: a spec, design, glossary, decision record, technique contract, validation result, or transport note.

### Ergonomics Is Governance

The work should be easy for humans and agents to understand, navigate, resume, and act on. Clarity is not decoration; it is how the system avoids misuse, duplicated reasoning, hidden state, and stalled handoffs.

### Smallest Coherent Unit

Find the smallest unit that still has meaning, responsibility, inputs, outputs, and recomposition in the current context.

### Open-Ended, Not Overbuilt

Avoid premature complexity, but do not create brittle minimalism. Ask what kind of evolution the artifact is likely to face, then preserve the smallest useful extension boundary.

### Tension Is Productive

Critique is not failure. Tension reveals where the structure needs sharpening, routing, or a human decision.

### Traceability Is Memory

The system should remember why a choice was made. Decisions without trace become future ambiguity.

### Local Vocabulary First

Create scoped language before promoting global definitions. Candidate terms should remain local until evidence and governance justify promotion.

### Lifecycle Ownership Matters

Invoke can prepare a handoff, but sigil-development owns sigil lifecycle. Spellcraft owns spell lifecycle. Task-session owns bounded execution. Routing preserves authority.

### Reflection Closes The Loop

A capability is not finished when the first artifact lands. It matures through observation, repeated use, reflection, and targeted iteration.

## Working With Complexity

CyberAlchemy handles complexity by separating four questions:

| Question | Purpose |
| --- | --- |
| What is the smallest coherent unit? | Prevents overlarge first designs. |
| How does it recompose upward? | Prevents meaningless fragmentation. |
| What evolution pressure is real? | Prevents brittle minimalism. |
| What should remain deferred? | Prevents premature optimization. |

Complexity is justified only when it answers a named tension in the current or clearly emerging context.

## Method Primitives

Method primitives are more general than techniques. A technique answers "what instrument should the agent apply in this phase?" A primitive answers "how should agent work be governed so artifacts, roles, gates, and lifecycle routes stay coherent?"

Use primitives when designing sigils, composing spells, defining agents, or turning a repeated working habit into a reusable method.

### Method Vocabulary

Use these distinctions when extending the method.

| Concept | Meaning |
| --- | --- |
| Principle | A value or constraint that explains why the method behaves this way. |
| Primitive | A reusable governing rule that shapes agent work across many phases. |
| Technique | A named instrument applied in a specific phase or trigger condition. |
| Mode | A configured run profile: budget, depth, roles, rounds, gates, and closeout behavior. |
| Artifact | The durable thing produced or updated by the work. |
| Trace | The remembered path: evidence, decisions, rejected alternatives, gaps, and next route. |

### Discovery Primitives

| Primitive | Purpose | Rule |
| --- | --- | --- |
| Research Before Closure | Prevent premature synthesis from hardening into a false artifact. | Close only after the agent has searched for missing evidence, alternative frames, comparable patterns, and contradiction sources appropriate to the task. |
| Cheap Evidence Baseline | Learn enough before asking or designing. | Inspect obvious local sources first, then ask focused questions only for what evidence cannot answer. |
| Source Horizon Expansion | Keep the method intellectually alive. | When the problem calls for it, look beyond software and local precedent into other domains, literature, operations, design, research practice, governance, or systems theory. |
| Unknowns Registry | Make ignorance workable. | Record blockers, non-blocker unknowns, assumptions, and discovery leads instead of hiding them inside confident prose. |

### Governance Primitives

| Primitive | Purpose | Rule |
| --- | --- | --- |
| Route Before Work | Choose the correct lifecycle authority before producing output. | Natural-language intent should resolve to the smallest responsible route: define, design, plan, validate, interrogate, implement, reflect, or defer. |
| Authority-Bound Composition | Compose capabilities without rewriting their contracts. | A spell, bridge, or orchestrator may sequence another capability, but contract changes route back to that capability's owner. |
| Gate Before Mutation | Protect consequential changes from unresolved ambiguity. | If a decision, planner, readiness, or evidence gate blocks, mutation stops until the blocker is resolved or explicitly overridden. |
| Pass/Flag/Block Verdict | Replace vague confidence with operational state. | Every review or gate should return whether work may proceed, may proceed with named risk, or must stop. |

### Synthesis Primitives

| Primitive | Purpose | Rule |
| --- | --- | --- |
| Objective-Artifact Pair | Keep purpose and product visible together. | State both the objective and expected output form before deep work begins, then revise the pair when discovery changes the responsible shape of the result. |
| Artifact As State | Make progress durable outside the conversation. | A run should leave a handoff, glossary, work-pack, decision record, trace, report, or another reviewable artifact. |
| Navigable Work Surface | Help humans and agents orient quickly. | Artifacts should expose clear entrypoints, headings, links, status, unresolved gaps, and next actions. |
| Obligation-Linked Context | Keep context small and load-bearing. | Include evidence because it closes a named obligation, not because it is generally interesting. |
| Tension Over Summary | Make multi-agent work produce insight instead of parallel notes. | Synthesis should surface contradictions, unsupported assumptions, and cross-layer tension before it summarizes. |
| Trace Before Promotion | Prevent local guesses from becoming global truth. | Terms, claims, conventions, and confidence states promote only when evidence and governance justify it. |
| Boundary Extraction Before Conversion | Avoid importing tangled workflows as oversized sigils. | When translating an external skill or workflow, first identify one coherent reusable capability and its exclusions. |

### Agent Collaboration Primitives

| Primitive | Purpose | Rule |
| --- | --- | --- |
| Role-Separated Agent Work | Keep delegation useful and accountable. | The primary agent integrates; proposer, balancer, mapper, verifier, and observer roles produce bounded evidence or critique. |
| One Question At A Time | Resolve ambiguity without flooding the user. | Ask the highest-discrimination question, update the artifact when the answer changes it, then continue only if another blocker remains. |
| Human Gate | Preserve user authority over consequential judgment. | Agents may prepare options and trade-offs, but blocker decisions, scope approval, and contract changes require human validation. |
| Delegation Health | Treat subagent execution as a governed stage. | Long-running delegated work needs a stage id, terminal outcome, evidence, retry policy, and stuck-state handling. |

### Evolution Primitives

| Primitive | Purpose | Rule |
| --- | --- | --- |
| Layered Proof Progression | Grow capability through evidence instead of ambition. | Start with the minimum working unit, then add bounded layers only when each layer unlocks a distinct decision. |
| Closure Seeding | Plan validation before the work expands. | Medium or high-risk work should seed verification, alignment, and closure tasks early, not after implementation drifts. |
| Reflection Outer Loop | Let repeated use improve the system. | Usage signals, threshold triggers, user corrections, and output drift should produce evidence-backed improvement proposals. |
| Local Adaptation Boundary | Preserve reusable contracts while allowing repository fit. | Local paths, aliases, thresholds, and gate strictness can adapt; upstream capability behavior should not silently fork. |

## Navigation Contract

A CyberAlchemy artifact should be navigable before it is considered complete. A future human or agent should be able to resume from the artifact without reconstructing the whole conversation.

At minimum, a navigable artifact should show:

- what the artifact is for,
- what objective it serves,
- what output shape it represents,
- where to start reading or acting,
- what is current versus historical,
- what is decided versus unresolved,
- what evidence or links matter,
- what changed in this pass,
- who or what owns the next step.

Dense detail is acceptable only when the artifact also provides a clear entrypoint and a short path to action.

## Technique Packs

Techniques are named instruments that agents use during synthesis. They are not ad hoc advice and not necessarily optional addons.

A technique should define:

- stable id,
- phase,
- trigger,
- allowed inputs,
- emitted trace,
- pass, flag, and block conditions,
- failure behavior,
- anti-patterns.

The Distill technique pack is an example of this method: recomposition proof, evolution profile, cognitive load check, requisite variety check, boundary-object check, premortem pass, and set-based tournament are all techniques attached to phase hooks.

## Development Packet Pattern

When creating a new sigil or spell, prefer an artifact-local development packet.

Common packet artifacts:

| Artifact | Purpose |
| --- | --- |
| Handoff | Defines identity, purpose, IO, modes, runtime expectations, and next route. |
| Glossary | Stabilizes local vocabulary and prevents term drift. |
| Discovery map | Records unknowns, searched sources, evidence gaps, and discovery leads. |
| Research | Expands the technique horizon, compares outside practices, and records source influence. |
| Design | Defines architecture, interfaces, surfaces, risks, and dependency rules. |
| Technique specs | Breaks reusable methods into inspectable contracts. |
| Implementation layering | Stages candidate package, validation, runtime, and registry work. |
| Interrogation review | Tests whether more design is needed before promotion or execution. |
| Transport report | Preserves provenance, outputs, gaps, and route. |

This packet is not bureaucracy. It is how agent synthesis becomes reusable capability.

## Quality Bar

A CyberAlchemy run should:

- produce a reviewable artifact,
- preserve the user's intent,
- state the current objective and expected output artifact,
- identify what was discovered and what still needs research,
- identify the target lifecycle owner,
- make the artifact clear enough for a human or future agent to navigate,
- expose where to start, what changed, what remains unresolved, and what happens next,
- record local vocabulary when terms matter,
- distinguish blocker gaps from non-blocker gaps,
- avoid silent promotion,
- include validation or an explicit validation gap,
- preserve observability when available,
- recommend a concrete next route.

## Anti-Patterns

Avoid:

- turning every idea into immediate implementation,
- treating the available context as the whole world,
- closing a design before discovery has tested central assumptions,
- continuing work when the objective or expected artifact has drifted without renaming it,
- producing dense artifacts that are technically complete but hard to navigate,
- adding abstractions because they sound elegant,
- treating critique as a detour instead of part of synthesis,
- hiding uncertainty behind confident prose,
- creating global terminology from local guesses,
- letting subagents produce unintegrated parallel summaries,
- collapsing multiple lifecycle authorities into one oversized workflow,
- claiming a capability is ready before validation examples exist.

## Baseline Statement

The CyberAlchemy Method is:

```text
governed synthesis through artifacts,
guided by objective and output,
fed by research and discovery,
shaped by tension,
made navigable for humans and agents,
bounded by lifecycle ownership,
made durable through trace and observation.
```

Use it when designing new agent capabilities, revising existing sigils, composing spells, or turning a complex idea into a reusable method.
