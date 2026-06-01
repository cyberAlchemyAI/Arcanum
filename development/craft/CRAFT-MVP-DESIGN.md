# Craft Recursive Ledger MVP Design

## Invoke Result

- Mode: design
- Spell: invoke
- Canonical ID: invoke
- Scope: Craft recursive ledger MVP
- Phase status: pass
- Mode contract: `spells/invoke/design.md`
- Outputs: `development/craft/CRAFT-MVP-DESIGN.md`
- Design views: context, high-level structure, low-level components, workflow process, decision flow, dependency interface
- Template/profile selection: local architecture/design bundle for a YAML-backed operational MVP
- Implementation layering: [CRAFT-MVP-IMPLEMENTATION-LAYERING.md](CRAFT-MVP-IMPLEMENTATION-LAYERING.md)
- Work-pack: n/a
- Decisions: use a YAML schema contract, a Markdown ledger fixture, and manual validation; keep generated indexes, scoring, runtime integration, and role delegation deferred
- Unresolved gaps: waiver behavior and validation proof remain execution tasks, not design blockers
- Next route: plan

## Purpose

Design the first Craft recursive-ledger MVP from the define baseline in [CRAFT-MVP-DEFINE.md](CRAFT-MVP-DEFINE.md).

This design is plan-ready: it identifies the artifacts, row families, validation flow, and boundaries needed by [CRAFT-MVP-WORK-PACK.md](CRAFT-MVP-WORK-PACK.md), but does not execute the work.

## Source Contracts

| Source | Role |
| --- | --- |
| [CRAFT-MVP-DEFINE.md](CRAFT-MVP-DEFINE.md) | MVP objective, scope, deferrals, glossary, and acceptance criteria. |
| [CRAFT-LEDGER-SCHEMA.yml](CRAFT-LEDGER-SCHEMA.yml) | YAML schema contract for row families, fields, enums, and validation rules. |
| [CRAFT-RECURSIVE-LEDGER-DESIGN.md](CRAFT-RECURSIVE-LEDGER-DESIGN.md) | Minimal schema for contexts, artifacts, relations, typed items, and decisions. |
| [CRAFT-LEDGER-TYPE-EXAMPLES.md](CRAFT-LEDGER-TYPE-EXAMPLES.md) | Example rows for contexts, blockers, gates, enablers, lanes, and role hints. |
| [CRAFT-LEDGER-TYPE-SYSTEM.md](CRAFT-LEDGER-TYPE-SYSTEM.md) | Type, lane, role-hint, and blocker-refinement vocabulary. |
| [CRAFT-RECURSIVE-LEDGER-GLOSSARY.md](CRAFT-RECURSIVE-LEDGER-GLOSSARY.md) | Candidate term baseline for recursive ledger concepts. |

## View 1: Context View

The MVP lives entirely under `development/craft/` and is owned by the Craft durable development session.

```text
Craft Development
  -> Recursive Ledger MVP
      -> Type And Lane Model
      -> Ledger Schema
      -> Ledger Fixture
      -> Ledger Validation
      -> Future Scoring
```

The ledger fixture represents the current operational state of these contexts. It is not the canonical Arcanum registry and does not promote Craft into a sigil, spell, or runtime command.

## View 2: High-Level Structure View

The MVP has three planned output artifacts:

| Artifact | Responsibility |
| --- | --- |
| `CRAFT-LEDGER-SCHEMA.yml` | Structured schema authority for row families, fields, enums, validation rules, and blocker lifecycle constraints. |
| `LEDGER.md` | Human-readable source of truth for recursive contexts, artifacts, relations, typed items, and decisions. |
| `LEDGER-VALIDATION.md` | Manual validation report for schema rules, blocker lifecycle behavior, and waiver behavior. |

Supporting artifacts:

| Artifact | Responsibility |
| --- | --- |
| [CRAFT-MVP-DEFINE.md](CRAFT-MVP-DEFINE.md) | Define baseline. |
| [CRAFT-MVP-DESIGN.md](CRAFT-MVP-DESIGN.md) | Design baseline. |
| [CRAFT-MVP-IMPLEMENTATION-LAYERING.md](CRAFT-MVP-IMPLEMENTATION-LAYERING.md) | L0-L2 promotion and deferral boundaries. |
| [CRAFT-MVP-WORK-PACK.md](CRAFT-MVP-WORK-PACK.md) | Execution plan and task contracts. |

## View 3: Low-Level Components View

`CRAFT-LEDGER-SCHEMA.yml` defines the valid shape of these row families. `LEDGER.md` should then contain these sections in schema order:

1. context rows,
2. artifact rows,
3. relation rows,
4. typed item rows,
5. decision rows,
6. notes for side-thread artifacts and deferrals.

Typed item rows unify blockers, gates, and enablers. Each typed item carries:

- `kind`,
- `base_type`,
- `context_type`,
- `primary_lane`,
- `secondary_lanes`,
- `source_id`,
- `target_id`,
- `status`,
- `refinement_status`,
- `default_role`,
- `delegation_route`,
- `closure_condition`,
- `evidence`,
- `reason`.

Decision rows are required for waivers and should be linkable from typed item evidence or reason fields.

## View 4: Workflow Process View

The MVP workflow is:

```text
define baseline
  -> design baseline
  -> MVP work-pack
  -> create LEDGER.md fixture
  -> add blocker refinement and waiver traces
  -> validate schema and lifecycle rules
  -> sync package state
```

Execution should use one task at a time:

1. `CRAFT-MVP-001`: create the first ledger fixture.
2. `CRAFT-MVP-002`: add blocker refinement and waiver traces.
3. `CRAFT-MVP-003`: create manual validation.
4. `CRAFT-MVP-004`: sync README and session ledger after validation.

## View 5: Decision Flow View

| Condition | Decision |
| --- | --- |
| Ledger row can represent a required example with current fields. | Continue execution. |
| Ledger row needs a new field to satisfy acceptance. | Stop and run compact `/refine` on the schema. |
| Blocker is raw or typed and lacks refinement evidence. | It cannot be marked resolved. |
| Blocker resolution must bypass normal refinement. | Require waiver decision row. |
| Validator or auditor lane is involved in closure. | Require evidence note before closure. |
| Runtime integration question appears. | Route to the separate runtime/refine thread, not this MVP. |
| Scoring or role delegation appears. | Record as deferred unless user explicitly opens a new plan. |

## View 6: Dependency Interface View

| Dependency | Interface | Risk |
| --- | --- | --- |
| YAML schema | `CRAFT-LEDGER-SCHEMA.yml` row families, required fields, enums, and validation rules | If fields cannot represent waiver or closure evidence, schema refinement is required. |
| Ledger fixture | `LEDGER.md` rows shaped by the YAML schema | If the fixture cannot instantiate a valid row, either the row is wrong or the YAML contract needs refinement. |
| Type system | `base_type`, `context_type`, `primary_lane`, `secondary_lanes`, `default_role` | Role hints may look too operational; keep delegation non-executable. |
| Example rows | Seed rows and acceptance examples | Examples may be copied too literally; update status to current Craft state. |
| Package state | README and session ledger links | Sync only after validation exists so package state does not overclaim. |
| Runtime side-thread | linked artifacts only | Runtime decisions must not become MVP acceptance criteria. |

## Glossary Consistency

| Term | Status | Notes |
| --- | --- | --- |
| recursive context | linked | Matches the broader recursive-ledger glossary. |
| typed item | linked | Uses schema family for blockers, gates, and enablers. |
| blocker refinement | linked | Preserves the user-requested rule before resolution. |
| waiver decision | linked | Design makes waiver explicit through decision rows. |
| operational lane | linked | Uses current lane vocabulary from the type system. |
| role delegation | partial | Preserved as future role hints, not executable delegation. |

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Plan starts from design artifacts but skips define/design lifecycle records. | Traceability gap. | This artifact and [CRAFT-MVP-DEFINE.md](CRAFT-MVP-DEFINE.md) close the gap. |
| Waiver policy is too abstract. | False blocker closure. | Require a real waiver row in `CRAFT-MVP-002`. |
| Runtime strategy leaks into Craft MVP. | Scope drift. | Keep runtime artifacts as side-thread references only. |
| Role hints are mistaken for automation. | Premature delegation. | Keep `default_role` and `delegation_route` advisory in MVP. |

## Plan Handoff Notes

The plan should:

- treat this design as the approved MVP design reference,
- treat [CRAFT-LEDGER-SCHEMA.yml](CRAFT-LEDGER-SCHEMA.yml) as schema authority,
- produce `LEDGER.md` from the YAML contract before `LEDGER-VALIDATION.md`,
- include waiver and blocker-refinement evidence in the fixture,
- validate manually before syncing README/session state,
- route only acceptance-affecting schema ambiguity through `/refine`.

## Next Route

`invoke plan` through [CRAFT-MVP-WORK-PACK.md](CRAFT-MVP-WORK-PACK.md).
