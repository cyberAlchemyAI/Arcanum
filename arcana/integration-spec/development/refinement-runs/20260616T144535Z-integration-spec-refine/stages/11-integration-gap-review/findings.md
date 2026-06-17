# Findings: IntegrationSpec Gap Review

Dispatch: `2026-06-16-integration-spec-gap-review`
Status: resolved
Final approver: parent

## Summary

The prior refine result is directionally right: **Integration Boundary Discipline first** is still the recommended route. The review found the gap is sharper than the result expressed:

- DomainSpec can model the domain/application side of an integration through existing concepts such as `Operation`, `Query`, `Interface`, `Mapping`, `Policy`, `Workflow`, `Saga`, and `Event`.
- DomainSpec does **not** currently model provider/resource topology, `Port -> Adapter -> External Resource`, cache/source-of-truth, data-store selection, or evidence/proof relationships as canonical graph vocabulary.
- The next artifact should therefore be an executable L0 discipline with local vocabulary, not a direct mutation of `arcanum/definitions/*`.

## Surviving Findings

| # | Target | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| 1 | `RESULT.md` | The result says "Lane Z proved the positive case" and "Lane A proved the caution" while the run is `pass-with-residue` and the bridge decisions are softer (`promotion-candidate`, `future-work`, `borrow-carefully`, `block`) (`RESULT.md:3`, `RESULT.md:17`, `RESULT.md:23`, `RESULT.md:34-46`). | MAJOR | Replace proof language with `argued`, `supported`, or `provided evidence for`. Add that these are refinement synthesis judgments, not executed proof. |
| 2 | `RESULT.md` / L0 route | The result selects Integration Boundary Discipline first and calls for a discipline card, component catalog, and counterexample (`RESULT.md:11-13`, `RESULT.md:50-59`). The plan names validation gates (`09-invoke-plan.md:40-45`), so the issue is not absence of gates; it is missing field-level authoring criteria and acceptance checks. | MAJOR | Make L0 executable: produce `INTEGRATION-BOUNDARY-DISCIPLINE.md` with required sections, field names, pass/flag/block criteria, owner boundaries, and one filled counterexample. |
| 3 | Package-local vocabulary | `RESULT.md` marks package-local labels as `future-work`, while the design already defines `Integration Port`, `Integration Adapter`, `Integration Resource`, `Integration Decision`, `Integration Policy`, `Integration Mapping`, and `Integration Evidence` (`RESULT.md:41-42`, `06-invoke-design.md:24-35`). | MAJOR | Change package-local labels from deferred future-work to allowed L0-local machinery. Keep them out of canonical DomainSpec until definitions-governance promotes them. |
| 4 | Database/cache/resource handling | The mapper says cache guidance includes source of truth, TTL, invalidation, stale data, and sensitivity decisions, and data-store guidance includes access pattern, consistency, lifecycle, cost, governance, and store family choice (`taxonomy-standards-mapper.md:47-48`). `06-invoke-design.md` names `Integration Resource` and `Integration Decision` but only says to select a resource family through a decision record (`06-invoke-design.md:31-32`, `06-invoke-design.md:41`). | CRITICAL | Add an Integration Decision Record schema for the integration problem: resource family, source of truth, access pattern, consistency model, latency/throughput, lifecycle/migration, cache role, invalidation/staleness, security/governance, provider failure modes, alternatives rejected, and evidence anchors. This is an IntegrationSpec/L0 requirement, not a claim that DomainSpec taxonomy already requires this exact artifact. |
| 5 | Route options | `05-distill.md` lists five tracks and says the DomainSpec aspect and formula validator are useful but insufficient alone (`05-distill.md:11-15`, `05-distill.md:40-45`). `RESULT.md` recommends one sequence but does not expose the alternatives as choices (`RESULT.md:48-59`). | MAJOR | Present A/B/C/D options explicitly, with A as recommended and D as allowed but constrained. |
| 6 | Decision-record fields | `06-invoke-design.md` defines Resource/Decision/Policy/Evidence, but not the decision-record fields (`06-invoke-design.md:31-35`, `06-invoke-design.md:41`). Existing DomainSpec templates do not provide Resource/Decision/Evidence fields; the spec template only references architecture decisions generally (`SPEC.md:121-125`). | MAJOR | Define a concrete decision-record template before writing a validator or DomainSpec aspect. |
| 7 | Local relation syntax | The design separates owners but does not state local relation syntax (`06-invoke-design.md:64-73`). The mapper names missing canonical edges for `Port -> Adapter`, `Adapter -> External Resource`, `Evidence -> Decision`, and cache/source-of-truth (`taxonomy-standards-mapper.md:31-37`). | MAJOR | Add local, noncanonical relations in L0: `operation_uses_integration_port`, `integration_port_implemented_by_adapter`, `adapter_connects_to_resource`, `resource_governed_by_decision`, `policy_attaches_to_boundary`, `mapping_transforms_external_shape`, `evidence_anchor_covers_obligation`. Do not put them in DS-D2. |
| 8 | Validator authority | The design says the formula validator candidate owns completeness (`06-invoke-design.md:45`, `06-invoke-design.md:70-72`), while the result blocks runtime receipts as canonical spec truth (`RESULT.md:45-46`). Definitions say schema validation is shape evidence, not execution evidence, promotion evidence, or authority transfer (`DEFINITIONS.md:91-95`). | MAJOR | Define the validator as checking required fields, links, local relation shape, and evidence anchors. It must not claim runtime truth or architecture correctness. |
| 9 | Plan detail | The plan has the right L0-L3 ladder (`09-invoke-plan.md:14-19`) but keeps validator fields, fixtures, and counterexample content as sketch-level tasks (`09-invoke-plan.md:23-38`). | MAJOR | Expand TASK-IBD-003 into schema plus pass/flag/block fixtures. Expand TASK-IBD-004 into a filled two-column counterexample. |
| 10 | Minimal package proof | The default plan defers `sigil-development` until L0, template, validator, and counterexample evidence exist (`09-invoke-plan.md:47-49`). Lane Z kept the package tier conditional, not dead. | MINOR | Keep deferral as the default, but expose a constrained Option D for a minimal local package proof if autonomous lifecycle evidence is the user's priority. |
| 11 | DomainSpec graph boundary | DS-D1 is closed to the canonical backend/UI type sets and has no `Port`, `ExternalResource`, `Evidence`, `Cache`, or `Decision` meta-type (`DEFINITIONS.md:122-140`). DS-D2 is closed to its edge sets and no larger extension is adopted (`DEFINITIONS.md:144-176`). `RELATIONSHIPS.md` lists supported signatures but no integration resource/cache/proof edges (`RELATIONSHIPS.md:11-53`). | CRITICAL | Treat the integration envelope as local vocabulary until promoted. DomainSpec can reference existing concepts but cannot currently own the full integration graph. |
| 12 | `Adapter` overload | `Adapter` is UI connective vocabulary and is defined as a UI-boundary data-shape transformation (`TAXONOMY.md:28-42`, `TAXONOMY.md:501-503`). `RELATIONSHIPS.md` gives `shapes` as `Adapter -> View Model` (`RELATIONSHIPS.md:40`, `RELATIONSHIPS.md:242-249`). | MAJOR | Do not reuse canonical `Adapter` for backend/provider integration implementation. Use local `Integration Adapter`, `Provider Adapter`, or `Connector`; use canonical `Mapping` for field/payload transformations. |
| 13 | Missing authoring aspect | The DomainSpec template family lists `operations.md`, `queries.md`, `interfaces.md`, `states.md`, `events.md`, and `mappings.md`, but no `integrations.md` (`README.md:5-8`; template directory checked). `SPEC.md` tells authors to use canonical edge names from `RELATIONSHIPS.md` in the concept graph (`SPEC.md:66-79`). | MAJOR | Add a candidate `integrations.md` only after L0 defines the fields. Keep local relations in the aspect, outside the canonical feature concept graph. |

## Refuted Or Narrowed

| Candidate | Final handling |
| --- | --- |
| "L0 lacks gates." | Dropped as written. The plan names validation gates. The surviving issue is missing field-level authoring criteria, required sections, and acceptance checks. |
| "Taxonomy requires an Integration Decision Record." | Dropped as written. Taxonomy proves the cache/resource/source-of-truth gap; the Integration Decision Record is the recommended L0 solution, not a requirement already present in DomainSpec canon. |
| "Validator proves evidence." | Rejected. Validator checks required structure, links, and evidence anchors only. |
| "B/C/D are equal next routes." | Rejected. They are valid options, but A is still recommended when the goal is to fill DomainSpec's practical integration gap. |

## Options For IntegrationSpec

| Option | What it does | Trade-off | Verdict |
| --- | --- | --- | --- |
| A. Discipline-first L0 | Create `INTEGRATION-BOUNDARY-DISCIPLINE.md`, local vocabulary, local relation syntax, decision-record fields, public-boundary/no-taxonomy gates, and a filled payment/webhook/cache/idempotency/reconciliation counterexample. | Fastest route to usable guidance without mutating canon. | Recommended |
| B. DomainSpec `integrations.md` aspect | Add an authoring surface for feature specs after L0 defines required fields. | Helps authors, but is incomplete without L0 mechanics and local vocabulary rules. | Candidate |
| C. Formula validator | Define schema/rules and pass/flag/block fixtures for required fields and evidence anchors. | Good for completeness; cannot select architecture trade-offs or prove runtime truth. | Candidate after A/B shape exists |
| D. Minimal local `integration-spec` package proof | Build a small public-safe package proof to test whether this needs an autonomous lifecycle owner. | Higher overhead and easy to over-promote; must not mutate DomainSpec or silently introduce canonical terms. | Optional lifecycle proof |

## How To Fill DomainSpec's Gap

Use a two-layer fill.

Layer 1: L0 Integration Boundary Discipline outside canonical DomainSpec.

Required sections:

- Integration boundary and application use case.
- Reused DomainSpec concepts: `Operation`, `Query`, `Interface`, `Mapping`, `Policy`, `Workflow`, `Saga`, `Event`.
- Local vocabulary: integration port, provider adapter/connector, external resource, integration decision, integration evidence.
- External standard references: OpenAPI, AsyncAPI, CloudEvents, provider docs, SQL/schema, SDK docs, or equivalent.
- Integration Decision Record: resource family, source of truth, access pattern, consistency model, latency/throughput, lifecycle/migration, cache role, invalidation/staleness, security/governance, provider failure modes, alternatives rejected, evidence anchors.
- Policies: idempotency, retry, timeout, auth, rate limit, circuit breaker, fallback, reconciliation, cache invalidation.
- Mappings: external payloads to domain events/entities/DTOs, using canonical `Mapping` where possible.
- Evidence anchors: contract tests, mapping tests, sandbox/emulator checks, migration checks, cache consistency checks, reconciliation checks, observability checks.
- Public-boundary and no-taxonomy-mutation gate.

Layer 2: DomainSpec candidate `integrations.md` aspect.

The aspect should reference canonical DomainSpec concepts where they fit, but carry provider/resource/cache/source-of-truth mechanics as local integration fields. Local relation names must stay outside the canonical feature concept graph unless definitions-governance promotes them.

## Counterexample Requirement

The minimum useful proof should be a two-column payment/provider example:

| Existing DomainSpec can capture | Remains unmodeled without Integration Boundary Discipline |
| --- | --- |
| API endpoint in `interfaces.md` | Provider ownership and resource responsibility |
| Request/response transformations in `mappings.md` | Idempotency key scope and duplicate webhook handling |
| `CreatePayment` as `Operation` | Synchronous return vs later webhook authority |
| `PaymentWebhookReceived` as `Event` | Provider/local state disagreement and reconciliation |
| `GetPaymentStatus` as `Query` | Cache-aside staleness, source-of-truth, invalidation, freshness |
| Retry/fallback as `Policy` | Evidence obligations across sandbox, contract tests, cache checks, reconciliation checks |

The gap is proved only if the right column contains implementation decisions a team must make before coding and that current DomainSpec aspect docs do not house cleanly.

## Close Decision

Accepted. The change request list is verified after narrowing. The review closes `resolved` with residue:

- Build A first unless the user explicitly prioritizes package lifecycle evidence.
- Keep local vocabulary local.
- Do not mutate `arcanum/definitions/*` from this review.
- Do not treat runtime receipts as canonical spec truth.
