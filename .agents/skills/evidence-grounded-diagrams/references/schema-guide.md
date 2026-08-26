# Schema Guide

This guide defines the meaning and authority of the package's machine
contracts. The YAML schemas own admissible shape; `SKILL.md` and the routed
references own behavior and judgment. A schema-valid value is not, by itself,
true, evidence-backed, rendered, published, or promoted.

## Contract Map

| Contract | Role | Authority boundary |
| --- | --- | --- |
| `diagram-request.schema.yml` | Immutable normalized invocation and permitted evidence set | Says what was asked and what evidence was allowed; does not prove the evidence or authorize publication |
| `diagram-semantic-model.schema.yml` | Auditable claim and visual-encoding model | Says what each visual element means and cites support; shape validation does not establish semantic truth |
| `diagram-bundle-manifest.schema.yml` | Bundle identity, members, tags, lineage, persistence, and declared lifecycle | Declares the bundle inventory; member hashes and the current validation receipt must confirm it |
| `diagram-commit-marker.schema.yml` | External persistence transaction record | Permanently reserves a revision identity after successful commit; later tampering never makes that identity reusable |
| `diagram-validation-receipt.schema.yml` | Validation results bound to exact manifest and member bytes | Reports named checks only; package-local manual assessments remain advisory |
| `diagram-review-receipt.schema.yml` | Read-only judgment on an exact bundle or normalized source | Authorizes neither mutation, publication, nor correction |
| `diagram-manual-attestation.schema.yml` | External source-aware or visual assessment | Supplies claimed assessor identity, provenance, exact bytes, and manual check results; package-local processing cannot establish authority |
| `usage-event.schema.yml` | Operational observability event | Records execution signals; it is not artifact evidence or a validation result |

## Shared Vocabulary

- `contract_version`: version of that machine contract, independent of the
  skill release version.
- `diagram_id`: stable lowercase identity across revisions.
- `revision`: immutable `rNNNN` version. A revise operation allocates a new
  value and never rewrites an earlier revision.
- `request_id`: identity of the normalized invocation.
- `evidence_set_id`: identity of the exact permitted evidence collection.
- `request_sha256`: SHA-256 of persisted `diagram.request.yml` bytes.
- `evidence_snapshot_digest`: optional digest of one disclosed, normalized
  evidence snapshot, including a snapshot embedded in the normalized request.
  `null` means the corpus identity is declared but no one snapshot digest was
  available; a digest proves byte identity, not the evidence's authority.
- `reader_question`: the one structural question the artifact must answer.
- `aggregate_status`: least-safe summary of included claim statuses. It cannot
  be stronger than the claims it summarizes.
- `content_digest`, `sha256`, `manifest_digest`: lowercase SHA-256 bindings to
  exact bytes; they are integrity claims, not truth claims.
- `normalization`: the disclosed byte-normalization rule used before hashing an
  inline source. The supported rule is UTF-8, LF line endings, no trailing
  newline.

## Request

- `mode`: `create`, read-only `review`, or authorized immutable `revise`.
- `resolution`: intended level of detail, not display resolution.
- `evidence_set.sources`: complete permitted corpus. Each source records its
  type, location, authority role, optional digest, and stable locators.
- `locator_id`: local reference identity; `selector` locates the supporting
  passage or region; `excerpt` is optional convenience, not a substitute for
  source identity.
- `publication.destination`: intended delivery location, if any.
- `publication.official`: whether the destination carries official authority.
- `publication.requested_readiness`: requested `draft` or `ready` gate. A
  request for `ready` does not make the result ready.
- `output.representation_format`: desired editable source form.
- `output.target_renderer`: requested renderer, or `null` when unspecified.
- `output.result_encoding`: user-facing result envelope.
- `storage.output_root`: governed bundle root; the persister writes below it.
- `storage.allow_draft_fallback`: permits an honest source-only draft when the
  publication gate cannot be completed.
- `target`: for review/revise, either an exact bundle identity plus manifest
  digest, or exact source bytes/path plus normalization and digest.
- `mutation_authorized`: must be true for revise and false for review.

## Semantic Model

- `caption`: short reader-facing summary of what the diagram says.
- `rationale`: why a diagram and this family were selected.
- `scope.coverage`: represented boundary; `completeness` says whether it is
  complete or partial; `exclusions` names material omissions.
- `claims`: explicit propositions carried by the visual. `relation_kind`
  defines the relation, `status` its epistemic class, `support` its source and
  locator links, `qualification` its limits, `load_bearing` its importance, and
  `included` whether it appears in the delivered artifact.
- `support_kind`: direct support, corroboration, conflict, or motivation. Only
  direct/corroborating evidence can strengthen a claim; motivating evidence
  merely explains why it was considered.
- `elements`: visible or layout-bearing units. `claim_ids` prevents a node,
  edge, direction, loop, enclosure, emphasis, or omission from being
  semantically anonymous.
- `encodings`: mapping from visual mark to exact meaning, affected elements and
  claims, plus a redundant text channel so meaning is not color-only.
- `textual_equivalent_coverage`: claim IDs represented in the textual
  equivalent. The textual equivalent is a non-visual expression of the same
  structure, not a general explanation or caption.
- `residue`: evidence or candidate content deliberately excluded, with reason
  and disposition.

## Manifest and Lifecycle

- `owner`: accountable artifact owner, not necessarily the runtime process.
- `created_at`: timestamp of this immutable revision.
- `lifecycle_status`: declared artifact state. `superseded` is normally derived
  by the resolver rather than written back into an older manifest.
- `retention_class`: why the bundle is retained: generated, durable evidence,
  source, or local runtime.
- `promotion_status`: separate governance decision; saving or publishing does
  not imply promotion.
- `promotion_evidence`: null before promotion. A promoted artifact must bind a
  decision identity/time, accountable authority and authority basis, plus the
  path, media type and SHA-256 of its external promotion attestation. Shape
  alone does not authenticate that authority.
- `supersedes`: immediate prior revision and its manifest digest.
- `tags.diagram_kind`: controlled diagram family.
- `tags.lifecycle`, `tags.epistemic`, `tags.scope`: searchable controlled
  summaries that must agree with manifest/model state.
- `tags.topics`: normalized topic terms; `extensions` are namespaced
  `namespace:value` tags.
- `members`: canonical bundle inventory. Request, source, semantic model,
  textual equivalent, and validation receipt are required; render is optional
  for drafts. Paths are bundle-relative and hashes bind exact bytes.
- `renderer`: renderer identity/version/adapter for a recorded render.
- `persistence`: stable output root, bundle path, index path, and saved state.
- `publication`: destination, official flag, and actual readiness. `published`
  or official `ready` requires a recorded render and all applicable checks.

The commit marker is stored outside the bundle because bundle bytes are the
object it protects. `manifest_sha256` captures the immutable inventory and
identity at commit time; `committed_at` records the completed transaction. The
refreshable validation receipt is deliberately not marker-bound and remains
governed by its own exact observed-byte contract. The marker is a no-reuse
tombstone even if bundle bytes are later damaged.

## Validation and Attestation

- `observed_manifest_sha256` and `observed_members`: exact byte set assessed.
  Validation and manual attestation require complete, unique coverage; a
  caller-selected subset cannot establish readiness.
- `checks`: `schema_shape`, `referential_integrity`, `evidence_adequacy`,
  `source_validation`, `render_inspection`, `semantic_reconciliation`,
  `accessibility`, and `persistence`.
- Check `status`: `PASS`, `FAIL`, `NOT_RUN`, or `N/A`. PASS/FAIL requires
  evidence; NOT_RUN requires a limitation. N/A means the check genuinely does
  not apply, not merely that it was inconvenient.
- `assessor`: actor or mechanism producing a check result.
- `overall`: PASS only when every required publication check passes on the same
  bytes; DRAFT preserves honest incomplete work; FAIL reports failed checks;
  BLOCKED reports an unmet prerequisite.
- `blockers`: concrete reasons the requested gate was not met.
- `manual_attestation`: provenance pointer copied into the computed receipt
  only after the validator verifies an external assessment's bytes and digest.
  It remains advisory because this package has no configured attestor trust
  anchor and therefore cannot upgrade overall validation to PASS.
- Attestation `assessor.kind`: claimed human, tool, or governed review identity.
  `provenance` should identify a stable review record or tool run, but these
  strings are not authenticated here; a separate governed trust surface is
  required before they can carry authority.

## Review Receipt

- `review_id`, `reviewed_at`, `reviewer`: review identity and actor.
- `target.kind`: `bundle` for a complete canonical revision or `source` for
  normalized standalone source.
- `observed_members`: exact inspected bytes. Bundle review requires the full
  canonical member set; source review requires exactly one source digest.
- `render_inspected`: true only when the exact render member was inspected.
- `evidence_boundary`: complete permitted source/locator set for the judgment.
- `verdict`: PASS, FIX, or INSUFFICIENT_EVIDENCE. PASS is not publication or
  mutation authority.
- `findings`: stable ID, consequence severity, visual claim, evidence status,
  evidence rationale, and smallest correction.
- `first_blocker`: optional first blocker-severity finding for FIX; omit it when
  a valid FIX has only major findings, and use null for non-FIX verdicts.

## Usage Event

- `meaningful_execution`: whether the attempt reached a decision, blocker,
  review, or bundle result.
- `outcome`: route result from the skill output contract.
- `generated_output_count`: emitted diagram count, not sidecar-file count.
- `quality_bar_status`, `anti_pattern_hits`, `workflow_gaps`, and
  `output_contract_drift`: operational quality signals.
- `user_correction`: whether user feedback changed the behavioral contract.
- `observer_recommendation` and `reflection_trigger`: lifecycle feedback; they
  do not change artifact state automatically.

## Versioning and Extension

Contract versions change when required fields, meanings, invariants, or
compatibility change. Additive optional fields may remain within a compatible
version only when old consumers can safely ignore them. Custom relation kinds
use `custom:<term>`; custom tags use `namespace:value`. Do not add undeclared
fields to strict schemas or use extension strings to bypass governed core
vocabulary.
