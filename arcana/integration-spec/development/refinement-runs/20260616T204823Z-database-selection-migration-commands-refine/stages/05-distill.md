# Distill: Coherent Unit

Status: pass
Owner capability: distill

## Selected Unit

The smallest coherent unit is a paired L0 model:

1. `Integration Data Resource Decision Record`
2. `Database Migration Command Profile`

Together they fill the DomainSpec practical gap without mutating DomainSpec canon.

## Distilled Model

```text
DomainSpec Operation/Query/Workflow
  -> Data Resource Boundary
  -> Integration Data Resource Decision Record
  -> selected Data Resource
  -> Database Migration Command Profile
  -> Evidence Anchors and Failure Fixtures
```

## Rejected Alternatives

| Alternative | Reason rejected |
| --- | --- |
| Put database families in DomainSpec taxonomy | DomainSpec canon is not the right owner yet. |
| Make migration commands DomainSpec operations | Migration commands are tool/runtime machinery, not business behavior. |
| Build validator first | Validator needs field schema and examples first. |
| Execute a migration proof now | Refine is non-executed design; live commands belong to task-session. |

## Recomposition

The two records can later feed `INTEGRATION-BOUNDARY-DISCIPLINE.md`, an `integrations.md` aspect, formula validator fixtures, and tool-specific profiles.
