# Test Derivation — engine (L0)

Reference implementation for the [test-derivation](../SKILL.md) sigil (M2-C3). **Built fresh in Arcanum** (decision B3) — no DomainSpec engine code ported. Deterministic, no LLM, no network. Run with `tsx`.

## L0 scope (implemented + verified)
The **state-transition rule**: each transition-table row in a DomainSpec `states.md` → one content-addressed existence-test obligation.

```
tsx derive.ts --states <states.md> --out <TEST-SPEC.md>   # derive
tsx derive.ts --states <states.md> --check <TEST-SPEC.md> # round-trip oracle (engine ⊇ committed)
```

Verified in-repo: deterministic (identical output across runs), round-trip oracle PASS, keys are `sha1(anchor|rule|params)`.

## Next layers (M2-C3 expansion)
- invalid-transition cardinality `(non-terminal states × events − valid)`, lexicographically ordered
- operation rules → presence/range/count-cap test cardinalities
- richer `TEST-SPEC` emit + runnable test scaffolds

Each new rule type keeps the determinism + round-trip-oracle discipline.
