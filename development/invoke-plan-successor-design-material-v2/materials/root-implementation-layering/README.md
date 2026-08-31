# Implementation Layering

Implementation Layering is a Transmutation sigil for turning an implementation goal into a staged build model.

It helps an agent or team avoid stuffing every concern into the first version. Instead, it defines Layer 0 as the smallest useful proof, then describes later layers that add repeatability, reliability, governance, scale, or packaging only when the evidence justifies them.

## Problem It Solves

Implementation plans often blur proof, hardening, pilot readiness, and productization into one oversized first step. That makes progress harder to verify and makes it unclear which decision the next work unit is supposed to unlock.

This sigil solves that by forcing each layer to answer a decision question:

```text
After this layer, we know whether ...
```

The result is an implementation path where scope grows because evidence unlocked the next decision, not because every desirable feature was bundled into the beginning.

## Use When

- a feature, workflow, or system improvement needs a practical build sequence,
- the first version is at risk of becoming too large,
- the team needs to separate proof, hardening, and scale concerns,
- there are known constraints around time, reliability, compliance, migration, or pilot readiness,
- reviewers need to understand why some work is included now and some is deferred.

## Do Not Use When

- the task is already a tiny deterministic edit,
- the work has no meaningful implementation sequence,
- the user needs a final architecture decision rather than staged execution,
- the main uncertainty is factual discovery rather than implementation scope.

## Inputs

Useful inputs include requirement notes, specs, issues, roadmap items, existing implementation files, tests, constraints, and stakeholder goals.

The sigil can still operate with partial context, but it should mark unresolved assumptions as open decisions rather than silently treating them as facts.

## Output

The primary output is an implementation layering artifact with:

- a Layer 0 minimum working unit,
- 3 to 5 decision-oriented layers,
- included and deferred scope for each layer,
- exit evidence and promotion decisions,
- non-regression guardrails,
- a recommended next layer.

## Why This Is A Transmutation

The sigil applies structured judgment to ambiguous planning material. It does not merely validate a fixed structure, and it does not coordinate autonomous multi-agent inquiry. Its job is bounded synthesis: transform rough implementation intent into a reviewable staged plan.