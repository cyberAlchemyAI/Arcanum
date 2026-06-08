# Workflow Reflect

Workflow Reflect is an Arcana sigil for turning accumulated sigil observability signals into evidence-backed improvement proposals.

It is the retrospective outer loop for sigil maintenance. It reads telemetry, detects repeated gaps and useful patterns, computes simple trend metrics, compares current behavior to previous reflections, and writes a reflection report with concrete recommendations.

## Problem It Solves

One failed run can be noise. Repeated failures, output drift, user corrections, or anti-pattern hits are signals that the sigil itself may need improvement.

Workflow Reflect prevents maintenance from being driven only by memory or vibes. It uses accumulated telemetry to decide whether a sigil needs no change, a targeted update, a major revision, or retirement.

## Use When

- a reflection threshold has been reached,
- a user asks for a retrospective on sigil behavior,
- repeated workflow gaps appear in observability ledgers,
- a sigil has generated enough outputs to review quality trends,
- maintainers need evidence before changing a sigil contract.

## Do Not Use When

- there are too few signals to support a useful pattern claim,
- the user only needs the latest run observed by [signal-observer](../signal-observer/),
- the sigil itself should be edited immediately by a separate maintenance workflow,
- telemetry contains sensitive content that has not been summarized or redacted,
- the desired outcome is implementation work rather than reflection.

## Reflection Loop

1. Load signal ledgers and reflection state.
2. Apply filters such as sigil name, date range, or minimum signal count.
3. Group signals by type, severity, sigil, mode, output contract, and gap category.
4. Detect recurring workflow gaps, quality failures, anti-pattern hits, output drift, and useful patterns.
5. Compare current patterns against previous reflection reports.
6. Generate evidence-backed proposals.
7. Write a reflection report.
8. Recommend no change, targeted update, major revision, or retirement.

## Output

The sigil produces a reflection report with:

- signal summary,
- triggered thresholds,
- repeated patterns,
- gap analysis,
- proposed iterations,
- rejected changes,
- contract preservation notes,
- updated reflection policy,
- recommended next lifecycle step.

## Related Docs

- [Signal Observer](../signal-observer/)
- [Sigil Observability Hook](../../framework/observability/SIGIL-OBSERVABILITY-HOOK.md)
- [Repository Observability Package](../../framework/observability/REPOSITORY-PACKAGE.md)

## Why This Is Arcana

Workflow Reflect coordinates cross-run evidence analysis, threshold interpretation, proposal generation, and lifecycle routing. It changes the future of the workflow by interpreting accumulated behavior, not by executing a single local transformation.
