# Whole Invoke Audit — 2026-08-27

## Verdict

`BLOCK`: Invoke contains several strong validators and bounded producers, but it is not an end-to-end implemented authoring workflow. Its root status claims exceed the executable closure currently proven.

| Mode | Audited status | Main reason |
| --- | --- | --- |
| Define | partial | Identity denominator is real; no atomic final Define bundle producer. |
| Design | partial | Scope/selection validation is real; no atomic six-view final bundle producer. |
| Plan | partial, terminal closure broken | WPRA/readiness slices pass; full Plan package producer is absent and preacceptance is red. |
| Handoff | contract-only | Contract says validation examples are pending; no canonical mode producer/validator. |
| Refresh | partial, apply claim broken | Material/handoff validation is real; promised report/patch/application family has no canonical producer. |
| Full | deferred removal candidate | Unsupported and unimplemented. |
| Validate | deferred | Unsupported and unimplemented. |

## Highest-risk findings

1. Capability status trusts a generic self-asserted artifact receipt instead of validating each mode's required evidence and exact refs.
2. The canonical aggregate suite is red: 14 preacceptance tests error because `joined_driver_digest` is missing from fixture production.
3. Plan v1 compiles only the WPRA subset, not the complete execution-candidate package promised by the Plan contract.
4. Several preacceptance stages use development adapters or schema parsing in place of actual production transformations.
5. Owner request/response versions are split across v2/v1 and v3/v2 families.

## Full-mode removal

Removing `full` is appropriate, but it is not a one-file deletion. The bounded removal must update the root mode router, `mode-capabilities.json`, capability request/result schemas and fixtures, Handoff route choices, templates, generated mirrors, and compatibility tests together. Historical evidence remains readable; new routing must not advertise `invoke full`.

## Validation summary

- Aggregate Invoke suite: `BLOCK` only at preacceptance; 14 closure errors and 6 teardown passes.
- Define denominator: 17/17 PASS.
- Design selection: 28 cases and 27 mutations PASS.
- Material/Refresh: 23/23 PASS.
- Capability resolver: 13/13 PASS against the current weak contract.
- Plan source compiler: 5/5 PASS.
- Plan implementation readiness: 5/5 PASS.
- Accepted-stream bridge: 9/9 PASS.
- Focused preacceptance companion suites: 13/13 PASS.
- Generated Invoke payload parity: 244/244 PASS.

## Recommended order

1. Harden capability-status evidence admission and make root status labels truthful.
2. Repair `joined_driver_digest` production and restore the complete preacceptance suite.
3. Add one versioned canonical producer for the complete Plan execution-candidate family.
4. Replace consumer substitutions and select one request/response version family.
5. Complete or downgrade the remaining active mode claims.
6. Remove deferred `full` as a compatibility-closed slice.
7. Prove the repaired workflow with one fresh generic laboratory run.

This audit grants no implementation, request, acceptance, selection, admission, execution, Git, publication, deployment, or external-effect authority.
