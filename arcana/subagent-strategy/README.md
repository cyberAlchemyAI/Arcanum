# Subagent Strategy

Subagent Strategy is an Arcana sigil for deciding when multi-agent work is
justified and governing it from proposal through closeout.

It preserves the reusable coordination contract behind repository-local
subagent routers without importing a consuming project's constitutions, agent
names, ledger schemas, paths, or private evidence into Arcanum.

Status: **seed**. The public contract and experiment harness exist, but live
runtime examples are still required before promotion readiness can be claimed.

## Problem It Solves

Spawning several agents is easy. Governing the work is harder. Without an
explicit strategy, a fan-out can duplicate angles, exceed the parent context,
act before human approval, lose partial failures, or finish without closing its
agents and ledger records.

This sigil supplies the portable lifecycle:

```text
trigger decision
  -> type-owner and preflight resolution
  -> persisted strategy sheet
  -> deterministic confirmation readiness
  -> tension checks on the admitted digest
  -> explicit human confirmation
  -> registration
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
- dispatch and close events must be registered in an append-only ledger.

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
- paired dispatch and close events,
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
3. Draft and persist groups, agents, angles, expected outputs, dependencies,
   final approval, and every field required by the current local form owner.
4. Run the form owner's non-mutating confirmation-readiness validator against
   the exact persisted sheet.
5. Warn and rematerialize before confirmation when a runtime or schema
   projection is stale; block all other form-admission errors.
6. Run two independent tension checks against the admitted sheet digest.
7. Present the complete admitted sheet and artifact destination to the human.
8. Freeze only after explicit confirmation.
9. Register before spawning any working group.
10. Run a consuming group only when blocking dependencies are complete and the
    type owner's declared handoff-readiness criteria pass for the exact upstream
    artifacts.
11. Route `needs_feedback` gaps through declared feedback or revision edges
    while loop capacity remains; preserve `blocked` gaps for final approval.
12. Propagate partial and failed results downstream.
13. Join and close every agent, report the exit reason, and append the close
    event.
14. Update configured result and observability hooks.

## Artifacts

- [SKILL.md](SKILL.md) is the executable behavior contract.
- [templates/runtime-profile.md](templates/runtime-profile.md) defines portable
  repository bindings.
- [templates/usage-telemetry.md](templates/usage-telemetry.md) defines the
  behavior signals used for later reflection.
- `development/` contains the Experiment Harness and promotion evidence.

## Why This Is Arcana

Subagent Strategy coordinates several agents across gates, dependencies,
partial failures, human authority, durable state, and final approval. It is not
a deterministic validator or a single bounded synthesis step.
