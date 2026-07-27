# Task Matrix

| ID | Complexity | Scenario | Expected Output | Status |
| --- | --- | --- | --- | --- |
| spell-low | low | Small focused request. | Contract-shaped result. | pass — profile fixture |
| spell-medium | medium | Multi-part realistic request. | Contract-shaped result with gates. | pass — profile fixture |
| spell-complex | complex | Cross-boundary or lifecycle request. | Contract-shaped result with risks and next steps. | pass — profile fixture |

The deterministic controller fixture additionally passes eight chain cases:
linear completion, later blocker, closeout failure, repeated cursor, cross-scope
successor, successor outside the captured frontier, ambiguous successor, and
validated no-op closeout.
