# Constitution Governance Implementation Layering

Status: candidate
Date: 2026-05-27

## L0: Source Contract

Goal: create the sigil folder with README, SKILL, templates, and registry entry.

Evidence:

- `arcana/constitution-governance/README.md`
- `arcana/constitution-governance/SKILL.md`
- templates under `arcana/constitution-governance/templates/`

## L1: Validator Awareness

Goal: make existing artifact constitution validation aware of the new rendering rule and preserve a validator integration pattern.

Evidence:

- `tools/validate-artifact-constitution.sh`
- `framework/ARTIFACT-CONSTITUTION.md`
- `framework/ARTIFACT-AUTHORING-MEMORY.md`

## L2: Example Composition Packs

Goal: add example prompts and fixtures showing selection versus composition.

Candidate examples:

- chart artifact rendering constitution,
- ontology schema artifact constitution,
- invoke work-pack artifact constitution.

## L3: Command Surface

Goal: install or expose `constitution-governance` as a command surface through sigil runtime installer once examples validate.

Promotion evidence:

- command resolves,
- example runs produce real composition packs,
- validator impact is traceable to rule IDs.

## L4: Reflection

Goal: observe repeated constitution bloat, validator drift, or context overload signals and reflect on sigil rules.

Promotion evidence:

- telemetry schema,
- reflection threshold,
- at least one reflection report after meaningful executions.
