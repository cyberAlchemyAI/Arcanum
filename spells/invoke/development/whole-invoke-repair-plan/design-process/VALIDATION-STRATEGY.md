# Invoke Design W1-W3 — Validation Strategy

## Structural Validation

1. Parse every new JSON file.
2. Run `Draft202012Validator.check_schema` over all twenty-two Design schemas.
3. Validate the canonical process and policy instances, their self-digests, and
   the downstream positive fixture family.
4. Apply one-field structural mutations and require the expected schema family
   to reject them.
5. Run scoped `git diff --check` and a public-content scan over the exact W1-W2
   allowlist, including untracked create targets.

## W1 Producer Validation

Positive coverage requires:

- normal activation through one real installed Define v2 compiler output;
- approved discovery activation with `input-review` as the only route;
- the public canonical example through the actual projector, frozen extractor,
  and frozen selection validator;
- two runs with byte-identical five-file output directories.

Negative coverage requires schema-valid failure receipts for governed blocks
and an absent success directory. It covers approval mismatch, stale digests,
unsafe paths and symlinks, missing or multiply classified candidates, boundary
and class gaps, unresolved conditions and conflicts, exclusions without exact
approval, public/private leaks, schema mismatch, invalid Define receipts,
false greenfield or ambiguous predecessor claims, invalid signal provenance,
illegal readiness evidence, predicate mismatch, extractor/selection blocks,
pre-existing destinations, late failure, and output inventory drift.

The unchanged 28-case/27-mutation selection corpus runs with a temporary report
directory. Focused Define v2 producer and authoring-guide regressions also run.

## W2 Candidate Validation

Positive coverage requires:

- real Define v2 PASS through normal W1 PASS and the installed public profile
  into one atomic W2 candidate;
- byte-identical repeat publication;
- lossless field comparison for all thirteen signal classes;
- the complete typed application denominator, including excluded and
  conditionally excluded inputs;
- required, recommended, and N/A concern traces;
- exact installed rule IDs, order, and rule-set digest;
- exact two-payload plus self-excluded receipt closure.

Governed negative cases leave the W2 success directory absent and issue one
schema-valid attempt receipt. They cover discovery/stale/wrong W1 evidence,
missing or duplicate typed pairs, wrong exclusion evidence, every signal-field
drift, dangling or wrong-kind fact edges, illegal N/A/view/selection/witness
claims, contract supersession without an eligible decision, evolution fail
closure, installed contract drift, unsafe destinations, and late output drift.

The persisted schema fixture validates directly against the installed W2
family; tests must not replace its current source/artifact/matrix documents in
memory to conceal fixture drift. The real producer fixture remains generated
because its exact W1 paths and digests are run-specific.

## W3 Bundle And Admission Validation

Positive coverage runs a real Define v2 → W1 → W2 → W3 chain, two absent
destinations with byte-identical fifteen-file bundles, clean replay admission,
capability `artifact_authored`, and a fresh W1/W2 evolution candidate consuming
one genuine v2 predecessor.

Negative coverage includes stale candidate or installed bindings, missing or
non-passing Distill evidence, unsafe paths, pre-existing destinations, late
projection drift, tampered Markdown/JSON, inventory mismatch, generic Design
self-assertion, historical v1 receipts, forged producer/validator identities,
and replay mismatch. Governed compiler failure leaves the success directory
absent and issues one schema-valid W3 attempt receipt. Admission failure leaves
the submitted bundle byte-for-byte unchanged.

## Deferred Validation

W1 cannot prove architectural coherence. W2 proves typed registry and six-view
candidate coherence only within the exact W1 denominator and installed policy.
W3 proves deterministic bundle production, exact Distill binding, replay
admission, and genuine v2 predecessor consumption. It does not prove
repository-global semantic completeness, mirror parity, Plan evidence,
acceptance, execution, publication, deployment, or external effect. Those
claims remain W4 or later.
