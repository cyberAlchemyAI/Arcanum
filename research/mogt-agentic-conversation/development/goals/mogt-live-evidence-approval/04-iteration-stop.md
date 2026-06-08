# Iteration And Stop

Iterate until one of these verdicts is proven:

- `approve-ready`: E1/E2/E4 gates are closed, calibration examples exist,
  live-run parameters are explicit, and evidence mutation policy is gated.
- `repair-needed`: approval cannot proceed because local protocol/rubric/run
  requirements are missing but repair is local.
- `research-gap`: bounded external prior-art/source normalization is required
  before approval.
- `block`: approval cannot be decided from local evidence or would require live
  execution.

Stop with `BLOCK` if:

- deciding approval would require live experiments;
- write scope must expand beyond the declared files;
- evidence status or paper result sections would need to change;
- E3 first-wave inclusion is required but lacks explicit approval evidence.
