---
name: resolution-router
description: Coordinate evidence-bounded explanations by obtaining a lens packet, choosing low, medium, or high resolution for a specific reader and purpose, and executing the installed writer at the lowest sufficient cumulative tier. Use for explanation requests that require resolution selection, for explicit low/medium/high requests, or when a resolution writer redirects a direct invocation with missing routing inputs.
---

# Resolution Router

<objective>
Produce an explanation at the lowest resolution that lets the intended consumer
correctly complete the intended task.

Resolution controls how many distinctions the reader must carry. It is not a
word-count target. Low, medium, and high form cumulative guarantee tiers:
`G_low` is contained by `G_medium`, and `G_medium` by `G_high`.
</objective>

<logic-type>
Transmutation: bounded reader-purpose interpretation, cumulative guarantee
selection, and deterministic routing to an installed writer.
</logic-type>

<ownership>
Act as the operational entrypoint for reader-facing explanations.

Own consumer-purpose binding, resolution selection, target resolution, writer
loading, and same-turn writer execution. Do not select, apply, or compose
lenses; invoke `lens-router` when a valid packet is absent. Writers own
representation at their selected tier.
</ownership>

<authority>
Read these references completely on every invocation:

- `references/routes.md` for target IDs, paths, and availability rules;
- `references/resolution-guarantees.md` for cumulative tier semantics and
  promotion;
- `references/resolution-plan.md` for the handoff contract.

The plan exchanged with a writer is a JSON-compatible object. Validate it
structurally against `references/resolution-plan.schema.json` and semantically
with `scripts/validate_resolution_plan.py`. A schema pass alone is not a valid
plan. Before writer execution, validate the supplied packet and plan together
with `scripts/validate_routing_handoff.py`; separate passes do not establish
that the pair belongs together.
The validator dependency is declared in `requirements.txt`. If `jsonschema` is
missing, return the script's actionable dependency error and do not claim a
validated plan or install packages without user authority.

When changing routes, availability, schemas, guarantee definitions, or writers,
read `references/validation.md` completely and run its checks before enabling a
route.
</authority>

<inputs>
Bind:

- `object`;
- `consumer`;
- `purpose`;
- `evidence_boundary`;
- `known_terms` and `reserved_terms`;
- optional `requested_resolution`;
- optional `lens_packet`.

Treat an explicit requested resolution as a minimum. Do not silently downgrade
it. Promote it only when a higher tier is required for the consumer to complete
the purpose correctly, and state the reason.
</inputs>

<lens-packet-gate>
If no `lens_packet` is supplied:

1. resolve `lens-router` using `references/routes.md`;
2. read its `SKILL.md` completely;
3. invoke it with the bound inputs;
4. require one valid packet before choosing final resolution.

If a packet is supplied, read the lens packet contract named in the route
manifest and validate its required fields and invariants. Reject a malformed
packet with the first failing rule. Do not reconstruct, select, or apply lenses
inside this router.

Preserve the packet unchanged after validation. Its canonical `packet_digest`
is the binding identity copied into the resolution plan.
</lens-packet-gate>

<routing-rule>
Choose the lowest tier whose guarantee IDs let the consumer complete the
purpose correctly using both `per_lens_findings` and `composed_findings`.

Classify the task the consumer must perform, not the apparent complexity of the
object or the presence of words such as architecture, interface, handoff, or
maintainer. A low explanation may name the central roles, one essential
handoff, and a load-bearing stop or branch when those distinctions are needed
to explain why the object exists and how it approaches the problem.

- choose `low` when the consumer only needs rationale, the central flow, role
  separation, or the minimum distinctions needed to orient and ask the next
  question;
- choose `medium` when the consumer must use the model to predict states,
  operate, troubleshoot, compare alternatives, decide, or apply several
  interactions, dependencies, assumptions, or authority boundaries;
- choose `high` when the consumer must inspect, validate, challenge, design, or
  implement mechanisms, interfaces, failure modes, or edge cases.

Never discard a material single-lens finding merely because it lacks a
cross-lens relation.

Lens-specific allocation may change emphasis inside one tier. It may not bypass
that tier's concept budget or activate a guarantee owned only by a higher tier.
When a lens requires a higher-tier guarantee, promote the whole route and record
the activating guarantee ID.
</routing-rule>

<cumulative-rule>
Treat inclusion as semantic guarantees, not textual reuse or runtime chaining.

Every writer remains self-contained at execution time. Medium must satisfy all
low guarantee IDs plus its additions. High must satisfy all low and medium IDs
plus its additions. Do not execute a lower writer as a subroutine of a higher
writer.
</cumulative-rule>

<plan-and-execution>
1. Build a valid `resolution_plan` using the selected tier, inherited guarantee
   IDs, promotion evidence, exact packet digest, one allocation for every
   selected lens and its findings, complete composition IDs, and manifest target.
2. Run `scripts/validate_resolution_plan.py` over the plan and resolve the exact
   target in `references/routes.md`.
3. Run `scripts/validate_routing_handoff.py` over the unchanged packet and
   plan. A failed joint binding forbids both writer execution and an assertion
   that the handoff is valid.
4. If the target is `unavailable`, return the selected route and missing target
   explicitly. Do not downgrade, improvise a writer, or claim execution.
5. If the target is `available`, read its `SKILL.md` completely.
6. Execute it in the same turn with the pair:
   `{ lens_packet, resolution_plan }`.
7. Do not rely on incidental simultaneous skill triggering.
</plan-and-execution>

<direct-entry-rule>
A resolution writer invoked without both a valid `lens_packet` and a valid
`resolution_plan` must redirect here with its own tier pinned as
`requested_resolution`. Complete the normal packet, routing, and execution
sequence. This router must not redirect a complete writer input back to itself.
</direct-entry-rule>

<claim-rule>
Preserve `claim <= evidence` at every tier. Higher resolution permits more
distinctions; it never permits stronger unsupported claims.
</claim-rule>

<output-contract>
For an available route, return the selected writer's result together with its
mandatory compact audit envelope: selected resolution, selected lenses,
evidence boundary, packet digest, route reason, promotion reason if any, lens-specific
allocation, target writer, finding disposition, and evidence-linked guarantee
audit.

For an unavailable route, return:

- selected resolution;
- packet digest;
- route reason;
- target writer ID and expected path;
- `status: unavailable`;
- the missing implementation;
- no fabricated explanation at another tier.
</output-contract>

<observability>
A meaningful execution is an attempted explanation route that returns a writer
result, an unavailable-route result, or a validation failure.

When repository observability is available, record requested and selected
resolution, promotion state and activating guarantee ID, selected lens IDs,
target writer, target availability, packet and plan validation status, redirect
count, guarantee-audit result, and caller. Do not copy explanation prose or
private evidence into telemetry.

Reflect after 5 meaningful executions, 10 routed outputs, 3 related routing
gaps, or 1 severe gap. Severe gaps include silent downgrade, fallback from an
unavailable writer, routing without a valid packet, redirect cycling, or a
higher-tier guarantee hidden inside a lower-tier route.
</observability>

<quality-bar>
A successful execution must:

- bind consumer, purpose, evidence boundary, and vocabulary constraints;
- require one valid lens packet before final resolution selection;
- select the lowest sufficient tier without downgrading an explicit request;
- use exactly the cumulative guarantee IDs owned by the selected tier;
- record valid promotion evidence whenever the selected tier exceeds a request;
- preserve material individual and composed findings during allocation;
- bind the plan to the exact packet and pass mandatory joint handoff validation;
- resolve the exact manifest target and respect its availability state;
- execute exactly one available writer with a valid packet-plan pair or return
  one explicit unavailable-route result;
- return an evidence-linked audit envelope without exceeding caller authority.
</quality-bar>

<anti-patterns>
Avoid:

- selecting or applying lenses inside the resolution router;
- treating resolution as word count, tone, or runtime chaining;
- downgrading an explicit resolution request;
- using lens-specific emphasis to smuggle higher-tier guarantees into a lower tier;
- inventing a writer, substitute path, or fallback explanation for an unavailable route;
- trusting schema validation without semantic validation;
- redirecting a complete writer input or relying on incidental co-triggering;
- treating higher resolution as permission for stronger unsupported claims.
</anti-patterns>
