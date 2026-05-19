# Concept Layer Optimizer Literature Research

Research date: 2026-05-19

## Research Question

What does cross-domain literature say about the kind of work Concept Layer Optimizer is trying to do: recursively decomposing a broad seed into coherent concept layers, selecting the smallest useful unit for the current context, preserving recomposition, avoiding premature complexity, and remaining open-ended when natural evolution pressure exists?

## Executive Synthesis

Concept Layer Optimizer is not just a decomposition tool. The closest literature cluster treats this as a controlled movement between four pressures:

- **Decomposition:** make the problem smaller enough to reason about.
- **Recomposition:** prove that smaller concepts can add back into a meaningful whole.
- **Cognitive economy:** keep the working frame small enough for judgment.
- **Evolvability:** leave the right seams for expected future change without building speculative machinery.

Across systems engineering, design theory, cognition, organizational learning, product development, biology, and AI planning, the same pattern appears: the best unit is rarely the smallest named fragment. It is the smallest unit that still has responsibility, boundary, interface, evidence, and a plausible future-change story.

## Research Claims

### 1. Decomposition must preserve recomposition.

Herbert Simon's work on complex systems argues that many stable complex systems are hierarchical or nearly decomposable: subsystems can be reasoned about locally while still participating in a larger whole. This supports the sigil's closure test, but it also warns against arbitrary fragmentation. A unit is useful when its internal relations are stronger than its external relations and when its interface back to the whole remains understandable.

NASA systems engineering guidance similarly treats architecture work as a movement between functions, requirements, interfaces, and verification, not as a simple splitting exercise. A decomposed part must still trace to higher-level purpose and later verification.

Technique implication:

- Add a **recomposition proof** to every reduction round: "How does this concept combine upward, and what would fail if it could not?"
- Treat unowned glue as evidence that the reduction is not closed.

Sources:

- Herbert A. Simon, "The Architecture of Complexity": https://comdig.unam.mx/2022/05/10/classics-the-architecture-of-complexity-1962/
- NASA Systems Engineering Handbook: https://www.nasa.gov/reference/systems-engineering-handbook/

### 2. The right unit is bounded by cognitive load as much as structure.

Cognitive load theory and chunking research both imply that planning quality degrades when a unit forces too many unrelated details into active attention. But chunking also means a larger unit can be easier than many small ones when it forms a meaningful pattern.

This is important for Concept Layer Optimizer: "smaller" is not always simpler. A concept split that creates five tiny fragments can increase cognitive load if the user must now remember all their coupling rules.

Technique implication:

- Add a **cognitive load check**: "Did this split reduce what the user must hold in mind, or did it create more coordination burden?"
- Prefer meaningful chunks over maximally granular fragments.

Sources:

- John Sweller, "Cognitive Load During Problem Solving": https://www.sciencedirect.com/science/article/pii/0364021388900237
- George A. Miller, "The Magical Number Seven, Plus or Minus Two": https://psychclassics.yorku.ca/Miller/

### 3. Design work alternates divergence and convergence.

The Design Council's Double Diamond describes design as alternating divergent exploration and convergent definition. Set-based concurrent engineering makes a similar move in product development: keep multiple feasible options alive long enough to learn, then narrow based on evidence.

This maps cleanly to the sigil's Tournament mode. Multiple proposals should not exist as decorative alternatives; they should expose different assumptions and eliminate weak options through evidence.

Technique implication:

- Make **proposal tracks** explicitly set-based: each track should state its assumption, preserved option value, and elimination condition.
- Add a **convergence gate** before final selection: "What evidence or constraint justifies collapsing to this option now?"

Sources:

- Design Council, Framework for Innovation / Double Diamond: https://www.designcouncil.org.uk/our-resources/framework-for-innovation/
- SBCE overview from product development literature: https://leaninstitute.org/explore-lean/what-is-lean/what-is-set-based-concurrent-engineering/

### 4. Wicked problems need provisional closure, not false finality.

Rittel and Webber's wicked-problem framing warns that some planning problems do not have a final problem statement or final solution. The act of framing the problem changes the candidate solution space.

For this sigil, that means "closed system" must be local and contextual, not metaphysical. A concept can be closed for the current target context while still open to later reframing.

Technique implication:

- Rename mental model from "final smallest unit" to **current smallest coherent unit**.
- Add a **frame-expiry note**: what context change would invalidate this optimization point?

Sources:

- Rittel and Webber, "Dilemmas in a General Theory of Planning": https://doi.org/10.1007/BF01405730
- Buchanan, "Wicked Problems in Design Thinking": https://web.mit.edu/jrankin/www/engin_as_lib_art/Design_thinking.pdf

### 5. Evolvability is a real design requirement when future variation is concrete.

Modularity and evolvability literature, including biological and product-design work, says systems evolve better when variation can occur locally without forcing the whole system to change. This supports the user's addition: avoiding premature complexity should not make the design brittle.

But the literature also distinguishes real option value from speculative generality. Modularity has a cost. It is justified when the expected evolution pattern is concrete enough to name.

Technique implication:

- Add an **evolution profile** before deferring future scale.
- Classify evolution pressure by type: variants, actors, volume, policy rules, integrations, migration, governance, environmental change, learning uncertainty.
- Use the smallest extension boundary that protects the likely change.

Sources:

- Baldwin and Clark, "Design Rules: The Power of Modularity": https://mitpress.mit.edu/9780262528762/design-rules-volume-1/
- Kirschner and Gerhart, evolvability and facilitated variation: https://www.pnas.org/doi/10.1073/pnas.0505957102

### 6. Requisite variety explains when complexity is necessary.

Ashby's law of requisite variety says a controller needs enough variety to handle the variety in the system it regulates. Translated for this sigil: a design should not be more complex than its environment requires, but it also should not be simpler than the variation it must absorb.

This gives the Balancer a stronger rule than "avoid complexity." The better question is: "What external variety must this unit handle, and is the unit's internal variety enough?"

Technique implication:

- Add a **requisite-variety check**:
  - External variety: what variation will hit the unit?
  - Internal variety: what knobs, states, policies, or extension points can handle it?
  - Mismatch: underfit, overfit, or fit.

Sources:

- Ross Ashby and cybernetics overview: https://en.wikipedia.org/wiki/Variety_(cybernetics)
- Principia Cybernetica summary of requisite variety: http://pespmc1.vub.ac.be/REQVAR.html

### 7. Boundaries are social artifacts, not only technical ones.

Boundary-object literature argues that shared artifacts can be robust enough to coordinate across groups while remaining flexible enough for local use. Organizational "loose coupling" literature makes a related point: parts can maintain local autonomy while still belonging to a coherent system.

This matters because Concept Layer Optimizer may be used for plans, institutions, workflows, organizations, or design systems. A good concept unit may be one that different stakeholders can use without forcing them into the same internal model.

Technique implication:

- Add a **boundary-object check** for multi-actor contexts:
  - Who needs to use this concept?
  - What must remain stable across users?
  - What can vary locally?

Sources:

- Star and Griesemer, "Institutional Ecology, Translations and Boundary Objects": https://journals.sagepub.com/doi/10.1177/030631289019003001
- Karl Weick, loosely coupled systems: https://journals.sagepub.com/doi/10.2307/2391875

### 8. Dialectical roles help, but only with stopping rules.

The Proposer/Balancer structure resembles dialectical inquiry, devil's advocacy, red teaming, premortems, Delphi-style iteration, and AI self-critique. These techniques improve plans by separating generation from criticism, but they can also cycle forever unless the process defines convergence criteria.

Gary Klein's premortem is especially useful here because it makes the Balancer concrete: instead of objecting abstractly, it imagines why the selected unit failed.

Technique implication:

- Add a **premortem pass** after selecting the current smallest coherent unit.
- Add a **stable-disagreement stop rule**: if roles repeat the same tension without new evidence, preserve the tension and route to decision-gate or robot-talks.

Sources:

- Gary Klein, "Performing a Project Premortem": https://hbr.org/2007/09/performing-a-project-premortem
- RAND Delphi method overview: https://www.rand.org/topics/delphi-method.html
- CIA structured analytic techniques and red team style challenge practices: https://www.cia.gov/resources/csi/static/9cdebf4d1781a00aae7a8fbd17c15a60/Tradecraft-Primer-apr09.pdf

### 9. Design theory treats concepts and knowledge as co-evolving.

C-K design theory distinguishes the concept space, where propositions are not yet fully decidable, from the knowledge space, where claims are supported. Design advances by expanding both. This is very close to what the sigil is doing when it recursively opens smaller concepts while checking whether they are grounded enough to close.

Technique implication:

- Track whether a unit is a **concept claim** or a **knowledge-backed unit**.
- Do not force closure when the run is actually revealing missing knowledge.

Sources:

- C-K theory overview: https://www.ck-theory.org/la-theorie-ck/

### 10. Abstraction hierarchy helps preserve multiple levels at once.

Work-domain analysis and abstraction hierarchy methods model systems across levels such as purpose, values, functions, processes, and physical forms. This is useful because Concept Layer Optimizer should not flatten everything into a single decomposition tree.

Sometimes the smallest useful unit at the purpose level is different from the smallest useful unit at the process or implementation level.

Technique implication:

- Add a **level-of-abstraction label** to each concept layer:
  - purpose
  - value/constraint
  - function
  - process
  - interface
  - artifact
  - operation
- Prevent cross-level mistakes, such as treating a value as a component or a workflow as a policy.

Sources:

- Rasmussen abstraction hierarchy and work-domain analysis overview: https://www.researchgate.net/publication/220663880_The_role_of_hierarchical_knowledge_representation_in_decisionmaking_and_system_management

### 11. AI planning literature supports generate-critique-refine, but warns against ungrounded self-confirmation.

Recent language-model planning patterns such as Tree of Thoughts, Self-Refine, Constitutional AI, and multi-agent debate all resemble the sigil's proposer/balancer loop. They show the value of explicit intermediate reasoning states, critique, and selection among candidates.

The warning is that critique without external grounding can become performative. The Balancer should cite evidence, constraints, closure failures, or named tensions, not merely sound skeptical.

Technique implication:

- Require Balancer objections to name one of:
  - lost recomposition
  - missing input/output
  - unconfirmed evolution profile
  - excessive coordination cost
  - unsupported assumption
  - unhandled external variety
  - validation burden

Sources:

- Tree of Thoughts: https://arxiv.org/abs/2305.10601
- Self-Refine: https://arxiv.org/abs/2303.17651
- Constitutional AI: https://arxiv.org/abs/2212.08073
- Multi-agent debate: https://arxiv.org/abs/2305.14325

## Technique Horizon For The Sigil

### Evolution Profile Prompt

Ask before deferring future scale:

```text
What kind of evolution is this system likely to have?

- variants
- new actors
- volume or performance growth
- new integrations
- policy/rule growth
- migration or replacement pressure
- governance/review pressure
- learning uncertainty
- none known yet
```

Then classify:

- **Concrete evolution:** preserve the smallest extension boundary.
- **Likely but vague evolution:** name the boundary, defer the mechanism.
- **Unknown evolution:** keep the unit simple and record what would trigger revision.

### Closure-Recomposition Ladder

For each proposed unit:

1. Responsibility: what does it own?
2. Boundary: what is inside and outside?
3. Inputs: what does it need?
4. Outputs: what does it produce?
5. Recomposition: how does it combine upward?
6. Evolution: what change can it absorb?
7. Failure: what breaks if this split is wrong?

### Requisite Variety Check

Use this when the Balancer suspects overbuilding or underbuilding:

| Check | Question |
| --- | --- |
| External variety | What variation will hit this unit? |
| Internal variety | What mechanisms can respond to that variation? |
| Fit | Is the unit underfit, overfit, or proportionate? |
| Smallest adjustment | What is the least complexity needed to reach fit? |

### Set-Based Tournament

Tournament mode should preserve several proposal tracks long enough to learn, then narrow by explicit criteria:

- context fit
- closure
- recomposition
- evolution fit
- cognitive load
- validation cost
- risk of brittle minimalism
- risk of premature generality

### Premortem Pass

After choosing an optimization point, ask:

```text
Six months later, this optimization point failed. What was the most likely reason?
```

Then classify the answer:

- too small to absorb expected evolution
- too broad to validate
- wrong abstraction level
- hidden coupling
- missing stakeholder boundary
- future scale assumed but not real
- no recomposition path

### Abstraction-Level Guard

Require each concept layer to declare its abstraction level. This prevents bad reductions like splitting a purpose into components or treating a policy as an implementation unit.

Suggested labels:

- purpose
- value/constraint
- capability
- function
- workflow/process
- policy/rule
- interface
- artifact
- operation

### Boundary-Object Check

Use when multiple groups or roles must share a concept:

```text
What must this concept mean identically for everyone, and what can each role interpret locally?
```

This is especially useful for plans, governance models, architecture diagrams, roadmaps, and organizational workflows.

## Candidate Additions To SIGIL-HANDOFF.md

These are not applied automatically. They are research-backed options for the next design revision.

1. Add "evolution profile" as a required sub-check in the Complexity Balance Rule.
2. Add a "recomposition proof" field to reduction rounds.
3. Add a "cognitive load changed?" check to every accepted split.
4. Add "requisite variety" as a Balancer objection category.
5. Add "premortem pass" before final output.
6. Add abstraction-level labels to concept layers.
7. Add a boundary-object check for multi-actor contexts.
8. Strengthen Tournament mode into set-based exploration with explicit elimination criteria.
9. Add concept-vs-knowledge status for uncertain units.
10. Add frame-expiry notes to the final optimization point.

## Bibliography

- Ashby, W. Ross. Requisite variety summaries: http://pespmc1.vub.ac.be/REQVAR.html
- Baldwin, Carliss Y. and Clark, Kim B. "Design Rules: The Power of Modularity": https://mitpress.mit.edu/9780262528762/design-rules-volume-1/
- CIA Center for the Study of Intelligence. "A Tradecraft Primer: Structured Analytic Techniques": https://www.cia.gov/resources/csi/static/9cdebf4d1781a00aae7a8fbd17c15a60/Tradecraft-Primer-apr09.pdf
- C-K Theory: https://www.ck-theory.org/la-theorie-ck/
- Design Council. "Framework for Innovation": https://www.designcouncil.org.uk/our-resources/framework-for-innovation/
- Kirschner, Marc and Gerhart, John. Facilitated variation / evolvability: https://www.pnas.org/doi/10.1073/pnas.0505957102
- Klein, Gary. "Performing a Project Premortem": https://hbr.org/2007/09/performing-a-project-premortem
- Lean Enterprise Institute. Set-Based Concurrent Engineering overview: https://leaninstitute.org/explore-lean/what-is-lean/what-is-set-based-concurrent-engineering/
- Miller, George A. "The Magical Number Seven, Plus or Minus Two": https://psychclassics.yorku.ca/Miller/
- NASA. Systems Engineering Handbook: https://www.nasa.gov/reference/systems-engineering-handbook/
- RAND. Delphi Method: https://www.rand.org/topics/delphi-method.html
- Rasmussen, Jens. Abstraction hierarchy and decision making: https://www.researchgate.net/publication/220663880_The_role_of_hierarchical_knowledge_representation_in_decisionmaking_and_system_management
- Rittel, Horst W. J. and Webber, Melvin M. "Dilemmas in a General Theory of Planning": https://doi.org/10.1007/BF01405730
- Buchanan, Richard. "Wicked Problems in Design Thinking": https://web.mit.edu/jrankin/www/engin_as_lib_art/Design_thinking.pdf
- Madaan et al. "Self-Refine: Iterative Refinement with Self-Feedback": https://arxiv.org/abs/2303.17651
- Simon, Herbert A. "The Architecture of Complexity": https://comdig.unam.mx/2022/05/10/classics-the-architecture-of-complexity-1962/
- Star, Susan Leigh and Griesemer, James R. Boundary objects: https://journals.sagepub.com/doi/10.1177/030631289019003001
- Sweller, John. "Cognitive Load During Problem Solving": https://www.sciencedirect.com/science/article/pii/0364021388900237
- Tree of Thoughts: https://arxiv.org/abs/2305.10601
- Weick, Karl E. "Educational Organizations as Loosely Coupled Systems": https://journals.sagepub.com/doi/10.2307/2391875
- Multi-agent debate: https://arxiv.org/abs/2305.14325
- Constitutional AI: https://arxiv.org/abs/2212.08073
