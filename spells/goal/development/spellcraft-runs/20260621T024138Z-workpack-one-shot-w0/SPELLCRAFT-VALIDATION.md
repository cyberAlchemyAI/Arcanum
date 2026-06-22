# Spellcraft Validation: Goal Work-Pack One-Shot W0

## Spellcraft Result

- Mode: validate
- Spell: goal
- Canonical ID: goal
- Alias used: none
- Scope: library
- Spell file: `arcanum/spells/goal/README.md`
- Sigils referenced: craft, dispatch-spec, observed-invocation-loop,
  decision-gate, task-session, observability-setup, signal-observer,
  robot-talks, refine, distill, experiment-harness
- Phases: 10
- Validation: block
- Observability: configured
- Next action: resolve public-boundary staged repair before W1 runtime SWUs.

## Source Packet Checked

| Source | Result |
| --- | --- |
| `arcanum/spells/goal/README.md` | pass |
| `arcanum/spells/goal/decision-profile.schema` | pass |
| `arcanum/spells/goal/development/invoke-runs/20260620T202601Z-goal-spec-definitions/SPEC.md` | pass |
| `arcanum/spells/goal/development/invoke-runs/20260620T202601Z-goal-spec-definitions/DEFINITIONS.md` | pass |
| `arcanum/spells/goal/development/invoke-runs/20260620T205253Z-goal-architecture-rules-schemas-contracts/ARCHITECTURE.md` | pass |
| `arcanum/spells/goal/development/invoke-runs/20260620T205253Z-goal-architecture-rules-schemas-contracts/RULES.md` | pass |
| `arcanum/spells/goal/development/invoke-runs/20260620T205253Z-goal-architecture-rules-schemas-contracts/CONTRACTS.md` | pass |
| `arcanum/spells/goal/development/invoke-runs/20260620T205253Z-goal-architecture-rules-schemas-contracts/SCHEMAS.md` | pass |
| `arcanum/spells/goal/development/invoke-runs/20260620T212656Z-goal-plan/WORK-PACK.md` | pass |
| `arcanum/spells/goal/development/invoke-runs/20260620T212656Z-goal-plan/PLAN-DISPATCH.json` | pass |
| `arcanum/spells/goal/CRAFT.md` | block |
| `arcanum/spells/goal/.craft/ledger.yml` | block |

## Checks Performed

| Check | Result | Evidence |
| --- | --- | --- |
| Public schema JSON parse | pass | `python3 -m json.tool arcanum/spells/goal/decision-profile.schema` |
| Design schema JSON parse | pass | `python3 -m json.tool schemas/*.schema.json` |
| Plan dispatch validation | pass | `validate-dispatch.py PLAN-DISPATCH.json --json` returned pass with no blocks or flags. |
| Markdown links | pass | `tools/check_markdown_links.sh` over `arcanum/spells/goal/**/*.md`. |
| Router-only contract | pass | README, ARCHITECTURE, CONTRACTS all keep delegated owner boundaries. |
| Generated-surface boundary | pass | README, RULES, CONTRACTS, WORK-PACK keep generated surfaces installer-owned. |
| Runtime SWU gating | pass | WORK-PACK and EXECUTION-PACK gate W1 behind W0. |
| Public/private boundary | block | CRAFT view and hidden Craft ledger include private provenance/profile path literals. |

## Blocking Finding

`arcanum/spells/goal/CRAFT.md` and `arcanum/spells/goal/.craft/ledger.yml`
still contain private workspace/profile provenance literals. Because
`arcanum` is public and the goal spell package lives under that public
submodule, W1 runtime SWUs must not start until the public package no longer
ships those details or the user explicitly approves a scoped repair.

## Runtime Gate

- W0 status: block
- W1 status: blocked
- W2 status: blocked
- W3 status: blocked

Runtime work may continue only after the staged public-boundary repair is
approved and applied, or after the user chooses a different explicit option in
the decision gate.

## Extra Sources Used

| Source | Justifying Gap | Effect |
| --- | --- | --- |
| `arcanum/spells/goal/CRAFT.md` | `G-GOAL-CRAFT-SYNC` | Revealed public-view private provenance literals. |
| `arcanum/spells/goal/.craft/ledger.yml` | `G-GOAL-CRAFT-SYNC` | Revealed source-ledger private provenance literals and stale authored-artifact state. |

## Receipt

See `SWU-GOAL-001-RECEIPT.yml`.
