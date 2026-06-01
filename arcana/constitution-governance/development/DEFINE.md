# Define: Constitution Governance Sigil

Status: candidate
Date: 2026-05-27
Authoring route: invoke define, materialized locally

## Problem

Constitutions are meant to enforce artifact structure and form. If every new rule is added to one large constitution, the file becomes expensive to load, weaker in context, and less likely to affect execution. A large constitution also blurs which rules are relevant to a task and which validator should enforce each rule.

## Definition

Constitution Governance is a sigil for modular constitution lifecycle work:

- creating constitutions,
- adding rules,
- selecting relevant constitutions before a task,
- composing selected rules into a minimal governance pack,
- connecting rules to validation adapters,
- splitting oversized constitutions,
- preparing canonical promotion.

## Core Decision

Context Builder selects relevant constitution evidence. Constitution Governance composes selected rules, resolves precedence/conflict, and maps enforceable rules to validators.

Context selection alone is not enough when rules interact or need enforcement.

## Glossary

| Term | Definition |
| --- | --- |
| Constitution | Durable governance artifact for structure, form, or artifact behavior. |
| Rule | One enforceable or reviewable requirement inside a constitution. |
| Selector | Predicate that says when a constitution or rule applies. |
| Composition pack | Minimal task-specific set of selected constitution rules. |
| Validation adapter | Script, lint, test, schema, or review checklist that enforces a rule. |
| Context load budget | Limit on governance context loaded before rule effect decays. |

## Scope

In scope:

- framework and capability constitutions,
- artifact-type constitutions,
- task-specific composition packs,
- validator impact analysis,
- split/debloat plans,
- promotion readiness.

Out of scope:

- executing downstream tasks,
- treating all selected context as canonical,
- replacing Context Builder,
- replacing Decision Gate for blocker choices,
- mutating validators without a rule-to-check mapping.

## Initial Validation Surface

- `tools/validate-artifact-constitution.sh`
- `framework/ARTIFACT-CONSTITUTION.md`
- future constitution-specific validators under `tools/`

## Invoke Result

- Mode: define
- Status: pass
- Next route: sigil-development
