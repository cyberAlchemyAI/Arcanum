---
name: observability-derivation
description: Derive a typed metric-obligation inventory from a DomainSpec spec's aspect docs (the doc->metrics rule method).
metadata:
  tier: arcana
  status: draft
  scope: repository-local
---

# Sigil: Observability Derivation

<objective>
From a feature's DomainSpec aspect docs, deterministically derive the set of observable obligations (metrics, gauges, SLOs) each structured behavior clause implies — a typed metric-obligation inventory, not instrumentation code.
</objective>

<logic-type>
Arcana: deterministic doc→metrics derivation. Produces a neutral metric-obligation inventory; instrumentation runtime (OTel/Prometheus code) is out of scope and stays in the product.
</logic-type>

<applicability>
Use when a feature has DomainSpec aspect docs and you need its observability obligations derived from the spec rather than hand-authored. M2-C4 of the DomainSpec capability pipeline.
</applicability>

<boundary>
This sigil derives the metric OBLIGATIONS (the rule method). It does NOT instrument code, emit OTel calls, or wire Prometheus — that runtime is private product. Output is a runtime-neutral obligation inventory any backend can satisfy.
</boundary>

<derivation-rules>
Each structured clause yields a typed obligation:
- **O1** every `states.md` transition row → 1 counter.
- **O2** each State Machine → 1 state-distribution gauge.
- **O3** each invariant → 1 runtime-assertion gauge.
- **O4** each Operation → 4 base metrics (count, duration, success, failure).
- **O5** each Operation rule → 1 rule-violation counter.
- **O6** each Calculation → 1 calc-drift gauge.
- **O7** each postcondition → 1 postcondition-check.
- **O8** each Interface → SLO (latency/availability) targets.
- **O9** idempotency-sensitive ops → 1 duplicate-suppression counter.
- **O10** each Event → 1 event-flow metric.
- **O11** each Query → 1 query-performance metric.
- **O12** each Workflow → completion/duration/compensation metrics.
- **O13** SPEC capabilities → business KPIs.
- **O14** stories → funnel metrics.
- **O15/O16** finance pillar (when present) → txn-integrity + reconciliation metrics.

Three-layer model for each obligation: **Domain Fidelity** / **Operational Health** / **Business Effectiveness**, with P0/P1/P2 alert tiers.
</derivation-rules>

<process>
1. Parse the aspect docs against the M2-CONTRACT shapes.
2. Apply O1–O16 to emit one typed obligation per matching clause, anchored to its source (`{aspect-file}#{anchor}`).
3. Tag each obligation with its layer (fidelity/health/effectiveness) and alert tier.
4. Emit the metric-obligation inventory. Do not generate instrumentation code.
</process>

<anti-patterns>
Avoid:
- emitting OTel/Prometheus/runtime code (out of scope — that is private product),
- deriving obligations for clauses not present in the spec,
- dropping the source anchor (obligations must be traceable),
- claiming the metrics are wired; this produces obligations, not instrumentation.
</anti-patterns>

<output-contract>
Return:

```markdown
## Observability Derivation

- Feature: <name>
- Obligations derived: <count> (by rule: O1..O16)
- Layers: fidelity <n> / health <n> / effectiveness <n>
- Alert tiers: P0 <n> / P1 <n> / P2 <n>
- Output: metric-obligation inventory (runtime-neutral)
- Unmatched clauses: <count>
```
</output-contract>
