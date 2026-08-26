# Review — Arcanum Composition Research Initial Definitions

## Coverage

| attacker | lens | targets checked | findings raised | zero-findings defense |
| --- | --- | --- | --- | --- |
| `initial-definitions-review` | fidelity and governance | `research-initial-definitions.md`; local and `domainspec-lean-formalization` initial-definition skills; `domainspec` research coverage contract | 5 provisional; 3 survived independent verification | n/a |
| parent | mechanics, evidence-boundary completeness, and question-to-gap coverage | complete target; governing question rules; cited Arcanum capability contracts | 1 independent finding; verified 3 attacker findings; refuted 2 | The cited baseline claims about Craft, Invoke, Task Session, Decision Gate, and Goal were checked without finding a contradictory owner or handoff contract. |
| `initial-definitions-review` as verifier | attempted refutation of the parent's independent finding only | target Context and both initial-definition skills | 1 verified | n/a |

## Findings

| # | artifact and locator | evidence | severity | consequence | proposed fix |
| --- | --- | --- | --- | --- | --- |
| 1 | `research/arcanum-composition/research-initial-definitions.md:13-17` | The target first says that the relations `are not yet established`, then warns against turning `a transverse state mechanism into a linear phase`. The governing `domainspec-lean-formalization` skill forbids candidate answers, vocabulary, and initial hypotheses at lines 89-92. | MAJOR | The Context supplies a partial answer about the shape of the composition before RQ-0 and RQ-4 are investigated, biasing later work toward treating transversal state as established. | Replace the phrase with a neutral risk statement that does not classify the relation in advance, such as `may mischaracterize the role of state as a phase`. |
| 2 | `research/arcanum-composition/research-initial-definitions.md:51-53,71-73,82-84` | RQ-2 combines relation endpoints, transferred content, detection, invocation, context supply, and result application; RQ-4 combines several separately governed state relations and their transition owners; RQ-5 combines evidential status with authority reconciliation. The governing skill requires clauses whose answers can differ or depend on different evidence or authority to be split (lines 45-48). The later coverage contract permits `answered` only when evidence resolves the entire RQ (`domainspec/.claude/skills/research/SKILL.md:154-159`). | MAJOR | A supported answer to one clause and an unresolved answer to another would force the whole RQ to remain unresolved, obscuring valid partial conclusions and making later per-RQ coverage imprecise. | Split only the independently answerable obligations: relation identity/transfer from orchestration responsibility; Craft–Decision Gate binding from other state write-back relations; and evidence classification from source-authority conflict. Preserve stable IDs and do not expand these into every possible diagnostic. |
| 3 | `research/arcanum-composition/research-initial-definitions.md:92-97` | RQ-6 asks which ownership boundaries `should remain`. The governing skill excludes proposed solutions and keeps initial definitions informational rather than decisional (`domainspec-lean-formalization/.../SKILL.md:89-100`). | MAJOR | The research baseline takes authority for a normative architecture decision that should instead be informed by findings and made in the later analysis or design decision. | Ask descriptively which separations are deliberate under current authority and what documented effects they have. Reserve whether they should remain for the later analysis. |
| 4 | `research/arcanum-composition/research-initial-definitions.md:154-157` | Known Gaps states that no shared definition of capability communication or composition has been identified, but no registered RQ asks which definitions are supported or authoritative. RQ-0 uses `composition`, while RQ-2 asks about instances of relations. The governing skill requires every material gap affecting the purpose to be covered by a research question (lines 83-85). | MAJOR | The research could answer every registered RQ while leaving the load-bearing meaning of `communication` and `composition` undefined, reproducing the ambiguity the analysis is supposed to resolve. | Add one stable, neutral RQ asking which operational definitions of capability communication and composition are supported for this analysis and what boundaries each definition has. |

## Artifact verdicts

| artifact | KEEP or FIX | rationale |
| --- | --- | --- |
| `research/arcanum-composition/research-initial-definitions.md` | FIX | Four MAJOR findings survive: one premature classification, non-atomic evidence obligations, one normative decision embedded in research scope, and one material gap without a registered RQ. |

## Change requests

1. Remove the premature `transverse` classification from Context while preserving the risk of falsely presenting a relationship as a linear phase.
2. Register an explicit, neutral question for the operational meaning and evidential boundary of capability communication and composition.
3. Split the independently answerable clauses in RQ-2, RQ-4, and RQ-5, keeping inseparable contrasts together and avoiding diagnostic proliferation.
4. Reframe RQ-6 as a descriptive question about deliberate ownership boundaries and their documented effects; defer `should remain` to the later analysis or design decision.

## Evidence boundary

The review checked the complete initial-definitions artifact against the local Arcanum skill, the more specific `domainspec-lean-formalization` initial-definition skill selected by the user, and the `domainspec` per-RQ findings-coverage rule. It also checked the named Craft, Invoke, Task Session, Decision Gate, and Goal contracts for contradictions in the current evidence baseline. It did not execute runtime integrations, conduct the registered research, review `analysis.md`, or decide the eventual architecture. The target artifact was not modified during this review.
