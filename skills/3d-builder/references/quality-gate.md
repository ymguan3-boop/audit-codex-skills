# 3D Experience Quality Gate

Run this checklist before reporting completion.

## Environment and provenance

- [ ] Required local and MCP capabilities were verified, not assumed.
- [ ] Every installation, model download, hosted upload, or paid request had explicit consent.
- [ ] Authored and generated assets record tool/model, source, license, and relevant settings.
- [ ] No credentials or confidential reference data appear in logs, source, metadata, or chat.
- [ ] Hosted Hunyuan3D runs record the Hugging Face Space/revision, consent, queue/quota outcome, and preserved raw output.

## Polygon profile

- [ ] The user selected `low-poly`, `high-poly master`, or `high-poly master + game LODs` before final modeling.
- [ ] Per-asset evaluated triangles, vertices, texture resolution, and applied/unapplied modifiers are recorded.
- [ ] A high-poly claim is supported by improved silhouette, purposeful secondary forms, clean curvature, back and close-up renders—not subdivision count alone.
- [ ] High-poly masters remain separate from runtime LODs and were not overwritten by decimation or retopology.

## Art approval and batch integrity

- [ ] Existing approved and rejected examples were discovered and recorded before modeling.
- [ ] The candidate meets or exceeds the approved baseline even when the baseline has fewer polygons.
- [ ] One representative per anatomy/topology pathway has a reference/baseline/candidate/deformation comparison sheet.
- [ ] Required user visual approval was recorded before batch expansion.
- [ ] `TECHNICAL_PASS`, `ART_REVIEW_PENDING`, `USER_APPROVED_PILOT`, `VERIFIED`, and `REJECTED_ART_QUALITY` were not conflated.
- [ ] Related stages or variants have reference-supported silhouette, proportion, and feature differences.
- [ ] High polygon counts came from an information-rich art source, not mechanical subdivision of a simplified primitive assembly.

## Asset integrity

- [ ] Every requested asset has a stable registry key and GLB or intentional procedural fallback.
- [ ] Axes, origin, scale, forward direction, normals, and transforms are verified in Blender and the browser.
- [ ] Materials have deliberate color, roughness, metalness, and texture resolution.
- [ ] Required clips exist with stable names; thumbnails match browser models.
- [ ] AI-generated meshes were checked for holes, intersections, duplicate geometry, topology, UVs, and animation readiness.
- [ ] Generated assets were retopologized, decimated, repaired, or rejected when necessary.
- [ ] The rig contains anatomy-appropriate joint groups and representative local deformations pass after GLB re-import.

## Runtime appearance and motion regression

- [ ] The approved high/master source is immutable; runtime, rigged, decimated, and exported derivatives use versioned paths.
- [ ] A clean GLB re-import preserves materials, textures, UVs, silhouette, proportions, and connected clothing/accessories relative to the approved render.
- [ ] Procedural Blender materials were either exported compatibly or replaced with baked/packed glTF-safe textures and verified in the target viewer.
- [ ] Displayed colors were compared from equivalent renders; source RGB/hex values alone were not treated as proof of a match.
- [ ] Decimation did not create jagged material seams, fringe triangles, holes, floating parts, or loss of identity features.
- [ ] Extreme poses show no garment/skin gaps, detached collars, separated head/neck, disconnected ankles/shoes, or collapsed shoulders/elbows/knees.
- [ ] Motion was checked in world space from the asset's declared forward axis; clip names and keyframe presence were not used as substitutes for visible motion.
- [ ] Throws and releases include anticipation, weight transfer, torso/shoulder drive, extension, follow-through, and a verified held-to-projectile visibility switch when required.
- [ ] Preview frame folders contain only the expected version and frame range; stale frames cannot leak into GIF/video output.
- [ ] Blender automation logs were scanned for tracebacks and an explicit success sentinel, and all expected artifacts exist even when Blender returned exit code 0.
- [ ] Every rejected build is quarantined, visibly marked `REJECTED-NOT-FOR-DELIVERY`, and excluded from game/runtime integration.

## Visual quality

- [ ] The first viewport has a clear subject, useful framing, sufficient contrast, and deliberate lighting.
- [ ] Important identity features remain visible at the intended camera distance.
- [ ] Reference-driven assets have front, three-quarter, side, back, and close-up comparison views.
- [ ] Desktop landscape and mobile portrait layouts were checked.
- [ ] Loading, empty, fallback, and error states are visible and understandable.

## Interaction and accessibility

- [ ] Camera reset and the primary pointer interaction work.
- [ ] Keyboard or touch equivalents work for important actions.
- [ ] Focusable controls have labels and visible active/focus states.
- [ ] Guided navigation or game state always has a path back.
- [ ] Audio begins only after user interaction and can be muted.

## Performance and lifecycle

- [ ] GLBs are cached; repeated instances clone cached scenes instead of re-downloading.
- [ ] Pixel ratio is capped and low-power paths exist for shadows, antialiasing, particles, AI, and mixers.
- [ ] Distant entities do not run full-frequency updates.
- [ ] Renderer, textures, geometries, materials, controls, and listeners are disposed when appropriate.
- [ ] Asset size and polygon/texture budgets match the target device and viewing distance.

## Verification

- [ ] Asset tests, lint, unit tests, and production build pass when applicable.
- [ ] A production-like server renders the intended route.
- [ ] Browser verification checks the visible canvas, controls, responsive layout, and console errors.
- [ ] Asset-only outputs open independently in the intended viewer/tool.
- [ ] If deployed, a fresh cache-busted tab verifies the public URL.
- [ ] Final `VERIFIED` counts include only assets that passed both technical and art-quality gates.
- [ ] Any discovered regression triggered status revocation, a visible rejection marker, archive quarantine, and removal from the delivery path.
