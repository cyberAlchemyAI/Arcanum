# Context Builder Handoff Pack

Status: pass
Mode: standard
Strict coverage: pass
Handoff: runtime

## Task

Run a full Refine session for a proposed public Arcanum integration-boundary capability. The operator wants something like DomainSpec, but focused on integrations: interfaces between systems, application-layer ports, database selection and handling, external APIs, cache, events, policies, mappings, and evidence.

## Obligations

| ID | Obligation | Coverage |
| --- | --- | --- |
| O1 | Preserve public `arcanum` boundary. | covered by seed, dispatch gates, and owner-boundary warnings |
| O2 | Reuse DomainSpec taxonomy where possible. | covered by `TAXONOMY.md`, `DEFINITIONS.md`, `RELATIONSHIPS.md` |
| O3 | Use Two-Lane Discipline. | covered by supplied discipline and subagent receipts |
| O4 | Run bounded external research. | covered by `04-bounded-research.md` |
| O5 | Decide whether a new package is justified. | covered by `05-distill.md`, `07-refine-design-review.md`, `RESULT.md` |
| O6 | Produce non-executed plan and next route. | covered by `09-invoke-plan.md` |

## Selected Evidence

| Source | Selectors | Why included |
| --- | --- | --- |
| `arcanum/definitions/TAXONOMY.md` | connective concepts, architecture mapping, layer dependency rule | proves existing Interface/Event/Mapping/Policy/Application-layer vocabulary |
| `arcanum/definitions/RELATIONSHIPS.md` | backend, cross-layer, and cross-feature edges | shows reusable and strained relationship vocabulary |
| `arcanum/definitions/DEFINITIONS.md` | DS-D1, DS-D2, canon boundary | blocks silent taxonomy mutation |
| `arcanum/spells/invoke/templates/domainspec-spec/` | README, SPEC, interfaces, mappings | shows existing DomainSpec template family and aspect docs |
| `arcanum/formulae/dispatch-spec/development/TANDEM-INTEGRATION-OPTIONS.md` | adapter and receipt options | prior integration-adapter evidence, analogy-only |
| supplied Two-Lane Discipline | Lane Z, Lane A, synthesis rules | required research tension and bridge decisions |

## Constraints

- Do not create or promote `arcanum/arcana/integration-spec/SKILL.md` in this refine run.
- Do not change `arcanum/definitions/*`.
- Do not change DomainSpec templates in this refine run.
- Do not treat runtime receipts as canonical spec truth.
- Keep all examples public-safe and system-agnostic.

## Fallback Rule

If the new arcana package is not proven as the smallest responsible unit, select a smaller governed route and record how it can later recompose into IntegrationSpec.
