# Source Claim Ledger

Target: Claude Shannon, "Communication Theory of Secrecy Systems"

Status: pass

## Claims

| ID | Claim | Source kind | Evidence | Local reading | Status |
| --- | --- | --- | --- | --- | --- |
| C1 | The paper develops a theoretical structure for secrecy systems rather than a practical catalog of ciphers | primary-source | `sources/source-record.md`; S2 lines 7-14 | Read it as a model of secrecy, not a handbook | accepted |
| C2 | The paper limits itself to true secrecy systems over discrete information | primary-source | S2 lines 16-34 | Exclude concealment and equipment-only privacy from this starter tower | accepted |
| C3 | Language redundancy is central to secrecy analysis | primary-source | S2 lines 55-63 | Redundancy is the attack surface that statistical analysis exploits | accepted |
| C4 | A secrecy system is a family of reversible transformations from messages to cryptograms, selected by keys | primary-source | S2 lines 65-70 and 368-408 | The key selects a possible world of transformation, not merely a password | accepted |
| C5 | Shannon assumes the cryptanalyst eventually knows the system and key-choice probabilities | primary-source | S2 lines 424-443 | Do not build security on obscurity in the local reading | accepted |
| C6 | Perfect secrecy means observing the cryptogram leaves posterior message probabilities equal to prior message probabilities | primary-source | S2 lines 1417-1477 | Perfect secrecy is invariance of belief under observation | accepted |
| C7 | Perfect secrecy requires enough key uncertainty; for infinite generated messages no finite key suffices | primary-source | S2 lines 1492-1565 | The one-time-pad lesson is key supply and rate, not aesthetic simplicity | accepted |
| C8 | Equivocation is used as a theoretical secrecy index for remaining uncertainty after interception | primary-source | S2 lines 1750-1800 | Treat secrecy as preserved uncertainty under observation | accepted |
| C9 | For random ciphers, the unicity distance is approximately `H(K) / D` | primary-source | S2 lines 3230-3237 | Finite-key secrecy degrades as intercepted material accumulates | accepted |
| C10 | Confusion and diffusion are methods for frustrating statistical analysis | primary-source | S2 lines 5451-5505 | Borrow as design heuristics only; they are not modern proof terms here | accepted |
| C11 | The 1948 communication theory paper supplies imported entropy and redundancy concepts | related-source | S2 lines 43-44 and 1410-1415 | A full tower should eventually add an MTC source pass | accepted |
| C12 | This tower can teach Arcanum operators to distinguish prior, observation, posterior, and residual uncertainty | operator-reading | C4-C9 | Useful as a local reasoning model for evidence boundaries | accepted |

## Open Claim Residue

| ID | Question | Blocking artifact | Next route |
| --- | --- | --- | --- |
| R1 | How does the 1945 report differ from the 1949 paper? | 1945 source text not added | Future source pass |
| R2 | Which modern security notions should be mapped to Shannon, and which should be kept separate? | Modern crypto source set missing | Future related-work crosswalk |
| R3 | Should any terms become repository-wide vocabulary? | No promotion decision | definitions-governance only by explicit request |

