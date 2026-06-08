---
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: arcana/structured-interview-kits/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
name: interrogation
description: "Use when: running one-question-at-a-time interviews with pluggable modes, evidence-backed prompts, and artifact updates after each answer."
argument-hint: "<target-scope> [--mode <mode-id>|auto] [--dry-run]"
tier: arcana
domain: structured-interviewing
version: 0.1.0
origin: generalized from recurring evidence-backed interview practice
aliases:
   - Interrogation
alias-command-slug: interrogation
alias-command: arcanum-sigil-interrogation
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, Agent
---

# Sigil: Structured Interview Kits

<objective>
Run a reusable interview session that asks one evidence-backed question at a time, records decisions, updates target artifacts, and exits with a readiness verdict.
</objective>

<logic-type>
Arcana: multi-turn human-gated inquiry with mode selection and artifact synchronization.
</logic-type>

<identity>
- Canonical ID: `structured-interview-kits`
- Primary alias: `Interrogation`
- Alias command slug: `interrogation`
- Alias command: `arcanum-sigil-interrogation`
</identity>

<process>
1. Resolve the target scope and candidate artifacts.
2. Build a cheap evidence baseline before asking avoidable questions.
3. Select interview mode:
   - use an explicit mode when provided,
   - select automatically when applicability is clear,
   - ask one clarification question when mode choice is ambiguous.
4. Generate candidate questions using the selected mode's formation strategy.
5. Select the highest-discrimination question: the one most likely to resolve a blocker, expose a risk, or improve an artifact.
6. Ask exactly one question at a time.
7. Each question must include:
   - concise context,
   - why the answer matters,
   - recommended default when safe,
   - unresolved risk if unanswered,
   - target artifact or decision record.
8. Wait for the user answer.
9. Patch or update the target artifact immediately when the answer changes it.
10. Record selected option, rejected alternatives, and rationale when a decision is made.
11. Repeat until mode exit criteria are satisfied.
12. Return `pass`, `flag`, or `block` with remaining ambiguities.
</process>

<mode-extension-contract>
To add a new interview mode, define:

- mode ID,
- applicability signals,
- question formation strategy,
- required question fields,
- allowed patch targets,
- exit criteria,
- readiness verdict rules.

Do not change the orchestrating sigil unless the mode contract itself changes.
</mode-extension-contract>

<quality-bar>
A successful execution must:

- ask one question at a time,
- base each question on evidence or explicit uncertainty,
- avoid dumping full question banks,
- update artifacts after answers when mutation is in scope,
- preserve decision traceability,
- distinguish blocker ambiguity from non-blocker ambiguity,
- stop cleanly when exit criteria are met.
</quality-bar>

<anti-patterns>
Avoid:

- asking broad generic questions without evidence,
- asking multiple unrelated questions at once,
- continuing after a blocker answer contradicts the target artifact without updating it,
- using interview mode as hidden implementation planning,
- inventing answers for the user,
- treating unresolved blocker ambiguity as readiness.
</anti-patterns>

<output-contract>
Return:

```markdown
## Structured Interview Result

- Target scope: <scope>
- Mode: <mode-id>
- Questions asked: <count>
- Decisions recorded: <count>
- Artifacts updated: <paths or none>
- Remaining ambiguities: <summary>
- Verdict: pass | flag | block
- Next step: <action>
```
</output-contract>
