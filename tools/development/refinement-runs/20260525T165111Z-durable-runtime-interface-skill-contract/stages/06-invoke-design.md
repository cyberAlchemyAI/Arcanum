## Invoke Result

- Mode: design
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `spells/invoke/design.md`
- Outputs: `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/stages/06-invoke-design.md`
- Design views: data, control, runtime, evidence, migration, validation
- Glossary consistency: pass
- Implementation layering: seed emitted
- Work-pack: n/a
- Complexity: medium
- Per-layer planning: compact
- Implementation detail: inline
- Smallest working units: n/a
- Target artifact: Durable Arcanum Runtime Interface, design artifact, owner `framework/runtime`
- Template or recipe selection: six-view architecture design.
- Decisions: Two-folder model, immutable handoff, runtime-owned status, adapter-owned concrete execution.
- Unresolved gaps: none blocking.
- Next route: interrogation

### Design Artifact

#### Data View

Runtime root:

```text
.arcanum/runtime/runs/<runtime-run-id>/
  RUN.json
  HANDOFF.md
  STATUS.json
  RESULT.md
  events.jsonl
  artifacts/
  children/
```

Required `RUN.json` fields:

- `run_id`
- `parent_run_id`
- `orchestrator_id`
- `orchestrator_run_id`
- `adapter_id`
- `target_kind`
- `target_id`
- `loop_role`
- `loop_id`
- `parent_loop_id`
- `stage_number`
- `stage_name`
- `handoff_path`
- `result_path`

Required `STATUS.json` fields:

- `status`
- `adapter_status`
- `output_paths`
- `blocked_reason`
- `started_at`
- `completed_at`

#### Control View

```text
orchestrator creates RUNTIME-HANDOFF.md
orchestrator calls tools/arcanum-runtime-run
runtime runner validates handoff
runtime runner creates durable run folder
runtime translator builds adapter request
adapter executes or blocks
runtime runner records STATUS.json, events.jsonl, RESULT.md
orchestrator indexes runtime run evidence
```

#### Runtime View

Adapters:

- `dry-run`: creates artifacts without external execution.
- `codex-exec`: invokes `codex exec` with isolated per-run `CODEX_HOME`.

#### Evidence View

Refine evidence remains target-local. Runtime evidence remains under `.arcanum/runtime/runs/`. The link is the runtime run id and output path.

#### Migration View

`tools/arcanum --exec` should become a compatibility wrapper over `tools/arcanum-runtime-run`.

#### Validation View

Validation should prove JSON validity, artifact presence, isolated adapter state, parent/child topology, and absence of required `/goal` language in active refine runtime paths.

### Observability Closeout

- OBSERVATION: skipped
- LEDGER: n/a
- REFLECTION_TRIGGER: none
- RECOMMENDATION: continue-to-design-review
- DEDUPE_KEY: local-skill-contract-invoke-design-20260525T165111Z
