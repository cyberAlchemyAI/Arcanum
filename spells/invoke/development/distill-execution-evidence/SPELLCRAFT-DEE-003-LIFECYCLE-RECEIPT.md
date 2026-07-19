# Spellcraft Lifecycle Receipt: SWU-DEE-003

## Identity

- Spellcraft mode: `validate`
- Spell: `invoke`
- Canonical ID: `invoke`
- Alias used: none
- Scope: library
- Source lifecycle receipt: `SPELLCRAFT-LIFECYCLE-RECEIPT.md`
- Source SWU: `SWU-DEE-003`
- Decision: **accept with bounded narrowing**
- Lifecycle status: resolved

## Accepted Responsibility

`SWU-DEE-003` owns one versioned Invoke-side runtime-event grammar and one deterministic
append/resolve boundary for Distill role evidence. It represents both true-subagent and labeled
role-simulation paths with the same Proposer/Balancer trace contract.

This is an Invoke spell integration contract. It does not change the Distill sigil's
runtime-role policy, and Task Session must not mutate `arcana/distill/` or any generated Distill
runtime package under this receipt.

## Accepted Event And Sequence Contract

Every event carries an event identity, Distill run identity, monotonic sequence, event type,
execution path, role when role-scoped, invocation reference policy, exact payload reference, and
emission timestamp.

The resolver must enforce these path-independent boundaries:

1. one capability probe opens the sequence;
2. one Proposer pass starts and completes before one Balancer pass starts and completes;
3. reconciliation follows both role results;
4. termination closes the sequence;
5. event identities and sequence numbers are unique and append ordered;
6. all events share one run identity and execution path.

For `true_subagent`, Proposer and Balancer require distinct non-empty native invocation
references. For `role_simulation`, both roles require a null invocation reference; a simulated
native identity blocks resolution. Both paths must preserve Proposer claims, Balancer objections,
and reconciliation evidence through exact payload references.

## Authority Boundary

- An event, event sequence, schema pass, or resolver pass is runtime evidence, not a verdict.
- The resolver may return sequence diagnostics and resolved role handles only.
- It must not set `mutation_handoff_allowed` or synthesize `DistillValidationResult`.
- Semantic objection/reconciliation checks, cross-artifact provenance, and handoff authority
  remain owned by later validator SWUs.
- This unit does not select a repository-wide event service, database, queue, or transport.
  JSONL files are the bounded append-only interchange and fixture form for this layer.

## SWU-DEE-003 Binding

Canonical lifecycle owner: `invoke` through Spellcraft.

Execution owner: Task Session, one SWU only.

Exact implementation write scope:

- `arcanum/spells/invoke/schemas/distill-runtime-event.schema.json`
- `arcanum/spells/invoke/development/distill_runtime_events.py`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/valid-runtime-events-true-subagents.jsonl`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/valid-runtime-events-role-simulation.jsonl`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/invalid-runtime-events-same-invocation.jsonl`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/invalid-runtime-events-missing-boundary.jsonl`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/invalid-runtime-events-out-of-order.jsonl`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/invalid-runtime-events-simulated-native-id.jsonl`
- `arcanum/spells/invoke/development/run-distill-runtime-event-fixtures.sh`

Task Session governance and completion-evidence scope:

- `arcanum/spells/invoke/development/distill-execution-evidence/SPELLCRAFT-DEE-003-LIFECYCLE-RECEIPT.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/WORK-PACK.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/tasks/TASK-DEE-02-EVIDENCE-SUBSTRATE.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/results/SWU-DEE-003-RESULT.md`

The governance scope may record only this bounded implementation and deterministic evidence.
Central observability remains deferred until its parent-repository ledger paths receive separate
write authorization.

## Acceptance Conditions

- the event schema has an explicit version and rejects missing identity, sequence, path, role,
  payload-reference, or timestamp obligations;
- the append operation refuses duplicate event IDs, non-monotonic sequences, run/path changes,
  and any attempt to rewrite existing ledger bytes;
- valid true-subagent and role-simulation sequences resolve to the same role-boundary shape;
- same invocation identities across true subagents block;
- missing role boundaries and invalid ordering block;
- simulated native invocation identities block;
- the resolver is deterministic and uses no model call;
- resolver output explicitly disclaims verdict and mutation authority;
- the focused event fixture report becomes the reusable Experiment Harness evidence for this
  structural runtime behavior;
- promotion remains blocked until `SWU-DEE-004` through `SWU-DEE-010` produce semantic,
  provenance, mode, and adversarial evidence.

## Rejected Alternatives

- changing the Distill sigil contract inside this Invoke SWU;
- separate schemas for true-subagent and role-simulation paths;
- treating native invocation IDs as mandatory for simulation;
- selecting a repository-wide event store before concrete runtime pressure exists;
- allowing an event or resolver result to authorize mutation;
- combining semantic validation or mode integration into this unit.

## Validation And Observability

- `SWU-DEE-002` completion evidence: `work-pack/results/SWU-DEE-002-RESULT.md`.
- `SWU-DEE-003` completion evidence: `work-pack/results/SWU-DEE-003-RESULT.md`.
- Existing Invoke Experiment Harness: focused DEE-003 event behavior passed 21 deterministic
  checks covering both execution paths, authority limits, malformed events, append protection,
  and full-ledger round trip.
- Observability: this receipt is the durable lifecycle-selection record. Central append is
  deferred by the explicit governance scope above.

## Next Route

`spellcraft` must bind the canonical semantic-validator owner and exact write paths for
`SWU-DEE-004`. `SWU-DEE-004` through `SWU-DEE-013` remain blocked and unselected.
