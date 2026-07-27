# TASK-DRE-VERIFY: Integrated Closeout

## Smallest Working Unit Exemption

Closure-only verification task; no source mutation is admitted.

## Checks

1. Runtime emitter focused suite.
2. True-subagent and role-simulation producer/resolver suites.
3. Direct telemetry and evidence-status suites.
4. Existing Distill schema, semantic, provenance, mode, positive, missing, and
   fabricated evidence suites.
5. Existing Invoke validation suite.
6. Isolated generated parity.
7. Markdown links and JSON/JSONL parsing.
8. Public-boundary scan.
9. Scoped `git diff --check`.
10. Claim audit confirming that events and telemetry remain non-authoritative.

## Result

Write `work-pack/results/TASK-DRE-VERIFY-RESULT.md`. On failure, preserve
`GAP-DEE-002` as open and route residue to the owning SWU.
