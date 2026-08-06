# 3D Builder Mode Recipes

Use one recipe as the primary domain contract. Combine recipes only when the user explicitly asks for a hybrid experience.

## Hunyuan3D-2 工作流（所有模式通用）

### 物件分類

在開始建模前，先將所有物件分類：

| 分類 | 工具 | 範例 |
|------|------|------|
| 結構性物件 | Blender Python | 牆、柱、樓板、門窗、楼梯 |
| 有機/複雜形狀 | Hunyuan3D-2 | 雕塑、裝置藝術、植物 |
| 家具/設備 | Hunyuan3D-2 | 桌椅、電腦、車輛 |
| 場景環境 | Blender/Shader | 天空、草地、道路 |

### Hunyuan3D-2 生成步驟

1. **文字描述** → `blender-mcp_generate_hunyuan3d_model(text_prompt="...")`
2. **等待完成** → `blender-mcp_poll_hunyuan_job_status(job_id)`
3. **匯入 Blender** → `blender-mcp_import_generated_asset_hunyuan(name, zip_file_url)`
4. **調整** → scale、position、rotation 對齊場景
5. **匯出** → GLB with `export_apply=True`

### Blender 精確建模步驟

1. **Python 腳本** → `bpy.ops.mesh.primitive_cube_add()` 等
2. **定義材質** → `bpy.data.materials.new()` + nodes
3. **套用 transform** → `obj.scale = (x, y, z)` + `bpy.ops.object.transform_apply(scale=True)`
4. **匯出 GLB** → `bpy.ops.export_scene.gltf(export_apply=True)`

### 品質檢查（混合建模）

- [ ] Blender 結構件尺寸精確，對齊正確
- [ ] Hunyuan3D-2 生成件比例合理，無破面
- [ ] 所有 GLB 在瀏覽器中正確載入
- [ ] 材質顏色、roughness、metalness 一致
- [ ] 無重複或遺漏的物件

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
