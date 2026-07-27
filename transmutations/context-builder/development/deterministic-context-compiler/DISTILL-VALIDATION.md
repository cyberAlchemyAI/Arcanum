# Plan Distill Validation

## Intent And Budget

- Intent: reduce the medium-complexity plan into serial, independently
  reviewable SWUs without losing the end-to-end compiler contract.
- Budget: Standard
- Role execution: local Proposer/Balancer simulation
- Delegation: none; repository policy requires user confirmation and the plan
  did not need parallel agents
- Selection authority: none

## Proposer Pass

The proposed first unit was:

> Freeze the typed request and receipt schemas and prove invalid shape,
> duplicate IDs, and escaping paths fail before compiler or cache writes.

This is smaller and more reversible than implementing snapshot, cache, or
renderer behavior.

## Balancer Pass

| Pressure | Objection | Disposition |
| --- | --- | --- |
| coherence | schema files alone do not prove a usable boundary | retain validator and negative fixtures in SWU-DCC-001 |
| scope | a complete compiler would be task-shaped | split exact compile, selection, rendering, measurement, reuse, evidence, and integration |
| evidence | token reduction is not proved by deterministic bytes | defer the claim to paired runtime receipts |
| authority | canonical integration cannot share the first implementation unit | isolate it in lifecycle-owned SWU-DCC-008 |
| concurrency | shared compiler and receipt files make parallel mutation unsafe | use serial waves and a fresh W0 baseline per unit |
| closure | source mutation alone can leave work-pack state stale | require terminal and owner receipts for every SWU |

## Atomicity Result

Eight mutation SWUs remain. Each owns one primary behavior:

1. structural validation;
2. exact single-selector compile;
3. deduplication and covering-set selection;
4. output parity and one-payload handoff;
5. evidence-separated measurement;
6. safe cache and delta reuse;
7. paired reusable-behavior evidence;
8. canonical lifecycle integration.

Each task file records plausible child units and why its retained acceptance
boundary cannot be split without losing semantic closure.

## Narrow-First Result

- First candidate: SWU-DCC-001
- Reversible: yes; it adds bounded schemas, validator, and sanitized fixtures
- Trust gained: malformed or escaping inputs fail before deeper writes
- Deferred: compiler, cache, selection, runtime adapter, measurements, and
  canonical docs
- Selected: no
- Verdict: pass

## Recomposition Proof

[TRACEABILITY.md](work-pack/shared/TRACEABILITY.md) maps every FR and
architecture rule to at least one SWU and witness. The ordered graph preserves:

```text
contract
  -> exact source binding
  -> coverage-preserving selection
  -> format/runtime parity
  -> honest measurement
  -> safe reuse
  -> paired evidence
  -> lifecycle-owned integration
```

Removing any unit leaves a named requirement or promotion boundary unproved.
No hidden glue is required beyond the versioned files declared in exact write
scopes.

## Deferred Complexity

- selector languages beyond exact Markdown headings and whole short files;
- exact optimization claims;
- multiple tokenizer plugins;
- provider-specific prompt caches;
- cache cleanup and retention automation;
- consumer-specific adapters and mirrors;
- registry release, publication, deployment, and production readiness.

Each item has an owner or a later route and is not silently pulled into L0.

## Cycle And Premortem Checks

- Recursive split rounds: 2
- Cycle guard: no SWU was re-expanded into its parent task
- Highest-risk failures: stale cache acceptance, false token precision,
  coverage loss, and canonical mutation before live evidence
- Negative proof: each risk maps to a blocker fixture or lifecycle gate

## Verdict

- Status: pass
- Blocking planning gaps: none
- Mutation authorization: none
- Evidence ceiling: Plan structure and recomposition only
- Next owner: Sigil Development
