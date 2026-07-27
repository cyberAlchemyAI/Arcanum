---
template_id: invoke.sigil
target_sigil: context-builder
status: ready-for-design-and-plan
lifecycle_owner: sigil-development
---

# Sigil Handoff: Context Builder Deterministic Compiler

## Sigil Identity

- Name: `context-builder`
- Purpose: compile bounded, obligation-linked task context from selected evidence
- Owning surface: `transmutations/context-builder/`
- Target extension: deterministic compilation and non-authority excerpt reuse

## Inputs

| Input | Required | Validation Rule |
| --- | --- | --- |
| Context request manifest | yes | schema-valid, stable obligation IDs |
| Evidence candidates | yes | each maps to at least one obligation |
| Repository root | yes | normalized and explicit |
| Source and selector bindings | yes | readable, in-root, digest-current |
| Compiler policy | yes | versioned budgets, normalization, ordering |
| Tokenizer configuration | no | named when exact token counts are emitted |
| Runtime base-pack receipt | no | required before delta payload emission |

## Outputs

| Output | Consumer | Contract |
| --- | --- | --- |
| Excerpt objects | compiler/cache | content-addressed and non-authoritative |
| Context pack Markdown | human reviewer | obligation-linked session evidence |
| Context index JSON | validators/adapters | exact selected-source and blocker projection |
| Compact runtime payload | runtime adapter | exactly one admitted representation |
| Pack receipt | Task Session and lifecycle owner | hashes, counts, cache state, validation |
| Runtime usage receipt | evidence review | actual usage when the runtime supplies it |

## Modes

| Mode | Trigger | Behavior |
| --- | --- | --- |
| compile | typed request available | validate, snapshot, select, render, receipt |
| validate | pack or cache object available | verify schemas, hashes, coverage, parity |
| inspect | human review requested | explain selected/excluded candidates without mutation |

These are proposed compiler modes. They do not change the canonical sigil flags
until Sigil Development approves and validates that contract update.

## Runtime Adapter Expectations

| Expectation | Required | Notes |
| --- | --- | --- |
| Inject one payload | yes | do not send both persisted Markdown and JSON |
| Return prompt usage | no | mark unavailable rather than estimate |
| Prove base pack before delta | yes | otherwise use the full payload |
| Preserve blockers | yes | adapter cannot lower compiler `block` |
| Keep cache non-authoritative | yes | current source validation remains mandatory |

## Observability

| Signal | Trigger | Payload Summary |
| --- | --- | --- |
| compile-result | every meaningful compile | status, coverage, selected/excluded counts |
| cache-result | cache lookup | hits, misses, stale/corrupt objects |
| payload-result | runtime handoff | selected representation and payload hash |
| token-result | declared tokenizer or runtime receipt | tokenizer ID, measured count, actual count or unknown |
| determinism-result | replay fixture | first and repeated output hashes |

## Validation Examples

| Example | Expected Result |
| --- | --- |
| exact single selector | pass and byte-identical replay |
| duplicate excerpt for two obligations | one object, two obligation refs |
| changed selected source | cache miss and new pack |
| changed unrelated source | unchanged pack |
| ambiguous selector | block |
| missing tokenizer | byte counts present, token count unavailable |
| unproved base pack | full payload |

## Sigil-Development Handoff

- Handoff status: ready after Design and Plan gates pass
- Handoff notes: Invoke owns only this authoring package. Sigil Development
  decides whether to mutate the canonical contract, initialize the experiment
  harness, and prepare reusable-behavior evidence.

## Gate Result

- Status: pass
- Reason: target identity, purpose, inputs, outputs, runtime expectations,
  observability, validation examples, and lifecycle owner are explicit.
