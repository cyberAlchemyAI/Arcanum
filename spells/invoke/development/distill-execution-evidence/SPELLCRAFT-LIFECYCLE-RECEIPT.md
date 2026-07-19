# Spellcraft Lifecycle Receipt: DEC-DEE-001

## Identity

- Spellcraft mode: `validate`
- Spell: `invoke`
- Canonical ID: `invoke`
- Alias used: none
- Scope: library
- Source Invoke handoff: `INVOKE-RESULT.md`
- Source SWU: `SWU-DEE-001`
- Decision: **accept with bounded narrowing**
- Lifecycle status: resolved

## Accepted Invariant

Only a validator-derived result over provenance-resolvable, contract-complete Distill evidence
may authorize Invoke handoff. An authored verdict, schema-valid receipt, or runtime event by
itself has no handoff authority.

## Accepted L0 Projection

Spellcraft accepts a versioned JSON projection for the first implementation slice:

1. `DistillRunRequest` freezes the parent Invoke run, mode namespaces, finite budget, requested
   techniques, and reviewed-input provenance.
2. `DistillExecutionReceipt` projects role/process/technique/result evidence and references
   runtime evidence; it is not authoritative.
3. `DistillValidationResult` is validator-owned and alone carries
   `mutation_handoff_allowed`.

The receipt may later be folded into validation if lifecycle evidence proves it redundant.
The validator-authoritative invariant must survive any topology change.

## Accepted Provenance Policy

For a reviewed artifact whose content can change and whose result may unlock mutation, the
future accepted evidence path must identify the exact reviewed content. Default evidence is a
recomputed content digest plus path and size; an alternative is allowed only when it identifies
the content exactly and immutably. Mutable paths or non-exact repository state are insufficient.

This policy applies prospectively to the accepted evidence path. It does not retroactively
invalidate historical Distill traces or claim that the earlier Workbench run definitely did not
execute Distill.

## Bounded Narrowing

- The runtime event grammar, event store, capability probe, and emission adapter remain owned
  by `SWU-DEE-003`; their canonical owner is not selected here.
- Any Distill sigil contract mutation routes through Sigil Development.
- Invoke spell schemas, validator-result consumption, and mode composition remain owned by
  Spellcraft.
- Task Session may implement only the selected SWU and cannot widen lifecycle authority.
- Anti-bias composition remains limited to qualifying governed multi-agent subject groups.
- Deferred Invoke `full` and Invoke `validate` remain unsupported; this decision does not
  implement them.

## SWU-DEE-002 Binding

Canonical lifecycle owner: `invoke` through Spellcraft.

Execution owner: Task Session, one SWU only.

Exact write scope:

- `arcanum/spells/invoke/schemas/distill-run-request.schema.json`
- `arcanum/spells/invoke/schemas/distill-execution-receipt.schema.json`
- `arcanum/spells/invoke/schemas/distill-validation-result.schema.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/valid-run-request.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/valid-execution-receipt.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/valid-validation-result.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/invalid-run-request-missing-budget.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/invalid-receipt-missing-role-trace.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/invalid-result-missing-handoff-flag.json`
- `arcanum/spells/invoke/development/run-distill-evidence-schema-fixtures.sh`

Task Session governance and completion-evidence scope:

- `arcanum/spells/invoke/development/distill-execution-evidence/SPELLCRAFT-LIFECYCLE-RECEIPT.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/WORK-PACK.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/tasks/TASK-DEE-02-EVIDENCE-SUBSTRATE.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/results/SWU-DEE-002-RESULT.md`

This governance scope may record the bounded implementation and its deterministic evidence. It
does not widen the implementation scope or grant Task Session lifecycle authority over later
SWUs. The result artifact is the authorized post-run evidence surface for this unit; central
observability remains deferred until its parent-repository ledger paths receive separate write
authorization.

The selected unit owns structural contracts only. It must not implement runtime event
resolution, semantic/provenance adjudication, mode integration, generated mirrors, or Workbench
replay.

## Acceptance Conditions For SWU-DEE-002

- all three schemas carry explicit versions and reject unknown required-contract omissions;
- valid fixtures parse and satisfy their matching schema;
- each malformed fixture fails for its named missing obligation;
- schema validation does not claim execution proof or mutation readiness;
- the fixture runner is deterministic and uses no model call;
- the existing Invoke experiment harness remains the reusable validation owner;
- runtime-behavior promotion remains blocked until DEE-003 through DEE-010 produce event,
  semantic, provenance, mode, and adversarial evidence.

## Rejected Alternatives

- receipt-only or schema-only authorization;
- treating one append-only event as a verdict;
- selecting a repository-wide event store before its owner contract exists;
- retroactive invalidation of historical evidence;
- blanket anti-bias composition;
- implementing multiple SWUs under this receipt.

## Validation And Observability

- Source Define/Design/Plan package: structurally validated.
- Distill role trace: true-subagent design pass and structural plan pass preserved.
- Existing Invoke fixture harness: available; it does not yet prove the new evidence behavior.
- Experiment Harness requirement: configured in Invoke development; new reusable behavior
  remains blocked until focused evidence fixtures and reports exist.
- Observability: this receipt is the durable lifecycle record. Central observability append is
  deferred because its ledger paths are outside SWU-DEE-001's authorized write scope.

## Next Route

`task-session` on `SWU-DEE-002` only. `SWU-DEE-003` through `SWU-DEE-013` remain blocked and
unselected.
