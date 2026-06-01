# Translate Fixture Corpus

## Purpose

Validate the first Translate schema against three positive cross-domain translations and one failed analogy.

## Fixture 1: Sales Terms To Software Architecture Decision

### Request

| Field | Value |
| --- | --- |
| translation_request_id | TRQ-SALES-ARCH-001 |
| target_concept | architecture boundary decision |
| source_domain | sales |
| target_domain | software architecture |
| requested_style | concrete-first |
| user_handle_refs | UDA-SALES-001, UVP-CONCRETE-FIRST-001 |

### Term Map

| source_term | target_term | mapping_note |
| --- | --- | --- |
| qualification criteria | interface contract | Both decide what is allowed to pass into the next step. |
| pipeline stage | architectural layer | Both represent a stage with expectations before handoff. |
| objection handling | boundary validation | Both identify why a handoff may fail. |

### Bridge Map

| Field | Value |
| --- | --- |
| analogy_or_metaphor | Architecture boundary as sales qualification gate. |
| maps_well | Both prevent bad-fit work from moving downstream. |
| breaks_here | Software boundaries enforce machine-readable behavior; sales qualification includes human judgment. |
| bridge_quality | strong |

### Output

| Field | Value |
| --- | --- |
| target_domain_definition | An architecture boundary is a designed separation between system parts, with explicit contracts for allowed dependencies, data, behavior, and failure handling. |
| translated_explanation | Think of a boundary like qualification criteria: it protects the next stage from receiving something that does not fit the contract. |
| mapping_limits | Do not treat architecture boundaries as negotiable conversations; code and runtime behavior need explicit enforcement. |
| research_need | none |
| status | pass |

## Fixture 2: Software Engineering Terms To Scientific Formula

### Request

| Field | Value |
| --- | --- |
| translation_request_id | TRQ-SOFT-SCI-001 |
| target_concept | scientific formula |
| source_domain | software engineering |
| target_domain | scientific modeling |
| requested_style | system behavior |
| user_handle_refs | UCS-API-001 |

### Term Map

| source_term | target_term | mapping_note |
| --- | --- | --- |
| function signature | formula variables | Both define required inputs and expected output shape. |
| invariant | conservation or constraint | Both describe what must remain true. |
| test case | experimental observation | Both check whether behavior matches expectation. |

### Bridge Map

| Field | Value |
| --- | --- |
| analogy_or_metaphor | Formula as a pure function with domain constraints. |
| maps_well | Inputs, transformations, outputs, and constraints can map clearly. |
| breaks_here | Scientific formulas model observed reality and uncertainty; software functions execute designed logic. |
| bridge_quality | partial |

### Output

| Field | Value |
| --- | --- |
| target_domain_definition | A scientific formula is a compact relationship among quantities that models or predicts behavior under defined conditions. |
| translated_explanation | Read the formula like a function: variables are inputs, constants and operators define the transformation, and the result is meaningful only inside the assumptions. |
| mapping_limits | Do not confuse model prediction with deterministic program execution. |
| research_need | none |
| status | pass |

## Fixture 3: Musician Terms To Civil Construction Plan

### Request

| Field | Value |
| --- | --- |
| translation_request_id | TRQ-MUSIC-CONSTRUCTION-001 |
| target_concept | construction sequencing plan |
| source_domain | music |
| target_domain | civil construction |
| requested_style | rehearsal and arrangement |
| user_handle_refs | UDA-MUSIC-001 |

### Term Map

| source_term | target_term | mapping_note |
| --- | --- | --- |
| arrangement | construction plan | Both organize parts into a coherent order. |
| rhythm | schedule cadence | Both create timing expectations. |
| rehearsal | dry run or readiness check | Both expose coordination problems before performance/work. |

### Bridge Map

| Field | Value |
| --- | --- |
| analogy_or_metaphor | Construction plan as an arrangement with dependencies and timing. |
| maps_well | Sequence, coordination, timing, and dependency awareness map well. |
| breaks_here | Construction has physical safety, permits, materials, and irreversible work that music analogy does not cover. |
| bridge_quality | partial |

### Output

| Field | Value |
| --- | --- |
| target_domain_definition | A construction sequencing plan orders work activities, dependencies, resources, and safety constraints so construction can proceed safely and efficiently. |
| translated_explanation | Like an arrangement, the plan decides what comes first, what supports what, and where timing problems will break the whole performance. |
| mapping_limits | Do not use the music analogy to ignore material constraints, safety, or regulatory requirements. |
| research_need | none |
| status | pass |

## Fixture 4: Failed Analogy Preserves Target Definition

### Request

| Field | Value |
| --- | --- |
| translation_request_id | TRQ-FAILED-001 |
| target_concept | architecture dependency inversion |
| source_domain | music |
| target_domain | software architecture |
| requested_style | metaphor |
| user_handle_refs | UDA-MUSIC-001 |

### Bridge Map

| Field | Value |
| --- | --- |
| analogy_or_metaphor | Dependency inversion as "letting the melody depend on harmony." |
| maps_well | Almost nothing beyond vague relationship language. |
| breaks_here | Dependency inversion is about source-code direction and abstractions, not aesthetic support. |
| bridge_quality | failed |

### Output

| Field | Value |
| --- | --- |
| target_domain_definition | Dependency inversion is a design principle where high-level policy depends on abstractions rather than concrete low-level details. |
| translated_explanation | The music metaphor should not be used here; explain with interface and contract examples instead. |
| mapping_limits | Failed analogy recorded as residue for User ledger. |
| research_need | none |
| status | flag |

## Fixture Checklist

- Each positive fixture includes target-domain definition.
- Each bridge includes `maps_well` and `breaks_here`.
- Failed analogy preserves target truth and produces residue.
- Translate flags research need instead of performing research.
