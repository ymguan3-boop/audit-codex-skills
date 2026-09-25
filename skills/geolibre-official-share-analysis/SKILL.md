---
name: geolibre-official-share-analysis
description: |
  不依賴使用者 GitHub、不自架 GitHub Pages 的 GeoLibre GIS 分析技能。
  使用本機／Codex 完成分析，將可分享的 GeoLibre project 上傳到官方 share.geolibre.app，
  最後以官方 web.geolibre.app / Project Gallery 呈現互動地圖；XLSX、CSV、report.md、
  summary.json 直接作為對話附件交付。適合希望免 GitHub 綁定、免自架網站的使用者。
---

# GeoLibre 官方 Share 分析技能

當使用者以中文溝通時，預設使用繁體中文。

## 0. 核心定位

本技能**不綁定使用者 GitHub、不建立 GitHub Pages、不使用 GitHub Actions 作為分析／發布必要流程**。

正式流程：

`公開資料／使用者資料 -> 本機或 Codex GIS 分析 -> GeoLibre inline project -> share.geolibre.app -> web.geolibre.app viewer -> 對話附件成果`

技能原始碼可以被存放在 GitHub 或其他位置，但那只是技能本身的版本管理，不能把 GitHub 當成任務成果的必要主機。

## 1. 官方服務

- 官方 viewer：`https://web.geolibre.app/`
- 官方分享／Project Gallery：`https://share.geolibre.app`
- 分享 API：`POST /api/projects`
- Token 環境變數：`GEOLIBRE_SHARE_TOKEN`

不得把 token 寫入：
- SKILL.md
- repository
- report
- summary
- command log
- 最終回覆

若 token 尚未設定，先完成分析與 share-readiness preflight；到正式上傳前才要求使用者進行一次官方 Share 帳號／token 設定。不要要求使用者把 token 貼進聊天內容。

預設 visibility 使用 `unlisted`，除非使用者明確要求 public/private。

## 2. 分享能力與重要限制

share.geolibre.app 儲存的是 GeoLibre project JSON，不是一般檔案雲端硬碟。

因此：
- 地圖資料若要讓收件者直接看到，優先把小型／中型 GeoJSON **inline 到 map.geolibre.json**。
- 不得把本機檔案路徑留在 shared project。
- 遠端 URL 圖層只有在匿名可讀、CORS 可用時才可保留。
- 若 project 超過 50 MiB，或大量資料不適合 inline，停止官方-only 發布並說明原因；可建議切回原本 `geolibre-analysis` 自架模式或使用另外的公開資料主機。
- Excel、CSV、report.md、summary.json 不會被 share.geolibre.app 保存；這些直接作為 ChatGPT/Codex 對話附件交付。

## 3. 需求探索

沿用 `references/topic-catalog.md`。

若使用者沒有想法：
1. 顯示 17 個主題。
2. 選定主題後提供 3～5 個可直接執行的分析題目。
3. 每回合只問 1～3 個必要問題。
4. 最後顯示分析設定摘要。
5. 只有使用者明確回覆「確認執行／開始分析／執行」才開始。

## 4. 執行

確認後：

1. 取得公開資料或使用者提供資料。
2. 使用 Python／GeoPandas／其他可用 GIS 工具完成分析。
3. 產出：
   - map.geolibre.json
   - result.geojson
   - result.csv
   - result.xlsx
   - summary.json
   - report.md
4. 依 `references/report-writing-standard.md` 產生完整正式報告。
5. 執行官方 Share preflight：
   - project JSON < 50 MiB
   - 至少一個正式結果圖層
   - 預設可見結果圖層
   - 初始 camera 對準結果
   - 不含本機 file path
   - 外部來源匿名可讀且 CORS 正常，否則改 inline
6. 使用 `assets/share-project.py` 上傳官方 Share。
7. 使用回傳的 `rawJsonUrl` 組成：
   `https://web.geolibre.app/?url=<encoded rawJsonUrl>&layout=viewer&loading=true&locale=zh-TW`
8. 使用真實瀏覽器做桌面 + Android QA；兩者都必須通過：
   - 非白屏
   - data-geolibre-load-state=ready
   - data-geolibre-load-errors=[]
   - 可見 map canvas
   - 主結果圖層名稱存在
   - canvas 有實際像素內容
9. QA 通過後才可宣告完成。

若沒有可用真實瀏覽器，不能把任務標成完整完成；應保留成果，但標示 viewer QA 尚待執行。

## 5. 完成條件

以下全部成立才算完成：
- 分析結果已產出。
- XLSX / CSV / summary / report 交叉一致。
- map.geolibre.json share-readiness 通過。
- 已成功上傳 share.geolibre.app。
- 官方 viewer 的桌面與 Android QA 都通過。
- report 中 QA 狀態已同步為最新結果。

## 6. 最終成果固定格式

遵守 `references/final-delivery-format.md`。

固定只顯示 6 項：
1. 直接在官方 GeoLibre 開啟這次分析
2. GeoLibre 分析專案檔 map.geolibre.json
3. Excel 完整分析表 result.xlsx
4. CSV 查核結果 result.csv
5. 分析報告 report.md
6. 結果摘要 summary.json

第 1、2 項使用 share.geolibre.app / web.geolibre.app 官方網址。
第 3～6 項用對話附件／工作區檔案交付，不假裝它們由官方 Share 保存。

## 7. 適合切回原技能的情況

若符合任一條件，建議改用 `geolibre-analysis` 自架 GitHub 版本：
- 需要所有成果都有長期公開 URL；
- 需要超過 50 MiB 的 project；
- 需要大量大型外部資料檔一起託管；
- 需要持續版本化保存分析成果；
- 需要機關內部固定網址或完全自有網域；
- 不希望分析 project 上傳官方 Share 服務。
