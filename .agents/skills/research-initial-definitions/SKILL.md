---
metadata:
  surface_kind: generated-native-runtime-package
  runtime: codex
  canonical_source: arcana/research-initial-definitions/SKILL.md
  alias_of: null
  generated_by: tools/bootstrap_arcanum.sh --profile
  mutation_policy: regenerate-from-canonical-source
name: research-initial-definitions
description: Creates or revises the informational research-initial-definitions.md required before governed research begins. Use when opening a research topic or documenting its context, purpose, organized refinable research questions with evidence obligations, confirmed constraints, existing evidence, and known gaps without designing or conducting the research.
---

# Research Initial Definitions

Create `<research-folder>/research-initial-definitions.md` before a governed research dispatch is
designed or proposed. The document explains what the research is about; it does not prescribe how
the research will be conducted. Its research questions govern epistemic scope: they state what must
be understood and evidenced, not how work will be divided, sequenced, executed, or accepted.

Place the research folder beneath a repository-local directory named exactly `research`, and use a
topic-specific child rather than the shared `research` directory itself. Treat this layout as the
canonical location contract for the baseline and its later research artifacts.

## Required structure

### Context

Write one or two high-level paragraphs. Begin with the broader project or system and its overall
purpose. Then describe the specific local problem this research supports solving and why resolving
that problem matters to the broader project.

Do not describe what the research will investigate, how it will be conducted, or what solution it
should produce.

### Purpose

Explain what the document establishes and which later discovery, design, or decision the research
will inform. Do not describe research execution.

### Research Questions (Can be refined)

State one required program question that defines the overall epistemic boundary. Then add every
materially distinct supporting question needed to expose unresolved dimensions within that
boundary. Organize supporting questions under descriptive thematic headings and number them for
stable reference. Do not impose a fixed maximum; consolidate overlapping questions rather than
expanding one unknown into every possible diagnostic.

Admit a supporting question only when it:

- asks for information genuinely unresolved in the current evidence baseline;
- can materially affect the stated purpose or a later decision named there;
- is grounded in the context, confirmed constraints, or known gaps;
- is neutral about candidate vocabulary, hypotheses, architectures, and solutions; and
- can be read as a knowledge boundary rather than as an instruction to an agent.

Make each question atomic enough to be answered or remain unresolved independently. Split clauses
whose answers could differ or depend on different evidence or authority. Keep together an
inseparable contrast that defines one boundary. Use stable identifiers when later artifacts will
need to cite, split, merge, defer, or reconcile individual questions.

Treat every registered question as a program-scope evidence obligation. A later answer must:

- state its exact scope and answer status;
- cite addressable evidence for every load-bearing claim;
- distinguish documentary assertion, executable observation, independent recomputation, and formal
  proof rather than treating them as interchangeable support; and
- state contrary evidence, residual uncertainty, and the boundary beyond which the answer does not
  apply when those are material.

Do not record an unsupported positive answer. When sufficient evidence is unavailable, keep the
question unresolved and cite the inspected evidence, attempted checks, and exact remaining gap;
absence of found evidence does not establish absence. A deferred question must retain its reason,
and a retired question must cite the authoritative scope decision that removed it.

Treat headings, numbering, and identifiers as semantic organization only. They do not define
workstreams, priority, sequence, dependency, ownership, source allocation, dispatch topology, or a
requirement that one dispatch answer every question.

Use this machine-verifiable Markdown shape:

- `### Program question` occurs exactly once and comes first in this section;
- the next non-empty line is one single-line question formatted as
  `**RQ-00.** <question ending in ?>`;
- one or more descriptive level-three thematic headings follow;
- supporting questions form one continuous numbered list across those headings and use
  `<n>. **RQ-<nn>.** <question ending in ?>`, beginning with `1. **RQ-01.**`; and
- every question identifier is unique and its numeric suffix matches its list number.

Within the Research Questions section, include only level-three headings and formatted question
entries. Do not place required headings or questions inside fenced code blocks.

### Confirmed Product Constraints

Record decisions, requirements, and boundaries already established by the user or an authoritative
project artifact. Do not present assumptions as confirmed constraints.

### Current Evidence Baseline

Summarize relevant information already known before this research begins. Cite existing artifacts
when available. Do not conduct new research merely to populate this section.

### Known Gaps

Record what is not yet understood about the subject. Describe missing knowledge, unclear
boundaries, or unresolved concepts without turning them into tasks or a research plan.

Ensure that every material supporting question corresponds to a known gap and every material gap
affecting the purpose is covered by a research question. Keep gaps declarative and questions
interrogative; do not require a traceability matrix unless the user requests one.

## Boundaries

Keep confirmed facts, existing evidence, and unknowns distinct. Do not include:

- candidate answers, vocabulary, initial hypotheses, or proposed solutions;
- research methods, workstreams, source selection, or source plans;
- agent roles, tools, dispatch topology, or budgets;
- prescribed experiments, witness or counterexample construction, success conditions, stopping
  conditions, or output contracts; or
- handoffs, implementation steps, or findings.

Questions may ask which failures, contrary evidence, discriminating cases, or unresolved boundaries
exist. They must not prescribe a test to run, witness or counterexample to construct, source corpus
to search, artifact to produce, or threshold to satisfy.

Treat the document as informational context. It is not a research plan, findings report, dispatch
configuration, specification, or runtime authority.
