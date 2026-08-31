# feature:craft-ledger-mutation-input

Define the smallest trustworthy protocol boundary for inspecting and mutating a Craft ledger, with one common request envelope and operation-specific payloads.

## Inspect before proposing

Before a ledger mutation is proposed, the caller must obtain a ledger inspection snapshot for the resolved workspace and target context. The snapshot supplies the authoritative source revision and current context needed to construct the request; remembered conversation or a derived CRAFT.md view is not a substitute.

## One request protocol

Ledger mutation input uses one versioned request protocol rather than an unrelated top-level YAML contract for every ledger family. Its common envelope binds request_version, request_id, operation, target.workspace, target.context_id, target.expected_revision, and payload.

## Discriminated operation payload

The operation value selects exactly one operation payload shape. Payload fields are not interchangeable across gaps, blockers, decisions, definitions, or other ledger families, and a payload that does not match operation is invalid.

## First supported slice

The first profile supports only operation add_gap. Its payload requires gap_id, summary, severity, treatment, owner_route, status, and evidence. Any other operation returns UNSUPPORTED until its own payload semantics and mapping are defined.

## Caller and runtime ownership

The interpretive caller supplies operation, context_id, and the semantic payload. A trusted caller adapter may inject or copy mechanical envelope values such as request_version, request_id, the resolved workspace, and expected_revision from the inspection snapshot, but the complete assembled request is the object validated and fingerprinted by the runtime.

## Plan without mutation

Planning must reread the authoritative ledger, verify the workspace, context, expected revision, IDs, references, and add_gap policy, construct and validate the complete candidate, and return a stable plan or non-writing outcome. Planning grants no write authority.

## Explicit apply boundary

Apply accepts a validated plan identity plus required authorization, rechecks the bound source revision inside the commit boundary, and either publishes the complete candidate atomically or writes nothing. A changed source returns STALE_SOURCE; a changed plan, profile, serializer, candidate, or authorization returns PLAN_MISMATCH.

## Stable fail-closed outcome

Every attempt returns a ledger mutation outcome from PLAN, APPLIED, NO_OP, ALREADY_APPLIED, CONFLICT, PLAN_MISMATCH, INVALID, UNKNOWN, UNSUPPORTED, or STALE_SOURCE, with diagnostics and persistence effect sufficient for the caller to know whether ledger bytes changed.
