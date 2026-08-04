---
name: blender-react-threejs-3d-builder
description: Build reusable Blender + React + Three.js 3D experiences from briefs, including product viewers, architectural and interior spaces, digital exhibitions, browser games, and animated scenes. Use when the user requests 3D asset generation, GLB integration, interactive camera controls, web-based 3D presentation, game mechanics, animation, or deployment of a Three.js experience.
---

# Blender + React + Three.js 3D Builder

## Mission

Turn a visual brief into a working, inspectable 3D web experience. Use Blender for authored geometry and animation, React for the application shell and UI, and Three.js for runtime rendering and interaction. Preserve an existing project architecture when one exists; add a thin asset/runtime layer instead of replacing the project wholesale.

## Select the product mode

Choose one primary mode before implementation and keep the shared pipeline:

- Product viewer: hero model, orbit/pan/zoom, material or variant switching, hotspots, specifications and call-to-action.
- Architecture/interior: navigable rooms, floor/space labels, lighting presets, hotspots, measurements and camera waypoints.
- Digital exhibition: exhibit cards, guided tour, room transitions, audio/video captions, timeline and accessible information panels.
- 3D game: player controller, camera, entities, collision, interaction, state, HUD, save data and a deterministic test loop.
- 3D animation: authored GLB clips, `AnimationMixer`, timeline controls, camera choreography, subtitles and playback controls.

Load the matching details from [references/modes.md](references/modes.md). Load the quality gate from [references/quality-gate.md](references/quality-gate.md).

## Standard architecture

Use this boundary unless the repository dictates otherwise:

```text
React / TypeScript app shell
  |- UI panels, menus, accessibility and responsive layout
  `- 3DExperience component
       |- Three.js Scene / Camera / Renderer
       |- Asset registry and GLTFLoader
       |- Interaction controller
       |- Animation and visual effects
       `- Domain state (viewer, gallery, game or timeline)

Blender Python -> GLB assets -> public/assets/models -> Three.js runtime
```

Keep asset loading separate from scene assembly. Cache GLB promises by asset key, clone loaded scenes for repeated instances, and attach `AnimationMixer` only when clips exist. Store all scale, rotation, camera framing and interaction metadata in a registry rather than scattering magic numbers through components.

## Blender asset pipeline

1. Translate the brief into a model sheet: silhouette, scale, materials, camera angles, animation clips and interaction points.
2. Create or update procedural Blender Python builders where repeated geometry or variants exist. Use named objects and materials.
3. Apply transforms, set the intended origin, verify forward/up axes, and keep the model at a predictable world scale.
4. Add only the geometry needed for the viewing distance. Preserve high-value identity features such as eyes, mouth, limbs, openings, rooflines, furniture edges, product controls or signage.
5. Author clips with stable names such as `Idle`, `Walk`, `Open`, `Turntable` or `TourStep01`.
6. Export glTF 2.0 binary GLB with embedded resources. Keep filenames lowercase, stable and URL-safe.
7. Render a thumbnail or contact sheet in Blender before wiring the asset into the browser.

For character-like or branded forms, use reference images supplied by the user or legally usable references. Do not scrape or embed unlicensed source images into a public build.

## Three.js runtime rules

- Create one renderer, scene and primary camera per experience; dispose resources when switching scenes or unmounting.
- Prefer `MeshStandardMaterial` or `MeshPhysicalMaterial` with deliberate roughness, metalness and color management.
- Use one main light rig and named lighting presets; avoid stacking uncontrolled lights.
- Use `requestAnimationFrame` with a `Clock`; clamp large frame deltas after tab suspension.
- Update animation mixers, camera transitions and domain state from the frame loop.
- Use raycasting or explicit distance tests for interaction, depending on the mode.
- Use frustum or distance-based update throttling for distant entities.
- Cap `devicePixelRatio`; reduce antialiasing, shadows, particle count and animation frequency on low-power devices.
- Never hide a failed GLB load silently. Show a fallback mesh or UI error and log the asset key and URL.

## React integration rules

- Keep Three.js mutable objects in refs, not React state.
- Use React state for UI state, selected objects, filters, dialogs, modes and playback controls.
- Initialize the renderer in an effect and clean it up on unmount.
- Keep canvas overlay UI in ordinary DOM so it remains accessible and responsive.
- Give every interactive object a stable ID and a human-readable label.
- Add keyboard and pointer/touch equivalents for important interactions.
- For large asset collections, lazy-load thumbnails and load 3D assets on demand.

## Domain behavior

Implement the selected mode as a small state machine. At minimum define loading, ready and error states; active asset or exhibit/entity; camera mode and selected interaction target; animation or tour state; reset/replay behavior; and save/restore behavior if progress or configuration matters.

For game mode, add movement, collision, interaction, entity lifecycle, win/lose rules and deterministic capture or combat outcomes. For exhibition and architecture modes, add guided navigation, waypoints and a clear way back to the main view. For product mode, add model variants and a reset camera control. For animation mode, add play, pause, scrub, restart and clip selection.

## Required workflow

1. Inspect the repository, existing scripts, package manager, asset folders and deployment configuration.
2. Ask only for missing decisions that materially change the result; make safe visual defaults otherwise.
3. Write a brief asset and interaction plan before creating many models.
4. Build one representative asset and one representative interaction first.
5. Validate the asset in Blender and in the actual browser canvas.
6. Expand to the requested asset set, keeping registry names and scale consistent.
7. Add responsive UI and touch/keyboard controls.
8. Run lint, tests and production build.
9. Start the production-like local server and verify with a browser at the real route.
10. If deployment is in scope, package the exact built output, deploy it, and re-open the public URL in a fresh tab with a cache-busting query.
11. Report changed files, asset counts, tests, visual checks, known limitations and the final URL.

## Do not claim completion until

- the first viewport renders a visible scene rather than a blank canvas;
- every required GLB has a matching registry entry and a visible fallback/error path;
- the main interaction works with mouse and at least one keyboard or touch path;
- the camera can be reset;
- mobile layout does not cover the primary controls;
- assets have been visually checked from the intended camera;
- tests and production build pass;
- the deployed URL has been opened and checked if deployment was requested.

## Useful project conventions

Prefer names such as:

- `public/models/<asset>.glb`
- `public/model-thumbnails/<asset>.png`
- `src/3d/asset-registry.ts`
- `src/3d/create-experience.ts`
- `src/3d/interaction-controller.ts`
- `tools/build_<project>_models.py`
- `tests/3d-assets.test.mjs`

When the existing project is a standalone HTML game, keep its working entry point and add the registry, asset cache, versioned URLs, fallback loaders and tests incrementally.
