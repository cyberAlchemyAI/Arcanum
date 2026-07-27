---
artifact: deterministic-context-compiler-architecture
status: design-validator-pass
design_evidence: design-only
plan_evidence: pending
lifecycle_owner: sigil-development
---

# Architecture: Deterministic Context Compiler

## Architecture Intent

Make Context Builder's mechanical evidence compilation reproducible and
cacheable while keeping semantic obligation formation, evidence sufficiency,
authority, and lifecycle decisions outside the deterministic kernel.

## Source Contracts

| Contract ID | Source | Required | Notes |
| --- | --- | --- | --- |
| SC-001 | `transmutations/context-builder/SKILL.md` | yes | canonical target behavior and authority boundary |
| SC-002 | `transmutations/context-builder/README.md` | yes | human-facing target contract |
| SC-003 | runtime handoff Markdown and JSON templates | yes | existing output compatibility |
| SC-004 | three public benchmark context indexes | yes | reproducibility evidence only |
| SC-005 | `SPEC.md` and `GLOSSARY.md` | yes | approved Define inputs |
| SC-006 | `WITNESS-CONTRACTS.md` | yes | planned, unexecuted validation contract |

## Closed Scope

- System of interest: `context-builder-deterministic-compiler`
- `DesignScopeManifest`: `DESIGN-SCOPE-MANIFEST.json`
  - input digest: `414222b2d0e5f227cc5d2d41ee8c09449f71ec156ea864c400ee06ff12692a33`
- `DesignDenominatorReceipt`: `DESIGN-DENOMINATOR-RECEIPT.json`
  - receipt digest: `d36b40b24b0a8b98c8b78d03b722757177e8c9fa614eb62e4c692760a43d0168`
- `DesignSelectionResult`: `DESIGN-SELECTION-RESULT.json`
  - result digest: `9f40868ef79b6fb16ef737c07fad313e17b37eb91d0be6c24de7c2a8e8858561`
- Fixed point: pass; pass-one and pass-two digest
  `ed7686812e887c61253c1778d6e07069fb5b16dff7a2b506cc65f74857c67ccb`

## View 1: Context View

```text
context author
    |
    | typed obligations + candidate mappings
    v
deterministic context compiler
    |                  \
    | one payload       \ pack and validation receipts
    v                    v
runtime adapter       session evidence
    |
    v
model/runtime

Inventory or other discovery read models may propose candidate handles.
Canonical source bytes remain the validation target.
Sigil Development owns contract mutation and reusable-behavior evidence.
```

The compiler is a local deterministic boundary. It does not call a model,
promote knowledge, or decide that an excerpt is semantically sufficient.

## View 2: High-Level Structure View

| Component | Responsibility | Authority |
| --- | --- | --- |
| Request Validator | Validate obligation IDs, candidate mappings, policies, and output request. | structural only |
| Source Snapshotter | Resolve in-root paths/selectors and bind current bytes. | current-byte evidence |
| Excerpt Normalizer | Produce versioned selector-level bytes. | transformation only |
| Content-Addressed Store | Reuse exact excerpt objects and manifests. | non-authority generated read model |
| Covering-Set Selector | Apply deterministic filtering, deduplication, cost comparison, and tie-breaking. | follows authored mappings; no semantic authority |
| Pack Renderer | Emit stable Markdown, JSON/index, payload, and receipt bytes. | projection only |
| Pack Validator | Verify coverage, parity, hashes, budgets, and blocker semantics. | validation evidence |
| Runtime Adapter | Inject one payload and return actual runtime usage when available. | transport only |

## View 3: Low-Level Components View

### Request Validator

Inputs:

- `context-request.v1.json`;
- compiler-policy version;
- repository root;
- optional tokenizer ID;
- optional base-pack receipt.

Checks:

- schema and stable ID uniqueness;
- every candidate maps to at least one obligation;
- every required obligation has at least one declared candidate before source
  validation;
- budget units are declared as bytes or a named tokenizer;
- output paths remain within the declared evidence/cache roots.

### Source Snapshotter

For each candidate:

1. normalize the repository-relative path;
2. reject absolute, escaping, missing, or non-file targets;
3. resolve the selector through a versioned selector resolver;
4. reject zero or multiple matches unless the selector contract explicitly
   permits a bounded set;
5. hash source bytes and normalized excerpt bytes;
6. emit a selector snapshot.

### Excerpt Normalizer

Normalization is versioned and format-specific. L0 supports exact Markdown
heading ranges and explicit whole-short-file selectors. Code symbols, JSON
pointers, table rows, and config keys are later admitted selector adapters.

Normalization must preserve material bytes. Whitespace or line-ending changes
are allowed only when the policy version declares them and the receipt records
the normalized digest separately from the source digest.

### Content-Addressed Store

Proposed consumer layout:

```text
<consumer-root>/.arcanum/cache/context-builder/
  objects/<object-sha256>
  manifests/<request-sha256>.json
  receipts/<pack-sha256>.json
```

Object key material:

```text
schema version
+ normalizer version
+ source digest
+ selector
+ excerpt policy
+ privacy/public-boundary policy
+ normalized excerpt digest
```

The store is rebuildable and disposable. Session evidence does not point to a
cache object as its sole source reference.

### Covering-Set Selector

Inputs are already semantically mapped candidates. The deterministic selector:

1. removes invalid candidates;
2. collapses byte-identical excerpt objects and unions obligation refs;
3. maintains the set of uncovered obligations;
4. compares candidates by uncovered coverage divided by effective cost using
   integer cross-multiplication;
5. breaks ties by authority rank, ambiguity rank, cost, normalized path,
   selector, and excerpt digest;
6. selects until coverage is total or no candidate remains;
7. enforces file and payload budgets; and
8. emits excluded candidates with exact reasons.

Effective cost begins with bytes. A named tokenizer may replace or supplement
that unit, but the receipt must not label byte estimates as exact tokens.

### Pack Renderer And Validator

The renderer owns stable ordering and canonical JSON. The validator recomputes:

- request and source snapshot hashes;
- selected object hashes;
- coverage and budget totals;
- Markdown/JSON/payload parity;
- output hashes;
- base-pack proof when a delta is requested.

The runtime adapter consumes exactly one payload hash. Persisting both Markdown
and JSON does not imply sending both.

## View 4: Workflow Process View

```text
validate request
  -> resolve and snapshot candidates
  -> cache lookup
     -> exact hit: reuse bytes
     -> miss/stale/corrupt: rebuild or block
  -> deduplicate
  -> select covering set
     -> uncovered/over budget: block
  -> render pack pair + one runtime payload + receipt
  -> validate parity and hashes
     -> mismatch: block
  -> optional runtime handoff
     -> full payload by default
     -> delta only with proved base
  -> record actual usage or unknown
```

Failure is fail-closed for correctness boundaries. Cache absence is degraded
performance, not a correctness failure, when current-source rebuild succeeds.

## View 5: Decision Flow View

| Decision | Rule | Result |
| --- | --- | --- |
| Can a candidate enter selection? | path and selector are exact, current, in-root, and policy-admitted | admit or block candidate/request |
| Can cache bytes be reused? | complete key and object bytes recompute exactly | hit or rebuild |
| Which candidate is next? | deterministic coverage/cost comparison and stable tie-break | one selected candidate |
| Is the pack runnable? | all obligations covered, budgets pass, outputs agree | pass or block |
| Can a delta be sent? | runtime receipt proves exact base pack | delta; otherwise full |
| Can token savings be claimed? | paired actual runtime receipts and coverage parity exist | measured claim; otherwise hypothesis |
| Can the canonical sigil change? | Sigil Development approves scope and reusable evidence | lifecycle decision outside compiler |

## View 6: Dependency Interface View

| Interface | Contract | Dependency Rule |
| --- | --- | --- |
| Request JSON | versioned schema | reject unknown required semantics; additive optional fields require version policy |
| Candidate source | repository-relative path, selector, digests | source bytes outrank cache and Inventory |
| Inventory lookup | candidate handles and source refs | read model may seed; never approve or prove freshness |
| Cache filesystem | content-addressed objects and atomic receipts | rebuildable, consumer-local, non-authority |
| Markdown/JSON templates | current Context Builder output concepts | compiler extension preserves obligation, blocker, provenance, and output-path semantics |
| Runtime adapter | one payload hash plus optional usage/base receipts | adapter cannot lower compiler block or invent usage |
| Experiment Harness | paired fixtures and live examples | validates reusable behavior; does not promote the sigil |
| Sigil Development | approved change scope and lifecycle receipts | owns canonical mutation and promotion readiness |

## Significant Behavior Scenario

| Stimulus | Preconditions | Ordered Response | Failure/Recovery | Observable Evidence | Acceptance Owner |
| --- | --- | --- | --- | --- | --- |
| compile a typed request | current source bindings, mapped candidates, policy | validate, snapshot, cache, dedupe, select, render, validate | stale or uncovered input blocks; corrupt cache rebuilds from current bytes | pack pair, payload hash, compile receipt | Sigil Development |
| rerun identical request | identical compiler/policy/source bytes | repeat the same ordered operations | any changed output is deterministic-replay failure | identical object, pack, and receipt hashes | Experiment Harness |
| request delta payload | exact base-pack receipt supplied | validate base then render delta | missing/stale base causes full payload or strict block | base and delta receipt bindings | runtime adapter owner |

## Concern-To-View Trace

| Concern | Class | Disposition | Owners | View Or Extension |
| --- | --- | --- | --- | --- |
| `concern:persistence` | persistence | required | persistence owner; architecture/work-pack contributors | content-addressed store and writer rules |
| `concern:integration` | integration | required | interface owner; architecture/work-pack contributors | request, output, runtime adapter compatibility |
| `concern:privacy-data` | privacy-data | required | data owner; architecture/work-pack contributors | receipt minimization and retention |
| `concern:performance` | performance | recommended | service owner; architecture/work-pack contributors | planned paired measurement only |
| `concern:ux` | ux | not applicable with rationale | UX plan owner | no changed human semantic surface |
| `concern:validation` | validation | required | design owner; architecture/work-pack contributors | witness and validator contracts |

## Persistence And Concurrency Extension

- One compiler process owns one manifest write.
- Object creation uses temporary files plus atomic rename.
- Existing matching object bytes are immutable and reusable.
- A matching key with mismatching bytes is corruption and blocks reuse.
- Concurrent writers may race only to create identical objects; manifest
  publication remains serialized.
- Cache cleanup is outside the first implementation layers and cannot delete
  session evidence.

## Integration And Versioning Extension

- Schema, normalizer, selector adapter, renderer, and receipt versions are
  explicit cache-key inputs.
- Unknown major versions block.
- Existing Context Builder output remains valid without the compiler.
- Compiler-assisted output is optional until Sigil Development changes the
  canonical contract.
- Runtime adapters declare which payload schema they accept.

## Data Lifecycle Extension

- Public receipts contain paths, selectors, hashes, counts, statuses, and
  bounded summaries; they do not persist unnecessary raw request text.
- Excerpt objects follow the consumer repository's privacy boundary.
- Cache retention is consumer-owned and may be disposable.
- Session evidence retention remains separate from cache retention.
- Telemetry records counts and digests rather than excerpt bodies.

## Planned Witness Contracts

See `WITNESS-CONTRACTS.md`. Every witness is unexecuted and begins Plan at
`plan-evidence-pending`.

## Constraints

| Constraint | Source | Impact |
| --- | --- | --- |
| Cache is non-authority | Define decision D-003 | always revalidate current source bindings |
| Public package is generic | repository boundary | no consumer-private fixtures or paths |
| Token savings are unproven | current evidence | performance output remains recommended |
| Context Builder strict coverage remains | canonical sigil | compiler cannot trade coverage for cost |
| Plan cannot pre-generate execution packs | Invoke Plan | execution-time Context Builder packs remain session evidence |

## Dependency And Interface Rules

| Rule ID | Rule | Applies To | Enforcement |
| --- | --- | --- | --- |
| R-001 | Current source bytes outrank cached bytes. | snapshot/cache | digest validation |
| R-002 | Candidate mappings must pre-exist deterministic selection. | request/selector | request schema |
| R-003 | One excerpt object may cover many obligations but appears once. | selector/renderer | parity fixture |
| R-004 | Persisted formats may be multiple; injected payload is exactly one. | renderer/adapter | payload receipt |
| R-005 | Missing tokenizer or runtime usage stays unknown. | usage receipt | schema and negative fixture |
| R-006 | Base/delta reuse requires an exact runtime base receipt. | adapter | base proof validator |
| R-007 | Compiler evidence cannot promote the target sigil. | lifecycle | owner boundary review |

## Decision Log

| ID | Status | Decision | Alternative Rejected | Revisit Trigger |
| --- | --- | --- | --- | --- |
| AD-001 | accepted | Typed semantic manifest precedes deterministic compilation. | Fully deterministic prose interpretation. | A separately validated typed-intent owner exists. |
| AD-002 | accepted | Cost-aware deterministic selector with explicit non-optimality ceiling. | Claim global minimum without an exact solver. | Exact solver proves bounded optimality worth its cost. |
| AD-003 | accepted | Filesystem content-addressed store is the first persistence design. | Database or service dependency in L0. | Concurrency or scale evidence exceeds filesystem model. |
| AD-004 | accepted | Bytes are the default cost unit. | Approximate tokens labeled exact. | A supported tokenizer is declared and validated. |
| AD-005 | accepted | Full payload is the default runtime transfer. | Unproved delta/base references. | Runtime supplies stable base-pack receipts. |
| AD-006 | accepted | Compiler is optional until lifecycle evidence exists. | Immediate canonical replacement. | Sigil Development approves validated behavior change. |

## Risks

| ID | Risk | Mitigation | Owner |
| --- | --- | --- | --- |
| RK-001 | Semantically bad candidate mappings compile perfectly. | keep semantic author and coverage review outside kernel | context author |
| RK-002 | Cache key omits a material policy input. | versioned key schema and negative mutants | compiler validator owner |
| RK-003 | Stable output hides stale source. | per-source and per-excerpt current hashes | snapshot validator owner |
| RK-004 | Token estimates are mistaken for runtime usage. | separated receipt fields and evidence sources | experiment owner |
| RK-005 | Cache leaks consumer-private excerpt bodies. | consumer-local storage, bounded retention, public fixture scan | data owner |
| RK-006 | Selection policy reduces cost by dropping authority context. | authority rank precedes cost and strict coverage remains | design owner |

## Downstream Planning Notes

- Start with schema/canonicalization and one exact selector proof.
- Keep selector adapter expansion, token plugins, delta reuse, and cache cleanup
  out of the first SWU.
- Split implementation into independently verifiable SWUs.
- Do not select an SWU during Invoke Plan.
- Route implementation through Sigil Development, then Task Session.

## Design Transport Notes

The Design result proves the selected architecture and planned validation
contracts only. It does not prove the fixtures, compiler, cache, runtime
adapter, token savings, or lifecycle readiness.

## Gate Result

- Status: pass
- Reason: six views are present; deterministic scope, denominator, ownership,
  selection, and fixed-point checks pass; required extensions are authored;
  performance and UX evidence ceilings remain honest.
