# TASK-SRG-INTEGRATION — Cross-capability proof and packaging

## Smallest Working Units

### SWU-SRG-009 — Integration fixture

- Primary behavior: prove the complete single-audit route and adversarial failure matrix.
- Dependencies: SWU-SRG-008.
- Write scope: public synthetic integration fixtures and validation report only.
- Done: one audit, explicit selection, later material production, one live admission, one mutation-shaped dry run, terminal receipt, and separate closeout; no second audit or pre-execution Refresh command. All reviewer counterexamples block.
- Split analysis: the success route and adversarial cases share one cross-capability receipt chain and are accepted as one integration behavior.
- Verification: deterministic integration runner plus existing audit and Task Session suites.
- Owner: parent-coordinated validation under both lifecycle owners.

### SWU-SRG-010 — Documentation and generated packages

- Primary behavior: publish the validated canonical contract to runtime mirrors without semantic drift.
- Dependencies: SWU-SRG-009.
- Write scope: canonical READMEs/SKILL contracts and targeted generated Work Pack Readiness Audit and Task Session packages.
- Done: docs distinguish selection-ready from mutation-ready; targeted sync produces canonical/generated parity; public/private scan passes.
- Split analysis: documentation and generated sync share one external contract version and one parity acceptance boundary; no source behavior changes here.
- Verification: targeted sync dry-run/apply, fixture replay, link/path checks, and diff review.
- Owner: Spellcraft/Sigil Development packaging owners; parent coordinates parity only.

## Closeout

Use the Work Pack closeout contract. Unique successors: 009→010→none.
