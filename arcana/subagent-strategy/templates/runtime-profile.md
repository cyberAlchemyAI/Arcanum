# Subagent Strategy Runtime Profile

Use this template to bind the public Subagent Strategy lifecycle to one
repository. Keep project-specific authority here rather than in the public
sigil.

```yaml
profile_id: <stable-id>
version: <version>
repository_root: <resolved-at-runtime>

dispatch_types:
  <type>:
    status: live | reserved
    owner_capability: <skill-or-file>
    preflights:
      - capability: <capability>
        mode: <read-only-mode>
        required: true | false

form_owner:
  capability: <skill-or-file>
  schema: <path>
  schema_version_source: <canonical field, schema, or executable>
  confirmation_readiness_validator: <non-mutating command>
  registration_validator: <command>
  version_drift_policy: warn-rematerialize-and-revalidate-before-confirmation
  composite_admission:
    - form-and-version
    - live-type-owner-prerequisites
    - agent-eligibility-and-identity-uniqueness
    - final-approver-admission
    - digest-owned-tension-evidence
    - publication-boundary

tension_gate:
  capability: <skill-or-file>
  independent_checks: 2
  input_boundary: exact-sheet-bytes-and-rubric-only
  protocol: parallel-independent-verdicts-then-optional-frozen-report-comparison

agent_pool:
  source: <path-or-runtime-provider>
  selection_rules: <summary>

registration:
  registrar: <deterministic-command-or-capability>
  ledger: <append-only-path>
  dispatch_events: 1
  close_events: 1

dependency_semantics:
  blocking: [sequential, zig-zag]
  non_blocking: [feedback]

final_approval:
  default_owner: parent
  dedicated_auditor_allowed: true
  eligibility_validator: <deterministic-rule-or-command>

human_gate:
  revision_authorization_is_confirmation: false
  normal_confirmation_request_count: 1

result_hooks:
  inventory: <capability-and-mode | none>
  observability: <capability-and-mode | none>

publication:
  public_paths: []
  private_paths: []
  forbidden_evidence: []
```

## Validation Rules

- Every live dispatch type names one readable owner capability.
- Reserved types cannot be dispatched.
- Registration and closeout use one deterministic registrar.
- The ledger is append-only and receives exactly one dispatch event and one
  paired close event per dispatch.
- The tension gate can run two independent checks.
- The confirmation-readiness validator accepts the exact persisted sheet without
  confirmation evidence, returns its current schema version and digest, performs
  no registration or ledger write, and blocks invalid sheets.
- Confirmation readiness is composite: every configured form, type-owner,
  identity, approver, tension-evidence, and publication obligation closes
  before a confirmation request is made.
- Every load-bearing tension input is present in the exact sheet bytes.
- Tension agents receive only the exact sheet bytes and rubric. Their
  independent verdicts are preserved before any comparison of apontamentos.
- A stale runtime or candidate form version is a visible warning followed by
  rematerialization and revalidation before the human gate; it is never an
  admission bypass.
- The agent pool or runtime provider is resolvable and every non-null identity
  is eligible and unique before confirmation.
- Final-approver eligibility is deterministic and consistent with the local
  sheet schema and registrar.
- Draft revision authorization is not dispatch confirmation; a normal ready
  proposal asks once.
- Post-result hooks are explicitly configured or explicitly absent.
- Publication rules prevent private evidence from crossing into public paths.
