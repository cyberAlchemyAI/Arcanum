# SWU-DV2-001 — Bounded Direct Implementation Contract

- Contract ID: `SWU-DV2-001-DIRECT-CONTRACT-2026-08-27`
- Route: bounded direct repository-local
- Embedded contract status: candidate pending independent rereview
- External review status: PASS (`SWU-DV2-001-DIRECT-CONTRACT-REVIEW-004`)
- Current authority: contract preparation only
- Implementation authorized: no
- Normal Task Session: excluded by explicit user direction

## Outcome Boundary

The future execution may create only the first TechniqueSpec vertical:

1. common structural schema,
2. TechniqueSpec schema,
3. `abstraction_level_guard` machine instance,
4. one positive and four persisted negative fixtures plus their manifest,
5. one deterministic Python fixture validator and its unit test,
6. exact run-local inventory and execution receipt.

It proves representational grammar and canonical-instance fidelity only. It does
not prove a complete Distill run, mode/profile/source closure, runtime readiness,
Invoke compatibility, publication, deployment, or promotion.

## Frozen Inputs

- Decision Gate: `STRICT-V2-8` plus `BOUNDED-OVERRIDE-BUDGETS`, exact machine
  record SHA-256 `2183eb31...3094`.
- Canonical sources: schema plan, SWU task, validation strategy, technique
  registry, and Abstraction-Level Guard spec are digest-bound in the JSON contract.
- Runtime: `/usr/bin/python3.12`, Python 3.12.3, `jsonschema` 4.10.3.
- Constraint: the standalone `referencing` module is absent. Use the installed
  `jsonschema.RefResolver` store; do not install packages or create a package root.

## Exact Mutation Boundary

The JSON contract lists thirteen future targets: eleven product/fixture/validator
create targets and two run-local evidence targets. Every target is currently
absent. The eight exact directory-baseline paths may be created only to contain
those targets and may be removed only by the guarded rollback. Every other
repository file or directory path is forbidden, including existing Distill
files, all Invoke files, generated skills, Git state, registries, dependencies,
network effects, publication, and deployment.

## Validation Denominator

- Both schemas meta-validate under Draft 2020-12 with local `$ref` closure.
- The positive Abstraction-Level Guard instance passes structural and exact
  canonical-instance policy checks.
- Hyphenated ID, forbidden per-technique hook, missing emitted field, unknown
  field, semantic coupling in common primitives, duplicate items, invalid path,
  and unknown enum mutations all block for the intended reason.
- The runner collects every case and returns the complete blocker set while
  preserving the first nonzero status.
- The exact denominator is fourteen cases: one persisted positive, four
  persisted negatives, and nine stable generated mutations. Every negative has
  a named exact blocker code in the machine contract.
- Whitespace, explicit untracked/create content checks, exact path inventory,
  and no-out-of-scope-change checks pass.

## Failure Rule

One `apply_patch` batch creates the eleven implementation targets, then the run
records every target's SHA-256 and size as its immutable rollback identity.
Any acceptance-critical failure stops before the next effect. Rollback may begin
only if all eleven current targets still match those recorded postimages. Any
absence or mismatch preserves every target and directory and blocks for owner
inspection. A passing guard authorizes one exact `apply_patch` deletion batch,
followed by the exact deepest-first `rmdir --` sequence for the seven product
directories that were absent and created by the attempt, only while empty. No
`rm`, glob, Git reset/checkout/clean, forced directory removal, or implicit retry
is permitted. Run-local failure evidence remains.

The changed-path inventory binds the eleven implementation targets and excludes
itself and the execution receipt. The receipt then binds the finalized inventory.
Each evidence document uses an explicit canonical-JSON digest domain that omits
its own digest field, so neither document is self-referential.

After both evidence documents are finalized, one read-only command validates
their JSON syntax, both declared digests, and the receipt's inventory reference.
Its exit status and four-check PASS summary are the outer host result and are not
written back into the receipt. This avoids circular self-validation. A failure at
this final evidence edge preserves every implementation and evidence byte and
stops for owner inspection; it does not trigger rollback or rewrite the receipt.

Scope validation uses two explicit domains: file content/type/existence changes
are limited to the thirteen future file targets, while directory creation/removal
and permission/ownership changes are limited to the eight directory baselines.
Incidental parent-directory mtime/ctime changes caused by authorized children are
excluded from that directory domain.

## Next State

The exact machine contract at SHA-256
`f45e29506ed2206d7497e75fbbd5856eeacf8450f593e93d5302cc8dedb96044`
passed independent read-only review. Its external safe next state is presentation
for a separate explicit execution request. Implementation remains stopped until
the user explicitly asks to execute that exact contract.
