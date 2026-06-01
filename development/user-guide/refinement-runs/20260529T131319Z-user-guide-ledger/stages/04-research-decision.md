# Stage 04: Research Decision

Status: `pass`

## Decision

Research mode: `bounded-research`

Reason: the operator explicitly asked to research techniques for helping the user understand and for improving the User ledger after Guide-assisted decisions or blocker resolutions.

## Bounded Research Summary

The useful techniques for this design are:

| Technique | Transfer Into User/Guide |
| --- | --- |
| Scaffolding and fading | Guide starts with support, diagnoses response, then reduces support as the user can explain or transfer the concept. |
| Analogical encoding | Guide compares multiple examples so the user extracts an abstract schema instead of memorizing one analogy. |
| Self-explanation | Guide asks the user to explain why an example works, which principle it instantiates, or what would break if conditions changed. |
| Retrieval practice | Guide treats "I understand" as a cue for a lightweight recall or teach-back before adding mastery. |
| Knowledge tracing / learner modeling | User ledger tracks concept-level mastery estimates or statuses over time, but as local learning state, not identity diagnosis. |
| Concept mapping / prerequisite mapping | Guide connects primitives such as schema, data, forms, APIs, constitutions, behavior, systems, and software architecture. |

## Research Anchors

- Scaffolding should be contingent and fade as learner responses improve: [Fading distributed scaffolds](https://pmc.ncbi.nlm.nih.gov/articles/PMC6519686/).
- Analogical encoding uses comparison across examples to support schema abstraction and transfer: [Learning and transfer: A general role for analogical encoding](https://loewenstein.web.illinois.edu/papers/Gentneretal%20JEP03.pdf).
- Self-explanation supports problem solving and conceptual understanding when learners actively connect actions to principles: [Self-explaining effect in general chemistry instruction](https://pubs.rsc.org/en/content/articlehtml/2014/rp/c3rp00172e).
- Knowledge tracing is a learner-modeling family used to estimate skill/mastery states over interactions: [An Introduction to Bayesian Knowledge Tracing with pyBKT](https://www.mdpi.com/2624-8611/5/3/50).

## Research Boundary

Do not import heavy adaptive-learning machinery into the first implementation. The first Arcanum-native shape should be a transparent ledger with simple statuses and receipts. Bayesian or statistical mastery estimation can be a later optional layer after evidence exists.
