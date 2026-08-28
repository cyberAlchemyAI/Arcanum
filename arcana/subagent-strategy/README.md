# Subagent Strategy

Subagent Strategy is an Arcana sigil for deciding when multi-agent work is
justified and governing it from proposal through closeout.

It preserves the reusable coordination contract behind repository-local
subagent routers without importing a consuming project's constitutions, agent
names, or private evidence. It ships a DomainSpec-derived default form and
ledger convention that consuming profiles may override.

Status: **seed**. The public contract, deterministic YAML registrar, and
experiment harness exist; broader live runtime evidence is still required
before promotion readiness can be claimed.

## Problem It Solves

Spawning several agents is easy. Governing the work is harder. Without an
explicit strategy, a fan-out can duplicate angles, exceed the parent context,
act before human approval, lose partial failures, or finish without closing its
agents and ledger records.

This sigil supplies the portable lifecycle:

```text
trigger decision
  -> type-owner and preflight resolution
  -> temporary UTF-8 JSON strategy sheet
  -> composite deterministic confirmation readiness
  -> sheet-only independent tension checks on the admitted digest
  -> one exact-sheet confirmation
  -> append-only YAML registration and temporary-sheet consumption
  -> dependency and type-owner handoff readiness
  -> execution
  -> final approval and closeout
  -> result hooks and observability
```

## Use When

- two or more agents may work independently or in a dependency graph,
- three or more sources, lenses, or returns require synthesis,
- raw exploration should be isolated from the parent context,
- a repository requires a proposal and human gate before subagents run,
- dispatch and close rows must be registered in an append-only YAML ledger.

## Do Not Use When

- one bounded helper is sufficient and stays inside its parent's scope,
- direct work is smaller than the coordination overhead,
- the runtime cannot execute the required tension gate,
- the repository has no valid runtime profile for registration or execution,
- the user has not explicitly confirmed the final strategy sheet.

## Portable Core And Local Profile

The sigil owns universal behavior:

- trigger assessment,
- helper-versus-dispatch distinction,
- tension and anti-bias requirements,
- proposal, confirmation, freeze, registration, execution, and closeout order,
- dependency semantics,
- type-owner stage-handoff readiness before consuming groups launch,
- partial-result propagation,
- final approval,
- paired dispatch and close YAML rows,
- observability and reflection signals.

A consuming repository owns the bindings:

- supported dispatch types and their owner capabilities,
- type-specific preflights and output judgment,
- the strategy-sheet schema and validator,
- agent-pool rules,
- tension-check implementation,
- registration command and append-only ledger,
- inventory and observability hooks,
- artifact locations and public/private constraints.

Use [templates/runtime-profile.md](templates/runtime-profile.md) to describe
those bindings. A missing profile does not prevent an inline trigger decision
or a proposed strategy, but it blocks registration and execution.

## Lifecycle Gates

1. Decide whether a dispatch trigger holds.
2. Resolve the dispatch type, local owner, and configured preflights.
3. Draft groups, agents, angles, expected outputs, dependencies,
   final approval, pairwise predicted disagreements, and every field required
   by the current local form owner as a UTF-8 `*.tmp.json` beneath
   `.arcanum/runtime/subagents-strategy/`. Load-bearing gate evidence belongs
   in the sheet, not a companion file.
4. Run the form owner's non-mutating composite confirmation-readiness validator
   against the exact temporary sheet. Form/version, live type prerequisites,
   agent and approver eligibility, tension-evidence completeness, and
   publication boundaries all close here.
5. Warn and rematerialize before confirmation when a runtime or schema
   projection is stale; block all other form-admission errors.
6. Run two independent tension checks against only the admitted sheet bytes
   and rubric. Preserve both independent verdicts before any checker/reviewer
   comparison.
7. Present the complete admitted sheet and artifact destination to the human.
8. Treat draft-revision authorization as discussion, not confirmation. Ask once
   after readiness and PASS/PASS. Confirmation binds the exact reviewed sheet
   bytes.
9. After any byte change, rerun readiness and both tension checks, present the
   sheet again, and require explicit reconfirmation.
10. Append the confirmed row to
    `.arcanum/observability/subagents-strategy/subagents-dispatch.yaml` and
    consume the temporary JSON before spawning any working group.
    For native capability-bound execution, bind the exact sheet digest and the
    governed temp paths in `subagent_strategy.registration`; Orchestrate must
    verify that ledger row and consumed sheet before emitting actions.
11. Run a consuming group only when blocking dependencies are complete and the
    type owner's declared handoff-readiness criteria pass for the exact upstream
    artifacts.
12. Route `needs_feedback` gaps through declared feedback or revision edges
    while loop capacity remains; preserve `blocked` gaps for final approval.
13. Propagate partial and failed results downstream.
14. Join and close every agent, report the exit reason, append the close row
    through the same registrar, consume its temporary JSON, and run
    Orchestrate `verify-close` when that runtime was used.
15. Update configured result and observability hooks.

## Artifacts

- [SKILL.md](SKILL.md) is the executable behavior contract.
- [templates/runtime-profile.md](templates/runtime-profile.md) defines portable
  repository bindings.
- [profiles/arcanum.yaml](profiles/arcanum.yaml) is this repository's active
  binding for the default registrar and observability ledger.
- [templates/dispatch-record.example.json](templates/dispatch-record.example.json)
  shows the direct temporary sheet fields accepted by the default registrar.
- [templates/usage-telemetry.md](templates/usage-telemetry.md) defines the
  behavior signals used for later reflection.
- [scripts/append-dispatch.cjs](scripts/append-dispatch.cjs) validates one
  temporary record, appends one YAML row, and safely consumes successful temp
  inputs.
- `development/` contains the Experiment Harness and promotion evidence.

## Default Dispatch Form And Registrar

The default form is the DomainSpec v0.7.0 shape: top-level `dispatch_id`,
`schema_version`, `dispatch_type`, `goal`, `context`, `max_loops`,
`final_approver`, and `groups`; optional `meta`, `parent_dispatch_id`,
`anti_bias_global`, `output_mode`, `working_folder`, `invoked_by`, and
`connections`. Groups contain agents directly, and groups/connections are
written as JSON flow columns inside the YAML row.

Write the confirmed candidate beneath the governed temp root and register it:

Every agent in a new candidate must have a non-null pool-backed `agent_name`.
Its `initial_prompt` begins with `You are {agent_name}.`, then one blank line,
then the bounded instructions. Confirmation binds that identity sentence as
part of the exact sheet bytes.

```text
node arcana/subagent-strategy/scripts/append-dispatch.cjs --consume .arcanum/runtime/subagents-strategy/<dispatch-id>.tmp.json
```

At termination, write a temporary close record containing `close_of`,
`exit_reason`, `agents_spawned`, optional `feedback_prompts`, and `invoked_by`,
then call the same command. Successful and idempotent appends consume the temp;
validation or append failures preserve it for diagnosis.

`agents_spawned` records `planned_total`, actual launched `total`,
`not_launched`, the launched-agent `tree`, and `loops_used`. Its tree sums to
`total`, while `total + not_launched` equals `planned_total`; a `resolved`
close requires every planned agent to have launched.

For native capability-bound execution, keep the richer Dispatch Spec document
as separate runtime state and add:

```json
{
  "subagent_strategy": {
    "registration": {
      "schema_version": "arcanum.subagent-strategy-registration.v0.3",
      "ledger": ".arcanum/observability/subagents-strategy/subagents-dispatch.yaml",
      "sheet_schema_version": "0.7.0",
      "sheet_sha256": "<digest returned by --check>",
      "execution_projection_sha256": "<digest returned by native_dispatch_coordinator.py projection-digest>",
      "temporary_sheet": ".arcanum/runtime/subagents-strategy/<dispatch-id>.tmp.json",
      "temporary_close": ".arcanum/runtime/subagents-strategy/<dispatch-id>.close.tmp.json"
    }
  }
}
```

Each capability-bound role declares one `agents` entry per planned instance;
each entry binds `agent_name`, the exact confirmed `initial_prompt`, and its own
typed `briefing_binding`. `orchestrate compile` and `verify-registration` block
until the ledger contains the matching identities and prompts and the temporary sheet is gone. After close append,
`verify-close` requires one later paired close row and a consumed close JSON.
Use forward-slash project-relative paths on Windows and Linux.

Historical per-topic `*.dispatch.json`, `material-strategy.json`,
`runtime-profile.json`, and `dispatch-ledger.jsonl` files predate this default
registrar. Treat them as migration sources, not as the active write path; do
not delete them until their dispatch and close evidence has been imported and
verified against the YAML ledger.

## Why This Is Arcana

Subagent Strategy coordinates several agents across gates, dependencies,
partial failures, human authority, durable state, and final approval. It is not
a deterministic validator or a single bounded synthesis step.
