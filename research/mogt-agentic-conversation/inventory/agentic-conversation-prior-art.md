# MOGT Agentic Conversation Prior Art

Purpose: secondary thematic rollup for first-wave prior art on agents making decisions through conversation, coordination, debate, and negotiation.

This file is a convenience view, not the content authority.

Backed per-source library entries:

- `inventory/library/PAPER-WU-2024-AUTOGEN.md`
- `inventory/library/PAPER-LIU-2024-AGENTBENCH.md`
- `inventory/library/PAPER-DU-2023-MULTIAGENT-DEBATE.md`
- `inventory/library/PAPER-LEWIS-2017-DEAL-OR-NO-DEAL.md`
- `inventory/library/PAPER-GUO-2024-LLM-MULTIAGENTS-SURVEY.md`

## Operationalized Authorities

### PAPER-WU-2024-AUTOGEN

- Canonical citation: Wu et al. AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation.
- Pin: `arxiv:2308.08155v2`
- Experiments: E1, E3, E4
- Operational constructs:
  - role-based multi-agent conversation
  - turn-level orchestration and handoff
  - inspectable intermediate conversation artifacts
  - conversational coordination policies
- Caution: useful orchestration prior art, but not a controlled benchmark authority by itself.
- Authority status: operationalized

### PAPER-LIU-2024-AGENTBENCH

- Canonical citation: Liu et al. AgentBench: Evaluating LLMs as Agents.
- Pin: `arxiv:2308.03688v3`
- Experiments: E1, E2, E4
- Operational constructs:
  - benchmark-oriented evaluation of agent behavior
  - task-completion and decision-quality framing
  - controlled comparisons across agent configurations
  - evaluation discipline for agentic systems
- Caution: strongest as evaluation prior art; it does not itself validate conversational multi-agent policies.
- Authority status: operationalized

### PAPER-DU-2023-MULTIAGENT-DEBATE

- Canonical citation: Du et al. Improving Factuality and Reasoning through Multiagent Debate.
- Pin: `arxiv:2305.14325v1`
- Experiments: E2, E3, E4
- Operational constructs:
  - debate-style deliberation
  - critique and revision loops
  - disagreement exposure before final selection
  - coordination through structured dialogue
- Caution: debate is narrower than full negotiation or orchestration; do not use it as the sole coordination authority.
- Authority status: operationalized

### PAPER-LEWIS-2017-DEAL-OR-NO-DEAL

- Canonical citation: Lewis et al. Deal or No Deal? End-to-End Learning of Negotiation Dialogues.
- Pin: `doi:10.18653/v1/D17-1259`
- Experiments: E3, E4
- Operational constructs:
  - dialogue-based negotiation tasks
  - agreement and convergence measures
  - utility-sensitive conversational outcomes
  - bounded-turn negotiation framing
- Caution: pre-LLM setting; use for negotiation structure and metrics, not as a full modern agent-framework authority.
- Authority status: operationalized

### PAPER-GUO-2024-LLM-MULTIAGENTS-SURVEY

- Canonical citation: Guo et al. Large Language Model based Multi-Agents: A Survey of Progress and Challenges.
- Pin: `arxiv:2402.01680v2`
- Experiments: E1, E2, E3, E4
- Operational constructs:
  - orchestration design space
  - communication and coordination failure modes
  - evaluation and systems challenges
  - external-validity framing for multi-agent LLM systems
- Caution: survey authority for framing and coverage, not for threshold setting.
- Authority status: operationalized
