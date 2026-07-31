# W2: Owner Integration

Layer question: can the runner invoke and join side jobs while preserving owner
authority?

Order: TSGR-007 -> TSGR-008.

TSGR-008 additionally requires the external Continuation Router readiness receipt.
Exit requires a digest-bound adapter manifest, validated generic hook envelopes,
Continuation Router receipt with a separately joined exact Invoke owner receipt,
successor discrimination, and proof that no next SWU executed.

Progress:

- TSGR-007: completed with passing manifest-bound owner-hook envelopes, bounded
  structured execution, negative receipt coverage, and zero live owner effects;
- TSGR-008: selected as the unique next candidate but blocked before admission by
  the absent external Continuation Router readiness receipt;
- W2 exit: not satisfied; no successor executed.
