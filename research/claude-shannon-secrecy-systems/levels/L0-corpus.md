# L0 Corpus

Status: pass

## Corpus Inventory

| ID | Source | Kind | Use | Status |
| --- | --- | --- | --- | --- |
| S1 | Shannon, "Communication Theory of Secrecy Systems," 1949 | primary-source | Main source for secrecy-system theory | pass |
| S2 | Internet Archive OCR text for S1 | primary-source access copy | Line-level evidence pointer | pass |
| S3 | Shannon, "A Mathematical Theory of Communication," 1948 | related-source | Imported entropy/redundancy background cited by S1 | bounded |
| S4 | "A Mathematical Theory of Cryptography," 1945 report | related-source provenance | Earlier confidential report named by S1 | bounded |
| S5 | Vernam system | related-source/example | Example named by S1 for perfect secrecy | bounded |

## Source-First Findings

| Finding | Source kind | Evidence | Local consequence |
| --- | --- | --- | --- |
| The paper is a theoretical treatment of secrecy systems, not a catalog of cipher-breaking tactics | primary-source | S2 lines 7-14 | Keep the tower structural and probabilistic |
| Scope is narrowed to true secrecy systems over discrete symbols | primary-source | S2 lines 16-34 | Do not map concealment/privacy systems into this tower |
| A secrecy system is modeled as reversible transformations from messages to cryptograms, indexed by keys | primary-source | S2 lines 65-70 and 368-408 | Use transformation vocabulary in notation and definitions |
| The cryptanalyst is assumed to know the system and key probabilities | primary-source | S2 lines 424-443 | Do not equate secrecy with obscurity |
| Perfect secrecy means the cryptogram leaves message probabilities unchanged | primary-source | S2 lines 1417-1477 | Treat secrecy as posterior-prior invariance |
| Equivocation measures remaining uncertainty after interception | primary-source | S2 lines 1750-1800 | Use uncertainty-residue language carefully |
| Unicity distance is the approximate intercepted length where solution becomes unique | primary-source | S2 lines 3230-3237 | Treat finite-key secrecy as length-sensitive |
| Confusion and diffusion are practical methods for frustrating statistical analysis | primary-source | S2 lines 5451-5505 | Borrow as design heuristics, not as cryptographic guarantees |

## Local Evidence Rule

Every synthesis artifact must label source kind:

- `primary-source`
- `related-source`
- `local-inference`
- `analogy`
- `operator-reading`
- `open-residue`

