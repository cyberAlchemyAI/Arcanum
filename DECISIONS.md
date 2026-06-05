# Decisions

## GUIDE-B-003: First Guide Spellcraft Target

| Field | Value |
| --- | --- |
| Status | `pass` |
| Timestamp | `2026-05-29T19:00:44Z` |
| Target scope | `development/user-guide/packages/guide/` |
| Consequential work blocked | Mutation-capable `spellcraft` for Guide. |
| Source | `development/user-guide/packages/guide/WORK-PACK.md`, `development/user-guide/packages/guide/SPELLCRAFT-HANDOFF.md` |

### Decision Question

Should the first Guide spellcraft target be narrow `guide-architecture` or generic `guide`?

### Options

| Option | Benefit | Cost / Risk | Choose When | Downstream Impact |
| --- | --- | --- | --- | --- |
| `guide-architecture` | Narrow, fixture-backed, easier to validate; directly matches the existing `/guide this architecture` route fixture. | May feel less general at first; later generalization step required. | We want the smallest reliable spellcraft slice. | Spellcraft can start with architecture-specific phases, fixtures, and validation. |
| `guide` | Matches the long-term user-facing command immediately. | Broader surface, more dispatch cases, higher risk of vague orchestration and under-specified validation. | We want to design the generic umbrella now and accept slower validation. | Spellcraft must define route families and stricter dispatch budgets before implementation. |

### Recommendation

Select `guide-architecture` first, then generalize to `guide` after one validated spell slice exists.

### Selected Option

`guide-architecture`

### Rationale

The user selected option 1 via `invoke refresh 1`. `guide-architecture` is narrow, fixture-backed, and directly matches the existing `/guide this architecture` route fixture. This keeps the first spellcraft slice small enough to validate before generalizing to a broader `guide` spell.

### Remaining Blockers

- None for first spellcraft target selection. `GUIDE-B-003` is resolved.

### Deferred Decisions

- Runtime dispatch budget defaults.
- Allowed callable capabilities in Guide L0.

### Assumptions

- User ledger and Translate L0/L2 evidence remain valid inputs.
- Spellcraft should start with `guide-architecture`, then generalize later to `guide`.

## 2026-06-01 - SWU-CLEAN-004 Personal And Live Surface Cleanup

- Target scope: `SWU-CLEAN-004`
- Status: PASS
- Decision question: How should Arcanum remove duplicate Codex skill and legacy command suggestions from live personal and repository surfaces?
- Consequential work blocked:
  - moving or removing generated packages under `/mnt/c/Users/vlad_/.codex/skills`
  - cleaning live repository `.codex/commands`
  - final verification that duplicate Arcanum suggestions no longer appear
- Source context:
  - `tools/development/CODEX-SKILL-SURFACE-CLEANUP-DRY-RUN.md`
  - `tools/development/CODEX-SKILL-SURFACE-CLEANUP-DRY-RUN-20260601T115842Z.md`
  - `tools/development/CODEX-SKILL-SURFACE-CLEANUP-POST-CLEANUP-20260601T120907Z.md`
  - `tools/development/CODEX-SKILL-SURFACE-CLEANUP-WORK-PACK.md`
  - `tools/development/task-sessions/20260601T113112Z-swu-clean-003.md`
  - `tools/development/task-sessions/20260601T121233Z-swu-clean-004.md`

### Options

1. Approve backed-up cleanup of generated duplicates.
   - Benefit: removes duplicate suggestions now while preserving rollback state.
   - Cost or risk: mutates personal Codex home and live repo generated surfaces.
   - When to choose: choose this when the dry-run classification is trusted.
   - Downstream impact: proceed with `SWU-CLEAN-004`; move remove candidates into timestamped backup directories, preserve unknowns, and rerun inventory.

2. Run another dry-run after regenerating alias-only surfaces.
   - Benefit: refreshes the candidate list against the newest generator behavior before mutation.
   - Cost or risk: adds one more validation step before cleanup.
   - When to choose: choose this when the current dry-run may be stale.
   - Downstream impact: produce a new dry-run report, then reopen this decision with updated counts.

3. Clean repository generated commands only.
   - Benefit: reduces repo-local duplicate command noise without touching personal Codex home.
   - Cost or risk: personal skill suggestions remain duplicated.
   - When to choose: choose this when machine-global cleanup should wait.
   - Downstream impact: run `--clean-legacy-codex-commands` on the repo and keep personal cleanup blocked.

4. Stop cleanup and keep compatibility surfaces.
   - Benefit: avoids any live mutation.
   - Cost or risk: duplicate suggestions remain and the export surface stays noisier.
   - When to choose: choose this if legacy command compatibility is more important than discovery hygiene.
   - Downstream impact: mark `SWU-CLEAN-004` deferred and document duplicate suggestions as accepted compatibility debt.

### Recommendation

Recommended option: Option 2 first, then Option 1 if the refreshed dry-run still matches generated provenance expectations.

Rationale: `SWU-CLEAN-002` changed the generator to alias-only packages and `SWU-CLEAN-003` added a safe legacy command cleanup path. A fresh dry-run gives the final candidate list after those changes, then backed-up cleanup can proceed with less ambiguity.

### Decision Record

- Selected preliminary option: Option 2, refresh dry-run before cleanup.
- Selected final option: Option 1, backed-up cleanup of generated duplicates.
- Rationale: user selected `invoke refresh 1` after option 2 refreshed the evidence; generated remove candidates were moved to backups and unknown entries were preserved.
- Source of decision: user messages on 2026-06-01.
- Refreshed dry-run result: personal skills keep 44, remove candidates 40, unknown 1; repository skills keep 0, remove candidates 0, unknown 0; legacy commands keep 0, remove candidates 84, unknown 1.
- Cleanup result: personal skills keep 44, remove candidates 0, unknown 1; repository skills keep 0, remove candidates 0, unknown 0; legacy commands keep 0, remove candidates 0, unknown 1.
- Backups:
  - personal duplicate skill packages: `/mnt/c/Users/vlad_/.codex/skills/.cleanup-backups/20260601T120907Z/personal-skills/`
  - generated legacy command files: `tools/development/cleanup-backups/20260601T120907Z/codex-commands/`
  - manifest: `tools/development/cleanup-backups/20260601T120907Z/manifest.txt`
- Remaining blockers: none for generated duplicate cleanup.
- Deferred decisions: optional policy for unknown `arcanum-orchestrate` personal package and unknown `.codex/commands/arcanum-runtime-smoke.md`.
- Assumptions: generated files are identified by Arcanum provenance frontmatter or legacy command markers.
