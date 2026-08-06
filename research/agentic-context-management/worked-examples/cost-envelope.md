# Worked Example: Cost Envelope

Source kind: `primary-source` arithmetic, with `operator-reading` guards.

Assume the paper's illustrative values:

```text
t = 500 new tokens per turn
W = 4,000 bounded input tokens per turn
p = 8 turns between compactions
c = 2 bounded-context equivalents per compaction event
```

At `n = 100` turns:

```text
C_append = 500 * 100 * 101 / 2 = 2,525,000 tokens
C_bounded = 100 * 4,000 = 400,000 tokens
append / bounded = 6.3125x

C_managed = 100 * 4,000 * (1 + 2/8)
          = 500,000 tokens
saving vs append = 1 - 500,000 / 2,525,000
                 ~= 80.2%
```

## What This Establishes

Under fixed turn growth and fixed budget, full append is quadratic while bounded
and periodically validated context is linear with a constant-factor overhead.

## What This Does Not Establish

- actual API cost after caching or tiered prices;
- output-token, retrieval, storage, or latency cost;
- that 4,000 tokens are sufficient for the task;
- that the validation step preserves all important information.
