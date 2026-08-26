# Multi-Lens Composition

Run composition only after every selected lens has produced an independent
view. Composition inspects relations between views; it does not summarize or
concatenate them.

## Questions

Ask:

- Does an epistemic distinction constrain a system transition?
- Does a system transition require an authority or evidence boundary?
- Does a structural transformation preserve the evidence or meaning required
  downstream?
- Does a local system effect compose into a larger context?
- Are different lenses naming the same load-bearing relation?
- Do the lenses disagree about the relevant unit?
- Does one lens expose a witness assumed by another?
- Does the joint view create a new question with operational consequences?

A cross-lens relation earns inclusion only when it changes what can be
understood, verified, decided, implemented, or asked next.

Do not call a property emergent merely because composition exposed it. State
the bounded fact: the joint view exposed a distinction, question, or capability
not produced by the individual views under the same task and evidence boundary.

## Preservation invariant

Composition augments `per_lens_findings`; it never replaces them.

Keep a material single-lens finding eligible for downstream use even when it
has no relation to another lens. Do not retain only agreements or jointly
produced findings.

## Return

Create `composed_findings` records using these relation kinds:

- `agreement`;
- `tension`;
- `dependency`;
- `joint-distinction`;
- `new-question`.

Every record must reference the contributing finding IDs, state the relation,
carry any additional evidence locators, and preserve material uncertainty.
