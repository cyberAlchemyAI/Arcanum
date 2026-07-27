# Expected Output: strategy-handoff-gap-complex

## Subagent Strategy Result

- Mode: run
- Runtime profile: fixture-graph-profile
- Dispatch type / owner: configured type / live owner
- Trigger decision: dispatch
- Trigger evidence: synthesis, isolation, and parallelism
- Preflight: pass; source requirements shaped the producer handoff contract
- Confirmation readiness: pass on the frozen sheet digest
- Groups / lanes: producer completed provisionally; consumer remains blocked
- Subagents: producer feedback is reopened; consumer and auditor have not started
- Dependency flow: sequential producer-to-consumer edge; declared feedback to producer; reserved consumer-to-auditor revision
- Tension gate: PASS/PASS
- Human gate: confirmed/frozen
- Registration: registered with evidence
- Execution: partial
- Stage handoffs: needs_feedback with two typed selector gaps; repair owner producer; declared feedback edge; one loop remaining
- Agent closeout: producer feedback open; consumer and auditor not launched
- Ledger closeout: pending
- Result artifacts: producer artifact preserved with typed gap report
- Validation: artifact existence did not satisfy type-owner readiness; no undeclared edge or loop was used
- Reflection trigger: gap-threshold
- Next human action: inspect only if producer feedback exhausts its declared loop
