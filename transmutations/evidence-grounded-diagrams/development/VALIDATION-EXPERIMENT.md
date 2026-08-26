# Validation Experiment

## Deterministic Controls

Run:

    python scripts/preflight_runtime.py
    python scripts/validate_skill_package.py
    python development/test_bundle_contract.py
    python development/test_bundle_lifecycle.py
    python development/test_security_contract.py
    python development/test_review_contract.py
    python development/test_persistence_boundary.py
    python development/test_resolver_lifecycle_security.py
    python scripts/validate_review_receipt.py templates/review.receipt.yml --shape-only
    python scripts/detect_renderer_capabilities.py --json
    python development/run_validation_fixtures.py

The controls cover package/runtime closure, request and review discrimination,
draft persistence, commit-marker crash recovery, permanent revision reservation,
resolver discovery, immutable lineage, draft/validated superseding semantics,
receipt authority, exact member coverage, evidence binding, atomic index updates,
concurrent writers, telemetry durability, promotion evidence, false readiness,
path confinement, and canonical byte stability during the report run.

## Forward Tests

Use fresh agents with only the canonical skill path, the task prompt, and raw
evidence. Preserve full user-facing output bodies under
development/example-outputs/.

These are retained one-shot behavioral observations, not Experiment Harness
loop regimes. The canonical lifecycle regimes are the five `LIVE-SIGIL-*`
entries declared by `EXPERIMENT-PROFILE.md`.

Required behavioral coverage:

- low create;
- negative insufficient evidence;
- medium read-only review;
- complex revise and official-publication boundary.

## Renderer Boundary

Mermaid CLI, Graphviz, and PlantUML are not assumed. A source-only draft is a
valid harness result when render inspection is NOT_RUN with a reason. It is not
promotion evidence for official publication.

## Platform Runtime

The Windows `bash.exe` entry points route to an unavailable WSL environment,
but Git Bash is available at `C:\Program Files (x86)\Git\bin\bash.exe`. The
canonical Experiment Harness was initialized and validated through that runtime.
The portable Python promotion runner is authoritative on this Windows host. The
shell wrappers remain compatible adapters for environments with the canonical
Experiment Harness shell dependencies.
