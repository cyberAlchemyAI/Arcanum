# Dispatch Spec Design

## Invoke Design Result

- Mode: `design`
- Spell: `invoke`
- Target artifact: `dispatch-spec`
- Target type: draft Formulae sigil package
- Phase status: `pass`
- Mode contract: `spells/invoke/design.md`
- Template/profile selection: lightweight Formulae architecture bundle with six required views.
- Work-pack: n/a
- Next route: `task-session` for validator implementation, then `experiment-harness`.

## 1. Context View

`dispatch-spec` sits between Arcanum route interpretation and lifecycle execution.

```text
operator sentence
  -> Necronomicon / Invoke / Spellcraft proposes dispatch document
  -> dispatch-spec validates document structure
  -> owner capability executes or authors next artifact
  -> Observed Invocation Loop groups results by dispatch_id
  -> Workflow Reflect can evaluate route quality later
```

The package is intentionally a Formulae validator. It does not choose the route, execute sigils, promote knowledge, or mutate registries.

## 2. High-Level Structure View

```text
formulae/dispatch-spec/
  README.md
  SKILL.md
  dispatch.schema.json
  WEAVER-EXTRACTION.md
  ARCANUM-DISPATCH-SYNTHESIS.md
  development/
    DEFINE.md
    GLOSSARY.md
    IMPLEMENTATION-LAYERING-SEED.md
    DEFINE-TRANSPORT.md
    DESIGN.md
    GLOSSARY-CONSISTENCY.md
    DESIGN-TRANSPORT.md
```

Responsibilities:

| Component | Responsibility |
| --- | --- |
| `README.md` | Human-facing package purpose, Weaver mapping, and integration target. |
| `SKILL.md` | Runtime-facing Formulae contract for validation behavior. |
| `dispatch.schema.json` | Machine-readable dispatch document structure. |
| `WEAVER-EXTRACTION.md` | Evidence extraction from external Weaver contract repository. |
| `ARCANUM-DISPATCH-SYNTHESIS.md` | Arcanum taxonomy, sentence grammar, and example route patterns. |
| `development/*` | Invoke define/design evidence and future handoff context. |

## 3. Low-Level Components View

### Dispatch document

Core fields:

- `dispatch_id`
- `parent_dispatch_id`
- `intent`
- `mode`
- `route_menu`
- `steps`
- `gates`
- `observability`
- `promotion_guardrails`

### Step model

Each step names:

- `step_id`
- `capability_ref`
- `pattern`
- `inputs`
- `outputs`
- optional `parallel`
- optional `roles`
- optional `join_policy`
- optional `convergence_criteria`
- optional `evidence_artifact`
- optional `stop_conditions`

### Gate model

Each gate names:

- `gate_id`
- `kind`
- `owner`
- `condition`
- `on_fail`

Gate kinds currently include policy, decision, quality, promotion guardrail, validation, and human approval.

## 4. Workflow Process View

```text
1. Capture raw operator intent.
2. Extract Arcanum vocabulary and candidate capability references.
3. Build a bounded route menu when route choice is ambiguous.
4. Produce selected dispatch steps with explicit inputs and outputs.
5. Attach gates, stop conditions, and observability requirements.
6. Validate the dispatch document against schema and Formulae rules.
7. If pass, hand off to owning capability.
8. If flag, allow bounded execution only with named gaps.
9. If block, route to decision-gate, Invoke repair, or Spellcraft/Sigil Development owner.
```

## 5. Decision Flow View

| Decision | Rule |
| --- | --- |
| Is this a single obvious sigil? | Skip dispatch-spec unless a reusable artifact or audit graph is needed. |
| Is the route ambiguous? | Use route menu / ChoiceCard-like selection before steps. |
| Is there a blocker route decision? | Route to `decision-gate` before validation or execution. |
| Is the sequence intended to become reusable? | Route to `spellcraft` after dispatch validation. |
| Does a step need implementation work? | Route to `task-session`, not dispatch-spec. |
| Does the dispatch claim promotion authority? | Block. Promotion belongs to owning lifecycle. |
| Are sibling steps parallel or tournament lanes? | Require `dispatch_id`, `join_policy`, and convergence criteria. |

## 6. Dependency Interface View

| Interface | Producer | Consumer | Contract |
| --- | --- | --- | --- |
| Operator sentence | User / Necronomicon / Invoke | route proposer | Free-form text plus intent fields |
| Route menu | Necronomicon / Spellcraft / Invoke | operator or LLM | Bounded selectable items |
| Dispatch document | route proposer | `dispatch-spec` | `dispatch.schema.json` |
| Validation result | `dispatch-spec` | Necronomicon / Spellcraft / Task Session | pass/flag/block report |
| Step frames | executed sigils/spells | later dispatch steps | safe summaries / structured data |
| Artifact handles | executed sigils/spells | later dispatch steps or human | controlled refs |
| Trace events | observed invocation loop | signal observer / workflow reflect | `dispatch_id`, `step_id`, outcome |

## Risks

| Risk | Mitigation |
| --- | --- |
| Schema becomes an execution engine by accident. | Keep Formulae boundary explicit: validate only. |
| Pattern enum becomes too rigid. | Treat starter patterns as L0; future schema can add extension metadata. |
| Dispatch bypasses owner lifecycles. | Promotion guardrail blocks false authority claims. |
| Operator language loses its expressive value. | Preserve operator sentence while extracting structured vocabulary. |
| Telemetry grouping is designed but not implemented. | Keep as integration gap until observed invocation loop changes. |

## Plan-Ready Handoff

Recommended next execution slice:

```text
task-session: implement a deterministic validator script and fixtures for dispatch.schema.json
```

Acceptance evidence:

- schema validation command passes,
- pass fixture validates,
- block fixture fails with clear reason,
- SKILL output contract can be generated from validator result.

