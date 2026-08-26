---
surface_kind: generated-native-runtime-package
runtime: codex
canonical_source: arcana/research-initial-definitions/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
name: research-initial-definitions
description: Create or revise the research-initial-definitions.md informational baseline required before a governed research dispatch. Use when opening or reframing a topic folder beneath a repo-local directory named research and documenting context, purpose, a refinable question, confirmed constraints, existing evidence, and known gaps without designing or conducting the research.
---

# Research Initial Definitions

<objective>
Create `<working-folder>/research-initial-definitions.md` before a governed
research dispatch is designed or proposed. The working folder must identify one
research beneath a directory literally named `research` somewhere inside the
repository. Explain what the research is about without prescribing how it will
run or which solution it should produce.
</objective>

<process>
1. Resolve the containing repository root.
2. Resolve the applicable directory literally named `research`. Any directory
   inside the repository may contain it; parent directory names carry no type or
   eligibility semantics. Prefer the container nearest to the user's explicit
   work target and use `<repository-root>/research` when no more local context is
   indicated.
3. Resolve one research-specific working folder beneath that directory, normally
   `<research-root>/<research-id>`. Do not place the artifact outside a
   `research` subtree or directly in the shared `research` container.
4. Read only the already available artifacts needed to distinguish confirmed
   constraints, existing evidence, and known gaps. Do not conduct new research
   merely to populate the baseline.
5. Create or revise `research-initial-definitions.md` using the six required
   sections below and no additional level-two sections.
6. Keep the initial question explicitly refinable.
7. Resolve this skill's directory independently of the process current directory
   and run:

   ```text
   python "<this-skill-dir>/scripts/validate_initial_definitions.py" "<absolute-working-folder>" --repo-root "<absolute-repository-root>" --json
   ```
8. Return the validated repository root, research root, working folder, artifact
   path, and SHA-256. Stop with `block` if location or structure validation fails.
</process>

<required-structure>
## Context

Write one or two high-level paragraphs. Begin with the broader system and its
purpose, then state the local problem and why it matters. Do not describe the
research method or intended solution.

## Purpose

State what this document establishes and which later discovery, design, or
decision the research will inform. Do not describe execution.

## Research Question (Can be refined)

State one clear initial question and preserve its refinable status.

## Confirmed Product Constraints

Record only decisions, requirements, and boundaries established by the user or
an authoritative project artifact. Never promote assumptions into constraints.

## Current Evidence Baseline

Summarize information known before the research begins and cite existing
artifacts when available. Do not perform new research solely for this section.

## Known Gaps

Record missing knowledge, unclear boundaries, and unresolved concepts without
turning them into tasks or a research plan.
</required-structure>

<boundaries>
Keep confirmed facts, existing evidence, and unknowns distinct. Do not include:

- candidate vocabulary or initial hypotheses;
- methods, workstreams, source selection, or source plans;
- agent roles, tools, dispatch topology, or budgets;
- counterexamples, success conditions, stopping conditions, or output contracts;
- handoffs, implementation steps, findings, or proposed solutions.

This artifact is informational context. It is not a plan, dispatch sheet,
findings report, specification, or runtime authority.
</boundaries>

<output-contract>
Return:

```markdown
## Research Initial Definitions Result

- Status: pass | block
- Repository root: <absolute-path>
- Research root: <absolute-path-to-a-directory-named-research>
- Working folder: <absolute-path-beneath-research-root>
- Artifact: <working-folder>/research-initial-definitions.md
- SHA-256: <digest | unavailable>
- Validation: <command and result>
- Residue: <remaining ambiguity or none>
```
</output-contract>
