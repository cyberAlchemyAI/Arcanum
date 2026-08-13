# Tracked Machine-Artifact Constitution

Status: candidate
Date: 2026-08-08
Owner: Constitution Governance

## Purpose

This constitution defines the reusable admission form for repository-tracked
`.json`, `.yml`, and `.yaml` changes and for current-tree residue checks over
those forms. It prevents an extension from becoming an allowlist: an extension
selects this constitution, but never grants admission by itself.

The constitution owns reusable vocabulary, selectors, precedence, lifecycle
gates, and validation obligations. A repository owner owns every concrete
policy entry, legacy baseline, adoption date, semantic validator, migration
adapter, cutover decision, and Git index/history decision. This document
therefore does not declare this repository's allowlist or authorize any
artifact change.

## Scope

Apply this constitution to a candidate staged addition, modification, rename,
or deletion whose old or new path has the `.json`, `.yml`, or `.yaml` extension,
and to protected current-tree paths with one of those extensions when checking
migration residue.

It governs admission form, not artifact semantics. It does not apply to JSONL
or another format until a separate constitution selects that format. It does
not authorize Git history rewriting, changing an already-tracked file's status
through `.gitignore`, promotion, publication, deployment, or a consumer's
repository policy.

## Authority and Required Repository Policy

For each target-extension change, the owning repository must supply exactly one
matching entry in its own tracked-artifact policy. The entry must bind all of
the following:

- a stable entry ID and the repository identity it belongs to;
- an exact repository-relative path or a narrow repository-relative selector;
- an artifact role and its owning capability or repository owner;
- allowed operations: `add`, `modify`, `rename`, and/or `delete`;
- form and lifecycle state, including a legacy-baseline binding when relevant;
- the deterministic validators that the operation must pass;
- a generator binding when the artifact is a generated projection;
- a migration ID and action binding when the operation is `migration-only`;
- an expiry and closure condition for every temporary exception.

No entry may be borrowed from another repository. A repository-local policy
entry is evidence for selection only inside the repository identity it names;
it cannot create authority over a sibling repository, submodule, parent, or
consumer repository.

An unmatched target-extension change is denied. More than one matching entry
is ambiguous and denied. A policy must not use a broad selector to silently
admit a path that a narrower rule prohibits.

## Composition and Conflict Rules

Policy entries select narrowest-first:

1. an exact repository-local path entry;
2. a narrower repository-local selector;
3. a repository-local artifact-role default.

A migration baseline is not an independent selector. It may bind only to the
already selected entry and can add lifecycle evidence obligations; it cannot
match or admit an otherwise unmatched path.

The resulting constitution pack also composes narrowest-first:

1. the selected repository-local policy entry;
2. the Schema Constitution for a `*.schema.*` form;
3. this constitution for its target extensions;
4. the Artifact Constitution;
5. the Gitignore Constitution's tracked/generated boundaries.

The selected entry does not override non-admission guardrails from a wider
constitution. In particular, Artifact Constitution classes, Schema Constitution
format rules, and the Gitignore Constitution's already-tracked and
generated-artifact boundaries remain conjunctive obligations. Repository-local
policy is the narrowest authority for its own contents; it never weakens those
guardrails.

Equal-precedence entries that both match are a deterministic conflict and deny
the change. A conflict between a selected entry and an artifact-class,
format, generated-projection, lifecycle, or history guardrail also denies the
change until the owner narrows or removes the contradiction. No newest-file,
longest-glob, or validator-success tie-breaker is allowed.

A rename is evaluated as a coupled delete at the prior path and add at the next
path. Both sides must have one matching policy entry and satisfy their own
operation, lifecycle, and validator obligations; a rename cannot bypass an
add or prohibition rule.

## Admission Rules

| Rule ID | Rule |
| --- | --- |
| `tracked-machine.extension-selects-only` | A target extension selects this constitution only. It does not admit a change, determine an artifact role, or waive an owner validator. |
| `tracked-machine.one-entry` | Exactly one repository-owned policy entry must match each target record. Unmatched and ambiguous records deny. |
| `tracked-machine.entry-binding` | The selected entry must bind selector, role, owner, operation, form/lifecycle state, deterministic validators, and applicable generator, migration, and exception fields. Missing required evidence denies or blocks the decision. |
| `tracked-machine.operation` | The requested operation must be explicitly listed. A rename must satisfy both old-delete and new-add obligations. |
| `tracked-machine.schema-format` | A selected entry cannot admit a schema form that the Schema Constitution prohibits. New canonical machine-readable schema artifacts remain `.schema.yml`; tracked non-YML schemas require a scoped migration. |
| `tracked-machine.lifecycle-form` | A selected entry cannot admit an old form that its lifecycle state prohibits, even when the path, role, and operation would otherwise match. |
| `tracked-machine.generated-projection` | A generated projection requires a declared generator route, canonical-source co-change, generator identity and version, and an output-digest receipt. Direct projection edits deny. |
| `tracked-machine.default-deny` | A missing policy, missing validator result, stale or non-pass required evidence, unlisted operation, or unresolved conflict denies or blocks admission. |
| `tracked-machine.historical-evidence` | Immutable historical evidence is a separate non-source role. It may not become a live source dependency or bypass old-form prohibition. |
| `tracked-machine.ownership-boundary` | The coordinator, typed adapter, domain validator, consumer owner, and policy owner retain the separate responsibilities defined below. |
| `tracked-machine.no-history-rewrite` | Current/future admission and residue checks never authorize rewriting earlier commits. |

### Examples

- A repository policy explicitly lists `formulae/dispatch-spec/dispatch.schema.yml`
  as a `source` artifact, allows `modify`, names its owner and validators, and
  the validators pass. The candidate change may be admitted by that repository.
- A repository policy lists a baseline `.schema.json` path in `migration-only`;
  a declared adapter action presents the expected prior digest, next digest,
  required receipts, and validators. The action may be considered for
  admission by that repository.

### Non-examples

- Adding `notes.json` because JSON is a target extension.
- Reusing another repository's `package.json` policy entry.
- Resolving two matching selectors by choosing the more recently written one.
- Editing `.agents/skills/**` generated JSON directly without canonical-source
  co-change, generator identity/version, and output receipt.

The examples describe policy shape only. They are not entries in this
repository's policy.

## Lifecycle of an Old Form

`current` names the replacement or normal form. The following states govern an
old form. A state describes obligations; it does not itself change a path,
rewrite history, or accept a migration.

| Rule ID | State | New old-form admission | Existing old-form mutation | Gate to enter or leave the state |
| --- | --- | --- | --- | --- |
| `tracked-machine.lifecycle.deprecated` | `deprecated` | The repository owner may warn or deny under its declared policy. | Ordinary mutation may remain available while a migration is prepared. | Name the replacement form, owner, and impact inventory. |
| `tracked-machine.lifecycle.new-only` | `new-only` | Deny every new old-form path. | Existing baseline membership remains bounded; it does not authorize expansion or an unbound migration. | Freeze exact baseline membership and initial snapshot; provide the current-form validator and no-new-old-form check. |
| `tracked-machine.lifecycle.migration-only` | `migration-only` | Deny. | Only a declared typed migration action may mutate, rename, or delete a baseline member. | Bind migration, adapter, expected prior and next digest, validators, reference repair, equivalence, rollback evidence, and owner authority. |
| `tracked-machine.lifecycle.prohibited` | `prohibited` | Deny. | Deny. | Replacement verified; references repaired; domain equivalence receipt accepted; consumer cutover accepted; protected live-source residue is zero; rollback disposition recorded. |
| `tracked-machine.lifecycle.retired` | `retired` | Deny. | Deny. | Preserve prohibition evidence through its observation window, close residue, and archive the registry closure. |

Backward movement is never inferred from a failed action. Rollback requires an
owner-approved transition to a named earlier state, a declared rollback method,
and a new receipt.

### Baseline and Action Digests

At `new-only`, a baseline freezes **membership**: the exact old-form paths,
their identity, and the inventory snapshot are fixed. It is not a permanent
wildcard and it is not one unchanging content digest for a path.

Each `migration-only` action is a compare-and-swap operation. It declares the
member, expected prior digest, emitted next digest, migration ID, action ID,
and receipt identity. A stale prior digest denies the action. Changing one
baseline member never adds a new member or silently changes a different
member's expected digest.

### Residue and Historical Evidence

Protected live-source residue is the current-tree set of source artifacts that
still use the prohibited old form. Immutable historical evidence may remain
only under a separately declared non-source role. It is outside live-source
residue, but it must be immutable and cannot be imported, resolved, or cited as
a live source dependency. Reference-repair validation must deny such a live
source reference before the migration reaches `prohibited`.

Earlier commits are historical evidence, not current-tree residue. This
constitution governs present/future tree admission only and never authorizes a
history rewrite.

## Migration Ownership Boundary

The generic migrations coordinator may do only the following: registry and DAG
handling, action eligibility, receipt admission, phase reduction, and residue
calculation. It must not transform an artifact, repair a reference, infer
semantic equivalence, or accept a consumer cutover.

Typed adapter owners perform transformation, reference repair, and rollback.
Domain validator owners verify equivalence. Consumer owners accept cutover.
The repository policy owner supplies the concrete policy and baseline. A
coordinator output is a side-effect-free eligibility or transition decision;
an authorized owner writes any next registry snapshot separately.

## Related Constitution Boundaries

- The [Artifact Constitution](ARTIFACT-CONSTITUTION.md) retains its source,
  durable-evidence, generated-artifact, and local-runtime classifications. Its
  development-to-canonical promotion rules continue to apply.
- The [Schema Constitution](SCHEMA-CONSTITUTION.md) retains `.schema.yml` as
  the canonical schema form and treats tracked non-YML schemas as explicit
  migration work rather than new ordinary source.
- The [Gitignore Constitution](GITIGNORE-CONSTITUTION.md) retains the
  already-tracked and generated/local-state boundaries. An ignore pattern does
  not untrack a file or grant it admission; generated output still needs an
  appropriate policy role and evidence.

## Validation Mapping

The existing Artifact Constitution validator is an evidence floor, not an
admission engine. It currently checks unignored local/generated artifacts,
tracked local runtime state, new non-YML schema formats, schema-shaped Markdown
boundaries, and a chart-text rule. It does **not** select a repository policy,
inspect the staged index as an admission decision, resolve selector ambiguity,
verify migration receipts/digests, validate source references, or reject a
direct generated-projection edit.

| Constitution rule IDs | Validation mode | Current or required validation surface |
| --- | --- | --- |
| `tracked-machine.extension-selects-only` | review | Constitution Governance review of scope until the policy compiler exists. |
| `tracked-machine.one-entry`, `tracked-machine.entry-binding`, `tracked-machine.operation`, `tracked-machine.default-deny` | future | Dedicated strict policy compiler/admission validator with staged-index and full-tree fixtures. |
| `tracked-machine.schema-format` | deterministic | `tools/validate-artifact-constitution.sh` and the Schema Constitution. |
| `tracked-machine.lifecycle-form`, `tracked-machine.lifecycle.deprecated`, `tracked-machine.lifecycle.new-only`, `tracked-machine.lifecycle.migration-only`, `tracked-machine.lifecycle.prohibited`, `tracked-machine.lifecycle.retired` | future | Migration-registry, receipt, transition, reference, residue, and rollback validators with passing and failing fixtures. |
| `tracked-machine.generated-projection` | future | Dedicated generated-projection admission fixture and validator. |
| `tracked-machine.historical-evidence` | future | Artifact-role plus reference-repair validator and fixtures. |
| `tracked-machine.ownership-boundary`, `tracked-machine.no-history-rewrite` | review | Owner review against this constitution and the selected migration contract. |
| Candidate promotion and any claim of strict admission, commit rejection, or canonical status | blocked | Blocked until a dedicated validator passes both passing and failing fixtures and one repository owner adopts an exact policy through it. |

Run the existing evidence floor only for its actual checks:

```bash
bash tools/validate-artifact-constitution.sh --self-test
bash tools/validate-artifact-constitution.sh
```

The required strict staged/full-tree policy validator is future work. Until it
exists, this constitution is a candidate and cannot claim strict enforcement,
commit rejection, full-tree admission, canonical status, or promotion.

## Candidate Fixtures

Readable expected cases are maintained at:

`arcana/migrations/development/constitution-fixtures/tracked-machine-artifact-cases.md`

They describe passing and failing future-validator behavior; they are neither a
repository policy nor an executable substitute for one.

## Promotion Boundary

This constitution remains `candidate` until all of the following hold:

1. a dedicated strict staged/full-tree validator exists and maps its checks to
   these rule IDs;
2. passing and failing fixtures cover the admission, ambiguity, lifecycle,
   stale-digest, residue, reference, generated-projection, and cross-repository
   boundaries;
3. a repository owner adopts an exact repository-local policy through that
   validator; and
4. Constitution Governance reviews the validator result, fixture coverage,
   ownership boundary, and compatibility with the Artifact, Schema, and
   Gitignore Constitutions.

No validation report, generated fixture, policy draft, coordinator receipt, or
this candidate file is promotion authority by itself.

## Maintenance

Split this constitution if generic policy admission and old-form lifecycle
governance cease to share selectors, precedence, and fixtures. Route a change
through Decision Gate if a proposed repository policy needs to override a
format, artifact-class, generated-projection, historical-evidence, or history
boundary.
