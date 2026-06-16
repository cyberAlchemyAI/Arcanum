# Refine Result: IntegrationSpec

Status: pass-with-residue
Run ID: 20260616T144535Z-integration-spec-refine
Dispatch ID: refine-20260616T144535Z-integration-spec
Preset: full
Research: bounded-research

## Final Synthesis

The IntegrationSpec problem is real, but immediate creation of a full `arcana/integration-spec` package is not yet the smallest responsible first move.

The selected route is **Integration Boundary Discipline first**, with `integration-spec` preserved as a future package candidate after evidence.

## Why

Lane Z proved the positive case: integration work needs more than DomainSpec `interfaces.md` and `mappings.md`. A real integration can combine synchronous API calls, webhook callbacks, cache-aside stale reads, duplicate delivery, idempotency, reconciliation, provider errors, and local state disagreement. That needs an application-layer envelope:

```text
application use case -> integration port -> adapter -> external resource -> policy -> mapping -> evidence
```

Lane A proved the caution: that envelope does not yet require an autonomous arcana package. A discipline-first route can harden the practice, then route narrower artifacts to the right owners:

- DomainSpec template extension for authoring;
- formula validator for completeness checks;
- Task Session for runtime evidence;
- definitions-governance only if local vocabulary stabilizes.

The mapper proved the boundary: DomainSpec can reuse `Interface`, `Mapping`, `Event`, `Policy`, `Operation`, `Query`, `Workflow`, and `Saga`, but current edges are strained for `Port -> Adapter`, `Adapter -> External Resource`, cache/source-of-truth relationships, and evidence/proof relationships.

## Bridge Decisions

| Claim | Decision |
| --- | --- |
| Integration boundary problem exists | promotion-candidate |
| Immediate `arcana/integration-spec` package | future-work |
| Integration Boundary Discipline | promotion-candidate |
| DomainSpec integration aspect | promotion-candidate |
| Formula-level integration contract validator | promotion-candidate |
| New canonical DomainSpec meta-types or edges | block |
| Package-local labels such as Integration Port and Integration Evidence | future-work |
| OpenAPI, AsyncAPI, CloudEvents | borrow-carefully |
| Database and cache architecture guidance | borrow-carefully |
| Runtime receipts as canonical spec truth | block |
| Runtime receipts as task evidence | borrow-carefully |

## Recommended Next Route

Run `discipline-governance` or a bounded `task-session` for L0:

1. Draft an Integration Boundary Discipline card.
2. Include a minimum component catalog.
3. Use the counterexample: payment API + webhook + cache-aside stale read + idempotency + reconciliation.
4. Add a public-boundary scan and no-taxonomy-mutation gate.
5. Then route candidate outputs to:
   - DomainSpec `integrations.md` aspect design;
   - formula-level integration contract validator design;
   - later `sigil-development` for `integration-spec` only if the L0 evidence shows the workflow needs an autonomous package.

## Stage Evidence

| Stage | Status | Artifact |
| --- | --- | --- |
| Context Builder evidence baseline | pass | `stages/01-context-builder/context-pack.md` |
| Invoke Define | pass | `stages/02-invoke-define.md` |
| Interrogation refine-review | pass | `stages/03-refine-review.md` |
| Research decision | pass | `stages/04-bounded-research.md` |
| Distill | pass | `stages/05-distill.md` |
| Invoke Redefine / Design | pass | `stages/06-invoke-design.md` |
| Interrogation refine-design-review | pass | `stages/07-refine-design-review.md` |
| Distill Repair | pass | `stages/08-distill-repair.md` |
| Invoke Plan | pass | `stages/09-invoke-plan.md` |
| Final Interrogation and Synthesis | pass | `stages/10-final-interrogation.md` |

## Subagent Receipts

| Role | Status | Receipt |
| --- | --- | --- |
| `lane-z-integration-spec-advocate` | completed | `stages/subagent-receipts/lane-z-integration-spec-advocate.md` |
| `lane-a-alternatives-challenger` | completed | `stages/subagent-receipts/lane-a-alternatives-challenger.md` |
| `taxonomy-standards-mapper` | completed | `stages/subagent-receipts/taxonomy-standards-mapper.md` |

## Residue

- `integration-spec` remains a good future package name, but not the first mutation.
- DomainSpec template extension and formula validator are both promotion candidates.
- New local vocabulary remains package-local until definitions-governance.
- External standards remain source authorities for protocol and wire shapes.
