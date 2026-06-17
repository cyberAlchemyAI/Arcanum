# Attacks: IntegrationSpec Gap Review

Dispatch: `2026-06-16-integration-spec-gap-review`
Dispatch type: `review`
Strategy version: DomainSpec subagents strategy v0.6.x, review flavor
Status: completed

This file preserves the public-safe attack, robot-talks, synthesis, and verification returns for the review. Local absolute paths from agent returns were normalized to repository-relative paths before writing this public artifact.

## Tension Gate

Two independent check-tension helpers reviewed the proposed sheet before registration.

| Helper | Result |
| --- | --- |
| checker | PASS |
| reviewer | PASS |

## Attack Group

Anti-bias axis: `attack-vector (governance/fidelity vs operability/mechanics vs ownership/reference-integrity)`

### Governance / Fidelity

Initial position:

- Discipline-first is licensed as the safest default, but the result should not present that route as conclusively proved.
- `RESULT.md` overstates with "Lane Z proved the positive case" and "Lane A proved the caution"; the receipts are refinement evidence, not proof-stage verification.
- Option D, a minimal `integration-spec` package proof, is over-deferred. Full canonical package promotion should wait, but a small local package proof should remain available if the user wants autonomous lifecycle evidence.
- Package-local vocabulary is blocked too hard: canonical DomainSpec meta-types or edges should remain blocked, but local Integration labels are already being used by the discipline design.
- The user should see live options: A discipline-first L0, B DomainSpec `integrations.md` aspect, C formula validator, D minimal local package proof.

Final robot-talks position:

- Keep the proof-language finding.
- Keep A/B/C/D as live route options, with A as the default.
- Upgrade the local-vocabulary issue: local terms are required as scaffolding, but explicitly non-canonical.
- Constrain D: any minimal package proof must be public-safe, local-vocabulary-only, and must not mutate DomainSpec taxonomy.
- Clarify validator scope: it checks anchors/completeness, not evidence truth.
- Drop any implication that B or C alone are equally strong next routes; they are useful but incomplete without L0 mechanics.

### Operability / Mechanics

Initial position:

- The route is directionally correct, but not mechanically useful enough for DomainSpec authors yet.
- L0 is currently too abstract: it needs an executable `INTEGRATION-BOUNDARY-DISCIPLINE.md` with required fields, gates, examples, and pass/flag/block criteria.
- Database/cache/resource selection is only named, not operationalized. A usable Integration Decision Record needs resource family, source of truth, consistency, cache role, invalidation/staleness, migration/lifecycle, security/governance, provider failure modes, alternatives rejected, and evidence.
- The validator cannot be defined directly from the result; it needs schema, fixtures, severity rules, and completeness checks.
- The counterexample must show what existing DomainSpec captures and what remains unmodeled.

Final robot-talks position:

- Keep L0 underspecification and resource-decision findings.
- Relation syntax must be explicitly IntegrationSpec-local/L0-local, not DomainSpec vocabulary:
  `operation_uses_integration_port`, `integration_port_implemented_by_adapter`, `adapter_connects_to_resource`, `resource_governed_by_decision`, `policy_attaches_to_boundary`, `mapping_transforms_external_shape`, `evidence_anchor_covers_obligation`.
- Validator checks completeness and evidence anchors, not runtime truth or architecture correctness.
- External standards own wire/protocol; IntegrationSpec-local vocabulary owns resource/provider responsibility shape; DomainSpec owns operations, queries, mappings, policies, workflows, sagas.
- Drop canonical DomainSpec meta-type or edge introduction for this pass.
- Option D is valid only when lifecycle-proof is the priority; it should not outrank Option A when the goal is to help DomainSpec authors immediately.

### Ownership / Reference Integrity

Initial position:

- `Port -> Adapter -> External Resource` is not supportable as canonical DomainSpec graph vocabulary today.
- `Adapter` is UI-only in DomainSpec; backend integration should use local wording such as `Integration Adapter`, `Provider Adapter`, or `Connector`.
- Evidence/proof is not canonical; validators can check evidence anchors/completeness but not runtime truth.
- Cache/source-of-truth, data-store selection, provider resource ownership, and evidence/proof relationships are real gaps, but should not be smuggled into DS-D1/DS-D2.
- DomainSpec reuse survives for `Interface`, `Mapping`, `Event`, `Policy`, `Operation`, `Query`, `Workflow`, and `Saga`, but only for domain/application behavior around integrations, not provider topology or proof authority.

Final robot-talks position:

- Soften "unsupported" to "not supportable as canonical DomainSpec vocabulary yet."
- Package-local labels are allowed and necessary.
- Discipline-first needs an actual artifact with required fields, gates, and a filled counterexample before it is executable.
- Local relation syntax is acceptable only if kept outside the DomainSpec Concept Graph and DS-D2 edge vocabulary.
- Minimal package proof is useful only as lifecycle evidence for IntegrationSpec, not as silent expansion of DomainSpec.

## Synthesis Draft

The synthesis identified seventeen candidate findings. The verifier pass narrowed or dropped several:

- Dropped as too broad: "L0 lacks gates." The refine plan does name validation gates; the surviving issue is missing field-level authoring criteria and schema detail.
- Narrowed: "database/cache guidance requires an Integration Decision Record" is not required by DomainSpec taxonomy itself. It is required by the integration problem and refine goal; taxonomy only proves current DomainSpec does not already carry cache/source-of-truth/resource semantics.
- Narrowed: "validator checks anchors/completeness" is supported by the refine design and schema-boundary definition, but the exact validator contract remains a design artifact.
- Out of scope for the refine-corpus verifier but substantiated by taxonomy/template verifier: missing `integrations.md`, canonical graph constraints, and DS-D1/DS-D2 closure.

## Verification

### Refine-Corpus Verifier

| Finding | Verdict | Evidence |
| --- | --- | --- |
| 1 proof language | SURVIVES | `RESULT.md` uses "proved" while bridge decisions are softer: `promotion-candidate`, `future-work`, `borrow-carefully`, `block`. |
| 2 L0 executable detail | DROP as broad | `RESULT.md` and `09-invoke-plan.md` do name gates/validation; the final finding must narrow to missing field-level criteria. |
| 3 package-local vocabulary | SURVIVES | `RESULT.md` marks package-local labels future-work while `06-invoke-design.md` already uses them as component vocabulary. |
| 4 database/cache/resource decision | SURVIVES | Refine corpus supports decision-record machinery for resource/cache choices. |
| 5 explicit options | SURVIVES | `05-distill.md` has alternatives and caution but not explicit A/B/C/D route choices. |
| 6 decision-record fields | SURVIVES | `06-invoke-design.md` defines Resource/Decision/Policy/Evidence but no decision-record fields. |
| 7 local relation syntax | SURVIVES | Owner boundaries exist, but local relation syntax is not stated. |
| 8 validator scope | SURVIVES | Validator scope is completeness; runtime truth/evidence is separated to Task Session. |
| 9 schema/fixture/counterexample detail | SURVIVES | L0-L3 supports discipline-first, but schema/fixtures/counterexample remain sketch-level tasks. |
| 10 minimal package proof option | SURVIVES | Default deferral is explicit; Lane Z residue supports preserving package proof as a route option. |
| 11 missing canonical edges | SURVIVES | Mapper directly states the missing canonical edges and local vocabulary. |
| 12 Adapter boundary | SURVIVES | Mapper directly warns not to shift UI `Adapter` into backend integration semantics. |
| 16 template gap | OUT OF SCOPE | Template authority is outside refine corpus. |
| 17 graph rule | OUT OF SCOPE | Canonical graph rule is taxonomy/spec authority. |

### Taxonomy / Template Verifier

| Finding | Verdict | Evidence |
| --- | --- | --- |
| 3 package-local vocabulary | SURVIVES | Local vocabulary can exist without promotion; canonical DomainSpec vocabulary is closed to DS-D1/DS-D2. |
| 4 Integration Decision Record | DROP as written | Taxonomy proves the cache/source-of-truth/resource gap but does not require a specific decision-record artifact. |
| 6 decision fields absent | SURVIVES, narrowed | Existing templates do not provide a decision-record template or Resource/Decision/Evidence fields; `Policy` is already canonical. |
| 7 local relation syntax | SURVIVES, narrowed | Any noncanonical relation syntax must stay outside DS-D2. |
| 8 validator truth boundary | SURVIVES, narrowed | Schema validation is not execution evidence or authority transfer; templates carry evidence anchors. |
| 10 package proof constraints | SURVIVES | No `ExternalResource`, `Evidence`, backend `Adapter`, or new edge can be promoted by implication. |
| 11 missing canonical concepts/edges | SURVIVES | DS-D1/DS-D2 and `RELATIONSHIPS.md` do not include Port, ExternalResource, Evidence, Decision, cache/source-of-truth edges. |
| 12 Adapter boundary | SURVIVES, narrowed | Canonical `Adapter` is UI-boundary only; `Mapping` is the supported transformation concept. |
| 16 missing `integrations.md` | SURVIVES | The template directory has no `integrations.md`. |
| 17 canonical graph rule | SURVIVES | `SPEC.md` requires canonical edge names from `RELATIONSHIPS.md`; DS-D2 boundary is closed. |

## Convergence

The review converged on the following:

- Keep discipline-first as the recommended route.
- Make L0 executable rather than merely directional.
- Treat integration ports/adapters/resources/decision/evidence/cache terms as local vocabulary.
- Do not mutate DomainSpec definitions or relationship canon in this pass.
- Add a DomainSpec authoring aspect only after L0 defines fields and boundaries.
- Permit a minimal local `integration-spec` package proof only as a lifecycle experiment, not as canonical promotion.
