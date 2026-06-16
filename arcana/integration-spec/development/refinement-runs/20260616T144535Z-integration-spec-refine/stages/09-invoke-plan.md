# Invoke Plan: Integration Boundary L0

Status: pass
Mode: plan
Capability: `invoke`
Complexity: medium

## Objective

Produce a non-executed plan for the first public-safe Integration Boundary proof without creating the final `integration-spec` package.

## Implementation Layering

| Layer | Question | Output |
| --- | --- | --- |
| L0 | Can the integration-boundary discipline describe the core problem and counterexample without taxonomy mutation? | discipline card plus minimum component catalog |
| L1 | Can DomainSpec authoring carry the surface? | candidate `integrations.md` aspect |
| L2 | Can a formula validator enforce completeness? | candidate validator schema/rules |
| L3 | Does repeated evidence justify `arcana/integration-spec`? | sigil-development decision gate |

## Work-Pack Sketch

| Task | Purpose | Owner Route | Validation |
| --- | --- | --- | --- |
| TASK-IBD-001 | Draft Integration Boundary Discipline card. | `discipline-governance` | public-boundary scan; component catalog review |
| TASK-IBD-002 | Draft DomainSpec integration aspect candidate. | `invoke` or `task-session` | template link and concept graph consistency |
| TASK-IBD-003 | Draft formula-level integration contract validator design. | `dispatch-spec` / formula route | fixture list for pass/flag/block cases |
| TASK-IBD-004 | Build counterexample proof package. | `research-evidence-harness` or `task-session` | payment API + webhook + cache + idempotency + reconciliation checklist |
| TASK-IBD-005 | Promotion review. | `decision-gate` then `sigil-development` if approved | bridge decisions and residue closure |

## SWU Suggestions

| SWU | Parent | Goal | Execution Owner |
| --- | --- | --- | --- |
| SWU-IBD-001 | TASK-IBD-001 | Create a discipline card with minimum components and owner boundaries. | local or subagent |
| SWU-IBD-002 | TASK-IBD-002 | Draft an `integrations.md` template without changing existing templates. | local or subagent |
| SWU-IBD-003 | TASK-IBD-003 | Define validator fields and three fixture cases. | local or subagent |
| SWU-IBD-004 | TASK-IBD-004 | Write the payment/provider/cache/webhook counterexample. | local or subagent |

## Validation Strategy

- `python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py` for dispatch artifacts.
- JSON syntax validation for any structured index or fixture.
- Public-boundary string scan for private paths and examples before staging public `arcanum` files.
- Link check for local artifact references.

## Next Route

Route to `discipline-governance` for TASK-IBD-001. Defer `sigil-development` for `integration-spec` until the L0 discipline, template candidate, validator candidate, and counterexample evidence exist.
