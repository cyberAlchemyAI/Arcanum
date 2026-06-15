# Craft Handoff — Automatic Artifact Lifecycle (co-locate · track · index · advance)

- Date: 2026-06-13
- Origin: live use of `craft` in an adjacent private workspace, abstracted for public Arcanum development
- Target contract: `arcana/craft/SKILL.md` (canonical) + working set under `development/craft/` (this folder)
- Hooks: `CRAFT-INTERACTION-CONTRACT.md`, `CRAFT-INTERACTION-DESIGN.md`, `CRAFT-INTERACTION-LEDGER-SCHEMA.yml`, `CRAFT-INTERACTION-DISPATCH.json`
- Type: capability gap + proposed behavior change. Not yet implemented.

## Why this handoff exists

A real adjacent-workspace pipeline ran: `state` over 12 Craft spaces -> research subagents -> `dispatch-spec validate` -> `refine` -> `invoke` produced one canonical `BUILD-SPEC.md` per space, plus a cross-space validation index and four owner handoff docs.

Every step that *should* have been a Craft receipt-application operation had to be done **by hand**, and two of those hand edits **broke the ledger YAML** before being caught by a re-parse. Craft's `<interaction-boundary>` already claims the right scope —

> "Craft may prepare handoffs, receive receipts, apply receipt evidence, and open residue."

— but there is **no mechanism** behind "apply receipt evidence." The result is that the operator (or the model) becomes the integration glue, and the ledger silently drifts out of sync with the artifacts the spaces actually own.

## What went wrong (observed, reproducible)

1. **Artifacts landed outside the owning space.** `invoke` wrote 12 `BUILD-SPEC.md` files into a parallel `docs/specs/<node>/` tree, detached from the `.craft/` space that owns each one. Nothing in Craft objected. The operator had to notice ("each craft space should contain its own files") and relocate all 12.
2. **Artifacts were not tracked.** None of the 12 produced specs appeared in any ledger's `artifacts:` list, `indexes.by_id`, or `indexes.artifacts_by_path`. A `state` / all-status read could not see them. They had to be appended by hand to all 12 ledgers.
3. **Indexes drifted.** `SKILL.md` says "Add or refresh ledger indexes after each meaningful mutation," but provides no routine to do it. `by_id` numeric offsets (`artifacts[N]`) and the `artifacts_by_path` map had to be computed and inserted manually.
4. **`next_move` went stale.** After research executed and specs were authored, every context's `next_move` still described the *pre-execution* step. Advancing them was a separate manual pass (and the context value and its `indexes.next_moves` mirror had to be kept in sync).
5. **Hand-editing corrupted the ledger twice.**
   - A replacement value contained `Pending: ` — an unquoted `": "` inside a YAML scalar — and broke 11 ledgers at once (`mapping values are not allowed here`).
   - The repo-root ledger indents list items by **2 spaces** (`  - artifact_id:`) while node ledgers use **column-0** (`- artifact_id:`); a one-size insertion produced an invalid block.
   Both were only caught because a `yaml.safe_load` validation pass was run afterward — Craft itself has no write-time safety.

## Proposed Craft behavior (make these automatic)

Implement an **`apply_receipt`** operation (realizing the `<interaction-boundary>` promise) plus invariants enforced on every mutating method:

### B1 — Co-location invariant (enforce on receipt)
When a called capability (`refine`, `invoke`, `task-session`, …) reports a produced canonical artifact for a space, its path MUST resolve **inside that space's scope**: the space root (sibling to `.craft/` and `CRAFT.md`) or `.craft/artifacts/`. An artifact written outside the owning scope is a `flag`/`block`: Craft either relocates it (and rewrites references) or refuses the receipt with a clear residue. No parallel detached trees.

### B2 — Automatic artifact tracking (`apply_receipt`)
On a receipt naming artifact(s), Craft appends a complete `artifacts:` row (`artifact_id`, `owner_context_id`, `path`, `artifact_type`, `status`, `notes`) and updates `indexes.by_id` (correct list offset) and `indexes.artifacts_by_path`. ID convention derived from the space prefix (e.g. `ART-<PREFIX>-<KIND>`). Idempotent: re-applying the same receipt updates in place, never duplicates.

### B3 — Index maintenance as a routine, not a reminder
Replace the prose "refresh indexes" guidance with a deterministic `reindex(ledger)` that rebuilds `by_id`, `artifacts_by_path`, `active_blockers`, `blocking_decisions`, `open_decisions`, `active_gaps`, and `next_moves` from the row families. Called after every mutation. (Would have prevented defects 2–4.)

### B4 — `next_move` advancement on stage close
When a receipt advances/closes a route stage for a context, Craft advances that context's `next_move` to the post-stage action **and** its `indexes.next_moves` mirror, atomically. Stale pre-stage next_moves should not survive a successful receipt.

### B5 — Cross-space artifacts attach to the parent
Artifacts that span multiple spaces (cross-cutting index, per-owner handoffs) attach to the parent/recomposition space, not to one child and not to a detached path. In the source fixture, these were the dispatch-validation record plus role-bound handoff files, now tracked in the parent recomposition ledger.

### B6 — YAML-safe ledger writer (prerequisite for B1–B4)
A structured read-modify-write that:
- quotes/escapes any scalar containing `: `, leading `?`, `#`, etc. (defect 5a);
- detects and **matches the file's existing list-item indentation** (column-0 vs 2-space) and key style (defect 5b);
- preserves comments, key order, and the `? key : value` block-mapping style used in `artifacts_by_path`;
- re-parses after write and fails closed on a parse error.
Text-surgery insertion (what was done by hand here) is explicitly insufficient; this likely needs `ruamel.yaml` round-trip or an equivalent format-preserving writer, since plain `yaml.safe_dump` would reformat the human-tuned ledgers.

## Acceptance criteria

- Running `invoke`/`refine` against a Craft space leaves the produced artifact **inside the space** and **tracked** in that space's ledger (row + both indexes) with **zero manual edits**.
- `state` / all-status immediately reflects the new artifact and the advanced `next_move`.
- Re-applying a receipt is idempotent.
- A mutation that would produce invalid YAML fails closed with residue, never writes a broken ledger.
- Works uniformly across ledgers with differing indentation styles (the source repo-root space vs. the node spaces are a good fixture pair).

## Evidence / fixtures (abstracted)

- 12 ledgers exercised in an adjacent private workspace: one repo-root ledger plus feature and strategy node ledgers. Exact local paths are intentionally omitted from this public artifact.
- Corrected end-state (what the automation should have produced): each space now holds its own `BUILD-SPEC.md` (features at `docs/features/<node>/`, strategy at `docs/strategy/development/<node>/`, repo-root space at `.craft/artifacts/BUILD-SPEC.md`), each tracked via an `ART-<PREFIX>-BUILD-SPEC` row + indexes; `next_move` advanced to the spec-authored state.
- Indentation-divergence fixture: repo-root `.craft/ledger.yml` (2-space list items, `GQ` prefix) vs. any node ledger (column-0 list items).
- The two break modes (unquoted `": "`, mismatched indentation) are both reproducible from the pre-correction state in git history.

## Suggested next step for the maintainer

1. Land `apply_receipt` + the B6 writer behind `CRAFT-INTERACTION-CONTRACT.md`; wire B1–B5 invariants into `state`/`decide`/`recompose` and the receipt path.
2. Add the indentation-divergence + `": "`-scalar cases to the Craft interaction validation fixtures.
3. Reflect the `<interaction-boundary>` and `<process>` (step 6) sections in `arcana/craft/SKILL.md` from prose guidance to enforced operations.
