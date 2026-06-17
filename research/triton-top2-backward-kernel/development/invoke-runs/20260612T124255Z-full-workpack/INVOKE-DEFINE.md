# Invoke Define - Full Work Pack To Completion

Run id: `20260612T124255Z-full-workpack`

Status: `pass`

## Objective

Define the full bounded work pack needed to carry the Top2/Triton challenge from
current research/reference scaffold to final implementation-readiness and, when
environment gates allow, Triton implementation and validation.

## Current State

Already complete:

- research tower;
- prior-art map;
- novelty map;
- V0 fixed-mask decisions;
- standard-library reference harness;
- finite-difference validation for manual `dW`;
- CAP2-v0 candidate spec.

Still required:

- PyTorch autograd/gradcheck parity;
- prior-art sparse baselines;
- CAP2-v0 reference and kill/promote decision;
- formal math validation/proof notes;
- Triton fixed-mask kernel;
- Triton selected-relaxation kernel if CAP2 or another relaxation survives;
- zero-allocation validation;
- FP16 tolerance validation;
- final comparison and novelty report.

## Work-Pack Definition

The work pack owns:

- task sequencing;
- gates;
- completion evidence;
- validation commands;
- final report.

It does not claim novelty until CAP2 survives comparison.
