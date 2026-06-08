# SWU-RCNS-001 Active Surface Inventory

## Status

- SWU: `SWU-RCNS-001`
- Parent task: `TASK-RCNS-001`
- Date: 2026-06-08
- Result: `flag`
- Reason: Parent-lane inventory completed, but delegated subagent receipt did not complete before timeout. The active-surface evidence below is sufficient to unblock the next implementation SWUs, but it must be treated as parent-owned evidence rather than delegated corroboration.

## Scope

Inventory active command-interface dependencies for the commandless native-schema refresh across:

- `arcana/refine`
- `spells/invoke`
- `formulae/dispatch-spec`
- `tools/arcanum`
- `tools/bootstrap_arcanum.sh`

Generated refinement-run history under `development/refinement-runs` was excluded from the active blocker count.

## Classification Key

- `rewrite-native-receipt`: active contract, template, fixture, or generator still treats `.codex/commands`, slash commands, `tools/arcanum --resolve`, `tools/arcanum --exec`, or command-backed stages as success-gate primitives.
- `legacy-compatibility`: deprecated command surface remains intentionally present for explicit opt-in compatibility.
- `deterministic-tooling-outside-success-gate`: deterministic helper, adapter preparation, or local proof surface may remain, but must not be required as the native lifecycle success gate.
- `historical-preserve`: prior migration report, run output, or old evidence should remain unchanged and excluded from active blocker counts.
- `false-positive`: matched search terms are path names or generic contract wording rather than deprecated command-interface dependency.

## Active Rewrite Targets

| Area | Evidence | Classification | Owning SWU | Required change |
| --- | --- | --- | --- | --- |
| Refine loop contract | `arcana/refine/REFINEMENT-LOOP.md:34`, `:35`, `:38`, `:43` | `rewrite-native-receipt` | `SWU-RCNS-002` | Replace resolve/exec preconditions with capability handle resolution plus native skill/subagent receipt semantics. |
| Refine README | `arcana/refine/README.md:75`, `:81`, `:84` | `rewrite-native-receipt` | `SWU-RCNS-002` | Refresh user-facing contract so `tools/arcanum --exec` is not presented as a stage execution primitive. |
| Refine skill contract | `arcana/refine/SKILL.md:130`, `:133`, `:134`, `:137`, `:142`, `:308`, `:310` | `rewrite-native-receipt` | `SWU-RCNS-002` | Rewrite stage execution language around parent native runtime, schema-bound dispatch, receipts, and explicit legacy opt-in only. |
| Runtime handoff template | `arcana/refine/templates/runtime-handoff.md:27`, `:28` | `rewrite-native-receipt` | `SWU-RCNS-002` | Replace command execution handoff with native receipt handoff fields. |
| Run manifest template | `arcana/refine/templates/run-manifest.md:39` | `rewrite-native-receipt` | `SWU-RCNS-002` | Rename command-backed stage proof to native execution receipt proof. |
| Evidence index template | `arcana/refine/templates/evidence-index.json:53` | `rewrite-native-receipt` | `SWU-RCNS-002` | Replace `command_file` with capability/skill source and receipt fields. |
| Usage telemetry template | `arcana/refine/templates/usage-telemetry.md:52` | `rewrite-native-receipt` | `SWU-RCNS-002`, `SWU-RCNS-004` | Replace resolved command-file telemetry with native capability handle and receipt telemetry. |
| Refine dispatch template | `arcana/refine/templates/refine-dispatch.json:138`, `:284`, `:291` | `rewrite-native-receipt` | `SWU-RCNS-003` | Replace command-backed permission and stage conditions with schema-enforced native dispatch and receipt language. |
| Refine dispatch generator | `arcana/refine/scripts/generate-refine-dispatch.py:174`, `:185` | `rewrite-native-receipt` | `SWU-RCNS-003` | Generate commandless subagent permission prompts and native stage conditions. |
| Refine validation fixture runner | `arcana/refine/development/run-validation-fixtures.sh:77`, `:78`, `:120` | `rewrite-native-receipt` | `SWU-RCNS-004` | Remove `/refine` command resolution as promotion proof; validate native schema, receipts, and active docs instead. |
| Refine validation doc | `arcana/refine/development/VALIDATION.md:9`, `:10`, `:21`, `:26`-`:31`, `:41` | `rewrite-native-receipt` | `SWU-RCNS-004` | Refresh validation checklist away from `.codex/commands/refine.md` and resolve commands. |
| Refine runtime internals | `tools/arcanum:505`, `:640`, `:845`, `:1049`, `:1050`, `:1082`, `:1097`, `:1421`, `:1716`, `:2156` | `rewrite-native-receipt` | `SWU-RCNS-007` | Separate native Refine orchestration from deprecated command execution; keep only explicit compatibility adapters. |

## Compatibility And Deterministic Tooling

| Area | Evidence | Classification | Owning SWU | Required change |
| --- | --- | --- | --- | --- |
| Repository-local command helper usage text | `tools/arcanum:8`-`:30`, `:39`, `:144` | `legacy-compatibility` | `SWU-RCNS-007` | Keep only as explicit legacy compatibility help; do not let it define Refine success criteria. |
| Bootstrap command flags | `tools/bootstrap_arcanum.sh:36`, `:38`, `:39`, `:242`, `:243` | `legacy-compatibility` | `SWU-RCNS-007` | Preserve deprecated command-file generation/removal flags as opt-in compatibility. |
| Bootstrap deterministic references | `tools/bootstrap_arcanum.sh:29`, `:610`, `:998`, `:1450`, `:1454` | `deterministic-tooling-outside-success-gate` | `SWU-RCNS-007` | Reword generated package text so helper execution is adapter preparation or compatibility, not native lifecycle proof. |
| Bootstrap generated `.codex/commands` writers | `tools/bootstrap_arcanum.sh:1346`, `:1425`, `:1500`, `:1528`, `:1568`, `:1570`, `:1605`, `:1636`, `:1666`, `:1836` | `legacy-compatibility` | `SWU-RCNS-007` | Keep behind explicit legacy flags, refresh metadata and docs to mark deprecated status. |

## Invoke Findings

| Area | Evidence | Classification | Owning SWU | Required change |
| --- | --- | --- | --- | --- |
| Invoke README path references | `spells/invoke/README.md:22`, `:116`, `:118`, `:120`, `:121` | `false-positive` | `SWU-RCNS-005` | No command-interface mutation required for these lines. They are mode/path references. |
| Invoke mode contracts | `spells/invoke/define.md:88`, `spells/invoke/design.md:173`, `spells/invoke/plan.md:289` | `false-positive` | `SWU-RCNS-005` | No command-interface mutation required for these lines. |
| Invoke development/example fixtures | `spells/invoke/development/example-prompts/*` and `spells/invoke/development/VALIDATION.md` from broader scan | `rewrite-native-receipt` or `historical-preserve` by fixture age | `SWU-RCNS-005` | Refresh current validation/example prompts that still instruct command adapters; preserve old run outputs as historical evidence. |

## Dispatch-Spec Findings

| Area | Evidence | Classification | Owning SWU | Required change |
| --- | --- | --- | --- | --- |
| Dispatch schema and validator | No active hits in `formulae/dispatch-spec/dispatch.schema.yml` or `formulae/dispatch-spec/scripts/validate-dispatch.py` for the command-interface terms in this SWU scan. | `deterministic-tooling-outside-success-gate` | `SWU-RCNS-006` | Add guardrails anyway: forbid command-interface success gates in native dispatches, enforce capability handles, validate role alignment, and require delegated receipt ledger when `subagent_strategy` is recommended or required. |
| Dispatch-spec migration reports | `formulae/dispatch-spec/development/*COMMAND*`, `*CANONICALIZATION*`, and report files in broader scan | `historical-preserve` | none | Preserve as historical migration evidence; exclude from active blocker count. |

## Subagent Receipt

- Agent: `Noether`
- Agent id: `019ea567-4054-7672-9d02-b8ade40d4bd2`
- Role: `active-contract-auditor`
- Status: `shutdown`
- Previous status before shutdown: `running`
- Receipt status: `missing`
- Impact: The SWU result is flagged rather than fully passed. The next SWUs can proceed using parent-owned evidence, but final readiness audit must not count this subagent as corroborating evidence.

## Next Available Work

1. `SWU-RCNS-002`: Refresh Refine active contract to native receipts.
2. `SWU-RCNS-003`: Refresh Refine dispatch template and generator.
3. `SWU-RCNS-005`: Refresh Invoke authoring contracts, mostly development/example fixtures rather than canonical mode docs.

`SWU-RCNS-006` can begin after `SWU-RCNS-003`, because the dispatch validator should enforce the refreshed commandless dispatch shape rather than today-new prose only.

## Verification

Search command used:

```bash
rg -n "tools/arcanum --resolve|tools/arcanum --exec|\\.codex/commands|command-backed|command file|slash command|/refine|/invoke|command interface|command surface" arcana/refine/README.md arcana/refine/SKILL.md arcana/refine/REFINEMENT-LOOP.md arcana/refine/scripts/generate-refine-dispatch.py arcana/refine/templates arcana/refine/development/run-validation-fixtures.sh arcana/refine/development/VALIDATION.md spells/invoke/README.md spells/invoke/define.md spells/invoke/design.md spells/invoke/plan.md formulae/dispatch-spec tools/arcanum tools/bootstrap_arcanum.sh --glob '!**/development/refinement-runs/**'
```

Acceptance status:

- Active blocker classification exists: `pass`
- Unknown active command-interface hits remain: `none known from parent-lane scan`
- Delegated receipt available: `fail`
- Overall SWU status: `flag`
