---
module: {module-name}
version: current
status: draft
updatedAt: {date}
docType: research-brief
---

# Research Brief: {Module Name}

Use this template when context is incomplete and decisions need evidence before design or implementation planning.

## Objective

State the research objective in one sentence.

## Scope

- In scope: {questions and boundaries}
- Out of scope: {explicit exclusions}

## Question Set

| Question ID | Question | Why It Matters | Expected Decision Impact |
| --- | --- | --- | --- |
| Q1 | {question} | {risk or uncertainty reduced} | {define, design, plan, or validate} |

## Evidence Sources

| Source | Type | Reliability | Notes |
| --- | --- | --- | --- |
| {source path or uri} | doc, code, telemetry, interview | high, medium, low | {reason} |

## Findings

| Finding ID | Summary | Evidence | Confidence |
| --- | --- | --- | --- |
| F1 | {finding summary} | {source reference} | high, medium, low |

## Options

| Option | Description | Trade-offs | Recommended |
| --- | --- | --- | --- |
| A | {option summary} | {cost, risk, complexity} | yes or no |
| B | {option summary} | {cost, risk, complexity} | yes or no |

## Unresolved Gaps

- {gap 1}
- {gap 2}

## Handoff Targets

| Target Contract | Purpose | Status |
| --- | --- | --- |
| [module-spec.md](module-spec.md) | Update module objective and boundaries. | pending |
| [architecture-bundle.md](architecture-bundle.md) | Convert findings into structural decisions. | pending |
| [implementation-plan.md](implementation-plan.md) | Convert decisions into delivery slices. | pending |
| [execution-pack.md](execution-pack.md) | Convert delivery slices into gated execution. | pending |

## Decision Snapshot

| Decision ID | Chosen Option | Rationale | Owner | Timestamp |
| --- | --- | --- | --- | --- |
| D-001 | {option} | {summary} | {owner} | {iso-timestamp} |
