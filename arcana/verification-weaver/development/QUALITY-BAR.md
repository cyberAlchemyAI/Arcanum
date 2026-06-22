# Quality Bar

The quality bar is intentionally fail-closed. `verification-weaver` is a parent
router, so uncertainty must stay visible in the parent receipt.

## Pass

A receipt may pass when all of these hold:

- target kind is recognized;
- owner lane refs are valid;
- required evidence refs exist or an explicit gap is recorded;
- an oracle type is present for required evidence;
- public-safety fields pass;
- top-level `promotion_action` is `none` or `candidate-request`;
- owner status is preserved without upgrade.

## Flag

A receipt should flag when work is routed but soft residue remains:

- UX evidence needs human comprehension review;
- dense expert UI creates possible false positives;
- architecture evidence is source-incomplete;
- research evidence is dry-run only;
- a mixed target is decomposed but child owner execution remains;
- a lane is seed, draft, or candidate-only.

Flags are useful output. They are not promotion evidence.

## Block

A receipt must block when any hard condition appears:

- target kind is unsupported;
- required oracle is missing;
- public-safety fields fail;
- evidence is flaky or runtime-adapter-dependent;
- owner lane is required and blocked;
- generated run artifacts are used as source authority;
- local telemetry is used as promotion evidence;
- parent receipt attempts owner promotion.

## Done Criteria

The candidate package is acceptable for this phase when:

- positive fixtures pass the receipt contract;
- all twelve negative controls are runnable;
- negative controls fail closed or preserve explicit residue;
- the validation harness writes `development/VALIDATION.md`;
- denylist scan has no matches in the package;
- no registry or generated runtime exposure is required.
