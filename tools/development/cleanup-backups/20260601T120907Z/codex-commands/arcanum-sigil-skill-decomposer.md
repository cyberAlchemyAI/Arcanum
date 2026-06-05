# Arcanum Sigil: skill decomposer

<!-- arcanum:capability-id skill-decomposer -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command arcanum-sigil-skill-decomposer -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-arcanum-sigil-skill-decomposer-<UTC timestamp>`.
- `capability.id`: `skill-decomposer`
- `capability.kind`: `sigil`
- `capability.tier`: `arcana`
- `capability.mode`: `command`
- `target_artifact`: this command file
- request summary: summarize the user request before execution.
- expected outputs: list intended artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- `OBSERVATION`
- `LEDGER`
- `REFLECTION_TRIGGER`
- `RECOMMENDATION`
- `DEDUPE_KEY`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.


## Objective

Run the installed Arcanum sigil `skill-decomposer` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `skill-decomposer`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/skill-decomposer/README.md

````markdown
# Skill Decomposer

Skill Decomposer is an Arcana sigil for extracting one reusable capability from a larger skill, prompt, workflow, command set, or mixed document.

It maps the source, identifies candidate capabilities, separates reusable behavior from local machinery, makes boundary decisions, and prepares a handoff package for [skill-transcriptor](../skill-transcriptor/) when a candidate is ready to become a sigil.

## Problem It Solves

Some sources are too broad to convert directly. They may contain several workflows, private routing rules, local assumptions, embedded validation logic, and useful fragments tangled together.

Skill Decomposer prevents over-conversion. It isolates the reusable part before authoring starts, so Arcanum gains focused sigils instead of oversized copies of source systems.

## Use When

- a source contains multiple possible sigils,
- the user points to one section inside a larger source,
- the reusable behavior is present but mixed with local mechanics,
- conversion should wait until a boundary is explicit,
- candidate capabilities need scoring before selection.

## Do Not Use When

- the source is already one coherent capability,
- the user only needs a direct package conversion,
- the fragment has too little context to judge safely,
- there is no reusable behavior beyond a local implementation detail.

Use [skill-transcriptor](../skill-transcriptor/) when the source is coherent enough for direct conversion.

## Outputs

Skill Decomposer can produce:

- source map,
- capability candidate list,
- boundary decision,
- coupling-risk review,
- decomposition report,
- handoff package for Skill Transcriptor.

## Relationship To Sigil Development

Skill Decomposer is an authoring helper, not a replacement for [sigil-development](../sigil-development/).

Use Skill Decomposer to define what should become a sigil. Use Skill Transcriptor to convert a coherent candidate. Use Sigil Development to govern lifecycle, telemetry, reflection, and later iteration.

## Why This Is Arcana

The sigil coordinates ambiguity, candidate discovery, boundary decisions, coupling risk, human gates, and handoff into conversion. It must stop safely when the reusable capability cannot be isolated.

````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/skill-decomposer/SKILL.md

````markdown
---
name: skill-decomposer
description: "Use when: extracting one reusable sigil capability from a larger or tangled skill, prompt, workflow, command set, or mixed document."
argument-hint: "<source-path-or-description> [--map | --extract | --boundary | --handoff | --validate | --observe] [--candidate <name>] [--output <path>]"
tier: arcana
domain: sigil-authoring
version: 0.1.0
origin: created to isolate reusable sigil candidates from broad or source-coupled workflows before conversion
allowed-tools: Read, Write, Glob, Grep, Bash, AskQuestions, Task
---

# Sigil: Skill Decomposer

<objective>
Extract one coherent reusable capability from a larger or tangled source and prepare it for sigil conversion without importing source-specific machinery.
</objective>

<logic-type>
Arcana: source mapping, candidate discovery, boundary judgment, coupling-risk review, decision gating, and handoff orchestration.
</logic-type>

<modes>
- `map`: identify sections, behaviors, roles, dependencies, and local vocabulary in the source.
- `extract`: define one target capability and its reusable core.
- `boundary`: decide what belongs inside or outside the candidate sigil.
- `handoff`: produce a package plan for `skill-transcriptor`.
- `validate`: verify the candidate is coherent, reusable, and not source-coupled.
- `observe`: emit decomposition telemetry for reflection.
</modes>

<applicability>
Use this sigil when the source is not cleanly one capability, or when the user points to one fragment of a larger source.
</applicability>

<inputs>
Expected inputs, if available:

- source file, folder, or fragment,
- user's intended extraction target,
- known source context,
- candidate names,
- source examples,
- target tier guess,
- conversion constraints.
  </inputs>

<default-output>
Return a decomposition report and handoff package. Do not create the final sigil package unless the user explicitly asks and the boundary decision is pass.
</default-output>

<process>
## Step 1 - Map Source

1. Identify source scope and available context.
2. Map sections, behaviors, roles, dependencies, local vocabulary, gates, and outputs.
3. Preserve source boundaries so extraction decisions remain reviewable.

## Step 2 - Identify Candidates

4. List candidate reusable capabilities.
5. Score each candidate for coherence, reuse value, coupling risk, tier clarity, and missing context.
6. Reject implementation details that do not generalize into reusable behavior.
7. Avoid splitting one coherent source into too many tiny candidates.

## Step 3 - Select Or Gate

8. Select the strongest candidate when evidence is clear.
9. Ask a human decision only when multiple candidates are equally plausible or the extraction target is ambiguous.
10. Block if the source fragment lacks enough context to define a safe boundary.

## Step 4 - Define Boundary

11. Define included behavior, excluded behavior, required context, source risks, target tier, and handoff assumptions.
12. Classify source material as keep, rewrite, reject, defer, or needs decision.
13. Preserve important gates from the parent workflow.
14. Remove source-specific names from the target public contract.

## Step 5 - Handoff

15. Produce a handoff package for `skill-transcriptor` when the candidate is coherent.
16. Include target name, tier recommendation, objective, inputs, modes, process outline, outputs, quality risks, anti-patterns, templates needed, and validation notes.
17. If the boundary remains ambiguous, return a block with the minimum decision needed.
    </process>

<quality-bar>
A successful execution must:

- preserve enough source context to justify extraction,
- identify candidate capabilities before selecting one,
- score coherence, reuse value, coupling risk, and tier clarity,
- define included and excluded behavior explicitly,
- reject local implementation details that are not reusable behavior,
- prevent final sigil authoring when boundaries are ambiguous,
- produce a clear handoff to `skill-transcriptor` when ready,
- avoid replacing `sigil-development` lifecycle governance.
  </quality-bar>

<anti-patterns>
Avoid:

- extracting from a fragment with no surrounding context,
- turning every source section into a separate sigil,
- hiding boundary uncertainty,
- losing gates from the parent workflow,
- keeping source-specific routing, project names, or artifact names as canonical terms,
- creating the final sigil before the boundary decision is explicit,
- treating implementation details as reusable capabilities.
  </anti-patterns>

<observability>
When `.arcanum/observability/` exists, emit telemetry for:

- source type,
- candidate count,
- selected candidate,
- rejected candidates,
- coupling risks found,
- boundary confidence,
- decision gate needed,
- handoff target,
- validation result.
  </observability>

<output-contract>
Return:

```markdown
## Skill Decomposer Result

- Source: <path or description>
- Mode: map | extract | boundary | handoff | validate | observe
- Candidates found: <count>
- Selected candidate: <name or none>
- Target tier: formulae | transmutations | arcana | undecided
- Boundary decision: pass | flag | block
- Coupling risks: <count>
- Handoff to skill-transcriptor: yes | no
- Files planned: <paths or none>
- Validation: pass | flag | block | not run
- Next action: <action>
```

</output-contract>

````
