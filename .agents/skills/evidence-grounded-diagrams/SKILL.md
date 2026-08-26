---
metadata:
  surface_kind: generated-native-runtime-package
  runtime: codex
  canonical_source: transmutations/evidence-grounded-diagrams/SKILL.md
  alias_of: null
  generated_by: tools/bootstrap_arcanum.sh --profile
  mutation_policy: regenerate-from-canonical-source
name: evidence-grounded-diagrams
description: "Use when: creating, reviewing, or revising structural diagrams whose nodes, edges, direction, grouping, loops, containment, sequence, causality, or emphasis must remain traceable to evidence. Covers architecture, process, state, sequence, dependency, hierarchy, timeline, causal, and typed-relation diagrams; can refuse a diagram when prose or a table is more faithful. Excludes primarily quantitative charts and cartographic maps."
argument-hint: "<create|review|revise> <reader-question> [--evidence <paths>] [--output-root <path>]"
tier: transmutations
domain: evidence-governed-visualization
version: 0.4.0
origin: revised from an evidence-grounded diagram prompt through governed Robot Talks and adversarial review
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Sigil: Evidence-Grounded Diagrams

<objective>
Create, review, or revise the smallest structural diagram that answers one
named reader question without asserting more than the permitted evidence, then
persist every emitted diagram as a tagged, versioned, validated artifact bundle.

A diagram is a compressed claim set, not decoration. Return prose, a table, or
an evidence blocker when that is more faithful.
</objective>

<logic-type>
Transmutation: bounded, evidence-constrained representational synthesis.
</logic-type>

<non-negotiable-invariants>
- Require `claim <= evidence` for every load-bearing visual choice.
- Keep evidence, inference, hypothesis, and unknown distinct and visible.
- Keep review read-only. Mutation requires `revise` and explicit authorization.
- Preserve the original artifact; every revision receives a new revision ID.
- Keep caption, rationale, and textual equivalent semantically distinct.
- Never declare official readiness without an inspected render.
- Never treat caller-authored attestation YAML as an authority or trust anchor.
- Persist and tag every emitted diagram before handoff. If persistence fails,
  return `persistence-blocked` and do not emit a final diagram inline.
- Treat persistence, publication, and promotion as separate states.
</non-negotiable-invariants>

<resource-router>
Load only what the selected route requires:

- Run `scripts/preflight_runtime.py` before the first package script in a new
  runtime; if it blocks, install `requirements.txt` before continuing.
- Always read `references/claim-model.md` before judging visual claims.
- Read `references/runbooks.md` for the selected create, review, or revise route
  and when choosing a diagram family.
- Read `references/artifact-lifecycle.md` before writing, rendering, persisting,
  publishing, or promoting an artifact.
- Use `schemas/diagram-request.schema.yml` when serializing an invocation.
- Read `references/schema-guide.md` when interpreting, extending, or debugging
  any request, model, manifest, receipt, attestation, or usage-event field.
- Use `schemas/diagram-semantic-model.schema.yml` while constructing claims and
  visual encodings.
- Use `schemas/diagram-bundle-manifest.schema.yml` and
  `schemas/diagram-validation-receipt.schema.yml` at persistence and handoff.
- Use `schemas/diagram-review-receipt.schema.yml` and
  `templates/review.receipt.yml` for a read-only review; store the receipt
  outside the audited bundle when the user requests persistence, then run
  `scripts/validate_review_receipt.py` on it.
- Use `schemas/diagram-manual-attestation.schema.yml` and an external
  `templates/manual-attestation.yml` only to record an explicit source-aware or
  visual assessment. Pass it with `--manual-attestation`; the package records
  it as advisory and never upgrades it to authoritative overall PASS. Never
  promote PASS values copied from mutable or caller-authored YAML.
- Use `schemas/usage-event.schema.yml`, `templates/usage-event.json`, and
  `scripts/record_usage_event.py` after each meaningful execution when a
  writable observability ledger is available.
- Run `scripts/detect_renderer_capabilities.py` before selecting a local
  renderer; capability detection is evidence, not permission to substitute.
- Start bundle sidecars from `templates/` rather than recreating their shape.
- Run `scripts/validate_diagram_bundle.py` on every persisted bundle.

Do not read machine schemas as cognitive instructions when no structured
artifact is being written or validated.
</resource-router>

<intake>
Resolve:

- mode: `create`, `review`, or `revise`;
- one exact reader question and intended resolution;
- the permitted evidence corpus with stable locators;
- publication intent and whether the destination is official;
- desired source format and target renderer, when specified;
- storage root;
- for review or revise, the exact artifact/revision to inspect;
- for revise, explicit correction authorization.

Classify missing inputs as:

- safely inferable and disclosed;
- useful but non-blocking;
- required before work;
- a blocker that produces `needs-evidence`, `render-blocked`, or
  `persistence-blocked`; use the `INSUFFICIENT_EVIDENCE` verdict for an
  indeterminate review.

For a non-official draft, default storage to
`<workspace>/.artifacts/diagrams/` when no governed artifact root exists. Never
choose an official publication destination silently.
</intake>

<mode-router>
- `create`: decide whether a diagram is warranted and, if so, create revision
  `r0001` or the next unused revision.
- `review`: inspect the exact source/render/revision without modifying it.
- `revise`: require explicit authorization, review first, then create a new
  revision that records `supersedes`.
- A request to review and fix is sequential `review -> revise`, never a mutable
  review pass.
</mode-router>

<process>
1. Normalize intake and establish the evidence boundary.
2. Make the admission decision: `diagram`, `no-diagram`, or `needs-evidence`.
   Return immediately for `no-diagram` or `needs-evidence`; those outcomes do
   not fabricate or persist an empty diagram bundle.
3. In `review`, follow the read-only runbook, bind a review receipt to the exact
   supplied bytes, and return `review-result`. Do not enter diagram persistence.
4. For `create` or authorized `revise`, write the structural claims in prose
   before drawing.
5. Build the semantic model: sources, locators, claims, elements, encodings,
   status, scope, completeness, and residue.
6. Choose the diagram family from the supported relation, not preference.
7. Draft the smallest source that preserves every load-bearing relation.
8. Write separately:
   - caption: short reader-facing summary;
   - rationale: why a diagram and this family were chosen;
   - textual equivalent: the same nodes, typed relations, direction, scope,
     conditions, and epistemic distinctions in text.
9. Validate source syntax when a parser is available.
10. Detect renderer capability and follow the renderer ladder in
   `references/artifact-lifecycle.md`. Do not substitute a renderer silently.
11. Inspect any render for clipping, overlap, legibility, direction,
    containment, status visibility, accessibility, and accidental layout claims.
12. Reconcile request evidence set, model, source, render, and textual
    equivalent. None may assert
    more than the others without an explicit qualification.
13. Stage the complete bundle, including the normalized `diagram.request.yml`
    and a validation receipt.
14. Persist atomically with `scripts/persist_diagram_bundle.py` or an equivalent
    host artifact operation that returns a stable handle.
15. Run `scripts/validate_diagram_bundle.py` against the persisted bytes.
16. Hand off only the persisted path/handle, lifecycle state, verdict,
    validation summary, first blocker, and a concise reader-facing result.
</process>

<emission-boundary>
A diagram is emitted when its source or render is delivered to the user as a
result or inserted into another artifact. Internal scratch that never crosses
that boundary may remain ephemeral.

Do not paste an unpersisted diagram as the final response and then attempt to
save it afterward. Persist first; hand off second. A failed render may still be
saved as a source-only draft with diagnostics. A failed persistence attempt is
not an emitted diagram.
</emission-boundary>

<review-boundary>
Return `PASS`, `FIX`, or `INSUFFICIENT_EVIDENCE`.

- `PASS`: no unsupported or ambiguous load-bearing visual claim survives.
- `FIX`: at least one such claim survives; name the first blocker and smallest
  correction for every material finding.
- `INSUFFICIENT_EVIDENCE`: the permitted corpus cannot support the judgment.

`PASS` is not render approval, publication readiness, or correction authority.
A review receipt must identify the exact revision and member digests inspected.
If the input is an inline source rather than a bundle, identify it as
`target.kind: source`, hash the normalized bytes, disclose the normalization,
and do not invent a diagram ID or revision. Persisting a review report never
authorizes a corrected diagram or mutation of the audited target.

Structured and inline receipts use the schema vocabulary `blocker`, `major`,
and `minor`; an inline summary must remain schema-isomorphic. Validate a saved
receipt against the inspected source or bundle bytes, not only against shape.
For supplied inline source, pipe the exact source to
`scripts/validate_review_receipt.py` with `--target-stdin`; a temporary target
file is not required.
</review-boundary>

<publication-boundary>
- Source-only output may be a saved draft.
- Official publication requires schema, reference integrity, evidence adequacy,
  semantic reconciliation, source validation, render inspection,
  accessibility, and persistence checks to pass for the same revision bytes.
- An externally produced render may satisfy the gate only when its renderer,
  bytes, inspection, and receipt are recorded.
- This package has no built-in attestor trust anchor. A manual attestation can
  preserve assessment evidence but cannot by itself authorize `validated`,
  `published`, or official `ready`; that requires a separately governed trusted
  validation surface.
- Saving does not imply Git tracking. Publishing does not imply promotion.
- Promotion to durable or canonical evidence is a separate governed action.
</publication-boundary>

<quality-bar>
A successful execution must:

- answer one structural reader question or honestly refuse;
- expose auditable claim-to-source locators;
- use a family justified by the represented relation;
- make uncertainty and partiality visible;
- preserve revision lineage;
- distinguish caption, rationale, and textual equivalent;
- persist every emitted diagram with normalized tags and a stable location;
- validate reference closure, aggregate status, textual coverage, member
  digests, and publication gates;
- report renderer and validation limitations truthfully;
- leave no user-visible final diagram outside its bundle.
</quality-bar>

<anti-patterns>
Avoid:

- boxes and arrows without typed relations;
- chronology, causality, ownership, hierarchy, acyclicity, or completeness
  inferred from layout alone;
- unlabeled inference or uncertainty represented only by color;
- an empty or appearance-only textual equivalent;
- `review` that writes or silently corrects its target;
- overwriting a prior revision;
- treating a schema pass as semantic or publication approval;
- saving only a render while losing editable source;
- arbitrary paths, free-form lifecycle tags, or receipts detached from bytes;
- calling source-only output officially published;
- editing `.agents/skills/` or another runtime surface as canonical source.
</anti-patterns>

<observability>
A meaningful execution is a create, review, or revise attempt that produces a
decision, bundle, or blocker. Record mode, outcome, lifecycle status, generated
artifact count, validation verdict, anti-pattern hits, workflow gaps, user
corrections, and reflection trigger state through the repository observability
surface when available. Telemetry failure must not falsify the primary result.
Default a package-local development run to `development/runs/usage-events.jsonl`;
in consuming workspaces, prefer the repository's governed observability ledger.
</observability>

<output-contract>
Return:

```markdown
## Evidence-Grounded Diagram Result

- Mode: create | review | revise
- Outcome: diagram | no-diagram | needs-evidence | review-result | render-blocked | persistence-blocked
- Verdict: PASS | FIX | INSUFFICIENT_EVIDENCE | DRAFT | BLOCKED
- Reader question: <question>
- Diagram ID / revision: <id / revision | not applicable>
- Bundle: <stable path or handle | none>
- Lifecycle: draft | validated | published | superseded | rejected | not applicable
- Aggregate epistemic status: evidence-backed | inferred | hypothesis | mixed | unknown | not applicable
- Renderer: <name and version | unavailable | not applicable>
- Validation: <checks and states>
- Review receipt: <path/handle or inline summary | not applicable>
- First blocker: <blocker | none>
- Evidence boundary: <corpus and material exclusions>
```

Include every field. Use `not applicable` or `none` instead of omitting a field.
</output-contract>
