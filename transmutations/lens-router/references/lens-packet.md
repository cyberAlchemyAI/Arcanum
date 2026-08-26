# Lens Packet Contract

`lens_packet` is the sole handoff owned by `lens-router`. It preserves analytic
material for later resolution selection without pre-compressing it for the
reader.

## Required fields

- `packet_version`: `2.0`.
- `packet_digest`: deterministic identity of the complete packet, encoded as
  `sha256:<lowercase hex>`. Compute it over UTF-8 canonical JSON after removing
  `packet_digest`, with keys sorted, no insignificant whitespace, exact array
  order, and non-ASCII characters preserved.
- `object`: bounded description of what was inspected.
- `consumer`: intended downstream consumer.
- `purpose`: what the consumer must understand or do.
- `evidence_boundary`: non-empty source records with stable `locator` and the
  structured, machine-checkable `scope` defined below.
- `known_terms`: terms the consumer already understands.
- `reserved_terms`: terms whose precise meaning must be preserved.
- `selected_lenses`: unique lens IDs from `epistemic`, `systemic`, and
  `categorical`.
- `selection_rationale`: one record per selected lens containing `lens`,
  observable `trigger`, and bounded `reason`.
- `per_lens_findings`: evidence-bounded findings produced independently.
- `composed_findings`: cross-lens relations; use an empty list for one lens.
- `qualitative_audit`: the required human/agent judgment checks described below.
- `open_questions`: material unanswered questions.

## Finding records

Every `per_lens_findings` record contains:

- `id`: unique stable ID within the packet;
- `lens`: one selected lens;
- `statement`: the bounded finding;
- `status`: one of `observed-implemented`, `supported-interpretation`,
  `product-direction`, `hypothesis`, or `open-question`;
- `evidence_refs`: stable locators directly supporting the statement;
- `materiality`: why the finding can change understanding, verification,
  decision, implementation, or the next question;
- `uncertainty`: remaining uncertainty or `null`.

Require at least one evidence locator for `observed-implemented` and
`supported-interpretation`. Other statuses may have no supporting locator only
when the record explicitly preserves that limitation.

## Evidence boundary and locator forms

Each boundary record uses exactly one structured scope:

- `{ "kind": "whole-resource" }`: the base locator, a single positive line
  locator `<locator>:N`, or a valid JSON Pointer `<locator>#/path`;
- `{ "kind": "line-range", "start_line": N, "end_line": M }`: only a
  single-line locator `<locator>:K` where `N <= K <= M`;
- `{ "kind": "exact-locator" }`: only the exact base locator;
- `{ "kind": "json-pointer-prefix", "pointer": "/path" }`: the exact
  JSON Pointer or one of its descendant pointer paths.

Line ranges are inclusive and use positive decimal integers without leading
zeroes. JSON Pointers follow RFC 6901 escaping. Free-form scope descriptions,
line ranges embedded in evidence references, fragments that are not JSON
Pointers, and locators that merely share a textual prefix are invalid. When a
reference does not match one of these forms exactly, validation fails closed.

## Composition records

Every `composed_findings` record contains:

- `id`;
- `kind`: `agreement`, `tension`, `dependency`, `joint-distinction`, or
  `new-question`;
- `finding_ids`: at least two contributing finding IDs from different lenses;
- `statement`;
- `evidence_refs`: any additional locators used during composition;
- `uncertainty`.

Composition augments and never replaces individual findings. Downstream routing
and writing must evaluate both collections. A material finding remains eligible
when no cross-lens relation references it.

## Qualitative audit

Some validity rules require language judgment and cannot be established by JSON
Schema or cross-field checks. Include exactly these audit records:

- `claim-status-language`: verify every claim's wording matches its status;
- `evidence-authority-permission`: verify evidence was not converted into
  authority, approval, or permission;
- `lens-forbidden-jumps`: reapply every selected lens's forbidden jumps.

Each record contains `check`, `status` (`pass` or `fail`), `reviewed_ids` covering
every individual and composed finding ID, and a bounded `note`. Do not return a
packet while any qualitative check is `fail`.

## Validity rules

A packet is valid only when:

- `packet_digest` matches the canonical packet content;
- every selected lens has a rationale and at least one finding;
- no unselected lens appears in a finding;
- all IDs are unique and every composition reference resolves;
- every evidence locator equals or is a child locator of a source in
  `evidence_boundary`;
- claim language matches finding status;
- compactness reflects relevance filtering rather than reader-facing
  resolution;
- no field silently converts evidence into authority or permission.

`lens-packet.schema.json` validates structure only. It cannot enforce digest
correctness, line-range ordering, coverage, ID resolution, cross-lens
composition, evidence-boundary membership, or the truth of qualitative
language judgments by itself.

Use `../scripts/validate_lens_packet.py <packet.json> --compute-digest` (or `-`
for stdin) to compute the canonical digest while constructing a packet. Insert
that exact value as `packet_digest`, then run normal validation.

Run `../scripts/validate_lens_packet.py` for every packet exchanged between
skills. The script validates structure, cross-field semantics, and audit
coverage, but not the truth of the audit judgments. A packet is valid only when
structural validation, cross-field validation, and the qualitative audit pass.
Human-readable Markdown may mirror the fields but does not replace the validated
JSON-compatible object.
