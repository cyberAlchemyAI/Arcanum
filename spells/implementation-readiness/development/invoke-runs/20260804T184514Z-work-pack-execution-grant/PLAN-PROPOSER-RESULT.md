# Plan Proposer Result

The proposed route uses eight dependency-ordered SWUs:

1. contract validation;
2. truthful Plan projection;
3. Work-Pack-bound Router admission;
4. outer-loop control;
5. Task Session fast guard;
6. fresh-session resumption;
7. end-to-end causal proof;
8. generated package parity.

This preserves one primary behavior per SWU and places the first irreversible
behavior only after schema, producer, router, and controller evidence exists.

The proposer rejects a Router-only patch because it would not fix contradictory
Plan handoff or late Task Session discovery, and rejects a new authorization
receipt because it would recreate the ceremony being removed.

