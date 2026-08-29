# Governance Flow Decision View

> Deterministically derived from the schema-valid machine graph. This view is non-authoritative and cannot widen its source.

## Digest Bindings

- Source SHA-256: `13b5cddb6ff0e0d731ddf4c2fb1163e8d465675771e646a860f13fcaff29d631`
- Decision graph SHA-256: `ab5df8f6c1046e5daa73db03f245ba408c2cb99840ec9277204a2619074b05d4`
- Renderer SHA-256: `88c2627fd5da7feafceb87dccad33dad016917a157dceafcdd75044ad8393347`

## Decision Identity

- Flow: `terminal-boundary-fixture-v1`
- Owner: `fixture-owner`
- Lifecycle route: `fixture-local-route`
- Request budget: `1`

## Exact Targets

| Path | Baseline SHA-256 | Postimage SHA-256 | Visibility |
| --- | --- | --- | --- |
| `outputs/result.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `5e2b18710851f48a53f68bd4932f4a167c34a967ad399d59539d2006facac418` | `public` |

## Authority and Risk

- Write Paths: `outputs/result.txt`
- Execution: `allowed`
- Publication: `denied`
- Git: `denied`
- Deployment: `denied`
- Credentials: `denied`
- Destructive Actions: `denied`
- External Effects: `denied`
- Successor Execution: `denied`
- Selection Required: `allowed`
- Admission Required: `allowed`
- Risk class: `low`
- Risk reasons: `isolated local fixture output only, no external calls or successor execution`

## Authority-Bearing Executable

- Path: `development/fixtures/positive/terminal-boundary-executor.py`
- SHA-256: `c77054bf9e9a87bc41e7f01f00cb6b5d442106f0f10331d2e9eeb851e5266cd9`
- Mode: `python_script`
- Arguments: `["--target","outputs/result.txt","--content","governance-flow-terminal\n"]`
- Working directory: `{isolated_root}`
- Environment allowlist: `none`

## Independent Review

- Required: `allowed`
- Reviewer: `fixture-independent-reviewer`
- Reviewer role: `independent-governance-review`

## Terminal Outcome

- Promised boundary: `local-output-materialized`
- Required effects: `write:outputs/result.txt`
- Prohibited effects: `external_call, successor_execution, write_outside_ceiling`
- Completion predicate: `exact_terminal_match`
- Terminal observer: `governance-flow-runner-v1`

## Mode Boundary

1. Preacceptance collects every reachable no-effect blocker and preserves the first nonzero.
2. Human-decision mode emits at most one idempotent request for this frozen graph and stops.
3. Effectful execution requires exact acceptance, selection, and admission, then fails fast to the promised terminal boundary.

Preparation, rehearsal, freeze, review, and request emission grant no execution, publication, Git, deployment, credential, destructive-action, external-effect, or successor authority.

## Metric Targets

| Metric | Event | Target |
| --- | --- | --- |
| `blockers_discovered_after_request` | `governance_flow.late_blocker.v1` | `0` |
| `manual_receipt_transfers` | `governance_flow.receipt_transfer.v1` | `0` |
| `postacceptance_consumer_defects` | `governance_flow.consumer_defect.v1` | `0` |
| `prompts_per_immutable_graph` | `governance_flow.owner_prompt.v1` | `1` |
| `unchanged_byte_approval_retries` | `governance_flow.request_retry.v1` | `0` |

Aggregate completion remains false until the exact terminal receipt satisfies the frozen terminal predicate; component PASS is not terminal completion.
