# Guide Implementation Layering

## L0: Route Fixture

Question: Can Guide describe the route for `/guide this architecture` without executing subagents?

Deliverables:

- `GUIDE-ROUTE-SCHEMA.yml`
- one static route fixture using User and Translate fixture handles.

## L1: Translate Integration

Question: Can Guide call Translate as a step and preserve returned mapping limits?

Deliverables:

- Guide route fixture with Translate call ref,
- guide receipt with translation receipt ref.

## L2: Dispatch Governance

Question: Can Guide bound research and subagent dispatch?

Deliverables:

- dispatch budget/gate rules,
- research-needed and subagent-needed route fixtures.

## L3: Spellcraft Runtime

Question: Is Guide ready to become a real spell?

Deliverables:

- spellcraft handoff,
- route validation fixtures,
- runtime command candidate.
