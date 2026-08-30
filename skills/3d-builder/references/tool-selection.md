# Modeling Tool Selection

Assess objects individually. A scene may legitimately use several pathways.

## Decision criteria

Score the following before recommending a tool:

- dimensional precision and alignment;
- hard-surface versus organic form;
- required topology, UVs, deformation, rigging, or animation;
- repetition, variants, and parametric editing;
- target polygon budget and camera distance;
- whether the deliverable is low-poly, a high-poly master, or a high-poly master plus game LODs;
- runtime interactivity or shader-driven behavior;
- reference-image confidentiality and licensing;
- available tools, GPU memory, time, cloud/API cost, and reproducibility.

## Default routing

| Object need | Prefer | Why | Typical fallback |
|---|---|---|---|
| Walls, floors, stairs, roads, dimensioned products, mechanical parts | Blender Python or authored Blender | Exact units, alignment, repeatability, editable geometry | Three.js primitives for simple prototypes |
| Hero hard-surface asset requiring clean topology or animation | Authored Blender | Controlled topology, UVs, rigging, and art direction | Procedural Blender base plus manual refinement |
| Organic sculpture, rocks, plants, creatures, rapid concept variants | Available AI 3D generator, then Blender cleanup | Faster complex surface ideation | Authored/sculpted Blender or licensed stock asset |
| Standard furniture or props | Case-by-case | AI is fast, but exact dimensions and clean topology may favor procedural Blender | Licensed stock GLB or simplified Blender builder |
| Sky, water, fog, grass fields, particles, glow, simple terrain | Three.js shader/procedural runtime | Dynamic, lightweight, and interactive | Baked Blender geometry/material when runtime cost is too high |
| Simple primitive placeholder or collision proxy | Three.js or Blender primitive | Lowest production cost | Existing asset proxy |
| Repeated configurable families | Blender Python plus registry | Deterministic variants and consistent scale | Runtime instancing for geometry-identical items |
| Image-to-3D reconstruction | AI 3D generator plus Blender cleanup | Rapid volume reconstruction | Manual reference modeling for accuracy |

## Selection guardrails

- Do not route all furniture or props to AI automatically.
- Do not use AI-generated meshes for engineering, safety, measurement, fabrication, or regulatory claims without independent geometric validation.
- Prefer a reproducible Blender Python builder when future parameter changes are likely.
- Prefer runtime Three.js effects when baking would inflate asset size or remove interactivity.
- Prefer local generation for confidential images when suitable hardware and licensing allow it.
- Prefer hosted generation only after disclosing likely cost, upload/privacy implications, and provider terms.
- Reject an option when required capabilities are unavailable and the user declines installation; use the documented fallback.
- Do not infer the polygon profile from the word “game”: a game may still require a high-poly baking master.
- Do not call a model high-poly solely because its triangle count is large. Check silhouette, secondary forms, curvature, close-up quality, and editability against [polygon-profiles.md](polygon-profiles.md).
- When recommending Hunyuan3D through Hugging Face, disclose upload/privacy, sign-in, shared queue, changing free allowance, and possible rolling/daily 24-hour quota exhaustion before the first job.

## Recommendation format

Before execution, provide a short table or compact mapping:

| Object/group | Polygon profile | Recommended tool | Reason | Tradeoff/dependency | Fallback |
|---|---|---|---|---|

Group objects with the same rationale. Call out any choice that requires downloads, credentials, cloud upload, paid usage, or licensing review.
