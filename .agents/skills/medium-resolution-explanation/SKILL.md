---
metadata:
  surface_kind: generated-native-runtime-package
  runtime: codex
  canonical_source: transmutations/medium-resolution-explanation/SKILL.md
  alias_of: null
  generated_by: tools/bootstrap_arcanum.sh --profile
  mutation_policy: regenerate-from-canonical-source
name: medium-resolution-explanation
description: Write or review a human-facing medium-resolution explanation that lets a specific reader predict, operate, troubleshoot, compare, or decide. Use for conversational or standalone operational understanding beyond basic orientation.
---

# Medium-Resolution Explanation

<objective>
Give the reader a usable operational model of the object: enough parts, states,
relations, boundaries, assumptions, alternatives, and consequences to reason
about what happens and make the intended decision or action.
</objective>

<entry>
Inherit the low-resolution foundation and its epistemic and systemic analysis,
then add the categorical analysis supplied by `resolution-router`. Consume the
same reader, purpose, delivery context, and evidence limits across all three
perspectives.

Redirect to `../resolution-router/SKILL.md` when that context or any required
perspective is missing, or when the reader must inspect, validate, challenge,
design, or implement mechanisms and failure behavior. Do not require serialized
intermediate artifacts.
</entry>

<writing-rules>
- Preserve low-resolution orientation: begin from the reader's need, objective,
  and central relation before expanding the model.
- Expose the parts, states, interactions, and transitions needed to predict or
  operate the object; do not enumerate everything available.
- Make material boundaries, assumptions, dependencies, and authority limits
  explicit where they affect action.
- Show alternatives, trade-offs, or downstream consequences needed for the
  stated comparison or decision.
- Keep epistemic analysis to bound claims and systemic analysis to preserve
  dynamics and consequences. Add categorical analysis to clarify entities,
  relations, transformations, interfaces, preservation, and loss.
- Connect the model selectively to examples and implementation without turning
  the explanation into an exhaustive inspection.
- Use shared context in conversation; make standalone text self-contained.
- Keep lens names and routing machinery out of the prose unless useful to the
  reader.
</writing-rules>

<process>
Draft a coherent operational explanation, test whether the reader can use it for
the stated prediction, operation, comparison, diagnosis, or decision, then
remove distinctions that do not change that capability. Preserve consequential
uncertainty and unresolved questions.
</process>

<output>
Return natural human-facing prose. Use headings, examples, tables, or diagrams
only when they materially improve the reader's operational understanding.
</output>

<review>
When reviewing an existing explanation, read
`references/medium-resolution-review.md` completely and follow it.
</review>
