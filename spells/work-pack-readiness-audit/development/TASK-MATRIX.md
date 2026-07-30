# Task Matrix — Work Pack Readiness Audit

| ID | Fixture | Expected |
| --- | --- | --- |
| WPA-F01 | exact read-only frontier | overall pass, one ready root, no selection |
| WPA-F02 | material plus output-only routed units | plan pass, runtime block by task class/admission |
| WPA-F03 | cyclic graph | graph block |
| WPA-F04 | traversal plus write-union mismatch | path and write-algebra blocks |
| WPA-F05 | incomplete attempt lifecycle | attempt block |
| WPA-F06 | fail-open receipt schema | receipt-semantics block |
| WPA-F07 | start/end snapshot mismatch | snapshot-drift block |
| WPA-F08 | refresh authority escalation | schema rejection |
| WPA-F09 | handoff route contradicts work-pack selection state | handoff block |

Required future additions before claiming coverage of an execution-specific
runtime are project-local fixtures for dependency receipt semantics, runtime
binary hashes, port/process teardown, and attempt collision against that
runtime's actual artifacts.

## Additive v2 projection

| ID | Fixture | Expected |
| --- | --- | --- |
| WPA2-F01 | stable exact-input projection regenerated under a new audit ID | identical projection digest; epoch preserved |
| WPA2-F02..11 | one missing package, owner, receipt, schema, inventory, baseline, delta, closeout, successor, or material digest | stable pre-route blocker code; no manifest |
| WPA2-F12..16 | owner, material, validation, receipt, or closeout semantic change | exact epoch-invalidation code |

The configured `false` command is intentionally never executed. The public
suite validates contracts and projection behavior; consuming projects own
empirical command and immediately-before-write drift fixtures.
