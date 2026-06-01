# Design: Constitution Governance Sigil

Status: candidate
Date: 2026-05-27
Authoring route: invoke design, materialized locally

## View 1: Context

```text
user/task intent
  -> Context Builder selects relevant constitution sources
  -> Constitution Governance composes selected rules
  -> Decision Gate resolves blocker conflicts
  -> validators enforce deterministic rules
  -> task executes with focused governance context
  -> failures feed constitution updates or validator updates
```

## View 2: High-Level Structure

| Part | Responsibility |
| --- | --- |
| Constitution catalog | Finds available constitutions and their selection predicates. |
| Selection handoff | Receives or requests Context Builder evidence for task-relevant rules. |
| Composition engine | Produces minimal rule pack, precedence, exclusions, and conflicts. |
| Validation mapper | Maps rules to deterministic, review, hybrid, or missing validators. |
| Promotion gate | Routes canonicality, scope, or conflict choices through Decision Gate. |
| Maintenance loop | Splits bloated constitutions and retires stale rules. |

## View 3: Low-Level Components

| Component | Input | Output |
| --- | --- | --- |
| `create` mode | rule idea or artifact concern | candidate constitution |
| `add-rule` mode | rule and target constitution | patch or proposal with validator impact |
| `select` mode | task and constitution catalog | selected rule list |
| `compose` mode | selected rules | composition pack |
| `validate` mode | artifact and composition pack | pass/flag/block result |
| `split` mode | oversized constitution | modularization plan |
| `promote` mode | candidate rule/constitution | promotion readiness packet |

## View 4: Workflow

1. Identify task or artifact type.
2. Gather constitution candidates.
3. Select only relevant rules.
4. Compose selected rules by scope and precedence.
5. Identify conflicts and validator requirements.
6. Block on unresolved precedence/canonicality decisions.
7. Run validators or prepare review checklist.
8. Report pass, flag, block, or proposed constitution mutation.

## View 5: Decision Flow

```text
Need governance rule?
  -> local note enough? stop
  -> reusable rule? create/add-rule
  -> task needs rules? select
  -> selected rules interact? compose
  -> conflict? decision-gate
  -> deterministic check possible? validation adapter
  -> no validator? mark none-yet and block promotion
```

## View 6: Dependency Interface

| Dependency | Contract |
| --- | --- |
| Context Builder | Select constitution evidence; does not compose or enforce. |
| Decision Gate | Resolve blocker precedence, scope, and canonicality decisions. |
| Inventory | Store source-backed recurring failures or constitution candidates. |
| Sigil Development | Own lifecycle mutation of this sigil. |
| Tools validators | Enforce deterministic constitution rules with actionable failures. |

## Design Verdict

Status: pass.

The sigil is justified because the workflow coordinates context selection, composition, validation mapping, conflict handling, and promotion. A single validator or Context Builder call would be too small.
