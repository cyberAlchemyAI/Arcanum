---
module: necronomicon
version: current
status: draft
updatedAt: 2026-05-23
docType: work-pack
---

# Necronomicon Work Pack

## Objective

Execute the substrate-first Necronomicon refactor in bounded slices, starting with canonical contract sync and L0 state contracts.

## Output Mode

Single-file work-pack for now. Split task files are deferred until implementation begins or task count grows.

## Active Layer Window

Current layer: L0 Substrate Proof.

Promotion target: L1 Setup And Manifest only after L0 scenario evidence passes.

## Task Board

| Task ID | Layer | Status | Summary | Validation |
| --- | --- | --- | --- | --- |
| NEO-L0-CONTRACT | L0 | complete | Sync canonical Necronomicon contract to substrate-first MVP. | Markdown review and stale-language search passed for `SWU-NEO-001`. |
| NEO-L0-SCHEMA | L0 | ready | Define `gaps.json`, `authority-classification.jsonl`, session evidence, and handoff packet shapes. | JSON examples parse. |
| NEO-L0-FIXTURES | L0 | ready | Add curated substrate-loop scenarios. | Inventory hit, missing inventory blocked state, ontology candidate, contradiction. |
| NEO-L0-ADAPTER | L0 | pending | Update adapter instructions for required inventory lookup and no-promotion closeout. | Command snapshot or generated adapter review. |
| NEO-L1-BOOTSTRAP | L1 | blocked | Add profile-aware bootstrap configuration after L0 proof. | Requires L0 promotion evidence. |

## Task Details

### NEO-L0-CONTRACT

Goal: Make the canonical Necronomicon contract agree with the corrected development pack.

Write scope:

- `spells/necronomicon/README.md`
- generated command snapshots only if explicitly approved after canonical edit

Done criteria:

- README says MVP is Inventory And Ontology Substrate Loop.
- Routing/setup are support layers.
- No-promotion guardrails are explicit.

Validation:

- Search for stale "MVP is Session Memory Router" wording.
- Manual contract review against `DEFINE.md`.

### NEO-L0-SCHEMA

Goal: Make L0 state shapes implementable.

Write scope:

- `spells/necronomicon/development/IMPLEMENTATION-PLAN.md`
- optional curated schema fixture files under `spells/necronomicon/development/fixtures/`

Done criteria:

- `gaps.json` kinds are defined.
- `authority-classification.jsonl` fields are defined.
- `evidence.md` sections are defined.
- handoff packet fields include owner and no-promotion note.

Validation:

- JSON snippets parse when extracted into temporary files.
- Schema examples cover at least one candidate and one gap.

### NEO-L0-FIXTURES

Goal: Prove the substrate loop with examples before runtime implementation.

Write scope:

- `spells/necronomicon/development/fixtures/`

Done criteria:

- Fixture 1: inventory hit.
- Fixture 2: missing inventory blocked state with setup/install guidance.
- Fixture 3: ontology candidate.
- Fixture 4: contradiction gap.

Validation:

- Fixtures are readable and cite expected output classes.

### NEO-L0-ADAPTER

Goal: Teach runtime adapters how to perform the L0 loop.

Write scope:

- `tools/bootstrap_arcanum.sh`
- `.codex/commands/arcanum-necronomicon.md` only via regeneration or explicit snapshot update

Done criteria:

- Adapter says inventory is required before active Necronomicon substrate work.
- Adapter says missing inventory creates a blocked state and routes to setup/install guidance, not local-search fallback.
- Adapter says candidate promotion is forbidden.

Validation:

- `bash -n tools/bootstrap_arcanum.sh`.
- Generated adapter text inspection.

### NEO-L1-BOOTSTRAP

Goal: Generate setup state after L0 passes.

Blocked by:

- L0 substrate proof validation.

Write scope:

- `tools/bootstrap_arcanum.sh`
- generated `.arcanum/necronomicon/` temp install outputs

Done criteria:

- profile-aware manifest,
- setup decisions,
- initial gap ledger,
- route and maintenance folders,
- privacy policy.

Validation:

- temp installs and JSON validation.

## Smallest Working Units

| SWU ID | Parent Task | Goal | Dependencies | Write Scope | Acceptance Evidence | Verification |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-NEO-001 | NEO-L0-CONTRACT | Rewrite canonical README around substrate-first MVP. | Current development pack. | `spells/necronomicon/README.md` | README matches define/design center. | `rg -n "Session Memory Router|Inventory And Ontology Substrate Loop" spells/necronomicon/README.md` |
| SWU-NEO-002 | NEO-L0-SCHEMA | Add concrete schema examples for L0 state. | `IMPLEMENTATION-PLAN.md`. | development docs or fixtures | JSON examples parse. | `jq empty <example>` |
| SWU-NEO-003 | NEO-L0-FIXTURES | Add four substrate scenarios. | schema examples | fixtures folder | scenarios cover inventory hit, missing-inventory blocked state, ontology, contradiction. | manual fixture review |
| SWU-NEO-004 | NEO-L0-ADAPTER | Update bootstrap-generated adapter instructions. | canonical README approved | `tools/bootstrap_arcanum.sh` | adapter includes required inventory, blocked-state guidance, no-promotion. | `bash -n tools/bootstrap_arcanum.sh` |

## Gate Status

| Gate | Status |
| --- | --- |
| Define/design/plan artifacts re-authored | pass |
| Canonical README synced | pass |
| L0 schema fixtures | pending |
| L0 adapter proof | pending |
| L1 bootstrap work | blocked until L0 passes |

## Recommended Execution

Start with `SWU-NEO-001`, then `SWU-NEO-002`. Do not start bootstrap generation until the L0 state contract and fixtures are accepted.

## Change History

| Date | Change |
| --- | --- |
| 2026-05-24 | Completed `SWU-NEO-001`: canonical README now centers the Inventory And Ontology Substrate Loop, support layers, and no-promotion guardrails. |
| 2026-05-23 | Created substrate-first work-pack. |
