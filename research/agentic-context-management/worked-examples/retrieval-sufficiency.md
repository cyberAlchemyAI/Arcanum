# Worked Example: Relevant Hit, Insufficient Reasoning

Source kind: `operator-reading` derived from paper §3.3.

Question:

```text
Why was deployment D-42 rolled back, and is the old rationale still valid?
```

Retrieved item A:

```text
D-42 was rolled back after error rate exceeded the release threshold.
```

Item A is highly relevant, but it cannot answer the second clause. The reasoning
chain also needs:

- item B: the decision record naming the original threshold and rationale;
- item C: the later policy revision that superseded that threshold;
- item D: provenance and timestamps establishing the order.

## Metric Consequence

A hit-based metric may score item A as success. A sufficiency-aware fixture must
require `{A, B, C, D}` or an equivalent evidence set and distinguish:

```text
missing evidence
wrong scope
stale evidence
reasoning failure despite sufficient evidence
```

## Boundary

This example illustrates the distinction; it is not evidence that the paper's
reference system retrieves all bridge items.
