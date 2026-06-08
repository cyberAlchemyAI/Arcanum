# Iteration And Stop

Iterate until a fixture-only result summary is generated from validated JSONL,
or until a local evidence blocker prevents safe completion.

Stop with `BLOCK` if:

- no validated fixture JSONL is available;
- summary generation cannot be verified locally;
- required writes would exceed the declared scope;
- completing the task would require live experiments.
