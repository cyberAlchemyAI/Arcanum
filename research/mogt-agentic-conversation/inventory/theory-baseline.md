# MOGT Theory Baseline

Purpose: secondary thematic rollup for the first-wave multi-objective and value-tradeoff authorities that ground E1, E2, and E4.

This file is a convenience view, not the content authority.

Current state:

- no theory-source entries are fully raw-backed yet in this pass
- use this file as a planning view until per-source library entries are added

## Operationalized Authorities

### PAPER-DEB-2001

- Canonical citation: Deb. Multi-Objective Optimization Using Evolutionary Algorithms.
- Pin: `book:deb-2001`
- Experiments: E2, E4
- Operational constructs:
  - objective-vector reasoning
  - Pareto dominance
  - frontier versus dominated alternatives
  - tradeoff-surface interpretation
- Caution: algorithm-heavy source; translate concepts into evaluation-friendly policy rules.
- Authority status: operationalized

### BOOK-KEENEY-RAIFFA-1976

- Canonical citation: Keeney and Raiffa. Decisions with Multiple Objectives: Preferences and Value Tradeoffs.
- Pin: `book:wiley-1976-keeney-raiffa`
- Experiments: E1, E2
- Operational constructs:
  - explicit objective articulation
  - value-tradeoff design
  - preference structuring before scoring
  - decision framing before arbitration comparisons
- Caution: use to define objectives and rubrics, not to prescribe the intervention algorithm.
- Authority status: operationalized

## Pending Normalization

### PAPER-MARLER-2010

- Canonical citation: Marler and Arora. The Weighted Sum Method for Multi-Objective Optimization: New Insights.
- Pin: `doi:10.1007/s00158-009-0460-7`
- Experiments: E2, E4
- Current use: practical comparison context for the weighted-sum baseline.
- Caution: the project previously referred to this source as if it were the broader survey; resolve whether MOGT needs the 2010 weighted-sum paper, the 2004 survey, or both.
- Authority status: pending normalization

### PAPER-WOOLDRIDGE-2009

- Canonical citation: Wooldridge. An Introduction to MultiAgent Systems.
- Pin: `book:wooldridge-2009`
- Experiments: E3
- Current use: second-wave coordination framing.
- Caution: not yet extracted because E3 is not in the first execution wave.
- Authority status: pending normalization

### PAPER-NASH-1950

- Canonical citation: Nash. Equilibrium and bargaining baseline.
- Pin: `paper:nash-1950`
- Experiments: E3
- Current use: second-wave negotiation-stability framing.
- Caution: keep pending until E3 protocol hardening begins.
- Authority status: pending normalization
