# Resolution Router Validation

Validate behavior with realistic human requests rather than JSON fixtures.

## Behavioral scenarios

| scenario | expected behavior |
|---|---|
| orientation in chat | selects low and answers naturally using shared context |
| standalone introduction | selects low but supplies enough context to stand alone |
| operational comparison | selects medium, applies all three lenses, and executes the medium writer |
| implementation challenge | selects high and reports unavailable until its writer exists |
| explicit high | never selects a lower tier |
| requested low but operational action required | promotes to medium with a human-readable reason |
| uncertain evidence | qualifies claims without forcing a structured packet |
| low lens coverage | applies epistemic and systemic views before writing |
| medium lens coverage | applies epistemic, systemic, and categorical views |
| lens invisibility | uses lens findings without forcing lens-named prose sections |
| direct low invocation with sufficient context | writes directly without a plan or packet |
| direct medium invocation with sufficient context | writes directly from all three required perspectives |
| medium-to-high boundary | redirects implementation-level inspection to high without silently downgrading |
| direct writer invocation with missing context | redirects once to the router |
| manifest drift | reports the exact missing available path without substitution |

## Required checks

1. Run `quick_validate.py` on the router and every available writer.
2. Verify every manifest path agrees with its declared availability.
3. Run strict artifact metadata validation on changed canonical skills and
   sidecars, plus advisory directory validation with a nonzero checked count.
4. Validate selective installation and dependency closure.
5. Run fresh-context conversational and standalone examples at every available
   tier, checking its required lens coverage.
6. Confirm outputs are human-facing, hide internal guarantee IDs, and require no
   JSON intermediates.

Keep high unavailable until its writer passes structural, behavioral, and
human-facing forward tests.
