# Execution Pack: Deterministic Task Session Governance Runner

## Waves

| Wave | Layer | Included SWUs | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0-LIFECYCLE-CONTRACT.md) | L0 | 000, 001, 002 | Invoke package complete | lifecycle acceptance, evaluator parity, schema closure |
| [W1](work-pack/waves/W1-RUNNER-MECHANISM.md) | L1 | 003, 004, 005, 006 | W0 pass | deterministic prepare, executor join, reconcile, atomic commit/resume |
| [W2](work-pack/waves/W2-OWNER-INTEGRATION.md) | L2 | 007, 008 | W1 pass | joined owner-hook and continuation/cursor evidence |
| [W3](work-pack/waves/W3-OPERATIONS-INTEGRATION.md) | L3 | 009, 010 | W2 pass | observer evidence and bounded experiment/pilot verdict |

## Choreography

The route is a strict sequence because later SWUs modify shared runner surfaces and
depend on prior receipt contracts. Test-fixture preparation may be parallelized only
inside one SWU when paths are disjoint and the selected SWU owner retains one
integration receipt.

No governed multi-agent dispatch is authorized by this plan. The dispatch document
describes capability sequencing for later execution; any actual multi-agent fan-out
requires separate DomainSpec strategy confirmation and registration.

## Closure obligations

Every mutation-capable SWU must:

1. run the closeout prerequisite preflight before mutation admission;
2. bind exact live target digests, including dirty-state identity;
3. write its terminal executor receipt last;
4. invoke Continuation Router with the required owner route
   `invoke:refresh:apply-approved`;
5. join its receipt and the separately referenced Invoke owner receipt;
6. validate the refreshed work-pack/task/wave/cursor set;
7. stop after returning the cursor.

## Prototype frontier

- After TSGR-001: production policy evaluator.
- After TSGR-003: deterministic dry-run preparation/status prototype.
- After TSGR-006: checkpointed synthetic execution/reconcile/commit prototype.
- After TSGR-008: end-to-end closeout prototype.
- After TSGR-009: observable end-to-end prototype.
- After TSGR-010: bounded opt-in pilot verdict; no automatic lifecycle integration.
