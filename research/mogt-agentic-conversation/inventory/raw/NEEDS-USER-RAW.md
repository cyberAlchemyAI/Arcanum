# MOGT Sources Awaiting User-Provided Raw Content

Purpose: track sources that cannot yet be treated as fully library-grade because raw content has not been preserved locally.

## Awaiting Raw Input

| Source ID                 | Reference ID            | Why Raw Is Needed                                                               |
| ------------------------- | ----------------------- | ------------------------------------------------------------------------------- |
| PAPER-WOHLIN-2012         | REF-WOHLIN-2012         | paywalled methodology book; current inventory is a rollup only                  |
| PAPER-DEB-2001            | REF-DEB-2001            | paywalled theory book; current inventory is a rollup only                       |
| BOOK-KEENEY-RAIFFA-1976   | REF-KEENEY-RAIFFA-1976  | paywalled theory book; current inventory is a rollup only                       |
| PAPER-MARLER-2010         | REF-MARLER-2010         | source scope is still being normalized and raw content is not preserved locally |
| PAPER-WALKER-1997         | REF-WALKER-1997         | open retrieval not yet preserved locally in this pass                           |
| BOOK-JAIN-1991            | REF-JAIN-1991           | paywalled performance-analysis book                                             |
| PAPER-HART-STAVELAND-1988 | REF-HART-STAVELAND-1988 | paywalled human-factors source                                                  |
| PAPER-WOOLDRIDGE-2009     | REF-WOOLDRIDGE-2009     | second-wave theory source, not yet inventorized with raw provenance             |
| PAPER-NASH-1950           | REF-NASH-1950           | second-wave theory source, not yet inventorized with raw provenance             |

## Intake Rule

When raw files are provided, place them under `inventory/raw/<source-id>/` and then create or refresh the matching `inventory/library/<source-id>.md` entry.
