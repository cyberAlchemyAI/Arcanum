# Whisper Idea-To-MVP Fixture

Status: fixture artifact for the Arcanum Development Usage Guide.

This fixture shows how one ambitious creative idea moved through the Arcanum loop:

1. raw author intent,
2. core extraction,
3. candidate comparison,
4. hard gates,
5. composition parts,
6. work-pack and SWU execution,
7. validator-backed evidence,
8. residue and next route.

The source example is Whisper rollout `019e6556-940e-7501-ab97-8dc127a624a9`, represented in this repository by the `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/` artifacts.

## What This Demonstrates

Whisper's `resonance_core`, `relevance_core`, and `trajectory_core` can be generalized into an idea exploration grammar:

| Whisper Core | General Idea Core | Question |
| --- | --- | --- |
| `resonance_core` | `idea_resonance` | What human energy, meaning, trust, or relief should the idea create? |
| `relevance_core` | `idea_relevance` | Who is it for, why does it matter here, and what objections must it respect? |
| `trajectory_core` | `idea_trajectory` | What movement does the user make from first encounter to evidence of value? |

Use the fixture files in order:

1. [idea-substrate.yml](idea-substrate.yml)
2. [candidate-routes.yml](candidate-routes.yml)
3. [composition-parts.yml](composition-parts.yml)
4. [WORK-PACK.md](WORK-PACK.md)
5. [EVIDENCE-LEDGER.md](EVIDENCE-LEDGER.md)
6. [PLAYBOOK.md](PLAYBOOK.md)
7. [toy-nonwriting-probe.yml](toy-nonwriting-probe.yml)
8. [validate-fixture.py](validate-fixture.py)

## Boundary

This fixture is explanatory. It does not replace the canonical Whisper source artifacts and does not publish the Substack draft. It translates the pattern so a designer, founder, researcher, or product builder can reuse the method for their own idea.

## Validation

Run:

```bash
python3 development/user-guide/fixtures/whisper-idea-to-mvp/validate-fixture.py --negative
```

The negative probe removes `idea_trajectory` from a tiny non-writing example and should fail internally. The validator reports that expected failure as `NEGATIVE_PROBE=pass`.
