---
name: discovery-writing
description: "Use when creating or revising a discovery document before DomainSpec authoring or implementation planning, to connect the broader project objective, business context, intended change, evidence, design direction, and technical specifications."
---

# Discovery Writing

## Purpose

A discovery explains **what should change, why it matters, and what the intended design must accomplish** before implementation planning begins.

It should move progressively from:

**project objective → business context → intended change → design → technical specification**

The beginning is for humans to understand the work. Later sections may become increasingly technical for engineers and agents.

A discovery is **not a task list**. If the document mainly describes a sequence of implementation steps, it is an implementation plan.

## Artifact Posture

A discovery is non-governing evidence. It may inform a DomainSpec, Design, or WORK-PACK, but it does not approve them or authorize implementation.

## Structure

Treat the sections below as a minimum narrative spine, not a closed template. Add any sections needed to explain material concepts, flows, constraints, risks, alternatives, or other aspects of the system. Preserve the progression from project objective to technical specification.

### Objective

Always start from the **broader project objective**, not the isolated feature.

Explain what the project is trying to achieve and how this work contributes to that outcome. Keep it short.

### 1. Business Context

Explain the current situation, why it matters, and why the existing system is insufficient.

Start in business or domain language. Introduce code details only when needed to substantiate the problem.

### 2. Intended Change

Explain what should become possible or behave differently after the change.

Give the reader a high-level mental model of the proposed direction before introducing technical design.

### 3. Current System and Constraints

Describe only the parts of the current implementation needed to understand the change.

Ground every material factual or technical claim in code, tests, runtime evidence, governing decisions, or other concrete sources. Cite a reproducible locator or durable reference for each claim, and label inference separately from observed evidence.

### 4. Design Direction

Explain the important abstractions, relationships, contracts, and design decisions.

For each important concept, state its name, responsibility or contract, relationships, and the rationale and alternatives when the choice is not obvious.

Clearly distinguish settled decisions, provisional ideas, and open questions. Treat a decision as settled only when a cited governing record supports it; otherwise keep it provisional or open.

Focus on **what the design must accomplish and why**, not the sequence in which it will be implemented.

### High-Level Diagrams

Include high-level diagrams for the principal parts of the system. Let the material determine the number and type of diagrams, such as context, component, flow, or state diagrams.

Focus on actors, boundaries, responsibilities, relationships, and major transitions rather than implementation details. Prefer Mermaid and place each diagram near the text it clarifies. Each diagram must visibly encode at least one material boundary, relationship, flow, or transition described in the adjacent text.

### 5. Technical Specifications

Add only the sections the change requires, such as:

* data model and invariants;
* interfaces and contracts;
* execution or state flow;
* migration and compatibility;
* cleanup.

Be precise enough that an agent can later produce an implementation plan.

### Open Questions

Record unresolved questions that could materially change the design or scope.

Include the current direction when evidence supports one, but do not force a recommendation where uncertainty remains.

---

## Before Writing

Anchor the discovery in the existing project:

* use existing vocabulary from canonical dictionaries or definitions and cite the consulted locations;
* resolve applicable governing records in `authority/decisions/` before treating a decision as settled;
* check constitutions and architectural rules only after verifying their applicability and authority through the governing records;
* inspect the actual code and dependencies before making technical claims.

---

## Quality Checks

Before finishing, verify:

* objective, context, and intended change are clear;
* material factual and technical claims cite reproducible evidence, and inferences are labeled;
* decisions, hypotheses, and open questions are distinguished;
* the design explains the relevant concepts, relationships, and decisions, with high-level diagrams for the principal parts of the system.

---

## Mandatory Don'ts

* Don't make the local feature the project objective.
* Don't begin with code before explaining why the work matters.
* Don't list implementation steps.
* Don't confuse hypotheses with design decisions.
* Don't add technical detail that does not help define the intended system.
* Don't list components when the important information is how they relate.
