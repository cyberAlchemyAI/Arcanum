# WORK-PACK: Deterministic Task Session Governance Runner

## Control fields

| Field | Value |
| --- | --- |
| workPackGateStatus | pass through completed `SWU-TSGR-005` receipt |
| implementationGateStatus | `SWU-TSGR-006` dependency-ready; fresh Task Session gates still required |
| complexity | high |
| outputMode | split |
| executionPackRef | [EXECUTION-PACK.md](EXECUTION-PACK.md) |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) |
| executionControlRef | [work-pack/shared/EXECUTION-CONTROL.md](work-pack/shared/EXECUTION-CONTROL.md) |
| activeLayerWindow | L1 |
| readinessProfile | proposal-to-opt-in-pilot |
| selectedSWU | `SWU-TSGR-006` |

## Objective

Update the existing Task Session sigil with a deterministic, checkpointed governance
runner that composes current controls and owner hooks without weakening the one-SWU
ceiling or absorbing implementation, Continuation Router, Invoke, or Signal Observer
authority.

## Task board

| Task | Layer | Goal | Gate | Status |
| --- | --- | --- | --- | --- |
| [TASK-TSGR-00](work-pack/tasks/TASK-TSGR-00-LIFECYCLE.md) | L0 | Sigil Development lifecycle decision | accepted receipt | complete |
| [TASK-TSGR-01](work-pack/tasks/TASK-TSGR-01-CONTRACTS.md) | L0 | evaluator and runner contracts | TSGR-000 accepted | complete |
| [TASK-TSGR-02](work-pack/tasks/TASK-TSGR-02-RUNNER.md) | L1 | controller, reconcile, application, resume | L0 complete | in progress |
| [TASK-TSGR-03](work-pack/tasks/TASK-TSGR-03-HOOKS.md) | L2 | owner hooks and continuation | L1 complete | blocked |
| [TASK-TSGR-04](work-pack/tasks/TASK-TSGR-04-OPERATIONS.md) | L3 | observation, experiment, and pilot verdict | L2 complete | blocked |

## SWU manifest

| SWU | Parent | Objective | Dependencies | Exact write scope | Validation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SWU-TSGR-000` | [TASK-TSGR-00](work-pack/tasks/TASK-TSGR-00-LIFECYCLE.md) | accept, narrow, or reject this lifecycle design | none | lifecycle receipt under this run only | Sigil Development rubric review | sigil-development/manual | accepted |
| `SWU-TSGR-001` | [TASK-TSGR-01](work-pack/tasks/TASK-TSGR-01-CONTRACTS.md) | productionize the pure governance evaluator with golden parity | TSGR-000 accepted | new evaluator, two schemas, fixture corpus, fixture validator | policy parity and negative schemas | task-session | completed |
| `SWU-TSGR-002` | [TASK-TSGR-01](work-pack/tasks/TASK-TSGR-01-CONTRACTS.md) | define the closed runner envelope family | TSGR-001 | new run, ticket, phase, executor, terminal schemas plus fixtures | schema positive/negative matrix | task-session | completed |
| `SWU-TSGR-003` | [TASK-TSGR-02](work-pack/tasks/TASK-TSGR-02-RUNNER.md) | implement deterministic `prepare` and read-only `status` | TSGR-002 | new runner script and runner fixtures/validator | repeatability, stale/tied scope, phase-order cases | task-session | completed |
| `SWU-TSGR-004` | [TASK-TSGR-02](work-pack/tasks/TASK-TSGR-02-RUNNER.md) | launch or join one structured executor and emit `execution-received` | TSGR-003 | runner script and runner fixtures/validator | argv/path/timeout/receipt-order cases | task-session | completed |
| `SWU-TSGR-005` | [TASK-TSGR-02](work-pack/tasks/TASK-TSGR-02-RUNNER.md) | reconcile writes, outputs, validation, and target classification without applying | TSGR-004 | runner script and runner fixtures/validator | target/write/output/validation matrix | task-session | completed |
| `SWU-TSGR-006` | [TASK-TSGR-02](work-pack/tasks/TASK-TSGR-02-RUNNER.md) | atomically commit admitted staged outputs and enforce terminal-final-write/resume | TSGR-005 | runner script and runner fixtures/validator | apply/idempotent-adoption and interruption matrix | task-session | selected |
| `SWU-TSGR-007` | [TASK-TSGR-03](work-pack/tasks/TASK-TSGR-03-HOOKS.md) | add the generic owner side-job protocol and versioned adapter manifest | TSGR-006 | hook manifest, two hook schemas, adapter, fixtures/validator | manifest digest, timeout, malformed receipt, bounded output, owner mismatch | task-session | blocked |
| `SWU-TSGR-008` | [TASK-TSGR-03](work-pack/tasks/TASK-TSGR-03-HOOKS.md) | invoke Continuation Router and validate its joined Invoke receipt before emitting a cursor | TSGR-007 plus external owner-readiness receipt | cursor schema, runner/hook integration, route fixtures | pass/no-op/block/unjoined and unique/ambiguous successor | task-session | blocked |
| `SWU-TSGR-009` | [TASK-TSGR-04](work-pack/tasks/TASK-TSGR-04-OPERATIONS.md) | integrate append-only Signal Observer invocation and dedupe | TSGR-008 | runner observation adapter and observation fixtures | observer append/dedupe and private-payload boundary | task-session | blocked |
| `SWU-TSGR-010` | [TASK-TSGR-04](work-pack/tasks/TASK-TSGR-04-OPERATIONS.md) | run the paired Experiment Harness and emit an opt-in pilot verdict | TSGR-009 | new experiment package only | paired-run report, acceptance equivalence, public scan, bounded verdict | experiment-harness | blocked |

Exact path inventories and closeout contracts are in each task contract and
[EXECUTION-CONTROL.md](work-pack/shared/EXECUTION-CONTROL.md).

## Execution evidence

- `SWU-TSGR-000`: accepted lifecycle receipt
  [SIGIL-DEVELOPMENT-LIFECYCLE-RECEIPT.md](SIGIL-DEVELOPMENT-LIFECYCLE-RECEIPT.md).
- `SWU-TSGR-001`: terminal Task Session receipt
  [SWU-TSGR-001-RESULT.json](work-pack/results/SWU-TSGR-001-RESULT.json), result
  `pass`, with evaluator validation `golden=25/25`, `negative=5/5`,
  `schema=4/4`, and no undeclared outputs.
- `SWU-TSGR-002`: terminal Task Session receipt
  [SWU-TSGR-002-RESULT.json](work-pack/results/SWU-TSGR-002-RESULT.json), result
  `pass`, with contract validation `positive=5/5`, `negative=14/14`,
  `semantic_negative=5/5`, `schema_contracts=5/5`, and zero undeclared outputs.
  The first canonical validator run blocked on a producer portability defect; its
  repaired bytes passed a fresh material admission and the recovered live matrix.
- `SWU-TSGR-003`: terminal Task Session receipt
  [SWU-TSGR-003-RESULT.json](work-pack/results/SWU-TSGR-003-RESULT.json), result
  `pass`, with prepare/status validation `positive=3/3`, `negative=6/6`, and
  zero undeclared outputs. Repeated prepare was byte-stable, status was read-only,
  and missing, tied, stale, skipped, and predecessor-drift cases blocked.
- `SWU-TSGR-004`: terminal Task Session receipt
  [SWU-TSGR-004-RESULT.json](work-pack/results/SWU-TSGR-004-RESULT.json), result
  `pass`, with executor-join validation `positive=6/6`, `negative=13/13`, and
  zero undeclared outputs. Structured launch, existing-receipt join, and idempotent
  replay passed; shell-vector and cwd escapes blocked; timeout and nonzero exit
  remained execution failures; identity, nonterminal receipt, and final-write drift
  remained governance failures.
- `SWU-TSGR-005`: terminal Task Session receipt
  [SWU-TSGR-005-RESULT.json](work-pack/results/SWU-TSGR-005-RESULT.json), result
  `pass`, with reconcile validation `positive=10/10`, `negative=20/20`, and
  zero undeclared outputs. Apply and exact-present targets classified without live
  writes; conflict, inventory, critical-validation, output-only re-admission,
  cardinality, and evidence-drift cases blocked.
- Returned successor: `SWU-TSGR-006`; this selection does not authorize or execute
  implementation.

## Atomicity review

Each SWU owns one independent acceptance decision: lifecycle acceptance, evaluator
parity, envelope closure, prepare/status, executor join, reconciliation, atomic
commit/resume, generic hook protocol, concrete continuation join, observation, or
experiment/pilot verdict. Shared runner files require strict sequential execution
but do not collapse those acceptance boundaries.

`SWU-TSGR-000` is the narrowest reversible first unit. The first implementation unit,
`SWU-TSGR-001`, is read-only relative to implementation targets and creates new
paths, avoiding collision with the currently dirty canonical files.

## Validation strategy

- run every existing Task Session and Continuation Router regression;
- add schema-positive and adversarial fixture matrices per SWU;
- run end-to-end cases only in synthetic temporary repositories;
- scan all public additions for consuming-project leakage;
- measure speed only in `TSGR-EXP-001`.

## Blocker board

| Blocker | State | Owner | Resolution |
| --- | --- | --- | --- |
| `TSGR-BLOCK-001` lifecycle change not accepted | resolved | sigil-development | accepted `SIGIL-DEVELOPMENT-LIFECYCLE-RECEIPT.md` |
| `TSGR-BLOCK-002` current Task Session package is dirty | guarded | each mutation SWU | exact preflight digest binding; block on unexpected overlap |
| `TSGR-BLOCK-003` stale architecture synchronization prose | deferred beyond this work pack | sigil-development | repair in a new post-pilot lifecycle package |
| `TSGR-BLOCK-004` speed unproven | deferred to TSGR-010 | experiment-harness | paired evidence; no threshold inflation |
| `TSGR-BLOCK-005` Continuation Router lacks a production launcher | blocks TSGR-008 only | continuation-router | provide the exact readiness receipt in `OWNER-READINESS.md` |

## Selection rule

Only one SWU may be selected. After each terminal receipt, Task Session must route
through Continuation Router and the exact Invoke closeout contract before returning a
cursor. A cursor never executes the next SWU.

## Completion

The work pack is complete only when all SWUs have accepted receipts, full regression
and public-boundary scans pass, and the paired experiment emits a bounded opt-in pilot
verdict. A working synthetic prototype is available at `SWU-TSGR-006`; end-to-end
closeout requires owner readiness and TSGR-008. Canonical documentation, generated
mirrors, and recommended-path promotion are intentionally outside this prototype
work pack.
