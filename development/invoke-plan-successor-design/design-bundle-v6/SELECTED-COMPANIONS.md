# Selected Design Companions: invoke:plan-successor:definition-target

This aggregate is a deterministic view of the selected companion records in `DESIGN.json`.

## `architecture:authority-trust`

| Fact ID | Kind | Name | Owner |
| --- | --- | --- | --- |
| `contract:plan-source-v2` | `contract` | Canonical Plan source contract | `invoke-plan-owner` |
| `decision:external-lifecycle-state` | `decision` | External lifecycle evidence | `authority-owner` |
| `decision:single-plan-source` | `decision` | Single Plan source authority | `authority-owner` |
| `risk:derived-view-authority` | `risk` | Derived view becomes a second source | `authority-owner` |
| `rule:single-plan-source` | `normative-rule` | W1 normative rules: rule:single-plan-source | `invoke-plan-owner` |

Requirement references:
- `selected-output:architecture:authority-trust`

## `architecture:failure-compensation`

| Fact ID | Kind | Name | Owner |
| --- | --- | --- | --- |
| `effect:implementation-execution` | `effect` | W1 effects: effect:implementation-execution | `invoke-plan-owner` |
| `risk:false-observer-closure` | `risk` | Prose mistaken for observer closure | `signal-observer-owner` |
| `risk:historical-plan-activation` | `risk` | Historical Plan format establishes new PASS | `migration-owner` |
| `state:plan-blocked` | `state` | Plan blocked | `invoke-plan-owner` |
| `workflow:admit-plan-bundle` | `workflow-step` | Admit Plan bundle | `invoke-plan-admission-owner` |

Requirement references:
- `selected-output:architecture:failure-compensation`

## `architecture:integration-versioning`

| Fact ID | Kind | Name | Owner |
| --- | --- | --- | --- |
| `component:execution-contract-projector` | `component` | Execution contract projector | `implementation-readiness-owner` |
| `contract:conditional-consumer-applicability` | `contract` | Conditional consumer applicability contract | `interface-owner` |
| `contract:consumer-applicability-matrix` | `contract` | Per-consumer applicability matrix | `interface-owner` |
| `contract:native-context-version` | `contract` | Native-context version selection contract | `context-builder-owner` |
| `decision:context-builder-applicability` | `decision` | Context Builder applicability | `context-builder-owner` |
| `decision:dispatch-applicability` | `decision` | Dispatch applicability | `dispatch-spec-owner` |
| `decision:goal-applicability` | `decision` | Goal applicability | `goal-owner` |
| `decision:implementation-readiness-applicability` | `decision` | Implementation Readiness applicability | `implementation-readiness-owner` |
| `decision:observer-applicability` | `decision` | Signal Observer applicability | `signal-observer-owner` |
| `decision:observer-gap` | `decision` | Signal Observer machine-gap treatment | `signal-observer-owner` |
| `decision:task-session-applicability` | `decision` | Task Session applicability | `task-session-owner` |
| `decision:wpra-applicability` | `decision` | WPRA applicability | `work-pack-readiness-audit-owner` |
| `dependency:task-context-route` | `dependency` | Task and context route dependency | `interface-owner` |
| `dependency:wpra-readiness` | `dependency` | Plan to readiness dependency | `interface-owner` |
| `interface:define-to-design` | `interface` | W1 interfaces: interface:define-to-design | `invoke-plan-owner` |
| `interface:design-to-distill-v1` | `interface` | W1 interfaces: interface:design-to-distill-v1 | `invoke-plan-owner` |
| `interface:plan-to-context-builder` | `interface` | W1 interfaces: interface:plan-to-context-builder | `invoke-plan-owner` |
| `interface:plan-to-dispatch` | `interface` | W1 interfaces: interface:plan-to-dispatch | `invoke-plan-owner` |
| `interface:plan-to-goal` | `interface` | W1 interfaces: interface:plan-to-goal | `invoke-plan-owner` |
| `interface:plan-to-observer` | `interface` | W1 interfaces: interface:plan-to-observer | `invoke-plan-owner` |
| `interface:plan-to-readiness` | `interface` | W1 interfaces: interface:plan-to-readiness | `invoke-plan-owner` |
| `interface:plan-to-task-session` | `interface` | W1 interfaces: interface:plan-to-task-session | `invoke-plan-owner` |
| `interface:plan-to-wpra` | `interface` | W1 interfaces: interface:plan-to-wpra | `invoke-plan-owner` |
| `risk:false-observer-closure` | `risk` | Prose mistaken for observer closure | `signal-observer-owner` |
| `workflow:produce-plan-bundle` | `workflow-step` | Produce complete Plan bundle | `invoke-plan-owner` |
| `workflow:project-consumer-contracts` | `workflow-step` | Project applicable consumer contracts | `interface-owner` |

Requirement references:
- `selected-output:architecture:integration-versioning`

## `architecture:migration-rollout`

| Fact ID | Kind | Name | Owner |
| --- | --- | --- | --- |
| `compatibility:work-pack-source` | `compatibility-boundary` | W1 compatibility boundaries: compatibility:work-pack-source | `invoke-plan-owner` |
| `component:plan-migration-validator` | `component` | Plan migration validator | `migration-owner` |
| `contract:plan-source-v2` | `contract` | Canonical Plan source contract | `invoke-plan-owner` |
| `risk:historical-plan-activation` | `risk` | Historical Plan format establishes new PASS | `migration-owner` |

Requirement references:
- `selected-output:architecture:migration-rollout`

## `architecture:persistence-concurrency`

| Fact ID | Kind | Name | Owner |
| --- | --- | --- | --- |
| `component:plan-bundle-admission-validator` | `component` | Plan bundle admission validator | `invoke-plan-admission-owner` |
| `component:plan-bundle-producer` | `component` | Plan bundle producer | `invoke-plan-owner` |
| `contract:plan-bundle-admission` | `contract` | Plan bundle admission contract | `invoke-plan-admission-owner` |
| `workflow:produce-plan-bundle` | `workflow-step` | Produce complete Plan bundle | `invoke-plan-owner` |
| `writer:plan-bundle` | `writer` | W1 writers: writer:plan-bundle | `invoke-plan-owner` |

Requirement references:
- `selected-output:architecture:persistence-concurrency`

## `architecture:quality`

| Fact ID | Kind | Name | Owner |
| --- | --- | --- | --- |
| `component:plan-bundle-admission-validator` | `component` | Plan bundle admission validator | `invoke-plan-admission-owner` |
| `component:plan-source-validator` | `component` | Plan source validator | `invoke-plan-owner` |
| `contract:plan-bundle-admission` | `contract` | Plan bundle admission contract | `invoke-plan-admission-owner` |
| `risk:derived-view-authority` | `risk` | Derived view becomes a second source | `authority-owner` |

Requirement references:
- `selected-output:architecture:quality`

## `architecture:state-event`

| Fact ID | Kind | Name | Owner |
| --- | --- | --- | --- |
| `rule:terminal-plan-handoff` | `normative-rule` | W1 normative rules: rule:terminal-plan-handoff | `invoke-plan-owner` |
| `state:plan-artifact-authored` | `state` | Plan artifact authored | `invoke-plan-owner` |
| `state:plan-blocked` | `state` | Plan blocked | `invoke-plan-owner` |
| `state:plan-bundle-admitted` | `state` | Plan bundle admitted | `invoke-plan-admission-owner` |
| `state:plan-bundle-compiled` | `state` | Plan bundle compiled | `invoke-plan-owner` |
| `state:plan-source-draft` | `state` | Plan source draft | `invoke-plan-owner` |
| `state:plan-source-valid` | `state` | Plan source valid | `invoke-plan-owner` |
| `workflow:admit-plan-bundle` | `workflow-step` | Admit Plan bundle | `invoke-plan-admission-owner` |
| `workflow:compile-plan-graph` | `workflow-step` | Compile Plan graph | `invoke-plan-owner` |
| `workflow:produce-plan-bundle` | `workflow-step` | Produce complete Plan bundle | `invoke-plan-owner` |
| `workflow:project-consumer-contracts` | `workflow-step` | Project applicable consumer contracts | `interface-owner` |
| `workflow:project-plan-views` | `workflow-step` | Project Plan human views | `plan-work-pack-owner` |
| `workflow:validate-plan-source` | `workflow-step` | Validate Plan source | `invoke-plan-owner` |

Requirement references:
- `selected-output:architecture:state-event`

## `ux-plan`

| Fact ID | Kind | Name | Owner |
| --- | --- | --- | --- |
| `actor:plan-coordinator` | `actor` | W1 human actors: actor:plan-coordinator | `invoke-plan-owner` |
| `component:plan-view-projector` | `component` | Plan view projector | `plan-work-pack-owner` |
| `contract:work-pack-navigation` | `contract` | Generated Work Pack navigation contract | `ux-plan-owner` |
| `surface:generated-work-pack` | `rendered-surface` | W1 rendered surfaces: surface:generated-work-pack | `invoke-plan-owner` |

Requirement references:
- `selected-output:ux-plan`

## `validation-contracts`

| Fact ID | Kind | Name | Owner |
| --- | --- | --- | --- |
| `claim:w1-input-closure` | `acceptance-readiness-claim` | W1 acceptance and readiness claims: claim:w1-input-closure | `invoke-plan-owner` |
| `component:plan-bundle-admission-validator` | `component` | Plan bundle admission validator | `invoke-plan-admission-owner` |
| `component:plan-evidence-resolver` | `component` | Plan evidence resolver | `invoke-plan-owner` |
| `component:plan-source-validator` | `component` | Plan source validator | `invoke-plan-owner` |
| `contract:conditional-consumer-applicability` | `contract` | Conditional consumer applicability contract | `interface-owner` |
| `contract:consumer-applicability-matrix` | `contract` | Per-consumer applicability matrix | `interface-owner` |
| `contract:native-context-version` | `contract` | Native-context version selection contract | `context-builder-owner` |
| `contract:plan-bundle-admission` | `contract` | Plan bundle admission contract | `invoke-plan-admission-owner` |
| `effect:author-plan-artifacts` | `effect` | W1 effects: effect:author-plan-artifacts | `invoke-plan-owner` |
| `rule:all-machine-backed-plan-consumers` | `normative-rule` | W1 normative rules: rule:all-machine-backed-plan-consumers | `invoke-plan-owner` |
| `rule:native-context-version-by-transients` | `normative-rule` | W1 normative rules: rule:native-context-version-by-transients | `invoke-plan-owner` |
| `rule:observer-machine-contract-required` | `normative-rule` | W1 normative rules: rule:observer-machine-contract-required | `invoke-plan-owner` |

Requirement references:
- `selected-output:validation-contracts`

These companions do not promote templates or complete Spellcraft, Sigil Development, UX, research, or Plan lifecycles.
