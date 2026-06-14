---
name: test-derivation
description: Deterministically derive a test-obligation spec from a DomainSpec feature's aspect docs (no LLM in the derivation path).
metadata:
  tier: arcana
  status: draft
  scope: repository-local
---

# Sigil: Test Derivation

<objective>
Turn a feature's DomainSpec aspect docs into a complete, content-addressed test-obligation spec — deterministically, so the same spec always yields the same obligations.
</objective>

<logic-type>
Arcana: deterministic spec→test derivation. The derivation function is pure; no LLM, no network in the obligation path.
</logic-type>

<applicability>
Use when a feature has DomainSpec aspect docs and you need its test obligations derived (not hand-written), with reproducibility and a coverage oracle. M2-C3 of the DomainSpec capability pipeline.
</applicability>

<method>
1. Parse the canonical aspect docs into a typed concept graph G (nodes = DS-D1 meta-types, edges = DS-D2 verbs).
2. Apply a pure total rule function δ(G, Δ) with exact cardinalities, e.g.:
   - state-transition row → existence test (1),
   - invalid-transition set → (non-terminal states × events − valid), lexicographically ordered,
   - presence rule → one test per conjunct,
   - range rule → boundary tests (4),
   - count cap → (2).
3. Content-address each obligation: `sha1(source_anchor | rule_type | canonical_params)` — stable, reproducible.
4. Emit a byte-stable `TEST-SPEC.md` (+ runnable tests).
5. **Round-trip oracle (L0):** the engine-derived obligation set must be a superset of the committed set ⇒ PASS; a missing obligation ⇒ the committed spec drifted.
</method>

<build-discipline>
Per decision B3, the engine is **built fresh in arcanum** — the private DomainSpec `test-derivation-engine/` skeleton is a design reference only; no DS engine code is ported. Layer the build: L0 = one rule type end-to-end (state-transition → existence test) with the round-trip oracle, then expand cardinalities. Implementation is tracked as M2-C3-impl (needs the build runtime); this SKILL defines the derivation contract.
</build-discipline>

<anti-patterns>
Avoid:
- introducing an LLM or network call into the derivation path (determinism is the property),
- non-stable obligation keys (must be content-addressed),
- porting the private DS engine code (build fresh — B3),
- claiming coverage without the round-trip oracle.
</anti-patterns>

<output-contract>
Return:

```markdown
## Test Derivation

- Feature: <name>
- Obligations derived: <count> (by rule type)
- Determinism: content-addressed keys | round-trip oracle <pass/fail>
- Output: TEST-SPEC.md (+ tests)
- Coverage: engine ⊇ committed? <yes/no>
```
</output-contract>
