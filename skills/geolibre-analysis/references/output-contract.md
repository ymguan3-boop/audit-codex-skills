# GeoLibre 分析成果契約

分析規格確認後，使用本成果契約。

## 必要成果套件

將任務成果寫入：

`<analysis_root>/<task_id>/`

適用時應產生：

- `map.geolibre.json` — 預設互動式 GeoLibre project
- `overview.geojson` — 大型結果使用的輕量 overview
- `result.geojson` — 完整且具權威性的向量分析結果
- `result.csv`
- `result.xlsx`
- `summary.json`
- `report.md`
- `performance.json`
- `index.html` — 穩定的公開導向／入口頁
- `map-overview.png` — 可使用瀏覽器自動化時，從實際 GeoLibre 頁面擷取的截圖
- 可選的 `map-detail-01.png` 等細部截圖

## XLSX 要求

若分析結果適合表格化，必須建立真正的 XLSX，不得只把 CSV 改副檔名。

至少包含下列工作表：

1. **分析結果**
   - 每列對應一個結果 feature／道路區段／地點
   - 可讀名稱
   - 可取得時的行政區
   - 使用風險分級／分數時，保留該欄位
   - 判斷規則／觸發原因
   - 相關距離／次數／年份
   - 使用高程／坡度時，保留該欄位
   - 可追溯時保留來源 feature id／OSM id／official id

2. **統計摘要**
   - 結果總筆數
   - 唯一 feature／道路／設施數
   - 適用時的總長度／面積
   - 各風險級別筆數
   - 有意義時的行政區統計

3. **分析參數**
   - 分析區域
   - 時間範圍
   - 空間門檻
   - 公尺制計算使用的 CRS
   - 風險／評分邏輯
   - 產生時間

4. **資料來源**
   - 圖層
   - 資料提供單位
   - URL／service
   - 資料日期／期間
   - 取得日期
   - CRS
   - 官方資料或補充資料
   - 在分析中的用途
   - 已知限制

工作簿格式至少包含標題列、自動篩選、凍結第一列、合理欄寬，以及正確的日期／數值格式。

## GeoLibre project 要求

- 結果／overview 圖層預設可見，並靠近 layer stack 上層。
- 初始 camera 應對準結果範圍。
- Context 圖層使用適度透明度，不應搶過結果主題。
- Popup 欄位應能說明 feature 為什麼被選中。
- Metadata 應記錄資料來源、參數、產生時間與限制。
- 中文使用者的瀏覽連結使用 `locale=zh-TW`。
- 預設 project 必須符合 `performance-and-publishing.md` 的效能預算。

## 穩定公開入口

當成果需要讓使用者直接開啟時，建立 `index.html`。

必須安全組合 viewer URL，確保經過 URL encoding 的 project URL 與外層參數分開，
例如 `locale=zh-TW`、`layout=viewer`、`loading=true`。

不得把 `&locale=...` 一併編碼成 project URL 的一部分。

## 真正的 GeoLibre 畫面截圖

可使用瀏覽器自動化時：

1. 以 `loading=true` 開啟實際已部署的 GeoLibre URL。
2. 等待 `document.documentElement.dataset.geolibreLoadState` 變成 `ready`。
3. 讀取 `data-geolibre-load-errors`；若渲染有錯誤，不得接受為完成成果。
4. 擷取 `map-overview.png`。
5. 只有在確實增加資訊價值時，才額外擷取 1～3 張細部截圖。

使用 matplotlib／plotly 或其他工具另外繪製的靜態地圖，不算 GeoLibre 截圖。

若執行環境沒有瀏覽器自動化，應清楚標示「GeoLibre 畫面截圖尚未驗證」，
不得假裝截圖已存在。

## 完成前交叉驗證

- `summary.json.resultCount` 必須與正式 GeoJSON feature count 一致。
- XLSX「分析結果」資料列數應與 result count 一致；若不同，report 必須說明原因。
- report 的統計數字必須與 summary 一致。
- 公開 project URL 必須能成功回應。
- 有 browser QA 時，GeoLibre render 必須到達 `ready` 且沒有 load errors。
- 所有非官方補充資料都必須明確標示。
