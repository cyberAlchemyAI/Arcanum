# Implementation Layering

## Layer decisions

| Layer | Scope | Evidence required to advance |
| --- | --- | --- |
| L0 Contract | Prerequisite and classification schemas; exact authority matrix. | Positive and negative schema fixtures; legacy records still validate or fail with typed diagnostics. |
| L1 Classification | Read-bounded classifier and fast-block receipt. | Phase/read instrumentation proves no Context Builder or mutation work on unmet prerequisites. |
| L2 Owner hop | Continuation Router prerequisite phase, exact authorization, joined owner receipt, revalidation, same-attempt resume. | Authorized, unauthorized, satisfied, stale, ambiguity, and cycle fixtures. |
| L3 Adoption | Invoke Plan handoff consistency, plan-once preference, outer composition guidance, integration and generated parity. | Cross-capability canary plus legacy regression and selective generation parity. |

## Boundary rules

- L0 cannot authorize mutation.
- L1 cannot invoke owner work.
- L2 cannot weaken owner gates or final Task Session admission.
- L3 cannot make plan-once a universal default without compatibility evidence.
- Canonical sources change before generated runtime mirrors.

## Promotion evidence

- L0 -> L1: schema fixtures pass.
- L1 -> L2: fast-block phase trace and bounded reads pass.
- L2 -> L3: owner-boundary, authorization, stale-scope, and cycle fixtures pass.
- L3 -> later lifecycle review: complete regression, canary, parity, and owner receipts pass.
