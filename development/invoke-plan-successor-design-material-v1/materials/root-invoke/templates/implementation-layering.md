---
module: {module-name}
version: current
status: draft
updatedAt: {date}
docType: implementation-layering
---

# Implementation Layering: {Module Name}

Use this template as the standalone invoke composition unit for the Implementation Layering transmutation.

## Purpose

Define a decision-first layering model that keeps Layer 0 minimal and promotes scope only when evidence justifies it.

## Source Contract

- Transmutation contract: [../../../transmutations/implementation-layering/SKILL.md](../../../transmutations/implementation-layering/SKILL.md)
- Canonical transmutation template: [../../../transmutations/implementation-layering/templates/implementation-layering.md](../../../transmutations/implementation-layering/templates/implementation-layering.md)

## Target And Scope

- Target: {module-name}
- Scope: {feature | capability | workflow | system | infrastructure | research | process}
- Current state: {greenfield | brownfield | partially implemented}

## Layer Boundary Rule

Use this sentence for every layer boundary:

```text
After this layer, we know whether {decision unlocked}.
```

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 (POC) | After this layer, we know whether {core concept works at all}. | {smallest useful end-to-end proof} | {what is included now} | {what is explicitly deferred} | {proof artifacts} | {continue, pivot, or stop} |
| L1 | After this layer, we know whether {repeatability is credible}. | {repeatable working slice} | {hardening scope} | {later reliability or scale concerns} | {evidence links} | {harden, narrow, or stop} |
| L2 | After this layer, we know whether {reliability and governance hold}. | {policy and degraded-mode proof} | {reliability controls} | {scale or packaging concerns} | {evidence links} | {scale, remediate, or stop} |
| L3 | After this layer, we know whether {scale or packaging claim is credible}. | {replication or packaging proof} | {scale-ready scope} | {future scope} | {evidence links} | {pilot, package, or defer} |

## Non Regression Guardrails

- Later layers must preserve guarantees proven in earlier layers.
- Deferred scope must stay explicit; do not silently pull it into earlier layers.
- Promotion decisions must cite evidence, not preference.

## Recommended Next Layer

- Next layer: {L0 | L1 | L2 | L3}
- Key decision unlocked: {decision summary}
- Major deferred scope: {summary}

This template is intentionally concise and composes the canonical transmutation model above.