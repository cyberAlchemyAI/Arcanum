# Guide Translate Integration

## Purpose

Define how Guide links a Guide route to a Translate receipt.

## Integration Contract

Guide owns:

- route framing,
- target inspection,
- explanation sequencing,
- active evidence prompt,
- guide receipt.

Translate owns:

- term map,
- bridge map,
- target-domain definition,
- mapping limits,
- translation receipt.

## Route Link

```yaml
guide_route:
  guide_request_id: GRQ-ARCH-001
  translate_request_ref: TRQ-SALES-ARCH-001
  translate_receipt_ref: TRR-SALES-ARCH-001
```

## Guide Receipt Shape

```yaml
guide_receipt:
  receipt_id: GUIDE-RECEIPT-ARCH-001
  guide_request_id: GRQ-ARCH-001
  translate_receipt_ref: TRR-SALES-ARCH-001
  explanation_sections:
    - concrete source-domain frame
    - target-domain definition
    - mapping limits
    - system-thinking abstraction
  active_evidence_prompt: explain what the boundary protects and what should not cross it
  user_ledger_update_proposal: mark architecture boundary as clarified only after user response; mastery requires teach-back or transfer
```

## Boundary Checks

| Check | Verdict |
| --- | --- |
| Guide references Translate receipt rather than copying Translate internals. | pass |
| Translate keeps mapping limits visible to Guide. | pass |
| User ledger update is a proposal only. | pass |
| Mastery is not claimed from passive route completion. | pass |
