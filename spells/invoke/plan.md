# Invoke Plan Contract

## Purpose

Plan turns one admitted Design into one canonical implementation plan without
starting implementation. The JSON source owns every planning decision. The
compiler derives the graph, Work Pack, task pages, wave pages, validation
strategy, gap view, execution navigation, and consumer projections.

`WORK-PACK.md` is a reading view. Editing it never changes the plan. Change
`PLAN-SOURCE.json` and compile a new absent bundle instead.

## Current And Historical Contracts

- Current source: `invoke.plan-source.v2`.
- Current producer: `invoke.compile-plan-bundle.v2`.
- Current stage receipt: `invoke.plan-stage-receipt.v2`.
- Current admission: `invoke.plan-bundle-admission-receipt.v1`.
- Historical `invoke.plan-execution-source.v1` and Work-Pack-as-source material
  remain validate-only and cannot establish a new artifact PASS.

## Authored Source

The source states, in concrete records:

- what the implementation must achieve;
- which delivery slices serve each objective;
- which implementation layer each wave crosses;
- which tasks and Smallest Working Units belong to each wave;
- the implementation detail and write boundary of each unit;
- the command and expected result for every validation;
- which gate closes every wave;
- current blockers, gaps, and repair routes;
- which units may later be offered to Task Session, Goal, or direct work;
- what closeout evidence will be required; and
- the exact current Design stage and admission receipts being implemented.

IDs are globally unique. All references must resolve. Wave dependencies must
be acyclic. Task, wave, gate, SWU, and validation membership must agree in both
directions. Every task has at least one SWU and one validation. Every wave has
exactly one gate. A mutation-capable plan has at least one execution entry.

## Generated Bundle

The producer creates one absent directory atomically. It contains the exact
source, normalized graph, consumer applicability matrix, SWU manifest, Work
Pack, layering and validation views, gap view, task and wave pages, optional
execution navigation, consumer projections or negative evidence, and the Plan
stage receipt.

Partial publication and overwrite are forbidden. Generated Markdown contains
no independent meaning.

## Consumer Applicability

Exactly seven rows are required:

| Consumer | Applicable when | False result |
| --- | --- | --- |
| Work-Pack Readiness Audit | The plan can mutate repository material. | Typed negative evidence. |
| Implementation Readiness | The plan can mutate and has an execution entry. | Typed negative evidence. |
| Task Session | An execution entry selects `task-session`. | Typed negative evidence. |
| Context Builder | An execution entry is delegated or requires bounded-context execution. | Typed negative evidence. |
| Dispatch Spec | Any of `multi_owner`, `delegated`, `protected_scope`, or `reusable_graph` is true. | Typed technique trace plus negative evidence. |
| Goal | An execution entry selects `goal`. | Typed negative evidence. |
| Signal Observer | Observation is configured and its contract is admitted. | Typed negative evidence when unconfigured; a configured but unadmitted contract blocks. |

An applicable consumer receives a machine projection and no-effect validation.
Every row binds the exact validator executable path, digest, and byte size.
WPRA receives audit-config v2 and must produce byte-identical semantic manifests
and selection handoffs in two runs of the real audit entrypoint. No configured
implementation command may run. Every applicable bounded-context unit is
validated, not only the first unit.
An inapplicable consumer receives the evaluated predicate inputs and reason.
An unknown predicate blocks the bundle. Context version is `1.2.0` when the
transient-output set is empty and `1.3.0` when it is nonempty.

Signal Observer validation uses the shared observability envelope schema and
validator. It does not append a telemetry event. Goal validation checks a
route contract without starting the Goal loop.

## Admission And Status

Admission reads the submitted bundle, validates its stage receipt and exact
inventory, recompiles the same source in a temporary directory, and compares
every path and byte. It returns PASS only when the replay and all seven
consumer results agree.

Admission proves deterministic authorship at one point in time. It does not
select work, launch a task, approve mutation, append telemetry, publish, or
promote anything.

A new Plan `artifact_authored: pass` requires the matching v2 stage receipt
and v1 admission receipt. Registry and mutation-runtime status remain separate
axes.

## Command Surface

```text
tools/arcanum invoke plan describe
tools/arcanum invoke plan check source --request REQUEST.json --repo-root ROOT
tools/arcanum invoke plan author source --request REQUEST.json --repo-root ROOT --output PLAN-SOURCE.json
tools/arcanum invoke plan produce bundle --source PLAN-SOURCE.json --repo-root ROOT --output ABSENT_BUNDLE
tools/arcanum invoke plan admit admission --bundle BUNDLE --repo-root ROOT --output PLAN-ADMISSION.json
tools/arcanum invoke plan status --request STATUS-REQUEST.json --repo-root ROOT --output STATUS.json
```

Every output must be absent. The CLI has no hidden session and never repairs or
overwrites an earlier result.
