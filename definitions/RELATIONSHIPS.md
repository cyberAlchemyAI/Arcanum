# Relationship Types

> **Example / explanatory layer.** This is the human-facing catalog of the DomainSpec edge vocabulary with signatures and examples. The **canonical, normative** definition is [`DEFINITIONS.md#ds-d2-typed-relationship-system`](DEFINITIONS.md#ds-d2-typed-relationship-system) (DS-D2), with edge-family/signature rules in DS-D7/DS-D8. Where wording differs, DS-D2 is authoritative.

> The 29 typed edges that connect domain concepts into a navigable knowledge graph — 15 backend, 8 intra-UI, and 6 cross-layer.

## Overview

Every concept in the system connects to other concepts through typed relationships. These edges make the knowledge graph navigable — from any concept, you can follow edges to understand what it touches.

### Backend Edges (15)

| Edge           | From → To                   | Description                                         |
| -------------- | --------------------------- | --------------------------------------------------- |
| `performs`     | Entity → Operation          | An entity initiates or is the actor of an operation |
| `produces`     | Operation → Event           | An operation emits an event upon completion         |
| `produces-for` | Operation@A → Entity@B      | An operation in A mutates or projects data into an entity owned by B |
| `triggers-cross` | Event@A → Operation@B    | An event in A triggers an operation owned by B      |
| `enforces-cross` | Rule@A → Operation@B     | A rule in A constrains whether B can execute an operation |
| `enforces`     | Rule → Operation            | A rule constrains when an operation can execute     |
| `calculates`   | Calculation → Operation     | A calculation derives values used by an operation   |
| `transitions`  | Event → State Machine       | An event triggers a state transition                |
| `exposes`      | Interface → Operation/Query | An interface makes an operation or query accessible |
| `orchestrates` | Workflow → Operation[]      | A workflow coordinates multiple operations          |
| `applies`      | Policy → Operation          | A policy governs how an operation behaves           |
| `maps`         | Mapping → Entity/Interface  | A mapping transforms data between shapes            |
| `contains`     | Entity → Value Object       | An entity embeds a value object as a field          |
| `queries`      | Query → Entity              | A query reads data from an entity                   |
| `emits`        | Entity → Event              | An entity is the source of a domain event           |

### Intra-UI Edges (8)

| Edge       | From → To               | Description                                        |
| ---------- | ----------------------- | -------------------------------------------------- |
| `renders`  | Page → Component[]      | A page renders components as interactive islands   |
| `wraps`    | Layout → Page[]         | A layout wraps pages providing the visual shell    |
| `composes` | Component → Component[] | A component includes child components              |
| `consumes` | Component → Hook        | A component consumes a hook for data/state         |
| `submits`  | Form → Action           | A form validates input then delegates to an action |
| `shapes`   | Adapter → View Model    | An adapter transforms API data into a view model   |
| `protects` | Guard → Page            | A guard controls access to a page                  |
| `displays` | Component → View Model  | A component renders data from a view model         |

### Cross-Layer Edges: UI ↔ Backend (6)

| Edge        | From → To                       | Description                                       |
| ----------- | ------------------------------- | ------------------------------------------------- |
| `fetches`   | Binding → Query                 | A binding fetches data from a backend query       |
| `mutates`   | Binding → Operation             | A binding invokes a backend operation             |
| `reflects`  | State Indicator → State Machine | A UI indicator mirrors a domain lifecycle state   |
| `derives`   | View Model → Entity             | A view model is derived from entity fields        |
| `contracts` | Form → Interface                | A form schema aligns with an interface endpoint   |
| `mirrors`   | Guard → Rule                    | A client-side guard mirrors a backend access rule |

---

## Edge Details

### `performs` — Entity → Operation

An entity (or its associated actor) initiates a business action.

> User **performs** CreateOrder
> Admin **performs** ApproveRefund

_In the registry:_ Shows which actors trigger which operations. Follow this edge to answer "What can a {User/Admin/System} do?"

### `produces` — Operation → Event

When an operation completes successfully, it emits one or more domain events.

> ProcessPayment **produces** PaymentInitiated
> CreateOrder **produces** OrderCreated

_In the registry:_ Traces cause → effect. Follow this edge to answer "What happens after {Operation} runs?"

### `produces-for` — Operation@A → Entity@B

An operation in one feature or bounded context writes or projects data into an entity owned by another feature or bounded context.

> GenerateSettlement **produces-for** Player (bankroll/makeup updates)
> Routing.ComputeItinerary **produces-for** Booking.Cargo

_In the registry:_ Captures cross-feature write-back and projection flows. Follow this edge to answer "Which foreign entity does {Operation} update?"

### `triggers-cross` — Event@A → Operation@B

An event produced in one feature or bounded context triggers an operation in another.

> OnboardingCompleted **triggers-cross** CreatePlayer
> PaymentCompleted **triggers-cross** ScheduleShipment

_In the registry:_ Captures event-driven cross-feature activation. Follow this edge to answer "Which operation is activated by {Event} outside the source feature?"

### `enforces-cross` — Rule@A → Operation@B

A rule defined in one feature or bounded context constrains operation execution in another.

> KYCVerificationRule **enforces-cross** OpenAccount
> PermissionRule **enforces-cross** AssignCoach

_In the registry:_ Captures cross-feature governance dependencies. Follow this edge to answer "Which external rule gates {Operation}?"

### `enforces` — Rule → Operation

A rule constrains an operation — the operation cannot proceed unless the rule is satisfied.

> MaxAmountRule **enforces** ProcessPayment
> StockAvailabilityRule **enforces** CreateOrder

_In the registry:_ Shows all constraints on an operation. Follow this edge to answer "What conditions must hold for {Operation} to execute?"

### `calculates` — Calculation → Operation

A calculation produces derived values that an operation consumes.

> FeeCalculation **calculates** for ProcessPayment
> TaxCalculation **calculates** for CreateOrder

_In the registry:_ Links pure computation to the operations that use it. Follow this edge to answer "What values does {Operation} compute?"

### `transitions` — Event → State Machine

An event causes a state machine to move from one state to another.

> PaymentCompleted **transitions** PaymentStatus (Processing → Completed)
> OrderShipped **transitions** OrderLifecycle (Confirmed → Shipped)

_In the registry:_ Connects events to lifecycle changes. Follow this edge to answer "What state change does {Event} cause?"

### `exposes` — Interface → Operation/Query

An interface makes a domain operation or query available to external or internal consumers.

> PaymentAPI **exposes** ProcessPayment
> PaymentModule **exposes** GetPaymentStatus

_In the registry:_ Maps API surface to domain logic. Follow this edge to answer "How do I call {Operation} from outside?"

### `orchestrates` — Workflow → Operation[]

A workflow coordinates multiple operations into a multi-step process.

> OrderFulfillment **orchestrates** [ChargePayment, ReserveInventory, ShipOrder, NotifyCustomer]

_In the registry:_ Shows process composition. Follow this edge to answer "What steps are in {Workflow}?"

### `applies` — Policy → Operation

A policy governs how an operation selects its behavior — choosing between strategies at runtime.

> RetryPolicy **applies** to RetryPayment
> PricingPolicy **applies** to CalculateDiscount

_In the registry:_ Shows which strategies control which behaviors. Follow this edge to answer "What decides how {Operation} behaves?"

### `maps` — Mapping → Entity/Interface

A mapping transforms data between an entity and an interface (or between two entities).

> RequestToTransaction **maps** APIRequest → PaymentTransaction
> TransactionToResponse **maps** PaymentTransaction → APIResponse

_In the registry:_ Shows data transformations at boundaries. Follow this edge to answer "How does {Entity} data change shape at {Interface}?"

### `contains` — Entity → Value Object

An entity embeds a value object as one of its fields.

> Order **contains** Money (as totalAmount)
> PaymentTransaction **contains** Money (as amount, fee, totalCharged)

_In the registry:_ Shows composition. Follow this edge to answer "What value objects are inside {Entity}?"

### `queries` — Query → Entity

A query reads data from one or more entities without modifying them.

> GetPaymentHistory **queries** PaymentTransaction
> GetOrderDetails **queries** Order

_In the registry:_ Shows read dependencies. Follow this edge to answer "Where does {Query} get its data from?"

### `emits` — Entity → Event

An entity is the source of a domain event — the event announces a change to that entity.

> PaymentTransaction **emits** PaymentCompleted
> Order **emits** OrderShipped

_In the registry:_ Shows which entities produce which signals. Follow this edge to answer "What events does {Entity} announce?"

---

## Intra-UI Edge Details

### `renders` — Page → Component[]

A page renders one or more components as its content. Pages are the routing layer; components are the interactive units within them.

> /players **renders** [PlayersTable]
> /settlements **renders** [SettlementPage → SettlementForm, SettlementPreviewCard, SettlementResultCard]

_In the registry:_ Shows what a user sees on each URL. Follow this edge to answer "What components appear on {Page}?"

### `wraps` — Layout → Page[]

A layout wraps multiple pages with consistent chrome (sidebar, header, navigation).

> DashboardLayout **wraps** [/players, /coaches, /settlements]
> AuthLayout **wraps** [/login, /onboarding]

_In the registry:_ Shows structural grouping. Follow this edge to answer "What pages share {Layout}?"

### `composes` — Component → Component[]

A component includes child components to build complex UI.

> PlayerStatsPage **composes** [StatsWindowCard, StatsHistoryTable]
> SettlementPage **composes** [SettlementPreviewCard, SettlementResultCard]

_In the registry:_ Shows component hierarchy. Follow this edge to answer "What building blocks make up {Component}?"

### `consumes` — Component → Hook

A component consumes a hook to access reactive data or mutation functions.

> PlayersTable **consumes** usePlayers()
> RecordStatsForm **consumes** useRecordStats()

_In the registry:_ Shows data dependencies. Follow this edge to answer "Where does {Component} get its data?"

### `submits` — Form → Action

A form validates input and delegates to an action (mutation hook call or navigation).

> CreatePlayerForm **submits** useCreatePlayer() → POST /players
> LoginForm **submits** login() → POST /auth/login

_In the registry:_ Traces user input to side effects. Follow this edge to answer "What happens when {Form} is submitted?"

### `shapes` — Adapter → View Model

An adapter transforms raw API response data into a view model shaped for rendering.

> PlayerAdapter **shapes** PlayerOverview (flatten entity + computed stats)
> StatsAdapter **shapes** StatsWindow (aggregate period data)

_In the registry:_ Shows data transformations in the UI layer. Follow this edge to answer "How was {View Model} produced?"

### `protects` — Guard → Page

A guard controls whether a user can access a page.

> AuthGuard **protects** /players, /coaches, /settlements
> PublicGuard **protects** /login (redirect away if already authenticated)

_In the registry:_ Shows access control surface. Follow this edge to answer "Who can access {Page}?"

### `displays` — Component → View Model

A component renders data from a view model.

> PlayersOverviewTable **displays** PlayerOverview[]
> SettlementPreviewCard **displays** SettlementPreview

_In the registry:_ Shows rendering dependencies. Follow this edge to answer "What data does {Component} show?"

---

## Cross-Layer Edge Details

### `fetches` — Binding → Query

A UI binding fetches data from a backend query via an API endpoint.

> usePlayers() **fetches** GetAllPlayers (via GET /players)
> useStatsWindow(id) **fetches** GetStatsWindow (via GET /players/:id/stats/window)

_In the registry:_ Traces UI data to its backend source. Follow this edge to answer "Where does the data displayed by {Hook} come from in the domain?"

### `mutates` — Binding → Operation

A UI binding invokes a backend operation via an API endpoint.

> useCreatePlayer() **mutates** CreatePlayer (via POST /players)
> useGenerateSettlement() **mutates** GenerateSettlement (via POST /settlements)

_In the registry:_ Traces UI actions to backend state changes. Follow this edge to answer "What domain operation does {Hook} trigger?"

### `reflects` — State Indicator → State Machine

A UI state indicator visually mirrors a backend state machine value.

> PlayerStatusBadge **reflects** PlayerStatus (OBSERVATION=blue, ACTIVE=green, INACTIVE=gray)
> EligibilityBadge **reflects** ProgressionEligibility (eligible=green, not-eligible=red)

_In the registry:_ Ensures UI stays in sync with domain lifecycle. Follow this edge to answer "What domain state does {Badge} visualize?"

### `derives` — View Model → Entity

A view model is derived from one or more backend entities, reshaped for rendering.

> PlayerOverview **derives** from Player (flatten + add computed stats)
> SettlementPreview **derives** from Settlement + Player + MakeupPolicy

_In the registry:_ Shows data lineage from domain to screen. Follow this edge to answer "What entities feed into {View Model}?"

### `contracts` — Form → Interface

A form's Zod schema is the client-side contract for a backend interface endpoint. Changes to the interface must be reflected in the form schema.

> CreatePlayerForm **contracts** POST /players (PlayerAPI.createPlayer)
> SettlementForm **contracts** GET /settlements/preview + POST /settlements

_In the registry:_ Shows schema alignment obligations. Follow this edge to answer "Which form breaks if {Interface} endpoint changes?"

### `mirrors` — Guard → Rule

A client-side guard replicates a backend access rule for UX purposes (the server still enforces authoritatively).

> AuthGuard **mirrors** AuthenticatedUserRule (token required)
> AdminGuard **mirrors** AdminRoleRule (role === 'admin')

_In the registry:_ Shows where frontend and backend access logic must stay in sync. Follow this edge to answer "What server rule does {Guard} duplicate?"

---

## Navigating the Graph

The edges form navigation paths that mirror how humans think about a system:

### Backend Navigation

**"What does this feature do?"**
→ Start at Entity → follow `performs` → find Operations → follow `produces` → see Events

**"What happens when a payment is processed?"**
→ ProcessPayment → `enforces` (see Rules) → `calculates` (see Calculations) → `produces` PaymentInitiated → `transitions` PaymentStatus

**"What consumes this event?"**
→ PaymentCompleted → look at event consumers → follow to downstream features

**"How do I call this operation?"**
→ ProcessPayment → follow `exposes` backward → find PaymentAPI → see endpoint details

**"What data does this API return?"**
→ GET /payments → `exposes` GetPaymentStatus → `queries` PaymentTransaction → `maps` TransactionToResponse

### UI Navigation

**"What does this page show?"**
→ Start at Page → follow `renders` → find Components → follow `consumes` → find Hooks → follow `fetches` → arrive at backend Query

**"What happens when the user submits this form?"**
→ CreatePlayerForm → `submits` useCreatePlayer() → `mutates` CreatePlayer (Operation) → `produces` PlayerCreated (Event) → `transitions` PlayerStatus

**"Where does the data on this table come from?"**
→ PlayersTable → `consumes` usePlayers() → `fetches` GetAllPlayers (Query) → `queries` Player (Entity)

**"What breaks if I change this API endpoint?"**
→ Interface endpoint → follow `contracts` backward → find Forms with aligned schemas
→ Interface endpoint → follow `fetches` backward → find Hooks with bindings

**"How does domain state appear on screen?"**
→ PlayerStatus (State Machine) → follow `reflects` backward → find PlayerStatusBadge (State Indicator) → see color mapping

### Full-Stack Trace (End to End)

**"Trace a user creating a player from click to database"**

```
/players/new (Page)
  → renders CreatePlayerForm (Component / Form)
    → submits useCreatePlayer() (Hook / Binding)
      → mutates CreatePlayer (Operation) via POST /players (Interface)
        → enforces [NameRequiredRule, EmailUniqueRule] (Rules)
        → produces PlayerCreated (Event)
          → transitions PlayerStatus: → OBSERVATION (State Machine)
```

**"Trace settlement data from database to screen"**

```
Player + MakeupPolicy + Stats (Entities)
  → queries GetSettlementPreview (Query)
    → exposes GET /settlements/preview (Interface)
      → fetches useSettlementPreview() (Hook / Binding)
        → shapes SettlementPreview (Adapter → View Model)
          → displays SettlementPreviewCard (Component)
            → renders /settlements (Page)
```

---

## Registry Format

In `registry.md`, the concept graph lists all edges as a flat table:

```markdown
## Concept Graph

| From                       | Edge     | To                       |
| -------------------------- | -------- | ------------------------ |
| payment.PaymentTransaction | contains | shared.Money             |
| payment.ProcessPayment     | produces | payment.PaymentInitiated |
| payment.MaxAmountRule      | enforces | payment.ProcessPayment   |
| payment.PaymentAPI         | exposes  | payment.ProcessPayment   |
```

### UI Concept Graph (same table, ui-prefixed IDs)

```markdown
| From                                   | Edge      | To                                |
| -------------------------------------- | --------- | --------------------------------- |
| ui.player-management./players          | renders   | ui.player-management.PlayersTable |
| ui.player-management.PlayersTable      | consumes  | ui.player-management.usePlayers   |
| ui.player-management.usePlayers        | fetches   | player-management.GetAllPlayers   |
| ui.player-management.CreatePlayerForm  | contracts | player-management.PlayerAPI       |
| ui.player-management.PlayerStatusBadge | reflects  | player-management.PlayerStatus    |
| ui.DashboardLayout                     | wraps     | ui.player-management./players     |
```

Backend concepts use `{feature}.{Concept}` IDs. UI concepts use `ui.{feature}.{Concept}` IDs. Shared UI concepts (layouts, guards) use `ui.{Concept}` without a feature prefix.
