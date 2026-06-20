# Notation Bridge

Target: Claude Shannon, "Communication Theory of Secrecy Systems"

Status: pass

No repository-level `research/shared-notation-glossary.md` exists, so all
symbols below are local to this tower.

## Core Objects

| Symbol | Source meaning | Plain-language reading | Shared link | Used in |
| --- | --- | --- | --- | --- |
| `M` | Message or clear text | The thing being protected | n/a | claim ledger, definitions |
| `K` | Key | The chosen control/secret that selects a transformation | n/a | definitions |
| `E` | Enciphered message or cryptogram | The observed output available to the interceptor | n/a | claim ledger |
| `T_i` | Transformation indexed by key `i` | One reversible mapping from message space to cryptogram space | n/a | secrecy-system definition |
| `p_i` | Probability of choosing key `i` | Prior probability over key choices | n/a | perfect secrecy |
| `q_i` | Prior probability of message `i` | Source probability over possible messages | n/a | equivocation |
| `P(M)` | Prior probability of message `M` | Belief before seeing a cryptogram | n/a | perfect secrecy |
| `P_E(M)` | Posterior probability of `M` after seeing `E` | Belief after interception | n/a | perfect secrecy |
| `P_M(E)` | Conditional probability of `E` if `M` was chosen | How likely this cryptogram is from this message | n/a | perfect secrecy |

## Information Measures

| Symbol | Source meaning | Plain-language reading | Shared link | Used in |
| --- | --- | --- | --- | --- |
| `H(M)` | Entropy of the message choice | Uncertainty in which message was chosen | n/a | definitions |
| `H(K)` | Entropy of the key choice | Uncertainty supplied by the key source | n/a | definitions |
| `H_E(M)` | Message equivocation after observing `E` | Remaining uncertainty about the message | n/a | claim ledger |
| `H_E(K)` | Key equivocation after observing `E` | Remaining uncertainty about the key | n/a | claim ledger |
| `D` | Redundancy per symbol/letter | Statistical constraint in the source language | n/a | unicity distance |
| `N` | Number of intercepted symbols/letters | How much cryptogram material the interceptor has | n/a | unicity distance |

## Source Formulas To Read Carefully

| Formula | Source kind | Plain-language reading | Boundary |
| --- | --- | --- | --- |
| `E = f(M, K)` | primary-source | The cryptogram depends on message and key | Equivalent source formula, not a software API |
| `E = T_i M` | primary-source | A key selects a transformation applied to the message | Local transformation model |
| `P_E(M) = P(M)` | primary-source | Perfect secrecy leaves message belief unchanged after interception | Source definition |
| `P_M(E) = P(E)` | primary-source | Perfect secrecy condition: cryptogram probability is independent of message | Source theorem condition |
| `H(K) / D` | primary-source | Approximate unicity distance for a random cipher | Do not apply blindly to modern ciphers |

## Reading Order

1. Core objects: message, key, cryptogram, transformation.
2. Probability movement: prior, posterior, conditional probability.
3. Information measures: entropy, equivocation, redundancy.
4. Practical design terms: confusion, diffusion, ideal systems.

## Notation Residue

| Symbol | Question | Status | Next route |
| --- | --- | --- | --- |
| OCR variants of `H_E(M)` and `H_E(K)` | The OCR mangles subscripts and symbols in places | open | Check page scan before formalization |
| `R`, `R_M`, `R_K` | Rate notation needs the 1948 MTC bridge for full rigor | open | Build MTC notation pass |

