---
name: resolution-router
description: Choose low, medium, or high resolution for a human explanation based on what a specific reader needs to understand or do, then execute the corresponding installed writer. Use for explanations in chat or standalone texts, explicit resolution requests, and writer redirects.
---

# Resolution Router

<objective>
Produce a human-readable explanation at the lowest resolution that lets the
intended reader correctly accomplish the intended purpose.

Resolution controls the distinctions the reader must understand. It is not a
word-count target, output format, or proxy for technical vocabulary.
</objective>

<ownership>
Act as the entrypoint for reader-facing explanations. Own reader-purpose
binding, resolution selection, delivery-context binding, required-lens routing,
writer selection, and same-turn writer execution. `lens-router` owns applying
the required perspectives; writers own the explanation at their selected tier.

Do not require JSON, schemas, digests, packets, plans, or persisted intermediate
artifacts to produce an explanation.
</ownership>

<authority>
Read `references/routes.md` to resolve the lens router and writers, and
`references/resolution-guarantees.md` to distinguish the cumulative tiers.
When changing routes, guarantees, or writers, read `references/validation.md`
and run its applicable checks before enabling a route.
</authority>

<inputs>
Determine from the request and available context:

- the object to explain;
- the intended reader;
- what the reader should understand or be able to do;
- the evidence available and its material limits;
- terms the reader already knows and terms whose precise meaning matters;
- whether delivery is conversational or standalone;
- an optional requested resolution.

Ask only when a missing distinction would materially change the result and
cannot be responsibly inferred. An explicit resolution is a minimum: never
silently downgrade it.
</inputs>

<delivery-context>
Resolution and delivery are independent. Conversational explanations may use
shared context and answer incrementally while satisfying the current request.
Standalone explanations must carry enough context, definitions, transitions,
evidence qualifications, and closure to work without the surrounding chat.
Delivery does not by itself promote or lower resolution.
</delivery-context>

<routing-rule>
Choose the tier by the reader's required action:

- `low`: orient, understand the rationale and central relation, or know what to
  ask next;
- `medium`: predict, operate, troubleshoot, compare, decide, or apply several
  interacting boundaries and assumptions;
- `high`: inspect, validate, challenge, design, or implement mechanisms,
  interfaces, failure behavior, and edge cases.

Choose the lowest sufficient tier. If the purpose requires a higher tier,
promote the whole explanation and state the human-readable reason. Higher
resolution permits more distinctions, never stronger unsupported claims.
</routing-rule>

<lens-rule>
After selecting resolution, invoke `lens-router` with the cumulative lens set:

- low requires epistemic and systemic;
- medium requires epistemic, systemic, and categorical;
- high requires epistemic, systemic, and categorical.

The epistemic view keeps claims inside their evidence. The systemic view keeps
state, change, constraints, and downstream effects visible. Medium adds the
categorical view because operational comparison and decision require clearer
entities, relations, transformations, interfaces, preservation, and loss. High
inherits all three.

Lenses guide analysis but do not dictate visible headings or terminology in the
human explanation.
</lens-rule>

<evidence-discipline>
Use the evidence actually available. Distinguish observation, supported
interpretation, intended behavior, hypothesis, and open question whenever the
difference matters. Preserve uncertainty that can change the reader's action.

Use the required lens analysis without forcing a serialized handoff. If prior
analysis covers every required lens over the same object, purpose, and evidence,
reuse it; otherwise invoke `lens-router` for the missing perspectives.
</evidence-discipline>

<execution>
1. Bind reader, purpose, delivery context, and evidence limits.
2. Select the lowest sufficient resolution and explain any promotion.
3. Resolve and invoke `lens-router` with the tier's required perspectives.
4. Resolve the exact writer in `references/routes.md`.
5. If unavailable, report the selected resolution and missing writer; do not
   silently downgrade or fabricate another tier.
6. If available, read its `SKILL.md` completely and invoke it in the same turn
   with the original request, bound context, selected resolution, route reason,
   and lens analysis notes.
</execution>

<direct-entry-rule>
A writer invoked without enough reader-purpose context or the perspectives
required by its tier redirects here with its own tier as the requested minimum.
A writer with sufficient context and analysis proceeds directly; no packet or
plan is required.
</direct-entry-rule>

<output-contract>
Return the selected writer's human-facing result. Keep routing notes compact and
outside the explanation, including them only for a consequential promotion,
evidence limitation, unavailable route, or uncertainty.
</output-contract>

<quality-bar>
A successful explanation fits the reader, purpose, and delivery context; uses
the lowest sufficient resolution; applies every perspective required by that
tier; stays within the evidence; preserves material relations and uncertainty;
executes exactly one available writer or reports one unavailable route; and
prioritizes human comprehension over bookkeeping.
</quality-bar>

<anti-patterns>
Avoid treating resolution as length, forcing schemas into ordinary explanation
work, exposing internal guarantee IDs, producing machine-shaped prose, silently
downgrading an unavailable tier, or using detail to imply unsupported certainty.
</anti-patterns>
