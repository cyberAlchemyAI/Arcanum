# Work Pack Readiness Audit

## Identity

- Canonical ID: `work-pack-readiness-audit`
- Aliases: `frontier-readiness-audit`, `work-pack-dry-run`
- Scope: library
- Lifecycle owner: `spellcraft`

## Purpose

Work Pack Readiness Audit captures one immutable planning frontier and proves
whether every declared unit can cross its stated execution, validation,
receipt, closeout, and successor boundaries without inventing missing
contracts.

The spell is audit-only. A passing result does not select a unit, authorize a
Task Session, execute target work, apply an Invoke Refresh, promote an
artifact, publish, deploy, or release.

## Use When

- an Invoke-authored work pack claims it is ready for explicit selection;
- a dry run is needed for every SWU and closure task before execution;
- task prose must be reconciled with the current Task Session admission
  contract;
- terminal receipt semantics or closeout ownership may be fail-open;
- new evidence should become an exact Invoke Refresh signal pack.

## Do Not Use When

- one already-selected bounded unit should execute; use `task-session`;
- rough intent still needs layering or blocker decisions; use
  `implementation-readiness`;
- an execution chain should continue until a blocker; use
  `task-session-until-blocker`;
- the caller wants this spell to mutate the audited plan. Route the emitted
  signal pack to `invoke:refresh`.

## Required Capabilities

| Capability | Role |
| --- | --- |
| `context-builder` | Bind the exact work pack, unit contracts, schemas, source selectors, and runtime contracts into the captured audit frontier. |
| `task-session` | Supply the current mutation-admission contract being tested. The spell does not execute it. |
| `signal-observer` | Record the audit verdict, blocker classes, evidence references, and next-owner route. |
| `experiment-harness` | Prove the reusable spell against realistic and adversarial fixtures before registry admission. |

## Optional Capabilities

| Capability | Use |
| --- | --- |
| `decision-gate` | Route a real blocker-level choice discovered by the audit; never infer a choice from missing evidence. |
| `invoke` | Consume the proposal-only refresh signal pack after the audit returns. Invoke remains the refresh owner. |

## Input Contract

The deterministic runner consumes a JSON audit configuration validated by
[`audit-config.schema.json`](schemas/audit-config.schema.json).

The configuration must bind:

- repository-relative exact references for the work pack and every controlling
  artifact;
- the live Task Session mutation-admission request schema;
- the terminal receipt schema and, when one exists, its semantic validator;
- every numeric SWU and closure task as a normalized unit;
- exact argv vectors, cwd, expected exit code, timeout, environment contract,
  runtime identity policy, and command risk class;
- material writes, execution outputs, allowed writes, and immutable paths;
- dependency and successor edges;
- attempt identity, collision policy, retention policy, and success/failure
  teardown for attempt-producing units;
- exact terminal and closeout receipt paths;
- an exact handoff-state projection whose selection status, selected unit, and
  next route must agree with the work-pack gate;
- authority and publication class;
- the only permitted next owner for refresh signals.

Paths are normalized relative paths. Absolute paths, traversal, unresolved
globs or environment variables, and symlink escape block the audit. The runner
never executes configured commands.

For Work-Pack-bound automatic routes, the admitted effect class is exactly
`repository-local-reversible`. A closeout-only boundary is carried by its
owner mode, exact target/write scope, closeout contract, and receipt; appending
`closeout-only` or another purpose label to the effect token is schema-invalid.

## Shared State

| State | Produced By | Consumed By |
| --- | --- | --- |
| immutable source snapshot | capture phase | every later phase and final drift check |
| normalized unit graph | graph phase | contract, frontier, and closeout phases |
| task-class admission matrix | runtime phase | verdict and refresh signals |
| receipt adversary result | receipt phase | verdict and schema repair signals |
| deterministic frontier simulation | simulation phase | selection-readiness verdict |
| blocker ledger | all phases | report, observability, Invoke refresh pack |
| refresh signal pack | verdict phase | `invoke:refresh` only |

## Phase Contract

### Phase 1 — Capture The Immutable Frontier

- Input: audit configuration and exact artifact references.
- Output: normalized paths, SHA-256/size snapshot, authority boundary.
- Gate: every reference resolves inside the repository, matches its declared
  digest and size, and contains no symlink or path escape.
- Failure: `block`; unsupported or drifting inputs are never partially audited.

### Phase 2 — Normalize Units And Graph

- Input: captured work pack and normalized unit declarations.
- Output: complete unit set, dependency graph, successor graph, closure
  insertion points, current ready frontier.
- Gate: unique IDs, all dependencies and successors in scope, acyclic graph,
  no unreachable units, exactly one deterministic ready root when work is
  unstarted, and no closure row without a full task contract.
- Failure: `block`; do not infer a missing unit, dependency, or selector.

### Phase 3 — Validate Execution Contracts

- Input: normalized units.
- Output: per-unit command, path, write, attempt, and teardown findings.
- Gate:
  - commands are argv arrays rather than shell prose;
  - cwd stays inside the repository;
  - runtime identity policy, environment, timeout, risk, and expected exit are
    explicit;
  - `materialWrites ∪ executionOutputs = allowedWrites`;
  - material and execution paths do not overlap;
  - immutable paths are not writable;
  - cross-unit overlapping writes have one explicit owner;
  - attempt IDs are deterministic and collision-safe;
  - success and failure teardown are both declared.
- Failure: `block` the affected unit and all of its successors.

### Phase 4 — Reconcile Current Runtime Admission

- Input: task class, requested execution mode, live Task Session request
  schema, and optional material-package evidence.
- Output: separate plan-contract and runtime-admission verdicts.
- Gate:
  - material mutation has current exact material-package and receipt evidence;
  - output-only and audit-only units use an execution mode that truthfully
    admits their writes;
  - no placeholder material write is invented to satisfy a schema;
  - dependency receipts, when required by completed dependencies, match unit,
    step, work-pack snapshot, status, digest, and owner.
- Failure: `block` runtime admission without lowering an otherwise complete
  plan-contract result.

### Phase 5 — Challenge Terminal Receipt Semantics

- Input: terminal receipt schema, unit/step map, and optional semantic
  validator.
- Output: named adversarial probe results.
- Gate: reject at least pass/not-run, pass-with-blockers, empty pass evidence,
  block/pass-validation, wrong unit/step, malformed hashes, nested unknown
  fields, and inconsistent successor claims.
- Failure: `block` closeout readiness and emit a schema-owner repair signal.

### Phase 6 — Simulate Frontier And Closeout

- Input: graph, admission matrix, expected receipts, and attempt contracts.
- Output: deterministic per-unit readiness, inherited blockers, closeout
  sequence, and terminal state.
- Gate: every pass advances to exactly one declared successor; every block
  stops; receipts are append-only and cannot be substituted by unrelated
  evidence; the handoff artifact cannot expose a ready route while the work
  pack is blocked.
- Failure: `block`; no unit is selected or executed.

### Phase 7 — Recheck Snapshot And Emit Verdict

- Input: initial snapshot and accumulated findings.
- Output:
  - `work-pack-readiness-report.json`;
  - `WORK-PACK-READINESS-REPORT.md`;
  - `REFRESH-SIGNAL-PACK.json`.
- Gate: every captured input still matches the initial digest and size.
- Failure: `block` with `snapshot-drift`; discard any earlier pass inference.

The refresh pack is always proposal-only:

- `authority_effect: none`;
- `mutation_ready: false`;
- `mutation_mode: proposal-only`;
- exact evidence and target paths for every signal;
- `next_owner: invoke:refresh`.

### Phase 8 — Observe

- Input: final report, blocker ledger, and output digests.
- Output: one Signal Observer envelope or an explicit observability residue.
- Gate: telemetry never changes the audit verdict.
- Failure: preserve the report and flag observability residue.

## Verdicts

| Verdict | Meaning |
| --- | --- |
| `pass` | The captured frontier is structurally, contractually, semantically, and currently runtime-admissible. No unit is selected. |
| `flag` | The audit is complete and only named noncritical residue remains. |
| `block` | At least one acceptance-critical graph, contract, runtime, receipt, closeout, snapshot, or authority condition fails. |

The report always keeps `plan_contract_status` separate from
`runtime_admission_status`.

For the explicit v2 `selected-unit-at-task-session` profile, `pass` means the
semantic plan is ready for selection, not that runtime mutation is ready. That
profile always reports `runtime_admission_status: pending-selection`,
`selected_unit: null`, `mutation_ready: false`, and
`next_owner: task-session:selection` until Task Session issues a separate live
admission receipt.

## Failure Policy

- Fail closed on unsupported formats, missing refs, unsafe paths, snapshot
  drift, ambiguous frontier, or authority escalation.
- Never repair target files inside the audit.
- Never execute configured validation commands.
- Never turn output-only work into a fake material mutation.
- Never claim that a schema-valid receipt is semantically valid without the
  named adversarial probes or semantic validator.
- Route exact repair signals to their lifecycle owner.

## Public/Private Boundary

This public spell contains only generic contracts and synthetic fixtures.
Project names, private paths, private prose, source excerpts, and project
specific expected values belong only in consuming-repository configurations
and run evidence.

## Observability

Record:

- canonical spell ID and version;
- input snapshot digest and drift result;
- total units and task-class counts;
- plan-contract and runtime-admission status;
- blocker counts by graph, command, path, write algebra, runtime admission,
  receipt semantics, attempt lifecycle, closeout, snapshot, and authority;
- refresh signal count and next owner;
- output paths and digests;
- explicit `selected_unit: none`, `authority_effect: none`, and
  `mutation_ready: false`.

## Output Contract

Return:

```markdown
## Work Pack Readiness Audit

- Canonical ID: work-pack-readiness-audit
- Verdict: pass | flag | block
- Snapshot: <digest and drift result>
- Units: <count by class>
- Plan contract: pass | flag | block
- Runtime admission: pass | flag | block
- Receipt semantics: pass | block
- Ready frontier: <unit | none | ambiguous>
- Selected unit: none
- Outputs: <report JSON, report Markdown, refresh signal pack>
- Authority effect: none
- Mutation ready: false
- Blockers: <counts and exact IDs>
- Next owner: invoke:refresh | task-session selection | deferred
```

## Deterministic Runner

```bash
python3 scripts/audit_work_pack.py \
  --config <audit-config.json> \
  --output-dir <empty-or-new-run-directory>
```

The runner validates the config and generated report against this spell's
schemas. It only reads the repository and writes the three output artifacts to
the caller-selected output directory.

## Additive v2 objective-execution projection

Version `2.0.0` is additive. The v1 audit configuration, report, refresh pack,
CLI, and fixtures remain supported unchanged. A v2 configuration is selected
only by `"schema_version": "2.0.0"` and uses:

- [`audit-config-v2.schema.json`](schemas/audit-config-v2.schema.json);
- [`objective-execution-manifest.schema.json`](schemas/objective-execution-manifest.schema.json);
- [`audit-report-v2.schema.json`](schemas/audit-report-v2.schema.json).

The v2 runner freezes exact artifact and JSON Pointer bindings, preserves
independently owned status receipts, verifies the material package tuple,
byte baselines, write algebra, unique canonical successor, receipt semantics,
closeout policy, risk policy, and run budget, then computes per-category
semantic digests and one deterministic projection digest.

A passing projection has:

- evidence ceiling `frozen-input-contractual-readiness`;
- `authority_effect: none`;
- `selected_unit: null`;
- `mutation_ready: false`;
- epoch approval status `unapproved`.

It is therefore input to Decision Gate approval, not approval itself. The
runner never executes configured commands. Missing bindings produce stable
pre-route codes; owner, material, validation, receipt, and closeout semantic
changes invalidate only through their named category. Equivalent regeneration
preserves the digest and may be proven with `compare_manifests_v2`.

The only flag class the v2 public contract admits is
`observability-residue`. All other gaps block and expose no manifest to a
chain consumer. Compensation is either `none` with a rationale or an explicit
owner-routed contract; the audit never invents rollback.

### Plan-once selected-unit admission

Set `"admission_timing": "selected-unit-at-task-session"` only when material
packages are intentionally produced after planning. Absence of this field, or
`full-frontier`, retains the strict v2 behavior and its missing-material
blockers.

The opt-in profile:

- requires task/SWU identity and complete structured validation contracts for
  every unit;
- resolves each declared JSON Pointer and hashes the normalized selected value,
  closed component payloads, and per-unit contracts;
- keeps whole-file hashes and the source snapshot as provenance, outside the
  plan epoch;
- excludes material-package bytes, target baselines, and mutable lifecycle or
  closeout receipts from the epoch;
- emits `plan-semantic-manifest.json` and `selection-handoff.json` instead of
  the strict Objective Execution Manifest;
- treats absent future material as pending selection, not as an Invoke Refresh
  defect.

`scripts/verify_plan_selection.py` then re-resolves the current semantic
selectors, requires exact task/SWU membership, complete dependency receipts,
current lifecycle eligibility, and explicit confirmation, and emits a
non-authoritative selection receipt. A semantic value or normalizer change
blocks selection and requires Refresh plus readiness re-audit. A status-only
or package-production change does not.
