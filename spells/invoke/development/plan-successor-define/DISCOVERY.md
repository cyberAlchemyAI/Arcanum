# Plan Successor Definition Discovery

## Purpose

Define the four Plan-local terms needed before rebuilding Invoke Plan. The
definitions must preserve the current Design-to-Plan boundary, distinguish
authored planning material from generated files, and prevent a valid file from
being mistaken for admitted or execution-ready evidence.

## Plan Authoring Source

The one machine-readable source of truth in which an author states the admitted
Design binding, objective, delivery boundary, slices, layers, waves, tasks,
SWUs, implementation details, validation obligations, blockers, gaps, eligible
execution routes, and closeout obligations. Generated views, calculated
digests, validator decisions, selected-unit state, readiness results,
acceptance, and execution receipts are not authoring fields.

## Plan Candidate Bundle

The complete deterministic set of Plan files generated from one exact Plan
authoring source. A candidate bundle is reviewable output; its existence does
not establish independent admission, implementation readiness, acceptance, or
execution authority.

## Plan Bundle Admission

An independent point-in-time result that replays the exact Plan authoring
source, compares every required candidate file, validates the live consumer
contracts, and reports whether that exact bundle is current. Admission does not
approve or execute the Work Pack.

## Plan Evidence State

The typed statement of what has actually been proved about one Plan artifact.
It keeps authoring, bundle admission, implementation readiness, owner
acceptance, and execution authority separate so an earlier result cannot be
reported as a later one.

## Plan

A governed translation of one admitted Design into implementation work. It
states what will be delivered, how the work is decomposed and ordered, what
evidence proves each unit, and which exact unit may be handed to an execution
owner. A Plan does not revise the Design it consumes and does not execute its
own work.

## Work Pack

A deterministic coordinator view of one exact Plan authoring source. It shows
the objective, delivery slices, task and SWU navigation, dependencies, gate
summary, blockers, gaps, and next eligible boundary without duplicating every
task or SWU contract. It does not own Plan meaning or downstream lifecycle
state.

## Delivery Slice

One coherent outcome that can be demonstrated or evaluated as part of the
implementation objective. A delivery slice groups tasks by delivered behavior;
it is not an execution-order wave and is not itself a smallest working unit.

## Implementation Layer

One decision boundary in the L0-L3 implementation model. It names the question
being resolved, the evidence required to advance, and what remains deferred. A
layer governs waves but does not contain task implementation instructions.

## Plan Wave

An authored execution-order group that maps tasks and SWUs to one
implementation layer, records dependencies and safe parallel work, and names
entry and exit gates. A generated wave file is a view of this source record and
does not own the detailed task or SWU contract.

## Plan Task

One authored implementation responsibility within the Plan source. It owns an
objective, dependencies, write scope, done criteria, validation, and one or
more SWUs when the task is not already the smallest executable unit. A split
task file is a generated view of this record.

## Smallest Working Unit

The smallest independently executable and reviewable change or decision. An
SWU belongs to exactly one Plan task and owns one primary behavior, one write
scope, one completion boundary, and the evidence needed to verify it.

## Implementation Detail Contract

The concrete task-level description of how work must be performed when a title
or outcome is insufficient. It records algorithms or steps, interfaces, data
flow, inputs, outputs, edge cases, failure handling, constraints, and checks.

## Validation Obligation

One exact command, deterministic check, or reviewable observation required to
prove a Plan unit or gate. It states when the check can run and which evidence
the result must produce; a planned future check is not already passing proof.

## Plan Gate

A typed condition that consumes named evidence before a layer, wave, task, or
handoff may advance. Missing, stale, failed, or contradictory evidence blocks
the gate; prose confidence does not pass it.

## Plan Blocker

A known condition that prevents the current Plan state, selected unit, gate, or
handoff from proceeding. It must name its cause, affected boundary, owner, and
repair route.

## Plan Gap

Known missing information or evidence that does not currently prevent the
bounded Plan state from proceeding. A gap must name its owner and escalation
condition; if it affects acceptance or safe execution, it is a blocker instead.

## Execution Entry

An authored eligibility contract for handing one task or SWU class from Plan
to an execution-readiness or Task Session owner. It binds admission timing,
dependencies, write and effect scope, allowed route, required evidence, and
stop conditions. A separate downstream selection receipt chooses and binds the
exact unit for one attempt.

## Execution Pack

A deterministic choreography view for medium or high complexity Plans. It
projects waves, cross-task dependencies, and safe parallelization directly from
the exact Plan authoring source, but it does not replace that source or own
selection, readiness, acceptance, or execution state.

## Thin Representation Decision

Preserve the complete Work Pack → slices → layers → waves → tasks → SWUs
contract, but keep only authored meaning in the Plan source. Generate compact
human views according to actual complexity. Store admission, readiness,
selection, acceptance, execution, and closeout results in independent receipts
or deterministic status projections. Thin the representation, not the proof
obligations.

## Existing Boundaries Considered

- `plan.md` owns the current Plan mode behavior and evidence ceiling.
- `PLAN-ARTIFACT-BOUNDARIES.md` separates the Work Pack from layering and
  execution evidence.
- `design.md` establishes the admitted Design input boundary that Plan must
  consume without silently redesigning it.
- `plan-execution-source-v1.schema.json` and its compiler are the current
  machine-first baseline, retained as historical input during successor work.
- Work Pack Readiness Audit and Implementation Readiness remain independent
  consumers; Plan authoring cannot manufacture their evidence.
- The capability-status resolver must preserve the difference between an
  authored artifact and later readiness or runtime states.

## Authority Limit

This discovery supports a candidate-only Define v3 bundle. It changes no
canonical definition, Plan contract, runtime package, acceptance state, or
execution authority.
