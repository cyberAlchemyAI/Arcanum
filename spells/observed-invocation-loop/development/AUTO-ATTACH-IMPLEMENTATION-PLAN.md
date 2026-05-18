# Implementation Plan: OIL Automatic Runtime Attachment

## Objective

Implement automatic Observed Invocation Loop attachment for Arcanum runtime adapters so any installed sigil, spell, or skill command carries hook-first telemetry closeout by generation or refresh.

## Source References

| Ref ID | Source | Required | Notes |
| --- | --- | --- | --- |
| SD-001 | `spells/observed-invocation-loop/development/AUTO-ATTACH-DEFINE-SPEC.md` | yes | define phase |
| SD-002 | `spells/observed-invocation-loop/development/AUTO-ATTACH-DESIGN.md` | yes | design phase |
| SD-003 | `spells/observed-invocation-loop/README.md` | yes | parent spell contract |
| SD-004 | `arcana/sigil-runtime-installer/SKILL.md` | yes | runtime propagation owner |
| SD-005 | `arcana/sigil-runtime-installer/templates/github-copilot-skill.md` | yes | first adapter template |
| SD-006 | `.arcanum/runtimes/github-copilot/OBSERVED-INVOCATION.md` | yes | current OIL runtime contract |

## Delivery Boundary

Included:

- observed adapter marker/template,
- installer template update for new adapters,
- idempotent refresh plan for existing GitHub Copilot adapters,
- attachment manifest generation,
- Codex command adapter plan/generation path,
- validation fixtures proving all installed sigil adapters are attached or explicitly reported.

Excluded:

- native hooks outside Arcanum-managed command surfaces,
- automatic mutation in external repositories,
- editing unsupported runtime conventions without a confirmed bridge,
- reflection-driven code mutation.

## Layering

| Layer | Decision Boundary | Scope | Validation |
| --- | --- | --- | --- |
| L0 | Can we identify all installed adapter targets and attachment status? | manifest dry-run only | manifest lists skill/sigil/spell adapters and missing OIL status |
| L1 | Can new adapters be generated with OIL closeout by default? | installer templates | fixture generated adapter contains marker and OIL reference |
| L2 | Can existing adapters be refreshed safely? | idempotent marker refresh and validation | repeated refresh is stable; conflicts are reported |
| L3 | Can this work across command surfaces? | GitHub Copilot plus Codex command plan/generation | GitHub Copilot attached; Codex command plan or generated commands validated |

## Per-Layer Planning Slices

| Layer | Tasks | Dependencies | Validation Evidence | Blockers | Promotion Criteria |
| --- | --- | --- | --- | --- | --- |
| L0 | T-AUTO-001 | existing adapter tree | attachment manifest dry-run | adapter naming drift | manifest covers every installed `arcanum-sigil-*`, `arcanum-spell-*`, and orchestrator adapter |
| L1 | T-AUTO-002 | L0, installer templates | generated adapter fixture contains OIL marker | template ownership | new installs get OIL without manual edits |
| L2 | T-AUTO-003, T-AUTO-004 | L1 | refresh is idempotent and conflict-aware | local adapter edits | existing adapters can be brought to attached or conflict status |
| L3 | T-AUTO-005, T-AUTO-VERIFY | L2 | Codex command plan/generation validated and pilot still appends telemetry | Codex command convention uncertainty | command-surface rollout has pass/flag/block evidence |

## Task Decomposition

| Task ID | Goal | Done When |
| --- | --- | --- |
| T-AUTO-001 | Add attachment inventory and manifest generation. | dry-run reports every installed adapter with `attached`, `missing`, `planned`, `conflict`, or `exempt` |
| T-AUTO-002 | Update runtime installer templates to include OIL marker by default. | newly generated GitHub Copilot adapter includes observed closeout reference |
| T-AUTO-003 | Add idempotent refresh behavior for existing adapters. | marker block can be inserted or refreshed without rewriting unrelated content |
| T-AUTO-004 | Add attachment validation. | validation fails on missing OIL marker for installed sigils unless explicitly exempt |
| T-AUTO-005 | Add Codex command adapter support as runtime target. | `.arcanum/runtimes/codex/commands/` and `.codex/commands/` are generated or command adapter plans are emitted with OIL marker |
| T-AUTO-VERIFY | Verify end-to-end attachment and telemetry. | all checks pass and pilot still emits observed telemetry |

## Implementation Detail Specs

| Task ID | Inputs | Outputs | Implementation Notes | Edge Cases | Validation |
| --- | --- | --- | --- | --- | --- |
| T-AUTO-001 | runtime adapter directories | attachment manifest | Scan `.arcanum/runtimes/<runtime>/skills/` and command dirs; infer kind from command prefix; detect OIL marker or contract reference. | empty runtime, alias commands, custom command names | manifest fixture |
| T-AUTO-002 | installer templates | updated templates | Add marker block to `github-copilot-skill.md`; add equivalent command adapter template for Codex/Claude plans. | template only handles orchestrator text today | generated file fixture |
| T-AUTO-003 | existing adapters, marker block | refreshed adapters | Use stable `arcanum:observed-invocation` markers; insert before closeout/result step when absent and safe. | local edits inside marker, no process section | idempotent double-run fixture |
| T-AUTO-004 | manifest | validation report | Fail or flag missing OIL status; allow explicit exemption only with reason. | intentionally non-observed diagnostic commands | validator fixture |
| T-AUTO-005 | runtime target codex | command adapters or plans | Generate canonical runtime command plus discovery bridge, or produce plan when convention is uncertain. Include OIL marker. | `.codex/commands` missing, command naming conflict | Codex dry-run fixture |
| T-AUTO-VERIFY | completed tasks | evidence report | Run shell syntax checks, manifest checks, adapter pilot, and telemetry append proof. | stale generated adapters | test commands |

## Smallest Working Units

| SWU ID | Parent Task | Goal | Write Scope | Acceptance Evidence | Verification Command |
| --- | --- | --- | --- | --- | --- |
| SWU-OIL-AUTO-001 | T-AUTO-001 | Generate attachment manifest in dry-run mode. | observability or installer script plus development evidence | manifest lists all installed adapter targets | manifest command |
| SWU-OIL-AUTO-002 | T-AUTO-002 | Add observed marker to generated adapter templates. | `arcana/sigil-runtime-installer/templates/` | generated adapter contains marker and runtime OIL contract ref | template fixture |
| SWU-OIL-AUTO-003 | T-AUTO-003 | Refresh existing adapters idempotently. | refresh script or installer path | second refresh produces no content diff | double-run fixture |
| SWU-OIL-AUTO-004 | T-AUTO-004 | Validate attachment coverage. | validation script | missing marker fails; attached marker passes | validation fixture |
| SWU-OIL-AUTO-005 | T-AUTO-005 | Add Codex command adapter plan/generation. | codex runtime templates and bridges | command plan or generated commands include marker | Codex dry-run fixture |
| SWU-OIL-AUTO-006 | T-AUTO-VERIFY | Verify telemetry after attached adapter pilot. | evidence docs | pilot appends signal through OIL observer | `run-observed-adapter-pilot.sh` |

## Blocker Ledger

| Blocker ID | Blocker | Impact | Route |
| --- | --- | --- | --- |
| B-AUTO-001 | `.codex/commands` convention is planned but not locally populated. | Codex runtime may need plan-first rollout. | Generate command adapter plan first; create commands only when convention is confirmed. |
| B-AUTO-002 | Existing adapters may have local manual changes. | Bulk refresh can overwrite intent. | Marker-only idempotent refresh; conflict status for unsafe files. |
| B-AUTO-003 | Some aliases do not map cleanly to `sigil` or `spell`. | Kind inference can be wrong. | Use registry lookup or explicit manifest override. |
| B-AUTO-004 | Observability package may be absent in consumer repos. | Strict telemetry cannot pass. | Flag unless setup is required; route to `observability-setup`. |

## Validation Strategy

| Check ID | Check | Expected |
| --- | --- | --- |
| V-AUTO-001 | attachment manifest dry-run | every installed adapter appears once |
| V-AUTO-002 | new GitHub Copilot adapter fixture | marker and OIL contract reference present |
| V-AUTO-003 | refresh idempotence | second run has no diff |
| V-AUTO-004 | validation missing marker fixture | fails or flags as expected |
| V-AUTO-005 | Codex command dry-run | generated/plan files include OIL marker |
| V-AUTO-006 | adapter pilot telemetry | skill, sigil, and spell telemetry still append |

## Recommended Test Commands

```bash
bash -n framework/observability/scripts/observe-invocation.sh
bash -n framework/observability/scripts/reflect-invocation-signals.sh
framework/observability/scripts/run-observed-adapter-pilot.sh --observability-dir "$(mktemp -d)/observability"
```

Add the following once scripts exist:

```bash
framework/observability/scripts/attach-observed-invocation.sh --runtime github-copilot --dry-run
framework/observability/scripts/attach-observed-invocation.sh --runtime github-copilot --validate
framework/observability/scripts/attach-observed-invocation.sh --runtime codex --dry-run
```

## Planning Decision

Automatic attachment should be implemented in `observed-invocation-loop` and propagated through `sigil-runtime-installer`.

Codex commands should be added as one supported runtime target. They should be generated from the same adapter template/manifest logic as GitHub Copilot and Claude, not hand-authored separately.

## Invoke Result

- Mode: plan
- Spell: invoke
- Phase status: pass
- Complexity: medium
- Per-layer planning: L0, L1, L2, L3
- Smallest working units: complete
- Next route: spellcraft
