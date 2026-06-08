---
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: arcana/architecture-pattern-inventory/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
name: architecture-pattern-inventory
description: "Use when: mapping a repository architecture and generating or refreshing a reusable architecture pattern inventory package with selective context, concept cards, dependency rules, testing alignment, and observability alignment."
argument-hint: "[--path <repo-root>] [--output <architecture-path>] [--update] [--subagents]"
tier: arcana
domain: architecture-inventory
version: 0.1.0
origin: created to generalize architecture mapping and pattern inventory packages across repositories
allowed-tools: Read, Write, Glob, Grep, Agent
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
