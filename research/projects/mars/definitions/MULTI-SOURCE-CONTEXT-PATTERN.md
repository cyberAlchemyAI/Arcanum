# Multi-Source Context Pattern

Purpose: define how MARS experiments aggregate context from multiple sources while preserving traceability and conflict handling.

Primary use: experiments that require cross-domain, cross-paper, or mixed source evidence (for example E11-E20).

## Inputs

- Experiment protocol: `experiments/<experiment-key>/protocol.md`
- Source selection: `experiments/<experiment-key>/sources.md`
- Source catalog: `sources/SOURCE-CATALOG.md`
- Inventory entries: `inventory/<source-id>.md`

## Required Context Bundle

Each multi-source run must build a context bundle with the following sections:

1. Scope and claim target
2. Source role matrix
3. Normalized terminology map
4. Metric definition map
5. Conflict log and resolution decisions
6. Open risks and follow-up actions

## Source Role Matrix

| Source ID | Entry Type | Role in Experiment | Authority Level | Version Pin |
|---|---|---|---|---|
| <id> | <type> | baseline | primary | <pin> |
| <id> | <type> | comparison | supporting | <pin> |

Authority level values:
- primary: required to evaluate success criteria
- supporting: used for triangulation or background
- fallback: used only if primary source fails quality checks

## Conflict Resolution Policy

Order of precedence when sources disagree:

1. Experiment protocol constraints
2. Version-pinned primary source artifacts
3. Peer-reviewed papers and formal specifications
4. Official tool or framework documentation
5. Secondary commentary and blog sources

Tie-breakers:

- Prefer the newest pinned source when versions differ.
- Prefer directly measured data over narrative claims.
- Mark unresolved conflicts explicitly; do not silently merge.

## Reconciliation Rules

| Conflict Type | Resolution Rule | Output Requirement |
|---|---|---|
| Terminology mismatch | Maintain canonical term plus aliases | Terminology map updated |
| Metric definition mismatch | Use stricter measurable definition | Metric map updated with rationale |
| Structural mismatch | Preserve both structures and annotate applicability | Conflict log entry |
| Contradictory findings | Keep both, assign confidence, schedule follow-up run | Follow-up action list |

## Quality Gates in Multi-Source Mode

- G2 source quality still applies per source.
- G3 inventory readiness must pass for all primary sources.
- G4 integrity must include a consistency check across merged records.

## Output Contract

```
## Multi-Source Context Summary

Experiment: <id>
Sources used: <n>
Primary sources: <list>
Supporting sources: <list>

Conflicts:
- Total conflicts: <n>
- Resolved: <n>
- Unresolved: <n>

Decisions:
1. <decision and rationale>
2. <decision and rationale>

Next actions:
1. <action>
2. <action>
```
