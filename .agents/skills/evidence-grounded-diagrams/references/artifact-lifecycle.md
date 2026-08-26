# Artifact Lifecycle

Schema Artifact Role: non-canonical operational companion. Bundle and receipt
shape is owned by `../schemas/`.

## Contents

- [Emission and storage](#emission-and-storage)
- [Bundle](#bundle)
- [States](#states)
- [Renderer ladder](#renderer-ladder)
- [Tags and discovery](#tags-and-discovery)
- [Validation and publication](#validation-and-publication)
- [Runtime installation](#runtime-installation)

## Emission and Storage

A source or render is emitted when delivered to a user as a result or inserted
into another artifact. Persist before handoff. Internal scratch may be deleted
or left ephemeral.

Storage resolution order:

1. explicit governed `output_root`;
2. an existing repository artifact root owned by the consuming workflow;
3. `<workspace>/.artifacts/diagrams/` for non-official drafts.

Official publication blocks when no destination is explicit or governed.
Platform artifact storage is acceptable when it returns a stable handle and the
same manifest, member, digest, and receipt semantics can be preserved.

## Bundle

```text
<output-root>/<diagram-id>/<revision>/
  diagram.request.yml
  diagram.<source>
  diagram.<render>              # optional for drafts
  diagram.model.yml
  diagram.meta.yml
  textual-equivalent.md
  validation.receipt.yml
```

Persist the directory atomically. Never overwrite a revision. Preserve source
and diagnostics when rendering fails.

The canonical persister writes an external commit marker under
`<output-root>/.evidence-grounded-diagrams/commits/<diagram-id>/<revision>.yml`
only after bundle verification and index finalization succeed. Once that marker
exists, the revision identity is permanently reserved: later corruption is
quarantinable evidence, never permission to recreate or reuse the revision.
An invalid final directory without a marker is recoverable incomplete-transaction
residue and may be quarantined before the same reservation is retried.
The resolver excludes every unmarked revision. If a crash leaves a fully valid
final bundle and index entry immediately before marker creation, retry finalizes
that exact transaction idempotently; it does not copy staging bytes again.

## States

- `working`: internal and possibly ephemeral; never handed off.
- `draft`: persisted, inspectable, but one or more publication checks may be
  `NOT_RUN` or failed.
- `validated`: persisted bytes pass all checks required by the declared profile.
- `published`: delivered into its declared destination; official publication
  requires inspected render.
- `rejected`: retained for provenance but not eligible for publication.
- `superseded`: effective resolver state for a preserved prior revision with a
  newer validated current revision; do not rewrite its immutable manifest.

`promotion_status` is independent: `not-promoted` or `promoted`. Promotion to
durable or canonical evidence requires the repository's separate governance.
`promotion_evidence` is null until that decision; a promoted manifest must bind
the external decision, authority basis, and attestation digest rather than
assert promotion with an ungrounded flag. A relative attestation path resolves
from the bundle directory. Validation requires that the declared regular file
exists, matches its digest, and names this diagram ID and revision as subject.
Those checks establish provenance closure only; they do not authenticate the
declared authority or convert the package into a promotion authority.

## Renderer Ladder

1. Use the requested renderer when available and record name/version.
2. Use a declared compatible local or browser renderer only with disclosed
   substitution and a new receipt.
3. Save source-only with syntax validation and `render_inspection: NOT_RUN` when
   no renderer exists.

Source-only may be draft or source-validated. It cannot be officially
published. An external render is acceptable only when its exact bytes and
inspection are recorded.

## Tags and Discovery

Every manifest carries controlled core tags:

- `diagram_kind`: one supported family;
- `lifecycle`: the manifest lifecycle state;
- `epistemic`: aggregate status;
- `topics`: normalized lowercase topic terms;
- `extensions`: optional `namespace:value` terms.

Use `scripts/list_diagram_bundles.py` to discover manifests with current
receipts, filter tags, group revisions, and resolve the newest non-rejected
revision. The resolver excludes stale, tampered, quarantined, or
deterministically failed bundles by running the same complete, non-mutating
bundle validation used at direct inspection time. With `--current`, the
resolver selects the newest non-superseded `validated` or `published` revision
when one exists; a newer draft remains discoverable in the unfiltered listing
but cannot displace that governed current. When no validated or published
revision exists, the newest non-rejected draft is current. Only the ancestry of
a newer `validated` or `published` revision derives `superseded`, without
rewriting prior bytes. A generated index caches persistence, but manifests plus
their current receipts remain the source of discovery truth.

## Validation and Publication

Validation layers:

1. schema shape;
2. reference closure and ID uniqueness;
3. evidence/status invariants;
4. source syntax;
5. semantic reconciliation;
6. render inspection;
7. accessibility;
8. persistence and digest closure.

`PASS` applies only to the named checks and exact member digests. `NOT_RUN`
always requires a reason. Schema validation alone never means semantic or
publication approval. A `validated` or `published` lifecycle declaration
requires every named check and the overall receipt to be `PASS`; `N/A` does not
satisfy this lifecycle gate. Drafts may retain `N/A` or `NOT_RUN` with explicit
evidence or limitations. Manual checks enter a receipt only through an explicit
external attestation bound to the same manifest/member digests and assessor
provenance. Package-local processing remains advisory because this package
ships no attestor trust anchor: it preserves assessment evidence but cannot
produce authoritative overall PASS or authorize validated/published state.
Editing a receipt or supplying caller-authored YAML never creates authority.

Every semantic member role (`request`, `source`, optional `render`,
`semantic_model`, `textual_equivalent`, and `validation_receipt`) must resolve
to a unique normalized path inside the bundle. Different spellings, symlinks,
or case aliases that collapse onto one file do not satisfy role-aware member
closure.

## Runtime Installation

Canonical source stays in `transmutations/evidence-grounded-diagrams/`.
Generated surfaces under `.agents/skills/`, `.claude/skills/`, or a personal
Codex home are derived.

Selective sync:

```text
tools/sync-generated-skill-package.sh \
  --target <repository-root> \
  --sigil evidence-grounded-diagrams \
  --profiles repo-codex,claude \
  --apply
```

The bootstrap copies top-level support files and every support directory except
`development/`. Validate package closure after generation; discoverability of
`SKILL.md` alone does not prove that referenced resources arrived.
