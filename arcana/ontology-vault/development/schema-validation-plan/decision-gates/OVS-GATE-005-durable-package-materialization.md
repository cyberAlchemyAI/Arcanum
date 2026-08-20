# Decision Gate: OVS-GATE-005 Durable Package Materialization

Status: pass
Date: 2026-08-20
Resolved: 2026-08-20
Target scope: Ontology Vault distinction between one-run evidence and durable ontology packages

## Prior Boundary

`OVS-GATE-004-default-output-declaration.md` authorized JSON as the primary
artifact for files written by Ontology Vault. It deliberately deferred a richer
graph format and did not authorize one invocation receipt to become a durable
ontology state store.

`OVS-GATE-001-promotion-boundary.md` also withheld authority for the older
branch-aware candidate schema and for cross-project template obligations.

## Owner Decision

The owner directed Ontology Vault to enforce this narrower behavior:

- an invocation or validation receipt may remain one machine-readable JSON;
- a durable, reusable, multi-view, or evolving ontology is a package;
- deterministic triggers choose the package path;
- unresolved package ownership or output location fails closed;
- genuinely small one-off maps remain eligible for one run artifact; and
- no universal cross-project graph schema or external adoption obligation is
  created by this decision.

Source of decision: owner instruction in the delegated 2026-08-20 Ontology
Vault durable-package task.

## Allowed Work

- Add the receipt-versus-package classifier to canonical Ontology Vault source.
- Add a capability-owned minimum package contract and deterministic validator.
- Add regression fixtures for simple, durable, bridged, evolving, and
  unresolved-owner cases.
- Synchronize the generated Codex and Claude Ontology Vault packages through
  the selective generated-package tool.
- Materialize an owner-scoped public candidate package when its owner, exact
  root, visibility, provenance, and authority ceiling are explicit.

## Still Disallowed

- Treating a run receipt as the product ontology's long-lived state store.
- Requiring unrelated ontology packages to migrate to one record schema.
- Promoting the older branch-aware development schema as final canonical law.
- Allowing ontology, validation, or generated mirrors to decide authority.
- Copying private proofs, scripts, evidence, or other-system material into a
  public package.
- Publication, release, promotion, commit, or push.

## Gate Result

Result: `PASS`

No blocker remains for the bounded package-materialization behavior. Package
owners and output roots remain instance-specific inputs and must fail closed
when unresolved.
