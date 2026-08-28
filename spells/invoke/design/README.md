# Design

Agreeing on the words a project uses does not decide how the project will
work. A team may agree on what a *return case* and an *inspection window* are,
but still disagree about which service stores the case, which component records
an inspection, or what must happen before a refund can be approved.

Design resolves those questions before implementation planning begins. It
records what belongs inside the system, which part owns each responsibility,
how parts exchange information, what sequence moves the work forward, which
rules choose an outcome, and which existing systems the project must continue
to use.

## Why Design follows Define

Define establishes what the project's important terms refer to and where those
definitions apply. Design uses those checked definitions when it assigns work
to components, names interfaces, and describes workflows.

If Design begins first, two components can use the same word for different
things. For example, one service might treat *customer* as a person while
another treats it as a billing account. Design can look internally consistent
and still connect the wrong records or give a component responsibility it does
not own.

## Why Design comes before Plan

Plan turns a checked design into implementation tasks. It needs more than a
feature goal. It needs to know which component will change, which interface it
must preserve, which event or state transition must be added, and which
dependency can block the work.

Design supplies those decisions. It does not split them into coding tasks,
estimate them, or authorize anyone to change the repository.

## What Design checks

Design begins with the project goal and an admitted Define result. It then
checks the material that can constrain the design:

- existing designs for the same or adjacent systems;
- current components, stores, queues, APIs, events, and external services;
- the owner-approved repository areas that may contain relevant inputs;
- constraints, invariants, and earlier decisions that must remain true;
- the owner of each responsibility and interface; and
- the systems, documents, and tools that will consume the result.

The approved input boundary matters. A Design result can prove that it checked
every file inside that boundary. It cannot claim that it searched parts of the
repository the owner did not include.

## Questions Design answers

| Question | Concrete result |
| --- | --- |
| What is inside the system? | A boundary showing which people, services, and external systems participate. |
| Who does each job? | Components with named responsibilities, such as a returns service owning return-case state. |
| What information moves between parts? | Contracts and interfaces, such as a `ReturnInspected` event carrying the case ID and inspection result. |
| What happens in what order? | Workflow steps and states, such as requested → received → inspected → refund pending. |
| How is an outcome chosen? | Decision rules, such as sending a failed inspection to manual review instead of refund approval. |
| What must the system depend on? | Dependencies such as a payment provider, inventory service, or existing customer record. |

These answers belong together. A workflow step that names no responsible
component, an event with no receiver, or a decision with no possible outcomes
is not a usable design.

## From checked definitions to a checked design

The process can be retold as one sequence:

```text
Project goal and admitted definitions
    ↓
Approve which repository inputs Design must inspect
    ↓
Catalog those inputs and resolve conflicts or missing ownership
    ↓
Describe components, contracts, workflows, decisions, and dependencies
    ↓
Generate one structured design and readable views
    ↓
Rebuild the bundle independently and compare every output byte
```

If an input is stale, an owner is unresolved, an interface has no source, or
the rebuilt files differ, the process stops and names the item that must be
repaired.

## What Design produces

The principal output is one structured Design accompanied by readable views
and checking records:

| File | Purpose |
| --- | --- |
| `DESIGN.json` | The complete component, contract, workflow, decision, state, and dependency model used by tools and later planning. |
| `ARCHITECTURE.md` | A readable explanation of the same model. |
| `SELECTED-COMPANIONS.md` | The additional UX, research, spell, or sigil material selected for later work. |
| `IMPLEMENTATION-LAYERING.md` | The order in which later planning may prove and combine implementation layers. |

Supporting JSON records identify the exact inputs, selected outputs, planned
witnesses, and validation results. They show what was checked; they do not add
new architectural decisions that are absent from `DESIGN.json`.

## A returns example

Continue the returns feature introduced in Define:

- The **returns service** creates the return case and owns its current state.
- The **inspection component** records whether the returned goods passed
  inspection. It does not approve refunds.
- The inspection component emits `ReturnInspected` with the return-case ID,
  result, and inspection time.
- The **returns service** receives that event and checks whether the inspection
  happened inside the defined inspection window.
- A passing result inside the window moves the case to **refund pending**. A
  failed or late result moves it to **manual review**.
- The **refund service** reads the approved refund request and calls the payment
  provider. It does not own the inspection result or the return-case workflow.

This example can be checked. Each responsibility has an owner, the event has a
sender and receiver, the workflow names its states, the decision names both
outcomes, and the payment provider is an explicit dependency.

## When Design must check again

A previously admitted Design may no longer describe the current system when:

- a component gains or loses a responsibility;
- an API, event, store, queue, or message changes;
- a workflow step, state, or transition is added, removed, or reordered;
- a decision rule or one of its outcomes changes;
- a dependency or external system is added, removed, or replaced;
- ownership of a component, interface, or rule changes;
- an upstream definition or admitted Design input changes;
- a new consumer starts depending on a contract or event; or
- a readable view no longer matches `DESIGN.json`.

These are concrete forms of **design drift**. They can change who performs a
job, what information crosses an interface, or what the system does next. A
changed file is not automatically a changed design, but the difference must be
checked rather than dismissed from filenames or matching counts.

## What Design does not approve

A completed Design bundle does not automatically:

- change application code or infrastructure;
- approve an implementation plan;
- prove that planned tests or witnesses have run;
- replace an existing Design;
- release a registry entry;
- authorize execution, publication, or deployment; or
- transfer ownership of a component, interface, definition, or decision.

Design prepares checked material for Plan or another named lifecycle owner.
Those later processes keep their own review, acceptance, and execution gates.

## Continue from here

- To inspect the machine workflow without creating files, run
  `tools/arcanum invoke design describe` from the repository root.
- To author Design as an agent or operator, follow the
  [Design authoring guide](../design-authoring-guide.md).
- To inspect the formal mode rules and evidence requirements, read the
  [Design contract](../design.md).
- To understand the definitions that Design consumes, start with the
  [Define overview](../define/README.md).
