# Design Distill Validation

## Intent And Budget

- Design intent: deterministic, non-authority compilation and reuse for Context Builder
- Target context: one public sigil extension
- Output artifact: six-view architecture plus planned witness contracts
- Optimization goal: smallest architecture that proves reproducible context compilation without smuggling semantic authority or future scale
- Budget: Standard, inferred because the user did not request another Distill budget
- Role execution: local Proposer/Balancer simulation; no subagent dispatch was authorized

## Discovery Baseline

- Canonical Context Builder contract and templates exist.
- No deterministic compiler exists in the target folder.
- Public benchmark outputs expose differing selected sets and output hashes.
- Exact token savings and runtime behavior are unproven.
- Public/private and lifecycle owner boundaries are fixed.

## Proposer Pass

Candidate unit:

> A typed request enters one deterministic kernel that validates exact
> selectors, stores content-addressed excerpts, chooses a covering set, renders
> one runtime payload plus evidence formats, and emits a receipt.

Evidence/assumption:

- selector extraction, hashing, ordering, rendering, and schema validation are mechanical;
- candidate-to-obligation mappings are supplied before the kernel;
- filesystem persistence is sufficient for the first proof.

## Balancer Pass

| Objection Category | Objection |
| --- | --- |
| responsibility | Semantic mapping must not be hidden inside deterministic selection. |
| premature complexity | Multiple selector languages, tokenizers, databases, cleanup, and delta protocols would overbuild L0. |
| evidence | Token reduction lacks actual runtime receipts. |
| boundary | Cache reuse must not become source or promotion authority. |
| closure | Hash-only output would not prove an end-to-end usable payload. |

## Reconciliation

| Objection | Decision |
| --- | --- |
| semantic mapping | accept; make typed candidate mapping a precondition |
| selector breadth | accept; L0 supports one explicit Markdown/short-file path |
| token plugin | defer; bytes are the L0 cost unit |
| database/cleanup | defer; filesystem cache is disposable |
| delta payload | defer; full payload is default |
| end-to-end closure | revise; L0 includes one exact selector, one cache object, one payload, and one receipt |

## Smallest Coherent Design Unit

```text
typed single-selector request
  -> exact current snapshot
  -> one content-addressed excerpt object
  -> one deterministic payload
  -> one validation receipt
  -> byte-identical replay and stale-source negative proof
```

Further splitting would lose either reusable context storage, runtime payload
utility, or deterministic proof. Broader selector adapters, multi-candidate
selection, tokenizer plugins, delta reuse, and lifecycle integration remain
separate later units.

## Recomposition Proof

The unit establishes the stable contracts used by later layers:

- multi-candidate deduplication and covering-set selection reuse the request,
  snapshot, object, payload, and receipt schemas;
- format parity reuses the same selected object projection;
- token accounting measures the same payload bytes;
- base/delta proof binds the same pack receipt;
- Sigil Development integrates only after these behaviors are evidenced.

No hidden glue is required beyond explicit versioned interfaces.

## Cycle And Frame Checks

- Recursive rounds used: 2
- Cycle guard: no repeated split
- Frame expiry: revisit if the source-selector model cannot express real Context Builder sources or if runtime adapters cannot consume a single payload
- Premortem: stale cache acceptance and fake token precision are the highest-risk failure modes; both have negative fixtures

## Verdict

- Status: pass
- Split pressure: later selector, token, delta, and lifecycle units remain separate
- Blocking gaps: none for Plan authoring
- Evidence ceiling: Design validation only
- Next route: Invoke Plan
