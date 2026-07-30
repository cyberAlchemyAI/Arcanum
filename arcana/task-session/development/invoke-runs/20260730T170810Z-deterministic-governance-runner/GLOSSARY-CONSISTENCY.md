# Glossary Consistency Review

Result: `PASS`

- `governance evaluator` is the pure policy component; `governance runner` is the
  phase controller. The terms are not interchangeable.
- `execution ticket` authorizes one attempt but is not an implementation command or
  lifecycle approval.
- `owner hook` retains its capability owner; “hook” does not mean Task Session owns
  the invoked semantics.
- `continuity cursor` points to a next route but never executes it.
- `output-only re-admission` does not reopen implementation mutation.
- Existing Task Session terms `SWU`, `closeout preflight`, `mutation admission`, and
  `terminal receipt` retain their canonical meanings.

