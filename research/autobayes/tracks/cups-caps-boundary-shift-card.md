---
profile: autobayes-research
name: Cups, Caps, And Boundary Shifts
description: Local source-backed card for AutoBayes cup/cap/reveal/copier boundary operations and appendix examples.
type: research-card
status: pass
lane: cups-caps-boundary-shift-card
last_updated: 2026-06-07
promotion_scope: local-research-only
---

# Cups, Caps, And Boundary Shifts

## Source Kind

- AutoBayes paper: section 2 and appendix examples.
- Local receipt: [appendix-examples-distill.md](appendix-examples-distill.md).
- Local definition: [open-model-definition-card.md](open-model-definition-card.md).

## Source Meaning

The local tower reads cups, caps, reveal, copier, and related notation as
open-model operations that change what is exposed, copied, hidden, or treated as
known at a boundary.

The source-level caution is that these are not UI metaphors. They are part of
the open-model calculus used to compose probabilistic structures.

## Boundary Shift Pattern

The clearest local example is supervised learning:

```text
label would normally be hidden / inferred
paired training data supplies the label
cup-shaped boundary move makes label observed for training
```

So the training surface changes:

```text
ordinary prediction:
  input -> label/output

supervised training:
  input + known label -> observed training receipt
```

The paper uses this to show that known labels can be incorporated as observed
structure, not merely treated as after-the-fact metadata.

## Arcanum Reading

The Arcanum-safe translation is:

```text
Sometimes the legal receipt shape changes because the operator has supplied
evidence that would normally be hidden.
```

This resembles Arcanum's boundary/evidence contracts:

- a route branch can change what fields are valid;
- a handoff can reveal a normally hidden intermediate;
- a supplied example can turn an inferred value into an explicit receipt;
- a dependent context can change the output shape.

## Misuse Warnings

- Do not translate "cup" as "attach labels" only.
- Do not use cup/cap vocabulary as canonical Arcanum pattern names.
- Do not treat boundary shifts as permission to skip source-state accounting.
- Do not flatten dependent receipt shape into optional fields when the source lesson is structural.

## Status

`closed-distill`

## Residue

If Arcanum wants to borrow this, the next artifact should be a toy game about
receipt shape changing by route branch. It should use Arcanum vocabulary, not
AutoBayes cup/cap names.
