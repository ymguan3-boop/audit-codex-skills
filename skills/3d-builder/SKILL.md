---
name: 3d-builder
description: Build, integrate, and verify low-poly or high-poly 3D assets and interactive experiences with Blender, Blender Python, Hunyuan3D or other AI 3D generators, and Three.js/React. Use for 3D modeling, product viewers, architecture/interiors, exhibitions, browser games, animated scenes, GLB/glTF pipelines, procedural geometry, or requests such as「3D 建模」「高模」「低模」「做 3D」「Blender 建模」「Hunyuan3D」「3d-builder」. Before modeling, resolve the polygon profile and any approved visual baseline, require representative art approval before batch expansion, keep technical validation separate from visual approval, check local/MCP capabilities, disclose hosted-generation quota/privacy risks, and obtain consent before installing tools or using hosted or paid services.
---

# 3D Builder

Turn a visual brief into inspectable 3D assets or a working 3D experience. Select tools by geometry, precision, topology, animation, runtime, cost, licensing, and the capabilities actually available in the current environment.

## Mandatory polygon-profile gate

Before every modeling task, resolve one of these profiles: `low-poly`, `high-poly master`, or `high-poly master + game LODs`. Ask the user when the prompt does not already make the choice explicit. Do not begin final modeling while the profile is unresolved.

Read [references/polygon-profiles.md](references/polygon-profiles.md), state the selected profile and measurable triangle/texture targets, and write them into the asset registry. A high triangle count alone is not evidence of high-quality modeling: require silhouette refinement, purposeful secondary forms, clean curvature, and close-up renders. Never relabel a mechanically subdivided low-detail mesh as a completed high-poly redesign.

## Mandatory visual-baseline and batch gate

Before modeling, inspect the task and repository for user-approved examples, earlier accepted pilots, reference sheets, and rejected versions. Treat an approved example as the minimum art-quality baseline even when it has fewer polygons. Record its exact file or image in the asset registry; never silently replace it with a higher-count but lower-information mesh.

Read [references/user-approved-baselines.md](references/user-approved-baselines.md) before every modeling task. Apply the recorded V3 baseline as the user's persistent minimum design-rigor standard, while adapting polygon count, topology, rigging, animation, and literal style to the requested asset type.

For any reference-driven character, creature, product hero, or batch of related assets, read and apply [references/art-quality-gate.md](references/art-quality-gate.md). Build one representative asset per anatomy/topology pathway and create a side-by-side sheet containing the reference, approved baseline when present, candidate views, and deformation evidence. Obtain explicit user visual approval before expanding beyond the representative pilot when fidelity is subjective, a previous attempt was rejected, or the batch contains materially different anatomy. Technical success does not authorize batch expansion.

## Mandatory runtime-character regression gate

For any character or deforming asset, and for any asset whose final delivery is GLB/glTF, read and apply [references/runtime-character-regression-gate.md](references/runtime-character-regression-gate.md). Treat rigging, decimation, material conversion, animation, export, and re-import as appearance-changing operations.

- Freeze the user-approved visual source as an immutable master. Build runtime derivatives in versioned folders; never overwrite the master or a rejected candidate.
- Compare the cleanly re-imported GLB against the approved render for silhouette, proportions, garment connections, material colors, and feature placement. A correct Blender viewport is not sufficient.
- Verify motion with world-space measurements and representative frames. Clip names, keyframe counts, bone counts, and exporter success are only structural evidence.
- Inspect extreme poses for clothing/skin gaps, detached collars, head/neck separation, shoes leaving ankles, collapsed joints, and projectile/prop release errors.
- Quarantine every rejected version with a visible `REJECTED-NOT-FOR-DELIVERY` marker and remove it from integration paths. Keep the evidence for regression comparison.
- Keep `TECHNICAL_PASS` separate from `ART_REVIEW_PENDING` or animation approval. Do not claim final delivery until both appearance and deformation pass after re-import.

## First-load environment gate

Run this gate before the first modeling task in an environment and repeat it when tools or configuration may have changed.

1. Inspect the current callable-tool catalog for Blender control, AI 3D generation, job polling, generated-asset import, image generation, and browser verification capabilities. Match capabilities, not assumed tool names.
2. Run `python scripts/check_environment.py --pretty` when shell access is available. The script cannot inspect Codex's MCP catalog; combine its result with step 1.
3. Classify every requirement as `ready`, `optional-missing`, or `required-missing`.
4. On the first invocation, if no related Blender-control or AI-3D MCP capability is present, always report the gap and ask whether the user wants the recommended MCP path installed before modeling. Follow [references/mcp-setup.md](references/mcp-setup.md) and pause for the answer even when a local fallback exists.
5. Never install, download models, connect a paid service, or change MCP configuration without explicit user consent. After consent, use the current official installation method, verify the capability is callable, and run a harmless health check.
6. If the user declines or installation cannot be verified, record that decision for the task and continue with the best Blender/Three.js fallback. Do not repeatedly ask during the same task unless requirements change.

Skills do not receive a reliable post-install execution hook. Treat the first invocation of this skill as its setup check; never claim that installation alone ran the gate.

## Required preflight recommendation

Before creating assets:

1. Parse the brief into individually named objects, environments, interactions, clips, and output targets.
2. Resolve the mandatory polygon profile and measurable budgets.
3. Apply [references/tool-selection.md](references/tool-selection.md) to each item.
4. Present a compact recommendation containing: object/group, polygon profile, proposed tool, reason, important tradeoff, dependency or likely cost, and fallback.
5. Continue automatically after the recommendation when the user already requested execution and the choice is local, reversible, and cost-free. This never bypasses the first-load MCP consent gate. Pause for confirmation when the choice introduces installation, download, cloud/API cost, licensing exposure, credential setup, destructive conversion, or a material fidelity/schedule tradeoff.
6. Honor a user override unless it is infeasible or unsafe; explain the concrete limitation when declining it.

Do not use Hunyuan3D merely because it is available. Do not use Blender for runtime-only effects that are simpler and better in Three.js.

## Select the product mode

Choose one primary mode and load its contract from [references/modes.md](references/modes.md):

- Product viewer
- Architecture/interior
- Digital exhibition
- 3D game
- 3D animation
- Asset-only delivery

Combine modes only when the brief genuinely requires a hybrid.

## Standard architecture

Preserve an existing project architecture after inspecting it. Never claim a framework or runtime already exists without evidence. Add a thin asset/runtime layer instead of replacing the project wholesale.

```text
Blender / Blender Python -----------\
AI 3D generator -> Blender cleanup --+-> GLB registry -> Three.js runtime
Three.js procedural geometry -------/                   -> React/DOM UI
```

Keep asset loading separate from scene assembly. Cache GLB promises by stable asset key, clone cached scenes for repeated instances, attach `AnimationMixer` only when clips exist, and keep scale, rotation, framing, licensing/source, and interaction metadata in the registry.

## Modeling rules

### Blender and Blender Python

- Use exact world units, named objects/materials, predictable origins, applied transforms, and verified forward/up axes.
- Prefer procedural builders for repeated, dimensioned, configurable, or structural geometry.
- Preserve identity features while matching polygon density to the intended camera distance.
- Use stable clip names such as `Idle`, `Walk`, `Open`, `Turntable`, and `TourStep01`.
- Export embedded glTF 2.0 binary GLB with stable lowercase URL-safe filenames.
- Render a thumbnail or contact sheet before browser integration.
- Match rig complexity to anatomy and required deformation. Validate the actual shoulder/elbow/wrist, hip/knee/ankle, spine, head, tail, wing, fin, or equivalent joints; a clip count alone is not rig validation.

### AI-generated 3D assets

- Use an available AI generator for organic, irregular, decorative, or rapid concept assets only when its speed outweighs topology and precision risks.
- Record provider/model, prompt or source image, license constraints, and generation settings in asset metadata.
- Import every generated mesh into Blender for scale, orientation, topology, normals, UV, material, and animation-readiness checks.
- Retopologize, decimate, repair, or reject defective meshes; never treat successful generation as production readiness.
- Never send confidential or unlicensed reference imagery to a hosted service without authorization.
- When Hunyuan3D uses a Hugging Face Space, say so before upload or generation. Disclose that the Space may require sign-in, queue on shared ZeroGPU, enforce a rolling or daily quota (often described as a 24-hour limit), change limits without notice, or stop mid-batch when quota is exhausted. Never promise a fixed free allowance or uninterrupted completion.
- Obtain explicit consent before sending images to Hugging Face. Record the Space/revision, generation time, job result, and any displayed quota/reset message. Preserve successful raw outputs locally after each job so a later quota interruption does not erase completed work.
- For batches, run one representative job first, then checkpoint every asset. If quota is exhausted, stop hosted requests, report completed and remaining asset IDs, the displayed reset estimate when available, and continue only with an authorized local Blender fallback or after the service recovers.

### Three.js runtime

- Use one renderer, scene, and primary camera per experience; dispose resources on scene changes and unmount.
- Prefer standard/physical materials with deliberate color management, roughness, and metalness.
- Use a single clock-driven frame loop; clamp large deltas after tab suspension.
- Update animation mixers, camera transitions, and domain state from the frame loop.
- Use raycasting or explicit distance tests for interaction; throttle distant entities.
- Cap device pixel ratio and provide low-power paths for shadows, antialiasing, particles, AI, and animation.
- Show a fallback mesh or visible error when an asset fails to load.

### React integration

- Keep mutable Three.js objects in refs and UI/domain state in React state.
- Keep overlay controls in accessible DOM with pointer, keyboard, and touch equivalents.
- Lazy-load large asset collections and thumbnails.
- Implement loading, ready, and error states plus reset/replay and save/restore when progress matters.

## Execution workflow

1. Inspect the repository, scripts, package manager, asset folders, existing changes, and deployment configuration.
2. Run the environment gate, resolve low-poly versus high-poly delivery, and deliver the preflight recommendation.
3. Resolve only decisions that materially affect scope, cost, safety, licensing, or fidelity.
4. Write the asset registry, approved visual baseline, art criteria, and interaction plan before generating many assets.
5. Build one representative asset per selected modeling and anatomy/topology pathway.
6. Separate technical status from art status, produce the side-by-side evidence sheet, and obtain required visual approval before batch expansion.
7. For rigged or GLB-delivered assets, freeze the approved master and run the runtime-character regression gate on a versioned derivative before wider production.
8. Expand only approved pathways with consistent naming, scale, source metadata, checkpoints, and fallbacks.
9. Add responsive UI and pointer plus keyboard or touch controls.
10. Run asset tests, lint, unit tests, and the production build.
11. Start a production-like local server and verify the real route, visible canvas, controls, and console.
12. If deployment is requested, deploy the exact built output and re-open the public URL in a fresh cache-busted tab.
13. Run [references/quality-gate.md](references/quality-gate.md) and report files, asset counts, per-asset evaluated triangle counts, polygon profile, approved baseline, technical status, art-approval status, selected tools, generated-versus-authored assets, tests, visual checks, limitations, hosted quota events, costs incurred, and final URL.

Never map `TECHNICAL_PASS` or a successful GLB import to `VERIFIED`. Claim completion only after both technical and art-quality gates pass, required user approval is recorded, and every failed item is reported explicitly. If later evidence disproves a completion claim, revoke it immediately and follow the rejection procedure in [references/art-quality-gate.md](references/art-quality-gate.md).
