# Refine Result: Role And Lifecycle Redundancy

Status: flag
Preset: compact
Research: no-research

## Finding

There is redundant vocabulary between `Lifecycle States` and `Candidate Role Semantics`, but not all of it is harmful.

The useful distinction is:

- lifecycle state answers: "how governed or relied-upon is this ontology object right now?"
- role semantic answers: "what kind of claim or governance function is this object playing?"

The current model states that roles do not automatically decide lifecycle status, which is the right guardrail. The redundancy becomes risky only if a future schema uses one field for both concepts.

## Redundancy Audit

| Term family | Current overlap | Evaluation | Recommended handling |
| --- | --- | --- | --- |
| `candidate` | State and role both use the same word. | True ambiguity. It can mean immature governance status or draft claim function. | Prefer `lifecycle_status: candidate`; replace role with `claim`, `candidateClaim`, or omit as a role. |
| `premise` | State and role both name a falsifiable working bet. | Mostly acceptable, but still dual-use. | Keep as role; consider whether lifecycle state should be `acceptedPremise` or `workingPremise`. |
| `policy` | State/outcome and role both describe decision rules. | Useful mirror. A policy can be a role before it becomes an accepted lifecycle outcome. | Keep both only if schema separates `role: policy` from `lifecycle_status: policy`. |
| `constitution` | State/outcome and role both describe enforceable governance. | Useful mirror, high-risk if collapsed. | Keep as promoted/outcome state; role can remain `constitutionalRule` or `constitutionCandidate`. |
| `axiom` | State/outcome and role both describe load-bearing commitments. | Useful mirror, high-risk if collapsed. | Keep role as `axiomCandidate` until accepted; reserve state `axiom` for committed reliance. |
| `contradiction` / `contradicted` | Role names the finding; state names lifecycle effect. | Healthy distinction with naming asymmetry. | Keep both; schema should allow `role: contradiction` and `lifecycle_status: contradicted`. |
| `retirement` / `retired` | Role names the decision/action; state names final condition. | Healthy distinction with naming asymmetry. | Keep both; schema should allow retirement records to result in retired status. |

## Distilled Boundary

Use four separate axes:

| Axis | Purpose | Example values |
| --- | --- | --- |
| `lifecycle_status` | Governance maturity and current reliance permission. | `raw`, `candidate`, `reviewed`, `promoted`, `retired`, `rejected` |
| `claim_role` | Function of the claim or record. | `hypothesis`, `observation`, `evidence`, `premise`, `policy`, `constraint`, `invariant`, `contradiction`, `retirement` |
| `governance_outcome` | Accepted special consequence when applicable. | `policy`, `constitution`, `axiom` |
| `bridge_outcome` | Cross-branch validation result. | `aligned`, `partial`, `drift`, `insufficient`, `contradicted` |

This avoids forcing terms such as `policy`, `constitution`, and `axiom` to be both the role and the lifecycle status.

## Suggested Source Model Refinement

Do not delete the candidate role catalog. It is valuable.

Before creating a schema, add a short boundary note near `Candidate Role Semantics`:

> Role semantics classify what a record is doing; lifecycle states classify its governance maturity and permitted reliance. Some words intentionally recur, but future schemas should keep these as separate axes.

Then adjust the role list only where ambiguity is highest:

- remove or rename role `candidate`;
- consider `axiomCandidate` and `constitutionCandidate` if examples show agents confusing roles with accepted outcomes;
- leave `contradiction` and `retirement` as roles because they name records/actions, not final states.

## Schema Implication

The next schema should not use a single `type`, `kind`, or `status` field to carry all of this. It should require separate fields or explicitly optional axes:

```yaml
lifecycle_status: candidate
claim_role: hypothesis
governance_outcome: null
bridge_outcome: insufficient
```

Promotion should update `lifecycle_status` or `governance_outcome`, not silently rewrite `claim_role`.

## Final Synthesis

The current text is acceptable as exploratory prose, but it is not schema-ready. The redundancy should be treated as a schema-design warning, not as a reason to collapse the role catalog.

Recommended next route: draft a candidate schema section that separates lifecycle status, claim role, governance outcome, and bridge outcome.
