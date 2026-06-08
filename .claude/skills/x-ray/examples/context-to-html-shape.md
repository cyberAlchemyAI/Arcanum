# Example: Context To HTML Shape

## Input

```text
We have an order ingestion process. A merchant uploads a CSV. The validator checks required fields, normalizes currency, and sends accepted rows to the pricing queue. Rejected rows are written to an error report. Support reviews recurring rejection causes weekly.
```

## Expected x-ray Result Shape

```markdown
## x-ray Result

- Status: pass
- Context type: process
- User intent: understand the order ingestion process
- Output: planned HTML explanation page
- Explanation model:
  - overview: merchant CSV rows move through validation into pricing or error review.
  - actors: merchant, validator, pricing queue, support.
  - entities: CSV rows, accepted rows, rejected rows, error report.
  - data flow: upload -> validation -> pricing queue or error report.
  - transformations: required-field checks, currency normalization.
  - process steps: upload, validate, normalize, route accepted rows, write rejected rows, review recurring causes.
  - relationships: validator separates valid and invalid rows; support learns from rejection patterns.
  - assumptions: pricing queue accepts normalized rows.
  - open questions: who owns validator rules, and where are error reports stored?
- Visual plan: simple left-to-right flow with a branch after validation.
- Evidence boundary: all named actors and steps come from the supplied context; ownership questions are inferred gaps.
```
