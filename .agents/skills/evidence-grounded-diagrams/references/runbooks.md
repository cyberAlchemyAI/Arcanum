# Mode and Diagram Runbooks

## Contents

- [Create](#create)
- [Review](#review)
- [Revise](#revise)
- [Admission decision](#admission-decision)
- [Diagram family selection](#diagram-family-selection)
- [Precision audit](#precision-audit)

## Create

1. Validate or normalize the request.
2. Decide whether a diagram is warranted.
3. Build the semantic model and residue before source.
4. Select the family from the supported relation.
5. Draft source, textual equivalent, caption, and rationale.
6. Validate source; render and inspect when possible.
7. Reconcile model, source, render, and text.
8. Stage, persist, validate, then hand off.

Creation outcomes:

- `diagram`: a diagram materially improves inspection and its claims are honest;
- `no-diagram`: prose or a table is more faithful;
- `needs-evidence`: a diagram is warranted but load-bearing claims cannot yet be
  supported or marked without defeating the reader question.

## Review

Review is read-only.

1. Identify the exact artifact revision and digests when available.
2. State the question the diagram appears to answer.
3. Decode load-bearing claims carried by labels and geometry.
4. Test each claim against exact permitted locators.
5. Record supported, unsupported, ambiguous, inferred, hypothetical, or unknown.
6. Inspect source and rendered bytes separately.
7. Order findings by consequence and name the first blocker.
8. Write a receipt bound to the inspected revision or normalized inline source
   bytes. Keep it outside the audited bundle unless it was already a declared
   immutable member.
9. Validate the receipt against the exact source bytes or bundle members, not
   only against its schema. Pipe supplied inline source through
   `validate_review_receipt.py --target-stdin` so validation does not require a
   fabricated durable target path.
10. Return `PASS`, `FIX`, or `INSUFFICIENT_EVIDENCE` without modifying the target.

## Revise

Revise requires explicit correction authorization.

1. Complete the review route first.
2. Preserve the reviewed bundle and receipt.
3. Allocate the next unused revision and record `supersedes`.
4. Apply the smallest corrections that resolve accepted findings.
5. Re-run the complete create validation and persistence path.
6. Leave the prior revision bytes unchanged. After the new revision validates,
   let the resolver derive the prior revision's effective `superseded` state.

Never overwrite or reuse the reviewed revision ID.

## Admission Decision

Before drawing, answer:

1. What exact relation, mechanism, comparison, boundary, or transformation must
   the reader understand?
2. Why is a diagram better than prose or a table?
3. What evidence supports the objects and relations?
4. What relation type is actually represented?
5. What do arrows, loops, enclosures, branches, styles, colors, and position mean?
6. Is the representation complete or explicitly partial?

## Diagram Family Selection

- Flowchart: process or control flow.
- State-transition: states and licensed transitions.
- Sequence: ordered interaction among actors or components.
- Dependency graph: edges mean dependency.
- DAG: dependency plus established or contractually imposed acyclicity.
- Tree: hierarchy with required single-parent structure.
- Containment: scope, nesting, ownership, or part-whole; declare which.
- Timeline: chronology is load-bearing.
- Typed-relation graph: several non-sequential relation types matter.
- Causal diagram: evidence licenses causal direction.

Do not reinterpret dependency as time, correlation as causation, adjacency as
ownership, or layout as authority.

## Precision Audit

Inspect the diagram with labels partly hidden:

- Does direction assert more than the source?
- Does layout invent chronology, precedence, or a main path?
- Does a branch look exclusive when branches can coexist?
- Does a merge imply guaranteed convergence?
- Does enclosure imply ownership when only association is known?
- Does a tree invent unique parentage or a DAG invent acyclicity?
- Does a loop return to the correct point and show the right trigger and exit?
- Does a missing edge look like proof of no relation?
- Does prominence imply unsupported importance, confidence, quantity, or authority?
- Could a reasonable reader retell the wrong mechanism from the visual alone?

Revise when any answer is yes.
