# Craft Ledger Mutation Candidate Definitions

Status: candidate
Owner route: definitions-governance
Scope: feature:runtime/craft-ledger:ledger-mutation
Authority effect: none

## Candidate Definitions

### DEF-CRAFT-LEDGER-INSPECTION-SNAPSHOT: ledger inspection snapshot

Aliases: inspection snapshot, snapshot de inspeção
Status: candidate

#### Normative voice

A ledger inspection snapshot is the read-only, revision-bound representation of the authoritative ledger state and selected context that a caller must consume before proposing a mutation.

#### Plain-language voice

It is the fresh read the caller gets before asking to change the ledger.

#### Domain context

In Craft ledger mutation, the snapshot prevents a model from relying only on conversation memory or CRAFT.md and gives the later request an exact expected_revision.

#### Evidence

- evidence: `runtime/craft-ledger/docs/features/ledger-mutation/discovery.md` (heading `5.4 Tratamento do contexto`; sha256 `fe6069cbe682d6f484042d9d7ea2db2bb6e450b571c21f99f7b7fcaa02072250`)

### DEF-CRAFT-LEDGER-MUTATION-REQUEST: ledger mutation request

Aliases: mutation request, requisição de mutação
Status: candidate

#### Normative voice

A ledger mutation request is the complete versioned proposal passed to the deterministic runtime, consisting of a common envelope and exactly one payload selected by operation; it proposes meaning but does not authorize or perform a write.

#### Plain-language voice

It is one change request with shared addressing fields and a type-specific body.

#### Domain context

In the first Craft slice, operation is add_gap and payload carries gap semantics; decision and blocker payloads do not exist until separately defined.

#### Evidence

- evidence: `runtime/craft-ledger/docs/features/ledger-mutation/discovery.md` (heading `4.2 Requisição de mutação`; sha256 `fe6069cbe682d6f484042d9d7ea2db2bb6e450b571c21f99f7b7fcaa02072250`)

### DEF-CRAFT-OPERATION-PAYLOAD: operation payload

Aliases: family payload, payload de operação
Status: candidate

#### Normative voice

An operation payload is the operation-selected semantic body of a ledger mutation request, with fields and invariants owned by exactly one supported ledger mutation operation.

#### Plain-language voice

The outside of the request stays the same; the inside changes according to the kind of ledger entry.

#### Domain context

For v1, only P_add_gap exists and requires gap_id, summary, severity, treatment, owner_route, status, and evidence.

#### Evidence

- evidence: `runtime/craft-ledger/docs/features/ledger-mutation/discovery.md` (heading `5.5 Validação por família`; sha256 `fe6069cbe682d6f484042d9d7ea2db2bb6e450b571c21f99f7b7fcaa02072250`)

### DEF-CRAFT-LEDGER-MUTATION-OUTCOME: ledger mutation outcome

Aliases: mutation result, resultado de mutação
Status: candidate

#### Normative voice

A ledger mutation outcome is the stable, non-ambiguous response that identifies the attempted request and reports its classified result, diagnostics, bound identities, and whether authoritative ledger bytes changed.

#### Plain-language voice

It tells the caller exactly what happened and whether the ledger changed.

#### Domain context

Craft uses the outcome to distinguish a valid dry-run, a committed mutation, a harmless replay, and every fail-closed case.

#### Evidence

- evidence: `runtime/craft-ledger/docs/features/ledger-mutation/discovery.md` (heading `4.6 Resultado e idempotência`; sha256 `fe6069cbe682d6f484042d9d7ea2db2bb6e450b571c21f99f7b7fcaa02072250`)

## Semantic Applications

| Probe | Disposition | Candidate definitions | Authority bindings |
| --- | --- | --- | --- |
| probe:ledger-inspection-snapshot | new-scoped-term | DEF-CRAFT-LEDGER-INSPECTION-SNAPSHOT | none |
| probe:ledger-mutation-request | new-scoped-term | DEF-CRAFT-LEDGER-MUTATION-REQUEST | none |
| probe:operation-payload | new-scoped-term | DEF-CRAFT-OPERATION-PAYLOAD | none |
| probe:ledger-mutation-outcome | new-scoped-term | DEF-CRAFT-LEDGER-MUTATION-OUTCOME | none |
