# Interrogation Review: Define

Status: pass
Owner capability: interrogation
Mode: refine-review

## Review Verdict

The definition is useful if the run keeps database and migration vocabulary local to IntegrationSpec and gives authors concrete fields rather than another generic "choose database" note.

## Confirmed

- Data-store selection is workload-led, not vendor-led.
- Polyglot persistence is allowed only when access patterns or lifecycle needs justify it.
- Cache/search/vector/analytics stores need explicit authority and rebuild/freshness rules.
- Migration command profiles need environment policy, drift/status validation, lock policy, and destructive-command gates.

## Repairs Applied

- Added source-of-truth role as a required field.
- Added schema-history/checksum/lock state as explicit migration evidence.
- Added reset/clean/drop as blocked-by-default production command classes.
- Kept migration logs and runtime receipts as task evidence, not spec truth.

## Residue

Exact local vocabulary names remain L0 choices: `Integration Data Resource Decision Record`, `DatabaseResource` label, `Migration Command Profile`, and `SchemaHistoryResource`.
