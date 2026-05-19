# Sigilcraft Session Implementation Layering Seed

## Layer 0: Define Session Baseline

Decision question:

```text
After this layer, we know whether the sigil-development-to-sigilcraft idea is coherent enough for lifecycle design.
```

Included:

- Sigilcraft session handoff with identity, intent, modes, session state, interaction contract, observability, quality bar, anti-patterns, and rename migration questions.
- Local glossary for session-process terminology.
- Define transport report with template selection evidence, decisions, governance, and unresolved gaps.

Deferred:

- Renaming `arcana/sigil-development/`.
- Updating registries, command adapters, invoke contracts, or README references.
- Editing Spellcraft to use the same session-state language.
- Creating runtime session persistence.

Exit evidence:

- Invoke define gate returns `flag` rather than `block`.
- Rename remains explicitly approval-gated.

## Layer 1: Sigilcraft Lifecycle Contract

Decision question:

```text
After this layer, we know how the current sigil-development README and SKILL should describe a resumable craft session.
```

Included:

- Revised lifecycle language: session target, active stage, artifact ledger, decision ledger, open gaps, next route.
- Mode model for start, refine, define, shape, validate, trial, observe, reflect, iterate, promote, and handoff.
- Clear boundary between `invoke` authoring artifacts and sigilcraft lifecycle ownership.
- Compatibility decision: canonical rename now, alias-only now, or docs-first rename.

Deferred:

- Filesystem move from `arcana/sigil-development/` to `arcana/sigilcraft/`.
- Registry mutation until compatibility decision is approved.
- Spellcraft session updates.

Exit evidence:

- README.md and SKILL.md can be reviewed as a coherent lifecycle contract.
- Existing sigil-development behavior remains addressable.

## Layer 2: Runtime And Compatibility Surface

Decision question:

```text
After this layer, we know whether `sigilcraft` can be exposed without breaking existing `sigil-development` routes.
```

Included:

- Command adapter or resolver behavior for `sigilcraft`.
- Compatibility alias for `sigil-development`, if canonical rename is approved.
- Registry entries and documentation references updated in one planned change.
- Telemetry mapping from old and new names to a stable capability identity.

Deferred:

- Removal of old names.
- Canonical upstream promotion.

Exit evidence:

- `tools/arcanum --resolve sigilcraft` or the chosen alias route resolves as expected.
- `tools/arcanum --resolve sigil-development` remains valid during migration.

## Layer 3: Session Examples And Validation

Decision question:

```text
After this layer, we know whether the session model behaves across small, medium, and complex sigil lifecycle work.
```

Included:

- Small example: typo or narrow behavior update, proving the session stays lightweight.
- Medium example: new candidate sigil from idea to README/SKILL and validation.
- Complex example: observed reflection or rename migration with artifacts, decisions, compatibility, and task-session handoff.
- Negative examples for hidden rename, task/session confusion, invoke authority creep, and missing stage closeout.

Deferred:

- Registry promotion.

Exit evidence:

- Examples produce pass, flag, and block outcomes with reviewable artifacts.

## Layer 4: Observability And Reflection

Decision question:

```text
After this layer, we know whether craft sessions emit useful signals for later improvement.
```

Included:

- Session-stage telemetry signals.
- Reflection thresholds for repeated gaps, output drift, and manual review.
- Stage closeout envelope fields: target, stage, outputs, validation, open gaps, next route.
- Mapping from telemetry to targeted lifecycle iteration.

Deferred:

- Automation beyond existing observed invocation hooks unless separately approved.

Exit evidence:

- A representative sigilcraft run appends one valid observed invocation signal.
- Reflection state updates without losing compatibility with existing sigil-development telemetry.

## Layer 5: Promotion And Cleanup

Decision question:

```text
After this layer, we know whether Sigilcraft should replace Sigil Development as the canonical public surface.
```

Included:

- Approved rename or alias decision.
- Registry and README update.
- Adapter compatibility policy.
- Migration note for old references.
- Optional follow-up design for Spellcraft session-state parity.

Deferred:

- Removing compatibility aliases until repeated use proves safe.

Exit evidence:

- User approves promotion.
- Validation confirms old and new invocation paths behave as intended.
