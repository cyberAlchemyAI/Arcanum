# Constitution Governance

Constitution Governance is an Arcana sigil for creating, selecting, composing, and validating modular constitutions.

It exists because constitutions are pattern enforcers for structure and form. They lose force when every rule is poured into one large file and loaded wholesale into every task. A constitution should be small enough to apply pressure, explicit enough to validate, and composable enough to travel with the work that needs it.

## Problem It Solves

A repository can accumulate many governance rules:

- artifact rules,
- chart rendering rules,
- validation rules,
- ontology branch rules,
- implementation planning rules,
- runtime evidence rules,
- presentation or document form rules.

If those rules live in one large constitution, agents either load too much context or ignore the parts that matter. If rules live only in memory, they do not reliably affect artifacts. Constitution Governance keeps constitutions modular, selects the relevant ones for a task, composes them into a small enforcement pack, and routes enforceable rules into validators or review checks.

## Core Stance

Context Builder is necessary but not sufficient.

Context Builder should select the constitutions relevant to a task. Constitution Governance should decide how selected constitutions compose, which rules are enforceable, which validators must run, and which conflicts require a decision gate.

```text
task intent
  -> select relevant constitutions
  -> compose minimal constitution pack
  -> identify enforceable rules
  -> update or require validation adapters
  -> execute task with focused governance context
  -> report pass, flag, block, or proposed constitution change
```

## Use When

- a new constitution or governance rule is needed,
- an existing constitution is growing too large,
- a task needs only selected constitution rules in context,
- multiple constitutions may conflict or overlap,
- a constitution rule should be enforced by a validator,
- a validation script should be updated after a constitution change,
- a governance rule should become canonical inside Arcanum.

## Do Not Use When

- a one-line local note is enough,
- the rule has no expected reuse or enforcement path,
- the task only needs ordinary Context Builder evidence selection,
- a validator change is purely mechanical and the constitution already exists,
- a decision gate is required and no acceptable default exists.

## Core Concepts

- Constitution: a durable governance artifact that enforces structure, form, or artifact behavior.
- Rule: one enforceable or reviewable requirement inside a constitution.
- Selector: a task-to-constitution matching condition.
- Composition pack: the minimal selected set of constitutions and rules for a task.
- Validation adapter: a script, lint rule, review checklist, or test that enforces one or more rules.
- Authority boundary: the owner, scope, and promotion state that say where the rule applies.
- Context load budget: the maximum governance context that should be loaded before rule force decays.

## Outputs

The sigil can produce:

- constitution proposal,
- constitution split plan,
- constitution composition pack,
- constitution selection map,
- validation adapter plan,
- validator update checklist,
- conflict report,
- decision gate packet,
- promotion readiness report.

## Integration

Use [context-builder](../../transmutations/context-builder/) to select task-relevant constitution excerpts and evidence.

Use [decision-gate](../decision-gate/) when constitution scope, precedence, conflict resolution, or canonical promotion needs human choice.

Use [inventory](../inventory/) to store source-backed constitution candidates or reusable evidence about recurring rule failures.

Use [sigil-development](../sigil-development/) when Constitution Governance itself is revised or promoted.

Use validators under [tools/](../../tools/) to enforce rules that can be checked deterministically.

## Why This Is Arcana

Constitution Governance coordinates long-lived rule authority across context selection, artifact form, validation, conflict handling, and promotion. It is not just a formatter or linter; it governs how rules are created, selected, composed, enforced, and retired.
