# Research Decision

## Decision

Mode: `bounded-research`

Reason: the user explicitly requested that `Arize-ai/openinference` be included as an option.

## External Option: Arize-ai/openinference

Source: `https://github.com/Arize-ai/openinference`

Observed fit:

- OpenInference defines conventions and plugins complementary to OpenTelemetry for tracing AI applications.
- It is intended to expose LLM invocation context, retrieval, tool/API usage, and related application context.
- It provides semantic conventions and instrumentation packages across Python, JavaScript, Java, and Go.
- It supports Arize Phoenix, Arize AX, and any OTEL-compatible collector.

Local interpretation:

- Treat OpenInference as an interoperability option for AI-span semantics and SDK instrumentation.
- Do not treat it as a replacement for the local Arcanum observer envelope, ledger, reflection trigger, command provenance, or target-artifact ownership model.
- A viable integration path would map Arcanum invocation envelopes and stage evidence to OpenTelemetry/OpenInference spans while preserving the repository-local ledger as canonical workflow evidence.

## Research Status

Status: `flag`

The option was identified and summarized, but the full refine loop did not run. This research note is candidate input for a later design stage, not promoted architecture.
