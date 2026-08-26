---
name: low-resolution-explanation
description: Write or review an evidence-bounded low-resolution explanation with the minimum distinctions a specific reader needs. Use when supplied a valid low resolution handoff, when explicitly invoked as $low-resolution-explanation, or when reviewing an existing explanation for premature detail, unearned concepts, unsupported claims, loose terms, catalogues, or implementation introduced before conceptual need. Natural-language requests to choose an explanation resolution belong to resolution-router.
---

# Low-Resolution Explanation

<objective>
Explain a complex object at the lowest resolution that still lets the intended
reader understand:

1. the need that makes the object relevant;
2. what the object is trying to achieve;
3. the smallest set of relations needed to understand its approach;
4. what those relations mean for the reader;
5. only then, how they appear in implementation.

The goal is minimum sufficient distinction, not maximum compression.
</objective>

<logic-type>
Transmutation: bounded evidence-grounded explanation synthesis and specialized
low-resolution critique for one consumer and purpose.
</logic-type>

<ownership>
Own reader-facing creation and specialized review at the low tier.

Do not select, apply, or compose lenses. Do not choose a resolution tier. Consume
the packet and plan produced by the sibling routers.
</ownership>

<entry-contract>
Normal creation requires the pair:

```text
{
  lens_packet,
  resolution_plan
}
```

Read these authorities completely before drafting:

- `../lens-router/references/lens-packet.md`;
- `../lens-router/references/lens-packet.schema.json`;
- `../resolution-router/references/resolution-plan.md`;
- `../resolution-router/references/resolution-plan.schema.json`;
- `../resolution-router/references/resolution-guarantees.md`;
- `../resolution-router/references/routes.md`.

Require `selected_resolution: low`, an available manifest target matching this
skill, and all `L01` through `L10` guarantee IDs. For JSON-compatible handoffs,
run `../lens-router/scripts/validate_lens_packet.py` and
`../resolution-router/scripts/validate_resolution_plan.py`, then run the
mandatory joint gate
`../resolution-router/scripts/validate_routing_handoff.py <packet> <plan>`
before drafting. Separate validator passes do not prove that the plan belongs
to the supplied packet.
If either validator reports its declared `jsonschema` dependency missing,
return that blocked state rather than skipping validation or installing the
dependency without user authority.

For creation, if either input is absent or invalid, read
`../resolution-router/SKILL.md` completely and invoke it with
`requested_resolution: low` plus the original user inputs. Do not repair the
handoff by selecting lenses locally. Do not redirect a complete valid input.

For an explicit review of an existing explanation, follow `<review-mode>`
instead. Review mode does not require a pre-existing resolution plan because
the target tier is fixed, but it still requires a valid lens packet and the low
guarantee authority.
</entry-contract>

<resolution-model>
Keep few distinctions active at once. Include a distinction only when omitting
it would materially change what the reader can correctly understand,
distinguish, verify, decide, or ask next.

The selected tier is the global minimum guarantee envelope, while detail may be
allocated unevenly across lens findings. This preserves lens-specific variation
without pretending that a low writer satisfies medium or high guarantees.
Allocation may change emphasis only; it may not introduce medium- or high-tier
guarantees into a nominally low explanation.

Prefer ordinary language, one conceptual move at a time, sparse examples, and
implementation names only after the underlying relation is understandable.
</resolution-model>

<evidence-use>
Use both `per_lens_findings` and `composed_findings` from the packet.

Composition never replaces individual findings. Keep a material single-lens
finding eligible even when it has no cross-lens relation. Select only the
minimum findings required for the consumer's purpose, but do not erase evidence
internally because the final prose is low resolution.

Do not expose lens names or lens-by-lens scaffolding unless the reader's purpose
requires them.
</evidence-use>

<claim-discipline>
Apply `claim <= evidence` sentence by sentence.

Match language to the packet status:

- state observed or implemented facts directly;
- identify supported interpretations as interpretations when material;
- describe product directions as objectives or intended behavior;
- label hypotheses and open questions;
- preserve uncertainty that changes the reader's understanding.

Do not turn aspiration into capability, evidence into authority, correlation
into causation, successful execution into correctness, or implementation
presence into demonstrated value.
</claim-discipline>

<reader-movement>
Build the explanation in this order:

1. Start with the concrete need or pressure, not an object definition.
2. Establish why the need matters to this consumer.
3. State what the object is trying to make possible, distinct from proven
   outcomes.
4. Introduce the first central mechanism in ordinary language.
5. Connect that mechanism back to the reader's need.
6. Use one small example only when it earns the next distinction.
7. Increase resolution one distinction at a time.
8. Introduce implementation as the place where an already understood relation
   appears.
</reader-movement>

<concept-budget>
- Avoid several unfamiliar named concepts in one paragraph.
- Prefer a relation explained in prose over a catalogue of components.
- Use at most two or three examples, and normally one.
- Do not add detail merely because it exists in the packet.
- Preserve reserved terms from the packet; do not use them as loose synonyms.
- Defer concepts not needed for the current purpose and report them as reserved
  for a higher-resolution pass when material.
</concept-budget>

<structure-fidelity>
Do not linearize load-bearing branching, recurrence, feedback, or local/global
effects merely to simplify the prose.

When relevant, distinguish whether local work can close independently, open
more work, invalidate a premise, redirect the larger route, or require evidence
before affecting global state.

Narrative order is not evidence of process order, causality, dependency, or
acyclicity. Recommend a diagram only when it materially improves understanding;
do not invent one from prose sequence.
</structure-fidelity>

<process>
1. Validate the packet and low resolution plan separately and as one bound
   handoff. Reject a digest, lens, finding, composition, consumer, purpose, or
   evidence-boundary mismatch instead of repairing it locally.
2. Read the consumer, purpose, evidence boundary, vocabulary constraints,
   findings, and uncertainty.
3. Identify the minimum material distinctions required by `L01` through `L10`.
4. Order them by reader need: problem first, names and implementation later.
5. Draft through the need, objective, and first mechanism.
6. Add only examples and distinctions that change reader capability.
7. Audit every sentence against evidence status and source locators.
8. Audit every low guarantee ID.
9. Remove unearned concepts, catalogues, repetitions, and implementation detail.
10. Return the explanation with bounded deferred concepts and uncertainty.
</process>

<review-mode>
When the user asks to review an existing low-resolution explanation:

1. Bind the explanation, object, consumer, purpose, and evidence boundary.
2. Use a supplied valid `lens_packet`; when absent, read and invoke
   `../lens-router/SKILL.md` to obtain one without choosing lenses locally.
3. Identify the first sentence or passage that exceeds the appropriate
   resolution.
4. Identify the first unearned concept.
5. Identify claims stronger than their evidence and important reserved terms
   used loosely.
6. Identify catalogues where a relation is needed and implementation detail
   introduced before conceptual need.
7. Audit `L01` through `L10` in order and locate the first failed guarantee.
8. Propose the smallest revision that repairs the first structural failure.
9. Do not polish downstream prose before repairing that failure.

Keep this review read-only unless the user separately authorizes revision.
</review-mode>

<quality-bar>
Pass only when every low guarantee ID in
`resolution-guarantees.md` is satisfied and the result:

- begins with the problem or need;
- distinguishes objective from demonstrated outcome;
- explains a central mechanism in ordinary language;
- keeps material claims inside the evidence boundary;
- preserves load-bearing structure and uncertainty;
- introduces implementation only after conceptual need;
- leaves the reader able to state why the object exists and how it approaches
  its problem.
</quality-bar>

<observability>
A meaningful execution is an attempted creation or review that returns a
reader explanation, a review result, a validation failure, or a redirect.

When repository observability is available, record mode, consumer-purpose
binding status, selected lens IDs, included and deferred finding counts, first
failed guarantee if any, redirect count, unearned-concept count, unsupported
claim count, and output status. Do not copy explanation prose or private
evidence into telemetry.

Reflect after 5 meaningful executions, 10 outputs, 3 related explanation gaps,
or 1 severe gap. Severe gaps include an unsupported claim presented as fact, a
material finding silently dropped, a medium/high guarantee emitted as low, or
implementation detail introduced before the reader's conceptual need.
</observability>

<anti-patterns>
Avoid:

- compressing until the reader can no longer explain the need or central relation;
- exposing several unfamiliar concepts or a component catalogue at once;
- defining the object before establishing the pressure that makes it relevant;
- turning intended behavior, a hypothesis, or an interpretation into demonstrated fact;
- linearizing load-bearing branching, recurrence, feedback, or local/global effects;
- introducing implementation names before the underlying relation is understood;
- selecting lenses or resolution locally to repair an invalid handoff;
- omitting a material finding without a bounded deferred disposition;
- claiming success while any `L01` through `L10` guarantee remains failed.
</anti-patterns>

<output-contract>
For creation, always return:

- `explanation`: the reader-facing prose;
- `reserved_concepts_deferred`;
- `uncertainty`;
- `routing_metadata`, kept outside the prose, containing:
  - `resolution: low`;
  - `packet_digest`, copied from both validated handoff artifacts;
  - `consumer` and `purpose`;
  - `evidence_boundary`;
  - `selected_lenses`;
  - `lens_specific_allocation` from the plan;
  - `finding_disposition` with every material individual and composed finding
    ID marked `included` or `deferred`, a bounded reason, and an explanation
    locator when included;
  - `guarantee_audit` with every `L01` through `L10` ID, `pass` or `fail`, and
    an exact explanation locator or short supporting excerpt.

Revise before returning a successful result when any guarantee is `fail`.
Do not treat a free-form assertion of compliance as an audit.

The audit envelope preserves provenance for the router. Do not insert lens
names or lens-by-lens scaffolding into the reader-facing prose unless explicitly
requested.
</output-contract>

<review-output-contract>
For review, return:

- consumer and purpose;
- evidence boundary and selected lenses;
- first excessive-resolution passage;
- first unearned concept;
- claim, terminology, catalogue, or implementation-order findings;
- first failed low guarantee with exact locator and evidence;
- smallest bounded repair;
- remaining uncertainty.
</review-output-contract>
