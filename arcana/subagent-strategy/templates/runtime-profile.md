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

sheet_lifecycle:
  format: json
  temporary_root: .arcanum/runtime/subagents-strategy
  filename_pattern: <dispatch-id>.tmp.json
  confirmation_binds: exact-sheet-bytes
  byte_change_policy: rerun-readiness-tension-and-human-confirmation
  consume_after: ledger-append
  preserve_on_failure: true

agent_pool:
  source: <path-or-runtime-provider>
  selection_rules: <summary>

registration:
  registrar: node arcana/subagent-strategy/scripts/append-dispatch.cjs --consume
  ledger: .arcanum/observability/subagents-strategy/subagents-dispatch.yaml
  ledger_format: yaml-with-json-columns
  dispatch_rows: 1
  close_rows: 1

native_runtime_binding:
  schema_version: arcanum.subagent-strategy-registration.v0.3
  dispatch_field: subagent_strategy.registration
  compile_command: <command-or-none>
  verify_registration_command: <command-or-none>
  verify_close_command: <command-or-none>
  portable_paths: forward-slash-project-relative
  temporary_close_pattern: <dispatch-id>.close.tmp.json

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
  confirmation_binds: exact-sheet-bytes
  byte_change_policy: require-reconfirmation

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
- The ledger is append-only and receives exactly one dispatch row and one
  paired close row per dispatch.
- The tension gate can run two independent checks.
- The confirmation-readiness validator accepts the exact temporary sheet without
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
- The agent pool or runtime provider is resolvable and every agent has one
  eligible, unique identity before confirmation. Its exact initial prompt
  begins with `You are {agent_name}.` followed by a blank line.
- Final-approver eligibility is deterministic and consistent with the local
  sheet schema and registrar.
- Draft revision authorization is not dispatch confirmation; a normal ready
  proposal asks once.
- Human confirmation binds the exact sheet bytes. Every byte revision reruns
  machine readiness and tension checks and requires explicit reconfirmation.
- A successful registrar call records the sheet digest in the YAML ledger and
  consumes only a `*.tmp.json` beneath the configured temporary root.
- Invalid records and failed appends preserve their temporary JSON for diagnosis.
- No per-dispatch sheet, material projection, runtime profile, or ledger is
  persisted beside result artifacts.
- Post-result hooks are explicitly configured or explicitly absent.
- Publication rules prevent private evidence from crossing into public paths.
