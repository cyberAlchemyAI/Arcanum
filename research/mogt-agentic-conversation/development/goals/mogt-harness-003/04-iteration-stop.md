# Iteration And Stop

Iterate until frontier/dominance metrics are computed or an explicit local
deferral is justified.

Stop with `BLOCK` if:

- objective-vector shape cannot be inferred from local evidence;
- fixture data is insufficient and cannot be created inside scope;
- calculator output cannot be verified locally;
- completing the task would require live experiments.
