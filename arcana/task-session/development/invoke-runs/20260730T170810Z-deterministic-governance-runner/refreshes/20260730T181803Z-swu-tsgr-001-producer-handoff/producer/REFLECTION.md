# Producer Reflection

## Signal summary

The independent observer found one severe ownership-and-receipt gap before producer
completion. Isolated staging was sound, but the draft conflated the target sigil
with the lifecycle owner and underspecified the evidence required to return staged
material through Task Session review.

## Patterns found

- A material target can belong to the `task-session` sigil while lifecycle ownership
  remains with `sigil-development`.
- Pre-admission staging is not a Task Session execution result.
- Parent-repository and Arcanum-root path conventions must both be explicit when a
  package is authored from the parent repository.
- Producer evidence must bind command argv, cwd, validator identity, exit status,
  counts, staged manifest, canonical preconditions, and undeclared-output checks.

## Changes applied

- Split lifecycle owner, target sigil, selection/review owner, and execution owner.
- Added a closed producer-receipt schema.
- Added exact source, selection, handoff, lifecycle, observer, root, precondition,
  staged-output, runtime, validation, Experiment Harness, blocker, and residue
  fields.
- Preserved Task Session review before any SWU-completion claim.
- Preserved `mutation_ready=false`.

## Changes rejected

- No direct canonical application.
- No claim that the producer receipt is Task Session mutation admission.
- No generated runtime mirror update.
- No Experiment Harness or promotion claim.

## Thresholds

No threshold changes. A future owner conflation, missing Task Session review, or
staged/canonical path ambiguity remains a severe-gap trigger.

## Next review trigger

Review again if Task Session cannot bind this receipt into an exact material package
or if any of the five canonical target preconditions changes before admission.
