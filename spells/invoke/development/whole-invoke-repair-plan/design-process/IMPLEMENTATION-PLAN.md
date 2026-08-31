# Invoke Design Production Process — Implementation Plan

## Objective

Implement `SWU-WIR-007` through a machine-first, coherence-preserving Design
artifact chain. This plan refines only the Design unit inside the existing
Whole-Invoke repair and does not change its global execution designation.

## Ordered Waves

| Wave | Layer | Scope | Outputs | Stop condition |
| --- | --- | --- | --- | --- |
| W0 | L0 | Process and schema family | Process definition, twenty-two current/historical schemas, canonical process/profile/policy instances, schema fixtures, structural tests. | Any schema overlap, invalid meta-schema, missing binding, or unresolved authority. |
| W1 | L1 | Input closure and scope projection | Boundary approval, input producer/validator, manifest projection, failure-capable atomic receipt, real fixtures. | Missing/stale input, coverage inequality, unresolved conflict, or public/private violation. |
| W2 | L2 | Design source and semantic coherence | Public profile, canonical source, deterministic candidate projector, independent coherence validator, failure-capable atomic candidate receipt, and fixtures. | Cross-view conflict, unbound input, illegal supersession, selection mismatch, or incomplete predecessor evidence. |
| W3 | L3 | Atomic production and admission (implemented) | Bundle closure, compiler, deterministic projections, v2 stage receipt, independent replay admission, resolver hardening, and genuine predecessor consumption. | Partial output, producer drift, wrong inventory, non-passing Distill evidence, replay mismatch, or consumer rejection. |
| W4 | L4 | Compatibility and package closure | Historical readers, selective mirror sync, aggregate evidence, Design-slice receipt. | Unexpected mirror delta or acceptance-critical regression. |

## Current Implemented Slice

W1, W2, and W3 are implemented. `design-result-v1` remains historical and
byte-preserved; only `design-result-v2` can establish a new Design stage PASS.
W3 adds exact W2/Distill closure, deterministic fifteen-file publication,
external clean-replay admission, Design-specific resolver enforcement, and
real v2 predecessor consumption. Generated mirrors and W4 aggregate closure
remain untouched.

## W1-W3 Done Criteria

- All twenty-two Design schemas validate under JSON Schema Draft 2020-12.
- A real Define v2 normal activation and an approved discovery activation pass.
- The compiler publishes the exact five-file W1 family atomically and produces
  byte-identical outputs on a second run.
- Governed failures leave the success directory absent and issue one valid,
  complete attempt receipt; malformed invocation returns exit `2` without a
  fabricated receipt.
- The unchanged Design selection corpus and focused Define v2 regressions pass.
- Protected consumer and Define hashes remain unchanged; generated Invoke
  package preview is not applied and every non-Design delta is reported as a
  synchronization blocker.
- One canonical source applies the complete W1 denominator, projects every W1
  signal field into the public profile, and indexes one fact registry into six
  legal ID-only views.
- An independent validator evaluates the exact twelve-rule installed coherence
  policy and rejects wrong edges, false N/A, selection drift, witness overclaim,
  contract drift, and evolution without a real final predecessor receipt.
- The W2 compiler publishes exactly the candidate, coherence receipt, and
  candidate production receipt atomically; governed failures publish no success
  directory and issue only the separate attempt receipt.
- The W3 compiler publishes exactly fourteen ordered payloads plus the v2 stage
  receipt; clean repeat runs are byte-identical.
- Non-passing or provenance-incomplete Distill evidence leaves the success
  directory absent and issues the block-only W3 attempt receipt.
- Independent admission replays from the bound closure, requires byte equality,
  leaves the submitted bundle unchanged, and opens only `artifact_authored`.
- One real W3 v2 bundle is consumed successfully by a fresh W1/W2 evolution
  run; v1, fake, ambiguous, and mismatched predecessors block.

## Evidence Ceiling

W1 proves approved-boundary-relative input closure, deterministic manifest
projection, denominator compatibility, fixed-point selection, and atomic W1
output closure. W2 additionally proves exact W1-bound authored application,
lossless signal projection, installed-profile candidate coherence, independent
policy validation, deterministic projection, and atomic candidate closure. W3
adds complete deterministic bundle production, exact Distill binding,
independent replay admission, and genuine v2 predecessor evidence. It does not
prove repository-global semantic completeness, mirror parity, Plan evidence,
registry release, mutation readiness, acceptance, execution, publication,
deployment, or external effect.
