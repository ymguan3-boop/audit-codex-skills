# 3D Builder Mode Recipes

Use one recipe as the primary domain contract. Combine recipes only when the user explicitly asks for a hybrid experience.

## Product showcase

### Runtime

- Start with a framed hero model and a camera reset button.
- Support orbit, pan and zoom with pointer and touch controls.
- Add a variant/material registry instead of duplicating scene code.
- Add hotspots with labels, camera targets and product specifications.
- Keep the model visible during asset loading with a low-cost placeholder.

### Acceptance

- Model is recognizable in the first viewport.
- Orbit never lets the camera pass through the model or lose it permanently.
- Variant changes do not reload the entire application.
- The page remains useful when WebGL or a model load fails.

## Architecture and interior

### Runtime

- Use a scene graph grouped by building, floor, room and object.
- Define named camera waypoints for entrances, rooms and detail views.
- Use lighting presets such as daylight, warm interior and night.
- Add floor/room labels, material legend, hotspots and optional measurement helpers.
- Prefer collision volumes or navigation zones over mesh-level physics.

### Acceptance

- Users can return to the entrance or overview from every room.
- Furniture, doors, windows and circulation paths remain readable at the intended camera distance.
- Large scenes use distance-based loading or update throttling.

## Digital exhibition

### Runtime

- Represent each exhibit as `{ id, title, model, description, media, cameraTarget }`.
- Provide a gallery index, selected-exhibit panel and next/previous navigation.
- Add a guided tour state with named steps, progress and replay.
- Keep captions and descriptions in DOM, not only inside the canvas.
- Allow audio/video to be muted, paused and restarted.

### Acceptance

- Every exhibit is reachable from the index and has a visible title.
- Guided tour can be paused, resumed and restarted.
- Keyboard navigation and reduced-motion preferences are respected.

## 3D game

### Runtime

- Define explicit game modes such as `world`, `challenge`, `capture`, `menu` and `result`.
- Keep player, entities, collision volumes, rewards and save data in separate state domains.
- Use an asset registry and shared GLB cache for all repeated characters.
- Update distant AI and mixers less often than nearby entities.
- Add a restart/reset path that clears transient state without corrupting saved data.

### Acceptance

- Player can move with keyboard and touch, lock a target, interact, and recover from a failed action.
- Collision prevents leaving the intended play area or walking through required obstacles.
- Win/lose and reward rules are deterministic enough to test.
- HUD communicates current mode, objective, inventory and progress.

## 3D animation

### Runtime

- Store clip names and durations in an animation registry.
- Use `AnimationMixer` and a single clock-driven update path.
- Add play, pause, restart, scrub and clip selection controls.
- Use camera keyframes or scripted camera targets for presentation shots.
- Support a thumbnail or poster frame while the scene loads.

### Acceptance

- Playback controls do not create duplicate mixers or animation loops.
- Scrubbing and restarting produce the same visual state every time.
- A missing clip falls back to a visible static pose and a clear message.
