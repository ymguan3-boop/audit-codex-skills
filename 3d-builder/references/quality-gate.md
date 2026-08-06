# 3D Experience Quality Gate

Run this checklist before reporting completion.

## Asset integrity

- [ ] Every requested asset has a stable registry key.
- [ ] Every registry key resolves to a GLB or an intentional procedural fallback.
- [ ] GLB axes, origin, scale and forward direction are verified in Blender and in the browser.
- [ ] Materials have deliberate color, roughness and metalness values.
- [ ] Required animation clips exist and are named consistently.
- [ ] Thumbnails match the actual browser models.

## Visual quality

- [ ] The first viewport shows a clear subject and useful camera framing.
- [ ] Important identity features are visible from the intended camera.
- [ ] Lighting does not wash out colors or create a black scene.
- [ ] Background, floor and subject have sufficient contrast.
- [ ] Mobile portrait and desktop landscape layouts are checked.
- [ ] Loading, empty and error states are visible and understandable.

## Interaction

- [ ] Camera reset works.
- [ ] Pointer/mouse interaction works.
- [ ] Keyboard or touch interaction works.
- [ ] Focusable controls have labels and visible active states.
- [ ] Guided navigation or game state always has a way back.
- [ ] Audio starts only after user interaction and can be muted.

## Performance

- [ ] GLBs are cached and not repeatedly downloaded.
- [ ] Repeated instances clone cached scenes instead of reloading assets.
- [ ] Pixel ratio is capped.
- [ ] Shadows, antialiasing, particles and mixer updates have a low-power path.
- [ ] Distant objects do not run full-frequency AI or animation updates.
- [ ] Renderer and geometries are disposed when changing experiences.

## Verification

- [ ] Lint passes.
- [ ] Unit or asset tests pass.
- [ ] Production build passes.
- [ ] Local production-like server renders the intended route.
- [ ] Browser verification checks the visible canvas, controls and console errors.
- [ ] If deployed, a fresh browser tab checks the public URL with a cache-busting query.
