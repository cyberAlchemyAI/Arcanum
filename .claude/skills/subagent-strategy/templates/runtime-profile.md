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
  validator: <command>

tension_gate:
  capability: <skill-or-file>
  independent_checks: 2

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
- The agent pool or runtime provider is resolvable before confirmation.
- Post-result hooks are explicitly configured or explicitly absent.
- Publication rules prevent private evidence from crossing into public paths.
