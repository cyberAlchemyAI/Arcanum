# Local Define: Dispatch Boundary/Evidence Schema

Status: flag
Owner: refine fallback synthesis
Reason: `invoke define` command surface resolved, but model-backed stage execution was blocked by `codex-exec-timeout`.

## Definition

The boundary/evidence schema is an optional `boundary_evidence` object inside a
dispatch document. It describes how a route preserves composition integrity
when work crosses capability, artifact, human, memory, state, or evidence
boundaries.

It is not an execution engine. It does not grant lifecycle, runtime, memory, or
promotion authority. It only makes boundary claims inspectable.

## Core Terms

| Term | Meaning |
| --- | --- |
| Boundary | A declared crossing between owners, artifacts, state namespaces, evidence surfaces, or approval semantics. |
| Authority | The capability or role allowed to decide lifecycle, execution, validation, evidence acceptance, memory, or promotion. |
| Receipt | A structured return record that proves what happened, where the evidence lives, and what remains unresolved. |
| State namespace | A named state root or class, such as repository source, generated evidence, `.arcanum/` observability, or external workspace state. |
| Promotion split | A rule that prevents evidence visibility from becoming canonical knowledge promotion. |

## Non-Goals

- No Tandem-specific integration.
- No runtime adapter registry.
- No automatic execution.
- No automatic Inventory, Ontology, sigil, or spell promotion.
- No replacement for `steps`, `gates`, `observability`, or `promotion_guardrails`.

## Success Criteria

- Dispatch authors can declare authority owners without prose-only ambiguity.
- Validator can block impossible or unsafe boundary claims.
- Existing dispatch documents remain valid when `boundary_evidence` is absent.
- The technique catalog can migrate away from runtime-specific language.
