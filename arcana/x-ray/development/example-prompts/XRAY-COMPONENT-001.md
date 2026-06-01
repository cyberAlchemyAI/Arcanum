# Experiment Prompt: XRAY-COMPONENT-001

Use `x-ray` in `object` mode.

Target context:

```text
Component: Payment Retry Policy

The Payment Retry Policy decides whether a failed card payment should be retried.
It receives a payment failure reason, retry count, customer account status, and merchant retry settings.
It returns one of: retry now, retry later, stop retries, or escalate for review.
It depends internally on failure classification, retry-window calculation, and merchant policy lookup.
It depends externally on the payment processor reason codes, merchant configuration, and customer account status.
Repeated hard declines should stop retries. Temporary network errors may retry later. The maximum retry count is merchant-configurable.
```

Expected evidence:

- mode: `object`
- lanes for properties, components, internal dependencies, external dependencies, lifecycle, and risk questions
- visible source-backed vs inferred boundary
- YAML visual library components selected when relevant
- HTML output shape or planned L0 HTML/SVG output
