---
name: geolibre-analysis
description: |
  GeoLibre 一般版 GIS 空間分析技能，也是預設 GeoLibre 技能。當使用者說「使用 GeoLibre 技能」、
  「使用 GeoLibre」、「幫我用 GeoLibre 分析」或其他未特別提 GitHub 的 GeoLibre 指令時使用。
  本技能不要求使用者 GitHub、不自架 GitHub Pages；使用本機／Codex 完成分析後，將可分享的
  GeoLibre project 上傳官方 share.geolibre.app，最後由官方 web.geolibre.app 呈現互動地圖；
  XLSX、CSV、report.md、summary.json 直接作為對話附件或工作區檔案交付。
  若使用者明確說「使用 GeoLibre GitHub 版技能」或要求 GitHub Pages／長期 Git 留痕，
  則改用 geolibre-github-analysis。
---

# GeoLibre 一般版分析技能

當使用者以中文溝通時，預設使用繁體中文。

## 0. 觸發與版本路由

### 一般版固定指令

`使用 GeoLibre 技能`

以下未特別提 GitHub 的說法也一律使用本技能：

- `使用 GeoLibre`
- `GeoLibre 技能`
- `幫我用 GeoLibre 分析`
- `GeoLibre，我沒想法`

### GitHub 版固定指令

若使用者明確輸入：

`使用 GeoLibre GitHub 版技能`

或明確要求 GitHub repository、GitHub Pages、GitHub Actions、長期公開網址／完整 Git 留痕，改用 `geolibre-github-analysis`。

**不得因為過去對話曾使用 GitHub 版，就推定本次仍要 GitHub 版。只要本次未明確指定 GitHub，預設回到本一般版。**

## 1. 核心定位

本技能**不綁定使用者 GitHub、不建立 GitHub Pages、不使用 GitHub Actions作為分析／發布必要流程**。

正式流程：

`公開資料／使用者資料 -> 本機或 Codex GIS 分析 -> GeoLibre inline project -> share.geolibre.app -> web.geolibre.app viewer -> 對話附件成果`

技能原始碼本身可以放在 GitHub 供下載與版本管理，但任務成果不需要使用者 GitHub。

## 2. 官方服務

- 官方 viewer：`https://web.geolibre.app/`
- 官方分享／Project Gallery：`https://share.geolibre.app`
- 分享 API：`POST /api/projects`
- Token 環境變數：`GEOLIBRE_SHARE_TOKEN`

不得把 token 寫入 SKILL.md、repository、report、summary、command log 或最終回覆。

若 token 尚未設定，先完成分析與 share-readiness preflight；到正式上傳前才要求使用者完成一次官方 Share 帳號／token 設定。不要要求使用者把 token 貼進聊天內容。

預設 visibility 使用 `unlisted`，除非使用者明確要求 public/private。

## 3. 分享能力與限制

share.geolibre.app 儲存 GeoLibre project JSON，不是一般檔案雲端硬碟。

因此：
- 小型／中型 GeoJSON 優先 inline 到 `map.geolibre.json`。
- 不得把本機檔案路徑留在 shared project。
- 遠端 URL 圖層只有在匿名可讀、CORS 可用時才可保留。
- 若 project 超過 50 MiB，或資料不適合 inline，停止官方-only 發布，建議切換 `geolibre-github-analysis`。
- Excel、CSV、report.md、summary.json 直接作為對話附件／工作區檔案交付，不宣稱由官方 Share 保存。

## 4. 需求探索

沿用 `references/topic-catalog.md`。

若使用者沒有想法：
1. 顯示 17 個主題。
2. 選定主題後提供 3～5 個可直接執行的分析題目。
3. 每回合只問 1～3 個必要問題。
4. 最後顯示分析設定摘要。
5. 只有使用者明確回覆「確認執行／開始分析／執行」才開始。

## 5. 執行

確認後：

1. 取得公開資料或使用者提供資料。
2. 使用 Python／GeoPandas／其他可用 GIS 工具完成分析。
3. 產出至少：
   - `map.geolibre.json`
   - `result.geojson`
   - `result.csv`
   - `result.xlsx`
   - `summary.json`
   - `report.md`
4. 依 `references/report-writing-standard.md` 產生完整正式報告。
5. 執行 Share preflight：
   - project JSON < 50 MiB
   - 至少一個正式結果圖層
   - 預設可見結果圖層
   - 初始 camera 對準結果
   - 不含本機 file path
   - 外部來源匿名可讀且 CORS 正常，否則改 inline
6. 使用 `assets/share-project.py` 上傳官方 Share。
7. 使用回傳 `rawJsonUrl` 組成：
   `https://web.geolibre.app/?url=<encoded rawJsonUrl>&layout=viewer&loading=true&locale=zh-TW`
8. 使用真實瀏覽器做桌面 + Android QA；兩者都必須通過：
   - 非白屏
   - `data-geolibre-load-state=ready`
   - `data-geolibre-load-errors=[]`
   - 可見 map canvas
   - 主結果圖層名稱存在
   - canvas 有實際像素內容
9. QA 通過後才可宣告完成。

## 6. 完成條件

以下全部成立才算完成：
- 分析結果已產出。
- XLSX / CSV / summary / report 交叉一致。
- map.geolibre.json share-readiness 通過。
- 已成功上傳 share.geolibre.app。
- 官方 viewer 桌面與 Android QA 都通過。
- report 中 QA 狀態已同步為最新結果。

## 7. 最終成果固定格式

遵守 `references/final-delivery-format.md`，一般完成回覆固定只顯示：

1. 直接在官方 GeoLibre 開啟這次分析
2. GeoLibre 分析專案檔 map.geolibre.json
3. Excel 完整分析表 result.xlsx
4. CSV 查核結果 result.csv
5. 分析報告 report.md
6. 結果摘要 summary.json

第 1、2 項使用 share.geolibre.app / web.geolibre.app 官方網址；第 3～6 項使用對話附件／工作區檔案。

## 8. 切換 GitHub 版的條件

符合任一情況，建議切換 `geolibre-github-analysis`：
- 所有成果都需要長期公開 URL；
- project 超過或接近 50 MiB；
- 需要大量大型外部資料檔一起託管；
- 需要完整 Git 版本歷史／Actions 稽核軌跡；
- 需要機關內部固定網址或自有部署；
- 不希望分析 project 上傳官方 Share。
