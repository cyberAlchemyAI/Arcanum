Here is the complete project handoff blueprint. This document is designed to serve as your foundational architectural reference, bridging the theoretical benchmarks with a deterministic, production-ready engineering plan.

You can drop this directly into your documentation wiki or project management tool to start building.

---

# Project Blueprint: Agentic Tech Debt & Optimization Harness

## 1. Context & Objectives

As autonomous coding agents become integrated into the software development lifecycle, evaluating their ability to write _new_ code is no longer sufficient. The next frontier is assessing their ability to manage **Essential Complexity** and resolve technical debt in legacy codebases.

**The Objective:** Build a unified, deterministic benchmarking harness that evaluates an agent's capacity to:

1. Refactor deprecated and spaghetti code without breaking test suites.
2. Identify and resolve cross-module architectural code smells (e.g., God Objects, deep inheritance).
3. Optimize algorithmic execution for better CPU/memory performance.

This harness will provide strict, reproducible telemetry on both the agent's success rate and its trajectory cost (how efficiently it navigated the repository).

## 2. Core References & Oracles

The system will ingest data and score agents based on three state-of-the-art evaluation frameworks:

- **SWE-bench (Tech Debt Subset):**
- _Source:_ `princeton-nlp/SWE-bench` (via Hugging Face).
- _Focus:_ Filtered specifically for `refactor`, `cleanup`, and `performance` labels.
- _Oracle:_ Dockerized repository unit tests verifying semantic correctness post-patch.

- **SmellBench (Released May 2026):**
- _Focus:_ Architectural and structural debt repair (e.g., resolving tight coupling in `scikit-learn`).
- _Oracle:_ Model Context Protocol (MCP) orchestrator paired with static analysis (PyExamine) to mathematically verify smell reduction.

- **PerfCodeBench (Released May 2026):**
- _Focus:_ System-level execution speed optimization.
- _Oracle:_ Deterministic execution environment that compares the agent's refactored runtime against a "human-expert" baseline.

## 3. System Architecture

To ensure scalability and clean domain boundaries, the architecture splits the orchestration logic from the execution sandboxes.

- **The Orchestrator (Node.js / TypeScript):** Manages the queue of benchmark tasks, handles state, and traces the agent's telemetry. This layer standardizes the task definitions before passing them to the agent.
- **The Agent Interface:** An abstract contract that your autonomous agent must fulfill. It accepts a `TaskDefinition` and a codebase state, returning a `.patch` file or structural diff.
- **The Execution Sandboxes (Python / Docker):** Ephemeral, heavily isolated containers spun up on demand via AWS or local daemon. These are strictly constrained (especially for PerfCodeBench) to ensure deterministic runtime metrics.
- **Telemetry & Visualization (React):** A frontend layer to visualize the agent's trajectory, the reduction in cyclomatic complexity, and pass/fail ratios across the three benchmark suites.

## 4. Execution Plan

1. **Phase 1: Infrastructure & Orchestration:** Weeks 1-2.
   Establish the core `BaseAgent` interface and the task routing logic. Set up the Docker daemon integration so the orchestrator can spin up and tear down isolated containers deterministically. Build the telemetry tracing to capture the agent's trajectory cost.

2. **Phase 2: SWE-bench Tech Debt Integration:** Weeks 3-4.
   Implement the dataset ingestion from Hugging Face. Build the filtering logic to isolate refactoring and cleanup tasks. Establish the evaluation loop: Agent generates patch -> Docker applies patch -> Container runs `pytest` -> Orchestrator records pass/fail.

3. **Phase 3: Structural & Performance Integrations:** Weeks 5-6.
   Integrate SmellBench by setting up the Model Context Protocol (MCP) bridge and PyExamine oracle. Next, implement PerfCodeBench, ensuring the Docker containers have strict, hard-coded CPU/RAM limits to prevent noisy execution speed metrics.

4. **Phase 4: Telemetry Dashboarding:** Week 7.
   Connect the orchestrator's telemetry data to a React frontend. Visualize the delta in complexity scores, execution runtimes, and the agent's API call efficiency during the refactoring loops.

---

## 5. Next Steps for Bootstrapping

1. **Define the Agent Interface:** Lock in the JSON schema for how the orchestrator will pass the repository context (e.g., AST dumps vs. raw file text) to the agent.
2. **Resource Allocation:** Provision the isolated environment for Phase 1. For PerfCodeBench, ensure the hardware running the Docker daemon is not shared with the LLM inference engine to avoid CPU throttling.
