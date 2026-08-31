# invoke:plan-successor:definition-target

Define the Plan itself, its executable parts and relationships, and the exact authoring, admission, and evidence states required before rebuilding Invoke Plan.

## One authored source

The Plan successor must have one machine-readable semantic source; Work Pack, task, wave, layering, and Execution Pack files are deterministic views, while lifecycle evidence remains external.

## Admission is independent

A generated Plan bundle may establish a new artifact PASS only after a separate validator replays the source, compares every required file, and runs the declared Plan consumers.

## Readiness remains separate

Bundle admission does not establish Work Pack readiness, implementation readiness, owner acceptance, or execution authority; each later state requires its own exact evidence.

## Admitted Design is bound input

Plan consumes one exact admitted Design result and may expose a missing planning detail, but it must not silently revise the Design decision while producing the Work Pack.

## Current Plan remains historical input

The Plan v1 source, compiler, and receipts remain available for validation and migration evidence but cannot establish a new successor-format PASS.

## Thin representation, complete obligations

The successor may omit unnecessary split views for simple Plans, but it must preserve the complete slices, layers, waves, tasks, SWUs, validation, gates, residue, route, and closeout contracts in the semantic source.
