# Stage 08 — Distill Repair

## Repair objective

Convert every independent-review blocker into a closed contract invariant without reintroducing the pre-execution Refresh/re-audit loop.

## Repair matrix

| Finding | Accepted repair | Planned falsification |
| --- | --- | --- |
| ABC-001 | Task Session consumes the plan epoch and recomputes the selected unit semantic digest. | change any immutable semantic selector after audit; selection blocks |
| ABC-002 | Semantic identity uses normalized selected values; lifecycle/status receipt bytes are separate. | status-only closeout preserves digest; graph/command change invalidates it |
| ABC-003 | Package, producer receipt, request, and receipt bind task, SWU, epoch, unit digest, and attempt. | cross-SWU and cross-epoch packages block |
| ABC-004 | Material contract carries exact target baselines; Task Session rehashes immediately before first write. | mutate one target after production; admission blocks |
| ABC-005 | Unit digest includes the full normalized command, writes, attempts, validation, receipts, closeout, owner, authority, and publication contract. | change cwd, environment, timeout, risk, or receipt schema; block |
| ABC-006 | Non-mutating selection receipt binds one audited-ready unit and current dependency/lifecycle evidence. | select blocked, complete, wrong, or dependency-incomplete unit; block |
| ABC-007 | Plan-once missing material is `pending-selection`; only real plan defects emit Refresh signals. | null package passes plan scope and produces no repair signal |
| ABC-008 | Every mutating execution ticket requires a single-use admission receipt digest; terminal receipt repeats it. | adapter invocation without current receipt blocks |

## Canonicalization decision

The audit owner must own one deterministic semantic normalizer and selected-unit verifier. Task Session calls the verifier and consumes its receipt; it must not duplicate the digest algorithm. Artifact byte hashes remain provenance, while normalized selector-value hashes define plan equivalence.

## Selection and lifecycle rule

A selection receipt passes only when exactly one explicitly chosen unit:

- exists in the plan epoch;
- has the expected unit-contract digest;
- is eligible under the current lifecycle status binding;
- has all current dependency receipts in a passing terminal state;
- is not complete, blocked, claimed elsewhere, or outside the ready frontier;
- carries no mutation authority.

## Toy-game outcomes

These are designed expectations, not executed fixtures:

| Case | Expected result |
| --- | --- |
| unchanged semantics + status-only closeout | epoch preserved |
| unchanged plan + newly produced selected material | no re-audit; continue to live admission |
| changed command cwd | stale plan; block before material |
| package for sibling SWU | identity mismatch; block |
| target changed after producer receipt | baseline mismatch; block |
| no admission receipt at adapter | execution-ticket rejection |

## Closure and recomposition

All eight findings now map to an invariant, owner, and finite failure case. The repaired contract recomposes as:

`semantic readiness once → explicit selection receipt → selected-unit material production → single-use live admission → mutation → separate closeout refresh`.

## Residue

- The exact schema field names and normalizer implementation remain Plan work.
- All toy cases are planned and unexecuted.
- The generator's relative-output validation bug remains separate tooling residue.

## Verdict

`pass` for repaired design completeness. This does not prove implementation or fixture execution.
