---
metadata:
  surface_kind: generated-native-runtime-package
  runtime: codex
  canonical_source: transmutations/lens-router/SKILL.md
  alias_of: null
  generated_by: tools/bootstrap_arcanum.sh --profile
  mutation_policy: regenerate-from-canonical-source
name: lens-router
description: Select, apply, and compose epistemic, systemic, and categorical perspectives over an object without requiring structured packets or schemas. Use when explanation routing, research, review, or design needs evidence-aware analysis before a human-facing result.
---

# Lens Router

<objective>
Inspect an object through the required investigative perspectives and return
concise analysis notes that downstream work can use directly.

A lens controls what becomes salient and which inferential jumps to avoid. It
does not prove that the inspected object contains the structure the lens seeks.
</objective>

<ownership>
Own lens selection when the caller has not fixed it, reference loading,
independent lens application, and multi-lens composition. Do not choose
explanation resolution or write the final reader-facing explanation.

Do not require JSON, schemas, digests, packets, or persisted intermediate
artifacts.
</ownership>

<lens-map>
- `epistemic`: claims, evidence, uncertainty, justification, authority,
  permission, and what may responsibly be believed or done;
- `systemic`: state, change, constraints, feedback, recurrence, downstream
  effects, and local-to-global consequences;
- `categorical`: relevant things, relations, transformations, composition,
  interfaces, transport, preservation, and loss.
</lens-map>

<inputs>
Use the object, reader or consumer, purpose, available evidence and its limits,
known or precision-sensitive terms, any explicitly required lenses, and the
consequence of getting the analysis wrong. Infer what is clear from context.
</inputs>

<selection-policy>
Honor lenses fixed by the caller. Otherwise select only perspectives whose core
questions can materially change what the consumer can understand, verify,
decide, implement, or ask next.

- use `epistemic` for claim support, uncertainty, falsification, authority,
  approval, or permission;
- use `systemic` for state transitions, constraints, feedback, recurrence,
  closure, or local-to-global effects;
- use `categorical` for type boundaries, relations, transformations,
  interfaces, composition, equivalence, preservation, or loss.

When invoked by `resolution-router`, follow its cumulative policy exactly:

- low: epistemic and systemic;
- medium: epistemic, systemic, and categorical;
- high: epistemic, systemic, and categorical.
</selection-policy>

<reference-loading>
Before analysis, read each selected reference completely:

- epistemic -> `references/epistemic.md`;
- systemic -> `references/systemic.md`;
- categorical -> `references/categorical.md`.

When two or more lenses are selected, finish each independent view before
reading and applying `references/composition.md`.
</reference-loading>

<process>
1. Bind the object, purpose, reader, evidence limits, and required lenses.
2. Load and apply each lens independently to the same object and evidence.
3. Keep only findings that can change understanding or action.
4. Preserve the evidence basis, claim status, and material uncertainty for each
   finding in concise prose notes.
5. Compose cross-lens relations only after the independent views are complete.
6. Preserve material findings even when they do not participate in composition.
7. Return the analysis to the caller without choosing resolution or writing the
   final explanation.
</process>

<invariants>
- Keep every claim at or below its evidence.
- Do not infer authority from evidence, causality from sequence, or correctness
  from successful execution.
- Do not infer composability, equivalence, reversibility, or preservation from
  adjacency or forward movement.
- Preserve hypotheses, conflicts, and uncertainty that can change the result.
- Keep lens vocabulary out of the final reader-facing prose unless useful to
  the stated purpose.
</invariants>

<output-contract>
Return concise analysis notes containing:

- the lenses used;
- the few load-bearing findings from each lens;
- their evidence basis or explicit evidentiary limitation;
- material cross-lens relations;
- remaining uncertainty and open questions.

This is an internal reasoning handoff, not a prescribed user-facing format.
Downstream skills may consume it directly without serialization.
</output-contract>

<quality-bar>
Every required lens was applied independently; findings remain evidence-bounded;
composition adds relations without replacing individual findings; material
uncertainty survives; and the result is concise enough to support downstream
human writing without becoming that writing.
</quality-bar>

<anti-patterns>
Avoid selecting all lenses without reason outside resolution routing, forcing
machine-shaped records, letting one lens rewrite another before composition,
reconstructing missing evidence, silently expanding the evidence boundary, or
writing the final explanation inside this skill.
</anti-patterns>
