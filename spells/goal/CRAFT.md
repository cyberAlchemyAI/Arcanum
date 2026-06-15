# Goal Spell Build — Craft View

> Human-readable view of [`.craft/ledger.yml`](.craft/ledger.yml). The ledger is
> the source of truth; this file is a linked summary only.

- **Ledger:** `spells/goal/.craft/ledger.yml`
- **Scope:** build the `goal` composed spell from the autonomous-dag-orchestration
  (ADO) Option A design.
- **Stage:** plan · **Gate:** flag

## Quick links

- **Next move:** Author `spells/goal/README.md` (SWU-GOAL-README) +
  `decision-profile.schema`, then execute the scrubbed ADO design move under approval.
- **Active blockers:** [BLK-GOAL-SUBMODULE-001](#blocker-blk-goal-submodule-001)
- **Readiness gate:** [GATE-GOAL-PROMOTION-001](#blocker-gate-goal-promotion-001)
- **Active gaps:** [GAP-GOAL-SCHEMA-001](#gap-gap-goal-schema-001),
  [GAP-GOAL-ADO-MOVE-001](#gap-gap-goal-ado-move-001)
- **Open decisions:** none (4 closed)

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
| <a id="decision-dec-goal-profile-home-001"></a>DEC-GOAL-PROFILE-HOME-001 | Where does the filled profile live? | **domainspec-core/.arcanum/profiles/** | Private, co-located with arcanum runtime; loadable; not in the submodule. |
| <a id="decision-dec-goal-craft-scope-001"></a>DEC-GOAL-CRAFT-SCOPE-001 | Where does this ledger live? | **spells/goal/.craft** | The spell is the scope; .craft sits at the spell root (operator correction). |

## Blockers & gates

- <a id="blocker-blk-goal-submodule-001"></a>**BLK-GOAL-SUBMODULE-001** (governance, active, refined) — `spells/goal` is in the **public** arcanum submodule; all authoring must exclude private operator data, and commits follow submodule discipline (arcanum first + `make bump-check`). Closes when authoring lands with no leak. → [DEC-GOAL-PRIVACY-SPLIT-001](#decision-dec-goal-privacy-split-001)
- <a id="blocker-gate-goal-promotion-001"></a>**GATE-GOAL-PROMOTION-001** (readiness gate, active) — spell stays **draft** until `experiment-harness` proves the spine: fail-closed not bypassable, gap-discovery terminates, approvals emit decision-gate records. Resolves audit B1/B2.
- **ENA-ADO-DESIGN-001** (enabler) — the validated Option A design + recomposition proof (16/16) + `SWU-GOAL-*` plan are the ready build contract.

## Gaps

- <a id="gap-gap-goal-schema-001"></a>**GAP-GOAL-SCHEMA-001** (flag, resolve) — `decision-profile.schema` (public shape + neutral default) not yet authored. Owner: SWU-GOAL-D3.
- <a id="gap-gap-goal-ado-move-001"></a>**GAP-GOAL-ADO-MOVE-001** (flag, defer) — scrubbed public-safe ADO design not yet moved into `spells/goal/development/`; move is gated (writes to public submodule). Owner: operator-approval.

## Artifacts

| ID | Path | Status |
| --- | --- | --- |
| ART-GOAL-CRAFT-LEDGER | `spells/goal/.craft/ledger.yml` | active |
| ART-GOAL-CRAFT-VIEW | `spells/goal/CRAFT.md` | active |
| ART-GOAL-SCAFFOLD | `spells/goal/` | planned |
| ART-ADO-DESIGN-RESULT | _(private)_ workspace-resonant ADO RESULT.md | pass |
| ART-ADO-PLAN | _(private)_ workspace-resonant s09-plan.md (SWU-GOAL-*) | pass |
| ART-DECISION-PROFILE-PRIVATE | _(private)_ `domainspec-core/.arcanum/profiles/decision-profile.yml` | active |
| ART-DECISION-PROFILE-SCHEMA | `spells/goal/decision-profile.schema` | planned |

## Build SWUs (from ART-ADO-PLAN)

SWU-GOAL-README · SWU-GOAL-COMPOSE · SWU-GOAL-RISK · SWU-GOAL-STAGE ·
SWU-GOAL-RO-BOUNDARY · SWU-GOAL-APPROVE · SWU-GOAL-GAP · SWU-GOAL-GUARD ·
SWU-GOAL-D3 · SWU-GOAL-AUDIT · SWU-GOAL-OBS
