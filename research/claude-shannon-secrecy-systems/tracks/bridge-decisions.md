# Bridge Decisions

Target: Claude Shannon secrecy systems starter tower

Status: pass

| Concept | Decision | Rationale | Follow-up |
| --- | --- | --- | --- |
| Observer prior/posterior model | borrow-carefully | Useful for artifact/evidence reasoning when source and observer are explicit | Reuse locally in research synthesis |
| Secrecy system as transformation family | borrow-carefully | Helps distinguish actual path from possible paths | Keep inside this tower unless promoted |
| Perfect secrecy | block | Too formal and strong to use as casual vocabulary | No promotion without formal governance |
| Equivocation | promotion-candidate | Strong local fit for "remaining uncertainty after evidence," but needs careful definition | Use `definitions-governance` only on request |
| Redundancy as leakage source | borrow-carefully | Useful for thinking about visible structure and inferential attack surface | Keep source-bound |
| Unicity distance | analogy-only | Valuable threshold metaphor but formula is source-specific | Do not apply quantitatively |
| Confusion | analogy-only | Can teach hidden-coordinate complexity but is easy to misuse | Keep in examples only |
| Diffusion | analogy-only | Can teach distributed leakage but is easy to overgeneralize | Keep in examples only |
| Enemy knows the system | borrow-carefully | Good safety posture against obscurity assumptions | Do not treat as full threat modeling |
| Ideal systems | block | Source-specific term likely to confuse local governance meaning of "ideal" | No promotion |

## Promotion Boundary

The only promotion candidate listed here is `equivocation`, and it is not
promoted by this tower. It requires a separate governed promotion decision.

