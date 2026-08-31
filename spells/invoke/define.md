# Invoke Define Mode

For a plain-language introduction, start with the
[human overview](./define/README.md). This file is the formal mode contract.

## Identity

- Spell: `invoke`
- Mode: `define`
- Status: implemented (L0 definitions-bearing atomic producer)

## Purpose

Define mode produces or updates a governed specification and a machine-readable
candidate definition registry with explicit decisions, evidence-aware template
routing, deterministic human views, and transport-ready handoff artifacts.

## Implementation Coverage

- New Define production uses `invoke.generic-definitions-baseline.v3` through
  `scripts/compile_define_source_v3.py`, after an independent semantic closure
  and before independent bundle admission.
- Define v3 publishes its complete candidate bundle without replacement through
  native atomic rename semantics on Linux, macOS, and Windows. Unsupported
  filesystem variants use an exclusive sibling-lock fallback.
- The v1/v2 sources, profiles, receipts, compilers, and tests remain readable
  and testable compatibility artifacts. Neither receipt version can establish
  a new Define PASS.
- `DEFINITIONS.json` is the machine artifact. `DEFINITIONS.md` and
  `GLOSSARY.md` are deterministic views derived from it; neither is an
  independent source of definition authority.
- Implementation layering is integrated as a companion artifact policy: define may seed L0 or record a layering gap for downstream plan/full modes.
- Registry release remains blocked until required template and profile-family validation examples pass.

## Required Sigils

| Sigil                       | Role In Mode                                                          | Required Mode                                       |
| --------------------------- | --------------------------------------------------------------------- | --------------------------------------------------- |
| `context-builder`           | Build bounded define context from user goal and existing artifacts.   | lean or standard                                    |
| `structured-interview-kits` | Clarify missing context one question at a time and capture approvals. | gap-check or equivalent one-question interview mode |
| `inventory`                 | Resolve templates and record selection evidence.                      | lookup, ingest, validate                            |

## Optional Sigils

| Sigil               | Use When                                                                    | Notes                                                                  |
| ------------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `decision-gate`     | A blocker-level define decision cannot be resolved from available evidence. | Route only consequential unresolved choices.                           |
| `distill`           | The definition target is broad, ambiguous, or likely to split into multiple spec/glossary units. | Run a definition-scope sanity check and record `pass`, `flag`, `block`, or `not required`; do not create plan-ready work. |
| `spellcraft`        | Approved define output targets spell authoring or spell revision.           | Invoke emits handoff pack; Spellcraft owns spell lifecycle mutation, validation, install/adaptation, observation, and reflection. |
| `sigil-development` | Approved define output targets sigil authoring or sigil revision.           | Invoke emits handoff pack; Sigil Development owns sigil lifecycle mutation, validation, observability, reflection, and promotion readiness. |

## Inputs

- user goal and scope hints
- existing artifacts and local constraints
- the [Define v3 authoring guide](./define-authoring-guide.md) and its exact
  [mixed source example](./examples/define-v3/DEFINE-SOURCE.json)
- an independently authored
  [semantic context](./schemas/define-semantic-context-v1.schema.json) and a
  current passing semantic-closure receipt
- template inventory or candidate-template permission
- optional existing implementation-layering artifact for update or reuse
- definition sources from Necronomicon context or exact repository-local
  evidence when needed
- an identity-denominator request when any Define artifact asserts an exact or
  canonical ID-to-label denominator

## Canonical Atomic Producer

Models first author one `invoke.define-semantic-context.v1` document for an
independent assessor. Only an exact `ready-for-define` closure may feed one
schema-valid `invoke.define-source.v3` source. That source applies every closure
disposition exactly once through candidate definitions and/or canonical
authority bindings. The compiler validates closure replay, profile selection,
declarations, evidence, relation closure, layering, dispatch and Distill
classifications, identity-denominator evidence, output contracts, transport
scope, and next route. It derives `DEFINITIONS.json`, `DEFINITIONS.md`, and
`GLOSSARY.md`, then publishes exactly thirteen files only after the final
`invoke.define-stage-receipt.v3` validates. That receipt exact-binds every
machine-checkable structural schema observed during compilation. Any failure
leaves the output directory absent.

The independent admission validator recompiles the exact source into an
ephemeral directory, byte-compares the submitted and clean bundles, revalidates
the semantic closure, machine artifact, deterministic views, structural
schemas, identity denominator, semantic outcome, and authority ceiling, and
emits `invoke.define-bundle-admission-receipt.v1`. It collects every reachable
blocker and classifies semantic, authority, topology, projection, source,
schema, identity, and inventory drift. A PASS binds the submitted bundle
digest and the fixed thirteen-check inventory, with every check passing. The
source cannot supply producer or
validator identities, inventories, output hashes, receipt fields, or drift
claims.

Before authoring the source, follow the ownership-first procedure in the
[Define v3 authoring guide](./define-authoring-guide.md). In particular:

1. author semantic context and obtain independent current closure;
2. apply every `reuse-existing`, `new-scoped-term`, and
   `specialize-existing` disposition exactly;
3. author semantic fields, compute exact evidence fields, copy fixed contract
   constants, and omit producer/admission-owned fields;
4. complete every required nullable field and empty array, align all five
   voices, and close every relation inside the candidate registry;
5. compile from one source into a previously absent output directory;
6. run independent bundle admission outside that directory; and
7. submit the matching stage and admission receipts to capability resolution.

The canonical example is a real compiler input and may be used as a shape
reference. Its target semantics, evidence paths, hashes, and sizes must never
be copied into another source without recomputation and case-specific
justification.

A new Define artifact PASS requires both the digest-valid Invoke-owned v3 stage
receipt and the exact current admission PASS over the same producer binding and
bundle inventory. Together they open only the `artifact_authored` axis. They do
not release a registry, grant definition authority, promote a candidate, or
establish mutation-runtime readiness. Historical v1/v2 receipts remain
readable but cannot open a new PASS.

## Execution Phases

| Phase | Sigil                                                  | Input                                               | Output                                                                     | Gate                                                                 | Failure Policy                                                                   |
| ----- | ------------------------------------------------------ | --------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| 1     | `context-builder`                                      | user goal, known constraints, existing artifacts    | bounded semantic context                                                   | authority, registry, consumer, and evidence boundaries are explicit | block on missing core goal, hidden topology, or contradictory scope              |
| 2     | independent semantic closure validator                 | exact context and configured roots                  | current closure receipt with one disposition per concept                   | `ready-for-define`, no blockers, independent assessor                | collect all reachable blockers; route conflicts before authoring                 |
| 3     | `structured-interview-kits` / `inventory`              | bounded context and closure                         | resolved intent and v3 profile selection                                   | every meaning-bearing choice is explicit                            | block on unresolved semantic ambiguity or profile tie                            |
| 4     | `invoke define` v3 compiler                            | exact closure-bound source                          | complete thirteen-file candidate bundle and stage receipt                  | atomic publication, evidence, relations, views, identity, and no-effect invariants pass | leave output absent on any failure                                               |
| 5     | independent bundle admission validator                | exact submitted bundle and current repository       | typed admission receipt                                                     | clean replay equality and `overall: current`                         | emit collect-all BLOCK receipt for evaluated drift; no receipt on invocation failure |
| 6     | capability status resolver                            | matching stage and admission receipts               | `artifact_authored` PASS or BLOCK                                           | v3-only, exact producer/admission agreement                          | v1/v2, missing, stale, forged, mismatched, or non-current admission blocks       |
| 7     | optional `decision-gate` / lifecycle handoff           | unresolved blocker or admitted candidate            | decision record or bounded next-owner handoff                               | target and authority are explicit                                   | keep blocker open; never infer promotion or execution                            |

## Mode Gates

- Define must block on missing core goal or contradictory scope.
- Define must flag when no eligible template exists and candidate creation is unapproved.
- Template selection must include eligibility evidence and explicit user choice on tie cases.
- New production selects only `invoke.generic-definitions-baseline.v3`.
  Historical v1/v2 and named-template artifacts are compatibility-only and do
  not satisfy new PASS evidence.
- Define v3 requires an independent, current `ready-for-define` semantic closure
  before source authoring. Every registry/consumer membership, authority, source
  byte, selector, structural schema, or identity-denominator change invalidates
  the affected point-in-time evidence.
- Discovery-existence soft gate: define searches for a discovery artifact for the target scope; if none exists it halts with a recommendation to run discovery first. `--skip-discovery` is permitted but must write a `discovery_waiver_reason` into the spec frontmatter.
- Define mode may emit an implementation-layering seed; if skipped, it must record an explicit layering gap for downstream `plan`, `full`, and `validate` modes.
- Every definition remains `candidate`, cites exact repository-local source
  bytes, carries formal, operational, plain-language, and domain-context
  voices, and resolves its relations within the emitted registry.
- Source authoring follows `define-authoring-guide.md`; the JSON Schemas remain
  the final shape authority if prose and schema ever disagree.
- Admission must report current evidence, unchanged semantic/authority/topology/
  projection states, byte-identical clean replay, no differences, no blockers,
  and `authority_effect=none`.
- The semantic validator checks normalized term and alias uniqueness, local
  selector resolution, exact source size and SHA-256, public/private source
  boundaries, relation closure, and exact parity of both generated views.
- Candidate definition promotion is never automatic. The producer emits
  `authority_effect=none` and cannot write an authoritative registry.
- No silent upstream mutation; direct upstream edits require explicit approval.
- Define-stage transport appends stage reports and complements matching Necronomicon sections only when they already exist.
- Define mode must record a Dispatch Spec technique trace that names the techniques used to justify template selection, glossary routing, owner boundaries, and next route.
- Define mode runs a Distill sanity check when the target is broad, ambiguous, or split-prone; otherwise it records `not required` with rationale.
- A `flag` or `block` Distill result routes to clarification, definition split, or deferred follow-up; it must not be treated as plan readiness.
- Every Define result classifies identity-denominator validation as `required`
  or `not-applicable` with a rationale. It is `required` whenever a Define
  artifact asserts an exact or canonical ID-to-label denominator.
- A required identity-denominator gate uses
  `schemas/define-identity-denominator-request.schema.json` and
  `scripts/define_identity_denominator_validator.py`. Define cannot pass
  without a current passing `DefineIdentityDenominatorResult` bound to the
  exact request, artifact, declared authority source, optional corroborating
  sources, field mappings, equality filters, and exact coverage rule.
- The validator proves identity consistency against the caller-declared
  authority source; it does not grant that source authority. A missing or
  blocking required receipt stops Design and Plan activation rather than being
  reconstructed from counts, prose, or stable whole-file digests.

## Handoff Artifacts

- define context summary
- spec artifact path
- machine-readable candidate definition registry path (`DEFINITIONS.json`)
- deterministic definition view path (`DEFINITIONS.md`)
- deterministic glossary view path (`GLOSSARY.md`)
- implementation layering artifact path or explicit layering gap
- template selection evidence
- Dispatch Spec technique trace
- Distill validation status and rationale
- identity-denominator passing receipt, or a not-applicable classification and rationale
- Define v3 producer stage receipt and independent bundle admission receipt
- unresolved gaps and blocker decisions
- Necronomicon transport report
- recommended next route (`design`, `spellcraft`, `sigil-development`, or deferred follow-up)

## Mode Output Contract

Return:

```markdown
## Outcome Brief

<Two to five plain-language sentences explaining what Define tried to establish,
what it established or why it stopped, and why that matters.>

- Objective: <what Define was trying to accomplish>
- Result: <what is now defined, flagged, or blocked>
- Why it matters: <practical consequence for the operator or next owner>

## Boundary and Next Decision

- Changed: <definition artifacts, evidence, or state changed>
- Unchanged: <implementation, authority, promotion, publication, deployment, or other explicit boundaries>
- Open questions: <remaining uncertainty or none>
- User decision: <exact decision needed or none>
- Next action: <next bounded action and owner>

## Technical Details

## Invoke Result

- Mode: define
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass | flag | block
- Mode contract: spells/invoke/define.md
- Outputs: <spec path>, <DEFINITIONS.json path>, <DEFINITIONS.md path>, <GLOSSARY.md path>, <layering seed path or gap>, <transport report path>
- Template selection: <selected template or candidate recommendation>
- Dispatch techniques: <technique ids and rationale>
- Distill validation: not required | pass | flag | block; <rationale>
- Identity denominator validation: <passing receipt | not-applicable with rationale | block>
- Decisions: <summary>
- Unresolved gaps: <summary>
- Next route: design | spellcraft | sigil-development | deferred
```

## Evidence Capability Contract

Active define output must carry `producer_receipt`,
`producer_admission_receipt`, `execution_path`, `dispatch_trace`,
`template_selection`, `layering_or_gap`, `identity_denominator_validation`,
`result`, and `next_route` evidence. A conditional Distill skip or
identity-denominator not-applicable classification requires a rationale. A
triggered identity-denominator gate requires its exact passing receipt. New
PASS requires current v3 stage/admission agreement; validator results, not
authored handoff labels, control downstream readiness.
