# Stage 5: Distill

Status: pass.

## Selected Smallest Coherent Unit

Add one new technique family:

```text
Runtime Bridge And Evidence Techniques
```

## Why This Unit

The current catalog already covers:

- route composition,
- standards-catalog discipline,
- validation/data-quality style checks.

The Tandem research introduces a different concern: how a dispatch route should describe boundary crossings into runtime execution, approval, evidence, audit, memory, and external plan projection. That concern is coherent enough to name, but not large enough to justify a schema change yet.

## Rejected Alternatives

| Alternative | Reason Rejected |
| --- | --- |
| Add Tandem-specific techniques only | Too coupled to one runtime; dispatch-spec should stay runtime-agnostic. |
| Add schema fields immediately | Premature; technique refs can prove vocabulary before schema hardening. |
| Fold bridge techniques into POLE-inspired standards techniques | Blurs standards catalog discipline with runtime authority crossings. |
| Create a Tandem adapter now | Execution belongs to Task Session next route, not this refine pass. |
