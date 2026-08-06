# TASK-PEP-CONTRACT: Pre-execution contract

## SWU-PEP-001

Primary behavior: define typed prerequisite and classification contracts.

### Inputs

- `SPEC.md` core types and authority rules;
- current Task Session and Continuation Router receipt identities;
- current Invoke Refresh mutation-mode and material-package contracts.

### Outputs

- `pre-execution-owner-prerequisite.schema.json`;
- `pre-execution-prerequisite-receipt.schema.json`;
- positive and adversarial schema fixtures;
- a deterministic fixture validator.

### Ordered rules

1. Bind prerequisite, task, SWU, attempt, owner route, target inventory, validation contracts, expected receipt, satisfaction predicate, resume point, and hop budget.
2. Restrict `max_owner_hops` to one and `resume_point` to `task-session:context-build`.
3. Separate route declaration from authorization evidence.
4. Require a stable fingerprint input set.
5. Represent `satisfied|unmet|ambiguous|stale|invalid` without collapsed booleans.
6. Reject unrelated effect classes such as promotion, publication, deployment, destructive action, policy acceptance, and cost acceptance.

### Edge and failure cases

- missing target inventory;
- extra authorized path;
- unknown owner route;
- ambiguous source selector;
- proposal/no-op receipt without a matching satisfaction predicate;
- repeated attempt/fingerprint;
- legacy untyped prerequisite routed to the adapter, not silently accepted.

### Split analysis

Schema and schema fixtures form one independently reviewable contract. Runtime classification is separate in `SWU-PEP-002`.

### Validation

```bash
python3 arcanum/arcana/task-session/development/pre-execution-prerequisite-fast-path/validate-fixtures.py --group schema
```
