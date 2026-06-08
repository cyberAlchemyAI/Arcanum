# Test Run: Monoidal Categories and Multicategories

Status: pass-standard with hardening notes

Date: 2026-06-07

## Target

Local PDF:

```text
/mnt/c/Users/vlad_/Downloads/Monoidal Categories and Multicategories.pdf
```

Tower output:

```text
research/monoidal-categories-multicategories/
```

## Result

The Research Tower sigil successfully produced a standard tower for a
notation-heavy category theory source. The run validated that the sigil needs
notation-first behavior for math papers, because the final learning pack is not
readable until symbols such as `C(A1 ... An; B)`, `b_n`, `gamma`, `iota`,
`R(A1 ... An)`, `u_A1...An`, and `V(C)` are explained.

Follow-up correction: the tower also needs an executable dispatch strategy as
the route contract before or alongside execution. This was added as
`research/monoidal-categories-multicategories/monoidal-categories-multicategories-research.dispatch.json`
and validated with Dispatch Spec.

## Produced Artifact Classes

- source record;
- tower scaffold;
- notation bridge;
- shared notation glossary additions;
- local glossary;
- governed local definitions;
- claim ledger;
- equivalence spine card;
- Arcanum bridge decision;
- open residue;
- final learning pack.

## Sigil Hardening Lessons

1. Research Tower should explicitly support a `notation-heavy` flag or inference.
2. The standard mode should allow a theorem-spine card instead of many separate
   definition cards when the target is one proof route.
3. The output contract should record extraction tooling when the source is a
   local PDF.
4. Related-work expansion should remain optional; this run correctly treated
   bibliography entries as related-source references but did not browse them.
5. A future experiment harness should include this paper as the medium/complex
   notation-heavy fixture.
6. Research Tower should emit or validate a dispatch-spec strategy as the
   executable route contract, not only the final research artifacts.

## Promotion State

This improves confidence in the draft sigil, but does not make it promotion
ready. Remaining blockers are unchanged: compact smoke test, another independent
notation-heavy run or proof audit, experiment harness, observability shape, and
explicit registry decision.
