# Validator Surface Decision

## Decision

Inventory should have two validation surfaces:

1. Agent/runtime surface: shell plus `jq`.
2. User interface surface: deferred.

## Rationale

Inventory is primarily a performance-sensitive agent substrate. Agents need a fast way to query, validate, and filter inventory artifacts without loading a heavy runtime or UI layer.

The first executable validator should therefore use shell plus `jq` because:

- current pilot fixtures are JSON;
- the repository command surface already uses shell and `jq`;
- the existing POC validation commands already use `jq` and `rg`;
- agents can run the checks quickly before lookup, retrieval, handoff, or task-session execution;
- the runtime stays portable and easy to compose with `tools/arcanum`.

## Surface Split

| Surface | Primary User | First Runtime | Purpose | Status |
| --- | --- | --- | --- | --- |
| Agent/runtime validator | Agents and local command flows | shell plus `jq` | Fast validation, query filtering, fixture checks, handoff packet safety checks. | selected |
| Human/user interface | Human reviewers | deferred | Browsable inspection, richer review UX, reports, navigation, and explanation. | later |

## First Validator Scope

The agent/runtime validator should check:

- required fields;
- controlled vocabularies;
- selector shape;
- full/minimal profile rules;
- `promotion_owner` and terminal status pairing;
- relation candidate `non_authority_notice`;
- handoff packet `source_refs`;
- handoff packet non-authority text.

## Non-Goals

- Do not build the human UI in the first validator task.
- Do not require Python, Node, or TypeScript before the shell plus `jq` surface proves insufficient.
- Do not make the validator responsible for Ontology Vault promotion or Definitions Governance acceptance.

## Revisit Trigger

Revisit the runtime if shell plus `jq` validation becomes difficult to read, cannot express cross-card consistency checks cleanly, or starts producing reports that humans need to inspect frequently.
