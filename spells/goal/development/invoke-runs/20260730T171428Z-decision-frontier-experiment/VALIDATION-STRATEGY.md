# Validation Strategy

## Validation Levels

| Level | Surface | Proof |
| --- | --- | --- |
| V0 | schemas and graph | positive fixtures pass; cycle, unknown endpoint, duplicate ID, invalid transition fail |
| V1 | pure reducer | exact eligible IDs and stable exclusion reasons |
| V2 | state controls | stale/competing claims and invalid resolutions fail without writes |
| V3 | boundaries | HITL stops; Way Clear is strict; task/SWU state is unchanged |
| V4 | reproducibility | two clean repeated runs are byte-identical |
| V5 | authority | closure reviewer proves bounded canonical source hashes and scoped diff are unchanged |
| V6 | closure | independent reviewer reconciles all witnesses and owner receipts |

## Core Commands

Planned commands use the future development root:

```bash
python3 spells/goal/development/decision-frontier-experiment/scripts/validate_contracts.py
python3 spells/goal/development/decision-frontier-experiment/scripts/run_frontier_fixtures.py
python3 spells/goal/development/decision-frontier-experiment/scripts/run_claim_fixtures.py
python3 spells/goal/development/decision-frontier-experiment/scripts/run_reconciliation_fixtures.py
python3 spells/goal/development/decision-frontier-experiment/scripts/run_hitl_fixture.py
python3 spells/goal/development/decision-frontier-experiment/scripts/run_way_clear_fixtures.py
python3 spells/goal/development/decision-frontier-experiment/scripts/run_noncollapse_fixture.py
```

These commands are contracts, not observed results.

## Claim Matrix

| Claim | Required evidence | Ceiling |
| --- | --- | --- |
| reducer is deterministic | DFE-FIX-009 receipt | synthetic inputs only |
| claim semantics fail closed | DFE-FIX-002 and DFE-FIX-004 | single-process simulator |
| control boundaries are preserved | DFE-FIX-008, DFE-FIX-011, DFE-FIX-012 | synthetic fixtures only |
| canonical authority inputs are unchanged | DFE-FIX-010 | exact bounded source hashes |
| decision map improves capability | paired real workflow experiment | not covered by this work pack |
| canonical adoption is safe | new Invoke Design plus Spellcraft lifecycle evidence | not covered |

## Failure Policy

Any unexpected output from a negative mutant, undeclared file delta, private
content, stale digest acceptance, or decision/execution collapse blocks its SWU.
Tests never silently rewrite expected fixtures.
