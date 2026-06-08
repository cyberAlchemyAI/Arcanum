---
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: arcana/research-tower/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
name: research-tower
description: "Use when: turning a paper, source corpus, or research question into a governed local research tower with source-first claims, notation bridge, glossary, definitions, distills, related-work map, bridge decisions, residue, and a final learning pack."
argument-hint: "<source-or-topic> [--target <folder>] [--preset compact|standard|full|deep] [--with-subagents] [--promotion-check]"
tier: arcana
domain: research-governance
version: 0.1.0
origin: extracted from the AutoBayes research tower closure
allowed-tools: Read, Write, Bash, Glob, Grep, Agent
---

# Sigil: Research Tower

<objective>
Transform a paper, source corpus, or research question into a reproducible,
source-backed local learning tower that another agent can inspect, reuse, and
extend without rediscovering the same conceptual work.
</objective>

<logic-type>
Arcana: governed research synthesis with evidence boundaries, local semantic
authority, subagent closeout, and promotion guardrails.
</logic-type>

<applicability>
Use this sigil when:

- the user wants durable understanding rather than a short summary;
- source claims, related papers, notation, and definitions need separation;
- the result should teach Arcanum operators in the user's design language;
- a future sigil, spell, ontology, runtime, or implementation decision depends
  on the research;
- subagents may be spawned and must be reconciled before closure.
</applicability>

<inputs>
Expected inputs, when available:

- primary source URL, PDF path, paper title, corpus path, or research target;
- intended output folder;
- desired depth: `compact`, `standard`, `full`, or `deep`;
- known related papers or concepts;
- existing local research artifacts;
- target audience or operator lens;
- promotion boundaries and non-goals;
- subagent strategy or delegation preference.
</inputs>

<process>
1. Resolve the research target and output root.
2. Verify whether related artifacts already exist before creating new ones.
3. Create or update a source record with version, URL/path, date checked, and
   source boundary.
4. Build the tower scaffold:
   - `README.md`,
   - `TOWER.md`,
   - `levels/L0-corpus.md`,
   - `levels/L1-residue-map.md`,
   - `levels/L2-closure-plan.md`,
   - `gates/closure-gates.md`,
   - `residue/open-residue.md`.
5. If route complexity is high, design a dispatch route with a mandatory
   subagent closeout ledger.
6. Build a notation bridge before deep synthesis when the source uses formal
   symbols. Link reusable symbols to `research/shared-notation-glossary.md`
   when a repository-level shared glossary exists.
7. Build a paper/source claim ledger that separates direct source claims,
   related-source claims, local inference, analogy, and open residue.
8. Create the local glossary. Every entry must include source kind, local
   meaning, Arcanum reading, promotion status, and misuse warning when relevant.
9. Create governed definitions for concepts that later artifacts will depend
   on. Keep formal expression, notation meaning, intuition, and anti-misuse
   guidance together.
10. Distill the target into compact operator knowledge:
    - one-sentence model,
    - compositional spine,
    - what to borrow,
    - what to keep analogy-only,
    - what to block.
11. Map related papers or frameworks only as far as they close named residue.
12. Produce definition cards and worked examples for the concepts that carry
    the most reasoning load.
13. Produce bridge decisions using explicit statuses:
    - `borrow-carefully`,
    - `analogy-only`,
    - `block`,
    - `promotion-candidate`,
    - `future-work`.
14. Reconcile all subagent outputs. Mark each spawned lane `closed`,
    `integrated`, `rejected`, or `blocked`; no hidden open subagent work may
    remain at closure.
15. Create the final learning pack with source-backed claims, notation entry
    point, operator model, borrow/block decisions, closed residue, and honest
    cutoff.
16. Validate structure, links, required artifacts, source labels, promotion
    guardrails, and subagent closeout.
17. Return a concise closure summary with produced artifacts, validation, open
    residue, and next governed route.
</process>

<evidence-execution-handoff>
Research Tower must hand off when the next blocker is empirical evidence
production rather than source-backed understanding.

Route to `research-evidence-harness` when the target needs:

- append-only run schemas;
- JSONL fixture validation;
- objective-vector, scoring, or reviewer-rubric checks;
- dry-run result summaries;
- live-run data integrity;
- claim-adjudication readiness from measured results.

The handoff should name the source/tower artifacts that support the experiment,
the evidence mechanics still missing, and the claim or paper section blocked by
missing run data.
</evidence-execution-handoff>

<source-kind-taxonomy>
Use these labels consistently:

- `primary-source`: stated by the main source;
- `related-source`: stated by a related paper or external source;
- `local-inference`: inferred from source-backed material;
- `analogy`: useful Arcanum mapping, not source meaning;
- `operator-reading`: practical design interpretation for the user;
- `open-residue`: unresolved question or future task.
</source-kind-taxonomy>

<subagent-closeout-rule>
When subagents are spawned, closure requires a visible ledger with:

- subagent/lane name;
- assigned question;
- evidence returned;
- integration decision;
- rejected or blocked material;
- final status;
- owner of follow-up residue.

A research tower cannot be marked closed while any subagent lane is implicit,
unreviewed, or missing an integration decision.
</subagent-closeout-rule>

<promotion-rule>
Research Tower outputs are local research artifacts by default. They may teach,
compare, and recommend, but they must not promote vocabulary or behavior into
Inventory, Ontology, sigils, spells, runtime contracts, or canonical definitions
without a separate governed promotion decision.
</promotion-rule>

<quality-bar>
A successful execution must:

- verify existing artifacts before creating new ones;
- cite or path-link the source evidence used;
- distinguish source claims from Arcanum readings;
- make important notation learnable before using it heavily;
- produce glossary, definitions, distilled knowledge, and final learning pack;
- close named residue or move it into explicit future work;
- reconcile every subagent lane;
- preserve local-only promotion boundaries;
- hand off to an evidence harness when data mechanics, metrics, or claim
  adjudication become the blocker;
- validate required artifacts and links;
- leave another agent able to reproduce or audit the learning path.
</quality-bar>

<anti-patterns>
Avoid:

- summarizing the paper without a reusable artifact spine;
- turning analogies into source claims;
- promoting terminology because it sounds useful;
- skipping notation until the final pack;
- hiding uncertainty inside polished prose;
- using related papers as unbounded background;
- spawning subagents without a closeout ledger;
- calling the tower closed while residue is unnamed;
- producing final recommendations without borrow/block decisions.
</anti-patterns>

<output-contract>
Return:

```markdown
## Research Tower Summary

- Target: <source-or-topic>
- Output root: <path>
- Depth: compact | standard | full | deep
- Source record: pass | partial | block
- Existing artifacts checked: yes | no
- Required artifacts: pass | partial | block
- Notation bridge: pass | not-needed | block
- Glossary/definitions: pass | partial | block
- Related work: pass | not-needed | partial | block
- Subagent closeout: pass | not-used | block
- Promotion boundary: local-only | promotion-candidates-listed | block
- Validation: pass | partial | fail | not-run
- Final learning pack: <path or none>
- Open residue: <count>

### Produced Or Updated

- <path> - <role>

### Next Governed Route

1. <next action>
```
</output-contract>
