# Invoke Design Schema Plan

## Rule

Each schema has one authority boundary. Cross-document semantic equality is
validated by an executable consumer rather than duplicated as prose or inferred
from matching labels.

## Schema Family

| Schema | Canonical instance | Responsibility | Explicitly does not own |
| --- | --- | --- | --- |
| `design-production-process-v1.schema.json` | `DESIGN-PRODUCTION-PROCESS.json` | Ordered stages, owners, gates, artifact transitions, failure states, compatibility, and evidence ceiling. | Design content. |
| `design-profile-v1.schema.json` | `DESIGN-PROFILE.json` | Public fact-kind denominator, exact core minima, ordered six-view IDs, and legal kinds per view. | Authored Design facts or a coherence verdict. |
| `design-input-boundary-approval-v1.schema.json` | `DESIGN-INPUT-BOUNDARY-APPROVAL.json` | Owner-approved target, visibility, epoch, finite roots, discovery rules, required classes, and exact permitted exclusions. | Input completeness PASS or architecture. |
| `design-input-closure-v1.schema.json` | `DESIGN-INPUT-CLOSURE.json` | Discovery boundary, exact typed input catalog, authority roles, target evolution, constraints, invariants, prior decisions, exclusions, and authored selection inputs. | Completeness PASS, architecture proposal, or `DesignScopeManifest` authority. |
| `design-input-closure-receipt-v1.schema.json` | `DESIGN-INPUT-CLOSURE-RECEIPT.json` | Independent boundary inspection, found/excluded/missing/stale/conflicting classifications, prior-Design determination, causal blockers, and pass/block verdict. | Concern selection or architecture proposal. |
| `design-input-production-receipt-v1.schema.json` | `DESIGN-INPUT-PRODUCTION-RECEIPT.json` | Failure-capable fixed W1 stage statuses, exact four-payload PASS inventory, blockers, routing, and evidence ceiling. | Design source, final Design stage PASS, or admission. |
| `design-source-v1.schema.json` | `DESIGN-SOURCE.json` | Sole authored architecture authority: exact upstream bindings, total input application, one typed fact registry, six ID-based view projections, selected companions, risks, and planned witnesses. | Coherence verdict, installed policy choice, or executed evidence. |
| `design-artifact-v1.schema.json` | `DESIGN.json` | Producer-owned normalized read model compiled from the exact source before coherence validation. | Coherence receipt, final stage PASS, or later admission. |
| `design-coherence-policy-v1.schema.json` | `DESIGN-COHERENCE-POLICY.json` | Versioned semantic rule catalog and diagnostic ownership. | Actual verdict. |
| `design-coherence-receipt-v1.schema.json` | `DESIGN-COHERENCE-RECEIPT.json` | Exact source/policy bindings, evaluated rules, diagnostics, and verdict. | Bundle production. |
| `design-candidate-production-receipt-v1.schema.json` | `DESIGN-CANDIDATE-PRODUCTION-RECEIPT.json` | Failure-capable fixed W2 stages, exact two-payload PASS inventory, blockers, routing, and candidate evidence ceiling. | Human views, final Design stage PASS, admission, or Plan entry. |
| `design-result-v1.schema.json` | historical `INVOKE-DESIGN-STAGE-RECEIPT.json` | Read-only historical Design receipt shape. It cannot establish a new PASS. | Current stage admission or later authority. |
| `design-bundle-closure-v1.schema.json` | `DESIGN-BUNDLE-CLOSURE.json` | Exact passing W2 candidate, target, Distill evidence, fixed output contract, and closure digest. | Architecture semantics or a Distill verdict. |
| `design-bundle-attempt-receipt-v1.schema.json` | separate W3 attempt receipt | Block-only fixed W3 stages, diagnostics, routing, empty outputs, and evidence ceiling. | Successful publication. |
| `design-result-v2.schema.json` | `INVOKE-DESIGN-STAGE-RECEIPT.json` | Current producer identity, exact W1/W2/source/profile/policy/Distill bindings, ordered fourteen-payload inventory, `design-stage-pass`, and ceiling. | Independent admission or later authority. |
| `design-bundle-admission-receipt-v1.schema.json` | external admission receipt | Complete fifteen-file inventory, validator identity, clean replay comparison, checks, blockers, and artifact-only ceiling. | Registry or runtime readiness. |
| `design-glossary-consistency-report-v1.schema.json` | `GLOSSARY-CONSISTENCY-REPORT.json` | Deterministic authored-complete glossary projection. | Glossary promotion. |
| `design-planned-witness-contracts-v1.schema.json` | `PLANNED-WITNESS-CONTRACTS.json` | Deterministic planned witness contracts with explicit non-execution. | Plan evidence. |
| `design-template-selection-receipt-v1.schema.json` | `TEMPLATE-SELECTION-RECEIPT.json` | Deterministic installed-profile and companion selection projection. | Template promotion. |
| `design-dispatch-trace-v1.schema.json` | `DISPATCH-TRACE.json` | Deterministic authored technique trace. | Dispatch execution evidence. |
| `design-transport-report-v1.schema.json` | `DESIGN-TRANSPORT-REPORT.json` | Deterministic no-op transport policy projection. | Transport, publication, or external effect. |
| `design-validation-matrix-v1.schema.json` | `DESIGN-VALIDATION-MATRIX.json` | Positive and negative case inventory, expected stage, diagnostic, and no-publication assertions. | Test execution results. |

## Existing Contracts Preserved

- `design-scope-manifest.schema.json` remains the exact detector input.
- `design-denominator-receipt.schema.json` remains independent extractor evidence.
- `design-selection-result.schema.json` remains selection and fixed-point evidence.

The new Design input-closure schema does not replace those contracts. It pins
the existing manifest schema as its projection contract. The future scope
projection consumer must prove total coverage between
`DESIGN-INPUT-CLOSURE.json` and `DesignScopeManifest`.

## Cross-Schema Bindings

- Every material ref uses repository-relative `path`, SHA-256, and byte `size`.
- Catalog selectors use canonical `file:<repo-relative-path>` whole-file form;
  projector adapters remove only the `file:` prefix where the frozen manifest
  consumer requires a repository path.
- Approved directory roots use sorted `{relative_path, sha256, size}` leaf
  records and total leaf size. The projector separately emits the frozen
  manifest consumer's historical directory digest without changing that
  protected contract.
- Every document has a versioned schema identity and stable document ID.
- The Design source binds the exact normal W1 production receipt, input closure,
  independent closure receipt, manifest, denominator, selection, and installed
  public profile refs.
- Every typed W1 obligation appears exactly once in the source `applications`
  array; the denominator includes excluded catalog inputs and conditional
  resolutions as explicit evidence-backed N/A applications. Uniqueness, total
  equality, exact exclusion evidence, and reciprocal fact provenance are
  semantic-validator responsibilities.
- The producer, not the author, binds the installed process and coherence policy
  while compiling `DESIGN.json`.
- `DESIGN.json` binds the same input, selection, and source digests but not the
  later coherence receipt; this avoids a digest cycle.
- The coherence receipt binds the staged `DESIGN.json`, source, installed policy,
  and all upstream closure evidence.
- The candidate production receipt binds the source, candidate artifact,
  coherence receipt, installed producer/validator identities, and exact atomic
  three-file output family while excluding its own bytes from payload closure.
- The v2 stage receipt binds the bundle closure, source, W1/W2 receipts,
  installed profile/process/policy, candidate artifact, coherence receipt,
  exact Distill evidence, producer identity, and ordered fourteen-payload family.
- The admission receipt binds the complete fifteen-file directory and clean
  compiler replay. It remains outside the submitted bundle.

## Compatibility

Existing manifests, denominator receipts, selection results, Markdown fixtures,
and live Design prose remain readable inputs or historical evidence. The
unreleased v1 stage contract is frozen historical/read-only; only v2 plus its
independent admission receipt can establish a new Design PASS. Evolution
accepts exactly one genuine v2 predecessor. Selection continues to use
`design-validator-pass`; neither W1 nor W2 candidate PASS substitutes for W3.
