# Refine Live Example Seeds

## Purpose

These are the first two realistic live examples for promoting `refine` beyond pilot status. They replace the generic starter scenario with user-supplied targets that exercise both major branches of the sigil:

- new sigil seed creation,
- broad architecture/package refinement.

## Live Example 1: `x-ray` New Sigil Seed

Prompt file: `example-prompts/sigil-new-low.md`

Intent:

`x-ray` accepts user-supplied context and creates an HTML page that explains the context through a structured, UX-driven view. It should help a user understand a component, plan, architecture, process, or system through step-by-step explanation, constructed visual explanations, data flow, transformations, actors, process steps, and relationships.

Expected `refine` behavior:

- produce a `Refine Seed Proposal`,
- select a conservative preset for new sigil development,
- offer research,
- plan the required execution stages,
- keep Task Session as executor through Codex Goal,
- route reusable sigil lifecycle ownership to Sigil Development,
- continue far enough through the approved Task Session/Codex Goal path to return final refinement evidence,
- flag or block the run if it can only produce a proposal.

Proposal-only output is useful as preflight evidence, but it is not sufficient promotion evidence for this live example.

## Live Example 2: Observability Package Refinement

Prompt file: `example-prompts/sigil-reflect-complex.md`

Target:

`/home/vrondelli/projects/domainspec-core/arcanum/framework/observability/development`, the observability architecture, and the whole observability package.

Expected `refine` behavior:

- produce a full architecture/design refinement seed,
- bound source context across development artifacts, architecture overview, scripts, and package contracts,
- offer research before browsing,
- plan Context Builder, Invoke, Interrogation, Distill, and Sigil Development stages as needed,
- keep Task Session/Codex Goal as execution owner,
- block with exact missing handoff fields if strict coverage is not ready.

## Promotion Use

Run the examples with:

```bash
arcana/refine/development/run-example-with-codex.sh sigil-new-low
arcana/refine/development/run-example-with-codex.sh sigil-reflect-complex
arcana/refine/development/run-validation-fixtures.sh
arcana/refine/development/write-experiment-report.sh
```
