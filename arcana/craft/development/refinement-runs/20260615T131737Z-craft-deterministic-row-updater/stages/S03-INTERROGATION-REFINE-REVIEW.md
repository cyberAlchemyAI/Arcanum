# S03 Interrogation: Refine Review

## Structured Interview Result

- Target scope: Craft row updater need.
- Mode: refine-review.
- Questions asked: 0.
- Decisions recorded: 1.
- Artifacts updated: this stage artifact only.
- Verdict: pass.
- Next step: distill strategy selection.

## Evidence-Backed Review Question

Question considered: Should Craft create a dedicated deterministic row updater,
or keep row-update semantics inside `import-csv --dry-run`?

Recommended default: create the row-update planner as an internal deterministic
primitive first, then let CSV import call it.

Why this matters: a broad CSV importer is too coarse as the first proof of safe
YAML writeback. The real acceptance-critical behavior is row selection,
stale-source blocking, ID preservation, reference validation, and patch-plan
determinism.

Unresolved risk if unanswered: the importer may become the accidental owner of
ledger reconciliation semantics, making future non-CSV update surfaces duplicate
or drift from it.

## Critique

The dedicated row updater is justified only if it stays narrower than a new
editing framework. The first slice must be dry-run only and must avoid arbitrary
nested YAML mutation.

The phrase "tool" could overstate the first need. The first need is a
deterministic planner contract and implementation unit. A user-facing CLI can
wait.

## Decision

Proceed with the `deterministic-row-updater` route, interpreted as a dry-run
row update planner primitive.
