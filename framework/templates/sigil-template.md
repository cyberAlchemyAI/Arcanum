---
name: <sigil-name>
description: "[State what the skill does and the concrete requests or contexts that should trigger it.]"
---

<!--
Keep name and description. Add metadata, license, or allowed-tools only when
the target runtime and this sigil require them. Put Arcanum governance fields
in SKILL.md.artifact.yml.
-->

# Sigil: <Sigil Name>

<objective>
[Clearly state the transformation or outcome this Sigil intends to achieve.]
</objective>

<logic-type>
[Formulae: Stateless/Deterministic | Transmutations: Probabilistic/Synthetic | Arcana: Recursive/Sovereign]
</logic-type>

<observability>
Define what counts as a meaningful execution, which compact signals are useful,
and the manual, usage, output, gap, and severe-gap reflection triggers. Emit or
prepare telemetry only when repository observability is available.
</observability>

<process>
1. [Step one of the execution loop]
2. [Step two of the execution loop]
3. [Step three of the execution loop]
...
</process>

<quality-bar>
See [Quality Bar](../QUALITY-BAR.md) for authoring guidance.

A successful execution of this Sigil must:

- [Constraint 1]
- [Constraint 2]
</quality-bar>

<anti-patterns>
See [Anti-Patterns](../ANTI-PATTERNS.md) for authoring guidance.

- [Avoid X because of Y]
- [Do not use this Sigil if Z is the primary goal]
</anti-patterns>

<output-contract>
The result must return:
- [Description of final artifact or state change]
</output-contract>
