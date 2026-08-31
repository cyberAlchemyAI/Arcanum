# Invoke Plan Authoring Guide

This guide is for the agent or operator supplying the planning decisions. A
human reader who first wants the idea should start with the
[Plan overview](./plan/README.md).

## The Job

Turn one admitted Design into a concrete build map. Do not repeat architecture
prose. State the work: objectives, slices, layers, waves, tasks, SWUs, exact
implementation details, validation commands, wave gates, blockers, gaps,
later execution entries, and closeout evidence.

## What You Author

| Record | Concrete question it answers |
| --- | --- |
| Objective | What result must exist when the plan is complete? |
| Slice | Which usable part of that result can be delivered and checked together? |
| Layer | What technical uncertainty is removed at this level, and what evidence lets work continue? |
| Wave | Which tasks can start after the named dependencies, and which gate closes them? |
| Task | Who owns a bounded outcome, which SWUs implement it, and what is the next action? |
| SWU | What is the smallest independently reviewable change, where may it write, and how is it checked? |
| Implementation detail | What algorithm, data flow, interface rule, or failure behavior must the task implement? |
| Validation | Which exact command or review runs, and what result counts as success? |
| Gate | Which wave it follows, which validations it requires, and where failure returns? |
| Blocker or gap | What is missing, whether it is open, and who or what repairs it? |
| Execution entry | Which unit may later be offered to which route and what receipt must return? |
| Closeout obligation | Which evidence must exist after implementation finishes? |

Use concrete nouns and actions. “Implement the architecture” is not a task.
“Parse duplicate JSON keys before schema validation and return exit 2 without
creating the bundle” is an implementation detail.

## What The CLI Owns

Omit `$schema`, `schema_version`, `source_id`, `profile_id`,
`authority_effect`, hashes, sizes, producer identity, inventories, receipt IDs,
and receipt digests. The CLI inserts or calculates them.

Bind exactly two evidence files in the authoring request:

```json
[
  {"pointer": "/design_binding/stage_receipt", "path": "path/to/INVOKE-DESIGN-STAGE-RECEIPT.json"},
  {"pointer": "/design_binding/admission_receipt", "path": "path/to/DESIGN-BUNDLE-ADMISSION.json"}
]
```

The CLI fills their hashes and byte sizes. Both must be current no-authority
PASS receipts for Design v3/v2.

## Author And Compile

```text
tools/arcanum invoke plan describe source
tools/arcanum invoke plan check source --request PLAN-SOURCE-AUTHORING-REQUEST.json --repo-root ROOT
tools/arcanum invoke plan author source --request PLAN-SOURCE-AUTHORING-REQUEST.json --repo-root ROOT --output PLAN-SOURCE.json
tools/arcanum invoke plan produce bundle --source PLAN-SOURCE.json --repo-root ROOT --output ABSENT_PLAN_BUNDLE
tools/arcanum invoke plan admit admission --bundle PLAN_BUNDLE --repo-root ROOT --output PLAN-BUNDLE-ADMISSION.json
```

The producer creates the directory only after graph and consumer checks pass.
Admission compiles it again. Never edit the generated Work Pack to repair a
failed admission.

## Consumer Inputs

Set these fields from the actual plan:

- on each execution entry, set `delegated` when another worker or owner will
  perform the unit;
- on each execution entry, set `bounded_context_execution` when the unit must
  run from a selected evidence set;
- set `consumer_inputs.dispatch.multi_owner` when execution crosses owners;
- set `consumer_inputs.dispatch.delegated` when the route delegates work;
- set `consumer_inputs.dispatch.protected_scope` when the route carries
  protected material;
- set `consumer_inputs.dispatch.reusable_graph` when the route will be reused;
- set `consumer_inputs.observability.configured` only when an observer is
  configured; and
- when configured, set `observer_contract_admitted` only after its machine
  contract is admitted. Configured-but-unadmitted observation blocks the bundle.

Choose `route: goal` or `route: task-session` on each execution entry. That
choice determines which route contract is generated. Write scopes must name
exact files; a directory is not an executable write boundary.

These values decide which projections exist. They do not authorize the later
consumer to run.

## Before Calling It Complete

- Every identifier is unique and every reference resolves.
- Every task belongs to its declared wave and slice.
- Every task has at least one SWU and validation.
- Every wave has one gate and no dependency cycle.
- Every mutation-capable plan has an execution entry.
- Every open blocker or gap has a concrete repair route.
- All seven consumer rows contain either a passing projection or negative evidence.
- Independent replay admission passes.

The complete example is under `examples/plan-v2/`.
