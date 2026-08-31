# Distill v2 Machine Contract — Validation Strategy

## Global Phases

| Phase | Purpose | Rule |
| --- | --- | --- |
| pre-execution | Rehash source anchors, accepted decision graph, target baselines, schemas, runner identities, and predecessor receipts. | Any mismatch blocks before writes. |
| post-produce | Validate staged syntax, schema closure, instances, semantic invariants, negative fixtures, determinism, and real consumer behavior. | Create targets may be absent before their SWU; canonical publication waits for the complete staged denominator. |
| closeout | Verify exact changed inventory, no partial files, generated parity when in scope, terminal receipt, and one deterministic successor. | Preserve every command status; return the first nonzero status with the complete blocker set. |

## Command Families

- `python3 -m json.tool <exact-json>` for JSON syntax.
- `Draft202012Validator.check_schema` and repository-local `$ref` resolution over all eight schemas.
- The future canonical `run-distill-v2-schema-fixtures` runner for instance matrices.
- The future canonical `run-distill-v2-semantic-fixtures` runner for cross-artifact invariants.
- `python3 -m unittest` for finalizer, renderer, atomic publication, compatibility, and consumer tests.
- Selective Distill generated-package preview first; `--apply` only in SWU-DV2-013 after canonical PASS and separate authorization.
- `git diff --check -- <exact allowlist>` plus explicit checks for untracked/create targets.

## Required Positive Matrix

1. Standard complete machine bundle through schema and semantic validation.
2. Compact run with declared technique skips.
3. Tournament three-track convergence and no-winner human-gate case.
4. Deep bounded multi-track/multi-round run with premortem.
5. Validate Balancer-led review with and without Proposer repair.
6. Direct no-effect production and versioned Invoke projection of the same semantic result.

## Negative Denominator

The complete denominator must reject at least:

- missing seed, target context, objective, output artifact, optimization goal, or discovery baseline;
- absolute, traversal, URI, stale digest, or wrong `size_bytes` artifact refs;
- unknown or hyphenated canonical technique ID;
- embedded/drifted mode or technique definition inside a profile;
- unbounded, zero, or over-maximum tracks/rounds and an override that removes cycle guards;
- technique at a forbidden hook, missing required technique, invalid skip, or non-applicable technique activation;
- mixed run identity, non-monotonic sequence, broken predecessor, excess track/round event;
- result that erases an objection/tension, invents a selected unit, or contradicts trace termination;
- `block` routed to implementation/task-session, `pass` with null selected unit, or unnamed `flag` effect;
- runtime evidence changing the substantive verdict;
- nondeterministic Markdown, hidden semantics in Markdown, or receipt/artifact digest mismatch;
- partial publication, stale target overwrite, adapter substitution, or a schema-only substitute reported as a real consumer PASS;
- old adapter input made unreadable without a selected compatibility decision;
- generated mirror drift or public output containing private source/path/prose.

## Determinism And Atomicity

- Two finalizations of one accepted candidate in isolated temporary directories
  must produce byte-identical JSON, JSONL, Markdown, and receipt outputs.
- A mutation injected before every validation/publication boundary must leave the
  previous canonical family byte-identical and publish no candidate residue.
- The receipt digest algorithm must explicitly exclude or canonicalize its own
  digest field; a self-referential hash is forbidden.

## Final Laboratory Proof

A generic public fixture runs raw intent → direct source normalization → exact
mode/profile/technique resolution → semantic candidate validation → deterministic
finalization → direct consumer → Invoke v2 projection rehearsal → runtime/telemetry
projection → deterministic docs/native preview. It performs no owner request,
implementation execution, publication, deployment, or external effect.
