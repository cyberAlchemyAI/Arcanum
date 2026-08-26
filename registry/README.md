# Arcanum Registry

The Arcanum registry catalogs reusable sigils and spells.

Use it when you want to choose a capability, install a composition, or review what the framework currently offers.

## Catalogs

- [Sigils](SIGILS.md) - available sigils by tier and use case.
- [Spells](SPELLS.md) - reusable compositions of multiple sigils.
- [Packs](PACKS.md) - future curated bundles of related sigils and spells.
- [Sigil Dependencies](SIGIL-DEPENDENCIES.tsv) - deterministic dependency edges
  used to close selective installations.

## Registry Rules

A registry entry should be stable enough for another repository to reference it by name.

Register a sigil only when it has:

- a folder under `formulae/`, `transmutations/`, or `arcana/`,
- an executable, runtime-native `SKILL.md` whose intent is human-reviewable,
- governed metadata in a runtime-compatible encoding,
- a clear output contract,
- quality and anti-pattern guidance,
- observability or reflection guidance when reuse is expected.

Register a spell only when it names the sigils it composes, phase order, shared state, gates, handoffs, observability, and output contract.

When one sigil cannot execute without another installed sigil, record the edge
in `SIGIL-DEPENDENCIES.tsv` and validate its transitive closure before release.
The public registry builder uses the same manifest. A download whose closure
contains more than one skill is published with an explicit `-bundle.zip` suffix
and contains one top-level folder per required skill. Do not describe or publish
a dependency-bearing sigil as a standalone ZIP.

## Framework Boundary

The registry lists reusable artifacts. The [framework](../framework/) defines how those artifacts are authored, reviewed, observed, and maintained.
