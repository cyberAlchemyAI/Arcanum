# Context Pack Goal Handoff Work Pack

## Invocation

- Spell: `invoke`
- Mode: `plan`
- Target artifact: `task-session`
- Target type: Arcana sigil implementation plan
- Output mode: single-file work-pack with companion layering

## Source Artifacts

- `TASK-SESSION-DEFINE.md`
- `TASK-SESSION-GLOSSARY.md`
- `TASK-SESSION-ARCHITECTURE-DESIGN.md`
- `TASK-SESSION-GLOSSARY-CONSISTENCY.md`
- `TASK-SESSION-DESIGN-TRANSPORT.md`
- `CONTEXT-PACK-GOAL-HANDOFF-OPTIMIZATION.md`
- `CONTEXT-PACK-GOAL-HANDOFF-DESIGN.md`

## Artifact Reuse Decision

This file is the canonical work-pack for the current Task Session improvement slice. A new parallel work-pack was not created because this artifact already contains the correct implementation SWUs for the pack-first Codex Goal handoff.

The plan update normalizes this existing work-pack against the define and design layers instead of duplicating it.

## Goal

Implement a pack-first Task Session to Codex Goal workflow where Context Builder selects and persists task context before runtime delegation.

Locked policy decisions:

- Handoff packs persist as session evidence.
- Codex Goal handoff uses strict coverage: every obligation is covered or explicitly resolved.
- Context Builder emits Markdown plus JSON/index for runtime handoff.

## Non-Goals

- Do not make subagent execution mandatory.
- Do not make generated context packs canonical planning documents.
- Do not require Invoke Plan to pre-generate context packs.
- Do not remove Task Session's existing gates or completion evidence.

## Complexity

Complexity: `medium`

Reasons:

- changes cross three capability boundaries: Task Session, Context Builder, and Codex Goal Profile/adapter,
- runtime delegation behavior and persisted execution evidence are affected,
- SWU handoffs must be explicit enough for task-session or goal execution,
- validation needs at least one dry runtime path.

## Layer Mapping

| Layer | Question | SWUs | Promotion Evidence |
| --- | --- | --- | --- |
| L0 | Can the handoff pack schema express the selected context contract? | SWU-CTX-GOAL-001 | Schema documents required sections, provenance, and quality gates. |
| L1 | Can Context Builder emit a task-ready handoff pack? | SWU-CTX-GOAL-002 | A task/SWU can produce Markdown plus JSON/index session-evidence handoff output. |
| L2 | Can Task Session and Codex Goal consume the pack-first contract safely? | SWU-CTX-GOAL-003, SWU-CTX-GOAL-004, SWU-CTX-GOAL-005 | Goal handoff blocks incomplete or non-strict-coverage packs and reports fallback exploration. |
| L3 | Can future invoke-generated plans remain context-builder-ready without stale prebuilt packs? | SWU-CTX-GOAL-006 | Invoke plan guidance produces SWUs with source anchors and validation context. |

## SWU Manifest

| SWU | Parent Slice | Layer | Dependencies | Execution Owner | Verification |
| --- | --- | --- | --- | --- | --- |
| SWU-CTX-GOAL-001 | Handoff Pack Schema | L0 | none | local-fallback | Review schema sections against define/design invariants. |
| SWU-CTX-GOAL-002 | Context Builder Handoff Mode | L1 | SWU-CTX-GOAL-001 | local-fallback | Dry-run Context Builder handoff output for one task/SWU. |
| SWU-CTX-GOAL-003 | Task Session Context Phase | L2 | SWU-CTX-GOAL-001, SWU-CTX-GOAL-002 | local-fallback | Dry-run task session blocks or proceeds based on pack quality. |
| SWU-CTX-GOAL-004 | Codex Goal Profile Input | L2 | SWU-CTX-GOAL-001 | local-fallback | Generated profile includes pack-first rule and fallback audit. |
| SWU-CTX-GOAL-005 | Codex Goal Adapter Enforcement | L2 | SWU-CTX-GOAL-003, SWU-CTX-GOAL-004 | local-fallback | Adapter rejects missing or non-strict-coverage packs and preserves pack evidence. |
| SWU-CTX-GOAL-006 | Invoke Work-Pack Readiness | L3 | SWU-CTX-GOAL-001 | local-fallback | Plan guidance requires source anchors and avoids prebuilt context packs. |

## Work Units

### SWU-CTX-GOAL-001: Define Handoff Pack Schema

**Outcome:** Context Builder has a documented task-ready handoff schema.

**Layer:** L0

**Write Scope:**

- `transmutations/context-builder/SKILL.md`
- `transmutations/context-builder/README.md`
- optional context-builder template or example file if the local pattern exists.

**Scope:**

- Add pack sections for identity, obligations, selected sources, architecture guidance, related feature context, constraints, write scope, validation, gaps, authority precedence, fallback rule, strict coverage, Markdown output, JSON/index output, and provenance.
- Define required vs optional fields.
- Define stale-source and secret/noise exclusion rules.
- Define session-evidence persistence as the default storage boundary.

**Acceptance:**

- Schema explains how Codex Goal should consume the pack.
- Schema distinguishes evidence from inference.
- Schema includes enough provenance for later consultation.
- Schema requires strict coverage for runtime handoff.

**Handoff Note:** Start from `TASK-SESSION-DEFINE.md` invariants and `CONTEXT-PACK-GOAL-HANDOFF-DESIGN.md` pack contents. Do not add runtime execution behavior to Context Builder.

**Execution Evidence:**

- Status: `complete`
- Context pack: `arcana/task-session/development/session-evidence/SWU-CTX-GOAL-001/context-pack.md`
- Context index: `arcana/task-session/development/session-evidence/SWU-CTX-GOAL-001/context-pack.json`
- Strict coverage: `pass`
- Validation: schema review against define/design invariants, targeted contract-term search, and `git diff --check`.
- Fallback search: `none`

### SWU-CTX-GOAL-002: Add Context Builder Handoff Mode

**Outcome:** Context Builder can emit and optionally persist a Codex Goal handoff pack.

**Layer:** L1

**Dependencies:** SWU-CTX-GOAL-001

**Write Scope:**

- `transmutations/context-builder/SKILL.md`
- `transmutations/context-builder/README.md`
- optional context-builder templates/examples.

**Scope:**

- Add a handoff mode such as `--handoff codex-goal`.
- Add a persistence option such as `--persist <session-evidence-path>` or runtime equivalent.
- Emit both human-readable Markdown and structured JSON/index forms.

**Acceptance:**

- A task/SWU can produce a session-evidence handoff pack.
- Pack includes source selectors and coverage summary.
- Pack records unresolved gaps rather than hiding them.

**Handoff Note:** Generated packs are execution evidence. They must not become canonical planning docs or replace source design artifacts.

**Execution Evidence:**

- Status: `complete`
- Context pack: `arcana/task-session/development/session-evidence/SWU-CTX-GOAL-002/context-pack.md`
- Context index: `arcana/task-session/development/session-evidence/SWU-CTX-GOAL-002/context-pack.json`
- Output templates: `transmutations/context-builder/templates/codex-goal-handoff-pack.md`, `transmutations/context-builder/templates/codex-goal-handoff-index.json`
- Strict coverage: `pass`
- Validation: targeted mode/output search, JSON template parse, SWU evidence JSON parse, and `git diff --check`.
- Fallback search: `none`

### SWU-CTX-GOAL-003: Update Task Session Context Phase

**Outcome:** Task Session builds the handoff pack before gates and delegation.

**Layer:** L2

**Dependencies:** SWU-CTX-GOAL-001, SWU-CTX-GOAL-002

**Write Scope:**

- `arcana/task-session/SKILL.md`
- `arcana/task-session/README.md`
- optional task-session examples or command adapters if they mirror the skill contract.

**Scope:**

- Run Context Builder as a subagent/delegated worker when available.
- Fall back to inline/local execution with the same output contract.
- Block or ask for decision when coverage, contradiction, or staleness gates fail.

**Acceptance:**

- `--via goal` cannot proceed without Markdown plus JSON/index handoff artifacts and strict coverage.
- Task-session report includes pack artifacts, strict coverage, gaps, and fallback search policy.

**Handoff Note:** Subagent use is preferred when available, but the contract is the pack. Keep inline/local fallback valid.

**Execution Evidence:**

- Status: `complete`
- Context pack: `arcana/task-session/development/session-evidence/SWU-CTX-GOAL-003/context-pack.md`
- Context index: `arcana/task-session/development/session-evidence/SWU-CTX-GOAL-003/context-pack.json`
- Command mirrors refreshed: `.codex/commands/task-session.md`, `.codex/commands/arcanum-sigil-task-session.md`
- Strict coverage: `pass`
- Validation: Task Session context/gate/report search, stale command mirror search, SWU evidence JSON parse, and `git diff --check`.
- Fallback search: `none`

### SWU-CTX-GOAL-004: Update Codex Goal Profile

**Outcome:** Codex Goal Profile includes context-pack inputs and pack-first instructions.

**Layer:** L2

**Dependencies:** SWU-CTX-GOAL-001

**Write Scope:**

- `transmutations/codex-goal-profile/SKILL.md`
- `transmutations/codex-goal-profile/README.md`
- `transmutations/codex-goal-profile/templates/codex-goal-profile.md`
- relevant examples under `transmutations/codex-goal-profile/examples/`.

**Scope:**

- Add handoff pack Markdown path and JSON/index path as required inputs for task-session goal delegation.
- Add fallback exploration rule.
- Add expected final reporting for context gaps and extra sources used.

**Acceptance:**

- Generated goal prompt instructs Codex to use pack first.
- Broad exploration is allowed only for named uncovered obligations or gaps.
- Goal completion reports any extra sources used.
- Missing strict coverage blocks profile generation.

**Handoff Note:** Codex Goal Profile owns prompt shape, not Task Session orchestration or Context Builder selection.

**Execution Evidence:**

- Status: `complete`
- Context pack: `arcana/task-session/development/session-evidence/SWU-CTX-GOAL-004/context-pack.md`
- Context index: `arcana/task-session/development/session-evidence/SWU-CTX-GOAL-004/context-pack.json`
- Strict coverage: `pass`
- Validation: profile/input/fallback/extra-source reporting search, blocked example review, SWU evidence JSON parse, and `git diff --check`.
- Fallback search: `none`

### SWU-CTX-GOAL-005: Update Codex Goal Adapter

**Outcome:** Runtime adapter passes context packs into native Codex Goal and records result evidence.

**Layer:** L2

**Dependencies:** SWU-CTX-GOAL-003, SWU-CTX-GOAL-004

**Write Scope:**

- `arcana/task-session/runtime-adapters/codex-goal.md`
- `arcana/task-session/runtime-adapters/README.md`
- `.codex/commands/task-session.md` only if the installed command adapter must mirror changed behavior.

**Scope:**

- Validate pack quality before `create_goal`.
- Pass pack Markdown path and JSON/index into the goal objective.
- Preserve pack reference in completion evidence.

**Acceptance:**

- Missing, stale, contradictory, unsafe, missing-validation, missing-write-scope, or non-strict-coverage packs block goal delegation.
- Successful goal delegation records pack identity and any gap-driven extra exploration.

**Handoff Note:** Adapter must not override Task Session blockers or broaden write scope.

**Execution Evidence:**

- Status: `complete`
- Context pack: `arcana/task-session/development/session-evidence/SWU-CTX-GOAL-005/context-pack.md`
- Context index: `arcana/task-session/development/session-evidence/SWU-CTX-GOAL-005/context-pack.json`
- Strict coverage: `pass`
- Validation: adapter blocker/evidence search, gap-driven extra-source reporting review, SWU evidence JSON parse, and `git diff --check`.
- Fallback search: `none`

### SWU-CTX-GOAL-006: Make Invoke Work Packs Context-Builder-Ready

**Outcome:** Invoke design/plan outputs make later context selection easy without pre-generating packs.

**Layer:** L3

**Dependencies:** SWU-CTX-GOAL-001

**Write Scope:**

- `spells/invoke/plan.md`
- `spells/invoke/design.md` only if design handoff language needs a small companion update.
- invoke templates under `spells/invoke/templates/` if they define SWU/source-anchor fields.

**Scope:**

- Ensure SWUs include source anchors, acceptance evidence, validation surface, write boundaries, and related-context hints.
- Add guidance that context packs are generated at execution time.

**Acceptance:**

- A generated work pack gives Context Builder enough structure to select context.
- The work pack does not depend on a stale generated context pack.

**Handoff Note:** Invoke should make future work-packs context-builder-ready. It should not generate task context packs during planning.

**Execution Evidence:**

- Status: `complete`
- Context pack: `arcana/task-session/development/session-evidence/SWU-CTX-GOAL-006/context-pack.md`
- Context index: `arcana/task-session/development/session-evidence/SWU-CTX-GOAL-006/context-pack.json`
- Strict coverage: `pass`
- Validation: Invoke source-anchor/acceptance-evidence/validation-surface/write-scope/related-context search, SWU evidence JSON parse, and `git diff --check`.
- Fallback search: `none`

## Validation Strategy

Validation is review-first until the individual contract changes are implemented.

Required checks by slice:

- SWU-CTX-GOAL-001: review schema against `TASK-SESSION-DEFINE.md` invariants and glossary terms.
- SWU-CTX-GOAL-002: dry-run a handoff pack for one benchmark SWU or equivalent local task and confirm Markdown plus JSON/index outputs.
- SWU-CTX-GOAL-003: dry-run `/task-session ... --via goal` and confirm context building happens before goal creation.
- SWU-CTX-GOAL-004: generate or review a Codex Goal profile and confirm pack-first instructions are present.
- SWU-CTX-GOAL-005: confirm adapter blocks missing/stale/non-strict-coverage packs and preserves pack reference in result evidence.
- SWU-CTX-GOAL-006: inspect generated invoke work-pack fields for source anchors, validation surfaces, and handoff context.

## Validation

- Run a dry task session with `--via goal` against a benchmark SWU.
- Confirm a context pack is produced before goal creation.
- Confirm the goal prompt references the pack.
- Confirm broad exploration is reported only when tied to a named gap.
- Confirm task-session evidence links Markdown pack, JSON/index, strict coverage, validation, and final sync.

## Risks

- Context packs can become too large. Mitigation: excerpt limits and selector-first summaries.
- Packs can become stale. Mitigation: source refs, timestamps, and optional content hashes.
- Subagent availability can vary. Mitigation: subagent is preferred, inline/local is valid fallback.
- Generated packs can be mistaken for canonical docs. Mitigation: store under session/runtime evidence and label as execution context.

## Execution Handoff

Next route: `task-session`

Recommended first executable SWU: `SWU-CTX-GOAL-001`

Suggested command:

```text
/task-session to arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-WORK-PACK.md --swu SWU-CTX-GOAL-001 --runtime codex --via goal
```
