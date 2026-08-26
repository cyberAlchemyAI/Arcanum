---
name: lens-router
description: Select, load, apply, and compose epistemic, systemic, and categorical investigative lenses over complex work. Use when the user explicitly requests one or more lenses, when research, review, or design requires a validated lens packet, or when another skill invokes this router for evidence-bounded analysis. Do not use as the natural-language entrypoint for a reader-facing explanation; resolution-router owns that entry.
---

# Lens Router

<objective>
Inspect one object through the smallest useful set of investigative lenses and
return an evidence-bounded `lens_packet` for downstream work.

A lens determines what to make salient, which questions to ask, and which
inferential jumps to avoid. It does not assert that the inspected object
contains the structure the lens seeks.
</objective>

<logic-type>
Transmutation: bounded evidence-grounded selection and relational synthesis
across independent investigative views.
</logic-type>

<ownership>
Own lens selection, reference loading, independent lens application, and
multi-lens composition.

Do not choose explanation resolution or write the final reader-facing
explanation. Do not replace governed research or review verdicts; provide an
investigative packet those capabilities may consume.
</ownership>

<lens-map>
- `epistemic`: inspect claims, evidence, uncertainty, justification, authority,
  permission, and what may responsibly be believed or done.
- `systemic`: inspect state, change, constraints, feedback, recurrence,
  downstream effects, and local-to-global consequences.
- `categorical`: inspect relevant things, relations, transformations,
  composition, interfaces, transport, preservation, and loss.
</lens-map>

<inputs>
Bind:

- `object`;
- `consumer` and `purpose`;
- `evidence_boundary` with stable source locators;
- `known_terms`;
- `reserved_terms` whose precise meaning must be preserved;
- any explicitly requested lenses;
- required confidence or consequence level.

Do not ask again for values that are clear from context.
Represent every evidence scope using the structured forms in
`references/lens-packet.md`; never translate a free-form phrase such as
"relevant lines" into an unbounded locator.
</inputs>

<selection-policy>
Select a lens only when its core question could materially change what the
consumer can understand, verify, decide, implement, or ask next.

Use one lens when the material question remains within one regime:

- select `epistemic` for claim support, uncertainty, falsification, authority,
  approval, or permission boundaries;
- select `systemic` for state transitions, constraints, feedback, recurrence,
  closure, or local-to-global effects;
- select `categorical` for type boundaries, relations, transformations,
  interfaces, composition, equivalence, preservation, or loss.

Select multiple lenses when:

- a conclusion under one lens depends on a distinction owned by another;
- evidence or authority constrains a system transition;
- a transformation must preserve meaning, evidence, or state downstream;
- local effects must compose into a larger structure;
- the task requests a cross-regime explanation, design, audit, or
  high-confidence assessment.

Select all three only when each core question is material or when the user asks
for the full set. Do not add lenses merely because they are available.

Record one concrete trigger and rationale for every selected lens in the packet.
For higher-confidence work, prefer independent runs when independent agents are
available and authorized. Otherwise run the lenses sequentially while keeping
their findings separate until composition.
</selection-policy>

<reference-loading>
Read `references/lens-packet.md` completely on every invocation.

After selection and before inspecting the object, read each selected reference
completely:

- `epistemic` -> `references/epistemic.md`;
- `systemic` -> `references/systemic.md`;
- `categorical` -> `references/categorical.md`.

When two or more lenses are selected, first finish their independent views,
then read `references/composition.md` completely and apply it.

The packet exchanged between skills is a JSON-compatible object. Validate it
structurally against `references/lens-packet.schema.json` and semantically with
`scripts/validate_lens_packet.py`. A schema pass alone is not a valid packet.
The validator dependency is declared in `requirements.txt`. If `jsonschema` is
missing, return the script's actionable dependency error and do not claim a
validated packet or install packages without user authority.
</reference-loading>

<process>
1. Bind the inputs and evidence boundary.
2. Select the smallest useful lens set using the observable triggers above.
3. Record the selection rationale before reading substantive lens prompts.
4. Load every selected lens reference completely.
5. Apply each lens independently to the same task and evidence boundary.
6. Represent every material finding using the status and evidence fields owned
   by `references/lens-packet.md`.
7. When multiple lenses are selected, compose their relations only after the
   individual views are complete.
8. Preserve all material single-lens findings. Composition augments and never
   replaces `per_lens_findings`.
9. Compute `packet_digest` exactly as defined by the packet contract, using
   `scripts/validate_lens_packet.py <packet> --compute-digest` when the packet
   is file- or stdin-backed. Insert the returned value, then run normal packet
   validation. Fix every structural and cross-field semantic failure.
10. Complete the qualitative audit required by `references/lens-packet.md`.
    Check claim language against status and reapply each selected lens's
    forbidden jumps. A deterministic validator cannot decide these language
    judgments.
11. Return the packet without silently performing resolution routing.
</process>

<invariants>
- Keep `claim <= evidence` for every finding.
- Do not infer truth or authority from evidence alone.
- Do not infer feedback or causality from sequence alone.
- Do not infer composability, equivalence, or preservation from adjacency or
  successful forward movement alone.
- Preserve uncertainty and unsupported hypotheses explicitly.
- Keep lens names and vocabulary internal to authoring unless the consumer's
  purpose requires them.
</invariants>

<output-contract>
Return one valid `lens_packet` as defined by `references/lens-packet.md`.

The packet must preserve:

- selection rationale;
- evidence-linked individual findings;
- a canonical digest binding consumer, purpose, selected lenses, evidence
  boundary, vocabulary, findings, composition, audit, and open questions;
- cross-lens relations when composition ran;
- material single-lens findings without cross-lens matches;
- open questions and uncertainty;
- reader vocabulary constraints required downstream.
</output-contract>

<observability>
A meaningful execution is an attempted or completed lens selection that
returns a packet, a validation failure, or a bounded missing-input result.

When repository observability is available, record the selected lens IDs,
rationale count, individual and composed finding counts, open-question count,
validation status, qualitative-audit status, forbidden-jump hits, and caller.
Do not copy finding statements or private evidence into telemetry.

Reflect after 5 meaningful executions, 10 packets, 3 related routing or packet
gaps, or 1 severe gap. Severe gaps include unsupported claims passing as facts,
composition erasing a material finding, or a lens result exceeding its evidence
or authority boundary.
</observability>

<quality-bar>
A successful execution must:

- select the smallest lens set that covers every material core question;
- record one observable trigger and rationale for every selected lens;
- apply selected lenses independently before composition;
- preserve every material individual finding and its evidence status;
- make every composed relation resolve to findings from different lenses;
- keep every evidence reference within the declared boundary;
- pass structural, semantic, and qualitative packet validation;
- preserve uncertainty, vocabulary constraints, and caller ownership.
</quality-bar>

<anti-patterns>
Avoid:

- selecting all lenses by default instead of proving materiality;
- using lens vocabulary as proof that the inspected structure exists;
- letting one lens see or revise another lens's findings before its independent pass;
- replacing individual findings with a composed summary;
- inferring authority, causality, correctness, equivalence, or preservation from
  evidence, sequence, successful execution, adjacency, or forward movement alone;
- reconstructing missing evidence or silently extending the evidence boundary;
- choosing explanation resolution or writing the final explanation inside this router.
</anti-patterns>
