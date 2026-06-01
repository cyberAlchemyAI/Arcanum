# Session Handoff: Guide / User / Translate Continuation

## Identity

- Source session reference: current Codex session ending 2026-06-01, plus committed artifact `706dae5 Add user guide translation overview`
- Destination label: `guide-user-translate-continuation`
- Handoff type: `new-lifecycle-thread`
- Target project or lifecycle: Arcanum `User / Translate / Guide` capability family
- Created for: start a new session with enough context to continue architecture, validation, or execution without replaying the whole conversation

## New Session Prompt

```text
Continue the Arcanum Guide / User / Translate work from the session handoff. Start by reading the handoff and the linked package artifacts. Decide whether the next route should be spellcraft validation for guide-architecture, task-session execution for the first ready package task, or invoke design/plan refresh if the architecture has drifted. Preserve the boundary that User and Translate are candidate sigil packages, while guide-architecture is the first candidate spell slice.
```

## Route Rationale

- Recommended next route: `spellcraft` for `guide-architecture` validation, then `task-session` for the next ready package task.
- Rationale: the broad concept has already been split into three packages and a first narrow spell slice. The next session should validate or execute from those artifacts instead of redefining the idea from scratch.
- Lifecycle owner: `spellcraft` for `spells/guide-architecture/`; `task-session` for bounded package work; `sigil-development` later for User/Translate promotion.

## Context Builder Selection

| Obligation | Coverage | Selected Source | Why It Matters |
| --- | --- | --- | --- |
| Preserve the high-level purpose | covered | `development/user-guide/guide-user-translate-overview.html` | Gives a 5-minute overview of what User, Translate, and Guide are trying to achieve. |
| Preserve package order and boundaries | covered | `development/user-guide/packages/README.md` | Records that User ledger comes first, then Translate, then Guide orchestration. |
| Continue from the first spell slice | covered | `spells/guide-architecture/README.md` | Defines `guide-architecture` as the current candidate spell and names its phases, gates, and dependencies. |
| Keep User as protected ledger, not uncontrolled memory | covered | `development/user-guide/packages/user-ledger/USER-LEDGER-SCHEMA.yml` and `VISIBILITY-POLICY.md` | Prevents new sessions from turning User into raw transcript storage or silent profile mutation. |
| Keep Translate separate from Guide | covered | `development/user-guide/packages/translate/GUIDE-CALL-CONTRACT.md` | Preserves Translate as the vocabulary/domain bridge Guide may call, not as hidden Guide internals. |
| Know what was committed | covered | git commit `706dae5` | Confirms the HTML overview was committed and pushed to `origin/main`. |

Strict coverage: `pass`

## Selected Session Context

- `development/user-guide/guide-user-translate-overview.html`
  - Obligation refs: purpose, current state, next steps
  - Context summary: PDF-exportable 5-minute briefing for the capability family. It frames User as a protected learning ledger, Translate as a meaning bridge, and Guide as the orchestration route that helps a user move from concrete examples to abstractions and system thinking.

- `development/user-guide/packages/README.md`
  - Obligation refs: package boundary, package order
  - Context summary: splits the framework into three Invoke-authored packages: `user-ledger`, `translate`, and `guide`. It explicitly states that Invoke authored planning artifacts only and did not promote sigils, install commands, mutate registries, or create durable user profile state.

- `spells/guide-architecture/README.md`
  - Obligation refs: first spell slice, validation route
  - Context summary: defines `guide-architecture` as the first narrow Guide spell. It composes context selection, structure inspection, optional translation, explanation sequencing, active-understanding validation, and User-ledger update proposals.

- `development/user-guide/packages/user-ledger/`
  - Obligation refs: ledger rules
  - Context summary: contains the candidate User ledger package, including schema, visibility policy, receipt update rules, mastery fixtures, and work-pack tasks.

- `development/user-guide/packages/translate/`
  - Obligation refs: translation boundary
  - Context summary: contains the candidate Translate package, including schema, receipt schema, fixtures, Guide call contract, glossary, and work-pack tasks.

- `development/user-guide/packages/guide/`
  - Obligation refs: guide orchestrator package
  - Context summary: contains the candidate Guide package, including route schema, route fixture, translate integration, dispatch governance, spellcraft handoff, implementation layering, and work-pack tasks.

## Excluded Context

| Candidate | Reason Excluded |
| --- | --- |
| Broad unrelated repo modifications currently present in the worktree | Not obligation-relevant to this handoff; they predate or sit outside the requested User/Translate/Guide overview. |
| Full prior conversation transcript | Too broad; this handoff selects obligation-linked artifacts instead. |
| Browser/PDF export attempts | Superseded by the user's instruction to use the HTML directly for PDF export. |

## Target Boundary

- In scope for the new thread: continue Guide/User/Translate architecture, validate `guide-architecture`, execute next package work-pack tasks, or refresh artifacts if new evidence requires it.
- Out of scope for the new thread: unrelated Arcanum repo cleanup, Whisper artifacts, registry promotion without validation, silent User-ledger writes, and broad generic Guide generalization before the architecture-specific slice is validated.
- Prior decisions to preserve:
  - User is a protected learning/profile/glossary ledger with proposed updates, not an uncontrolled memory dump.
  - Translate is a separate sigil candidate before broad Guide orchestration.
  - Guide can dispatch supporting capabilities, but `guide-architecture` is the first narrow spell slice.
  - Mastery should require active evidence; passive "I understand" only supports clarified status.
  - Candidate glossary or registry promotion is not automatic.

## Gaps And Blockers

| Gap | Owner | Status | Next Action |
| --- | --- | --- | --- |
| User and Translate are candidate packages, not promoted sigils | `sigil-development` | open | Validate package fixtures and lifecycle evidence before promotion. |
| `guide-architecture` is candidate and needs live validation evidence | `spellcraft` | open | Run or complete the first validation fixture in `spells/guide-architecture/development/`. |
| Generic `guide` remains intentionally deferred | `spellcraft` / `invoke` | deferred | Generalize only after `guide-architecture` produces usable validation residue. |
| No durable user profile state should be written yet | `user-ledger` | open | Keep updates as receipt proposals until User-ledger rules are validated and accepted. |

## Next-Session Start Prompt

```text
Use Invoke handoff context for the Arcanum Guide / User / Translate family.

Start with:
- development/user-guide/session-handoffs/20260601T093612Z-guide-user-translate-session-handoff.md
- development/user-guide/guide-user-translate-overview.html
- development/user-guide/packages/README.md
- spells/guide-architecture/README.md

Goal: continue from existing artifacts, not from scratch. First determine the best next route:
1. spellcraft validate guide-architecture,
2. task-session execute the first ready package task,
3. invoke refresh if the artifacts have drifted.

Preserve the boundaries:
- User is a protected ledger with proposed updates only.
- Translate is the separate vocabulary/domain bridge.
- Guide orchestrates explanation and validation; guide-architecture is the first narrow spell slice.
- Do not promote registries or write durable user profile state without validation and approval.
```

## Provenance

- Source refs:
  - `development/user-guide/guide-user-translate-overview.html`
  - `development/user-guide/packages/README.md`
  - `development/user-guide/packages/user-ledger/`
  - `development/user-guide/packages/translate/`
  - `development/user-guide/packages/guide/`
  - `spells/guide-architecture/README.md`
  - git commit `706dae5`
- Context Builder mode: `standard`
- Evidence date: `2026-06-01`
- Output path: `development/user-guide/session-handoffs/20260601T093612Z-guide-user-translate-session-handoff.md`

## Gate Result

- Status: `pass`
- Reason: source prompt, handoff type, context selection, selected artifacts, gaps, and next route are all explicit. No target lifecycle mutation was performed.
