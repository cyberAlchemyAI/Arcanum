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