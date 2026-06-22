# Stage 05 Smallest Review Unit

## Status

`pass`

## Smallest Unit

The smallest coherent implementation unit is:

`SWU-RLP-001`: create the candidate Spellcraft contract from [SPELL-HANDOFF.md](../../../SPELL-HANDOFF.md).

## Why This Unit

Directly implementing runtime SWUs would skip lifecycle ownership. The work-pack already declares `spellcraft` as next owner, and the package boundary says this development package does not install the spell.

## Recomposition Proof

`SWU-RLP-001` recomposes into the full spell because it establishes the contract that later SWUs need:

1. Tower/source intake contract.
2. Preset profile contract.
3. Whisper substrate handoff.
4. Manuscript/source-trace output contract.
5. PDF renderer/fallback contract.
6. Validation and residue contract.

After that contract exists, Task Session can implement one bounded SWU at a time without taking over Spellcraft lifecycle authority.

## Deferred Units

- `SWU-RLP-002` through `SWU-RLP-007`: runtime implementation after Spellcraft accepts.
- `SWU-RLP-008`: experiment fixtures after the runnable contract exists.
- `SWU-RLP-009`: reusable readiness validation.
