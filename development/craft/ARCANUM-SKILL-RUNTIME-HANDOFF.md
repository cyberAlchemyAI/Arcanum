# Arcanum Skill Runtime Interface Handoff

## Identity

| Field | Value |
| --- | --- |
| Handoff ID | `arcanum-skill-runtime-interface` |
| Source session | Craft durable development session under `development/craft/` |
| Source artifact | [CRAFT-REFINE-RUNTIME-STRATEGY.md](CRAFT-REFINE-RUNTIME-STRATEGY.md) |
| Handoff type | new-lifecycle-thread |
| Target lifecycle | Arcanum runtime / command interface design |
| Recommended next route | `invoke define` |
| Status | pass |

## New Session Prompt

```text
Start a new Arcanum runtime interface development thread.

Goal: design an easy, runtime-agnostic way for Arcanum to call skills in different runtimes such as Codex, Claude, and GitHub Copilot while preserving an observation envelope around each skill run.

The interface must support:
- calling a selected skill in any supported runtime,
- attaching the Arcanum observation envelope before the skill starts,
- collecting skill run content, tool usage, artifacts, validation results, blockers, and final response,
- returning a normalized run envelope to Arcanum,
- supporting orchestrator/subagent refine workflows without recursive model-backed command deadlocks,
- preserving runtime-specific differences without hiding them.

Use development/craft/ARCANUM-SKILL-RUNTIME-HANDOFF.md as the source handoff.
Begin with invoke define. Do not mutate canonical runtime, command, skill, sigil, or plugin files until the define/design/plan artifacts are reviewed.
```

## Route Rationale

This should move to a new lifecycle thread because the problem is broader than Craft's recursive ledger.

The source Craft session discovered that:

- command-backed nested refine runs timed out,
- bounded direct skill work succeeded,
- refine should behave more like an orchestrator,
- individual stages should run as subagents, skill-direct calls, or runtime-specific workers,
- CI should be able to run skills directly without recursive `tools/arcanum --exec refine` behavior.

The target thread should design the runtime interface that makes this possible across runtimes.

## Context Builder Selection Summary

Selected context is intentionally narrow. It includes only evidence needed for the new runtime-interface design.

| Obligation | Selected Context | Coverage |
| --- | --- | --- |
| Prove the current runtime strategy is failing. | Two Craft refine run manifests show command-backed refine timeouts with no artifacts. | pass |
| State the proposed runtime shape. | [CRAFT-REFINE-RUNTIME-STRATEGY.md](CRAFT-REFINE-RUNTIME-STRATEGY.md) defines orchestrator plus stage workers/subagents. | pass |
| Preserve observation requirements. | User request requires observation envelope, skill run content, tool usage, artifacts, validation, blockers, and final response. | pass |
| Preserve runtime portability requirement. | User request names Codex, Claude, and GitHub Copilot. | pass |
| Avoid premature canonical mutation. | Craft session guardrails require no canonical runtime/command mutation without reviewed design. | pass |

## Selected Session Context

### Runtime Failure Evidence

From [refinement-runs/20260527T081822Z-CRAFT-REFINE-001/RUN-MANIFEST.md](refinement-runs/20260527T081822Z-CRAFT-REFINE-001/RUN-MANIFEST.md):

- `tools/arcanum --exec refine development/craft/WORK-PACK.md --task CRAFT-REFINE-001` timed out after 600 seconds.
- No output artifact was produced.
- The bounded target artifact was completed locally from the work-pack contract.

From [refinement-runs/20260527T085253Z-CRAFT-REFINE-002/RUN-MANIFEST.md](refinement-runs/20260527T085253Z-CRAFT-REFINE-002/RUN-MANIFEST.md):

- `tools/arcanum --exec refine development/craft/WORK-PACK.md --task CRAFT-REFINE-002` timed out after 300 seconds.
- No output artifact was produced.
- The bounded schema artifact was completed locally from the work-pack contract.

### Proposed Runtime Strategy

From [CRAFT-REFINE-RUNTIME-STRATEGY.md](CRAFT-REFINE-RUNTIME-STRATEGY.md):

```text
Refine is an orchestrator,
not a monolithic model-backed command.
```

Recommended topology:

```text
Refine Orchestrator
  -> Context Builder worker
  -> Invoke Define worker
  -> Interrogation worker
  -> Distill worker
  -> Invoke Design worker
  -> Interrogation worker
  -> Distill Repair worker
  -> Invoke Plan worker
  -> Final Synthesis worker
```

Each worker should return a normalized stage result:

```yaml
stage_id: <stage>
result: pass | flag | block | timeout
artifact_path: <path-or-null>
files_touched:
  - <path>
validation:
  - <check>
blockers:
  - <blocker-or-none>
handoff_note: <summary for orchestrator>
```

### New Runtime Interface Requirement

The new thread should generalize this beyond refine:

```text
Arcanum Skill Runtime Interface
  -> select runtime adapter
  -> attach observation envelope
  -> call skill
  -> capture tool usage and skill content
  -> collect artifacts, validation, blockers, and final response
  -> return normalized run envelope
```

## Target Boundary

In scope:

- define an Arcanum interface for calling skills across runtimes,
- support Codex, Claude, and GitHub Copilot as runtime targets or adapter families,
- attach observation envelopes before skill execution,
- capture skill run content, tool calls, artifacts, files touched, validation, blockers, and final answer,
- return normalized run envelopes to Arcanum,
- support orchestrator/subagent stage workflows,
- define CI skill-direct mode,
- distinguish runtime-specific capabilities and limitations.

Out of scope for first define/design:

- implementing every runtime adapter,
- mutating canonical `tools/arcanum`,
- changing installed skills/plugins,
- solving all telemetry storage details,
- building UI,
- priority scoring,
- Craft recursive ledger implementation.

## Candidate Concepts

| Concept | Candidate Meaning |
| --- | --- |
| Skill Runtime Interface | Arcanum-facing contract for invoking a skill in a selected runtime. |
| Runtime Adapter | Runtime-specific executor for Codex, Claude, GitHub Copilot, or CI skill-direct mode. |
| Observation Envelope | Standard pre/post wrapper containing run ID, capability identity, request summary, expected outputs, tool usage, artifacts, validation, blockers, and final result. |
| Skill Run Content | The actual content produced by the skill, including stage outputs and final message. |
| Tool Usage Capture | Structured record of tools called by the runtime during skill execution. |
| Normalized Run Envelope | Runtime-neutral result returned to Arcanum after a skill run. |
| Orchestrator | Parent process that assigns stage workers and collects run envelopes. |
| Stage Worker | Subagent, skill-direct call, or runtime worker executing one bounded stage. |

## Obligations For The Next Thread

The next thread should answer:

1. What is the smallest shared invocation contract for a skill run?
2. What fields must be present in the observation envelope before execution?
3. What fields must be returned after execution?
4. How does Arcanum capture tool usage when runtimes expose tools differently?
5. How does Arcanum distinguish skill content from orchestration metadata?
6. What adapter boundary lets Codex, Claude, GitHub Copilot, and CI share the same interface?
7. How should timeouts, partial artifacts, and blocked stages be represented?
8. How does this interface support subagents without requiring every runtime to implement the same subagent primitive?

## Excluded Context

Excluded from this handoff:

- Full Craft philosophical definition.
- Full recursive ledger schema details except where runtime-stage modeling matters.
- Priority scoring discussion.
- Canonical Craft promotion decisions.
- Broad Arcanum registry details.
- Full prior conversation transcript.

These are not needed to begin the runtime interface thread.

## Gaps And Blockers

| Gap | Severity | Suggested Handling |
| --- | --- | --- |
| Exact runtime adapter APIs differ across Codex, Claude, and GitHub Copilot. | high | Start with a normalized contract and adapter capability matrix. |
| Tool usage capture may not be equally exposed by all runtimes. | high | Define required, optional, and unavailable capture fields. |
| Observation envelope attachment point may differ by runtime. | medium | Define pre-run, during-run, and post-run envelope phases. |
| CI skill-direct execution may not have model tool traces. | medium | Allow CI to return deterministic script logs and artifact diffs as substitute evidence. |
| Current refine command runtime has timeout evidence but no internal trace. | medium | Treat as regression evidence, not as full diagnosis. |

## Next-Session Start Prompt

```text
/invoke define Arcanum Skill Runtime Interface

Use development/craft/ARCANUM-SKILL-RUNTIME-HANDOFF.md as the handoff source.

Design a runtime-agnostic interface that lets Arcanum call skills in Codex, Claude, GitHub Copilot, and CI skill-direct mode while attaching an observation envelope and collecting skill run content, tool usage, artifacts, files touched, validation, blockers, timeouts, and final response.

Do not implement yet. Produce define artifacts, glossary, open gaps, and the next route.
```

## Provenance

- Handoff produced by `invoke handoff`.
- Source session: Craft durable development session.
- Source evidence: `development/craft/` artifacts and two local refine timeout run manifests.
- No canonical Arcanum runtime files were mutated by this handoff.
