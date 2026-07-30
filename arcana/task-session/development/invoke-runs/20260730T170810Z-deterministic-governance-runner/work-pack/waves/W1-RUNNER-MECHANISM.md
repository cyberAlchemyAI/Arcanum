# W1: Runner Mechanism

Layer question: can one exact run advance and resume safely?

Order: TSGR-003 -> TSGR-004 -> TSGR-005 -> TSGR-006.

Shared-path overlap forbids parallel mutation. Exit requires deterministic prepare,
structured executor join, complete read-only reconciliation, atomic idempotent
commit, and crash/restart evidence.

Progress:

- TSGR-003: completed with passing deterministic prepare and read-only status evidence;
- TSGR-004: completed with passing structured launch/join, idempotent replay, and
  failure-class separation evidence;
- TSGR-005: completed with passing read-only target classification, validation,
  output-only re-admission, and evidence-drift evidence;
- TSGR-006: completed with passing journaled commit/resume, exact-present no-op,
  terminal transaction receipt ordering, interruption recovery, partial-state
  rejection, and contradictory-replay evidence;
- W1 exit: satisfied; the unique dependency-ready successor is TSGR-007 in L2.
