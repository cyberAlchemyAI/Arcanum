# Glossary Consistency: Craft Row Update Planner Architecture

## Verdict

Status: `pass`

The architecture terms align with Craft's existing source-of-truth and
link/index contracts. No glossary, registry, or canonical definition promotion
is performed by this Invoke run.

## Term Map

| Term | Status | Meaning In This Bundle | Source Alignment |
| --- | --- | --- | --- |
| Craft ledger | linked | `.craft/ledger.yml`, authoritative project-local state. | Aligns with Craft storage contract. |
| Generated index | linked | `.craft/index.json`, rebuildable lookup surface. | Aligns with generated index non-authority rule. |
| Projection | linked | CSV/JSON derived view or staging surface. | Aligns with prior projection refine result. |
| Row selector | candidate-local | `{family, id}` pointer to exactly one ledger row. | Consistent with stable row ID policy. |
| Proposed delta | candidate-local | Typed field-level change proposed by CSV, CLI, form, or agent. | New architecture term; not canonical yet. |
| Row update planner | candidate-local | Deterministic dry-run primitive that emits patch/no-op/block reports. | New architecture term; owned by Craft proposal. |
| Patch plan | candidate-local | Ordered dry-run operation report, not direct mutation. | Consistent with YAML authority guardrail. |
| Stale source | candidate-local | Proposed edit's expected hash does not match current ledger bytes. | Consistent with generated projection freshness gates. |
| Read-only field | candidate-local | Projected field that first-slice planner may report but not change. | Consistent with nested evidence/link risk controls. |

## Conflicts

None blocking.

## Notes

- `row update planner` should remain candidate-local until implementation
  evidence proves the contract.
- `patch plan` must not be described as execution evidence or source authority.
- `proposed delta` should remain format-neutral so CSV import does not own the
  core reconciliation concept.
