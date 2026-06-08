# Craft Interface Native Goal Profile

Source work-pack: `development/craft/CRAFT-INTERFACE-WORK-PACK.md`
Selected unit: ordered sequence `CRAFT-INTERFACE-001` then `CRAFT-INTERACTION-001`
Readiness: pass
Strict coverage: pass

## Native Goal

```text
/goal Execute all ready tasks in development/craft/CRAFT-INTERFACE-WORK-PACK.md in order: CRAFT-INTERFACE-001 then CRAFT-INTERACTION-001. Use development/craft/CRAFT-INTERFACE-GOAL-CONTEXT.md and development/craft/CRAFT-INTERFACE-GOAL-CONTEXT-INDEX.json as the strict handoff pack before reading wider context. Outcome: create every output file named by both tasks, preserve the local Craft interface/interaction contracts, and update SESSION-LEDGER.md only append-only if evidence supports it. Verification: parse generated interface/interaction YAML schema and example files with python/yaml, run dispatch validation for CRAFT-INTERFACE-DISPATCH.json and CRAFT-INTERACTION-DISPATCH.json, and manually check all work-pack done criteria and hard gates. Constraints: keep .craft/ledger.yml as target-project source of truth; keep CRAFT.md as human view; keep definitions local; require recomposition evidence before context closure; treat dispatch pass as route-shape evidence only. Boundaries: write only named outputs plus optional append-only development/craft/SESSION-LEDGER.md; do not edit command surfaces, runtime adapters, registries, sigils, spells, canonical glossary state, or promotion artifacts. Iteration: after each task, validate, repair bounded failures, record residue, then continue to the next task. Fallback exploration: named gaps only; final report must list any extra source, why it was needed, and whether it changed the result. Stop with BLOCK if a hard gate in CRAFT-INTERFACE-DEVELOPMENT-GAP-REVIEW.md fails, source context contradicts the pack, required files are missing, or validation cannot pass after bounded repair.
```

## Verification Surface

- YAML parse check for generated schema/example files.
- Dispatch validation for both existing dispatch files.
- Manual review against work-pack done criteria and hard gates.

## Boundaries

Write scope is limited to task output files and optional append-only
`development/craft/SESSION-LEDGER.md` synchronization.

## Handoff Pack

- Markdown: `development/craft/CRAFT-INTERFACE-GOAL-CONTEXT.md`
- JSON/index: `development/craft/CRAFT-INTERFACE-GOAL-CONTEXT-INDEX.json`

## Stop Condition

Stop with `BLOCK` on hard-gate violation, missing source, source contradiction,
or validation failure after bounded repair.
