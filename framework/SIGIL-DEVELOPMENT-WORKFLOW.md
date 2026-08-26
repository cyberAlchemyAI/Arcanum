# Sigil Development Workflow

This workflow defines how a sigil moves from an idea to a maintained capability in Arcanum.

The goal is to keep sigils clear, reusable, and governed without making the authoring process heavy. Each step should leave enough evidence that another person can understand why the sigil exists, where it belongs, and how to judge whether it works.

## Workflow Overview

| Stage                           | Purpose                                                         | Main Output                                | Gate                                                     |
| ------------------------------- | --------------------------------------------------------------- | ------------------------------------------ | -------------------------------------------------------- |
| 1. Candidate Capture            | Record the capability idea and the problem it should solve.     | Candidate note or draft folder.            | The problem is specific enough to evaluate.              |
| 2. Tier Classification          | Decide whether the sigil is Formulae, Transmutation, or Arcana. | Tier decision with rationale.              | The epistemic nature is clear.                           |
| 3. Intent Design                | Define objective, trigger conditions, scope, and authority.     | `SKILL.md` intent sections and candidate evidence under `development/`. | The sigil has a bounded purpose.                         |
| 4. Behavior Contract            | Write the executable `SKILL.md`.                                | Skill instruction contract.                | The agent can execute without hidden assumptions.        |
| 5. Quality And Failure Design   | Add Quality Bar and Anti-Patterns.                              | Reviewable success and failure boundaries. | The sigil can be accepted or rejected by evidence.       |
| 6. Template And Artifact Design | Add reusable templates only when needed.                        | Optional `templates/` files.               | Templates reduce ambiguity or repetition.                |
| 7. Observability Design         | Define telemetry signals and reflection triggers.               | Usage telemetry and reflection templates.  | Future usage can be observed and improved from evidence. |
| 8. Review And Validation        | Check structure, links, wording, and tier fit.                  | Review notes or edits.                     | The sigil is self-contained and product-neutral.         |
| 9. Trial Execution              | Run or simulate the sigil against a realistic task.             | Trial result and improvement notes.        | The sigil produces the intended output shape.            |
| 10. Promotion                   | Mark the sigil ready for library use.                           | Final folder in the correct tier.          | The review gates pass.                                   |
| 11. Observe And Reflect         | Emit usage telemetry and reflect when triggered.                | Telemetry signals and reflection reports.  | Iteration is based on evidence.                          |
| 12. Maintenance                 | Improve the sigil from observed use.                            | Changelog notes or targeted edits.         | Changes preserve the sigil's core contract.              |

## Stage 1 - Candidate Capture

Start with the problem, not the format.

Capture:

- working name,
- problem statement,
- who or what benefits from the sigil,
- example task that would trigger it,
- expected output or state change,
- why the capability should be reusable.

Do not create a full skill yet if the problem is still vague. A good candidate can answer: "What recurring agent behavior are we trying to make dependable?"

## Stage 2 - Tier Classification

Classify the sigil by epistemic nature:

- Formulae: rule-based, deterministic, repeatable.
- Transmutations: bounded synthesis, interpretation, or transformation.
- Arcana: autonomous orchestration, recursive inquiry, or multi-agent governance.

Use the tier concept files as placement references:

- [Formulae](../formulae/)
- [Transmutations](../transmutations/)
- [Arcana](../arcana/)

If the sigil appears to span tiers, choose the highest-authority behavior it performs. A workflow that uses deterministic checks but mainly coordinates multi-agent synthesis belongs in Arcana, not Formulae.

## Stage 3 - Intent Design

Create the skill folder under the selected tier:

```text
<tier>/<sigil-name>/
```

Keep the runtime package native to the target skill format. For Codex-native
skills, do not add a `README.md` or other auxiliary documentation inside the
skill folder. Express the human-reviewable intent through the `description`,
`objective`, ownership, inputs, and output contract in `SKILL.md`. Put candidate
notes, design rationale, and trial evidence under `development/`, which the
runtime installer excludes.

The intent surface should make clear:

- what the sigil is,
- what problem it solves,
- when to use it,
- when not to use it,
- expected inputs,
- expected outputs,
- why it belongs in its tier.

It should help someone decide whether the sigil should exist and when it should
be invoked without loading development history at runtime.

## Stage 4 - Behavior Contract

Create `SKILL.md` from [sigil-template.md](templates/sigil-template.md).

The skill file should define executable behavior, not just describe intent. Include:

- Codex-compatible frontmatter containing required `name` and `description`,
- objective,
- logic type,
- process,
- quality bar,
- anti-patterns,
- output contract.

Codex activation depends on `name` and `description`. Runtime-supported
optional keys such as `metadata`, `license`, and `allowed-tools` may be used
when the target host and the skill's behavior require them. Record Arcanum
repository-governance metadata in `SKILL.md.artifact.yml` rather than mixing it
into runtime frontmatter. The sidecar should carry the required artifact
metadata plus `tier`, `domain`, `version`, and `origin`.

The process should be specific enough that two agents following the same sigil produce comparable results.

## Stage 5 - Quality And Failure Design

Use [Quality Bar](QUALITY-BAR.md) and [Anti-Patterns](ANTI-PATTERNS.md) as authoring references.

The Quality Bar should make success observable. It should answer:

- What must be present?
- What makes the output reviewable?
- What constraints must be preserved?
- What result should fail review?

The Anti-Patterns should make misuse visible. They should answer:

- When should this sigil not be used?
- What shortcuts make the result untrustworthy?
- What scope expansion must be blocked?
- What output can look complete but still be wrong?

## Stage 6 - Template And Artifact Design

Add a `templates/` folder only when the sigil repeatedly creates a structured artifact.

Use templates for:

- report shapes,
- decision records,
- checklists,
- output schemas,
- preserved session records.

Avoid templates when they would duplicate the `SKILL.md` process or force a rigid structure onto a judgment-heavy task.

## Stage 7 - Observability Design

Design the signal path before the sigil is promoted.

Define:

- what counts as a meaningful execution,
- which outputs should be counted,
- which Quality Bar failures should be recorded,
- which Anti-Pattern hits should be recorded,
- which workflow gaps should trigger reflection,
- where usage telemetry and reflection reports should be stored.

Use the [Sigil Development](../arcana/sigil-development/) sigil when observability or reflection design is non-trivial.

Default reflection triggers:

- manual request,
- 5 meaningful executions,
- 10 generated outputs,
- 3 related workflow gaps,
- 1 severe workflow gap.

## Stage 8 - Review And Validation

Before promotion, review the sigil for:

- tier fit,
- product-neutral wording,
- clear trigger conditions,
- complete skill folder structure,
- working markdown links,
- no hidden dependency on local project names or private workflows,
- no contradiction between `SKILL.md`, loaded references, schemas, scripts,
  runtime metadata, and development evidence.

Recommended validation commands from the repository root:

```bash
find arcanum -path arcanum/.git -prune -o -name "*.md" -print0 | xargs -0 -n1 ./tools/check_markdown_links.sh
rg -n -i "<project-specific-term>|<source-specific-term>|<legacy-label>" arcanum --glob '!/.git/**'
```

Adapt the scan terms to the repository context. A clean scan means no accidental source-specific language remains.

## Stage 9 - Trial Execution

Run the sigil against a realistic task or simulate its execution from the written contract.

Check whether:

- the trigger condition is clear,
- required inputs are named,
- the process has no missing steps,
- the output contract is achievable,
- the Quality Bar can be evaluated,
- the Anti-Patterns catch likely misuse.

If the trial reveals ambiguity, revise the intent sections in `SKILL.md` when
the purpose is unclear and revise the executable process when behavior is
unclear. Keep trial artifacts under `development/`.

## Stage 10 - Promotion

A sigil is ready for library use when:

- it lives in the correct tier folder,
- its folder has a Codex-compatible `SKILL.md`, matching `agents/openai.yaml`
  when that surface is used, and governed metadata in the format supported by
  the artifact,
- optional templates are present only when useful,
- Quality Bar and Anti-Patterns are specific,
- validation passes,
- a realistic trial does not expose blocking ambiguity.

Promotion does not mean the sigil is final. It means the sigil is safe enough to use and learn from.

## Stage 11 - Observe And Reflect

After promotion, each meaningful execution should preserve enough telemetry for reflection.

Reflection can be executed:

- manually when a user asks for review or improvement,
- automatically when a configured usage or output threshold is reached,
- immediately when a workflow gap is identified.

The reflection pass should use an observer subagent when available. The observer identifies signals and recommends changes, but the main agent decides what to edit after synthesis.

Reflection should produce:

- signal summary,
- gap analysis,
- proposed iterations,
- rejected changes,
- contract preservation notes,
- next reflection trigger.

## Stage 12 - Maintenance

Maintain sigils through small, evidence-driven edits.

Update a sigil when:

- repeated use reveals a missing step,
- users select it for the wrong task,
- outputs fail the Quality Bar,
- Anti-Patterns do not catch a known misuse,
- templates drift from the behavior contract,
- telemetry shows repeated workflow gaps,
- reflection thresholds are reached,
- the tier classification no longer matches the actual behavior.

Avoid broad rewrites unless the sigil's core purpose has changed. If the purpose changes, treat the revision like a new candidate and rerun the workflow from Tier Classification.

## Development Checklist

- [ ] Candidate problem is specific and recurring.
- [ ] Tier classification is documented.
- [ ] Folder exists under the correct tier.
- [ ] `SKILL.md` explains intent and usage without auxiliary runtime docs.
- [ ] `SKILL.md` defines executable behavior.
- [ ] Governed metadata records tier, domain, version, and origin without
      violating runtime frontmatter constraints.
- [ ] Quality Bar is observable and tier-appropriate.
- [ ] Anti-Patterns block likely misuse.
- [ ] Templates exist only when they reduce ambiguity.
- [ ] Observability signals are defined.
- [ ] Manual, threshold-based, and gap-based reflection triggers are defined.
- [ ] Markdown links validate.
- [ ] Product-specific source wording has been removed.
- [ ] Trial execution or simulation has been reviewed.
- [ ] Reflection path is ready for future iteration.
