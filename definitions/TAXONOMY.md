# Meta-Concept Taxonomy

> **Example / explanatory layer.** This is the human-facing catalog of the DomainSpec meta-types with examples and selection guidance. The **canonical, normative** definition is [`DEFINITIONS.md#ds-d1-meta-type-system`](DEFINITIONS.md#ds-d1-meta-type-system) (DS-D1). Where wording differs, DS-D1 is authoritative.

> The 25 building blocks for describing any domain — 14 backend and 11 UI. Every concept in your system maps to exactly one of these types.

## Overview

### Backend Meta-Concepts (14)

| Category       | Meta-Concept  | Purpose                                          |
| -------------- | ------------- | ------------------------------------------------ |
| **Structural** | Entity        | Identity-bearing domain objects with lifecycle   |
|                | Value Object  | Identity-less reusable concepts (Money, Address) |
|                | Enum / Type   | Finite sets of states or categories              |
| **Behavioral** | Operation     | Business action that changes state (≈ mutation)  |
|                | Query         | Reads data without side effects                  |
|                | Calculation   | Derives a value from inputs                      |
|                | Rule          | Business constraint or validation                |
|                | Policy        | Decision logic that selects behavior             |
|                | Workflow      | Multi-step orchestration of operations           |
|                | Saga          | Cross-feature transactional orchestration        |
| **Connective** | Interface     | API boundary — REST, GraphQL, module contract    |
|                | Event         | Notification of something that happened          |
|                | Mapping       | Data transformation between shapes               |
| **Lifecycle**  | State Machine | States + transitions + guards + effects          |

### UI Meta-Concepts (11)

| Category              | Meta-Concept    | Purpose                                              | Backend Counterpart  |
| --------------------- | --------------- | ---------------------------------------------------- | -------------------- |
| **UI Structural**     | Page            | Routable URL view with layout + auth gate            | —                    |
|                       | Layout          | Reusable page shell (sidebar, header, slot)          | —                    |
|                       | Component       | Composable UI building block with typed props        | —                    |
|                       | View Model      | Shaped data optimized for rendering                  | Value Object         |
| **UI Behavioral**     | Hook            | Encapsulated reactive data/state logic               | —                    |
|                       | Form            | Schema-validated user input contract                 | —                    |
|                       | Action          | User-triggered mutation or navigation                | —                    |
|                       | Guard           | Client-side access gate (auth, permissions)          | Rule                 |
| **UI Connective**     | Binding         | Named connection between hook and API endpoint       | Interface            |
|                       | Adapter         | Data shape transformation at UI boundary             | Mapping              |
| **UI Presentational** | State Indicator | Visual encoding of domain state (badge, icon, color) | State Machine / Enum |

---

## Structural — What things exist

These define the **nouns** of the domain: the objects, values, and categories that make up the data model.

### Entity

An object with a unique identity that persists over time and moves through a lifecycle. Two entities with the same field values are still different if they have different IDs. Entities are the primary "actors" in the domain — operations act on them, state machines track their lifecycle, events announce changes to them.

> _Examples:_ User, Order, PaymentTransaction, Invoice, Subscription

_When to use:_ If you'd give it an ID in a database and track its history, it's an entity.

**Documented in:** `domain.md` → Entities section
**Template:** templates/domain.md
**Example:** examples/payment-processing/domain.md — PaymentTransaction

**Typical structure:**

- Field table (name, type, required, description)
- Link to state machine (if lifecycle exists)
- Links to operations that act on it

### Value Object

An immutable concept defined entirely by its fields, with no identity of its own. Two value objects with the same fields are equal. Value objects are often shared across features and embedded within entities.

> _Examples:_ Money (amount + currency), Address (street + city + zip), DateRange (start + end), Email

_When to use:_ If you compare two instances by their content (not ID), and they're interchangeable when equal, it's a value object.

**Documented in:** `domain.md` → Value Objects section, or `shared/{name}.md` if cross-feature
**Template:** templates/domain.md, templates/shared-value-object.md
**Example:** examples/shared/money.md — Money

**Typical structure:**

- Field table with constraints
- Equality definition
- Validation rules
- Operations on the value object (add, compare, etc.)

### Enum / Type

A fixed, finite set of named values that categorize or classify. Enums constrain which values a field can hold and often drive branching logic (different behavior per enum value).

> _Examples:_ PaymentMethod (CREDIT_CARD, BANK_TRANSFER, WALLET), OrderStatus, UserRole, Currency

_When to use:_ If you can list all possible values and that list rarely changes, it's an enum.

**Documented in:** `domain.md` → Enums section
**Template:** templates/domain.md
**Example:** examples/payment-processing/domain.md — PaymentMethod, PaymentErrorCode

**Typical structure:**

- Value table (value, description)

---

## Behavioral — What happens

These define the **verbs** of the domain: actions, reads, logic, and processes.

### Operation

A business action that changes the state of one or more entities. Operations are the write side of the system — they validate input, check rules, perform calculations, transition state, and emit events. Every mutation in the system should map to a named operation.

> _Examples:_ ProcessPayment, CreateOrder, CancelSubscription, ApproveRefund

_When to use:_ If it changes state and has business meaning (not just a CRUD "update"), it's an operation. Document its rules, calculations, state transitions, postconditions, and error states.

**Documented in:** `operations.md`
**Template:** templates/operations.md
**Example:** examples/payment-processing/operations.md — ProcessPayment, RefundPayment, RetryPayment

**Typical structure:**

- Type, actor, trigger
- Input table
- Rules (with formal expressions)
- Calculations (with formulas)
- State transition
- Postconditions
- Error states

### Query

A read operation that retrieves data without side effects. Queries define what data consumers can ask for, with what filters, and in what shape. They separate the read model from the write model.

> _Examples:_ GetPaymentStatus, GetOrderHistory, SearchProducts, ListUserSubscriptions

_When to use:_ If calling it twice produces the same result and nothing changes, it's a query.

**Documented in:** `queries.md`
**Template:** templates/queries.md
**Example:** examples/payment-processing/queries.md — GetPaymentStatus, GetPaymentHistory

**Typical structure:**

- Input table
- Filters / pagination
- Output shape (with source entity fields)
- Authorization rules

### Calculation

A pure function that derives a value from inputs. Calculations are deterministic — same input always produces same output. They are used inside operations but documented separately because they carry their own formulas, edge cases, and testable properties.

> _Examples:_ FeeCalculation (amount × rate), TaxCalculation, DiscountAmount, ShippingCost

_When to use:_ If it has a formula and you'd want to test it independently of the operation that uses it, extract it as a calculation.

**Documented in:** `operations.md` → as a standalone section or inline within an operation
**Template:** templates/operations.md
**Example:** examples/payment-processing/operations.md — FeeCalculation

**Typical structure:**

- Rate/lookup table
- Formula
- Properties (non-negative, bounded, deterministic)

### Rule

A business constraint that must be satisfied for an operation to proceed. Rules are the **guards** of the system — they prevent invalid state transitions. Each rule has a formal expression that makes it unambiguous and directly testable.

> _Examples:_ MaxAmountRule (`amount <= 10000`), MinimumAgeRule (`user.age >= 18`), StockAvailabilityRule (`product.stock >= quantity`)

_When to use:_ If violating it should prevent an operation from executing, it's a rule. Rules answer: "Under what conditions is this operation allowed?"

**Documented in:** `operations.md` → Rules table within each operation
**Template:** templates/operations.md
**Example:** examples/payment-processing/operations.md — R1 through R10

**Typical structure:**

- ID, human-readable description, formal expression
- Documented inline within the operation they guard

### Policy

Decision logic that selects between different behaviors at runtime. Unlike rules (which block or allow), policies _choose_ how something happens. Policies encode business strategy and are often configurable.

> _Examples:_ RetryPolicy (when to retry, how many times), PricingPolicy (which discount tier applies), RoutingPolicy (which payment gateway to use), EscalationPolicy (when to notify a manager)

_When to use:_ If the system needs to choose between strategies based on context, it's a policy. Policies answer: "How should this be handled?"

**Documented in:** `workflows.md` → Policies section, or `operations.md` if embedded in an operation
**Template:** templates/workflows.md
**Example:** examples/payment-processing/SPEC.md — RetryPolicy (referenced in operations)

**Typical structure:**

- What it applies to
- Decision logic (conditions → selected behavior)
- Configuration parameters

### Workflow

A multi-step process that orchestrates multiple operations in sequence, with decision points, parallel paths, and compensation logic (undoing completed steps if a later step fails). Workflows are scoped to a single feature or bounded context.

> _Examples:_ OrderFulfillment (charge → reserve → ship → notify), UserOnboarding (register → verify email → setup profile), RefundProcess (validate → reverse charge → update inventory → notify)

_When to use:_ If it involves more than one operation coordinated across time or services within one feature, it's a workflow. Use Saga when orchestration crosses feature or bounded-context ownership.

**Documented in:** `workflows.md`
**Template:** templates/workflows.md

**Typical structure:**

- Mermaid flow diagram
- Step table (step → operation → on success → on failure)
- Policies at decision points
- Compensation table (how to undo completed steps)
- Invariants

### Saga

A long-running coordination process that orchestrates operations across multiple features or bounded contexts, with explicit compensation for partial failures. A saga owns cross-feature progression and rollback semantics.

> _Examples:_ OrderFulfillmentSaga (ordering → payment → shipping), WireTransferSaga (accounts → compliance → transfer), DeliveryOrderSaga (order → dispatch → payment)

_When to use:_ If orchestration spans ownership boundaries and requires cross-feature consistency guarantees, model it as a saga.

**Documented in:** `workflows.md`
**Template:** templates/workflows.md

**Typical structure:**

- Participant features/bounded contexts
- Forward-step sequence with entry/exit conditions
- Compensation step per participant
- Cross-context failure handling and retry/dead-letter policy
- End-state invariants across participants

---

## Connective — How things communicate

These define the **bridges** between parts of the system: boundaries, signals, and data transformations.

### Interface

An API boundary that exposes operations and queries to consumers. Interfaces can be external (REST endpoints, GraphQL schema) or internal (module contracts between services). They document the shape of data that crosses the boundary and how it maps to domain concepts.

> _Examples:_ PaymentAPI (REST), OrderGraphQL (GraphQL), PaymentModule (internal contract), NotificationService (internal)

_When to use:_ If there's a boundary where data changes shape or access is controlled, it's an interface. Document request/response shapes and the domain concepts they expose.

**Documented in:** `interfaces.md`
**Template:** templates/interfaces.md
**Example:** examples/payment-processing/interfaces.md — PaymentAPI (REST), PaymentModule (internal)

**Typical structure:**

- External: METHOD + path, auth, request fields with "Maps To" column, response table
- Internal: method signature table with "Maps To" column

### Event

A notification that something happened in the domain. Events are the past-tense announcements of state changes — they decouple the thing that happened from the things that react to it. Each event has a typed payload and a list of consumers.

> _Examples:_ PaymentCompleted, OrderShipped, UserRegistered, SubscriptionCancelled

_When to use:_ If other parts of the system need to react to a state change without the source knowing about them, it's an event. Events answer: "What just happened?"

**Documented in:** `events.md`
**Template:** templates/events.md
**Example:** examples/payment-processing/events.md — PaymentInitiated, PaymentCompleted, PaymentFailed, RefundCompleted

**Typical structure:**

- Produced by (link to operation)
- Triggers transition (link to state machine)
- Payload table
- Consumed-by table (consumer → action)

### Mapping

A data transformation between two shapes. Mappings document field-by-field how data moves between domain entities, DTOs, API payloads, and external systems. They make the transformation explicit, including defaults, computed fields, and validation at the boundary.

> _Examples:_ RequestToTransaction (API → Entity), TransactionToResponse (Entity → API), ExternalGatewayToEvent (third-party webhook → domain event)

_When to use:_ If data crosses a boundary and its shape changes, document the mapping. This catches mismatches early and makes integration testable.

**Documented in:** `mappings.md`
**Template:** templates/mappings.md
**Example:** examples/payment-processing/mappings.md — RequestToTransaction, TransactionToResponse

**Typical structure:**

- From → To (with direction: inbound/outbound/bidirectional)
- Field mapping table (source → target → transform → notes)
- Defaults table
- Validation table

---

## Lifecycle — How things evolve

### State Machine

A formal specification of how an entity moves through states over time. State machines define: all possible states, valid transitions between them, guards (conditions for transitions), effects (side effects of transitions), and invariants (properties that must always hold). They are the most formal and testable meta-concept — producing transition tests, negative tests, and property-based tests.

> _Examples:_ PaymentStatus (Created → Processing → Completed/Failed), OrderLifecycle (Draft → Confirmed → Shipped → Delivered), SubscriptionState (Trial → Active → Cancelled)

_When to use:_ If an entity has a `status` field or moves through stages, it has a state machine. Document it with a mermaid diagram, transition table, invalid transitions, and invariants.

**Documented in:** `states.md`
**Template:** templates/states.md
**Example:** examples/payment-processing/states.md — PaymentStatus (8 states, 9 transitions, 6 invariants)

**Typical structure:**

- Mermaid `stateDiagram-v2` diagram
- States table (state, terminal?, description)
- Transition table (from, event, to, guard, effect)
- Invalid transitions table
- Invariants table (with formal expressions)

---

## UI Structural — What users see

These define the **surfaces** of the frontend: the pages, shells, building blocks, and shaped data that compose the user experience.

### Page

A routable URL that renders a complete view. Each page is bound to a layout, optionally gated by authentication/permissions, and renders one or more components as interactive islands. Pages are the entry points of the UI — every user journey starts at a page.

> _Examples:_ `/players` (All Players), `/login`, `/settlements`, `/coaches/[coachId]/players`

_When to use:_ If it has a URL and the user can navigate to it, it's a page. Document its route, layout, auth requirements, and the components it renders.

**Documented in:** `UI-SPEC.md` → Route Table
**Template:** templates/ui-spec.md

**Typical structure:**

- Route path, page title, layout reference
- Auth requirement and permission
- ASCII wireframe showing component arrangement

### Layout

A reusable page shell that provides consistent structure (sidebar, header, footer, content slot). Layouts wrap pages — they own the navigation chrome but not the page content. Multiple pages share the same layout.

> _Examples:_ DashboardLayout (sidebar + breadcrumb + content area), AuthLayout (centered card)

_When to use:_ If multiple pages share the same structural shell, extract it as a layout.

**Documented in:** `UI-SPEC.md` → Route Table (Layout column)
**Template:** templates/ui-spec.md

**Typical structure:**

- Slot diagram (where content renders)
- Navigation structure
- Responsive behavior

### Component

A composable UI building block with typed props. Components are the atoms and molecules of the interface — tables, cards, badges, dialogs, forms. Each component has a single responsibility and communicates through props and callbacks.

> _Examples:_ PlayersTable, SettlementPreviewCard, AssignPlayerDialog, StatsWindowCard, EligibilityBadge

_When to use:_ If it renders UI and can be composed into a page, it's a component. Document its purpose, prop contract, and which hooks it consumes.

**Documented in:** `UI-SPEC.md` → Component Inventory
**Template:** templates/ui-spec.md

**Typical structure:**

- Component name, type classification (Table, Card, Dialog, Badge, Form)
- File location
- Purpose description
- Props (if complex)

### View Model

A typed data shape optimized for rendering. View models decouple what the API returns from what the component needs to display. They are derived from backend entities but shaped for the UI — flattened, formatted, enriched with display-only fields.

> _Examples:_ PlayerOverview (entity + computed stats), SettlementPreview (flattened response), StatsWindow (aggregated period data)

_When to use:_ If the raw API response needs reshaping, formatting, or enrichment before the component can render it, extract a view model type.

**Documented in:** `UI-SPEC.md` → Data Flow section (hook return types)
**Template:** templates/ui-spec.md

**Typical structure:**

- TypeScript type definition
- Source entity reference
- Transformation notes (computed fields, formatting)

---

## UI Behavioral — What users do

These define the **interactions** of the frontend: the data fetching, form validation, mutations, and access control.

### Hook

Encapsulated reactive data/state logic exposed as a composable function. Hooks abstract TanStack Query calls, local state machines, and side-effect coordination behind a clean API. Components consume hooks — they never make API calls directly.

> _Examples:_ `usePlayers()`, `useSettlementPreview()`, `useCreatePlayer()`, `useProgression(id, period)`

_When to use:_ If a component needs data from an API, manages async state, or coordinates multiple state values, encapsulate it in a hook.

**Documented in:** `UI-SPEC.md` → Data Flow section
**Template:** templates/ui-spec.md

**Typical structure:**

- Hook name, return type
- API call(s) it wraps
- Cache key strategy
- Invalidation rules

### Form

A schema-validated user input contract. Forms combine field definitions, Zod validation schemas, error message mappings, and submission actions into a single documented unit. The schema must align with the backend interface it targets.

> _Examples:_ CreatePlayerForm (4 fields, Zod schema, 409 conflict handling), SettlementForm (3 fields, date refine)

_When to use:_ If the user enters data that must be validated before submission, it's a form. Document every field, its validation, and its error messages.

**Documented in:** `UI-SPEC.md` → Form Contracts section
**Template:** templates/ui-spec.md

**Typical structure:**

- Field table (name, type, input element, validation, error message)
- Zod schema code block
- API error code → UI message mapping

### Action

A user-triggered mutation or navigation. Actions are the write-side of the UI — button clicks, form submissions, dialog confirmations that invoke mutation hooks or trigger navigation. Each action has a trigger, target, and observable outcome.

> _Examples:_ Submit login form → `POST /auth/login`, Click "Assign" → `POST /coaches/:id/players/:pid`, Click "Preview" → fetch settlement preview

_When to use:_ If clicking something changes server state or navigates the user, it's an action. Document its trigger, the mutation hook it calls, and the UI outcome (toast, redirect, invalidation).

**Documented in:** `UI-SPEC.md` → Data Flow (On Success column) and Form Contracts (submission)
**Template:** templates/ui-spec.md

**Typical structure:**

- Trigger (button, form submit, dialog confirm)
- Mutation hook or navigation target
- On success: cache invalidation, toast, redirect
- On error: error display strategy

### Guard

A client-side access gate that controls page/component visibility based on authentication or permissions. Guards prevent unauthorized UI rendering and redirect to appropriate fallback routes. They mirror backend rules but operate at the presentation boundary.

> _Examples:_ AuthGuard (redirect to `/login` if no token), PermissionGuard (hide admin tabs for non-admin roles)

_When to use:_ If a page or component should only render for certain users/roles, protect it with a guard. Guards answer: "Can this user see this?"

**Documented in:** `UI-SPEC.md` → Route Table (Auth Required / Permission columns)
**Template:** templates/ui-spec.md

**Typical structure:**

- What it protects (page, component, route group)
- Check logic (token presence, role match)
- Fallback (redirect path or hidden)

---

## UI Connective — How UI talks to the backend

These define the **bridges** between the frontend and the API surface.

### Binding

A named connection between a UI hook and a specific API endpoint. Bindings make the UI-to-backend data flow explicit — which hook calls which endpoint, with what parameters, using what cache key. They are the connective tissue between the UI data layer and the backend interface.

> _Examples:_ `usePlayers() → GET /players`, `useCreatePlayer() → POST /players`, `useSettlementPreview() → GET /settlements/preview`

_When to use:_ Every hook that calls an API endpoint has a binding. Document the endpoint, HTTP method, query parameters, and cache key.

**Documented in:** `UI-SPEC.md` → Data Flow tables
**Template:** templates/ui-spec.md

**Typical structure:**

- Hook name → `METHOD /path`
- Cache key
- Trigger condition (page mount, user action)
- Invalidation targets

### Adapter

A data shape transformation at the UI boundary. Adapters convert API response shapes into view model shapes and form input shapes into API request bodies. They are the UI equivalent of backend mappings — pure functions that reshape data without side effects.

> _Examples:_ API player response → PlayerOverview (add computed display fields), Form values → CreatePlayerRequest (coerce types)

_When to use:_ If the API response shape doesn't match what the component needs, or the form values don't match the API request body, document the adapter transformation.

**Documented in:** `UI-SPEC.md` → Data Flow or Form Contracts (implicit in hook return types)
**Template:** templates/ui-spec.md

**Typical structure:**

- Source shape → Target shape
- Transformation rules
- Computed/formatted fields

---

## UI Presentational — How state looks

### State Indicator

A visual encoding of a domain state value using color, icon, badge, or label. State indicators are the UI projection of backend enums and state machines — they translate abstract status values into visual affordances that users can scan at a glance.

> _Examples:_ PlayerStatusBadge (OBSERVATION=blue, ACTIVE=green, INACTIVE=gray), EligibilityBadge (eligible=green, not eligible=red), StatsStatusBadge (RECORDED=green, CORRECTED=yellow)

_When to use:_ If a domain enum or state machine value needs a visual encoding (color, icon, badge), it's a state indicator. Document the value-to-visual mapping.

**Documented in:** `UI-SPEC.md` → State-to-UI Mapping
**Template:** templates/ui-spec.md

**Typical structure:**

- Domain value → color / icon / badge variant mapping table
- Source domain concept reference (Enum or State Machine)

---

## Quick Reference: Choosing the Right Meta-Type

### Backend

| If you're describing...               | It's a...     | Document in...         |
| ------------------------------------- | ------------- | ---------------------- |
| A thing with an ID and history        | Entity        | domain.md              |
| A thing defined by its values, no ID  | Value Object  | domain.md or shared/   |
| A fixed set of options                | Enum / Type   | domain.md              |
| An action that changes something      | Operation     | operations.md          |
| A read that returns data              | Query         | queries.md             |
| A formula that computes a value       | Calculation   | operations.md          |
| A condition that blocks an action     | Rule          | operations.md (inline) |
| A strategy that chooses behavior      | Policy        | workflows.md           |
| Multiple steps coordinated in one feature | Workflow  | workflows.md           |
| Cross-feature transactional coordination | Saga       | workflows.md           |
| A boundary where data crosses         | Interface     | interfaces.md          |
| A signal that something happened      | Event         | events.md              |
| A shape conversion between boundaries | Mapping       | mappings.md            |
| How something moves through states    | State Machine | states.md              |

### UI

| If you're describing...                         | It's a...       | Document in...                   |
| ----------------------------------------------- | --------------- | -------------------------------- |
| A URL the user can navigate to                  | Page            | UI-SPEC.md → Route Table         |
| A shared page shell (sidebar, header)           | Layout          | UI-SPEC.md → Route Table         |
| A reusable visual building block                | Component       | UI-SPEC.md → Component Inventory |
| Shaped data optimized for display               | View Model      | UI-SPEC.md → Data Flow           |
| Reactive data/state logic for a component       | Hook            | UI-SPEC.md → Data Flow           |
| Schema-validated user input                     | Form            | UI-SPEC.md → Form Contracts      |
| A button/submit that changes state or navigates | Action          | UI-SPEC.md → Data Flow           |
| Client-side auth/permission check               | Guard           | UI-SPEC.md → Route Table         |
| A hook-to-API-endpoint connection               | Binding         | UI-SPEC.md → Data Flow           |
| Data reshaping at API/component boundary        | Adapter         | UI-SPEC.md → Data Flow           |
| Color/badge/icon encoding of domain state       | State Indicator | UI-SPEC.md → State-to-UI Mapping |

## Common Confusion

### Backend

| Concept A   | vs. | Concept B    | How to tell apart                                                                     |
| ----------- | --- | ------------ | ------------------------------------------------------------------------------------- |
| Rule        | vs. | Policy       | Rules **block** (yes/no). Policies **choose** (which strategy).                       |
| Entity      | vs. | Value Object | Entities have **IDs**. Value objects are equal by **fields**.                         |
| Operation   | vs. | Workflow     | Operations are **single actions**. Workflows **orchestrate multiple** operations.     |
| Workflow    | vs. | Saga         | Workflows coordinate **within one feature**. Sagas coordinate **across features/contexts**. |
| Event       | vs. | Operation    | Operations **cause** change. Events **announce** that change happened.                |
| Calculation | vs. | Rule         | Calculations **produce values**. Rules **check conditions**.                          |
| Interface   | vs. | Mapping      | Interfaces define the **boundary**. Mappings define the **transformation** across it. |
| Query       | vs. | Operation    | Queries are **read-only**. Operations **change state**.                               |

### UI

| Concept A       | vs. | Concept B    | How to tell apart                                                                         |
| --------------- | --- | ------------ | ----------------------------------------------------------------------------------------- |
| Page            | vs. | Layout       | Pages have **routes**. Layouts are **shells** that wrap pages.                            |
| Component       | vs. | Page         | Components are **embedded**. Pages own a **URL**.                                         |
| Hook            | vs. | Binding      | Hooks are the **consumer API**. Bindings are the **hook↔endpoint** connection.            |
| Form            | vs. | Component    | Forms are components with **schema-validated input**. Not all components are forms.       |
| View Model      | vs. | Value Object | View models are **display-shaped** (UI). Value objects are **domain-shaped** (backend).   |
| Adapter         | vs. | Mapping      | Adapters transform at the **UI boundary**. Mappings transform at the **API boundary**.    |
| Guard           | vs. | Rule         | Guards are **client-side** access gates. Rules are **server-side** operation constraints. |
| Action          | vs. | Hook         | Actions are **event triggers** (click → mutate). Hooks **encapsulate** the data logic.    |
| State Indicator | vs. | Enum         | State indicators are **visual encodings**. Enums are **abstract value sets**.             |

---

## Architecture Mapping Appendix (Functional Style)

This appendix maps each meta-concept to an implementation pattern in a clean, layered architecture using only functions and types.

### Backend Layer Mapping

| Meta-Concept  | Primary Layer           | Functional Implementation Pattern                              |
| ------------- | ----------------------- | -------------------------------------------------------------- |
| Entity        | Domain                  | `type` + factory function + exported transition functions      |
| Value Object  | Domain                  | immutable `type` + exported constructor/factory + pure helpers |
| Enum / Type   | Domain                  | enum or union type                                             |
| Operation     | Application             | use-case factory `makeX(deps) -> (input) => Promise<output>`   |
| Query         | Application             | query factory `makeX(deps) -> (input) => Promise<view>`        |
| Calculation   | Domain                  | pure deterministic function                                    |
| Rule          | Domain                  | pure predicate function (`boolean`)                            |
| Policy        | Domain                  | strategy selection function                                    |
| Workflow      | Application             | intra-feature orchestrator function with compensation stack    |
| Saga          | Application             | cross-feature orchestration function with compensation policy  |
| Interface     | Interface / Adapters    | boundary handlers (HTTP/RPC/module) that call use-cases        |
| Event         | Domain + Infrastructure | event payload type in domain + publisher adapter in infra      |
| Mapping       | Infrastructure          | pure shape transformation functions                            |
| State Machine | Domain                  | transition table/map + guard checks + pure transition function |

### UI Layer Mapping

| Meta-Concept    | Primary Layer      | Implementation Pattern                                              |
| --------------- | ------------------ | ------------------------------------------------------------------- |
| Page            | Pages (routes)     | Astro `.astro` file importing layout + React island                 |
| Layout          | Layouts            | Astro layout component with `<slot />` for content                  |
| Component       | Components         | React function component with typed props interface                 |
| View Model      | Hooks / Components | TypeScript `type` (exported from hook or co-located with component) |
| Hook            | Hooks              | `use{Name}()` custom React hook wrapping TanStack Query             |
| Form            | Components         | Zod schema + `useForm()` resolver + field render                    |
| Action          | Components         | Event handler calling mutation hook or `navigate()`                 |
| Guard           | Components / Pages | Auth context check → redirect or `null` render                      |
| Binding         | Hooks              | TanStack `useQuery()` / `useMutation()` call configuration          |
| Adapter         | Hooks / Lib        | Pure function transforming API shape to view model shape            |
| State Indicator | Components         | Badge/icon with `switch` / `Record<Value, VisualConfig>` color map  |

### Layer Dependency Rule

- Domain depends on nothing external.
- Application depends on domain only.
- Infrastructure depends on domain/application contracts.
- Interface depends on application only.

### Encapsulation Rule

- Public API = exported functions and types only.
- Private implementation = unexported file-local helpers.
