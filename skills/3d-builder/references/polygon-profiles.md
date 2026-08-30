# Polygon Profiles

Resolve the profile before final modeling. Treat the ranges as starting budgets, then adjust for silhouette complexity, camera distance, deformation, platform, and texture strategy.

| Profile | Typical evaluated triangles per hero asset | Purpose | Required delivery |
|---|---:|---|---|
| `low-poly` | 5k–80k | Mobile, distant NPCs, stylized realtime assets | Runtime mesh, UV/materials, rig when needed |
| `high-poly master` | 250k–2M+ | Close-up renders, sculpt source, baking source | Editable high-resolution source and close-up renders |
| `high-poly master + game LODs` | Master 250k–2M+; LOD0 40k–150k; lower LODs by measured need | Hero game characters | High master, retopologized LOD0, lower LODs when required, normal/AO baking |

For unusually simple forms, justify a lower count with close-up curvature evidence. For complex creatures, hair, foliage, scales, or layered clothing, raise the budget when silhouette and deformation require it.

If an approved lower-count pilot exists, preserve or improve its visual information and deformation quality. A higher triangle target never authorizes a silhouette, anatomy, feature-density, stage-differentiation, or rig-quality regression.

## High-poly acceptance

Require all of the following:

- record evaluated triangles, vertices, texture resolution, and whether modifiers are applied;
- refine primary silhouette and stage/object-specific proportions against references;
- add purposeful secondary forms and surface transitions visible in close-up;
- eliminate obvious primitive intersections, faceting, pinching, and paper-thin unintended parts;
- render front, three-quarter, side, back, and close-up views at the intended quality;
- preserve an editable source; generate runtime LODs separately rather than overwriting the master;
- validate rig deformation on the runtime topology when animation is required.
- record the pre-subdivision art source and prove that it already meets the approved visual baseline.

Subdivision can support smooth curvature, but subdivision alone does not satisfy the high-poly gate. Reject assets whose evaluated count increased without corresponding shape or surface improvement.

## Decision wording

If the user did not specify a profile, ask one concise question: “這次要製作低模、純高模母版，還是高模母版加遊戲用 LOD？” State the likely storage, render-time, and runtime consequences before execution.
