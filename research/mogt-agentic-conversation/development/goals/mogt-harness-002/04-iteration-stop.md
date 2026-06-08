# Iteration And Stop

Iterate until the four policy-regime fixtures exist and validate, or until a
local evidence blocker prevents safe completion.

Stop with `BLOCK` if:

- `RuntimeDecisionReceipt` cannot be mapped to validator-compatible rows;
- fixture validation cannot be completed from local evidence;
- required writes would exceed the declared scope;
- completing the task would require live experiments.
