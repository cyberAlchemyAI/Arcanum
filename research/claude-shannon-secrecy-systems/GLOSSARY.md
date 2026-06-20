# Local Glossary

Status: pass

Promotion scope: local-research-only

## `secrecy system`

- Source kind: primary-source
- Local meaning: A family of reversible transformations from possible messages
  into possible cryptograms, where each transformation corresponds to a key
  choice with an associated probability.
- Arcanum reading: A system is not only the actual path taken; it is the whole
  set of alternatives the observer must reason over.
- Promotion status: local-only
- Misuse warning: Do not use this to mean any security system, privacy feature,
  or access-control layer.
- Evidence: `tracks/paper-claim-ledger.md` C4.

## `cryptogram`

- Source kind: primary-source
- Local meaning: The enciphered output `E` available to the receiving point and
  possibly to the interceptor.
- Arcanum reading: The observed artifact from which posterior beliefs are
  updated.
- Promotion status: local-only
- Misuse warning: Do not equate it with any arbitrary log, trace, or output
  unless the transformation and observer model are explicit.
- Evidence: `NOTATION.md`.

## `a priori probability`

- Source kind: primary-source
- Local meaning: A message or key probability before a specific cryptogram is
  intercepted.
- Arcanum reading: The prior state of an observer's belief.
- Promotion status: local-only
- Misuse warning: Do not treat this as objective truth; in the source, it is the
  cryptanalyst's probability model.
- Evidence: `tracks/paper-claim-ledger.md` C4-C6.

## `a posteriori probability`

- Source kind: primary-source
- Local meaning: A message or key probability after observing a cryptogram.
- Arcanum reading: The belief state induced by a visible artifact.
- Promotion status: local-only
- Misuse warning: Do not collapse posterior update into "the answer"; posterior
  mass may remain spread across many possibilities.
- Evidence: `tracks/paper-claim-ledger.md` C6 and C8.

## `perfect secrecy`

- Source kind: primary-source
- Local meaning: A secrecy condition where observing any cryptogram leaves the
  probabilities of messages unchanged.
- Arcanum reading: An observation that carries no update about the protected
  message.
- Promotion status: local-only
- Misuse warning: Do not use this as a vague synonym for strong security.
- Evidence: `definition-cards/perfect-secrecy.md`.

## `equivocation`

- Source kind: primary-source
- Local meaning: Conditional uncertainty about the message or key after a
  cryptogram has been observed.
- Arcanum reading: The amount of uncertainty that remains after evidence is
  visible.
- Promotion status: promotion-candidate
- Misuse warning: Do not promote without clarifying whether it is formal
  entropy, a local metaphor, or a governance term.
- Evidence: `definition-cards/equivocation.md`.

## `redundancy`

- Source kind: primary-source
- Local meaning: Statistical constraint in a language/source that makes some
  symbols or sequences predictable.
- Arcanum reading: The compressible structure that can leak information under
  observation.
- Promotion status: local-only
- Misuse warning: Do not equate with duplicate files, extra docs, or operational
  slack without a separate analogy decision.
- Evidence: `tracks/paper-claim-ledger.md` C3.

## `unicity distance`

- Source kind: primary-source
- Local meaning: Approximate amount of intercepted material needed before a
  unique solution emerges for a random cipher.
- Arcanum reading: A threshold where accumulated evidence collapses ambiguity.
- Promotion status: analogy-only
- Misuse warning: Do not apply the formula to modern systems unless the source
  assumptions have been rebuilt.
- Evidence: `definition-cards/unicity-distance.md`.

## `confusion`

- Source kind: primary-source
- Local meaning: Making the relation between cryptogram statistics and key
  description complex and difficult to exploit.
- Arcanum reading: Preventing simple observable features from cleanly revealing
  hidden coordinates.
- Promotion status: analogy-only
- Misuse warning: Do not use confusion to justify confusing documentation or
  opaque governance.
- Evidence: `definition-cards/confusion-diffusion.md`.

## `diffusion`

- Source kind: primary-source
- Local meaning: Spreading source statistical structure across longer-range
  cryptogram statistics.
- Arcanum reading: A way to distribute leakage so local observations carry less
  direct leverage.
- Promotion status: analogy-only
- Misuse warning: Do not call any broad distribution "diffusion" unless the
  hidden statistical structure and observation model are named.
- Evidence: `definition-cards/confusion-diffusion.md`.

## `ideal system`

- Source kind: primary-source
- Local meaning: A finite-key system where equivocation does not approach zero
  even with arbitrarily much intercepted material, under the paper's model.
- Arcanum reading: A system where ambiguity remains structurally preserved.
- Promotion status: local-only
- Misuse warning: Do not confuse with idealized UX, ideal processes, or modern
  security ideals.
- Evidence: `tracks/paper-claim-ledger.md` C8-C9.

