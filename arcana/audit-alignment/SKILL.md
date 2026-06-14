---
name: audit-alignment
description: Audit implementation fidelity against a DomainSpec spec and produce a classified alignment report.
metadata:
  tier: arcana
  status: draft
  scope: repository-local
---

# Sigil: Audit Alignment

<objective>
Compare an implementation against its DomainSpec spec and report, per spec obligation, whether the code is compliant, partial, missing, or has undocumented extras — with prioritized remediation.
</objective>

<logic-type>
Arcana: spec-vs-implementation fidelity audit. Read-only over code; produces an evidence-classified verdict, not a mutation.
</logic-type>

<applicability>
Use when a feature has a DomainSpec `SPEC.md` + aspect docs and implementation code exists, and you need to know how faithfully the code realizes the spec. M2-C6 of the DomainSpec capability pipeline.
</applicability>

<boundary>
This sigil audits spec↔code fidelity ONLY. It must not import or depend on the CyberAlchemy governance chain, promotion-DAG, or KPI taxonomy (those are private moat). It reads the public DomainSpec spec interface (`M2-CONTRACT`) and the code; nothing else.
</boundary>

<inputs>
- a feature `SPEC.md` + aspect docs (operations/queries/interfaces/states/events/mappings),
- the implementation code paths for that feature,
- optionally prior audit reports or test evidence.
</inputs>

<process>
1. Extract expected obligations from the spec: each Operation's rules/calculations/state-transitions/postconditions/error-states; each Query's output+authz; each Interface contract; each State Machine transition; each Event.
2. Locate the realizing code for each obligation (by concept ID, code tag, or name).
3. Classify each obligation:
   - **compliant** — code implements it and tests/evidence confirm,
   - **partial** — implemented but incomplete (missing edge case, error state, or postcondition),
   - **missing** — no realizing code found,
   - **extra** — code behavior with no spec obligation (possible scope creep or undocumented behavior).
4. Assign each non-compliant item a severity (critical/high/medium/low) by domain impact.
5. Produce a prioritized remediation list: for each gap, the spec obligation, the code location (or absence), and the smallest fix.
6. Do not mutate code or spec; this is an audit. Route fixes to `task-session`.
</process>

<anti-patterns>
Avoid:
- importing governance-chain / promotion logic (moat boundary),
- treating absence of tests as automatic non-compliance without inspecting code,
- silently merging "extra" behavior into the spec,
- reporting a verdict without per-obligation evidence,
- claiming bug-reduction; frame findings as "relocated, legible review" (R-IB-1).
</anti-patterns>

<output-contract>
Return:

```markdown
## Alignment Audit

- Feature: <name>
- Obligations: <total>
- Compliant / Partial / Missing / Extra: <c> / <p> / <m> / <e>
- Critical gaps: <count>
- Remediation (prioritized): <ordered list of obligation → location → fix>
- Verdict: PASS | FLAG | BLOCK
- Evidence: <per-obligation references>
```
</output-contract>
