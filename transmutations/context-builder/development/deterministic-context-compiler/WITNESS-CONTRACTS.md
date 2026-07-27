# Planned Witness Contracts

Status: Design-authored and unexecuted.

These contracts specify later evidence. They are not Plan evidence, runtime
evidence, reusable-behavior proof, or promotion evidence.

## Fixture Matrix

| Fixture ID | Claim | Polarity | Input Or Violation | Expected Result |
| --- | --- | --- | --- | --- |
| DCC-FIX-001 | identical admitted inputs are byte-stable | positive | compile the same single-selector request twice | identical object, pack, and receipt hashes |
| DCC-FIX-002 | duplicate excerpts are stored and rendered once | positive | two obligations map to the same excerpt bytes | one excerpt object with both obligation refs |
| DCC-FIX-003 | selected-source drift invalidates reuse | negative | mutate one selected source after manifest freeze | stale-source block or current rebuild; never stale hit |
| DCC-FIX-004 | unrelated drift does not perturb the pack | positive | mutate an unselected source | identical selected set and pack hash |
| DCC-FIX-005 | ambiguous selectors fail closed | negative | two headings normalize to one requested selector | block with ambiguity diagnostic |
| DCC-FIX-006 | repository escape fails closed | negative | candidate path contains `..` or resolves outside root | block before file read |
| DCC-FIX-007 | uncovered obligations fail closed | negative | no valid candidate covers one required obligation | block with uncovered obligation ID |
| DCC-FIX-008 | budget overflow is explicit | negative | all legal covering sets exceed declared budget | block with budget diagnostic |
| DCC-FIX-009 | missing tokenizer does not invent counts | negative | tokenizer ID unavailable | byte counts present; token measurement unavailable |
| DCC-FIX-010 | unproved delta is rejected | negative | delta references a base with no runtime receipt | full payload emitted or block under strict delta policy |
| DCC-FIX-011 | persisted formats agree | positive | compile Markdown, JSON/index, and runtime payload | exact obligation/source/blocker parity |
| DCC-FIX-012 | one payload is injected | positive | runtime adapter receives persisted pack pair | receipt names exactly one injected payload hash |

## Deterministic Selection Contract

The selection policy consumes candidates that have already been mapped to
obligations. It:

1. rejects stale, missing, escaping, or ambiguous candidates;
2. collapses byte-identical excerpts and unions their obligation refs;
3. repeatedly selects the candidate with the best deterministic
   uncovered-coverage-to-cost comparison;
4. compares rational costs without floating-point rounding;
5. breaks ties by authority rank, ambiguity rank, byte or declared-token cost,
   normalized path, selector, and excerpt digest;
6. stops only when all obligations are covered or a blocker is emitted; and
7. orders rendered evidence by obligation ID, normalized path, and selector.

The policy is cost-aware and deterministic. It does not claim a globally
minimum set unless a later exact solver and proof receipt explicitly establish
that stronger property.

## Validator Contracts

| Validator ID | Target | Pass Condition | Required Negative Proof |
| --- | --- | --- | --- |
| DCC-VAL-REQUEST | context request | schema valid, IDs unique, mappings total | malformed and duplicate-ID fixtures fail |
| DCC-VAL-SNAPSHOT | source snapshot | every path in-root and digest-current | escape, missing, stale, ambiguous fail |
| DCC-VAL-CACHE | excerpt cache | object key and bytes recompute exactly | tampered object fails |
| DCC-VAL-COVERAGE | selected set | all obligations covered within policy | uncovered and over-budget fail |
| DCC-VAL-PARITY | persisted outputs | Markdown, JSON, payload share exact projection | mismatch fails |
| DCC-VAL-REPLAY | repeated compile | output and receipt hashes identical | nondeterministic ordering mutant fails |
| DCC-VAL-USAGE | token/runtime receipt | labels and evidence sources do not collapse | missing tokenizer/runtime remains unknown |
| DCC-VAL-PUBLIC | public package | no consumer-private paths or prose | injected private fixture fails |

## Live Evidence Contract

After deterministic fixtures pass, Experiment Harness runs paired baseline and
candidate examples:

- same task/SWU and same source snapshot;
- current model-driven Context Builder assembly;
- deterministic compiler-assisted assembly;
- actual runtime prompt usage when available;
- selected source and obligation coverage parity;
- cache hit/miss and compile duration;
- human review of sufficiency and noise;
- no claimed percentage when the runtime lacks actual usage receipts.

Promotion readiness requires fixture evidence plus live runtime evidence.
