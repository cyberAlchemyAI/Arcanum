# SWU-CTX-GOAL-001 Context Pack

## Identity

- Task/SWU: `SWU-CTX-GOAL-001`
- Source work-pack: `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-WORK-PACK.md`
- Session evidence path: `arcana/task-session/development/session-evidence/SWU-CTX-GOAL-001/`
- Runtime handoff: local Task Session execution; Codex Goal delegation not used for this schema audit.
- Repository revision observed: `b17b888`
- Evidence date: `2026-05-23`

## Obligations

| Obligation | Status | Evidence |
| --- | --- | --- |
| O1: Define handoff pack sections for identity, obligations, selected sources, architecture guidance, related context, constraints, write scope, validation, gaps, authority precedence, fallback rule, strict coverage, Markdown output, JSON/index output, and provenance. | covered | `transmutations/context-builder/SKILL.md` `<handoff-pack-contract>` and `transmutations/context-builder/README.md` `Handoff Pack Schema`. |
| O2: Define required vs optional fields. | resolved | Required runnable fields are expressed by the strict coverage rule and blocker list; run/session id and content hash/git SHA are conditional when available. |
| O3: Define stale-source and secret/noise exclusion rules. | covered | `transmutations/context-builder/SKILL.md` strict coverage and anti-patterns cover stale, unsafe, irrelevant, and noisy material. |
| O4: Define session-evidence persistence as the default storage boundary. | covered | `transmutations/context-builder/SKILL.md` persistence rule and `transmutations/context-builder/README.md` output section. |
| O5: Explain how Codex Goal consumes the pack. | covered | `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-DESIGN.md` `Goal Handoff View`; `transmutations/context-builder/SKILL.md` `--handoff codex-goal`. |
| O6: Distinguish evidence from inference. | covered | `transmutations/context-builder/SKILL.md` quality bar requires evidence/inference separation; selected sources require selectors and excerpts. |
| O7: Include provenance for later consultation. | covered | `transmutations/context-builder/SKILL.md` and `README.md` require timestamp, source refs, and hash or git SHA when available. |
| O8: Require strict coverage for runtime handoff. | covered | `transmutations/context-builder/SKILL.md` strict coverage rule and `README.md` strict coverage paragraph. |

## Selected Sources

- `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-WORK-PACK.md`
  - Selectors: `SWU-CTX-GOAL-001`, scope, acceptance, handoff note.
  - Why included: source of the selected SWU contract.
- `arcana/task-session/development/TASK-SESSION-DEFINE.md`
  - Selectors: `Context First`, `Runtime Delegation`, `Invariants`.
  - Why included: governing invariants for pack-first runtime handoff.
- `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-DESIGN.md`
  - Selectors: `Artifact View`, `Goal Handoff View`, `Gate View`, `Contract Changes`.
  - Why included: design source for handoff pack contents and Codex Goal consumption.
- `transmutations/context-builder/SKILL.md`
  - Selectors: frontmatter flags, `<handoff-pack-contract>`, process steps 10-11, quality bar, anti-patterns.
  - Why included: canonical Context Builder skill contract updated by this SWU.
- `transmutations/context-builder/README.md`
  - Selectors: output section, `Handoff Pack Schema`, strict coverage paragraph.
  - Why included: user-facing Context Builder contract updated by this SWU.

## Architecture Guidance

- Context Builder owns context selection and handoff pack structure.
- Task Session owns task selection, gates, and evidence synchronization.
- Codex Goal consumes the pack; it must not become the authority for selecting broad context before handoff.

## Related Feature Context

This SWU is L0 schema work. Later SWUs apply the schema to Context Builder handoff mode, Task Session, Codex Goal Profile, the Codex Goal adapter, and Invoke-generated work packs.

## Constraints And Non-Goals

- Do not make generated context packs canonical planning documents.
- Do not add runtime execution behavior to Context Builder in this SWU.
- Do not make subagent execution mandatory.

## Write Scope

- `transmutations/context-builder/SKILL.md`
- `transmutations/context-builder/README.md`
- Optional context-builder template/example only if the local pattern needs it.

## Validation Surface

- Review schema coverage against SWU-001 scope and acceptance.
- Search for required contract terms in Context Builder canonical docs.
- Run `git diff --check` on the touched Context Builder files and session-evidence artifacts.

## Gaps And Blockers

- No blocker for SWU-001.
- No additional broad exploration needed; selected sources cover all obligations.

## Authority Precedence

1. User locked policy decisions in the current work-pack.
2. `TASK-SESSION-DEFINE.md` invariants.
3. `CONTEXT-PACK-GOAL-HANDOFF-DESIGN.md` contract changes.
4. Context Builder skill and README contract text.

## Fallback Exploration Rule

No fallback exploration is authorized for SWU-001 because all obligations are covered or explicitly resolved by selected evidence. Later SWUs may broaden only for named uncovered obligations.

## Provenance

- Repository revision observed: `b17b888`
- Source refs: listed in `Selected Sources`
- Evidence type: session evidence for one Task Session SWU execution

## Strict Coverage Status

`pass`

