# Sigil Development Material Producer Handoff

## Route

- Capability: `sigil-development`
- Mode: `update`
- Target sigil: `task-session`
- Unit: `SWU-TSGR-001`
- Lifecycle decision: already accepted by `SWU-TSGR-000`
- Authority ceiling: staged material and producer receipt only

## Objective

Stage the exact five files for the pure governance evaluator without writing their
canonical targets. Emit a closed producer receipt and its exact JSON Schema so a
later `apply-approved` Invoke material package can bind those bytes.

## Exact canonical target inventory

1. `arcanum/arcana/task-session/scripts/evaluate-governance.py`
2. `arcanum/arcana/task-session/schemas/governance-evaluation-request.schema.json`
3. `arcanum/arcana/task-session/schemas/governance-evaluation-receipt.schema.json`
4. `arcanum/arcana/task-session/development/fixtures/governance-evaluation-cases.json`
5. `arcanum/arcana/task-session/development/validate-governance-evaluator.py`

All targets are absent at handoff time.

## Producer output scope

Write only beneath:

`producer/`

Required outputs:

- `producer/staged/` with a repository-relative mirror of the five canonical paths;
- `producer/material-producer-receipt.schema.json`;
- `producer/material-producer-receipt.json`;
- `producer/VALIDATION.md`.

The receipt must bind every staged output by Arcanum-root-relative canonical target
path, parent-repository-relative staged path, SHA-256, size, operation `create`,
lifecycle owner `sigil-development`, target sigil `task-session`, selection/review
owner `task-session`, authority class `public`, and publication class `public`. It
must also bind every controlling source artifact by path, digest, size, and role.

## Behavior contract

- The production CLI consumes a versioned JSON request and the canonical
  `decision-validation-policy.json`.
- The request binds request ID, evaluation kind, policy digest, exact input, and
  named receipt output.
- The evaluator is pure except for the explicitly named receipt output.
- Allowed terminal outcomes remain kind-constrained: `PROCEED`, `PASS`, `NO_OP`,
  `FLAG`, or `BLOCK`.
- All current decision-policy fixtures receive golden-parity coverage.
- Malformed request, stale policy digest, unknown kind, and invalid outcome block.
- Existing development-only evaluator logic is identified as future
  removal/delegation residue; it is not silently declared a second authority.

## Validation contract

The staged validator must be runnable against the staged tree without copying bytes
into canonical targets. It must cover:

- JSON Schema validation for request and receipt;
- golden parity for all current decision-policy fixtures;
- malformed request;
- stale policy digest;
- unknown evaluation kind;
- invalid evaluator outcome;
- refusal to write any undeclared output.

After a later admitted canonical apply, the material package must retain:

```text
python3 arcana/task-session/development/validate-governance-evaluator.py
python3 arcana/task-session/development/validate-decision-validation-policy.py
```

## Owner and dirty-state constraints

- Do not modify existing dirty canonical Task Session files.
- Do not modify any canonical implementation target during this producer pass.
- Do not generate or edit `.agents/skills`.
- Do not claim apply approval, mutation admission, implementation completion,
  promotion, publication, or production readiness.
- Do not continue to `SWU-TSGR-002`.

## Required return receipt

Return the producer receipt path and digest, schema path and digest, staged output
digests, validation commands/results, exact residual duplication, and a
`mutation_ready: false` statement. Use the full Sigil Development runtime-evidence
shape, record Experiment Harness as `not_run`, and return the receipt through Task
Session review before any SWU-completion claim. The later material-packaging owner
is Invoke `refresh` in `apply-approved` mode, contingent on exact scoped approval.
