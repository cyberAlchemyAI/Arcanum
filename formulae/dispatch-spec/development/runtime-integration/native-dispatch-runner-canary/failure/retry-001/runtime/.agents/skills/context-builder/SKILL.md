---
surface_kind: generated-native-runtime-package
runtime: codex
canonical_source: transmutations/context-builder/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
name: context-builder
description: "Use when: building a compact, task-ready context pack from selector-level evidence and obligation-linked excerpts."
argument-hint: "<task-reference> [--mode lean|standard|deep] [--max-files <n>] [--strict] [--emit markdown|json|both] [--handoff runtime] [--persist <session-evidence-path>] [--dry-run]"
tier: transmutations
domain: context-synthesis
version: 0.2.0
origin: generalized from recurring task-context retrieval practice
allowed-tools: Read, Write, Glob, Grep, Bash, AskQuestions
---

# Sigil: Context Builder

<objective>
Produce a minimal task-ready context bundle that maximizes relevance, preserves evidence selectors, and minimizes reading overhead. When requested for runtime delegation, emit a strict handoff pack as session evidence in both Markdown and structured JSON/index form.
</objective>

<logic-type>
Transmutation: bounded evidence selection and structured context synthesis.
</logic-type>

<flags>
- `--mode lean|standard|deep`: control excerpt budget. Default: `standard`.
- `--max-files <n>`: override the file count budget.
- `--strict`: require every selected item to map to an obligation. Default: on.
- `--emit markdown|json|both`: choose output format. Default: `markdown`.
- `--handoff runtime`: emit a runtime handoff pack suitable for runtime delegation. This implies strict obligation coverage and `--emit both`.
- `--persist <session-evidence-path>`: write handoff artifacts under a run/session evidence path. Persisted packs are execution evidence, not canonical planning documents.
- `--dry-run`: preview selected context without writing artifacts.
</flags>

<handoff-pack-contract>
When `--handoff runtime` is used, Context Builder produces a handoff pack with:

- identity: task/SWU id, source work-pack or task reference, run/session id when available;
- obligations: every parsed obligation with `covered`, `resolved`, or `block` status;
- selected sources: file paths, selectors, short excerpts, and obligation refs;
- architecture guidance and related feature context;
- constraints, non-goals, write scope, done criteria, and validation surface;
- gaps, blockers, contradictions, and explicit resolutions;
- authority precedence used to resolve conflicts;
- fallback exploration rule for the runtime;
- provenance: timestamp, source refs, and content hash or git SHA when available;
- output paths for the Markdown pack and JSON/index.

Strict coverage rule: a runtime handoff pack is runnable only when every obligation is covered by selected evidence or explicitly resolved as not applicable/deferred. Uncovered, contradictory, stale, unsafe, missing write-scope, or missing validation obligations return `BLOCK`.

Persistence rule: persisted handoff packs live under session/run evidence. They are audit artifacts for that execution, not reusable source-of-truth documents.
</handoff-pack-contract>

<process>
1. Resolve the target task and its expected output.
2. Parse task obligations from the request, task file, requirements, checklist, acceptance criteria, or completion criteria.
3. Build an obligation matrix where each obligation has an ID, required evidence, and unresolved status.
4. Seed retrieval from explicit links and references first.
5. Extract selectors before inclusion:
   - markdown headings, anchors, tables, or bullet ranges,
   - code symbols, declarations, tests, endpoint contracts, or minimal snippet windows,
   - config keys, scripts, schemas, or command references.
6. Expand search only for uncovered obligations and scope searches to relevant folders or filenames.
7. Exclude any candidate that does not close at least one obligation.
8. Rank selected evidence by relevance, cost, and ambiguity.
9. Enforce budgets:
   - `lean`: up to 8 files and 140 excerpt lines,
   - `standard`: up to 14 files and 280 excerpt lines,
   - `deep`: up to 24 files and 520 excerpt lines.
10. If `--handoff runtime` is set, enforce strict coverage and prepare Markdown plus JSON/index handoff outputs.
11. Use `templates/runtime-handoff-pack.md` and `templates/runtime-handoff-index.json` as the output shape when a concrete repository template is needed.
12. Persist handoff outputs under the requested session evidence path when `--persist` is provided.
13. Emit the context pack and optional index.
14. Return blockers for obligations that lack sufficient evidence.
</process>

<quality-bar>
A successful execution must:

- include only selector-level evidence,
- map every selected item to at least one obligation,
- keep the noise ratio low,
- separate evidence from inference,
- report uncovered obligations,
- block runtime handoff packs unless all obligations are covered or explicitly resolved,
- avoid repository-wide context dumps,
- produce a compact artifact another agent can use immediately,
- emit Markdown plus JSON/index for runtime handoff packs,
- label persisted handoff packs as session evidence rather than canonical docs.
</quality-bar>

<anti-patterns>
Avoid:

- copying whole files when a selector would suffice,
- including background material because it is interesting,
- running broad unbounded searches,
- omitting why each item was selected,
- hiding unresolved obligations,
- allowing a runtime handoff from incomplete, stale, contradictory, unsafe, or validation-missing context,
- persisting handoff packs beside canonical planning docs without labeling them session evidence,
- exceeding the selected mode budget without explanation.
</anti-patterns>

<output-contract>
Return:

```markdown
## Context Pack Summary

- Task: <task-reference>
- Mode: lean | standard | deep
- Files selected: <count>
- Snippets selected: <count>
- Obligation coverage: <percent>
- Noise ratio: <value>
- Output markdown: <path or dry-run>
- Output index: <path or none>
- Handoff pack: <none | runtime>
- Session evidence path: <path | none | dry-run>
- Strict coverage: pass | block | n/a
- Blockers: <count>

### Included Context

- <path> - <why included> - <selectors> - <obligation refs>

### Excluded Candidates

- <path> - <why excluded>

### Next Actions

1. <action>
```
</output-contract>
