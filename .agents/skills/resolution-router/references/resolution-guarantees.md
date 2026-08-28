# Cumulative Resolution Guarantees

Resolution tiers are sets of reader-facing guarantees. They are not word-count
targets and do not execute lower-tier writers recursively.

## Low: `G_low`

- `L01-problem-first`: begin with the need or condition that makes the object
  relevant rather than an object definition or component list.
- `L02-consumer-relevance`: establish why that need matters to this consumer.
- `L03-objective-status`: distinguish the object's objective from demonstrated
  outcomes.
- `L04-central-mechanism`: explain at least one central mechanism in ordinary
  language and connect it to the need.
- `L05-earned-concepts`: introduce specialized terms only after the reader has
  a need for the distinction.
- `L06-evidence-ceiling`: keep every claim at or below its evidence and preserve
  material uncertainty.
- `L07-relations-over-catalogue`: explain load-bearing relations rather than
  merely listing components.
- `L08-implementation-last`: introduce implementation only as a concretization
  of an understood relation.
- `L09-structure-fidelity`: preserve load-bearing loops, local/global effects,
  boundaries, and uncertainty.
- `L10-minimum-sufficiency`: leave the reader able to say why the object exists
  and how it approaches its problem without carrying unnecessary distinctions.

## Medium additions: `G_medium - G_low`

- `M01-operational-model`: expose the central parts, states, relations, and
  interactions needed for operational reasoning.
- `M02-boundaries-assumptions`: make relevant boundaries, assumptions,
  dependencies, and authority limits explicit.
- `M03-alternatives-consequences`: show material alternatives, trade-offs, or
  downstream consequences needed for comparison or decision.
- `M04-evidence-mapping`: connect important operational claims to their evidence
  status and unresolved questions.
- `M05-selective-concretization`: include examples and implementation detail
  sufficient to connect the model to the real system without exhaustive audit.

`G_medium = G_low + M01..M05`.

## High additions: `G_high - G_medium`

- `H01-mechanisms-interfaces`: expose mechanisms, interfaces, schemas, and
  transformations required for inspection or implementation.
- `H02-failure-edge-cases`: cover material edge cases, failure modes,
  degradation, and exception behavior.
- `H03-verification`: expose tests, validation evidence, falsifiers, and claim
  support needed to challenge correctness.
- `H04-unresolved-structure`: preserve hypotheses, open questions, conflicting
  evidence, and decisions that remain unclosed.
- `H05-implementation-sufficiency`: provide the implementation-level detail
  needed for the stated design, validation, challenge, or build task.

`G_high = G_medium + H01..H05`.

## Calibration boundary

Tier selection follows the reader's required action, not the complexity or
vocabulary of the source object.

- Low may identify central roles, one essential handoff, and a load-bearing
  branch or stop condition when they are required for minimum orientation.
- `M01` activates only when the reader must use the model to predict, operate,
  troubleshoot, compare, or decide; merely understanding that parts and
  handoffs exist remains low.
- `M02` activates when the reader must enumerate or apply multiple boundaries,
  assumptions, dependencies, or authority limits. Stating one essential
  ownership boundary does not force promotion.
- High-tier nouns such as interface, schema, failure mode, or edge case do not
  activate high by themselves. The consumer must need to inspect, validate,
  challenge, design, or implement them.

## Promotion

Select the lowest tier containing every guarantee required for the consumer's
purpose. Record the first higher-tier guarantee that forces promotion.

Lens use is cumulative with resolution: low requires epistemic and systemic;
medium and high require epistemic, systemic, and categorical. If the reader's
purpose requires categorical distinctions for operational reasoning, select at
least medium. Do not hide a higher-tier need by calling it mere emphasis.

## Validation

A writer satisfies a tier only when the human explanation fulfills its
cumulative guarantees and reflects all required perspectives. Guarantee IDs are
internal maintenance labels, not required output fields.
