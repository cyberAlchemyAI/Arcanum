---
profile: codex-goal
sourceWorkPack: arcana/refine/development/REFINE-COMMANDLESS-NATIVE-SCHEMA-IMPLEMENTATION-PLAN.md
selectedUnit: SWU-RCNS-001
readiness: pass
---

# Codex Goal Profile: SWU-RCNS-001

## Codex Goal Profile Result

- Source work-pack: `arcana/refine/development/REFINE-COMMANDLESS-NATIVE-SCHEMA-IMPLEMENTATION-PLAN.md`
- Selected unit: `SWU-RCNS-001`
- Readiness: `pass`
- Native Goal:

```text
/goal Outcome: complete SWU-RCNS-001 by inventorying active command-interface dependencies for the Refine commandless native schema migration and writing arcana/refine/development/SWU-RCNS-001-ACTIVE-SURFACE-INVENTORY.md with every active hit classified as remove, rewrite-native-receipt, legacy-compatibility, historical-preserve, or deterministic-tooling-outside-success-gate.

Verification surface: run `rg -n "tools/arcanum --resolve|tools/arcanum --exec|\\.codex/commands|command-backed|command file|slash command|/refine|/invoke" arcana/refine spells/invoke formulae/dispatch-spec tools/bootstrap_arcanum.sh --glob '!**/development/refinement-runs/**'` and ensure the report accounts for every relevant active hit with no unknown active classifications.

Constraints: read the handoff pack first at arcana/refine/development/SWU-RCNS-001-CONTEXT.md and structured index at arcana/refine/development/SWU-RCNS-001-CONTEXT.json; preserve historical evidence; do not edit canonical Refine, Invoke, Dispatch Spec, tools, bootstrap, or generated package source in this goal; write only the inventory report under arcana/refine/development/ unless explicitly blocked by the context pack.

Boundaries: this goal is report-only and covers active command-interface dependency classification for arcana/refine, spells/invoke, formulae/dispatch-spec, tools/bootstrap_arcanum.sh, and tools/arcanum. Do not broaden into unrelated Arcanum cleanup, live installed package mutation, or canonical source rewriting. Extra sources outside the handoff pack are allowed only for named classification gaps, and the final report must list each extra source, the gap it answered, and whether it changed the result.

Iteration policy: proceed pack-first, run the inventory command, classify hits, write the report, rerun the inventory command to check coverage, and stop when the report has no unknown active hits. If subagent audit receipts are available, integrate them as evidence but parent synthesis owns the final classification.

Blocked stop condition: stop and report block if the grep command cannot run, source files are missing, any active hit cannot be classified after bounded nearby-context inspection, or completing the report would require modifying files outside the allowed write scope.
```

- Verification surface: active-surface grep plus report coverage check.
- Boundaries: report-only; allowed write path is `arcana/refine/development/SWU-RCNS-001-ACTIVE-SURFACE-INVENTORY.md`.
- Handoff pack: `arcana/refine/development/SWU-RCNS-001-CONTEXT.md` and `arcana/refine/development/SWU-RCNS-001-CONTEXT.json`
- Strict coverage: `pass`
- Fallback exploration: named gaps only
- Extra-source reporting: required
- Stop condition: block if active hits cannot be classified, validation cannot run, or write scope would exceed report-only bounds.
- Validation: profile generated from `SWU-RCNS-001` row and parent task in the commandless native schema implementation plan.

