# Local Distill: Smallest Coherent Schema Unit

Status: flag
Owner: refine fallback synthesis
Reason: `distill` command surface resolved, but semantic execution used dry-run evidence only.

## Selected Unit

The smallest coherent unit is:

> An optional dispatch-level `boundary_evidence` object that declares boundary
> claims, authority owners, evidence receipts, state namespace rules, and
> promotion splits for the route.

## Rejected Alternatives

| Alternative | Rejection Reason |
| --- | --- |
| Rename only the technique family | Fixes wording but does not make claims inspectable. |
| Add a runtime adapter block | Reintroduces the Tandem/runtime drift the user corrected. |
| Add fields directly to every step | Too noisy; route-level invariants should be declared once and referenced by steps when needed. |
| Make receipts required globally | Too strict for exploratory dispatches and route planning. |

## Recomposition Requirement

`boundary_evidence` must connect back to:

- `techniques`, especially generalized boundary/evidence technique ids;
- `steps`, through optional boundary references or step ids;
- `gates`, through authority and approval validation;
- `observability`, through receipt and trace references;
- `promotion_guardrails`, through explicit no-promotion claims.
