# Business Ontologies in Arcanum

## The Core Concept

In the context of Arcanum's Ontology Harness and Ontology Vault, a **Business Ontology** represents the pure domain intent, language, rules, policies, premises, and expected outcomes of a software system. It is strictly separated from how that system is implemented.

This separation creates a branch-aware ontology model consisting of three distinct layers:

1. **Business Ontology (Intent):** The definitive source of truth for domain semantics. It defines *what* the system is, *who* interacts with it, and the *value* it provides, completely devoid of implementation details.
2. **System Ontology (Realization):** The operational reality. It represents the codebase, runtime evidence, infrastructure topology, and technical architecture (e.g., databases, API endpoints).
3. **Bridge Layer (Traceability):** The connective tissue that links Business Intent to System Realization. It contains the traceability graph, tests, observability metrics, constraints, and drift reports.

## Epistemic Foundations: Antifragility via *Via Negativa*

Following Nassim Taleb's principle of *Via Negativa* (subtraction over addition), the Business Ontology avoids formalizing rules prematurely. The ontology is curated using a rigorous evidentiary threshold: **formalize a rule or axiom only when its absence has proven costly or caused measurable harm (drift, architectural bugs, miscommunication).** 

## The Knowledge Substrate: Building Blocks of the Ontology

To accurately map domain intent, the Business Ontology uses specific node types and metadata to classify the weight, certainty, and governing force of information. These elements form the "substrate" of the ontology:

### 1. Axioms
Axioms are the load-bearing truths and epistemic foundations of the domain. They define *why* certain principles exist (e.g., "Docs before code"). They are treated as indisputable constraints until overwhelming empirical evidence forces their revision. Axioms serve as the ultimate justification for all downstream governance rules and system implementation choices.

### 2. Constitutions
Constitutions are the codified governance rules and process conventions derived from Axioms (e.g., a *Domain Tagging Constitution* or *Frontend Constitution*). While an Axiom explains the *why*, a Constitution mandates the *how* for human collaborators and AI agents. Constitutions ensure that all execution within the repository adheres strictly to the Business Ontology's constraints.

### 3. Premises
Not all domain knowledge starts as a hardened fact. Premises are working bets, hypotheses, or unverified domain assumptions currently under review. A premise represents an evolving piece of the Business Ontology. Over time—and based on the accumulation of bridge evidence or decision gates—a premise can be promoted (to a formal rule/axiom), revised, split, or retired.

### 4. Confidence Levels
The Business Ontology does not treat all knowledge nodes as equally trustworthy. It relies on a dual-signal confidence system to manage uncertainty and risk:
- **Evidence Confidence:** Measures how well a claim, policy, or premise is supported by reality (e.g., Is there a system test proving this? Are there user analytics validating this assumption?).
- **Commitment Confidence:** Measures how deeply the project should currently rely on this node. Can we build core architectural pillars on this premise, or is it too speculative?

By separating *how well supported* something is from *how heavily we depend on it*, the Business Ontology allows teams to explore uncertain domain areas (low evidence) without building brittle architectures (safeguarding via low commitment).

## Hierarchical Data & Policy Resolution

A core concept of an effective Business Ontology is the structuring of domain data and policies using **Trees**—a fundamental hierarchical data structure in computer science. In a complex enterprise, policies cannot realistically be defined exclusively at the root (as a single global policy cannot accommodate all exceptions and context details) nor exclusively at the leaf level (as defining entirely personalized policies for every single customer or employee is completely unmaintainable). 

Instead, policies are scattered across the various levels of the hierarchy, attached to specific nodes. Because tree traversal is highly efficient, Necronomicon can seamlessly determine the exact list of policies applicable to any specific leaf or node based on its inheritance path.

**Examples of Hierarchical Specificity:**
- **Jurisdictional Context:** When asking, *"What is the minimum driver age for renting a car in Alabama?"* the ontology traverses from a global corporate policy (root), overrides it with US-specific regulations (mid-level node), and ultimately applies Alabama's specific state laws or company self-regulations preventing recent local incidents (leaf).
- **Environmental & Location Context:** Answering *"What is a valid air pressure for a minivan delivery truck in winter?"* requires the ontology to fold in facility locations and adjust policies dynamically based on local weather structures linked in the ontology.

Attempting to force high-level generalized rules (e.g., "Always turn on headlights between November and March globally") wastes resources on sunny days or misses exceptions. The Business Ontology resolves this by ensuring specificity: policies are inherited and overridden exactly where the business context demands it.

## Value Proposition for Necronomicon

Necronomicon is designed to act on domain intent rather than just document it. Business Ontologies provide the foundational layer for this cybernetic control loop.

- **Preventing Drift:** By treating the Business Ontology as an executable baseline rather than static documentation, Necronomicon can continuously compare the System Ontology against it. If the implementation diverges from the domain intent, it's flagged as architectural drift.
- **Governed Traceability:** The ontology harness maps every runtime artifact back to a business premise. If a component exists in the System Ontology but lacks a corresponding link in the Business Ontology, it represents untracked technical debt or unauthorized scope.
- **Deterministic Context for Agents:** When AI agents (or human operators) interact via the Necronomicon harness, the Business Ontology provides a strict, unambiguous glossary and rule set. This prevents hallucinations and ensures all executed tasks align with the approved domain model.

## Integration with Ontology Vault

The `ontology-vault` sigil and `ontology-harness` spell utilize this branch-aware structure:

- When discovering a domain, the harness first extracts and solidifies the **business ontology map**.
- It subsequently maps the **system ontology** from repository evidence.
- Finally, it validates the **bridge** between the two, generating actionable insights for the `task-session` to resolve discrepancies.
