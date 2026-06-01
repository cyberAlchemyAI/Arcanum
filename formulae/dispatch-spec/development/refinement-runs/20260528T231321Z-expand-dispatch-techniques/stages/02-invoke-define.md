# Stage 2: Invoke Define

Status: pass with caveat.

## Definition

The target is a **dispatch technique catalog expansion**, not a validator change.

The expansion should add a fourth technique family:

```text
Runtime Bridge And Evidence Techniques
```

This family sits beside:

- Arcanum Dispatch Techniques,
- POLE-Inspired Standards Techniques.

It names techniques that help dispatch documents explain how a route crosses from Arcanum capability/lifecycle governance into runtime execution or external runtime evidence without collapsing authority.

## Non-Goals

- Do not make Tandem a required runtime.
- Do not make dispatch-spec execute anything.
- Do not treat runtime approval as Arcanum promotion.
- Do not mirror runtime logs into Arcanum observability.
- Do not change `dispatch.schema.json` until the technique catalog update proves useful.

## Candidate Output

A later Task Session should update `TECHNIQUE-CATALOG.md` with a new table of runtime bridge/evidence techniques and add a short reference section in `README.md` and `ARCANUM-DISPATCH-SYNTHESIS.md`.
