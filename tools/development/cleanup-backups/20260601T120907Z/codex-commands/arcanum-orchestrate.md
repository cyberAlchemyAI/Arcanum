# Arcanum Orchestrate

<!-- arcanum:capability-id arcanum-orchestrate -->
<!-- arcanum:capability-kind skill -->
<!-- arcanum:capability-tier runtime -->
<!-- arcanum:command arcanum-orchestrate -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-arcanum-orchestrate-<UTC timestamp>`.
- `capability.id`: `arcanum-orchestrate`
- `capability.kind`: `skill`
- `capability.tier`: `runtime`
- `capability.mode`: `command`
- `target_artifact`: this command file
- request summary: summarize the user request before execution.
- expected outputs: list intended artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- `OBSERVATION`
- `LEDGER`
- `REFLECTION_TRIGGER`
- `RECOMMENDATION`
- `DEDUPE_KEY`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.


## Objective

Route a user request to the installed Arcanum command surface.

## Process

1. Classify the request as Necronomicon, Ontology Harness, sigil usage, spell usage, install/setup, authoring, validation, observability, or help.
2. Route Necronomicon start, create, resume, close, memory, route, fallback, or capability-update requests to `arcanum-necronomicon` when installed.
3. Route ontology, vault, premise, session distillation, business/system branch, or bridge-validation requests to `arcanum-ontology-harness` when installed.
4. Route lifecycle authoring requests through `arcanum-spell-invoke` when installed.
5. Route explicit sigil or spell requests to the matching installed command and resolve configured aliases to canonical commands.
6. If multiple routes are plausible, ask one focused clarification.
7. Preserve selected command contracts, quality bars, anti-pattern checks, validation gates, gaps, and next route.
8. Return selected route, command used, validation result, observability result, and next action.

## Installed Command Surface

- `arcanum-orchestrate`: general Arcanum router.
- `arcanum-ontology-harness`: alias for `arcanum-spell-ontology-harness`.
- `arcanum-necronomicon`: persistent repository harness command.
- `arcanum-sigil-observability-setup`
- `arcanum-sigil-context-builder`
- `arcanum-sigil-feature-glossary`
- `arcanum-sigil-implementation-layering`
- `arcanum-sigil-architecture-pattern-inventory`
- `arcanum-sigil-decision-gate`
- `arcanum-sigil-definitions-governance`
- `arcanum-sigil-experiment-harness`
- `arcanum-sigil-inventory`
- `arcanum-sigil-invoke-example-runner`
- `arcanum-sigil-ontology-vault`
- `arcanum-sigil-residuality-spec`
- `arcanum-sigil-robot-talks`
- `arcanum-sigil-scope-interview`
- `arcanum-sigil-sigil-development`
- `arcanum-sigil-sigil-runtime-installer`
- `arcanum-sigil-signal-observer`
- `arcanum-sigil-skill-decomposer`
- `arcanum-sigil-skill-transcriptor`
- `arcanum-sigil-spellcraft`
- `arcanum-sigil-structured-interview-kits`
- `arcanum-sigil-interrogation`: alias (Interrogation) for `arcanum-sigil-structured-interview-kits`.
- `arcanum-sigil-task-session`
- `arcanum-sigil-workflow-reflect`
- `arcanum-spell-arcanum-bootstrap`
- `arcanum-spell-discovery-to-inventory`
- `arcanum-spell-implementation-readiness`
- `arcanum-spell-invoke`
- `arcanum-spell-necronomicon`
- `arcanum-spell-observed-invocation-loop`
- `arcanum-spell-ontology-harness`
- `arcanum-spell-repository-harness`
- `arcanum-spell-sigil-maintenance-loop`
