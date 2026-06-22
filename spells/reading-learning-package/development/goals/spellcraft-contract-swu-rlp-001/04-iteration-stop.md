# Iteration And Stop Policy

## Iteration Policy

1. Read this goal folder first.
2. Read the handoff and work-pack artifacts.
3. Draft the candidate contract at `arcanum/spells/reading-learning-package/README.md`.
4. Validate links, dispatch source, and whitespace.
5. Repair only contract-scope issues.
6. Final report must list validation results and any extra sources used.

## Fallback Exploration

Fallback exploration is limited to named gaps from the Refine result:

- contract not installed,
- preset fixtures absent,
- transcript fixture absent,
- renderer fallback unresolved,
- custom preset persistence undecided,
- runtime evidence shape-only.

For this SWU, only the first gap should be repaired. The remaining gaps become downstream handoff notes.

## Stop With BLOCK If

Stop and report `BLOCK` if:

- creating the contract requires implementing runtime behavior,
- required source artifacts are missing or contradict each other,
- the contract would need private parent-repo details,
- a validation command fails for a reason outside the write scope,
- the contract cannot preserve `research-tower` and `whisper` authority boundaries,
- the needed write target is not `arcanum/spells/reading-learning-package/README.md` or a narrowly justified development evidence update.
