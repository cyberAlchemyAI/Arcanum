## Agent 1 — Lifecycle and creation-process cartography

Preflight evidence: `research/unified-skill-model/research-initial-definitions.md` validated `pass`; SHA-256 `2704196c95469e06ee2d74aa4e0e6c13395ecb7ec9a22c7b0246a7e1c8787684`. Investigation was read-only.

## Concise lifecycle/state model

The strongest documentary reconstruction is:

```text
idea
  → candidate capture
  → tier classification
  → intent/contract/quality/template/observability design
  → review and validation
  → realistic trial
  → promotion readiness
  → registry release/public bundle generation
  → runtime projection and installation
  → discovery/invocation
  → observation/reflection
  → targeted maintenance
       ↘ purpose-changing revision loops back to classification
```

Evidence: the twelve prescribed stages are enumerated in `framework/SIGIL-DEVELOPMENT-WORKFLOW.md:7-22`; trial and promotion conditions are elaborated at `:183-213`; maintenance loops purpose changes back to classification at `:236-251`.

The executable model is materially smaller:

```text
tier directory + SKILL.md
  ├→ bootstrap selection/install
  ├→ public registry build, unless development/REGISTRY-HOLD.md exists
  └→ generated runtime package
       → local runtime discovery by exact .agents/skills/<id>/SKILL.md
```

Evidence: bootstrap selects every first-level tier directory containing `SKILL.md` at `tools/bootstrap_arcanum.sh:420-434`; the public builder discovers the same directory shape and skips only an explicit hold at `tools/build-skill-registry.py:578-598`; runtime resolution requires an exact installed `SKILL.md` path at `tools/arcanum:489-501`.

No executable consumer located reads a unified lifecycle state or promotion receipt before install/publication.

## RQ-01 — Authoritative initiation entry point

**Exact scope:** initiation of a new reusable sigil, including direct creation, pre-authoring, and conversion/extraction helpers.

**Status:** answered: there is no single mandatory initiation entry point. `sigil-development` is the authoritative lifecycle owner once work is recognized as sigil creation, while `invoke` is an optional authoring front door and other helpers serve specialized intake cases.

**Supported answer:**

- Repository contribution guidance says to follow the framework workflow and template directly; it does not require invoking a capability first (`README.md:231-240`). This permits manual initiation.
- Repository lifecycle guidance assigns creation, validation, observation, reflection, and iteration to `sigil-development`, while `invoke` prepares definition/design/plan/handoff context and must not absorb lifecycle authority (`README.md:148-161`).
- `sigil-development` explicitly calls itself lifecycle owner and owns contract mutation, experiment harness, validation, observability, reflection, iteration, and promotion readiness (`arcana/sigil-development/SKILL.md:50-59`).
- `invoke` describes itself as an authoring front door, not lifecycle owner (`spells/invoke/README.md:20-26`), and the explicit new-sigil chain is `invoke … -> sigil-development --new/--update` (`spells/invoke/README.md:112-129`).
- `skill-decomposer` is only for tangled sources and hands coherent candidates to `skill-transcriptor` (`arcana/skill-decomposer/SKILL.md:22-32,78-95`).
- `skill-transcriptor` handles coherent-source conversion but explicitly must not replace sigil-development governance (`arcana/skill-transcriptor/SKILL.md:22-32,110-119`).

**Contrary evidence:** the phrase “authoring front door” could be read as making `invoke` the initiator, and generated repository instructions tell agents to use `spells/invoke/` for lifecycle authoring artifacts (`tools/bootstrap_arcanum.sh:1393-1405`). But the same canonical Invoke contract says a clearly identified sigil should be routed early and assigns creation authority to `sigil-development` (`spells/invoke/README.md:112-128,157`).

**Residual uncertainty:** no dispatcher-level rule was found that deterministically chooses direct `sigil-development --new` versus an Invoke pre-pass.

**Boundary:** this establishes authority and available entry paths, not which future unified creation UX should be chosen.

## RQ-02 — Recognized lifecycle states

**Exact scope:** states or state-like distinctions applied to a skill by authoritative documents and executable consumers.

**Status:** partial: documentary states are identifiable, but they do not form one coherent state schema and are not jointly consumed executably.

**Documentary state families:**

- Twelve workflow stages: candidate capture through maintenance (`framework/SIGIL-DEVELOPMENT-WORKFLOW.md:7-22`).
- Validation promotion targets: `candidate`, `local reusable`, `library reusable`, `registry release` (`framework/VALIDATION-EXPERIMENT-PROTOCOL.md:18-33`).
- Validation verdicts: `pass`, `flag`, `block` (`framework/VALIDATION-EXPERIMENT-PROTOCOL.md:100-106`).
- Sigil-development operating modes: `new`, `update`, `observe`, `reflect` (`arcana/sigil-development/SKILL.md:133-160`).
- Lifecycle progress suggestions after bounded implementation: `validate`, `observe`, `reflect`, `iterate`, `promote` (`arcana/sigil-development/SKILL.md:75-94`).
- General governed-artifact statuses: `candidate`, `reviewed`, `canonical`, `deprecated`, `generated`, `local-runtime` (`framework/ARTIFACT-METADATA-CONSTITUTION.md:40-50`). These are artifact-level metadata vocabulary, not proven to be a skill runtime state machine.
- Registry availability is a documentary release state: registry entries are supposed to represent reusable, stable artifacts (`registry/README.md:15-26`).

**Executable states actually observed:**

- discoverable canonical package: directory exists under a named tier and contains `SKILL.md` (`tools/bootstrap_arcanum.sh:425-432`);
- public-release eligible: same, unless `development/REGISTRY-HOLD.md` exists (`tools/build-skill-registry.py:578-598`);
- installed/generated: runtime package has generated provenance, including `surface_kind`, runtime, canonical source, generator, and mutation policy (`tools/bootstrap_arcanum.sh:844-857`);
- invocable: exact `.agents/skills/<selected>/SKILL.md` exists, or a legacy command exists (`tools/arcanum:489-501`).

**Contrary evidence:** the validation protocol says registry entry is blocked until validation passes (`framework/VALIDATION-EXPERIMENT-PROTOCOL.md:35-49,51-67`), suggesting a coherent transition. The builder, however, does not read the verdict.

**Residual uncertainty:** artifact sidecars can contain `lifecycle_status`, but no inspected install, registry-build, or invocation code used it to determine a skill state.

**Boundary:** directory placement is reported only as an executable discovery predicate, not as runtime type or semantic lifecycle state.

## RQ-03 — Effective transition conditions

**Exact scope:** what makes changes between candidate, validated, promoted, registered, generated, installed, observed, and maintained states effective.

**Status:** partial: prescribed gates are explicit, while executable effectiveness is governed by separate file and command predicates.

**Prescribed transitions:**

- Candidate → contract drafting: the problem must be specific; vague candidates should not become full skills (`framework/SIGIL-DEVELOPMENT-WORKFLOW.md:24-37`).
- Draft → validation/trial: structure, links, trigger conditions, product neutrality, dependency consistency, and realistic execution must be reviewed (`framework/SIGIL-DEVELOPMENT-WORKFLOW.md:161-198`).
- Trial → promotion readiness: correct placement, compatible contract/metadata, specific quality/failure boundaries, passing validation, and no blocking ambiguity (`framework/SIGIL-DEVELOPMENT-WORKFLOW.md:200-213`).
- Development evidence → canonical source: a promotion patch must name owner, source evidence, durable claim, rationale, validation, and approval; then pass the owner gate (`framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md:19-24,49-72`).
- Canonical candidate → registry release: validation report verdict must be `pass` before registry update (`framework/VALIDATION-EXPERIMENT-PROTOCOL.md:51-67`).
- Use → reflection: manual request, 5 executions, 10 outputs, 3 related gaps, or 1 severe gap (`arcana/sigil-development/SKILL.md:186-204`).
- Maintenance → new candidate: core-purpose changes rerun from tier classification (`framework/SIGIL-DEVELOPMENT-WORKFLOW.md:236-251`).

**Executable transition predicates:**

- canonical filesystem package → selected for install: first-level tier directory plus `SKILL.md`; dependencies are added from the TSV (`tools/bootstrap_arcanum.sh:420-456`);
- package → published bundle: discoverable contract and no `development/REGISTRY-HOLD.md`; duplicate IDs and invalid dependency closure fail (`tools/build-skill-registry.py:578-621`);
- canonical package → runtime projection: explicit bootstrap/profile generation (`tools/bootstrap_arcanum.sh:1189-1227,1289-1329`);
- staged projection → consuming repository: explicit `--apply`; the sync uses checksum replacement and rollback on failure (`tools/sync-generated-skill-package.sh:184-209,211-258`);
- installed package → invocable by deterministic tool: exact skill file exists (`tools/arcanum:489-501`).

**Contrary evidence:** registry rules say a candidate should not become listed merely because it exists and requires validation plus lifecycle approval (`README.md:169-177`). The executable public builder admits by file presence/absence of a hold instead.

**Residual uncertainty:** human approval may be represented in development reports or PR review, but no common machine-readable transition receipt is consumed across the lifecycle.

**Boundary:** “effective” distinguishes documentary authorization from actual state changes produced by repository scripts.

## RQ-04 — Executably enforced versus conventional guarantees

**Exact scope:** lifecycle guarantees from authoring through maintenance, tested against executable consumers.

**Status:** answered for the inspected lifecycle paths.

### Executably enforced

- Dependency manifest validity is a blocking install precondition (`tools/bootstrap_arcanum.sh:397-410,2148-2151`).
- Selected sigils must resolve to a tier path with a `SKILL.md`; dependencies are transitively queued (`tools/bootstrap_arcanum.sh:420-456`).
- Generated packages receive canonical-source and regeneration provenance (`tools/bootstrap_arcanum.sh:844-857,1189-1227`).
- `development/` is excluded from generated runtime support; other support directories are copied (`tools/bootstrap_arcanum.sh:885-935`).
- Claude generated packages receive a blocking structural validation when the validator exists; absence of the validator only warns (`tools/bootstrap_arcanum.sh:1456-1468`).
- Public registry generation blocks duplicate IDs and missing dependency endpoints and honors `REGISTRY-HOLD.md` (`tools/build-skill-registry.py:578-608`).
- Selective sync requires one valid capability ID, stages through bootstrap, verifies `SKILL.md`, refuses symlink destinations, and rolls back failed apply (`tools/sync-generated-skill-package.sh:86-99,116-177,211-258`).
- Deterministic invocation resolves only an installed native `SKILL.md` or legacy command (`tools/arcanum:489-501`).

### Documentary/conventional only in these paths

- specific candidate problem;
- tier rationale;
- required intent/body sections;
- Quality Bar and Anti-Patterns quality;
- observability design;
- realistic positive and negative trials;
- passing validation verdict;
- promotion approval;
- registry Markdown update;
- reflection threshold execution;
- preservation of the core contract during maintenance.

These are prescribed in `framework/SIGIL-DEVELOPMENT-WORKFLOW.md:24-22` collectively, with validation/trial/promotion at `:161-213`, and in the release protocol at `framework/VALIDATION-EXPERIMENT-PROTOCOL.md:35-67`; none is read by the inspected bootstrap or public registry builder.

**Concrete divergence:** `registry/SIGILS.md` lists Sigil Development as available (`registry/SIGILS.md:45`), while the package has no `development/VALIDATION.md` in the inspected tree. More broadly, the builder’s only explicit pre-publication state exclusion is `development/REGISTRY-HOLD.md` (`tools/build-skill-registry.py:585-590`).

**Contrary evidence:** individual skills can own strong package-specific validators and experiment harnesses. That proves local enforcement is possible, but not a common lifecycle guarantee.

**Residual uncertainty:** CI configuration outside the requested surfaces may invoke additional validators; no evidence inspected established a repository-wide promotion gate.

**Boundary:** this is not a quality judgment on existing skills; it is a comparison of prescribed common guarantees with common executable consumers.

## RQ-05 — Propagation from canonical contract to derived artifacts

**Exact scope:** registry pages/downloads, repo and personal runtime packages, aliases/adapters, installations, and discovery surfaces derived from canonical skill contracts.

**Status:** answered: there is no universal automatic propagation rule. Propagation is per-surface and occurs only through direct linkage or an explicit rebuild/regeneration/sync/install operation.

**Rules found:**

- Framework rule: after canonical promotion, update required indexes, registries, runtime copies, downloads, or drift audits; a source update is incomplete if its lookup layer remains stale (`framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md:74-84`).
- Registry documentation requires manual registry update on add/rename/retire/tier move/material purpose change (`registry/SIGILS.md:135-139`).
- Public downloads/page require rerunning the builder whenever skills change; generated rows must not be hand-edited (`tools/build-skill-registry.py:2-10`).
- Generated runtime packages declare `mutation_policy: regenerate-from-canonical-source` (`tools/bootstrap_arcanum.sh:844-857`).
- Bootstrap reconstructs generated `SKILL.md` from the canonical source and copies runtime support excluding `development/` (`tools/bootstrap_arcanum.sh:1189-1227,885-935`).
- Selective propagation is explicit preview/apply through `sync-generated-skill-package.sh`; without `--apply`, nothing changes (`tools/sync-generated-skill-package.sh:6-30,184-209,211-258`).
- Full installation is also explicit through bootstrap profiles (`tools/bootstrap_arcanum.sh:1384-1414`).

**No freshness guarantee found:** no watcher, digest comparison, timestamp gate, or install/publication check ensures a derived artifact reflects the current canonical bytes. Provenance states the intended regeneration policy but does not itself trigger regeneration.

**Current discovery-surface divergence:**

- Documentation says `.agents/skills/` consists of symlinked canonical folders (`.agents/README.md:3-5`; `README.md:181-189`).
- The inspected tree contains multiple shapes: `.agents/skills/sigil-development:1` is a one-line path pointer, while `.agents/skills/low-resolution-explanation/SKILL.md:8-12` is a versioned wrapper that delegates to canonical source, and generated packages such as `.agents/skills/research/SKILL.md:1-7` carry regeneration provenance.
- `tools/arcanum` only recognizes `.agents/skills/<id>/SKILL.md` (`tools/arcanum:489-501`), so a one-line pointer file is not equivalent to an installed runtime package for that executable consumer.

**Contrary evidence:** a true filesystem symlink would reflect canonical edits immediately. The documentary claim is therefore a valid possible propagation mechanism, but it does not describe all artifacts currently present.

**Residual uncertainty:** host-native Codex discovery may interpret some repository pointer forms independently of `tools/arcanum`; the deterministic repository tool does not.

**Boundary:** this identifies present propagation mechanics and drift risk, not a proposed replacement strategy.

## RQ-00 contribution — Current properties that remain distinguishable

Only evidence relevant to the program question:

- Canonical capability behavior and development evidence have different authority: development artifacts are proposal/evidence; canonical artifacts are authority (`framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md:19-24,28-47`).
- Lifecycle authoring, lifecycle mutation, bounded implementation, experiment mechanics, registry cataloging, runtime projection, and observation have distinct owners:
  - Invoke authoring: `spells/invoke/README.md:112-121`
  - Sigil lifecycle mutation/promotion readiness: `arcana/sigil-development/SKILL.md:50-59`
  - Task execution and experiment mechanics: `arcana/sigil-development/SKILL.md:62-94`
  - Registry catalog versus framework governance: `registry/README.md:37-39`
  - Native runtime projection versus legacy command compatibility: `arcana/sigil-runtime-installer/SKILL.md:31-35`
- Canonical source, generated runtime package, alias package, installed surface, public download, registry catalog entry, telemetry evidence, and development evidence are observably different roles even though all may relate to one capability.
- Directory placement currently drives install/publication tier identity, but that is an executable routing heuristic, not evidence that directory placement is the capability’s intrinsic runtime type (`tools/bootstrap_arcanum.sh:425-432`; `tools/build-skill-registry.py:26-31,578-598`; `tools/arcanum:385-400`).

Overall answer for RQ-00 within this workstream: the lifecycle requires preserving distinctions among authority, evidence, release status, generated projection, installation, runtime availability, and observation. The present three-directory category is used operationally for discovery and labeling, but the lifecycle evidence does not justify treating placement itself as runtime type.
## Agent 2 — Schema and authority-surface cartography

Research preflight passed read-only. Baseline SHA-256: `2704196c95469e06ee2d74aa4e0e6c13395ecb7ec9a22c7b0246a7e1c8787684`.

## RQ-00 contribution

The current Arcanum “skill contract” is not one schema. It is a stack of consumer-specific contracts:

1. runtime activation and instruction contract in `SKILL.md`;
2. repository governance metadata, usually intended for `SKILL.md.artifact.yml`;
3. optional product/UI metadata in `agents/openai.yaml`;
4. inter-skill installation edges in `registry/SIGIL-DEPENDENCIES.tsv`;
5. directory-derived category and source routing;
6. generated-package provenance and runtime rewrites.

These must remain distinguishable because different consumers read different surfaces and resolve conflicts differently. No inspected artifact establishes a global precedence across all layers.

## Representative package inventory

| Tier/package | Witnessed shape | Classification |
|---|---|---|
| `formulae/anti-bias-vector-composition` | Only required native `name`/`description`; prose body rather than the common XML-like section template ([SKILL.md:1-16](../../formulae/anti-bias-vector-composition/SKILL.md#L1)) | Runtime-valid minimal shape; governance and UI sidecars absent |
| `formulae/dispatch-spec` | Rich legacy top-level fields: `argument-hint`, `tier`, `domain`, `version`, `origin`, `allowed-tools` ([SKILL.md:1-10](../../formulae/dispatch-spec/SKILL.md#L1)) | Runtime fields mixed with descriptive/repository fields |
| `transmutations/lens-router` | Minimal runtime frontmatter ([SKILL.md:1-4](../../transmutations/lens-router/SKILL.md#L1)); full governance sidecar ([artifact:1-19](../../transmutations/lens-router/SKILL.md.artifact.yml#L1)); UI metadata ([openai.yaml:1-4](../../transmutations/lens-router/agents/openai.yaml#L1)) | Closest witnessed package to the documented layered model |
| `transmutations/evidence-grounded-diagrams` | UI metadata additionally contains invocation policy ([openai.yaml:1-7](../../transmutations/evidence-grounded-diagrams/agents/openai.yaml#L1)); bespoke validator requires exact package files and checks its default prompt ([validate_skill_package.py:15-53](../../transmutations/evidence-grounded-diagrams/scripts/validate_skill_package.py#L15), [118-123](../../transmutations/evidence-grounded-diagrams/scripts/validate_skill_package.py#L118)) | Package-local enforcement beyond the repository-wide minimum |
| `arcana/review` | Minimal runtime frontmatter plus structured governed body ([SKILL.md:1-22](../../arcana/review/SKILL.md#L1)) and optional UI metadata | Modern native runtime shape without a governance sidecar |
| `arcana/research` | Canonical file currently contains the older operating-guide contract ([SKILL.md:1-17](../../arcana/research/SKILL.md#L1)), while the repo Codex projection contains different metadata, description, and body ([projection:1-20](../../.agents/skills/research/SKILL.md#L1)) | Direct witnessed canonical/projection divergence |

The filesystem inventory found 4 canonical packages under `formulae/`, 10 under `transmutations/`, and 45 under `arcana/`. Only the three router packages currently have `SKILL.md.artifact.yml`; `agents/openai.yaml` is also non-uniform. These counts are direct directory observations; absent files have no line locator.

## Schema-layer matrix

| Layer/property | Required/optional | Nature | Actual consumer/enforcement |
|---|---|---|---|
| Package folder + `SKILL.md` | Required | Identity/discovery | Native skill contract requires `SKILL.md` ([skill-creator:58-69](installed-native-skill-creator/SKILL.md#L58)); bootstrap discovers only tier directories containing it ([bootstrap:425-432](../../tools/bootstrap_arcanum.sh#L425)) |
| `name` | Required | Runtime-consumed identity/routing | Native contract says it and folder name are required/matching ([skill-creator:75-80](installed-native-skill-creator/SKILL.md#L75), [239-242](installed-native-skill-creator/SKILL.md#L239)); native validator enforces syntax ([quick_validate.py:51-75](installed-native-skill-creator/scripts/quick_validate.py#L51)) |
| `description` | Required | Runtime-consumed trigger | Native contract identifies it as the activation mechanism ([skill-creator:75-80](installed-native-skill-creator/SKILL.md#L75)); validator checks presence/type/length ([quick_validate.py:51-88](installed-native-skill-creator/scripts/quick_validate.py#L51)) |
| Markdown body | Required | Runtime-consumed instructions | Loaded after triggering; no native semantic section schema ([skill-creator:75-80](installed-native-skill-creator/SKILL.md#L75)) |
| `metadata`, `license`, `allowed-tools` | Optional | Runtime-specific | Allowed by native validator ([quick_validate.py:40-48](installed-native-skill-creator/scripts/quick_validate.py#L40)); Claude generator rewrites two tool names ([bootstrap:1092-1153](../../tools/bootstrap_arcanum.sh#L1092)) |
| Legacy top-level `tier/domain/version/origin/argument-hint` | Present but not native-valid | Descriptive/registry input | Native validator rejects keys outside its allowlist; registry builder nevertheless consumes `domain/version` ([build registry:124-147](../../tools/build-skill-registry.py#L124)) |
| `SKILL.md.artifact.yml` | Documentary requirement for governed skills; actually non-uniform | Governance/descriptive, partially validated | Constitution assigns governance fields to it ([constitution:104-110](../../framework/ARTIFACT-METADATA-CONSTITUTION.md#L104)); validator checks required fields/status when invoked ([validator:271-312](../../tools/validate-artifact-metadata.py#L271)) |
| `agents/openai.yaml` | Recommended/optional | Product UI and invocation policy | Native contract calls it UI-facing ([skill-creator:82-89](installed-native-skill-creator/SKILL.md#L82)); extended config is machine/harness-facing ([openai_yaml.md:1-25](installed-native-skill-creator/references/openai_yaml.md#L1)) |
| `agents/openai.yaml.dependencies.tools` | Optional | External tool dependency declaration | Product schema currently supports MCP dependencies ([openai_yaml.md:16-22](installed-native-skill-creator/references/openai_yaml.md#L16), [42-46](installed-native-skill-creator/references/openai_yaml.md#L42)) |
| `SIGIL-DEPENDENCIES.tsv` | Optional edges, authoritative when dependency exists | Installation/distribution routing | Registry rules require declaring hard dependencies ([registry README:28-35](../../registry/README.md#L28)); bootstrap validates and auto-adds closure ([bootstrap:397-456](../../tools/bootstrap_arcanum.sh#L397)) |
| Generated provenance | Derived | Projection traceability | Current generator adds runtime, canonical source, alias, generator, mutation policy ([bootstrap:844-857](../../tools/bootstrap_arcanum.sh#L844)) |
| Registry tier/path | Derived from location | Publication category/routing | Builder receives tier from directory and constructs path from tier plus folder ([build registry:114-149](../../tools/build-skill-registry.py#L114)) |

## RQ-06 — Conflict precedence

**Scope:** Canonical location, runtime frontmatter/body, sidecars, agent metadata, dependencies, registries, and generated packages.

**Status:** Partial. Consumer-specific precedence is answered; no global precedence exists.

**Findings:**

- Bootstrap resolves duplicate names in hard-coded order `formulae`, then `transmutations`, then `arcana` ([bootstrap:372-380](../../tools/bootstrap_arcanum.sh#L372)). In contrast, the public registry builder rejects duplicate released IDs rather than choosing one ([build registry:595-597](../../tools/build-skill-registry.py#L595)).
- Registry extraction prefers `SKILL.md` over `README.md`; frontmatter `name` over body canonical ID over folder; frontmatter description over body purpose/first paragraph; and frontmatter `version/domain` over sidecar values. Tier and published path are directory-derived ([build registry:114-149](../../tools/build-skill-registry.py#L114)).
- The artifact validator prefers embedded artifact metadata appropriate to the file format; it falls back to a sidecar only when embedded artifact metadata is absent ([validate-artifact-metadata.py:239-268](../../tools/validate-artifact-metadata.py#L239)).
- The dependency manifest is separately authoritative for selective-install closure; it does not override `SKILL.md` semantics ([validate-sigil-dependencies.py:47-79](../../tools/validate-sigil-dependencies.py#L47)).
- `agents/openai.yaml` governs machine/UI presentation and invocation policy, not the agent instruction body ([openai_yaml.md:1-3](installed-native-skill-creator/references/openai_yaml.md#L1)).
- A thin adapter may explicitly delegate semantic authority to canonical source, as `lens-router` does ([adapter:8-12](../../.agents/skills/lens-router/SKILL.md#L8)). A generated full copy does not resolve conflicts dynamically; `research` presently claims `arcana/research/SKILL.md` as source while containing a different body ([projection:2-20](../../.agents/skills/research/SKILL.md#L2), contrary canonical [1-17](../../arcana/research/SKILL.md#L1)).

**Contrary evidence:** The artifact constitution does state a precedence for constitution-pack composition—task-specific, artifact type, domain/capability, framework, fallback—but this governs selected constitutions, not the whole skill schema ([constitution:141-154](../../framework/ARTIFACT-METADATA-CONSTITUTION.md#L141)).

**Residual uncertainty:** Host-internal conflict behavior when folder name and frontmatter name differ was not directly instrumented. Repository validators imply intended behavior but only Claude has a wired generated-surface gate.

**Boundary:** This does not infer authority from field presence; precedence is reported only where an executable or explicit delegation rule was found.

## RQ-07 — Common minimum identity and routing properties

**Scope:** Codex, Claude, and GitHub Copilot native skill projections produced by current bootstrap tooling.

**Status:** Partial.

**Answer:** The defensible common minimum is:

- one folder containing `SKILL.md`;
- frontmatter `name`;
- frontmatter `description`;
- a Markdown instruction body;
- folder/name correspondence for hosts whose validator checks it.

The native Codex contract explicitly identifies `SKILL.md`, `name`, `description`, and Markdown instructions as required ([skill-creator:58-80](installed-native-skill-creator/SKILL.md#L58)). The native validator enforces YAML shape, the allowed top-level property set, name syntax, and description bounds ([quick_validate.py:17-88](installed-native-skill-creator/scripts/quick_validate.py#L17)). Claude’s repository validator additionally enforces folder/name equality, kebab case, maximum length, description, tool vocabulary, and sibling `skills:` references ([validate-claude-skills.sh:73-116](../../tools/validate-claude-skills.sh#L73)).

Routing is split:

- `name`/`description` route activation;
- folder location routes discovery;
- `SIGIL-DEPENDENCIES.tsv` routes installation closure;
- `agents/openai.yaml` optionally controls UI presentation and implicit-invocation policy.

**Contrary evidence:** Many legacy canonical packages use top-level keys outside the native validator’s allowed set; `dispatch-spec` is a direct example ([SKILL.md:1-10](../../formulae/dispatch-spec/SKILL.md#L1)). Current bootstrap copies source frontmatter while injecting metadata and only rewrites `name`/Claude tool tokens ([bootstrap:1092-1153](../../tools/bootstrap_arcanum.sh#L1092), [1189-1227](../../tools/bootstrap_arcanum.sh#L1189)).

**Residual uncertainty:** There is no equivalent repository CI validator for generated Codex or Copilot packages. Therefore the common minimum is supported by native contract and generator shape, but effective host enforcement is proven only for Claude.

**Boundary:** External tool dependencies in `agents/openai.yaml` and sigil-to-sigil installation dependencies are distinct contracts and are not part of the minimum skill identity.

## RQ-08 — Required body semantics

**Scope:** Recognition as a runtime skill versus documentary recognition as an Arcanum-governed skill.

**Status:** Answered for effective enforcement; partial for normative consistency.

**Answer:**

- Runtime recognition requires Markdown instructions but no named semantic sections. The native contract loads the body only after activation and specifies no mandatory headings/tags ([skill-creator:75-80](installed-native-skill-creator/SKILL.md#L75)).
- Arcanum’s documentary authoring contract requires objective, logic type, process, quality bar, anti-patterns, and output contract ([workflow:87-104](../../framework/SIGIL-DEVELOPMENT-WORKFLOW.md#L87)). The template instantiates these sections ([template:12-54](../../framework/templates/sigil-template.md#L12)).
- Registry doctrine similarly requires human-reviewable intent, output contract, quality/anti-pattern guidance, and usually observability ([registry README:19-26](../../registry/README.md#L19)).
- No repository-wide validator parses or requires those semantic body elements. The public builder accepts `SKILL.md` or even `README.md` and derives description from loose prose fallbacks ([build registry:114-137](../../tools/build-skill-registry.py#L114)).

**Contrary evidence:** Registered/current packages exist without the template sections. `anti-bias-vector-composition` uses prose headings ([SKILL.md:6-25](../../formulae/anti-bias-vector-composition/SKILL.md#L6)); current canonical `research` uses numbered Markdown sections rather than the XML-like contract ([SKILL.md:9-20](../../arcana/research/SKILL.md#L9)).

**Residual uncertainty:** Individual package validators may impose additional body/resource requirements, as evidence-grounded-diagrams does, but these are capability-local rather than a universal Arcanum schema.

**Boundary:** “Required” is separated into documentary authoring expectation and executable recognition; the former is not reported as runtime-enforced.

## RQ-09 — Normative role of `SKILL.md.artifact.yml`

**Scope:** Sidecar authority over runtime activation, governance, registry publication, and validation.

**Status:** Answered.

**Answer:** The intended role is repository-governance metadata, not runtime activation. The constitution says runtime frontmatter owns `name`/`description` and supported runtime keys, while Arcanum governance metadata belongs in `SKILL.md.artifact.yml`; it may additionally carry tier/domain/version/origin ([constitution:104-110](../../framework/ARTIFACT-METADATA-CONSTITUTION.md#L104)). The full required governance fields are artifact ID/type, intent, owner, lifecycle, selectors, and validation profile ([constitution:40-60](../../framework/ARTIFACT-METADATA-CONSTITUTION.md#L40)).

Its effective roles are limited:

- artifact validator input, with field/status checks ([validator:271-312](../../tools/validate-artifact-metadata.py#L271));
- fallback source of `version` and `domain` for the public registry, subordinate to runtime frontmatter ([build registry:124-147](../../tools/build-skill-registry.py#L124));
- descriptive selectors/profiles; the validator does not resolve selectors or execute named profiles.

`lens-router` witnesses the intended encoding and a `reviewed` lifecycle declaration ([sidecar:1-19](../../transmutations/lens-router/SKILL.md.artifact.yml#L1)).

**Contrary evidence:** The constitution’s relevant enforcement rules are themselves marked `candidate` and refer to future enforcement ([constitution:112-120](../../framework/ARTIFACT-METADATA-CONSTITUTION.md#L112)). Most canonical skills have no sidecar, so sidecar presence is not an effective prerequisite for discovery, installation, or registry building.

**Residual uncertainty:** No universal mapping from `validation_profile` values to commands was found; the constitution explicitly lists that mapping as future work ([constitution:165-172](../../framework/ARTIFACT-METADATA-CONSTITUTION.md#L165)).

**Boundary:** A lifecycle value such as `reviewed` is a declaration validated for vocabulary, not proof that promotion gates ran.

## RQ-10 — Permitted canonical/projection differences

**Scope:** Projections generated by `tools/bootstrap_arcanum.sh`, selective synchronization, and the checked-in `.agents/skills` surface.

**Status:** Partial.

**Explicitly implemented differences:**

- inject generated provenance: surface kind, runtime, canonical source, alias, generator, and regenerate-only mutation policy ([bootstrap:844-857](../../tools/bootstrap_arcanum.sh#L844));
- replace the visible `name` for runtime package/alias naming ([bootstrap:1092-1129](../../tools/bootstrap_arcanum.sh#L1092));
- translate Codex-flavored `Task` and `AskQuestions` tool tokens to Claude equivalents ([bootstrap:1133-1150](../../tools/bootstrap_arcanum.sh#L1133));
- preserve the remaining source stream and copy support files/directories, excluding only `SKILL.md` and `development/` ([bootstrap:885-928](../../tools/bootstrap_arcanum.sh#L885));
- create intentionally thin alias packages whose body redirects to the canonical generated package ([bootstrap:1229-1260](../../tools/bootstrap_arcanum.sh#L1229));
- derive `name` and `description` for source documents without frontmatter, chiefly spells ([bootstrap:1205-1224](../../tools/bootstrap_arcanum.sh#L1205)).

Selective synchronization stages a fresh bootstrap package, requires `SKILL.md`, rejects symbolic links, and applies it with checksum-based `rsync --delete` ([sync:140-177](../../tools/sync-generated-skill-package.sh#L140), [211-245](../../tools/sync-generated-skill-package.sh#L211)).

**Contrary evidence:** The checked-in `.agents/skills` surface contains two incompatible projection styles:

- `lens-router` is a thin live-reference adapter that declares canonical source the complete authority ([adapter:8-12](../../.agents/skills/lens-router/SKILL.md#L8));
- `research` is a self-contained generated copy that declares regeneration provenance but currently differs materially from its named canonical source ([projection:2-20](../../.agents/skills/research/SKILL.md#L2); canonical [1-17](../../arcana/research/SKILL.md#L1)).

The current generator nests provenance under `metadata:` ([bootstrap:849-857](../../tools/bootstrap_arcanum.sh#L849)), while checked-in `research` has those fields at top level ([projection:2-9](../../.agents/skills/research/SKILL.md#L2)), demonstrating historical generator-shape drift.

**Residual uncertainty:** No content hash, generated-source parity validator, or global stale-projection gate was found. Therefore prohibited semantic divergence is documented by `mutation_policy`, but not effectively enforced for repo Codex projections.

**Boundary:** This identifies current implemented transformations and witnessed divergence; it does not claim that all checked-in differences are permitted merely because they exist.

## RQ-11 — Compliance enforcement

**Scope:** Native validation, repository-wide validators, installation, CI, registries, and package-local checks.

**Status:** Answered.

**Effective enforcement points:**

1. **Native skill validator, when explicitly run:** requires `SKILL.md`, valid YAML frontmatter, allowed keys, `name`, `description`, name syntax, and description constraints ([quick_validate.py:17-91](installed-native-skill-creator/scripts/quick_validate.py#L17)). It is not wired into inspected Arcanum CI.
2. **Claude generated-surface validator:** enforces package/file/frontmatter/name/description/tool/reference shape ([validate-claude-skills.sh:73-132](../../tools/validate-claude-skills.sh#L73)). Bootstrap blocks Claude installation on failure ([bootstrap:1456-1468](../../tools/bootstrap_arcanum.sh#L1456)), and CI regenerates then validates the full Claude surface ([workflow:31-52](../../.github/workflows/claude-skills.yml#L31)).
3. **Dependency validator:** checks TSV row shape, duplicate/self edges, and whether IDs resolve to tier directories with `SKILL.md` ([validate dependencies:17-65](../../tools/validate-sigil-dependencies.py#L17)). Bootstrap refuses installation when this validation fails ([bootstrap:397-408](../../tools/bootstrap_arcanum.sh#L397)).
4. **Registry builder:** refuses duplicate released IDs and unresolved manifest dependencies, then packages transitive closure ([build registry:578-620](../../tools/build-skill-registry.py#L578)).
5. **Artifact metadata validator, when directed at paths:** validates syntax, required fields, list shape, lifecycle vocabulary, and companion metadata ([validate metadata:271-312](../../tools/validate-artifact-metadata.py#L271)).
6. **Package-local validators:** may enforce substantially more; evidence-grounded-diagrams checks exact resources, references, schemas, templates, requirements, and agent prompt ([validate_skill_package.py:15-53](../../transmutations/evidence-grounded-diagrams/scripts/validate_skill_package.py#L15), [66-133](../../transmutations/evidence-grounded-diagrams/scripts/validate_skill_package.py#L66)).

**Major enforcement gaps/contrary evidence:**

- Artifact metadata absence fails only with `--require-metadata`; no paths means nothing is checked ([validate-artifact-metadata.py:536-565](../../tools/validate-artifact-metadata.py#L536)).
- The repository artifact-constitution wrapper runs changed-file metadata validation with `--advisory`, converting all metadata errors into warnings ([validate-artifact-constitution.sh:391-401](../../tools/validate-artifact-constitution.sh#L391)).
- Its governed-path heuristic includes `arcana/` and `transmutations/` but omits `formulae/` ([validate-artifact-metadata.py:87-96](../../tools/validate-artifact-metadata.py#L87)).
- No universal validator enforces the required Arcanum body sections.
- No checked-in Codex/Copilot projection CI or canonical/generated parity gate was found.
- `agents/openai.yaml` consistency is documentary except where a package-local validator checks it. Workflow doctrine says it should match when used ([workflow:200-211](../../framework/SIGIL-DEVELOPMENT-WORKFLOW.md#L200)), but no universal comparison exists.
- The native creator prose says frontmatter should contain only `name` and `description` ([skill-creator:348-356](installed-native-skill-creator/SKILL.md#L348)), while its executable validator permits `license`, `allowed-tools`, and `metadata` ([quick_validate.py:40-48](installed-native-skill-creator/scripts/quick_validate.py#L40)). The validator is the effective machine gate.

**Residual uncertainty:** Host-runtime validation beyond the installed local `skill-creator` and repository Claude gate was not introspected.

**Boundary:** “Enforced” here means a failing executable path blocks that specific validation/install/build operation. Documentary promotion criteria are not counted as enforced without a wired gate.

No files were created or modified.
## Agent 3 — Category-consumer falsification

Read-only governed return for dispatch `2026-08-26-unified-skill-model-research`, RQ-12–RQ-14. Preflight passed: repository root `[repository-root]`, research root `research/`, working folder `research/unified-skill-model/`, initial-definitions SHA-256 `2704196c95469e06ee2d74aa4e0e6c13395ecb7ec9a22c7b0246a7e1c8787684`. No files created/edited.

Falsification verdict on RQ-00 consolidation premise: a *naive physical/name deletion* is falsified by current operational consumers; a consolidation that preserves capability handles and compatibility for path-bearing surfaces is not falsified. I found no executable consumer that grants execution authority or dependency semantics because a capability is Formulae vs Transmutation vs Arcana. The strongest category dependencies are discovery roots, representation/provenance, publication layout, validation triggers, and telemetry—not differentiated execution behavior. Conversely, many exact canonical paths are operational inputs, and some closed consumer contracts reject path substitution even when bytes match.

Dependency classification
- semantic: lifecycle and authoring classify epistemic nature (`framework/SIGIL-DEVELOPMENT-WORKFLOW.md:12`, `framework/SIGIL-DEVELOPMENT-WORKFLOW.md:53`); registry explains tier meanings (`registry/SIGILS.md:64`, `registry/SIGILS.md:79`, `registry/SIGILS.md:117`). Some SKILL bodies embed tier/logic assertions, e.g. `transmutations/resolution-router/SKILL.md:17-20`.
- structural: discovery/install/build enumerate the three roots (`tools/bootstrap_arcanum.sh:372-381`, `tools/bootstrap_arcanum.sh:420-433`; `tools/sync-generated-skill-package.sh:122-131`; `tools/build-skill-registry.py:26-31`, `tools/build-skill-registry.py:578-598`; `tools/validate-sigil-dependencies.py:12-15`, `tools/validate-sigil-dependencies.py:47-53`).
- generated: runtime projections record category-bearing canonical paths (`tools/bootstrap_arcanum.sh:844-857`, `tools/bootstrap_arcanum.sh:1189-1226`, `tools/bootstrap_arcanum.sh:1300-1317`; concrete `.claude/skills/research/SKILL.md:1-9`). Installer inventory repeats `id` plus `tier` (`tools/bootstrap_arcanum.sh:2037-2048`; concrete `.arcanum/necronomicon/capabilities.json:8-32`).
- cosmetic: public headings/counts and prose tier labels are presentation where no consumer branches on them (`docs/registry.html:98-105`, `docs/registry.html:888-890`, `docs/registry.html:960-962`).
- historical: cleanup backups and archived research retain old path strings but were excluded from operational conclusions; they are evidence of former surfaces, not current authority.
- external-observable: committed public registry source URLs/download paths (`docs/registry.html:350-363`, `docs/registry.html:900-913`, `docs/registry.html:971-972`), README installation/link examples (`README.md:181-191`, `README.md:198-221`), and canonical URLs embedded into generated legacy commands (`tools/bootstrap_arcanum.sh:1600-1623`).
- unresolved: unknown downstream clones/bookmarks/scripts; whether `artifact_id` values prefixed with category are consumed outside metadata tooling; and whether schema `$id` is used as a network/identity key by external validators.

RQ-12 — Which observable repository behaviors depend on `formulae`, `transmutations`, or `arcana`?
Scope: active registries, builders, installer/bootstrap/sync, dependency closure, dispatch, observability, generated adapters, committed public artifacts, CI triggers, active links/tests/fixtures; development archives/backups treated as historical only.
Status: ANSWERED for in-repository consumers; external downstream use remains RQ-14 uncertainty.
Answer:
1. Package discovery and selection structurally depend on those exact root names. Bootstrap resolves a sigil by probing `formulae`, `transmutations`, `arcana` in order and stores the matched root as tier (`tools/bootstrap_arcanum.sh:372-381`, `tools/bootstrap_arcanum.sh:437-456`); `all` enumerates exactly those roots (`tools/bootstrap_arcanum.sh:425-433`). Selective sync repeats the ordered probe (`tools/sync-generated-skill-package.sh:122-131`). Dependency validation defines availability by scanning exactly those roots (`tools/validate-sigil-dependencies.py:12-15`, `tools/validate-sigil-dependencies.py:47-64`). Registry build treats roots as tiers, derives `tier` and `path` from directory placement, and rejects duplicate released slugs across them (`tools/build-skill-registry.py:26-31`, `tools/build-skill-registry.py:114-149`, `tools/build-skill-registry.py:578-598`).
2. Dependency closure is *not* tier-semantic: the TSV edges are bare IDs (`registry/SIGIL-DEPENDENCIES.tsv:1-5`), traversal is ID-only (`tools/validate-sigil-dependencies.py:68-79`), and bootstrap auto-adds by ID (`tools/bootstrap_arcanum.sh:450-456`). Tier names matter only to find the package. This is strong contrary evidence to claims that the taxonomy itself defines dependency behavior.
3. Generated projection and provenance depend on category-bearing canonical paths. Runtime packages read `$root/$tier/$id/SKILL.md` and emit `canonical_source: $tier/$id/SKILL.md` (`tools/bootstrap_arcanum.sh:1300-1317`); provenance declares regeneration from canonical source (`tools/bootstrap_arcanum.sh:844-857`). `tools/arcanum` derives kind and tier from canonical-source path patterns (`tools/arcanum:360-400`). Thus changing path text can change detected kind/tier even if skill content is identical.
4. Publication depends on tier namespace: download ZIP location uses `downloads/<tier>/...`, source URL uses the tier-derived path, and page grouping uses tier (`tools/build-skill-registry.py:250-287`, `tools/build-skill-registry.py:610-620`). Committed examples prove this is externally rendered (`docs/registry.html:350-363`, `docs/registry.html:900-913`, `docs/registry.html:971-972`).
5. CI watches the exact three roots; moves outside them stop triggering this validation unless its path filters change (`.github/workflows/claude-skills.yml:3-25`).
6. Registries/docs/linking depend structurally and cosmetically: registry entries expose tier and folder (`registry/SIGILS.md:3-11` onward); repo docs state canonical locations and symlink examples (`README.md:121-138`, `README.md:181-191`); `.agents` declares those roots as source of truth (`.agents/README.md:3-5`).
7. Some capability contracts use tier-qualified paths as semantic owner handles, not labels. Goal names required capabilities and owners as `arcana/craft`, `formulae/dispatch-spec`, etc. (`spells/goal/README.md:28-46`, `spells/goal/README.md:58-68`). Craft’s compatibility schema enumerates canonical sources and entrypoints under `arcana/craft` (`arcana/craft/templates/ledger.schema.yml:3-8`, `arcana/craft/templates/ledger.schema.yml:14-40`). Invoke’s preacceptance closure names exact `arcanum/arcana/...` consumers and explicitly rejects a different path despite hash equality (`spells/invoke/preacceptance-closure.md:47-61`, `spells/invoke/preacceptance-closure.md:63-75`). These are hard falsifiers to path-blind consolidation.
8. Observability carries tier but stable grouping is capability kind+ID: command telemetry emits both (`tools/arcanum:1672-1712`), while migration groups by `kind:id` and accepts legacy `sigil` fallback (`framework/observability/scripts/check-observability-migration.sh:9-12`, `framework/observability/scripts/check-observability-migration.sh:54-72`). Tier is diagnostic/legacy context, not grouping identity.
Contrary evidence: no active search result showed `if tier == formulae/transmutations/arcana` selecting different runtime permissions, dependency closure, or dispatch authority. Most tier occurrences are schema/prose/telemetry. Dispatch canonical handles are bare IDs (`formulae/dispatch-spec/scripts/validate-dispatch.py:170-181`, `formulae/dispatch-spec/scripts/validate-dispatch.py:956-968`).
Residual uncertainty: external tooling; unsearched generated output copies nested deeply under sample products; host runtime behavior beyond repository code.
Boundary: this answers current observable repository behavior, not whether category semantics should remain.

RQ-13 — What supplies stable capability identity across surfaces?
Scope: canonical SKILL/frontmatter, directory slug, registry/dependency handles, generated names/aliases/provenance, command adapters, dispatch and observability.
Status: PARTIAL: a de facto composite precedence is executable, but no single normative identity contract was found.
Answer: the most stable operational handle is the unprefixed capability ID/slug (normally directory basename and SKILL `name`), qualified by kind when collision matters; aliases resolve to it. Canonical path and tier are locator/classification/provenance, not the core ID.
Evidence:
- Canonical SKILL frontmatter exposes `name`, e.g. `transmutations/resolution-router/SKILL.md:1-4`; registry builder separately sets `slug = directory.name`, `name = frontmatter/fallback`, `tier = root`, `path = tier/dirname` (`tools/build-skill-registry.py:128-149`). This separation is explicit.
- Dependency edges and closure use bare IDs across all roots (`registry/SIGIL-DEPENDENCIES.tsv:1-5`; `tools/validate-sigil-dependencies.py:47-79`).
- Dispatch validates bare `capability_ref` handles against canonical ID strings, independent of tier (`formulae/dispatch-spec/scripts/validate-dispatch.py:170-181`, `formulae/dispatch-spec/scripts/validate-dispatch.py:956-968`).
- Generated skills preserve `name`, `canonical_source`, and `alias_of` separately (`.claude/skills/research/SKILL.md:1-9`; alias example `.claude/skills/structured-interview-kits/SKILL.md:1-16`).
- Executable resolution precedence is `alias_of` → `name` → basename extracted from recognized canonical-source path → package directory fallback (`tools/arcanum:346-371`). Kind is separately inferred from canonical source (`tools/arcanum:374-382`), and tier separately from frontmatter then path (`tools/arcanum:385-400`).
- Observability uses `capability.id` plus `kind` as grouping identity, not tier (`framework/observability/scripts/check-observability-migration.sh:54-72`).
- CLI compatibility names encode kind+ID (`tools/arcanum:428-455`), while generated alias packages point to canonical generated names (`tools/bootstrap_arcanum.sh:1229-1260`).
Contrary evidence / instability:
- The build registry makes slug authoritative for downloads and duplicate detection even if frontmatter `name` differs (`tools/build-skill-registry.py:141-147`, `tools/build-skill-registry.py:595-598`), while `tools/arcanum` prefers `name` over canonical path (`tools/arcanum:346-371`): no universal precedence.
- Artifact sidecars may carry a category-qualified artifact identity distinct from capability ID, e.g. `transmutations/resolution-router/SKILL.md.artifact.yml:1-18`; this is artifact identity, not proven capability identity.
- The structured-interview case demonstrates package-name/canonical-ID inversion: canonical source folder/name `structured-interview-kits`, generated visible package `interrogation`, legacy package aliases back to it (`.claude/skills/structured-interview-kits/SKILL.md:1-16`; generator logic `tools/bootstrap_arcanum.sh:1307-1317`).
- Current snapshot inspection found 59 released sigil directories, no cross-root duplicate directory slugs and no `name`/directory mismatch, but this is an observed invariant, not an enforced universal contract.
Residual uncertainty: whether artifact metadata validators or external systems treat `artifact_id` as capability identity; host discovery may privilege folder name vs frontmatter differently.
Boundary: stable identity is an evidenced operational composite, not a claim that any one field is normatively authoritative.

RQ-14 — Which external canonical references function as compatibility contracts?
Scope: committed public docs/downloads, generated runtime packages/legacy commands, CLI names, provenance, schema IDs, repository-local exact consumer paths; excludes unknown external installations.
Status: PARTIAL because downstream reliance cannot be enumerated from this repository.
Answer: compatibility-contract candidates with executable or public observability are:
1. Bare skill/package IDs and prefixed command names. README says short aliases are default and prefixed packages are explicit compatibility packages (`README.md:221`); installer emits `arcanum-sigil-<id>` plus bare IDs and aliases (`tools/bootstrap_arcanum.sh:1736-1741`, `tools/bootstrap_arcanum.sh:1939-1958`). `tools/arcanum` resolves those names to IDs (`tools/arcanum:428-455`).
2. Generated `canonical_source`, `alias_of`, `generated_by`, mutation policy. These are deliberately emitted provenance (`tools/bootstrap_arcanum.sh:844-857`) and consumed for ID/kind/tier resolution (`tools/arcanum:346-400`). Concrete committed packages expose them (`.claude/skills/research/SKILL.md:1-9`).
3. Public GitHub canonical-source URLs and tiered download URLs. Generator constructs them from tier/path (`tools/build-skill-registry.py:250-287`); committed public page exposes them (`docs/registry.html:350-363`, `docs/registry.html:900-913`, `docs/registry.html:971-972`).
4. README/registry relative links and repo-scoped canonical paths are navigation contracts (`README.md:181-191`; `registry/SIGILS.md:3-11` onward; `.agents/README.md:3-5`).
5. Schema identifier includes category path (`formulae/dispatch-spec/dispatch.schema.yml:1-4`; JSON mirror `formulae/dispatch-spec/dispatch.schema.json:1-5`). Potentially externally keyed; consumption not proved.
6. Exact consumer/owner paths are stronger than public navigation where closed validation says identity is path-bound: Invoke closure’s canonical-consumer table and no-substitution rule (`spells/invoke/preacceptance-closure.md:47-75`); Craft compatibility entrypoint and source-of-truth paths (`arcana/craft/templates/ledger.schema.yml:3-8`, `arcana/craft/templates/ledger.schema.yml:14-40`).
7. CI path filters are internal compatibility obligations for change detection (`.github/workflows/claude-skills.yml:3-25`).
Contrary evidence / false blockers:
- Tier labels/headings/counts alone are cosmetic and can be regenerated; their existence does not prove callers require category semantics (`docs/registry.html:98-105`).
- Dependency closure and dispatch refs are bare-ID-based, so preserving category names is not required by those contracts (`registry/SIGIL-DEPENDENCIES.tsv:1-5`; `formulae/dispatch-spec/scripts/validate-dispatch.py:170-181`).
- Observability can migrate legacy rows using `sigil` and groups by kind+ID, so tier continuity is not its identity requirement (`framework/observability/scripts/check-observability-migration.sh:9-12`, `framework/observability/scripts/check-observability-migration.sh:54-72`).
Residual uncertainty: no repository evidence can establish who bookmarked URLs, downloaded tiered ZIPs, pinned schema `$id`, or parsed `canonical_source` externally.
Boundary: ‘compatibility contract’ here means public or executable reliance evidenced in-repo, not a guarantee of all downstream consumers.

Hard falsifiers
- Physical removal/rename without changing discovery roots makes capabilities unknown/unavailable (`tools/bootstrap_arcanum.sh:372-381`; `tools/validate-sigil-dependencies.py:47-64`).
- Path-blind equivalence is false for at least one closed consumer: Invoke rejects a different path even with identical hash (`spells/invoke/preacceptance-closure.md:73-75`).
- A unified namespace cannot admit duplicate released IDs without an identity rule; registry build currently fails on duplicate slugs (`tools/build-skill-registry.py:595-598`). No duplicates exist in the current 59-sigil snapshot, so this is a compatibility guard, not a current blocker.
- Dropping old path strings breaks generated kind/tier inference and provenance (`tools/arcanum:360-400`).

False blockers
- Tier is not shown to control runtime authority or dependency closure.
- Bare ID continuity does not require path continuity for dependency and dispatch contracts.
- Cosmetic registry headings, taxonomy prose, and telemetry tier values do not themselves falsify consolidation.
- Category-qualified `artifact_id` values are not proved to be capability IDs.

Compatibility obligations only (no migration proposal): preserve stable capability ID+kind, documented aliases and command names; keep dependency closure resolvable by bare ID; keep generated provenance resolvable; retain continuity for public source/download/schema identifiers and exact path-bound consumer contracts; preserve observability attribution by kind+ID; ensure validation/change-detection still covers every canonical package; detect/reject identity collisions.
## Connections

- derives: `./findings.md`
