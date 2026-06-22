# Goal Spell Build — Craft View

> Human-readable view of [`.craft/ledger.yml`](.craft/ledger.yml). The ledger is
> the source of truth; this file is a linked summary only.

- **Ledger:** `spells/goal/.craft/ledger.yml`
- **Scope:** build the `goal` composed spell from a validated upstream design
  contract while keeping public artifacts generic.
- **Stage:** registered · **Gate:** pass

## Quick links

- **Next move:** Use the installer-owned generated runtime surface in the
  consuming repository; keep publication and parent gitlink movement separately
  approved.
- **Public-boundary guard:** [BLK-GOAL-SUBMODULE-001](#blocker-blk-goal-submodule-001)
- **Readiness gate:** [GATE-GOAL-PROMOTION-001](#blocker-gate-goal-promotion-001)
- **Active gaps:** [GAP-GOAL-ADO-MOVE-001](#gap-gap-goal-ado-move-001)
- **Open decisions:** none (5 closed)

## Context

### <a id="context-ctx-goal-root"></a>CTX-GOAL-ROOT — Goal Spell Build
Router-only, fail-closed control spine (read-frontier → classify-risk → select
owner+technique → dispatch → audit gate → stage delta → promote behind batched
approval token) + opt-in gap-discovery and proportionality modules. Delegates
reusable mechanisms to owning sigils; owns inline 6 new mechanisms; N5 reads a
**private** decision-mentality profile.

## Decisions (closed)

| ID | Question | Selected | Why |
| --- | --- | --- | --- |
| <a id="decision-dec-goal-packaging-001"></a>DEC-GOAL-PACKAGING-001 | How to package the goal-loop? | **Option A — one composed spell at spells/goal** | Single gated home, composition over duplication; tournament A=19 (Pareto-dominant). |
| <a id="decision-dec-goal-privacy-split-001"></a>DEC-GOAL-PRIVACY-SPLIT-001 | Private model vs public arcanum? | **public schema only, private filled profile** | arcanum is public; operator rule D12 forbids private data in it. |
| <a id="decision-dec-goal-profile-home-001"></a>DEC-GOAL-PROFILE-HOME-001 | Where does the filled profile live? | **private consuming-root profile instance** | Public arcanum ships only generic contracts and schemas; the consuming root supplies the filled schema instance at runtime. |
| <a id="decision-dec-goal-craft-scope-001"></a>DEC-GOAL-CRAFT-SCOPE-001 | Where does this ledger live? | **spells/goal/.craft** | The spell is the scope; .craft sits at the spell root (operator correction). |
| <a id="decision-dec-goal-promote-register-001"></a>DEC-GOAL-PROMOTE-REGISTER-001 | Promote and register the spell? | **promote, register, then install** | Spellcraft post-workpack validation, fixtures, dispatch validation, and Experiment Harness evidence pass. |

## Blockers & gates

- <a id="blocker-blk-goal-submodule-001"></a>**BLK-GOAL-SUBMODULE-001** (governance, active, refined) — `spells/goal` is in the **public** arcanum submodule; all authoring must exclude private operator data and keep only generic contracts, schemas, neutral defaults, opaque handles, and public-safe evidence. Commits follow submodule discipline (arcanum first + `make bump-check`) only when publication is separately requested. → [DEC-GOAL-PRIVACY-SPLIT-001](#decision-dec-goal-privacy-split-001)
- <a id="blocker-gate-goal-promotion-001"></a>**GATE-GOAL-PROMOTION-001** (readiness gate, closed) — Spellcraft post-workpack validation and `experiment-harness` evidence prove the spine: fail-closed not bypassable, gap-discovery terminates, approvals emit decision-gate records. Resolves audit B1/B2.
- **ENA-ADO-DESIGN-001** (enabler) — the validated Option A design + recomposition proof (16/16) + `SWU-GOAL-*` plan are the ready build contract.

## Gaps

- <a id="gap-gap-goal-ado-move-001"></a>**GAP-GOAL-ADO-MOVE-001** (flag, defer) — public-safe upstream design notes are represented by opaque handles; any future materialization into `spells/goal/development/` remains gated. Owner: operator-approval.

## Artifacts

| ID | Path | Status |
| --- | --- | --- |
| ART-GOAL-CRAFT-LEDGER | `spells/goal/.craft/ledger.yml` | active |
| ART-GOAL-CRAFT-VIEW | `spells/goal/CRAFT.md` | active |
| ART-GOAL-SCAFFOLD | `spells/goal/` | active |
| ART-ADO-DESIGN-RESULT | private upstream design handle | pass |
| ART-ADO-PLAN | private upstream plan handle | pass |
| ART-DECISION-PROFILE-PRIVATE | private consuming-root profile instance | active |
| ART-DECISION-PROFILE-SCHEMA | `spells/goal/decision-profile.schema` | active |
| ART-GOAL-ARTIFACT-SCHEMAS | `spells/goal/schemas/` | active |
| ART-GOAL-PROMOTION-RECEIPT | `spells/goal/development/spellcraft-runs/20260621T034046Z-promote-register-install/PROMOTE-REGISTER-INSTALL-RESULT.md` | pass |

## Build SWUs (from ART-ADO-PLAN)

SWU-GOAL-README · SWU-GOAL-COMPOSE · SWU-GOAL-RISK · SWU-GOAL-STAGE ·
SWU-GOAL-RO-BOUNDARY · SWU-GOAL-APPROVE · SWU-GOAL-GAP · SWU-GOAL-GUARD ·
SWU-GOAL-D3 · SWU-GOAL-AUDIT · SWU-GOAL-OBS
