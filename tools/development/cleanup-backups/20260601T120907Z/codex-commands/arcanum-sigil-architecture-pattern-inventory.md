# Arcanum Sigil: architecture pattern inventory

<!-- arcanum:capability-id architecture-pattern-inventory -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command arcanum-sigil-architecture-pattern-inventory -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-arcanum-sigil-architecture-pattern-inventory-<UTC timestamp>`.
- `capability.id`: `architecture-pattern-inventory`
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

Run the installed Arcanum sigil `architecture-pattern-inventory` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `architecture-pattern-inventory`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/architecture-pattern-inventory/README.md

````markdown
# Architecture Pattern Inventory

Architecture Pattern Inventory is an Arcana sigil for mapping a repository's architecture and producing a reusable pattern inventory package.

It helps teams turn an existing or emerging codebase into a navigable architecture pack: an index, layer model, dependency rules, pattern library, concept cards, testing alignment, observability alignment, and inventory data that future agents can load selectively.

## Problem It Solves

Codebases accumulate architectural knowledge in scattered places: source folders, conventions, tests, docs, build scripts, route files, integration seams, and reviewer memory. Agents working in that codebase then either load too much context or miss the local patterns that should guide implementation.

This sigil solves that by mapping the architecture into a package that is explicit, selective, and maintainable.

## Use When

- a repository needs an architecture map,
- a project has repeated implementation patterns that should be inventoried,
- agents need selective context instead of reading the whole codebase,
- a team wants concept cards for backend, frontend, infrastructure, data, or workflow patterns,
- a codebase needs dependency rules, testing alignment, and observability alignment documented together,
- an existing architecture pack needs to be refreshed from code evidence.

## Do Not Use When

- the task is a small local bug fix,
- the repository has no reusable architecture conventions yet,
- the user only needs a single component explanation,
- the output should be a one-off code review rather than a maintained package.

## Output Package

By default, the sigil creates or updates:

```text
architecture/
  ARCHITECTURE.md
  ARCHITECTURE-PATTERN-LIBRARY.md
  pattern-library/
    README.md
    ARCHITECTURE-FOUNDATIONS.md
    DEPENDENCY-RULES.md
    TESTING-ALIGNMENT.md
    OBSERVABILITY-ALIGNMENT.md
    concepts/
      README.md
    relationships/
      README.md
    inventory/
      README.md
      architecture-inventory.schema.yml
```

## Subagent Mapping

For large repositories, this sigil should delegate independent mapper roles by concern:

- structure mapper,
- layer and dependency mapper,
- pattern inventorist,
- testing alignment mapper,
- observability alignment mapper.

Each mapper returns evidence-backed findings. The main agent synthesizes the package and decides what belongs in the canonical architecture inventory.

## Why This Is Arcana

The sigil coordinates repository exploration, evidence synthesis, package generation, and maintenance policy. It may use deterministic checks and bounded synthesis, but its primary behavior is lifecycle-level architecture discovery and inventory governance.
````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/architecture-pattern-inventory/SKILL.md

````markdown
---
name: architecture-pattern-inventory
description: "Use when: mapping a repository architecture and generating or refreshing a reusable architecture pattern inventory package with selective context, concept cards, dependency rules, testing alignment, and observability alignment."
argument-hint: "[--path <repo-root>] [--output <architecture-path>] [--update] [--subagents]"
tier: arcana
domain: architecture-inventory
version: 0.1.0
origin: created to generalize architecture mapping and pattern inventory packages across repositories
allowed-tools: Read, Write, Glob, Grep, Task
---

# Sigil: Architecture Pattern Inventory

<objective>
Map a repository's architecture and produce a reusable architecture pattern inventory package that future agents can use as selective implementation context.
</objective>

<logic-type>
Arcana: repository-scale architecture discovery, multi-concern synthesis, and inventory governance.
</logic-type>

<applicability>
Use this sigil for:

- creating a new architecture inventory package,
- refreshing an existing architecture package from code evidence,
- extracting reusable implementation patterns,
- documenting layer and dependency rules,
- creating concept and relationship cards,
- aligning architecture guidance with testing and observability expectations,
- preparing a codebase for agentic implementation with selective context loading.
</applicability>

<inputs>
Expected inputs, if available:

- repository root,
- existing architecture docs,
- source directories,
- tests,
- build or dependency configuration,
- routing or module boundaries,
- known architectural constraints,
- desired output path,
- whether existing package files should be updated or preserved.
</inputs>

<default-output>
If the user does not provide `--output`, create or update:

```text
architecture/
```

inside the target repository.
</default-output>

<subagent-contract>
Use mapper subagents for medium or large repositories when available.

Recommended mapper roles:

1. Structure mapper: identifies top-level folders, applications, packages, modules, and ownership boundaries.
2. Layer mapper: identifies layers, dependency direction, allowed and forbidden imports, and boundary seams.
3. Pattern inventorist: identifies repeated concepts, implementation motifs, naming conventions, and reusable cards.
4. Testing mapper: identifies how architectural units are verified and where gaps exist.
5. Observability mapper: identifies logs, metrics, traces, events, health checks, and operational signals tied to architecture.

Each mapper must return findings with evidence. The main agent synthesizes; mapper agents do not decide canonical package contents independently.
</subagent-contract>

<process>
1. Determine target repository and output path. Use `architecture/` by default.
2. Detect existing architecture package files and decide create vs update mode.
3. Gather minimal repository context: README, package/build config, source tree, tests, docs, dependency config, and existing architecture notes.
4. If repository size or ambiguity warrants it, delegate mapper subagents by concern using the subagent contract.
5. Identify the architecture layers actually present in the repository.
6. Identify dependency rules from code structure, import patterns, module boundaries, runtime boundaries, and tests.
7. Inventory recurring implementation patterns as concept cards. Prefer project-local evidence over generic categories.
8. Inventory relationships between concepts as relationship cards, including direction, contract, and evidence.
9. Produce or update the architecture package using the templates:
	- `ARCHITECTURE.md`,
	- `ARCHITECTURE-PATTERN-LIBRARY.md`,
	- `pattern-library/README.md`,
	- `pattern-library/ARCHITECTURE-FOUNDATIONS.md`,
	- `pattern-library/DEPENDENCY-RULES.md`,
	- `pattern-library/TESTING-ALIGNMENT.md`,
	- `pattern-library/OBSERVABILITY-ALIGNMENT.md`,
	- concept and relationship inventory files.
10. Keep the package selective: indexes should point to detail files; detail files should not duplicate the whole repository.
11. Validate markdown links and, when possible, verify that cited paths exist.
12. Return a summary of mapped layers, inventoried patterns, generated files, deferred gaps, and recommended next refresh trigger.
</process>

<quality-bar>
A successful execution of this sigil must:

- produce a navigable architecture package with an index and pattern-library entrypoint,
- ground layer and pattern claims in repository evidence,
- separate observed architecture from recommended architecture,
- include dependency rules, testing alignment, and observability alignment,
- make concept and relationship cards selectively loadable,
- preserve existing package content unless update scope is explicit,
- identify unresolved gaps rather than inventing missing architecture.
</quality-bar>

<anti-patterns>
Avoid:

- copying a generic architecture model over a repository without evidence,
- treating folder names as architecture without checking usage and dependencies,
- mixing product-specific terminology into a reusable package unless it is truly local to the target repo,
- creating one giant architecture document when selective context files are needed,
- letting mapper subagents write canonical files without synthesis,
- documenting ideal rules as if they are currently enforced,
- ignoring tests and observability when mapping implementation patterns.
</anti-patterns>

<output-contract>
Return:

```markdown
## Architecture Pattern Inventory Result

- Repository: <path>
- Package path: <path>
- Mode: created | updated
- Mapper pass: subagents | local fallback
- Layers mapped: <summary>
- Patterns inventoried: <count and categories>
- Relationships inventoried: <count and categories>
- Files changed: <paths>
- Gaps deferred: <summary>
- Validation: <checks performed>
- Next refresh trigger: <condition>
```
</output-contract>

````
