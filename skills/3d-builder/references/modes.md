# 3D Builder Mode Recipes

Use one recipe as the primary domain contract. Combine recipes only when the user explicitly requests or the brief clearly requires a hybrid.

## Product viewer

- Frame a recognizable hero model in the first viewport and provide camera reset.
- Support orbit, pan, and zoom with pointer and touch controls.
- Use variant/material registries instead of duplicated scene code.
- Add labeled hotspots, camera targets, specifications, and a visible loading placeholder.
- Keep the page useful when WebGL or model loading fails.

Acceptance: the camera cannot permanently lose or pass through the product; variants do not reload the app; required controls have keyboard or touch equivalents.

## Architecture and interior

- Group the scene graph by building, floor, room, and object.
- Define named waypoints for entrances, rooms, overview, and details.
- Add deliberate lighting presets, labels, material legend, hotspots, and optional measurements.
- Prefer navigation zones or collision volumes over mesh-level physics.
- Use distance-based loading or update throttling for large scenes.

Acceptance: users can return to overview from every room; dimensions and circulation remain readable; generated furniture is scale-checked against the authored structure.

## Digital exhibition

- Represent exhibits with stable IDs, titles, models, descriptions, media, source/license metadata, and camera targets.
- Provide an index, selected-exhibit panel, next/previous navigation, and guided-tour state.
- Keep captions in accessible DOM and honor reduced motion.
- Allow audio/video to be muted, paused, resumed, and restarted.

Acceptance: every exhibit is reachable and titled; the tour can pause/resume/restart; missing assets have visible fallbacks.

## 3D game

- Define explicit modes such as `world`, `challenge`, `capture`, `menu`, and `result`.
- Separate player, entities, collision, rewards, inventory, and save data.
- Use a shared GLB cache; throttle distant AI and mixers.
- Provide deterministic win/lose/reward rules and a reset that preserves valid saved data.

Acceptance: pointer/keyboard plus touch paths work as applicable; collision contains the player; HUD communicates mode, objective, inventory, and progress.

## 3D animation

- Store clip names and durations in a registry and update one `AnimationMixer` path from one clock.
- Provide play, pause, restart, scrub, and clip selection.
- Use camera keyframes or scripted targets and a poster frame while loading.

Acceptance: controls never create duplicate loops; scrubbing/restarting is deterministic; missing clips fall back to a static pose and clear message.

## Asset-only delivery

- Define units, axes, origin, polygon budget, materials, texture resolution, required clips, LODs, thumbnails, and output formats before modeling.
- Deliver source `.blend` or procedural builder when requested, plus stable GLB/GLTF outputs.
- Include an asset manifest with authored/generated provenance, tool/model, source/license, scale, clips, and known limitations.

Acceptance: every asset opens independently, matches the manifest, and passes geometry/material/animation checks without depending on a web application.

