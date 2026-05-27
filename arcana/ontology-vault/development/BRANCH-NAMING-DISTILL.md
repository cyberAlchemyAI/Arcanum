# Distill Result: Branch Naming For Meaning Layer

## Target Context

The current branch-aware ontology candidate uses `proposition` as the global name for the branch that existing Ontology Vault material often calls `business`.

The user flagged that `proposition` may not be the best naming. This distillation tests the smallest coherent naming correction that preserves the branch-context discriminator and still works across Arcanum, CyberAlchemy, DomainSpec, and future systems.

## Objective And Output Artifact

Objective: choose or narrow the naming unit for the first branch in the candidate model.

Output artifact: a naming distillation note for later revision of `BRANCH-AWARE-ONTOLOGY-CANDIDATE.md`, not a canonical convention change.

## Mode And Budget

- Mode: Standard
- Proposal tracks: one role-simulated Proposer/Balancer track
- Recursive rounds: 2 / 2
- Verdict: flag

Flag reason: `meaning` is the strongest current replacement candidate, but this should still go through a decision gate before broad replacement because existing docs use `business` and the candidate currently uses `proposition`.

## Discovery Baseline

Observed evidence:

- The handoff described the first layer as "the proposition or meaning layer a system exists to satisfy."
- The branch-role distill described `business` as "proposition / meaning / method / type / problem frame."
- The candidate model replaced `business` with global `proposition`, preserving `business` as a local alias.
- The first branch needs to cover definitions, concepts, types, methods, policies, premises, outcomes, value measures, and problem frames.
- The model must apply beyond business software: Arcanum, CyberAlchemy, DomainSpec, research-flavored systems, and future systems.

Assumptions:

- The branch name should be short enough to use as a discriminator value.
- The name should not imply a commercial business domain.
- The name should not imply only one logical claim.
- The name should preserve the intent-to-implementation bridge with `system`.

Blocker unknowns:

- Whether the global branch name should optimize for precision, readability, or continuity with existing `business` branch material.
- Whether a two-word discriminator such as `meaning_intent` is acceptable in schemas and templates.

Non-blocker unknowns:

- Exact local aliases for future systems.
- Whether existing templates should be migrated later.

## Role Conversation Trace

### Round 1 Proposer Claim

Replace `proposition` with `intent`.

Evidence or assumption:

- The branch captures what the system exists to satisfy.
- `intent` pairs well with system realization and bridge traceability.
- "Intent-to-implementation" is a familiar formulation.

### Round 1 Balancer Objection

Category: meaning loss.

`intent` captures purpose and desired direction, but it weakens definitions, types, methods, and domain language. A glossary entry or type model is not always an intent, even though it belongs in this branch.

Reconciliation decision:

Revise. Keep `intent` as a key role or alias, but not the best global branch label.

### Round 2 Proposer Claim

Replace `proposition` with `meaning`.

Evidence or assumption:

- The branch is responsible for governed meaning: definitions, concepts, types, methods, policies, premises, outcomes, and problem frames.
- `meaning` is general enough for Arcanum's methods, CyberAlchemy's principles, DomainSpec's domain language, and future non-commercial systems.
- It avoids the logical narrowness of `proposition` and the commercial narrowness of `business`.

### Round 2 Balancer Objection

Category: underspecified boundary.

`meaning` can sound too broad. Almost everything in an ontology has meaning, including system and operational records. Without a decision rule, the branch could become a catch-all.

Reconciliation decision:

Accept with constraint. Use `meaning` only as a branch discriminator for the meaning the system exists to preserve, satisfy, or govern. Keep system machinery, situated operation, and cross-branch relations outside it.

Stable disagreement:

`meaning` is probably the best current name, but it needs a boundary phrase, not just a bare label.

## Current Smallest Coherent Unit

### Unit Name

`meaning` branch with an explicit boundary phrase.

### Responsibility

Classify claims that define the governed meaning a system exists to preserve, satisfy, interpret, or make actionable.

Suggested discriminator:

```yaml
branch_context:
  primary: meaning | system | operational | bridge
  local_alias: business | domain | intent | proposition | philosophy | null
```

Suggested branch question:

```text
meaning: What definition, concept, method, type, policy, value, rule, premise,
problem frame, or outcome gives the system its intended significance?
```

Boundary phrase:

```text
The meaning branch governs what the system means and what it is trying to make true,
not the machinery that realizes it, the situated context where it is used, or the
evidence relation between branches.
```

## Optimization Point

`meaning` is the best current optimization point because it is:

- smaller and clearer than a two-word compound such as `meaning-intent`,
- broader than `intent`,
- less commercial than `business`,
- less logic-bound than `proposition`,
- less implementation-adjacent than `domain`,
- less academic than `normative`,
- still able to recompose into bridge rules such as `meaning -> system realization`.

## Concept Layer Map

```text
Broad layer:
General branch-aware ontology model

Naming problem:
First branch currently named proposition

Candidate naming field:
business | domain | intent | meaning | normative | conceptual | proposition

Selected unit:
meaning branch with explicit boundary phrase

Deferred lower layers:
template migration, SKILL wording updates, schema-facing field rename, examples rewrite
```

## Technique Pack Trace

| Technique | Activation reason | Output | Decision |
| --- | --- | --- | --- |
| Abstraction-level guard | Naming could drift into full branch redesign. | Keep scope to first-branch name only. | pass |
| Recomposition proof | New name must still support system and bridge relations. | `meaning -> system -> operational`, connected by bridge. | pass |
| Evolution profile | Name must survive multiple systems and local aliases. | Global `meaning`, local aliases allowed. | pass |
| Frame-expiry note | Existing candidate is exploratory. | Expire after decision-gate or example validation. | pass |
| Navigable result check | User needs a next route. | Recommend candidate revision or decision gate. | pass |
| Boundary-object check | The branch name must be shared across Arcanum/CyberAlchemy/DomainSpec. | `meaning` is understandable across systems; boundary phrase prevents catch-all drift. | triggered |
| Concept-vs-knowledge status | The name is a model choice, not evidence-backed truth. | Mark as candidate naming, not convention. | triggered |
| Premortem | Naming could become too broad. | Guardrail: use branch question and exclusions. | triggered |

## Closure And Recomposition Proof

Closure:

- Responsibility: name the first branch and define its decision question.
- Inputs: candidate branch model, handoff language, user's naming concern.
- Outputs: recommended label, boundary phrase, aliases, unresolved governance question.
- Abstraction level: naming primitive inside a branch-context discriminator.
- No hidden glue: does not require role catalog changes to be useful.
- No smuggled future scale: defers template migration and schema-facing fields.
- No meaning loss if split further: splitting into `intent`, `domain`, and `definition` would create roles, not a better branch label.

Recomposition:

```text
meaning:
  what the system means, values, defines, promises, or frames

system:
  machinery that realizes meaning

operational:
  situated use of the system in context

bridge:
  evidence, traceability, realization, validation, constraint, and drift across branches
```

Bridge language after replacement:

- `realized_by`: a meaning claim is implemented or served by a system artifact.
- `drifts_from`: observed behavior diverges from meaning, contract, or expected operation.
- `operationalizes`: a meaning claim or system capability is adapted into a situated operating context.

## Evolution Profile

Expected evolution:

- `business` remains a local alias for repositories where that language fits.
- `domain` remains a local alias when the branch is mostly domain semantics.
- `intent` becomes a role or alias for desired direction, promise, or outcome.
- `proposition` can remain a local alias for formal claim-heavy systems.
- future systems can provide profile-specific aliases without changing the global discriminator.

Smallest extension boundary:

```yaml
branch_context:
  primary: meaning | system | operational | bridge
  local_alias: business | domain | intent | proposition | philosophy | null
  role_hint: definition | concept | type | method | policy | premise | outcome | value-measure | problem-frame | string
```

## Deferred Complexity

Deferred:

- replacing `proposition` throughout `BRANCH-AWARE-ONTOLOGY-CANDIDATE.md`,
- updating Ontology Vault README or SKILL,
- changing any templates,
- coordinating with structured-action-schema,
- migrating existing `business` branch language,
- deciding whether `meaning` is canonical.

Reason:

This pass is an interrogation and distillation of naming fit, not an approved convention update.

## Tension Ledger

Resolved:

- `proposition` is too narrow as a global branch name.
- `business` is too domain-specific as a global branch name.
- `intent` is useful but loses definitions and type systems.
- `meaning` is the strongest current candidate if bounded.

Unresolved:

- Should the candidate document be revised now from `proposition` to `meaning`, or should this go through a decision gate first?
- Should the first branch display name be "Meaning Branch" while the field value is `meaning`?
- Should `business` remain the first listed local alias for continuity?

## Premortem

Likely failure:

`meaning` becomes a catch-all because everything in an ontology has meaning.

Guardrail:

Use the branch question and exclusion rule every time:

```text
Does this claim define what the system means, values, promises, frames, or tries
to make true? If yes, meaning. If it realizes that meaning, system. If it applies
the system in context, operational. If it relates branches, bridge.
```

## Frame-Expiry Note

This optimization point expires when:

- a decision gate selects another global label,
- example validation shows `meaning` causes repeated misclassification,
- a schema-facing implementation requires a different stable discriminator,
- Ontology Vault keeps `business` as the governed global label for migration reasons.

## Navigation Guide

Start here:

Use `meaning` as the candidate replacement for `proposition` in discussion and examples.

What changed:

The first branch is no longer best understood as "a proposition." It is better understood as the system's governed meaning layer.

What remains unresolved:

Whether to immediately revise the candidate model or first run a decision gate on the global branch label.

How to use the result:

If revising the candidate, replace:

```text
proposition | system | operational | bridge
```

with:

```text
meaning | system | operational | bridge
```

and preserve:

```text
business, domain, intent, proposition
```

as local aliases or role-level terms.

## Next Route

Decision gate if the goal is to canonically choose the global label.

Candidate revision if the goal is to keep iterating the exploratory model.
