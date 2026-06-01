# Refine Seed Proposal: Expand Dispatch Techniques

Status: seed accepted for refinement.

## Target

`formulae/dispatch-spec/TECHNIQUE-CATALOG.md`

## Starting Intent

The dispatch package recently gained a technique catalog, including Arcanum route-shaping techniques and POLE-inspired standards-catalog techniques. After the whole-system Arcanum/Tandem research run, the catalog should expand to cover runtime bridge, evidence bridge, and authority-boundary techniques.

## Source Context

Primary local sources:

- `formulae/dispatch-spec/TECHNIQUE-CATALOG.md`
- `formulae/dispatch-spec/ARCANUM-DISPATCH-SYNTHESIS.md`
- `formulae/dispatch-spec/development/TANDEM-ARCANUM-CROSSWALK.md`
- `formulae/dispatch-spec/development/TANDEM-INTERACTION-TENSIONS.md`
- `formulae/dispatch-spec/development/TANDEM-INTEGRATION-OPTIONS.md`
- `arcana/task-session/runtime-adapters/README.md`
- `spells/arcanum-bootstrap/README.md`

External comparison source already cloned locally:

- `/tmp/frumu-ai-tandem`

## Refinement Objective

Design the next expansion of the dispatch technique catalog so dispatch documents can cite techniques for:

- runtime adapter boundaries,
- dispatch-to-plan projection,
- runtime receipt handoff,
- approval semantics mapping,
- artifact contract bridging,
- evidence bridge discipline,
- state namespace separation,
- memory/promotion distinction,
- protected action mapping,
- preview/import gates,
- audit summary handoff.

## Write Scope

This refinement run may write only run evidence under:

```text
formulae/dispatch-spec/development/refinement-runs/20260528T231321Z-expand-dispatch-techniques/
```

It must not directly mutate `TECHNIQUE-CATALOG.md`, `dispatch.schema.json`, or runtime adapters. Those become recommended next-route work.

## Done Criteria

- Identify the smallest coherent expansion unit.
- Separate route-shaping, standards-catalog, runtime-bridge, and evidence-authority technique families.
- Propose concrete new technique IDs with use and validation expectations.
- Preserve `dispatch-spec` as validation/route contract, not runtime execution.
- Recommend a bounded next route for implementation.

## Preset And Research Mode

- Preset: `standard`
- Research mode: `no-research`

Reason: the Tandem research artifacts already provide the needed external comparison. No new internet or repository research is needed inside this refine pass.

## Planned Stage Configuration

The command surface was resolved for:

- `context-builder`
- `invoke`
- `interrogation`
- `distill`

Nested model-backed execution was not used. Command-backed stages were captured through the `dry-run` runtime adapter as dispatch evidence, and the refinement synthesis is authored locally from existing evidence.
