---
contextPack: SWU-RCNS-001
sourceWorkPack: arcana/refine/development/REFINE-COMMANDLESS-NATIVE-SCHEMA-IMPLEMENTATION-PLAN.md
sourceDispatch: arcana/refine/development/REFINE-COMMANDLESS-NATIVE-SCHEMA-DISPATCH.json
strictCoverage: pass
generatedFor: codex-goal-profile
---

# SWU-RCNS-001 Context Pack

## Selected Unit

- SWU: `SWU-RCNS-001`
- Parent task: `TASK-RCNS-001`
- Goal: inventory active command-interface dependencies and classify them.
- Write scope: report only under `arcana/refine/development/`.
- Dependencies: none.
- Execution owner: local fallback or active-contract-auditor subagent receipt.
- Acceptance evidence: classification report has no unknown active hits.

## Source Contract

The implementation plan says the first task must identify active command-interface dependencies and classify historical or legacy references before source mutation begins.

Required classifications:

- `remove`
- `rewrite-native-receipt`
- `legacy-compatibility`
- `historical-preserve`
- `deterministic-tooling-outside-success-gate`

Validation command:

```bash
rg -n "tools/arcanum --resolve|tools/arcanum --exec|\\.codex/commands|command-backed|command file|slash command|/refine|/invoke" arcana/refine spells/invoke formulae/dispatch-spec tools/bootstrap_arcanum.sh --glob '!**/development/refinement-runs/**'
```

## Evidence Boundaries

- Active policy files may be classified as rewrite or remove candidates.
- Historical run evidence must not be rewritten during this SWU.
- Legacy compatibility surfaces may remain only when explicitly classified as legacy, deterministic tooling, or outside active Refine/Invoke success gates.
- Live installed packages are out of scope for this SWU.

## Required Output

Write a report under:

```text
arcana/refine/development/SWU-RCNS-001-ACTIVE-SURFACE-INVENTORY.md
```

The report must include:

- command used for inventory,
- active hits table with file path, line, excerpt, classification, rationale, and recommended follow-up SWU,
- historical/legacy preservation notes,
- blocker-level unknowns or `none`,
- validation result,
- subagent receipt summary if a subagent was used.

## Fallback Exploration

Named gaps only:

- If a hit appears in generated or historical output, inspect just enough nearby path context to classify it.
- If a file is clearly active but ownership is unclear, inspect nearest README, SKILL, or validation file in the same capability folder.
- Do not broaden into unrelated Arcanum cleanup.

## Stop Conditions

Stop and report `block` if:

- active hits cannot be classified,
- the grep command cannot run,
- write scope would need to leave `arcana/refine/development/`,
- a required source file is missing.

