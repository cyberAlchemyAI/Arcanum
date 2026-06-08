---
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: arcana/research-evidence-harness/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
name: research-evidence-harness
description: "Use when: converting research protocols into validated run schemas, JSONL fixture checks, objective/metric calculations, result summaries, and claim-adjudication readiness without running or overclaiming live experiments."
argument-hint: "<research-project> [--swu <id>] [--dry-run] [--validate] [--summarize]"
tier: arcana
domain: research-governance
version: 0.1.0
origin: proposed from MOGT harness feasibility and MARS import/absorption refinement
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Sigil: Research Evidence Harness

<objective>
Turn planned research experiments into validated evidence-capture artifacts:
schemas, append-only JSONL checks, dry-run fixtures, metric calculations,
result summaries, and claim-adjudication readiness.
</objective>

<logic-type>
Arcana: empirical research evidence governance with schema discipline, dry-run
proof, metric validation, and publication-safe claim boundaries.
</logic-type>

<applicability>
Use this sigil when:

- a research project has claims, protocols, experiment bundles, or a paper
  contract, but lacks executable evidence mechanics;
- dry-run fixtures must prove data shape before live runs;
- JSONL run data needs schema and metadata validation;
- objective vectors, scoring policies, reviewer rubrics, or analysis summaries
  must be checked before evidence status changes;
- MARS-style research pipeline assets are being adapted locally.
</applicability>

<non-applicability>
Do not use this sigil when:

- the task is source understanding, notation translation, local glossary, or
  bridge decisions; use `research-tower`;
- the task is generic spell/sigil prompt validation; use `experiment-harness`;
- the task is broad planning with no approved work unit; use `refine` and
  `invoke`;
- the user wants live experiment execution before dry-run validation has passed.
</non-applicability>

<inputs>
Expected inputs:

- research project root;
- selected experiment or SWU;
- protocols and methodology profiles;
- required common run fields;
- metric and success-criteria definitions;
- source/context requirements;
- write scope;
- validation command or review surface;
- evidence-status guardrails.
</inputs>

<process>
1. Verify the project already has a bounded research objective, claims, and
   experiment bundle roots.
2. Read the selected task or SWU and its write scope.
3. Identify required run fields from the protocol, feasibility report, or
   work-pack.
4. Create or update a project-local run schema.
5. Create or update a validator for append-only JSONL rows.
6. Add synthetic passing and failing fixtures before any live run.
7. Validate fixtures and record command output.
8. Add objective-vector, policy-regime, reviewer-rubric, or metric calculators
   only when the selected SWU owns them.
9. Generate result summaries only from validated fixture or run data.
10. Preserve dry-run/live evidence separation.
11. Block evidence-status upgrades unless live experiment analysis supports the
    claim update and the project gate allows it.
12. Return the validation result, files produced, remaining blockers, and next
    governed route.
</process>

<quality-bar>
A successful execution must:

- preserve the selected write scope;
- create project-local evidence mechanics rather than mutating canonical
  Arcanum contracts;
- validate at least one passing and one failing fixture for schema work;
- reject missing run metadata, objective vectors, policy regimes, and malformed
  metric fields when applicable;
- distinguish dry-run fixture evidence from live experiment evidence;
- keep claim/evidence status unchanged unless a later approved analysis task
  supports an update;
- record validation commands or reviewable evidence;
- leave the next SWU or blocker explicit.
</quality-bar>

<anti-patterns>
Avoid:

- treating a planned protocol as empirical support;
- upgrading paper claims from synthetic fixture data;
- copying MARS project-specific fields into unrelated projects unchanged;
- hiding protocol deviations;
- mixing source discovery, learning tower, and run-data validation in one
  artifact;
- mutating `experiment-harness`, `research-tower`, or paper contracts without a
  separate governed route.
</anti-patterns>

<output-contract>
Return:

```markdown
## Research Evidence Harness Result

- Target: <research project>
- Selected unit: <experiment | task | SWU>
- Mode: dry-run | validate | summarize | mixed
- Status: pass | flag | block
- Schema: <path or none>
- Validator: <path or none>
- Fixtures: <paths or none>
- Metrics: <paths or none>
- Result summary: <path or none>
- Evidence-status boundary: preserved | updated-by-approved-live-analysis | block
- Validation: <commands or review evidence>
- Remaining blockers: <items or none>
- Next route: task-session | codex-goal-profile | publication-research-pipeline | deferred
```
</output-contract>
