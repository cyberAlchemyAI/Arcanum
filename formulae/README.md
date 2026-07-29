# Formulae - Operational Sigils

Formulae are deterministic sigils: tightly bounded procedures whose success depends on following explicit rules against explicit inputs.

Formulae should feel closer to a validator, formatter, adapter, converter, or mechanical checklist than to an open-ended reasoning partner. They may be executed by an LLM-enabled agent, but the agent's role is to apply rules faithfully rather than invent missing semantics.

## Epistemic Contract

- Primary logic: rule-based execution.
- State model: stateless or explicitly scoped state.
- Input tolerance: low; missing inputs should block, default, or fail predictably.
- Output shape: fixed, inspectable, and repeatable.
- Success measure: reliability, determinism, and auditability.

## Use Formulae For

- validating a document, schema, contract, link set, or policy gate,
- converting one known structure into another known structure,
- enforcing formatting, naming, routing, or packaging rules,
- calling APIs or tools where the operation has a fixed result shape,
- producing pass/fail reports from objective criteria.

## Avoid Formulae When

- the task requires synthesizing ambiguous meaning,
- the agent must decide what the categories themselves should be,
- the result depends on taste, interpretation, negotiation, or trade-off framing,
- the task must coordinate multiple independent agents or recursive decision loops.

## Quality Bar

A Formulae sigil is ready when:

- its trigger conditions are narrow and unambiguous,
- its process can be followed without inventing hidden steps,
- all required inputs and failure modes are named,
- its output contract is stable enough for another agent or script to consume,
- its anti-patterns prevent accidental use for interpretive work.

## Example Sigils

[observability-setup](observability-setup/) installs or verifies the standard repository-local observability package for sigil telemetry.

It belongs here because the procedure is deterministic: create or verify a known folder structure, preserve existing telemetry, and validate known JSON files.

[html-preview-server](html-preview-server/) starts, reuses, verifies, opens, checks,
and stops one exact local HTML artifact through a managed loopback-only server.

It belongs here because target resolution, containment, port binding, readiness,
reuse, and cleanup are explicit operations with fixed receipts and fail-closed
boundaries.

## Relationship To Other Tiers

- Formulae can serve Transmutations by validating the artifacts they produce.
- Formulae can serve Arcana by enforcing gates before or after autonomous orchestration.
- Formulae should not hide probabilistic judgment behind deterministic-sounding language.
