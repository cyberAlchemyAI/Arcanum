---
name: verification-weaver
description: Use when routing a verification target to status-qualified owner lanes and joining native evidence receipts into a VERIFICATION-WEAVE parent receipt without promoting owner outputs.
argument-hint: "<target-or-receipt> [--mode route|validate-receipt|fixture-plan|report]"
tier: arcana
domain: verification-evidence-routing
version: 0.1.0-candidate
origin: created from SWU-VW-001 on 2026-06-21
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Verification Weaver

Use `verification-weaver` when a target needs evidence routing across testing,
UX, execution, architecture, or research lanes and the output must remain a
parent receipt instead of an owner-level promotion.

## Contract

Core verb: `route`.

Receipt type: `VERIFICATION-WEAVE`.

The capability:

1. classifies the target kind;
2. selects the owning verification lane or records an unsupported target;
3. checks for a recognized oracle or explicit gap;
4. joins owner statuses into a parent receipt;
5. fails closed when public-safety or promotion boundaries are violated.

## Owner Boundaries

`verification-weaver` may route to these lanes:

- `test-derivation`
- `ux-evidence-validator`
- `experiment-harness`
- `architecture-pattern-inventory`
- `research-evidence-harness`

It must not perform the owner work itself. Owner outputs stay status-qualified,
and parent receipts may use only `promotion_action: none` or
`promotion_action: candidate-request`.

## Inputs

Accept one bounded target or one existing receipt. A target can be:

- a formal/spec obligation;
- a frontend or UX validation concern;
- an execution repeatability concern;
- an architecture-alignment gap;
- a research-evidence question;
- a mixed target requiring decomposition;
- an unsupported input that must block.

## Output

Emit or update a `VERIFICATION-WEAVE` parent receipt with:

- target identity and `target_kind`;
- classification and oracle type;
- owner lane refs and owner statuses;
- evidence refs or explicit gaps;
- public-safety scan statuses;
- parent `status`;
- `promotion_action`;
- next route recommendation.

## Pass, Flag, Block

Pass only when the target is classified, required owner evidence or explicit
gaps exist, public-safety checks pass, and no parent promotion is attempted.

Flag when the route is useful but still has soft residue, such as UX human
comprehension risk, architecture source incompleteness, mixed-target split
needs, or research dry-run limits.

Block unsupported targets, missing oracles, hard public-safety failures,
flaky evidence, adapter failures, and parent promotion attempts.

## Development Validation

Run:

```sh
bash arcanum/arcana/verification-weaver/development/run-validation-fixtures.sh
```

The runner validates synthetic fixtures and runnable negative controls. Treat
the runner output as candidate package evidence, not as registry promotion.
