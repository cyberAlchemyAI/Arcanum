# Research Evidence Harness

Research Evidence Harness is a draft Arcana sigil for turning a planned research
experiment into validated, append-only evidence artifacts. It is the proposed
owner for MARS-derived experiment mechanics that do not belong inside
`research-tower`: run schemas, fixture validation, objective/metric checks,
result summaries, and claim-adjudication readiness.

Status: draft candidate, not promoted.

## Problem Solved

Research Tower makes source understanding durable. It does not execute or
validate empirical research evidence.

MOGT needs a reusable evidence harness because its publication path requires:

- experiment bundle discipline;
- append-only JSONL run data;
- schema validation;
- objective-vector and policy-regime checks;
- Pareto/frontier and overhead metric support;
- reviewer-rubric ingestion;
- result summaries that do not overclaim evidence status;
- dry-run fixture proof before live experiment execution.

## When To Use

Use this sigil when:

- a research project already has claims, protocols, and experiment bundles;
- the next blocker is data shape, fixture validation, scoring, or result
  summarization;
- dry-run evidence must be separated from live evidence;
- a paper, research graph, or claim ledger depends on measured outputs;
- MARS-style research gates need to become project-local executable checks.

## When Not To Use

Do not use this sigil for:

- learning or summarizing a paper;
- broad source discovery or related-work mapping;
- canonical term promotion;
- narrative paper rewriting;
- live experiment execution before dry-run schema and fixture validation pass;
- replacing `experiment-harness` for spell/sigil lifecycle experiments.

## Standard Artifact Set

A standard research evidence harness may produce or update:

- `experiments/schema/*.schema.json`;
- `tools/validate-*-run-jsonl.*`;
- `tools/*metric*.*`;
- `development/fixtures/*.jsonl`;
- `development/fixture-validation-report.md`;
- `experiments/*/data/*.jsonl`;
- `experiments/*/results/*.md`;
- `results/*-EVIDENCE-STATUS.md` readiness notes;
- telemetry or observability signal references.

## Relationship To Existing Capabilities

- `research-tower` owns source-backed learning towers and promotion guardrails.
- `context-builder` owns compact source/evidence packs.
- `inventory` owns source library and provenance coverage.
- `experiment-harness` owns reusable spell/sigil validation mechanics.
- `research-evidence-harness` owns project research data mechanics.
- `task-session` owns bounded execution of approved SWUs.

## Lifecycle

This draft candidate is seeded from MOGT and MARS evidence:

- MOGT harness feasibility blocked on missing research-project mechanics.
- MARS provides reusable bundle, pipeline, context, schema, and telemetry
  patterns.
- MOGT should prove the pattern locally before Arcanum absorbs it as canonical.

## Promotion Rule

This sigil may create validation and result artifacts. It must not mark claims
supported, partially supported, contradicted, or paper-ready unless the relevant
project-specific evidence gate allows that update.
