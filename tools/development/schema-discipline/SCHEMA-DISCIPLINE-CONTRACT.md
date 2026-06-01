# Schema Discipline Contract

## Purpose

This contract defines the lightweight schema discipline Arcanum and CyberAlchemy should apply to runtime artifacts, handoffs, sigils, spells, work-packs, context packs, observability records, and ontology promotion candidates.

The contract is intentionally small. Artifact families may add fields, but they should not remove these review surfaces without a documented reason.

## Contract Fields

| Field / Rule | Tier | Description |
| --- | --- | --- |
| `schema_version` | required | Stable version for the artifact family or template contract. |
| `status` | required | Controlled lifecycle or authority state. |
| `owner` | required | Human, route, lifecycle, or capability responsible for review and mutation. |
| `id` or stable path | required | Stable reference used by other artifacts. |
| field tiers | required | Required, recommended, and optional fields or sections are documented. |
| inline enums | required | Controlled values are listed beside their field definitions. |
| provenance | required | Source inputs, generator, route, command, task/session, or activity that produced the artifact. |
| validation surface | required | Exact checks, commands, fixtures, or review criteria. |
| failure modes | recommended | Named blocked, flagged, failed, deferred, rejected, contradicted, or retired cases. |
| non-goals | recommended | Claims this artifact family must not make. |
| expiry/review date | optional | Use for version-sensitive evidence, context solutions, and operational lessons. |

## Field Tier Rules

- Required fields block consumption when absent.
- Recommended fields flag consumption when absent unless the artifact family says otherwise.
- Optional fields must not change the meaning of required fields.
- `<unset>` or `null` is allowed only when the field definition explicitly permits it.

## Inline Enum Rule

Enums must be documented in the artifact-family contract or template where authors will see them.

Each enum definition must include:

- allowed values;
- field meaning;
- unset/null rule;
- validation behavior for invalid values.

## Provenance Rule

Generated, derived, or candidate artifacts must identify where they came from.

Minimum provenance should name:

- source artifact paths or selectors;
- producing route, task, command, skill, sigil, spell, or agent when known;
- timestamp when the artifact is runtime evidence or development session evidence;
- whether the artifact is candidate, reviewed, promoted, blocked, or retired.

## Validation Surface Rule

Every schema-disciplined artifact family must define how reviewers can validate it without hidden reasoning.

Preferred early validators:

- `test -f` for required files;
- `jq empty` for JSON parse checks;
- `jq -e` for field and enum checks;
- shell checks for path, symlink, and isolation constraints;
- quality-bar review for human-facing Markdown artifacts.

Schema libraries are deferred until repeated structured consumers and drift justify the maintenance cost.

## Blocked-Vs-Flagged Rule

- `blocked`: required evidence, required input, safe execution, or schema validity is missing.
- `flagged`: output exists and can be reviewed, but gaps, warnings, or weaker validation remain.
- `failed`: execution or processing began and then failed unexpectedly.
- `deferred`: the artifact may matter, but owner, evidence, or scope is missing.
- `rejected`: evidence does not support the claim or the artifact is out of scope.

Artifact families may define narrower status models, but they must preserve the distinction between no-safe-consumption and usable-with-warning.

## Candidate-Vs-Canonical Promotion Rule

Candidate schema docs, generated artifacts, telemetry, observability signals, and development handoffs are not canonical authority by default.

Promotion requires:

- visible candidate status before promotion;
- owner or lifecycle route;
- evidence and provenance;
- validation surface;
- use scope;
- contradiction or rollback/retirement path when the result can guide future agents;
- bridge validation when the claim crosses business, system, and operational authority.

## First Family: Runtime

`framework/runtime/` is the first proof family.

Runtime schema discipline currently includes:

- `RUN.json.schema_version`;
- `STATUS.json.schema_version`;
- controlled status and adapter status values;
- `validation_grade`;
- `adapter_profile_path`;
- runner-owned `events.jsonl`;
- adapter event contributions;
- blocked/flagged/failed classification rules;
- shell and `jq` validation.

The runtime family should prove the pattern before the contract expands to all sigils, spells, and ontology promotion records.
