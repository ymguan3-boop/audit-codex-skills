---
name: 3d-builder
description: 混合建模技能 — Blender 精確建模 + Hunyuan3D-2 AI 生成。適用於：產品展示、建築/室內、數位展覽、3D 遊戲、3D 動畫。說「3D 建模」「做 3D」「建立 3D 場景」「 Blender 建模」「3d-builder」時載入。
---

# 3D Builder（Blender + Hunyuan3D-2 混合建模）

## Mission

將視覺簡報轉化為可互動的 3D 網頁體驗。採用**混合建模策略**：Blender 負責精確結構，Hunyuan3D-2 負責有機/複雜物件，結合兩者優勢加速產出。

## 混合建模策略

### 物件分類決策樹

對需求中的每個建模物件，依以下決策樹分類：

```
物件描述
  │
  ├─ 結構性物件（建築主體、牆、柱、樓板、門窗、樓梯、電梯、道路）
  │   → Blender Python 精確建模
  │   理由：需精確尺寸、對齊、可編輯幾何
  │
  ├─ 有機/複雜形狀（雕塑、裝置藝術、植物、人物、地形）
  │   → Hunyuan3D-2 文字生成
  │   理由：AI 擅長複雜曲面，手建耗時
  │
  ├─ 家具/設備（桌椅、櫃子、電腦、車輛、燈具）
  │   → Hunyuan3D-2 圖像或文字生成
  │   理由：標準物件 AI 生成快，品質足夠
  │
  └─ 場景環境（天空、草地、水面）
      → Blender Python 或 Three.js Shader
      理由：簡單幾何或程式化生成即可
```

### 建模流程

```
1. 分析需求 → 自動分類物件清單
2. 結構件 → Blender Python 建模 → 匯出 GLB
3. 裝飾件 → Hunyuan3D-2 生成 → 輸入 Blender → 調整尺寸/位置 → 匯出 GLB
4. 全部 GLB 併入 Three.js 場景
5. 驗證尺寸、位置、材質一致性
```

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

Blender Python -> GLB assets -> public/models -> Three.js runtime
Hunyuan3D-2 -> GLB/OBJ -> Blender adjust -> public/models -> Three.js runtime
```

## Hunyuan3D-2 工作流

### 何時使用 Hunyuan3D-2

- 需要複雜有機形狀（雕塑、裝置藝術）
- 需要標準家具/設備（桌子、椅子、電腦）
- 需要人物或角色模型
- 時間有限，AI 生成比手建快 10 倍以上

### 文字生成流程

```
使用 blender-mcp_generate_hunyuan3d_model 工具：
  text_prompt: "一張現代辦公桌，白色桌面，金屬支架，簡約設計"
  → 等待 job_id 完成
  → 使用 blender-mcp_import_generated_asset_hunyuan 輸入 Blender
  → 調整 scale、position、rotation
  → 匯出 GLB
```

### 圖像生成流程

```
使用 blender-mcp_generate_hunyuan3d_model 工具：
  input_image_url: "路徑或URL"
  → 等待完成
  → 輸入 Blender 調整
  → 匯出 GLB
```

### Blender 精確建模流程

```
1. 建立 Python 腳本（使用 bpy）
2. 定義尺寸、位置、材質
3. 套用 transform、設定 origin
4. 匯出 GLB（export_apply=True）
5. 在瀏覽器驗證
```

## Blender asset pipeline

1. Translate the brief into a model sheet: silhouette, scale, materials, camera angles, animation clips and interaction points.
2. Use the object classifier to split items into Blender vs Hunyuan3D-2.
3. Create Blender Python builders for structural elements.
4. Generate decorative elements with Hunyuan3D-2.
5. Import generated assets into Blender, adjust scale/position/rotation.
6. Apply transforms, set the intended origin, verify forward/up axes.
7. Export glTF 2.0 binary GLB with embedded resources.
8. Render a thumbnail in Blender before wiring into the browser.

## Three.js runtime rules

- Create one renderer, scene and primary camera per experience; dispose resources when switching scenes or unmounting.
- Prefer `MeshStandardMaterial` or `MeshPhysicalMaterial` with deliberate roughness, metalness and color management.
- Use one main light rig and named lighting presets; avoid stacking uncontrolled lights.
- Use `requestAnimationFrame` with a `Clock`; clamp large frame deltas after tab suspension.
- Use raycasting or explicit distance tests for interaction, depending on the mode.
- Cap `devicePixelRatio`; reduce antialiasing, shadows, particle count and animation frequency on low-power devices.
- Never hide a failed GLB load silently. Show a fallback mesh or UI error and log the asset key and URL.

## React integration rules

- Keep Three.js mutable objects in refs, not React state.
- Use React state for UI state, selected objects, filters, dialogs, modes and playback controls.
- Initialize the renderer in an effect and clean it up on unmount.
- Keep canvas overlay UI in ordinary DOM so it remains accessible and responsive.
- Give every interactive object a stable ID and a human-readable label.
- Add keyboard and pointer/touch equivalents for important interactions.

## Required workflow

1. Inspect the repository, existing scripts, package manager, asset folders and deployment configuration.
2. Ask only for missing decisions that materially change the result; make safe visual defaults otherwise.
3. Write a brief asset and interaction plan before creating many models.
4. Classify all objects using the decision tree (Blender vs Hunyuan3D-2).
5. Build one representative structural asset first.
6. Generate one representative decorative asset with Hunyuan3D-2.
7. Validate both in Blender and in the actual browser canvas.
8. Expand to the full asset set, keeping registry names and scale consistent.
9. Add responsive UI and touch/keyboard controls.
10. Run lint, tests and production build.
11. Start the production-like local server and verify with a browser at the real route.
12. Report changed files, asset counts, tests, visual checks, known limitations and the final URL.

## Do not claim completion until

- the first viewport renders a visible scene rather than a blank canvas;
- every required GLB has a matching registry entry and a visible fallback/error path;
- Hunyuan3D-2 generated assets are properly scaled and positioned in Blender;
- the main interaction works with mouse and at least one keyboard or touch path;
- the camera can be reset;
- mobile layout does not cover the primary controls;
- assets have been visually checked from the intended camera;
- tests and production build pass.

## Useful project conventions

Prefer names such as:

- `public/models/<asset>.glb`
- `public/model-thumbnails/<asset>.png`
- `src/3d/asset-registry.ts`
- `src/3d/create-experience.ts`
- `src/3d/interaction-controller.ts`
- `tools/build_<project>_models.py`
- `tests/3d-assets.test.mjs`
