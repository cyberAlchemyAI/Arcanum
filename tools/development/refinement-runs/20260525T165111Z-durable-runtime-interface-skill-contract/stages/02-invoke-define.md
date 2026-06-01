## Invoke Result

- Mode: define
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `spells/invoke/define.md`
- Outputs: `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/stages/02-invoke-define.md`
- Design views: n/a
- Glossary consistency: pass
- Implementation layering: seed emitted
- Work-pack: n/a
- Complexity: medium
- Per-layer planning: compact
- Implementation detail: inline
- Smallest working units: n/a
- Target artifact: Durable Arcanum Runtime Interface, architecture/design handoff, owner `framework/runtime`
- Template or recipe selection: define-mode concept baseline using local evidence from Context Builder.
- Decisions: Codex Goal removed from core runtime; Codex retained only as adapter.
- Unresolved gaps: no blocker gaps; implementation details deferred to Invoke Plan.
- Next route: invoke design

### Define Artifact

#### Name

Durable Arcanum Runtime Interface

#### Purpose

Provide a generic file-backed execution substrate that lets Arcanum orchestrators hand off work to runtime adapters without depending on Codex Goal, native `/goal`, or shared Codex runtime state.

#### Core Formula

```text
orchestrator -> async task handoff -> runtime translator -> runtime executor -> adapter
```

#### Glossary

- **Orchestrator**: Arcanum capability that owns workflow meaning and final synthesis. Examples: `refine`, `task-session`.
- **Async task handoff**: immutable file-backed request describing objective, inputs, scope, expected outputs, validation, adapter preference, and blocked conditions.
- **Runtime translator**: adapter-specific transformation from generic handoff to executable request.
- **Runtime executor**: shared tool that creates durable run state, invokes adapters, records status/events, and captures results.
- **Adapter**: concrete runtime implementation such as `dry-run` or `codex-exec`.
- **Runtime run**: durable execution folder under `.arcanum/runtime/runs/<runtime-run-id>/`.
- **Loop topology**: metadata that relates parent runs, child runs, stages, candidates, nested loops, repairs, and continuations.

#### Initial Boundaries

The runtime interface owns execution mechanics. It does not own refine's stage semantics or task-session's task/SWU safety decisions.

### Observability Closeout

- OBSERVATION: skipped
- LEDGER: n/a
- REFLECTION_TRIGGER: none
- RECOMMENDATION: continue-to-interrogation
- DEDUPE_KEY: local-skill-contract-invoke-define-20260525T165111Z
