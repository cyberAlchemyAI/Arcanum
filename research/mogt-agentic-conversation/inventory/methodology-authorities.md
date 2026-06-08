# MOGT Methodology Authorities

Purpose: secondary thematic rollup for the first-wave methodology, evaluation, and overhead authorities used by E1 through E4.

This file is a convenience view, not the content authority.

Current raw-backed library coverage:

- `inventory/library/REPORT-DOSHI-VELEZ-KIM-2017.md`

Current sources still awaiting raw-backed library entries:

- `PAPER-WOHLIN-2012`
- `PAPER-WALKER-1997`
- `BOOK-JAIN-1991`
- `PAPER-HART-STAVELAND-1988`

## Operationalized Authorities

### PAPER-WOHLIN-2012

- Canonical citation: Wohlin et al. 2012. Experimentation in Software Engineering.
- Pin: `book:springer-2012`
- Experiments: E1, E2, E3, E4
- Operational constructs:
  - paired comparative design
  - validity-threat framing
  - reproducibility metadata discipline
  - success-criteria evaluation and reporting
- Caution: use for experimental rigor, not for multi-objective decision theory.
- Authority status: operationalized

### REPORT-DOSHI-VELEZ-KIM-2017

- Canonical citation: Doshi-Velez and Kim. Towards A Rigorous Science of Interpretable Machine Learning.
- Pin: `arxiv:1702.08608v2`
- Experiments: E1
- Operational constructs:
  - explanation-evaluation taxonomy
  - human-grounded evaluation
  - application-grounded evaluation
  - avoid verbosity-as-interpretability in rubric design
- Caution: evaluation framing source, not a general methodology authority.
- Authority status: operationalized

### PAPER-WALKER-1997

- Canonical citation: Walker et al. 1997. PARADISE: A Framework for Evaluating Spoken Dialogue Agents.
- Pin: `doi:10.3115/976909.979652`
- Experiments: E1, E4
- Operational constructs:
  - matched dialogue-episode evaluation
  - task-success plus cost tradeoffs
  - acceptance-style outcome scoring
  - quality-versus-overhead interpretation
- Caution: spoken-dialogue framing must be adapted carefully to agentic conversation decisions.
- Authority status: operationalized

### BOOK-JAIN-1991

- Canonical citation: Jain. The Art of Computer Systems Performance Analysis.
- Pin: `book:jain-1991`
- Experiments: E4
- Operational constructs:
  - latency and throughput measurement discipline
  - benchmark comparability
  - breakpoint analysis
  - confidence-aware reporting of overhead metrics
- Caution: use for instrumentation and threshold discipline, not for quality scoring.
- Authority status: operationalized

### PAPER-HART-STAVELAND-1988

- Canonical citation: Hart and Staveland. Development of NASA-TLX (Task Load Index): Results of Empirical and Theoretical Research.
- Pin: `doi:10.1016/S0166-4115(08)62386-9`
- Experiments: E4
- Operational constructs:
  - subjective workload dimensions
  - reviewer-burden accounting
  - paired workload comparison across policy regimes
  - human-cost interpretation alongside system overhead
- Caution: measures reviewer workload, not system cost; use as a complementary signal only.
- Authority status: operationalized
