---
name: code-tag-audit
description: Deterministic code<->spec traceability — extract source tags, validate against a schema, and detect drift vs the spec.
metadata:
  tier: arcana
  status: draft
  scope: repository-local
---

# Sigil: Code Tag Audit

<objective>
Maintain a living traceability matrix between code and spec using deterministic tag tooling: annotate code symbols, extract the tags, validate them against a schema, and report drift between code tags and feature docs.
</objective>

<logic-type>
Arcana: deterministic code-annotation audit (validators/audits — the commodity wedge). No LLM in the audit path.
</logic-type>

<applicability>
Use when code carries (or should carry) docstring tags linking symbols to spec concepts, and you need a deterministic check that code and spec have not drifted. M2-C2 of the DomainSpec capability pipeline.
</applicability>

<capability>
Four deterministic operations over a configurable tag schema and feature root:
1. **extract** — scan source for docstring tags → a tag inventory (language adapters: js/ts/py).
2. **validate** — check the inventory against the tag schema (strict/warn; BLOCK on critical/high).
3. **drift** — compare code tags against the feature docs; emit a drift report.
4. **composability** — check that tags compose without conflict.
</capability>

<implementation-note>
The reference implementation is the DomainSpec deterministic TypeScript toolchain (`extract-code-tags`, `validate-code-tags`, `compare-code-tag-drift`, `check-code-tag-composability`). Porting it into arcanum requires decoupling the default tag-schema path and feature root (currently DS-specific) and verifying it builds/tests green — a code task needing the build runtime, tracked as M2-C2-impl. This SKILL defines the capability contract the tooling must satisfy.
</implementation-note>

<process>
1. Resolve the tag schema and feature root from project config (not hardcoded).
2. extract → validate → drift → composability, in that order.
3. In strict mode, BLOCK on critical/high validation or drift failures; otherwise flag.
4. Emit the tag inventory + validation + drift + composability reports. Read-only over source.
</process>

<anti-patterns>
Avoid:
- hardcoding DomainSpec-specific schema/feature paths,
- coupling the audit to any governance-engine logic,
- treating an LLM pass as a substitute for the deterministic checks,
- claiming traceability without the drift report as evidence.
</anti-patterns>

<output-contract>
Return:

```markdown
## Code Tag Audit

- Tags extracted: <count>
- Validation: pass | warn | block (<critical/high failures>)
- Drift: <count> (code-vs-doc)
- Composability: pass | fail
- Verdict: PASS | FLAG | BLOCK
- Reports: <paths>
```
</output-contract>
