# Claim Model

Schema Artifact Role: non-canonical semantic companion. Machine-validatable
shape is owned by the `.schema.yml` files in `../schemas/`.

## Contents

- [Core terms](#core-terms)
- [Epistemic status](#epistemic-status)
- [Visual claims](#visual-claims)
- [Evidence rules](#evidence-rules)
- [Aggregate status](#aggregate-status)
- [Textual equivalence](#textual-equivalence)
- [Semantic invariants](#semantic-invariants)

## Core Terms

**Reader question:** the single structural question the diagram must answer.

**Load-bearing claim:** a claim whose removal, reversal, or status change would
materially change the answer.

**Visual claim:** meaning carried by a node, label, edge, arrow, order, branch,
merge, loop, enclosure, grouping, proximity, omission, position, color, line
style, size, or emphasis.

**Appropriate evidence:** evidence supporting the same relation, direction,
scope, condition, and strength asserted by the visual encoding.

**Residue:** relevant but undrawn claims, gaps, conflicts, or deferred material
preserved so omission is not mistaken for absence.

## Epistemic Status

| Status | Meaning | Requirement |
|---|---|---|
| `evidence-backed` | A source directly establishes the claim at the represented strength. | At least one exact locator with `direct` support. |
| `inferred` | The claim follows from cited evidence plus explicit synthesis. | At least one locator and a non-empty inference qualification. |
| `hypothesis` | The claim is proposed or speculative. | Must be visibly labeled; motivating evidence does not establish it. |
| `unknown` | Evidence is absent, insufficient, or conflicting. | Record the gap; never render it as established. |

Authority role describes a source's role, not truth. Corroborating or motivating
references alone never make a claim evidence-backed.

## Visual Claims

- A node asserts relevance or existence in scope.
- An edge asserts a relation.
- An arrow asserts asymmetry such as flow, dependence, precedence, or direction.
- Order can imply chronology or priority.
- A branch can imply alternatives, parallelism, or fan-out.
- A merge can imply convergence.
- A loop asserts recurrence, a return point, and usually an exit condition.
- Enclosure asserts containment, ownership, scope, or part-whole structure.
- Grouping and proximity imply shared type or context.
- Size, weight, color, line style, and position can imply confidence, quantity,
  authority, status, or importance.
- Omission can imply absence when the diagram appears complete.

Decorative marks that could reasonably be read semantically must be removed or
declared non-semantic.

## Evidence Rules

- Require direct mention or observation for existence in scope.
- Require ordered evidence for chronology or precedence.
- Require contract, mechanism, or validated behavior for dependency.
- Require an authoritative boundary for ownership or containment.
- Require evidence that licenses causal direction for causality.
- Do not infer absence from missing mention alone.
- Preserve materially conflicting evidence; narrow, split, qualify, or block.
- Use stable source IDs and locator IDs. Every claim support reference must
  resolve to a permitted locator.

## Aggregate Status

Compute aggregate status from included load-bearing claims:

| Included statuses | Aggregate |
|---|---|
| evidence-backed only | `evidence-backed` |
| inferred only, or evidence-backed plus inferred | `inferred` |
| hypothesis only | `hypothesis` |
| unknown only | `unknown` |
| any other multi-status combination | `mixed` |
| no diagram | `not-applicable` |

Do not include residue-only claims in the aggregate.

## Textual Equivalence

The textual equivalent is the diagram's semantic structure expressed without
dependence on the image. It must preserve:

- entities or states;
- typed and directed relations;
- conditions, alternatives, convergence, and recurrence;
- scope, completeness, and material exclusions;
- evidence, inference, hypothesis, and unknown distinctions.

It is not:

- a caption, which is a short summary;
- a rationale, which explains why the diagram was chosen;
- appearance-only alt text.

The semantic model must list every included load-bearing claim covered by the
textual equivalent. The validator checks coverage IDs and non-empty content;
semantic parity still requires assisted or human reconciliation.

## Semantic Invariants

1. IDs are unique within their namespace.
2. All source, locator, claim, element, encoding, member, and lineage references resolve.
3. Evidence-backed claims have direct support.
4. Inferred claims have cited support and explicit synthesis.
5. Material conflicts are preserved and weaken, split, or block the claim.
6. Included unknowns are visibly marked.
7. Every included load-bearing claim maps to a visual element or encoding.
8. Every included load-bearing claim is covered by the textual equivalent.
9. Aggregate status is computed rather than selected by preference.
10. Receipts identify the exact revision and member digests inspected.
11. Official readiness requires all publication checks to pass.
12. Corrections create a new revision and never overwrite the reviewed bytes.
