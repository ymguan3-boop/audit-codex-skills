# GitHub MCP 執行協定

只有在以下條件都成立後才使用本協定：

1. 已解析出有效的 `geolibre_profile`；
2. 使用者已明確確認最終分析規格。

## 動態執行目標

不得把 repository 硬編碼在技能中。

應從正式 profile 解析：

- `repo_full_name`
- `default_branch`
- `source_path`
- `web_root`
- `analysis_root`
- `task_script_root`
- `task_manifest_path`
- `pages_url`

使用已連線的 GitHub MCP／工具處理 repository metadata、檔案讀寫、commit，以及 workflow／log 檢查。

## 每個任務的路徑

建立穩定的 `task_id`，例如：

`yilan-traffic-accident-safety-2026-09`

任務程式：

`<task_script_root>/<task_id>.py`

觸發 manifest：

`<task_manifest_path>`

若較舊的 profile 沒有 `task_manifest_path`，則從 `web_root` 推導為
`<web_root>/tasks/current-task.json`。只有在 `web_root` 也不存在時，
才可退回使用舊路徑 `<source_path>/GeoLibre-Web/tasks/current-task.json`。

輸出目錄：

`<analysis_root>/<task_id>/`

通用 workflow 目標：

`.github/workflows/geolibre-analysis.yml`

若不存在，使用目前技能提供的通用分析 workflow asset 建立，或產生具備相同功能且能讀取 profile 的 workflow。

## Manifest 結構

```json
{
  "enabled": true,
  "task_id": "<task_id>",
  "execution_mode": "analysis",
  "script": "<resolved task script path>",
  "topic": "<topic>",
  "goal": "<analysis_goal>",
  "confirmed_spec": {
    "geographic_scope": "...",
    "time_range": "...",
    "input_layers": [],
    "spatial_rules": [],
    "thresholds": {},
    "filters": {},
    "outputs": []
  }
}
```

Manifest 是分析執行的觸發器。**必須最後才寫入或更新。**

`execution_mode`：

- `analysis`（預設）：執行 GIS 任務程式、最佳化、驗證並發布。
- `postprocess_only`：重用既有成果，只執行最佳化、驗證與發布。適用於樣式調整、外部化、手機效能修正或重新發布，而且分析條件／資料沒有變更的情況。不要只是為了改變呈現方式，就重新執行昂貴的 GIS 計算。

## 任務程式要求

產生的 Python 程式必須：

1. 讀取已解析的 task manifest。
2. 確認 manifest 的 `task_id` 與目前任務一致。
3. 僅取得／載入使用者已確認的資料來源。
4. 明確處理 CRS。
5. 完整套用已確認的空間規則與門檻。
6. 在輸出 metadata／report 中保留資料來源與處理脈絡。
7. 只把成果寫入 `<analysis_root>/<task_id>/`。
8. 不得修改與本任務無關的其他成果資料夾。
9. 若任何必要判斷條件無法評估，必須明確失敗，不可默默跳過。
10. 任何已允許的替代資料或替代方法，都必須記錄在 `report.md` 與 `summary.json`。
11. 遵循 `performance-and-publishing.md`。
12. 若完整結果超過 2,000 個 features 或 5 MiB，建立輕量的 `overview.geojson` 作為預設地圖顯示內容，並保留 `result.geojson` 作為完整正式成果。
13. 對非小型顯示圖層，優先在 `source.data` 使用 URL-backed GeoJSON；不要再於頂層 `geojson` 重複放入相同 FeatureCollection。
14. 除非使用者明確要求，預設可見的專題圖層不得超過 3 個。

臺灣需要以公尺進行距離或面積計算時，適用情況下優先使用合適的本地投影 CRS，
例如 TWD97 / TM2（臺灣 121 分帶可使用 EPSG:3826），之後再將 GeoLibre 顯示用幾何轉為 EPSG:4326。

## 資料來源優先順序

依序優先使用：

1. 使用者既有 GeoLibre 專案內已驗證的資料來源；
2. 主管機關正式、免費且公開的政府 GIS／開放資料；
3. 可信賴的開放資料，例如 OpenStreetMap；
4. 使用者提供的檔案。

未經使用者明確同意，不得自行加入付費服務或需要秘密 API 憑證的資料來源。

## MCP 寫入順序

1. 重新驗證已綁定的 repository 與正式 profile。
2. 讀取安全整合所需的既有任務／workflow 檔案。
3. 建立或更新 `<task_script_root>/<task_id>.py`。
4. 確認技能 asset 中的 `.geolibre/tools/optimize-project.py` 已存在，並確認能讀取 profile 的 `.github/workflows/geolibre-analysis.yml` 會在分析後呼叫它。
5. 程式完成後，才建立或更新解析後的 `current-task.json`。
6. 讓 manifest 的 commit 觸發 Action。若只有成果呈現／效能調整，使用 `postprocess_only`；若資料、條件、門檻、計算或要求輸出有任何變更，使用 `analysis`。
7. 可取得時，檢查 Action 執行結果與 logs。
8. 讀回並驗證產生的成果。
9. 適用時，從使用者既有的 Pages 部署發布或連結成果，不要因此替換 GeoLibre 本體。

**不要先更新 manifest。**

## 完成前檢查

適用時，必須具備以下成果：

- `map.geolibre.json`
- 大型結果規則適用時的 `overview.geojson`
- `result.geojson`
- `result.csv`
- 適合表格化時的 `result.xlsx`
- `report.md`
- `summary.json`
- `performance.json`

檢查內容：

- `summary.json`：結果筆數與資料來源註記；
- `report.md`：判斷條件、資料來源、限制與替代處理；
- map project：預期的結果圖層是否可見；
- `performance.json`：project bytes、inline layer bytes 與 initial-load budget。

若 `mobile_hard_budget_ok` 為 false，不得宣告任務完成。應在不改變已確認分析條件的前提下，
重新產生更小的預設 overview 地圖。

最終回覆應包含：

- 任務名稱；
- 已綁定 repo；
- 實際採用的分析條件；
- 結果筆數；
- 資料來源；
- 限制與替代處理；
- GitHub 檔案連結／路徑；
- 可用時提供 Pages URL 或 GeoLibre URL。

所有成果驗證完成前，不得宣稱「分析完成」。
