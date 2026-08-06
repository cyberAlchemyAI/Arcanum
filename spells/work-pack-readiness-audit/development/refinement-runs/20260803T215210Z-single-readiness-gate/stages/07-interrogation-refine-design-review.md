# Stage 07 — Interrogation refine-design-review

## Independent review

The approved `admission-boundary-critic` returned `block` against the initial whole-file receipt design. Its normalized receipt is `stages/07-admission-boundary-critic.json`.

## Blocking questions and answers

1. **Can Task Session prove it is executing the audited contract?**
   - Initial answer: no.
   - Required repair: a versioned plan epoch with per-unit semantic digest, consumed by Task Session.
2. **Can the epoch survive normal closeout updates?**
   - Initial answer: no for whole-file hashes.
   - Required repair: normalized selector-value digests for immutable semantics; mutable lifecycle/status receipts outside the digest.
3. **Can material for another SWU be replayed?**
   - Initial answer: possibly.
   - Required repair: bind task ID, SWU ID, plan epoch ID, unit-contract digest, and attempt ID through package, producer receipt, admission request, and receipt.
4. **Can targets change after material validation?**
   - Initial answer: the current verifier does not compare live targets to exact producer baselines.
   - Required repair: per-target baseline hashes rechecked immediately before the first write, plus single-use receipt/attempt binding.
5. **Does the Task Session validation command equal the audited command contract?**
   - Initial answer: strings omit cwd, environment, timeout, exit code, runtime identity, and risk.
   - Required repair: per-unit digest over the full normalized command, writes, attempts, receipts, closeout, owner, authority, and publication contract.
6. **Does explicit selection prove current eligibility?**
   - Initial answer: not against both audited frontier and current lifecycle/dependency receipts.
   - Required repair: a non-mutating selection receipt binding one unit, plan epoch, unit digest, current dependency receipts, lifecycle eligibility, and explicit confirmation.
7. **Can an executor bypass admission?**
   - Initial answer: a direct adapter could unless the contract requires the receipt.
   - Required repair: every mutating execution ticket and terminal receipt binds the single-use admission-receipt digest.

## Verdict

`block` for the initial design. The review is accepted in full and routed to Distill Repair; no objection is dismissed.
