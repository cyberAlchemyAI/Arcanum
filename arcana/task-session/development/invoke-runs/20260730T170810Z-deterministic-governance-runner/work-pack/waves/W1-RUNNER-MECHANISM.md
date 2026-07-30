# W1: Runner Mechanism

Layer question: can one exact run advance and resume safely?

Order: TSGR-003 -> TSGR-004 -> TSGR-005 -> TSGR-006.

Shared-path overlap forbids parallel mutation. Exit requires deterministic prepare,
structured executor join, complete read-only reconciliation, atomic idempotent
commit, and crash/restart evidence.

Progress:

- TSGR-003: completed with passing deterministic prepare and read-only status evidence;
- TSGR-004: selected as the unique dependency-ready successor.
