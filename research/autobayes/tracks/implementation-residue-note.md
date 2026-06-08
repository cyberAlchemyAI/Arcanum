---
profile: autobayes-research
name: Implementation Residue Note
description: Local bridge note for what AutoBayes suggests but does not implement for Arcanum.
type: residue-note
status: pass
lane: implementation-residue-note
last_updated: 2026-06-07
promotion_scope: local-research-only
---

# Implementation Residue Note

## Source Kind

- AutoBayes paper: implementation is framed as future-facing; the paper defines compositional tools and sketches optimization semantics.
- Local receipts: [semantics-functor-reader.md](semantics-functor-reader.md), [related-framework-crosswalk.md](related-framework-crosswalk.md), [arcanum-bridge-decision.md](arcanum-bridge-decision.md).

## What Is Closed

AutoBayes supplies a strong research lens:

```text
declared local structure
  -> reverse/inversion behavior
  -> local objective pressure
  -> exposed parameters
  -> runtime/optimization semantics
```

The Arcanum-safe bridge is closed:

```text
use the separation discipline;
do not import the math vocabulary as canon.
```

## What Remains Implementation Residue

| Residue | Why It Remains Residue | Candidate Arcanum Owner | Promotion Condition |
| --- | --- | --- | --- |
| Reverse handoff legality | The analogy is strong, but Arcanum needs a workflow-specific example before changing contracts. | `dispatch-spec`, `task-session` | Toy game proves a downstream artifact can reinterpret upstream context only with a named state namespace. |
| Local evidence pressure vs global validation | AutoBayes local loss is mathematical; Arcanum evidence is broader. | `experiment-harness`, `observability` | Example distinguishes local evidence, global verdict, and promotion evidence without VI terminology. |
| Runtime semantics registry | AutoBayes section 5 sketches semantics strategies but does not provide an Arcanum runtime registry. | `experiment-harness`, `dispatch-spec` | A proposed registry records allowed handles, semantics choice, approximation residue, and validation expectations. |
| Parameter/knob exposure | The principle is safe, but Arcanum needs owner-specific fields. | `task-session`, `experiment-harness` | Work-pack defines how write scope, runtime choice, and optimizable knobs differ. |
| Branch-dependent receipt shape | Appendix examples suggest receipt shape can depend on input/branch. | `dispatch-spec`, `context-builder` | Toy game demonstrates branch-indexed receipt schema without importing cup/cap names. |

## Borrow / Block / Analogy-Only Closure

Borrow now:

- syntax versus semantics split;
- explicit state namespace for reverse handoffs;
- local evidence before global synthesis;
- parameter/knob exposure;
- composition receipts.

Block now:

- canonical vocabulary promotion;
- renaming residue as latent space;
- treating validation scores as VFE/loss;
- treating optimizer/runtime as orchestrator;
- collapsing guides, inversions, adapters, and handoffs into one term.

Analogy-only:

- open model;
- Bayesian lens;
- statistical game;
- pushed-forward prior;
- semantics functor;
- lax section.

## Proposed Follow-Up Work-Pack Candidate

```text
AutoBayes-Inspired Arcanum Contract Hygiene Toy Games
```

Candidate SWUs:

1. reverse handoff state namespace toy game;
2. local evidence pressure versus global validation toy game;
3. explicit runtime knob exposure report shape;
4. branch-dependent receipt shape example.

This note does not authorize those changes. It only sharpens the residue.

## Status

`promoted-residue`
