# Tracked Machine-Artifact Constitution Candidate Fixtures

Status: design fixture for `TRACKED-MACHINE-ARTIFACT-CONSTITUTION.md`
Owner: Constitution Governance
Authority effect: none

## Purpose and Boundary

These cases specify expected behavior for the future strict policy compiler and
admission validator. They are readable fixtures, not an executable validator,
not a repository-owned policy, not a migration registry, and not an allowlist
for this repository. Every path, policy entry, digest, owner, and repository ID
below is illustrative only.

The cases use `admit` only to mean that a future implementation may continue to
the listed validator checks. They never authorize a Git change, commit,
promotion, consumer adoption, or history rewrite.

## Common Fixture Vocabulary

- `repository-A` and `repository-B` are distinct repository identities.
- `POL-A-001` is an illustrative repository-A policy entry.
- `MIG-FORM-001` is an illustrative typed migration ID.
- `sha256:prior` and `sha256:next` are illustrative per-action blob digests.
- `old-form` is a form that has entered the named lifecycle state; it is not
  inferred from extension alone.

## Admission Cases

| ID | Candidate record and evidence | Expected future decision | Required reason |
| --- | --- | --- | --- |
| `TMA-01-declared-current-admit` | Repository-A has exactly one exact entry for `specs/current.schema.yml`, role `source`, owner, `modify` operation, current form, and all named validators pass. | admit | Exact repo-local entry, permitted operation, and validator evidence align. |
| `TMA-02-undeclared-path-deny` | Repository-A stages `notes.json`; no repository-A entry matches it. | deny | A target extension selects the constitution but no entry grants admission. |
| `TMA-03-ambiguous-selector-deny` | Two same-precedence repository-A selectors both match `config/service.yml`. | deny | More than one matching entry is a deterministic conflict. |
| `TMA-04-new-old-form-deny` | Repository-A adds `new.schema.json` after that old form is `new-only`. | deny | New old-form paths are denied from `new-only` forward. |
| `TMA-05-baseline-edit-without-action-deny` | Repository-A modifies exact baseline member `legacy.schema.json` during `migration-only`, but supplies no declared migration/action/adapter evidence. | deny | Baseline membership does not authorize an ordinary edit. |
| `TMA-06-stale-digest-deny` | A declared `MIG-FORM-001` action expects `sha256:prior`, but the present member digest differs. | deny | Per-action compare-and-swap rejects stale input. |
| `TMA-07-prohibited-residue-block` | A transition asks for `prohibited` while a protected current-tree source still uses the old form. | block | Live-source residue is nonzero; prohibition cannot be entered. |
| `TMA-08-historical-evidence-retain-reference-deny` | Immutable historical evidence remains under an explicit non-source role after prohibition, while a live source references it as input. | retain evidence; deny source reference | Historical evidence is outside residue only when immutable and non-source; it cannot become a live dependency. |
| `TMA-09-generated-direct-edit-deny` | A generated projection is edited directly without canonical-source co-change, generator identity/version, or output-digest receipt. | deny | A generated path and extension do not grant mutation authority. |
| `TMA-10-cross-repository-reuse-deny` | Repository-B presents `POL-A-001`, which names repository-A, to admit a repository-B `package.json`. | deny | A concrete entry is scoped to its declared repository identity. |

## Coverage Matrix

| Constitution boundary | Cases |
| --- | --- |
| Extension selects but does not admit; exact one-entry rule | `TMA-01`, `TMA-02`, `TMA-03` |
| New-old-form and migration-only lifecycle restrictions | `TMA-04`, `TMA-05` |
| Frozen baseline membership and per-action digest | `TMA-05`, `TMA-06` |
| Prohibition and live-source residue | `TMA-07` |
| Immutable historical evidence and reference boundary | `TMA-08` |
| Generated-projection mutation boundary | `TMA-09` |
| Repository-local ownership boundary | `TMA-10` |

## Future Validator Contract

A dedicated future validator must turn each case into a passing or failing
machine-readable fixture without treating this Markdown as the policy source.
It must test both staged-index admission and full-tree residue where applicable,
and emit stable diagnostics that identify the selected entry, conflict, missing
evidence, lifecycle gate, or repository identity mismatch. Until that validator
and one owner adoption exist, the companion constitution remains candidate.
