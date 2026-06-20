# Governed Starter Definitions

Status: pass

Promotion scope: local-research-only

## Perfect Secrecy

- Source kind: primary-source
- Formal shape: `P_E(M) = P(M)` for every cryptogram `E` and message `M`.
- Notation meaning: The observer's probability for a message after seeing the
  cryptogram equals the observer's prior probability for that message.
- Intuition: The cryptogram is visible, but it carries no information about
  which message was sent.
- Anti-misuse guidance: Do not use "perfect secrecy" for practical security,
  encryption strength, or confidentiality vibes.
- Evidence: `tracks/paper-claim-ledger.md` C6-C7.

## Secrecy System

- Source kind: primary-source
- Formal shape: a family of reversible transformations `T_i`, each selected by
  key `i` with associated probability `p_i`, mapping message space into
  cryptogram space.
- Notation meaning: `E = T_i M`, and knowing `E` plus the key recovers `M`.
- Intuition: The key selects one reversible path among many possible paths.
- Anti-misuse guidance: Do not turn this into a generic architecture term.
- Evidence: `tracks/paper-claim-ledger.md` C4-C5.

## Equivocation

- Source kind: primary-source
- Formal shape: conditional entropy of the message or key after a cryptogram is
  known, written locally as `H_E(M)` or `H_E(K)`.
- Notation meaning: Uncertainty remains distributed over possible messages or
  keys after observation.
- Intuition: Equivocation is not ignorance in general; it is residual
  uncertainty after a particular evidence event.
- Anti-misuse guidance: Do not use it as a synonym for ambiguity unless the
  observed evidence and candidate set are explicit.
- Evidence: `tracks/paper-claim-ledger.md` C8.

## Unicity Distance

- Source kind: primary-source
- Formal shape: for a random cipher, approximately `H(K) / D`.
- Notation meaning: key uncertainty divided by source redundancy.
- Intuition: More key uncertainty delays unique solution; more redundancy makes
  unique solution arrive sooner.
- Anti-misuse guidance: Do not apply the approximation outside Shannon's random
  cipher model without a new derivation.
- Evidence: `tracks/paper-claim-ledger.md` C9.

## Confusion And Diffusion

- Source kind: primary-source
- Formal or structural shape: diffusion spreads source statistics across longer
  combinations; confusion complicates the relation between observed statistics
  and key coordinates.
- Notation meaning: no single required symbol; both are practical design
  principles in the paper's later section.
- Intuition: Diffusion distributes statistical leakage; confusion makes the
  hidden key relation harder to use.
- Anti-misuse guidance: Do not collapse these into "make things complex."
- Evidence: `tracks/paper-claim-ledger.md` C10.

