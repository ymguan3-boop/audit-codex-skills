# Runtime Character Regression Gate

Apply this low-freedom gate to rigged characters, animated creatures, props with release events, and any Blender asset delivered through GLB/glTF. Its purpose is to stop an approved model from becoming visually or mechanically worse during retopology, decimation, rigging, animation, material conversion, or export.

## 1. Freeze evidence before conversion

1. Record the exact approved `.blend`, reference image, preview sheet, polygon profile, displayed colors, feature checklist, units, axes, and forward direction.
2. Make runtime work in a new versioned directory. Never overwrite the high master, approved preview, or rejected evidence.
3. Render a baseline front, three-quarter, side, back, head close-up, garment/shoe close-up, and neutral pose using fixed camera and lighting.
4. Mark subjective approval separately for static appearance, rig deformation, and each important action.

## 2. Preserve material appearance through GLB

- Assume Blender procedural node graphs, Generated coordinates, viewport display colors, and Workbench shading may not survive glTF export identically.
- Prefer glTF-compatible Principled BSDF materials with UV-backed, packed textures for critical color regions. Bake procedural materials when exact appearance matters.
- Never conclude that a color matches because the source RGB or hex value matches. Color management, view transform, lighting, and viewer shading can make the same input appear white, black, or differently saturated.
- Compare approved and runtime outputs with equivalent camera, lighting, exposure, and display transform. Sample the displayed reference when necessary, then verify the cleanly re-imported GLB and the real target runtime.
- Ensure every runtime material has the expected image, UV map, channel packing, alpha mode, and texture embedding. Missing node export or diffuse fallback is a rejection, not a cosmetic note.
- Do not assign a diagonal or curved color boundary after decimation by polygon-center classification; it creates jagged fringe triangles. Preserve a UV/texture boundary, authored topology seam, or mask before decimation.

## 3. Preserve topology and attachments

- Retain the accepted high master; produce LOD0 and lower LODs as derivatives.
- Inspect decimation around the face, silhouette, hands, collars, diagonal garment regions, joints, and identity features. Triangle budget compliance does not excuse a visible regression.
- Use progressive torso weights across pelvis, spine, and chest for long shirts or coats. Rigidly weighting the whole garment to the chest commonly opens the hem during torso rotation.
- Inspect windup, release, follow-through, crouch, stride, and other extreme poses for body/garment gaps, floating badges or collars, head/neck separation, ankle/shoe disconnection, and elbow/knee collapse.
- Smooth deforming joints; use rigid weights only for genuinely rigid pieces such as certain shoes, props, or armor.

## 4. Prove motion rather than clip metadata

1. Declare the asset's world-space forward and up axes.
2. Render action-revealing front and three-quarter views; add a side view when foreshortening hides the active limb.
3. Measure relevant bones, vertices, and props in world space at key frames. Do not infer world motion from pose-bone local channels: bone orientation can map local Y or Z to unexpected world axes.
4. Verify each action's visible phases. A forceful forward throw normally needs anticipation, rear-foot push or weight transfer, pelvis/chest rotation, shoulder acceleration, elbow extension, wrist snap, forward projectile travel, follow-through, and recovery.
5. For a held/released prop, verify the held copy is visible before release, the projectile copy becomes visible at release, and the projectile travels forward after release. Measure the actual displacement; do not accept only keyed scale or a named release frame.
6. Keep locomotion in-place when game code owns translation, and verify root drift is within the declared tolerance.

Use measurements as evidence, not universal aesthetic thresholds. Every new asset needs scale-appropriate targets and visual review.

## 5. Make Blender automation fail loudly

- Run a small compatibility probe before a long build. Blender APIs change; for example, code that assumes legacy `Action.fcurves` access can fail on newer action-layer/slot APIs.
- Render PNG frames when the Blender build lacks the required FFmpeg output support, then encode externally.
- Treat Blender exit code 0 as insufficient. Scan stdout/stderr for `Traceback`, require an explicit success sentinel, and verify every expected `.blend`, GLB, image, report, and frame count.
- Add resumable frame generation for long renders, but isolate outputs by version and expected frame range. Stale frames from an older 48-frame clip must never enter a newer 40-frame GIF or video.
- Reuse unchanged renders only after confirming the source hash, camera, material, clip version, frame range, and render settings match.

## 6. Clean re-import acceptance

Open the exported GLB in a fresh Blender scene or the intended runtime and record:

- evaluated triangles, mesh count, armature count, bones, clips, durations, units, axes, and bounding box;
- material, image, UV, texture-embedding, alpha, and displayed-color checks;
- actual vertex/bone displacement for required joints;
- prop visibility/release state and world-space trajectory when applicable;
- screenshots of neutral, extreme deformation, and key action phases;
- comparison against the approved master from matched views.

Do not accept `export completed`, file existence, clip-name presence, or clean import as proof of visual fidelity or usable animation.

## 7. Reject, quarantine, and recover

When any required check fails:

1. Set the affected artifact to `REJECTED_ART_QUALITY`, `REJECTED_DEFORMATION`, or another explicit rejected status.
2. Set delivery approval to false and block the file from runtime/game integration.
3. Preserve it in a versioned folder containing `REJECTED-NOT-FOR-DELIVERY.md`, the failed source/GLB, previews, measurements, and the reason.
4. Repair from the last approved master or derivative; never silently patch and overwrite rejected evidence.
5. Re-run clean export, re-import, matched-view comparison, deformation measurement, and user review as required.

Only report `VERIFIED` when technical structure, runtime appearance, required deformation/actions, and the applicable art/user approval all pass.
