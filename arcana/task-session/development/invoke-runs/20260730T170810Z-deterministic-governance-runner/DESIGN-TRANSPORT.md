# Invoke Design Transport

## Result

Design authoring is complete. Deterministic selection evidence is produced by
`DESIGN-DENOMINATOR-RECEIPT.json` and `DESIGN-SELECTION-RESULT.json`; Plan may proceed
only when the result verdict is `pass`.

## Baseline outputs

- `ARCHITECTURE.md` covers system context, components, runtime flow, data/state,
  integration, security/trust, and operations/evolution.
- `GLOSSARY-CONSISTENCY.md` confirms term alignment.

## Key boundary

The runner owns phase order, checkpoint evidence, and receipt joins. Continuation
Router, Invoke, Signal Observer, Sigil Development, and the implementation executor
retain their own semantics and authority.

## Planning direction

Use a medium, split work pack. Start with the read-only production policy evaluator,
then build the runner in dependency order. Keep generated mirrors and promotion
behind accepted canonical and experiment evidence.

