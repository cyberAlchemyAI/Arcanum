# Invoke Design Authoring Guide

This guide is for the agent or operator supplying Design decisions to the
stateless Invoke CLI. Human readers who first need to understand what Design
does should start with the [Design overview](./design/README.md). The formal
[Design contract](./design.md) remains the authority for gates and evidence.

## The Job In One Sentence

Turn one admitted Define result and one owner-approved set of repository inputs
into a checked description of components, responsibilities, interfaces,
workflows, decisions, states, and dependencies—without inventing approvals or
claiming that implementation has begun.

For the returns example, the agent decides that the returns service owns the
return-case state, the inspection component emits `ReturnInspected`, the
returns service chooses refund pending or manual review, and the refund service
calls the payment provider. The CLI records those supplied decisions in the
required structure; it does not choose them.

## The Complete Path

```text
current Define v3 stage + admission v1
    ↓
owner-supplied input boundary
    ↓
DESIGN-INPUT-CLOSURE.json v2
    ↓
W1 v2 input bundle
    ↓
DESIGN-SOURCE.json v2
    ↓
W2 v2 candidate
    ↓
DESIGN-BUNDLE-CLOSURE.json v2 + external Distill PASS
    ↓
W3 v3 final bundle
    ↓
independent admission v2
    ↓
artifact_authored capability status
```

Each arrow has a separate check. A later PASS cannot repair a stale input, an
unowned responsibility, an unresolved interface, or missing independent
evidence from an earlier stage.

## Use The Stateless CLI

Inspect the available modes and the current Design stages before authoring:

```text
tools/arcanum invoke modes
tools/arcanum invoke design describe
tools/arcanum invoke design describe boundary
tools/arcanum invoke design describe source
tools/arcanum invoke design describe admission
```

`describe` shows the request schema, output schema, fixed fields, derived
fields, available operations, and next stage. JSON Schemas and the CLI stage
catalog remain the machine authority. This guide explains how to supply useful
content; it does not replace those contracts.

Every mutating operation receives one explicit output path that must not
already exist. The CLI keeps no session state and never overwrites a previous
result. Pass each earlier output explicitly to its consumer.

## The Nine Stages

| Stage | What a person or agent supplies | What the CLI or validator produces |
| --- | --- | --- |
| 1. Boundary | The target, visibility, observation time, repository roots, discovery rules, required input classes, and exact allowed exclusions approved by the target owner. | `DESIGN-INPUT-BOUNDARY-APPROVAL.json` with calculated IDs, directory digests, sizes, and approval digest. |
| 2. Input closure | Every discovered file, its owner and use, conflict resolutions, constraints, existing Design status, and concrete signals such as components, interfaces, states, and decisions. | `DESIGN-INPUT-CLOSURE.json` v2 with exact evidence hashes and closure digest. |
| 3. Input bundle | The completed closure and its exact repository root. | Five W1 v2 files proving coverage only inside the approved roots and rules. |
| 4. Source | The component, contract, workflow, state, decision, dependency, view, glossary, witness, and routing decisions that apply every W1 input. | `DESIGN-SOURCE.json` v2 with fixed profile, route, authority ceiling, evidence hashes, and source digest. |
| 5. Candidate | The exact Design source and W1 bundle it binds. | `DESIGN.json`, an independent coherence receipt, and the W2 v2 candidate-production receipt. |
| 6. Bundle closure | The exact W2 receipt, fixed output list, and externally supplied Distill request, event log, execution receipt, and validation result. | `DESIGN-BUNDLE-CLOSURE.json` v2. |
| 7. Final bundle | The complete bundle closure. | Fourteen payloads plus `INVOKE-DESIGN-STAGE-RECEIPT.json` v3 in one atomic directory. |
| 8. Admission | The unchanged W3 directory. | An external admission v2 receipt after a clean replay produces byte-identical files. |
| 9. Status | The exact W3 stage and admission receipts inside a capability-status request. | Independent `artifact_authored`, `registry_released`, and `mutation_runtime_ready` axes. |

## Know Who Supplies Every Value

| Value | Owner |
| --- | --- |
| The repository roots and permitted exclusions | Target owner. The CLI can record this approval but cannot grant it. |
| Components, responsibilities, stores, interfaces, events, workflows, states, decisions, and dependencies | Design author, backed by admitted inputs and explicit owner decisions. |
| Existing definitions | The admitted Define v3 bundle and its current admission v1. Design refers to them; it does not rewrite them. |
| Existing Design used for evolution | The current predecessor's W3 v3 stage and admission v2. The author selects it explicitly. |
| Schema IDs, versions, installed profiles, fixed filenames, calculated IDs, hashes, sizes, and digests | CLI and installed producers. These fields are omitted from authoring requests. |
| Input-closure, coherence, replay-admission, and capability results | Their independent validators. The author cannot self-issue them. |
| Distill execution and validation evidence | External Distill owners. The CLI only checks exact supplied files. |

Never manufacture a target-owner approval, Define admission, predecessor
selection, Distill PASS, coherence verdict, or bundle admission. If the
responsible owner has not supplied it, stop and route to that owner.

## W1: Close The Exact Inputs

W1 answers a concrete question: *which files must this Design respect, and what
does each file require?* Its completeness is limited to the directories,
include rules, and exact exclusions approved by the target owner.

A boundary is not a vague statement such as “inspect the architecture.” It
names the target, repository-relative directories, file patterns, visibility,
observation time, required input classes, and any exact file the owner permits
the run to exclude.

Check and author the boundary:

```text
tools/arcanum invoke design check boundary \
  --request BOUNDARY-AUTHORING-REQUEST.json \
  --repo-root ROOT

tools/arcanum invoke design author boundary \
  --request BOUNDARY-AUTHORING-REQUEST.json \
  --repo-root ROOT \
  --output DESIGN-INPUT-BOUNDARY-APPROVAL.json
```

Then catalog the discovered files. For each file, record who owns it, whether
it applies, and what it contributes: for example, the current return-state
file supplies the allowed states, an event schema supplies the
`ReturnInspected` fields, and a payment adapter supplies the external refund
interface. Resolve every conflict and conditional input instead of silently
choosing one.

```text
tools/arcanum invoke design check input-closure \
  --request CLOSURE-AUTHORING-REQUEST.json \
  --repo-root ROOT

tools/arcanum invoke design author input-closure \
  --request CLOSURE-AUTHORING-REQUEST.json \
  --repo-root ROOT \
  --output DESIGN-INPUT-CLOSURE.json

tools/arcanum invoke design produce input-bundle \
  --closure DESIGN-INPUT-CLOSURE.json \
  --repo-root ROOT \
  --output ABSENT_W1_DIRECTORY
```

Normal W1 requires a current Define v3 stage receipt and its matching,
drift-free admission v1. Discovery W1 can inspect an approved boundary, but it
cannot activate W2. See the detailed
[Design input authoring guide](./design-input-authoring-guide.md) and the
[boundary request schema](./schemas/design-input-boundary-authoring-request-v1.schema.json).

## W2: State What The System Will Do

W2 applies every W1 item to one typed Design source. An application states how
one input affects the design. For example, the inspection-window definition
may constrain the `choose-refund-route` decision, while an excluded historical
prototype has no component or workflow records and keeps its exact exclusion
evidence.

Author concrete records instead of category labels:

- an `actor` such as a customer or returns operator;
- a `system` such as returns management;
- a `component` such as the returns service or inspection component;
- a `contract` or `interface` such as `ReturnInspected` or the refund API;
- a `workflow-step` and `state` such as inspect return and refund pending;
- a `decision` such as choose refund route;
- a `dependency` such as the payment provider; and
- a `store`, `queue`, or other installed fact kind only when an admitted input
  requires it.

Every identifier must resolve. Every responsibility must name its component.
Every event or API must name the parts that send, receive, or implement it.
Every workflow transition must point to a valid next step or state. Every
decision must identify its inputs and possible outcomes.

Check and author the source, then compile the candidate:

```text
tools/arcanum invoke design check source \
  --request DESIGN-SOURCE-AUTHORING-REQUEST.json \
  --repo-root ROOT

tools/arcanum invoke design author source \
  --request DESIGN-SOURCE-AUTHORING-REQUEST.json \
  --repo-root ROOT \
  --output DESIGN-SOURCE.json

tools/arcanum invoke design produce candidate \
  --source DESIGN-SOURCE.json \
  --repo-root ROOT \
  --output ABSENT_W2_DIRECTORY
```

The coherence validator checks observable relationships: every W1 item is
applied, referenced IDs exist, component and contract links resolve, the
selected outputs are preserved, and each view contains only permitted record
kinds. It does not decide whether the author chose the best architecture.

See the detailed [Design source authoring guide](./design-source-authoring-guide.md)
and [source request schema](./schemas/design-source-v2-authoring-request-v1.schema.json).

## Put Each Record In A Useful View

The six views are different reading routes through the same `DESIGN.json`
records:

1. **Context** shows the people, system, and external services around the
   target—for example, customer, returns management, and payment provider.
2. **High-level structure** shows the major parts and their connections—for
   example, returns, inspection, and refund services.
3. **Low-level components** shows each component's responsibility, store, API,
   event, queue, or internal contract.
4. **Workflow process** shows steps and states—for example, requested → received
   → inspected → refund pending.
5. **Decision flow** shows which information selects an outcome—for example,
   inspection result plus inspection time selecting refund pending or manual
   review.
6. **Dependency interface** shows required connections to existing or external
   systems—for example, the refund service calling the payment provider.

Views contain record IDs; they do not create additional decisions. A record
missing from a view still exists in the registry, but a required view that
cannot show its relevant records blocks candidate production.

## W3: Bind Review And Reproduce The Bundle

W3 does not accept a claim that the candidate “looks good.” It requires four
exact Distill files showing that an external run reviewed the exact
`DESIGN.json` and candidate receipt. Both Distill execution and independent
validation must report `pass`.

Check and author the closure, then produce and admit the bundle:

```text
tools/arcanum invoke design check bundle-closure \
  --request BUNDLE-CLOSURE-AUTHORING-REQUEST.json \
  --repo-root ROOT

tools/arcanum invoke design author bundle-closure \
  --request BUNDLE-CLOSURE-AUTHORING-REQUEST.json \
  --repo-root ROOT \
  --output DESIGN-BUNDLE-CLOSURE.json

tools/arcanum invoke design produce final-bundle \
  --closure DESIGN-BUNDLE-CLOSURE.json \
  --repo-root ROOT \
  --output ABSENT_W3_DIRECTORY

tools/arcanum invoke design admit admission \
  --bundle W3_DIRECTORY \
  --repo-root ROOT \
  --output DESIGN-BUNDLE-ADMISSION-RECEIPT.json
```

Admission leaves the submitted directory unchanged. It rebuilds the bundle in
temporary storage and compares every filename and byte. A different
`ARCHITECTURE.md`, a missing receipt, an added file, or a changed
`DESIGN.json` blocks admission.

See the detailed [Design bundle authoring guide](./design-bundle-authoring-guide.md)
and [bundle-closure request schema](./schemas/design-bundle-closure-v2-authoring-request-v1.schema.json).

## Resolve Capability Status

After W3 and admission pass, submit both exact receipts to the capability
resolver:

```text
tools/arcanum invoke design status \
  --request DESIGN-STATUS-REQUEST.json \
  --repo-root ROOT \
  --output DESIGN-CAPABILITY-STATUS.json
```

A valid W3 v3 stage plus admission v2 may open only
`artifact_authored`. Registry release and mutation-runtime readiness remain
separate axes with separate owner evidence.

## Greenfield And Evolution

Greenfield Design requires exact evidence that no applicable prior Design was
found inside the approved roots. It is not a label the author can choose to
avoid examining an existing system.

Evolution requires one current predecessor: its `DESIGN.json`, W3 v3 stage
receipt, and admission v2 must agree on the target and complete file inventory.
Historical v1/v2 stage receipts, admission v1, Markdown prose, or a copied
`DESIGN.json` cannot activate evolution. If two possible predecessors remain,
stop and obtain an owner decision rather than selecting one implicitly.

## Handle Failure At The Owning Stage

- Exit `0` means the requested operation passed and wrote its declared output
  when the operation has one.
- Exit `1` means the evidence was evaluated and blocked. Read the diagnostic's
  JSON Pointer or evidence selector, causal blockers, and repair route.
- Exit `2` means the request or invocation could not be evaluated—for example,
  malformed JSON, a missing required argument, or an existing output target.

Do not repair a W1 input problem by changing W2 architecture, and do not repair
a missing Distill result by editing the W3 closure. Return to the stage and
owner named by the diagnostic, create a new absent output, and pass that exact
result forward.

## Retell-Chain Check

Before calling the documentation or authored source complete, verify that
another agent can retell this chain without reading field names:

1. The Define result establishes what *return case* and *inspection window*
   refer to.
2. W1 identifies the exact state, event, payment-interface, and owner evidence
   the Design must respect.
3. W2 assigns the return-case state to the returns service, the inspection
   result to the inspection component, and refund execution to the refund
   service.
4. `ReturnInspected` moves information from inspection to the returns workflow.
5. The inspection result and time choose refund pending or manual review.
6. W3 binds independent review, generates the readable bundle, and proves that
   a clean replay produces the same bytes.
7. The result can enter Plan only through Plan's own evidence and approval
   gates.

If the retell relies on phrases such as “apply the architecture,” “preserve
meaning,” or “ensure coherence” without naming a component, interface, state,
decision, or dependency, the explanation is still too abstract.

## Claim Ceiling

W1 PASS proves only that the approved directories and file rules were covered,
their inputs were classified, and selection reached a fixed result. W2 PASS
proves that the supplied Design source applied those inputs and projected a
deterministic candidate whose IDs and view memberships passed the installed
checks. W3 stage plus admission proves that the exact final bundle can be
reproduced byte for byte.

None of those results proves that the architecture is optimal or implemented.
They do not run planned witnesses, approve a Plan, change code, release a
registry, open mutation-runtime readiness, transfer ownership, publish,
promote, deploy, or create an external effect.
