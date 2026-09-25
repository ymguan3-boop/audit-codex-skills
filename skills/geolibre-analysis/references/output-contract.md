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

- `summary.json.result_count` 必須與正式 GeoJSON feature count 一致。
- XLSX「分析結果」資料列數應與 result count 一致；若不同，report 必須說明原因。
- report 的統計數字必須與 summary 一致。
- 公開 project URL 與報告引用的每個成果檔都必須可開啟。
- 必須完成雙入口 browser QA：自架 GitHub Pages 與官方 web.geolibre.app 都要實際開啟並截圖檢查；自架與官方入口都必須各自測試桌面與 Android 手機 viewport；至少一個入口必須在兩種裝置模式都通過「非白屏、ready、無 load errors、可見 canvas、預期圖層 UI 與實際地圖內容」的全部條件。沒有任何入口同時通過桌面＋手機時，不得宣告完成。
- 若聊天環境沒有 browser QA 能力，必須改由 GitHub Actions + Playwright 或等效真實瀏覽器完成，不得省略。
- 所有非官方補充資料都必須明確標示。

## 正式分析報告與交付清單

`report.md` 必須先載入並遵守 `report-writing-standard.md`。該文件的固定報告骨架屬於**硬性成果契約**，不得用較短的白話摘要、表格或新版追加章節取代。

最低固定結構如下：

1. 標題
2. 任務摘要列點
3. `## 方法`
4. `## 分類`
5. `## 資料品質`
6. `## 重要限制`
7. `## 資料來源`
8. `## 交付檔案`

只有完成上述八個部分後，才可追加主要發現、圖層—圖資—檔案對照、地圖圖層說明、效能與發布、瀏覽器驗證、後續建議與總結。

報告必須保留原版完整分析報告的寫法特徵：

- 開頭直接列出本次分析的核心參數與統計結果；
- 「方法」以完整段落交代資料、CRS、GIS 邏輯與時間邏輯；
- 「分類」把文字規則、風險級別或標籤判斷清楚寫出；
- 「資料品質」量化原始筆數、可分析筆數、排除、缺日期、缺幾何、期間外或其他缺口；
- 「重要限制」明確區分公開資料限制、替代來源、空間鄰近與正式認定；
- 「資料來源」逐項交代提供者、URL／service、資料期間、取得日期、用途與限制；
- 「交付檔案」逐檔說明用途，未產出的檔案不得假裝存在。

報告仍須有**圖層—圖資—檔案對照表**，但此表必須放在固定骨架之後，不能取代「資料來源」或「交付檔案」。

備援／快取不得說成當次重新下載。若 Pages 把 `.md` 顯示為原始文字，另產生可讀 `report.html`，並納入驗收。

完成前必須檢查固定章節是否齊全；缺任一章節即視為 `report.md` 驗收失敗。

## 使用者最終成果清單

Repository 內部成果套件維持完整，但一般使用者最終回覆不得把所有技術成果逐項列出。最終回覆必須載入並遵守 `final-delivery-format.md`，固定只顯示：

1. 直接在你的 GeoLibre 開啟這次分析
2. GeoLibre 分析專案檔 map.geolibre.json
3. Excel 完整分析表 result.xlsx
4. CSV 查核結果 result.csv
5. 分析報告 report.md
6. 結果摘要 summary.json

一般最終回覆不得主動增加第 7 項，也不得把 result.geojson、overview、performance、source snapshot、diagnostics、report.html、截圖或 Actions 狀態列成主要交付成果。

只有在使用者明確要求「完整技術成果」、「全部檔案」或特定額外檔案時，才可在固定六項之後補充。

如果固定六項中的某項不存在、未發布或未驗證，仍保留該位置並標示狀態，不得偷偷以其他檔案替代。
