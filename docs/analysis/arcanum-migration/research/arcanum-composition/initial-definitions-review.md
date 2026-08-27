# Review — Arcanum Composition Research Initial Definitions

This is the review that previously lived at
`docs/analysis/arcanum-migration/review.md`. It is preserved here because its
target was the research initial-definitions artifact, not the later migration
map and Craft write-back claims.

## Coverage

| attacker | lens | targets checked | findings raised | zero-findings defense |
| --- | --- | --- | --- | --- |
| `initial-definitions-review` | fidelity and governance | `research-initial-definitions.md`; local and `domainspec-lean-formalization` initial-definition skills; `domainspec` research coverage contract | 5 provisional; 3 survived independent verification | n/a |
| parent | mechanics, evidence-boundary completeness, and question-to-gap coverage | complete target; governing question rules; cited Arcanum capability contracts | 1 independent finding; verified 3 attacker findings; refuted 2 | The cited baseline claims about Craft, Invoke, Task Session, Decision Gate, and Goal were checked without finding a contradictory owner or handoff contract. |
| `initial-definitions-review` as verifier | attempted refutation of the parent's independent finding only | target Context and both initial-definition skills | 1 verified | n/a |

## Findings

| # | artifact and locator | evidence | severity | consequence | proposed fix |
| --- | --- | --- | --- | --- | --- |
| 1 | `research-initial-definitions.md:13-17` | The target first says that the relations `are not yet established`, then warns against turning `a transverse state mechanism into a linear phase`. The governing initial-definition skill forbids candidate answers, vocabulary, and initial hypotheses. | MAJOR | The Context supplies a partial answer about the shape of the composition before the relevant questions are investigated. | Replace the phrase with a neutral risk statement that does not classify the relation in advance. |
| 2 | `research-initial-definitions.md:51-53,71-73,82-84` | Several research questions combine obligations whose answers can differ or depend on different evidence or authority. | MAJOR | Partial answers would remain hidden inside an unresolved compound question. | Split only the independently answerable obligations while preserving stable IDs. |
| 3 | `research-initial-definitions.md:92-97` | The question asks which ownership boundaries `should remain`, introducing a normative architecture decision into informational research. | MAJOR | The research baseline assumes authority that belongs to later analysis or design. | Ask descriptively which separations are deliberate and what documented effects they have. |
| 4 | `research-initial-definitions.md:154-157` | A material gap in the meanings of communication and composition had no registered research question. | MAJOR | Research could close while leaving its load-bearing terms undefined. | Add a neutral question for the operational meanings and evidence boundaries of communication and composition. |

## Artifact verdicts

| artifact | KEEP or FIX | rationale |
| --- | --- | --- |
| `research-initial-definitions.md` | FIX | Four MAJOR findings survived verification. |

## Change requests

1. Remove the premature `transverse` classification.
2. Register a neutral question for communication and composition.
3. Split independently answerable clauses in the compound questions.
4. Defer normative ownership decisions to later analysis or design.

## Evidence boundary

The review checked the complete initial-definitions artifact and its governing
question rules. It did not review `analysis.md`, execute runtime integrations,
or decide the eventual architecture.
