---
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: arcana/skill-transcriptor/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
name: skill-transcriptor
description: "Use when: converting a complete, coherent skill, prompt, command, or workflow into an Arcanum-compliant sigil package."
argument-hint: "<source-path-or-description> [--assess | --convert | --validate | --register-plan | --observe] [--target-name <name>] [--tier <formulae|transmutations|arcana>] [--output <path>]"
tier: arcana
domain: sigil-authoring
version: 0.1.0
origin: created to convert coherent external skills and workflows into Arcanum sigils without importing source-specific machinery
allowed-tools: Read, Write, Glob, Grep, Bash, AskUserQuestion, Agent
---

# Sigil: Skill Transcriptor

<objective>
Convert a complete, coherent source skill, prompt, command, or workflow into an Arcanum sigil package while preserving reusable behavior and removing source-specific coupling.
</objective>

<logic-type>
Arcana: source analysis, conversion gating, tier classification, neutral rewrite, package planning, validation, and observability.
</logic-type>

<modes>
- `assess`: decide whether the source is suitable for direct conversion.
- `convert`: produce a sigil package plan and draft artifact guidance.
- `validate`: check a converted sigil against Arcanum entry requirements.
- `register-plan`: propose registry, pack, and roadmap updates.
- `observe`: emit conversion telemetry for future reflection.
</modes>

<applicability>
Use this sigil when the source is already one coherent reusable capability and the main work is translation into Arcanum form.
</applicability>

<inputs>
Expected inputs, if available:

- source file or source description,
- desired target name,
- known target tier,
- local examples of successful use,
- source validation rules,
- source templates,
- desired output folder.
  </inputs>

<default-output>
If writing artifacts, prefer:

```text
<tier>/<target-name>/
```

If the user has not approved file creation, return a package plan and conversion report instead of creating files.
</default-output>

<process>
## Step 1 - Resolve Source And Target

1. Identify the source artifact and target repository.
2. Detect whether the source is a skill, prompt, command, workflow, or mixed document.
3. Capture the requested target name or derive a neutral candidate name.
4. Record source assumptions and missing context.

## Step 2 - Coherence Gate

5. Decide whether the source is one coherent reusable capability.
6. If the source contains multiple separable capabilities, stop direct conversion and recommend `skill-decomposer`.
7. If the source is coherent but has unclear boundaries, return `flag` with required clarification.
8. If the source is coherent and reusable, continue.

## Step 3 - Extract Behavior

9. Extract objective, triggers, modes, inputs, required context, process steps, gates, outputs, validation, tools, and observability.
10. Separate reusable behavior from source-specific vocabulary, local routing, private artifact names, and implementation details.
11. Preserve important gates even when source wording changes.

## Step 4 - Classify Tier

12. Classify the target as Formulae, Transmutations, or Arcana.
13. Record tier rationale and rejected tiers.
14. Escalate to `skill-decomposer` if tier ambiguity comes from multiple capabilities in the source.

## Step 5 - Plan Package

15. Define target folder, `README.md`, `SKILL.md`, templates, examples, registry updates, pack updates, and roadmap updates.
16. Draft neutral content guidance for each artifact.
17. Identify whether templates are required or optional.
18. Identify whether observability should use the general sigil hook, sigil-local telemetry, or no telemetry.

## Step 6 - Validate Conversion

19. Check Arcanum entry requirements: dedicated folder, human README, executable skill contract, Quality Bar, Anti-Patterns, output contract, and observability guidance.
20. Check neutral wording and coupling risks.
21. Check links, JSON templates, and registry references when files exist.
22. Return pass, flag, or block.
    </process>

<quality-bar>
A successful execution must:

- reject direct conversion when the source contains multiple separable capabilities,
- preserve reusable behavior while removing source-specific machinery,
- classify the target tier with rationale,
- define README, SKILL, template, registry, and validation expectations,
- include Quality Bar, Anti-Patterns, output contract, and observability guidance,
- route unclear boundaries to `skill-decomposer`,
- distinguish source facts, conversion inference, and authored target content.
  </quality-bar>

<anti-patterns>
Avoid:

- converting a tangled source as one large sigil,
- copying source frontmatter without checking compatibility,
- preserving private routing or local workflow names as canonical Arcanum vocabulary,
- treating tool permissions as portable without review,
- creating templates that do not support the output contract,
- registering the sigil before validation,
- replacing `sigil-development` lifecycle governance.
  </anti-patterns>

<observability>
When `.arcanum/observability/` exists, emit telemetry for:

- source type,
- target name,
- target tier,
- conversion accepted or rejected,
- decomposition recommended,
- coupling risks found,
- files planned,
- files created,
- validation result,
- blocker count.
  </observability>

<output-contract>
Return:

```markdown
## Skill Transcriptor Result

- Source: <path or description>
- Mode: assess | convert | validate | register-plan | observe
- Target name: <name>
- Target tier: formulae | transmutations | arcana | undecided
- Direct conversion: pass | flag | block
- Decomposition recommended: yes | no
- Coupling risks: <count>
- Files planned: <paths>
- Files created: <paths or none>
- Registry updates: <planned or none>
- Validation: pass | flag | block | not run
- Next action: <action>
```

</output-contract>
