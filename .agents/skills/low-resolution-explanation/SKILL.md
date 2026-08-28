---
metadata:
  surface_kind: generated-native-runtime-package
  runtime: codex
  canonical_source: transmutations/low-resolution-explanation/SKILL.md
  alias_of: null
  generated_by: tools/bootstrap_arcanum.sh --profile
  mutation_policy: regenerate-from-canonical-source
name: low-resolution-explanation
description: Write or review a human-facing low-resolution explanation with the minimum distinctions a specific reader needs. Use for orientation in chat or standalone text, or to identify premature detail and unsupported claims.
---

# Low-Resolution Explanation

<objective>
Explain why an object matters and how it approaches its problem using the
fewest distinctions the reader needs. Minimum sufficiency is not maximum
compression.
</objective>

<entry>
Consume the reader, purpose, delivery context, evidence limits, and epistemic
and systemic analysis supplied by `resolution-router`.

Redirect to `../resolution-router/SKILL.md` when that context or either required
perspective is missing, or when the reader must predict, operate, compare,
validate, design, or implement. Do not require serialized intermediate
artifacts.
</entry>

<writing-rules>
- Begin with the reader's need, then explain the object's objective and central
  relation.
- Distinguish demonstrated results from intentions, interpretations,
  hypotheses, and open questions.
- Use epistemic analysis to bound claims and systemic analysis to preserve
  relevant state, change, constraints, feedback, and downstream effects.
- Introduce terminology, examples, and implementation only when they improve
  understanding.
- Preserve material branching, recurrence, boundaries, and uncertainty.
- Use shared context in conversation; make standalone text self-contained.
- Keep lens names and routing machinery out of the prose unless useful to the
  reader.
</writing-rules>

<process>
Draft the explanation, check it against the evidence and both required
perspectives, then remove unnecessary concepts, catalogues, repetition, and
premature implementation detail.
</process>

<output>
Return natural human-facing prose. Mention deferred concepts and uncertainty
only when material.
</output>

<review>
When reviewing an existing explanation, read
`references/low-resolution-review.md` completely and follow it.
</review>
