# Distill v2 Machine Contract — Implementation Layering

- Target: canonical public Distill semantic machine contract
- Complexity: high
- Execution designation: `blocked-before-execution-candidate`
- Authority effect: `none`

## Control Gate Before L0

The existing Decision Gate admits alternatives but does not select one. It also
describes a five-schema family that is now known to be incomplete: modes,
techniques, and shared primitives need independent contracts. Before any
canonical schema byte is authored, the Distill semantic-contract owner must
freeze the amended eight-schema surface and the decisions in
`SCHEMA-PLAN.md#owner-decision-freeze`.

No layer is executable while that gate is open.

## Layer Boundary Heuristic

Each layer ends when it proves a new operator-visible decision through a real
vertical. A schema-shaped file without a concrete instance and a rejecting
consumer is not a working layer.

| Layer | Decision question | Minimum working unit | Included SWUs | Deferred scope | Exit evidence | Promotion decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 — machine grammar | Can each of the eight document kinds be represented and can malformed structures be rejected? | Eight Draft 2020-12 schemas, each with positive and mutation-negative fixtures; no complete-run or executable-semantics claim. | SWU-DV2-001–007 | Complete technique/mode catalogs, profile/source composition, semantic finalization, adapters. | Schema meta-validation and per-schema positive/negative fixtures PASS with repository-local `$ref` closure. | Promote only as representational grammar; do not claim a usable run family. |
| L1 — catalog and input closure | Do five finite modes, eleven phase-bound techniques, one exact profile, and one normalized RunFrame form a single configuration authority? | Eleven technique instances, five mode instances, exact profile composition, normalized Standard source, and cross-reference validation. | SWU-DV2-008–023 | Semantic result finalization and external adapters. | Every instance validates; exact profile → mode/technique → source bindings close; budget, hook, skip, and input negatives reject. | Promote only when the profile is the composition authority and the source binds exactly one profile. |
| L2 — semantic production closure | Can semantic candidates be validated, rendered, and published atomically without the finalizer inventing meaning? | Cross-artifact semantic validator plus deterministic Markdown renderer/finalizer and self-consistent stage receipt. | SWU-DV2-024–025 | Direct and Invoke consumers, generated mirrors. | Semantic invariant matrix PASS; repeated finalization is byte-identical; invalid input publishes nothing. | Promote only when source, profile, trace, result, Markdown, and receipt form one digest-bound family. |
| L3 — consumer, compatibility, and package closure | Can direct Distill and separately owned Invoke projections consume the same family while public/native surfaces remain deterministic and authority-safe? | Direct no-effect run, versioned Invoke/runtime/telemetry projections, compatibility reads, deterministic docs/native preview, public scan, and fresh lab. | SWU-DV2-026–028 | Publication, release, deployment, and external rollout. | Direct/invoked laboratory PASS, historical-read PASS, link/schema/semantic/parity denominators PASS, changed-byte inventory closed. | Final promotion remains a separate owner decision; cross-owner Invoke writes require their own acceptance. |

## Non-Regression Guarantees

- Distill owns semantic source, policy, trace, result, deterministic human
  projection, and stage receipt; Invoke owns invocation/evidence/handoff adapters.
- Modes alter bounded orchestration only. Techniques retain stable semantics and
  phase hooks. Profiles compose exact references and do not redefine either.
- `authority_effect` remains `none`; a Distill verdict cannot grant acceptance,
  selection, admission, execution, publication, or deployment.
- Existing Invoke adapter schemas remain compatibility-read surfaces until their
  owner selects a versioned replacement.
- Invalid input or a failed consumer produces no partial final bundle.
- Generated native packages change only after canonical tests and through the
  selective Distill synchronization path.

## Recommended Next Layer

No implementation layer yet. First freeze the amended owner decision. After a
selected and independently reviewed decision record exists, begin L0 with
SWU-DV2-001: one canonical TechniqueSpec slice with common primitives,
`abstraction_level_guard`, and its positive/negative runner. Stop at each SWU receipt.
