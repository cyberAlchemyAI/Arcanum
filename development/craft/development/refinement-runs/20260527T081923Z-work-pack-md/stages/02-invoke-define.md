## Invoke Result

- Mode: define
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `spells/invoke/define.md`
- Outputs: [02-invoke-define.md](/home/vrondelli/projects/domainspec-core/arcanum/development/craft/development/refinement-runs/20260527T081923Z-work-pack-md/stages/02-invoke-define.md), [native-stage-evidence.jsonl](/home/vrondelli/projects/domainspec-core/arcanum/development/craft/development/refinement-runs/20260527T081923Z-work-pack-md/stages/native-stage-evidence.jsonl)
- Template selection: generic define-stage artifact with native Refine stage contract
- Decisions: defined `CRAFT-REFINE-001` as the L0 examples refinement; preserved the context-builder obligations; did not execute schema design, runtime integration, delegation, scoring, or canonical mutation
- Unresolved gaps: lane naming, schema storage shape, priority scoring, and blocker waiver policy remain deferred target gaps
- Next route: task-session

Validation passed: `tools/arcanum --resolve invoke`, JSON envelope parse, JSONL stage evidence parse, and output-contract checks on the new define artifact.

OBSERVATION: recorded
LEDGER: `.arcanum/observability/signals/sigil-invocations.jsonl` line 149
REFLECTION_TRIGGER: none
RECOMMENDATION: none
DEDUPE_KEY: `arcanum-command-invoke-20260527T083243Z:signal-observer:0.1.0`
