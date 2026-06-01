# Stage 08: Distill Repair

Status: `pass`

## Repairs Applied

| Repair | Result |
| --- | --- |
| Reduce ledger scope | First schema should include only profile seed, domain anchors, vocabulary preferences, concept states, guide receipts, bridge patterns, glossary entries, residue, and consent visibility. |
| Rename attempt semantics | Use `clarification_turns` and define it as interaction friction, never user ability. |
| Add mastery evidence rule | Mastered glossary entries require active evidence, not passive agreement. |
| Add bridge guardrail | Every analogy records what maps, what breaks, and the target-domain definition. |
| Add skip/replay install path | Install game is optional and replayable. |
| Keep libraries candidate-only | Software primitives are a seed library, not the universal Guide ontology. |

## Repaired Unit

The selected unit becomes:

```text
User Learning Ledger Contract v0
  + Guide Interaction Receipt v0
  + Mastery Evidence Rule
  + Bridge Mapping Guardrail
```

## Validation Expectations

First implementation should validate with fixtures:

1. Sales terms explain software architecture decision.
2. Software engineering terms explain a scientific formula.
3. Music terms explain a civil construction plan.
4. User says "I understand" without teach-back: concept becomes `clarified`, not `mastered`.
5. User gives teach-back and transfer: concept can become `mastered`.
6. User dislikes an analogy: record residue and avoid similar strategy until reviewed.

## Residue

- Exact persistence format is unresolved: YAML, JSONL, Markdown, or hybrid.
- Whether `User` is an `arcana` sigil family or a framework service is unresolved.
- Whether `Guide` is one spell, a spell family, or a mode overlay across several spells is unresolved.
- UI/HTML for the install game is a later task.
