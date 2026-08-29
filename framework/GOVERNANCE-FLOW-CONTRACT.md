# Governance Flow Contract

Status: candidate

## Purpose

This contract keeps strict governance protections while preventing deterministic,
no-effect validation defects from becoming a sequence of human approval requests.
It defines one monotonic artifact chain and three execution modes for governed work.

The contract is project-agnostic. Adoption by a capability, repository, or runtime
requires a separate owner decision over its exact integration bytes.

## Core Terms

- **Machine source**: the schema-valid, model-produced source of governance intent.
- **Decision graph**: the normalized immutable envelope derived from the machine
  source. Human prose is never an authority source.
- **Human view**: a deterministic projection of the decision graph that binds the
  exact source, graph, and renderer digests.
- **Rehearsal**: deterministic execution of every reachable declared consumer under
  a no-effect ceiling. Only isolated run-local evidence may be written.
- **Terminal outcome contract**: the frozen predicate that decides aggregate
  completion after effectful execution.
- **Bounded slice**: the smallest complete vertical slice that traverses every
  required real consumer and can reach its promised terminal boundary without
  unrelated scope.

## Preserved Decision Envelope

One decision graph binds every field whose change can alter owner intent or the
accepted risk. At minimum it contains:

- exact target baselines and postimages;
- owner identity and lifecycle route;
- authority, write, risk, and request ceilings;
- public/private and publication classification;
- Git, deployment, credential, destructive-action, and external-effect policy;
- authority-bearing executable path, digest, arguments, mode, working directory,
  and environment allowlist;
- independent-review requirement and reviewer separation;
- selection, admission, terminal outcome, and successor policy.

Non-authoritative run identifiers, timestamps, and replaceable mechanical evidence
are descendants, not members of the decision envelope. They may be replaced only
when machine checks prove the decision graph and target-byte digests unchanged.

## Monotonic Artifact Chain

The only forward order is:

```text
machine source
  -> normalized decision graph
  -> rehearsal
  -> freeze
  -> independent review
  -> owner request
  -> acceptance
  -> selection and admission
  -> effectful execution
  -> terminal receipt
```

Every descendant binds its exact predecessor digest and the decision graph digest.
A source, target-byte, or decision-envelope change makes all older descendants stale.
No receipt may rebind backward to different bytes.

Compilation, rendering, rehearsal, freeze, review, and request emission are
preparation. Preparation grants no selection, admission, execution, publication,
deployment, Git, credential, destructive-action, successor, or external-effect
authority.

## Mode 1: Preacceptance / No Effect

Preacceptance validates the machine source, derives the graph and human view, and
rehearses every declared consumer in isolation.

- Run all reachable checks even after ordinary failures.
- Preserve the first nonzero status as the process result while retaining the full
  ordered blocker set.
- Mark a dependency-blocked check `not_evaluable` with its exact causal blockers;
  never report it as PASS or omit it.
- Continue bounded environmental retries and independently reviewed mechanical
  evidence-only repairs automatically while their predicates and budgets hold.
- Stop when safe evaluation is impossible or a semantic or authority decision is
  required.
- Complete only when all required consumers pass, none is `not_evaluable`, the
  blocker set is empty, repeated derivation is byte-stable, and protected inputs are
  unchanged.

The only permitted writes are declared isolated run-local evidence. Repository
targets, owner decisions, credentials, external systems, publication, deployment,
and successors remain untouched.

## Mode 2: Human Decision

Human-decision mode begins only after a zero-blocker rehearsal, graph freeze, and
passing independent review.

- Persist request identity by `decision_graph_digest`.
- Emit at most one prompt event and one request identity for that immutable graph.
- A duplicate emission returns the original schema-valid request bytes.
- Stop immediately after presenting the request or returning its existing identity.
- Continue only from an exact accept or reject response bound to that request.
- A requested revision creates a new source and graph; it never mutates the frozen
  graph in place.

The request itself grants no downstream authority.

## Mode 3: Effectful Execution

Effectful execution begins only after exact acceptance, selection, and admission.

- Execute only the accepted target, write, risk, executable, and effect envelope.
- Verify exact target baselines immediately before the first effect.
- Fail fast on the first failed effect or governance blocker.
- Prove that no later effect or successor ran after failure.
- Never infer publication, deployment, credential, destructive, Git, external, or
  successor permission from general execution acceptance.

The mode completes only when the promised terminal receipt validates and its terminal
predicate is true.

## Terminal Outcome Dominance

A component PASS is local evidence only. Aggregate completion is false until the
required terminal receipt proves all of the following:

- the promised boundary identifier is exact;
- required effects and exact postimages occurred;
- prohibited effects and successors did not occur;
- the observer and authority/write ceiling match the frozen graph;
- the monotonic predecessor chain is current; and
- the completion predicate is true.

A schema-valid receipt for the wrong boundary, effect set, postimage, observer, or
successor state is not terminal completion.

## Retry Classification

Retry class is a machine decision, never a prose judgment.

| Class | Predicate | Action | Owner request |
| --- | --- | --- | --- |
| `environmental` | Decision graph, target bytes, semantic inputs, evidence schemas, and authority-bearing executable are unchanged; the failure is a declared transient runtime condition. | Retry within the frozen budget and record every attempt. Exhaustion blocks. | None. |
| `mechanical_evidence_only` | Only validation, wrapper, locator, formatting, or receipt mechanics change; exact consequential digests remain unchanged. | Independently review the repair, revalidate, and resume once at the recorded continuation point. | None. |
| `semantic_or_authority` | Any target, terminal effect, owner, route, risk, write, privacy, publication, deployment, credential, external-effect, successor, or executable-authority field changes. | Supersede the chain, compile and rehearse a new graph, and request one decision for it. | Exactly one for the new graph. |

## Governance-Only Auto-Resume

A suspended chain auto-resumes exactly once only when all predicates are true:

```text
classification == mechanical_evidence_only
AND independent_repair_review == pass
AND decision_graph_digest unchanged
AND target_byte_digest unchanged
AND authority_bearing_executable_digest unchanged
AND required_revalidation == pass
AND resume_count == 0
```

Any false or missing predicate keeps the chain suspended. The repair may not alter
accepted targets, semantics, authority, publication, deployment, credentials,
external effects, or executable authority.

## Metric Event Contract

Implementations emit schema-valid events for these measures. Targets are evaluated
per immutable graph unless the owning adoption contract declares a wider aggregation.

| Metric | Event | Target |
| --- | --- | --- |
| Postacceptance consumer defects | `governance_flow.consumer_defect.v1` | `0` |
| Prompts per immutable graph | `governance_flow.owner_prompt.v1` | `1` |
| Unchanged-byte approval retries | `governance_flow.request_retry.v1` | `0` |
| Blockers discovered after request | `governance_flow.late_blocker.v1` | `0` |
| Manual receipt transfers | `governance_flow.receipt_transfer.v1` | `0` |

An implementation must preserve event identity, graph binding, occurrence count, and
the evidence edge that produced the value. A human copying or translating a receipt
is a failed automatic evidence edge and increments the manual-transfer measure.

## Compatibility

- Existing accepted records remain historical evidence with their original authority.
  They are not retroactively promoted into this contract.
- New owner requests require the schema-valid source, normalized graph, complete
  rehearsal, freeze, independent review, and idempotent request record.
- Legacy projections need explicit adapters that prove field equality or safe subset
  relations. Prose cannot repair divergent machine records.
- Preacceptance wrappers change from early exit to collect-all with first-nonzero
  preservation. Effectful runners retain fail-fast behavior.
- Human-authored summaries remain useful communication, but cannot become request or
  authority inputs.

## Reference Implementation Boundary

The companion `governance-flow/` package supplies strict schemas, a deterministic
compiler and renderer, a bounded runner, and fixture validation. It is a public
candidate reference implementation. Passing its fixtures does not adopt it into a
capability, authorize repository mutation, publish it, deploy it, or grant effects.
