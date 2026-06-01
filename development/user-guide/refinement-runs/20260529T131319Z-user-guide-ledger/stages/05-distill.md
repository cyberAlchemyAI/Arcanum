# Stage 05: Distill

Status: `pass`

## Selected Coherent Unit

`User Learning Ledger + Guide Interaction Receipt`

This is the smallest unit that makes the larger system real:

```text
Guide explains or clarifies
  -> user responds
  -> Guide records what strategy was used
  -> user confirms, retrieves, transfers, or remains blocked
  -> receipt proposes a User ledger update
  -> glossary or residue updates only under clear rules
```

## Why This Unit Wins

| Candidate | Verdict | Reason |
| --- | --- | --- |
| Whole User/Guide framework | reject for now | Too large and would blur ledger, guide, game, library, install, and glossary. |
| Guide spell first | reject for now | Would generate adaptive behavior before defining what evidence is safe to store. |
| Install game first | defer | Useful, but it should output to the ledger contract rather than inventing profile shape by itself. |
| Software concept library first | defer | It will be needed, but library content is less foundational than the receipt/update contract. |
| User ledger plus Guide receipt | select | It provides the data contract that all other pieces need. |

## Core Primitive

The first primitive is not "profile". It is a `learning receipt`.

A learning receipt is a bounded record of one Guide interaction:

- target concept,
- prior source domain used,
- explanation strategy,
- number of attempts or turns,
- evidence of understanding,
- friction/residue,
- proposed ledger update,
- user confirmation status.

## Recomposition Proof

The selected unit recomposes into:

- `cyberalchemy-install-game`: emits initial profile receipts.
- `guide-clarify-blocker`: emits blocker-resolution receipts.
- `guide-domain-bridge`: emits bridge effectiveness receipts.
- `guide-master-definition`: turns receipt evidence into glossary rows.
- `guide-generalize`: uses mastered definitions and bridges to move from specific to abstract.
