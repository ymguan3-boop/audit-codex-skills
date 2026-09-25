# GeoLibre 效能與發布規則

除非使用者明確要求完全 self-contained 的 project file，所有分析成果都套用本規則。

## 目標

預設 `map.geolibre.json` 是**互動式瀏覽入口**，不是整個分析資料集的容器。

完整、高保真分析資料應保留在 `result.geojson`、CSV／XLSX 或其他專用成果檔中。
預設地圖應維持輕量。

## 預設效能預算

- `map.geolibre.json` 目標：**<= 2 MiB**
- `map.geolibre.json` 硬性上限：**5 MiB**
- 每個 layer 的 inline GeoJSON 最大 payload：**256 KiB**
- 初始載入 soft budget（project + 可見 external GeoJSON）：**6 MiB**
- 初始載入 hard budget：**12 MiB**
- 大型結果門檻：`result.geojson` **超過 2,000 個 features 或 5 MiB**

以上是 GitHub Pages／手機使用情境的操作預設值，不是 GeoLibre 格式本身的限制。

## 使用 URL-backed GeoJSON

不可預設所有 GeoLibre 部署版本都支援在 `source.data` 使用遠端 GeoJSON URL。**若目前綁定的自架 GeoLibre 尚未有明確、已驗證成功的 URL-backed 相容性紀錄，預設必須使用 inline GeoJSON：`source: {"type":"geojson"}` 搭配 layer 頂層 `geojson: FeatureCollection`。** 不得僅因為檔案較小或 optimizer 支援外部化，就自行改成 `source.data`。

只有在目標 Pages 已用瀏覽器驗證過 URL-backed 圖層「圖層面板可見且地圖上確實畫出圖徵」後，才可使用 `source.data`。某些版本即使顯示 `ready` 仍會忽略此格式。

GeoJSON 樣式欄位亦必須沿用目前部署版本已驗證的 schema。對點／面 GeoJSON，優先使用 `fillColor`、`fillOpacity`、`strokeColor`、`strokeWidth`、`circleRadius`；不得自行改用尚未驗證的 `circleColor`、`circleStrokeColor`、`circleStrokeWidth`。

目標部署通過相容性測試時，大型圖層可使用：

```json
{
  "id": "risk-overview",
  "name": "高風險摘要",
  "type": "geojson",
  "source": {
    "type": "geojson",
    "data": "https://user.github.io/repo/GeoLibre-Web/analysis/task/overview.geojson"
  },
  "visible": true,
  "opacity": 0.8,
  "style": {
    "fillColor": "#ef4444",
    "fillOpacity": 0.4,
    "strokeColor": "#991b1b",
    "strokeWidth": 1
  }
}
```

不要同時在 layer 的頂層 `geojson` 再放一次相同 FeatureCollection。

若 project 是透過 `?url=...` 載入，使用絕對 Pages URL，以避免相對 URL 解析產生歧義。

## 大型成果架構

當 `result.geojson` 超過任一大型結果門檻時：

1. 保留 `result.geojson` 作為完整正式分析成果。
2. 另外建立 `overview.geojson`，專供預設地圖顯示。
3. Overview 通常應包含：
   - 高優先／高風險結果；
   - 或具代表性的 top subset；
   - 或聚合 polygon／hex／grid cells；
   - 足夠支援 popup 的必要欄位。
4. 可行時，overview 目標控制在 <= 1,000 features 且 <= 3 MiB。
5. 預設 `map.geolibre.json` 應只包含：
   - 小型 boundary／context 圖層；
   - 1～3 個 overview 圖層；
   - 非小型資料在已驗證相容時可用 URL-backed；不相容時縮小 overview、按預算內嵌，或修正 viewer 後再驗證。
6. 不要只因完整詳細圖層檔案已存在，就全部附加到預設 project。
7. 若詳細互動地圖確實有價值，可另外建立可選的 `map-full.geolibre.json`，並明確說明它較重。
8. CSV／XLSX／完整 GeoJSON 仍是逐筆分析的正式成果。

## 幾何與屬性

不得在未說明的情況下簡化正式 `result.geojson`。

只供顯示的 overview 資料可以：

- 在 `summary.json`／`report.md` 有記錄時進行 geometry simplification；
- 可行時保留 topology；
- 使用符合地圖尺度的 tolerance；
- 保留能從顯示 feature 追溯到完整紀錄的識別碼；
- 移除 popup、label、filter 或說明不需要的大型中間／debug properties。

## 圖層可見性

第一次開啟時：

- 預設可見的 thematic layers 不超過 3 個；
- 優先顯示一個清楚的高優先 overview；
- 診斷／中間處理圖層不要放在預設 project；
- 如果一個分類式或 rule-based layer 就能表示，不要為同一來源建立多個重複 URL-backed layers。

## 自動後處理

發布前執行 `optimize-project.py`。

它可能將過大的 inline GeoJSON 外部化到 `layers/*.geojson`，把 project 改寫成 URL-backed sources，並產生 `performance.json`。大小預算通過不代表圖層能顯示；若目標 viewer 不支援 URL-backed，必須縮小 overview、維持相容的 inline 資料或修正 viewer，再做瀏覽器驗收。

Optimizer 是安全網，不代表任務程式可以忽略大型分析需要建立輕量 overview 的責任。

## 必要效能驗證

讀取 `performance.json` 並確認：

- project size；
- externalized layer count；
- largest inline layer；
- visible external payload estimate；
- soft／hard mobile budgets。

若 hard budget 未通過，不得宣告任務完成。
應重新產生以 overview 為主的預設地圖，或降低首次可見資料量，
但不得因此變更使用者已確認的分析條件。

## 相容性與畫面驗收

對每個預設可見圖層，核對 project 資料欄位、實際 GeoLibre 圖層面板及畫面上的圖徵；必要時點擊圖徵檢查 popup。HTTP 200、`loading=ready` 及 `performance.json` 通過不能取代畫面驗收。

### 雙入口真實瀏覽器 QA

每個任務都必須以真實瀏覽器分別驗證：

1. 使用者自架 GitHub Pages GeoLibre；
2. 官方 `https://web.geolibre.app/` 備援入口。

兩者載入同一份已發布 `map.geolibre.json`，且 URL 必須加入 `loading=true`。

每個入口至少檢查：

- 頁面不是白屏；
- App root 有實際尺寸與文字／控制項；
- `data-geolibre-load-state=ready`；
- `data-geolibre-load-errors` 無錯誤；
- 存在實際可見的地圖 canvas；
- canvas／整頁截圖不是近乎全白；
- 預期主圖層名稱存在於圖層 UI；
- 必要時點擊圖徵或檢查 popup，確認不是只有底圖而沒有分析圖層。

**完成門檻：至少一個入口全部通過。兩個都失敗時，任務狀態必須維持 failed / needs-fix，不得宣告完成。**

若目前執行環境沒有瀏覽器工具，必須用 GitHub Actions + Playwright（或等效真實瀏覽器）執行 QA；不得只標示「未驗證」後仍宣告完成。

建議保存：

- `viewer-qa/viewer-qa.json`
- `viewer-qa/self-hosted.png`
- `viewer-qa/official-fallback.png`
- 必要時保存 canvas 細部截圖

這些為內部驗證證據，不列入一般最終六項成果，除非使用者要求技術明細。
