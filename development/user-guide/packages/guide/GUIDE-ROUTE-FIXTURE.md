# Guide Route Fixture

## Purpose

Static `/guide this architecture` route fixture. This fixture does not execute research or subagents.

## Request

| Field | Value |
| --- | --- |
| guide_request_id | GRQ-ARCH-001 |
| target_ref | architecture decision note fixture |
| target_type | software architecture |
| user_goal | Understand why a boundary decision matters and how to reason about it. |
| user_handle_refs | UDA-SALES-001, UVP-CONCRETE-FIRST-001, UCS-SCHEMA-001 |
| status | pass |

## Route Steps

| Order | Step Kind | Action | Output |
| --- | --- | --- | --- |
| 1 | frame | State what the architecture decision is trying to protect. | guide frame |
| 2 | inspect | Identify boundary, dependency, data, behavior, and failure concerns from provided context. | structure notes |
| 3 | translate | Call Translate with sales source domain and software architecture target domain. | translate request ref |
| 4 | explain | Assemble explanation sections: concrete example, term map, target definition, mapping limits, system-thinking abstraction. | guide explanation |
| 5 | validate_understanding | Ask user to explain a new boundary decision in their own words. | active evidence prompt |
| 6 | receipt | Propose User ledger updates for concept state, vocabulary preference, or residue. | guide receipt |

## Translate Call

```yaml
translate_request:
  target_concept: architecture boundary decision
  source_domain: sales
  target_domain: software architecture
  requested_style: concrete-first
  user_handle_refs:
    - UDA-SALES-001
    - UVP-CONCRETE-FIRST-001
  target_context_ref: architecture decision note fixture
```

## Validation Prompt

In your own words, explain what the boundary protects and give one example of what should not cross it.

## Receipt

```yaml
guide_receipt:
  receipt_id: GUIDE-RECEIPT-ARCH-001
  route_ref: GRQ-ARCH-001
  translate_receipt_ref: pending
  proposed_user_update: concept state for architecture boundary may become clarified after user response; mastery requires teach-back or transfer.
```

## Fixture Check

- Guide calls Translate instead of embedding Translate internals.
- No live research or subagent dispatch occurs.
- User ledger write is only proposed through receipt.
