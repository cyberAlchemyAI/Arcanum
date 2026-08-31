# Vocabulary Map: Source Terms To Module Formulae Terms

This map keeps semantics stable while reducing framework-specific wording.

## Core Terms

| Source Term | Module Formulae Term | Preserved Meaning |
| --- | --- | --- |
| Feature | Module | Scoped capability boundary with clear ownership. |
| Feature Spec | Module Spec | Canonical contract for behavior and boundaries. |
| Domain Concepts | Concept Model | Structural definitions and constraints. |
| Concept Registry | Concept Index | Canonical identifiers for all concepts. |
| Feature Concept Graph | Relationship Map | Typed links with evidence traceability. |
| Aspect Docs | Supporting Contracts | Decomposed contracts by concern. |
| Operations | Actions | State-changing behavior contract. |
| Queries | Read Views | Read-model contract without mutation. |
| Workflows | Flows | Multi-step orchestration and decision points. |
| Rules | Constraints | Hard behavior conditions that must hold. |
| Work-Pack | Execution Pack | Planned waves, tasks, gates, and closure strategy. |
| Acceptance Criteria | Completion Criteria | Conditions required to close work. |

## Governance Terms

| Source Term | Module Formulae Term | Preserved Meaning |
| --- | --- | --- |
| Alignment Audit | Contract Alignment Audit | Check behavior matches documented contracts. |
| Layering Audit | Boundary Layering Audit | Check dependency and boundary direction. |
| Registry Sync | Concept Index Sync | Synchronize global concept naming references. |
| Readiness Gate | Readiness Review | Decide pilot/release/production fit with evidence. |

## Language Guardrails

1. Keep semantic load-bearing words: approval, gate, blocker, traceability, evidence, transport.
2. Avoid framework-exclusive terms unless a downstream tool explicitly requires them.
3. Prefer plain-language action words over taxonomy labels.
4. Keep relationship labels typed and deterministic.
5. Keep glossary as the terminology authority for all artifacts.
