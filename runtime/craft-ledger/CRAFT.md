# Craft Ledger Runtime

Human-readable view of `.craft/ledger.yml`. The ledger is the source of truth;
this page is only a linked navigation surface.

## Quick Links

- Root context: [CTX-CRAFT-LEDGER-RUNTIME](#context-ctx-craft-ledger-runtime).
- Current next move: [implement the S0 kernel and admit S1 contracts](#next-move).
- Source contract: [ledger mutation discovery](docs/features/ledger-mutation/discovery.md).
- Admitted Define: [protocol specification](.invoke/ledger-mutation/define-v1/bundle/SPEC.md).
- Active blockers: none.
- Decisions: [2 closed and 9 open](#decisions); none currently marked blocking.
- Active gaps: [GAP-LEDGER-MUTATION-DESIGN](#gap-ledger-mutation-design) and [GAP-LEDGER-MUTATION-DEFINITION-OVERHEAD](#gap-ledger-mutation-definition-overhead).

## Contexts

### <a id="context-ctx-craft-ledger-runtime"></a>CTX-CRAFT-LEDGER-RUNTIME — Craft Ledger Runtime

- Stage: `design`
- Gate: `flag`
- Purpose: design and implement deterministic, fail-closed mutation of Craft ledgers.
- Description: Define v1 admits the `add_gap`-only S0 transaction kernel. The accepted operation inventory keeps read, standalone validation, projections, orchestration, and external execution outside the mutation discriminator; S1 adds `transition_gap`, `next`, `open_decision`, and `decide` after their contracts are admitted.
- Existing foundation: the [canonical persisted `gaps` row schema](../../arcana/craft/templates/schemas/ledger-core.schema.yml) is already defined; it does not need to be redesigned.

#### <a id="next-move"></a>Next Move

1. Design and implement the S0 `add_gap` transaction kernel under `runtime/craft-ledger/implementation/`, using subdirectories to separate responsibilities.
2. Reuse the existing persisted `gaps` row schema, constrain `add_gap` to active-row creation, and materialize its request, mappings, `inspect`, `plan`, `apply`, and outcome contracts.
3. Close only the remaining decisions required for the S0 implementation.
4. Reduce and measure the definition overhead observed in the 38-minute Define cycle.
5. Admit the S1 contracts for `transition_gap`, `next`, `open_decision`, and `decide`; do not claim those operations before their lifecycle rules are governed.

## Artifacts

- `ART-CRAFT-LEDGER-SOURCE`: [`.craft/ledger.yml`](.craft/ledger.yml), authoritative Craft state.
- `ART-CRAFT-LEDGER-VIEW`: [`CRAFT.md`](CRAFT.md), this human-readable view.
- `ART-CRAFT-LEDGER-MUTATION-DISCOVERY`: [ledger mutation discovery](docs/features/ledger-mutation/discovery.md), initial source contract.
- `ART-LEDGER-MUTATION-DEFINE-SPEC`: [admitted Define specification](.invoke/ledger-mutation/define-v1/bundle/SPEC.md), one-envelope protocol and first supported slice.
- `ART-LEDGER-MUTATION-DEFINE-DEFINITIONS`: [candidate definitions](.invoke/ledger-mutation/define-v1/bundle/DEFINITIONS.json), no authority effect.
- `ART-LEDGER-MUTATION-DEFINE-ADMISSION`: [independent admission receipt](.invoke/ledger-mutation/define-v1/DEFINE-BUNDLE-ADMISSION-RECEIPT.json), replay pass.
- `ART-LEDGER-MUTATION-DEFINE-STATUS`: [capability status](.invoke/ledger-mutation/define-v1/CAPABILITY-STATUS.json), `artifact_authored: pass`; release/runtime not claimed.
- `ART-CRAFT-OPERATIONS-ROBOT-TALKS`: [operation-boundary review](robot-talks/craft-operations-decision/review.md), accepted evidence for the phased inventory.

## Candidate Definitions

- `DEF-CRAFT-LEDGER-INSPECTION-SNAPSHOT`: fresh, read-only, revision-bound context read before proposal.
- `DEF-CRAFT-LEDGER-MUTATION-REQUEST`: common envelope plus exactly one operation-selected payload.
- `DEF-CRAFT-OPERATION-PAYLOAD`: family-specific fields and invariants selected by `operation`.
- `DEF-CRAFT-LEDGER-MUTATION-OUTCOME`: stable result that makes persistence effects explicit.

## Active Gaps

### <a id="gap-ledger-mutation-design"></a>GAP-LEDGER-MUTATION-DESIGN

- Severity: `flag`
- Treatment: `plan`
- Owner: `planner`
- Summary: the persisted `gaps` row schema already exists. What remains is the machine-checkable request envelope, the `add_gap` payload contract, deterministic mapping into that row, and the `inspect`/`plan`/`apply`/outcome contracts.
- Evidence: [admitted Define specification](.invoke/ledger-mutation/define-v1/bundle/SPEC.md).

### <a id="gap-ledger-mutation-definition-overhead"></a>GAP-LEDGER-MUTATION-DEFINITION-OVERHEAD

- Severity: `flag`
- Treatment: `plan`
- Owner: `operations`
- Observation: producing and admitting the definition for only `add_gap` took 38 minutes.
- Impact: the current workflow is too expensive to repeat independently for every ledger operation.
- Evidence: operator observation on 2026-08-31, linked to the [Define admission receipt](.invoke/ledger-mutation/define-v1/DEFINE-BUNDLE-ADMISSION-RECEIPT.json).

## Decisions

The runtime-owner and operation-inventory decisions are closed by operator direction. The other nine questions remain `active`, non-blocking at the current design stage, and have `selected: pending`; their option sets have not yet been admitted.

### <a id="decision-dec-ledger-mutation-runtime-owner"></a>DEC-LEDGER-MUTATION-RUNTIME-OWNER

- Question: Qual componente será o owner canônico do runtime mutável: o pacote Craft, um adapter separado ou uma superfície compartilhada de runtime?
- State: `closed`; blocking: `false`; selected: `runtime/craft-ledger/implementation`.
- Owner: `architecture`
- Rationale: the operator selected a project-local implementation root and allowed subdirectories there to separate responsibilities.
- Impact: runtime code, implementation-local schemas, tests, and responsibility boundaries now have one project-owned root; the concrete subdirectory layout remains Design work.

### <a id="decision-dec-ledger-mutation-operation-inventory"></a>DEC-LEDGER-MUTATION-OPERATION-INVENTORY

- Question: Qual é o inventário inicial de operações suportadas e qual delas fornece o menor slice útil sem fingir cobertura completa?
- State: `closed`; blocking: `false`; selected: `phase coherent mutation lifecycles after the add_gap kernel`.
- Owner: `product`
- Rationale: `add_gap` remains the create-active S0 transaction kernel. S1 adds `transition_gap`, `next`, `open_decision`, and `decide`; later slices add evidence and local knowledge, typed items and gates, then recursive contexts. Shared `inspect`/`plan`/`apply` mechanics do not erase operation-specific semantics, and read, standalone validation, projections, orchestration, and external execution remain outside the mutation discriminator.
- Evidence: [accepted Robot-Talks review](robot-talks/craft-operations-decision/review.md).
- Impact: bounds runtime coverage, supplies the expansion order, and prevents partial support from being represented as complete ledger support.

### <a id="decision-dec-ledger-mutation-id-policy"></a>DEC-LEDGER-MUTATION-ID-POLICY

- Question: Qual autoridade fecha o domínio de unicidade e a política de alocação de IDs por família?
- State: `active`; blocking: `false`; selected: `pending`; options and final rationale: not yet admitted.
- Owner: `governance`
- Impact: controls proposed IDs, allocation authority, and collision handling.

### <a id="decision-dec-ledger-mutation-apply-authority"></a>DEC-LEDGER-MUTATION-APPLY-AUTHORITY

- Question: Quem pode autorizar `apply` em cada ambiente: o mesmo caller, um humano, uma policy engine ou uma combinação deles?
- State: `active`; blocking: `false`; selected: `pending`; options and final rationale: not yet admitted.
- Owner: `governance`
- Impact: controls who may cross from a non-writing plan to an authoritative mutation.

### <a id="decision-dec-ledger-mutation-embedded-index"></a>DEC-LEDGER-MUTATION-EMBEDDED-INDEX

- Question: Quais famílias compõem cada índice embutido e quais filtros definem itens ativos por versão?
- State: `active`; blocking: `false`; selected: `pending`; options and final rationale: not yet admitted.
- Owner: `architecture`
- Impact: defines the index effects validated and published atomically with row changes.

### <a id="decision-dec-ledger-mutation-legacy-020"></a>DEC-LEDGER-MUTATION-LEGACY-020

- Question: Qual é a semântica operacional definitiva para ledgers `0.2.0`?
- State: `active`; blocking: `false`; selected: `pending`; options and final rationale: not yet admitted.
- Owner: `architecture`
- Impact: determines whether legacy ledgers are readable, mutable, rejected, or require migration.

### <a id="decision-dec-ledger-mutation-atomic-commit"></a>DEC-LEDGER-MUTATION-ATOMIC-COMMIT

- Question: Qual mecanismo fornecerá compare-and-commit e substituição atômica nas plataformas suportadas?
- State: `active`; blocking: `false`; selected: `pending`; options and final rationale: not yet admitted.
- Owner: `tech`
- Impact: underpins `STALE_SOURCE` enforcement and the no-partial-write guarantee.

### <a id="decision-dec-ledger-mutation-derived-index"></a>DEC-LEDGER-MUTATION-DERIVED-INDEX

- Question: Como `.craft/index.json` será atualizado ou invalidado após o commit sem ampliar a transação autoritativa?
- State: `active`; blocking: `false`; selected: `pending`; options and final rationale: not yet admitted.
- Owner: `tech`
- Impact: prevents consumers from trusting a stale derived index.

### <a id="decision-dec-ledger-mutation-replay-evidence"></a>DEC-LEDGER-MUTATION-REPLAY-EVIDENCE

- Question: Qual superfície admitida pelo schema guardará a prova durável de replay na mesma unidade atômica do ledger, e por quanto tempo ela será retida?
- State: `active`; blocking: `false`; selected: `pending`; options and final rationale: not yet admitted.
- Owner: `architecture`
- Impact: determines whether retries can recover the original result without duplicating effects.

### <a id="decision-dec-ledger-mutation-dry-run-plan"></a>DEC-LEDGER-MUTATION-DRY-RUN-PLAN

- Question: O plano de dry-run será um artefato serializado estável ou uma resposta efêmera sem perder a identidade imutável exigida por `apply`?
- State: `active`; blocking: `false`; selected: `pending`; options and final rationale: not yet admitted.
- Owner: `architecture`
- Impact: determines how a plan is inspected, transported, authorized, and applied later.

### <a id="decision-dec-ledger-mutation-yaml-serialization"></a>DEC-LEDGER-MUTATION-YAML-SERIALIZATION

- Question: Quais perfis preservarão a representação YAML existente e quais adotarão serialização canônica?
- State: `active`; blocking: `false`; selected: `pending`; options and final rationale: not yet admitted.
- Owner: `architecture`
- Impact: determines byte identity, formatting preservation, fingerprints, and reproducibility.

Evidence for every decision: [discovery open questions](docs/features/ledger-mutation/discovery.md#questões-abertas). No decision outcome or option set has been invented in this projection.

## Pending by Node

### CTX-CRAFT-LEDGER-RUNTIME

- Blockers: none.
- Blocking decisions: none.
- Closed decisions:
  - [DEC-LEDGER-MUTATION-RUNTIME-OWNER](#decision-dec-ledger-mutation-runtime-owner) — runtime root selected as `runtime/craft-ledger/implementation/`.
  - [DEC-LEDGER-MUTATION-OPERATION-INVENTORY](#decision-dec-ledger-mutation-operation-inventory) — phased mutation lifecycles selected after the `add_gap` kernel.
- Other open decisions:
  - [DEC-LEDGER-MUTATION-ID-POLICY](#decision-dec-ledger-mutation-id-policy) — establish ID uniqueness and allocation authority.
  - [DEC-LEDGER-MUTATION-APPLY-AUTHORITY](#decision-dec-ledger-mutation-apply-authority) — establish per-environment apply authorization.
  - [DEC-LEDGER-MUTATION-EMBEDDED-INDEX](#decision-dec-ledger-mutation-embedded-index) — define versioned embedded-index membership and filters.
  - [DEC-LEDGER-MUTATION-LEGACY-020](#decision-dec-ledger-mutation-legacy-020) — define operational behavior for ledger version 0.2.0.
  - [DEC-LEDGER-MUTATION-ATOMIC-COMMIT](#decision-dec-ledger-mutation-atomic-commit) — select compare-and-commit and atomic replacement mechanics.
  - [DEC-LEDGER-MUTATION-DERIVED-INDEX](#decision-dec-ledger-mutation-derived-index) — define generated-index invalidation or rebuilding.
  - [DEC-LEDGER-MUTATION-REPLAY-EVIDENCE](#decision-dec-ledger-mutation-replay-evidence) — define durable replay evidence and retention.
  - [DEC-LEDGER-MUTATION-DRY-RUN-PLAN](#decision-dec-ledger-mutation-dry-run-plan) — define stable versus ephemeral plan representation.
  - [DEC-LEDGER-MUTATION-YAML-SERIALIZATION](#decision-dec-ledger-mutation-yaml-serialization) — define representation-preserving versus canonical serialization profiles.
- Active gaps:
  - `GAP-LEDGER-MUTATION-DESIGN` — design the request, mapping, and runtime contracts while reusing the existing persisted `gaps` row schema.
  - `GAP-LEDGER-MUTATION-DEFINITION-OVERHEAD` — reduce the 38-minute per-operation definition cost before scaling the operation inventory.
- Pending artifacts or routes: registry release and mutation runtime readiness are not claimed; the next lifecycle route is `design`.
- Recomposition residue: none.
- Next move: design and implement the S0 `add_gap` transaction kernel under `runtime/craft-ledger/implementation/` with responsibility-separated subdirectories; constrain it to active-row creation; close only decisions required by S0; simplify and measure the workflow; then admit the S1 contracts for `transition_gap`, `next`, `open_decision`, and `decide`.
