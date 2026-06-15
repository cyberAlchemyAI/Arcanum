---
tags: [arcanum, dispatch-composition, observability, subagents, architecture, ontology, attack-plan]
node_type: discovery
is_session: true
layer: architecture, ontology
nature: explanatory, technical
status: active
created: 2026-06-13
timestamp: 2026-06-13T16:50:20-03:00
expires: 2026-08-12
conversation_id: dispatch-composition-observability
decisions_made: true
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "Converts the consolidated DISPATCH-COMPOSITION-MODEL into a concrete Phase-1/Phase-2 attack plan with binding architectural decisions (telemetry-plane writer, governance discipline, join key), the load-bearing planning artifact for Arcanum's observability and dispatch-spec evolution."
---

# Dispatch-Composition Attack Plan + Observability Adaptation

## Summary

Turned the consolidated DISPATCH-COMPOSITION-MODEL (TO-VLAD) into an actionable, staged attack plan for Arcanum — Phase 1 observability wiring; Phase 2 dispatch-spec Wave band + strategy-as-typed-object — through three governed, logged subagent dispatches: a research→findings→discovery bundle, the three structural sibling views (system/engineer/ontology) conforming to the domainspec view skills, and a tensioned evaluation of how to adapt observability. Decided to keep **two planes, not one ledger**: reuse Arcanum's `observe-invocation.sh` as the sole writer of the capability-telemetry plane (do not port domainspec's appender), adopt domainspec's two-append/append-only/model-authored governance discipline as-is for the dispatch-governance plane, and join them by `dispatch_id`/`run_id`. Identified the real native gap as wiring, not code: `bootstrap_arcanum.sh` emits only the Codex hook surface and must grow a Claude hook-wiring step (governance PreToolUse hooks + the UserPromptSubmit/PostToolUse/Stop observability surface), plus an envelope-producer Formula and additive L2/L3 schema extensions. Also mapped canonical-vs-generated edit locations (`formulae/`, `framework/`, `tools/bootstrap_arcanum.sh`) and bumped the discovery + three views to v0.2.0.

## Files touched

- TO-VLAD/README.md
- research/dispatch-composition-attack/research.md
- research/dispatch-composition-attack/findings.md
- research/dispatch-composition-attack/discovery.md
- research/dispatch-composition-attack/system-view.md
- research/dispatch-composition-attack/engineer-view.md
- research/dispatch-composition-attack/ontology-view.md
- research/observability-adaptation/research.md
- research/observability-adaptation/findings.md
- telemetry/agents/subagents-dispatch.yaml
