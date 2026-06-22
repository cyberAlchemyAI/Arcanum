# Verification Weaver Validation

- Result: pass
- Timestamp UTC: 20260621T142304Z
- Positive fixtures: 6
- Negative controls: 12
- Parent receipt: VERIFICATION-WEAVE
- Promotion action allowed: none, candidate-request

## Validated Items
- positive:development/fixtures/positive/architecture-gap-basic.receipt.yml
- positive:development/fixtures/positive/execution-repeatability-basic.receipt.yml
- positive:development/fixtures/positive/frontend-ux-seed-flag.receipt.yml
- positive:development/fixtures/positive/mixed-target-split.receipt.yml
- positive:development/fixtures/positive/research-evidence-basic.receipt.yml
- positive:development/fixtures/positive/spec-derivation-basic.receipt.yml
- negative:development/negative-controls/NC-ADAPTER-001.receipt.yml
- negative:development/negative-controls/NC-ARCH-FOLDER-ONLY-001.receipt.yml
- negative:development/negative-controls/NC-E2E-FLAKE-001.receipt.yml
- negative:development/negative-controls/NC-GENERATED-001.receipt.yml
- negative:development/negative-controls/NC-MIX-001.receipt.yml
- negative:development/negative-controls/NC-NO-ORACLE-001.receipt.yml
- negative:development/negative-controls/NC-PRIVATE-001.receipt.yml
- negative:development/negative-controls/NC-RECEIPT-PROMOTE-001.receipt.yml
- negative:development/negative-controls/NC-RESEARCH-DRYRUN-001.receipt.yml
- negative:development/negative-controls/NC-UNSUPPORTED-001.receipt.yml
- negative:development/negative-controls/NC-UX-DENSE-001.receipt.yml
- negative:development/negative-controls/NC-UX-HUMAN-001.receipt.yml

## Failures
- none

## Residue
- Candidate package is not registered.
- Owner lanes remain authoritative for their own evidence.
- Follow-up route: sigil-development review, then experiment-harness calibration.
