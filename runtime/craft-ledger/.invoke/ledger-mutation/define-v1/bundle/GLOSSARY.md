# Glossary

| Term | Status | Meaning or authority reference |
| --- | --- | --- |
| ledger inspection snapshot | candidate | It is the fresh read the caller gets before asking to change the ledger. |
| ledger mutation request | candidate | It is one change request with shared addressing fields and a type-specific body. |
| operation payload | candidate | The outside of the request stays the same; the inside changes according to the kind of ledger entry. |
| ledger mutation outcome | candidate | It tells the caller exactly what happened and whether the ledger changed. |
