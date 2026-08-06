# TASK-SRG-CONSUMER — Selected-unit live admission

## Smallest Working Units

### SWU-SRG-005 — Selection schemas

- Primary behavior: define non-mutating selection request/receipt contracts.
- Dependencies: SWU-SRG-004.
- Write scope: audit-owned selection request/receipt schemas and examples.
- Done: exactly one task/SWU, epoch, unit digest, explicit confirmation, dependencies, lifecycle eligibility, authority none, mutation ready false.
- Split analysis: request and receipt are two sides of one verifier contract and cannot be reviewed independently.
- Verification: schema positive/negative examples.
- Owner: Spellcraft lifecycle worker.

### SWU-SRG-006 — Plan-epoch selection verifier

- Primary behavior: recompute current selected-unit semantics and issue a selection receipt only when the epoch and current eligibility agree.
- Dependencies: SWU-SRG-005.
- Algorithm: validate request; read manifest; verify zero authority; resolve current selectors through the audit-owned normalizer; compare unit/component digests; verify ready-frontier membership; verify current lifecycle state and dependency receipts; bind explicit confirmation; emit non-mutating receipt.
- Write scope: audit-owned verifier, tests, and Task Session owner-hook registration if required.
- Done: exact case passes; wrong/ineligible/stale/dependency-incomplete cases block with stable codes.
- Split analysis: digest and eligibility checks must be atomic because either alone can select an unsafe unit.
- Verification: selection verifier fixture matrix.
- Owner: Spellcraft lifecycle worker with Task Session consumer review.

### SWU-SRG-007 — Material identity and baseline schemas

- Primary behavior: require selection identity and live baseline inputs throughout material admission.
- Dependencies: SWU-SRG-006.
- Write scope: Task Session mutation request/receipt, execution-ticket, terminal-receipt, and producer material schemas.
- Done: task, SWU, epoch, unit digest, selection receipt, attempt, target baselines, complete validation digest, owner, authority, and publication are required and consistent.
- Split analysis: schema fields are one cross-artifact identity chain; verifier behavior remains 008.
- Verification: schema chain positive/negative examples.
- Owner: Sigil Development lifecycle worker.

### SWU-SRG-008 — Single-use live admission enforcement

- Primary behavior: prevent mutation unless current targets and all bound identities match one unused admission receipt.
- Dependencies: SWU-SRG-007.
- Algorithm: validate selection receipt; compare identities across request/package/producer receipt; hash live targets against baselines immediately before first write; compare full validation digest; bind attempt/non-replay state; issue admit receipt; require its digest on mutating execution ticket; repeat digest in terminal receipt.
- Write scope: Task Session readiness verifier, governance runner/adapter gates, and their fixtures.
- Failure modes: replay, cross-unit package, target TOCTOU, missing adapter receipt, changed validation contract, wrong attempt.
- Done: all negative cases block before mutation; exact case admits once.
- Split analysis: issuing and consuming the receipt are one safety behavior; separating them would permit an unused gate.
- Verification: Task Session mutation-admission and governance-runner suites.
- Owner: Sigil Development lifecycle worker.

## Closeout

Use the Work Pack closeout contract. Unique successors: 005→006→007→008→009.
