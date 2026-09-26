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

本技能**不綁定使用者 GitHub、不建立或管理使用者自己的 GitHub Pages、不使用使用者 GitHub Actions 作為分析／發布必要流程**。依官方文件，`web.geolibre.app` 本身目前由官方部署在 GitHub Pages；這屬官方服務基礎設施，不構成使用者 GitHub 綁定。

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

## 3A. 台灣公部門／敏感資料發布閘門

一般版使用官方 `share.geolibre.app` 發布 project，因此在分析開始前要判斷輸入與輸出是否適合送至第三方外部服務。

若資料屬於公開資料、開放資料或已充分去識別且可公開的結果，可照一般流程。

若資料包含或可能包含下列內容，不得預設上傳官方 Share：

- 個人資料或可重新識別個人的組合資料；
- 未公開公務資料；
- 敏感設施、關鍵基礎設施、資安配置或其他受限資訊；
- 機關內部分級為不得外傳或須核准上雲的資料。

此時：

1. 先完成本機分析，不發布。
2. 提醒使用者依機關個資、資安、資料分級與雲端服務政策確認授權。
3. 未取得明確允許前，不呼叫 Share API。
4. 可建議改成本機／機關自架 GeoLibre；只有機關政策允許時才使用其他雲端託管方式。

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

一般版沿用 GitHub 版相同的成果正確性與畫面驗收標準，差別只在互動地圖驗證入口改為官方 GeoLibre Viewer。

以下全部成立才算完成：

1. 分析任務與使用者確認的 GIS 條件一致，沒有為了跑通流程而弱化門檻。
2. `summary.json.result_count` 與 `result.geojson` feature count 一致。
3. XLSX「分析結果」資料列數與 result count 一致；若不同，report 必須說明。
4. `report.md` 的統計、資料來源、限制與 summary 一致。
5. `map.geolibre.json` 確實包含或引用正式結果，預設可見結果圖層存在，初始 camera 對準結果。
6. Share preflight 通過：project < 50 MiB、無本機路徑、無未驗證的私有／CORS 失敗來源。
7. 已成功上傳 `share.geolibre.app`。
8. 官方 `web.geolibre.app` 必須用真實瀏覽器分別做桌面 Chromium 與 Android viewport QA，兩者都通過：
   - 非白屏；
   - `data-geolibre-load-state=ready`；
   - `data-geolibre-load-errors=[]`；
   - 有可見 map canvas；
   - 主結果圖層名稱出現在 UI；
   - canvas 有實際地圖像素／圖徵。
9. report 中的 Viewer QA 狀態與最新 QA 結果一致。
10. 資料來源、替代來源、公開資料母體缺口及分類推論限制均已說明。

任何一項失敗都不得宣告完成，先做最小必要修正後重試。


## 6A. 驗收失敗後的自動修復與完整重跑


### 強制規則：驗收不合格不得交付半成品

以下規則屬於**不可跳過的完成閘門**，優先級高於「先給使用者目前可用成果」的方便性考量：

1. 只要分析、檔案一致性、發布、Viewer、瀏覽器畫面或固定六項成果中的任何一項未符合技能規則，**不得直接進入最終成果回覆，也不得把現有檔案包裝成「完成版」交付**。
2. 必須先主動告知使用者：
   - 哪一項未通過；
   - 原因；
   - 對正式成果的影響；
   - 建議採取的最小修正方式。
3. 告知後不得停在建議。只要現有工具、公開資料、替代來源、其他可用執行環境或官方支援的替代載入方式可以解決，就必須**自行繼續處理到解決**。
4. 修復成功後，必須從**最早受影響的分析／產檔／發布步驟重新執行**，並重建所有受影響的正式成果；不得只補缺少的單一檔案或網址。
5. 修復後必須重新跑完整驗收。若又發現新問題，重複「建議 → 修復 → 重跑 → 全驗收」循環，直到全部通過。
6. 前一版、初篩版、失敗版、缺網址版、未完成 QA 版一律視為 **superseded／已由新版取代**，不得再作為最終交付。
7. **「直接在你的 GeoLibre 開啟這次分析」是必要成果，不是可選項。** 若尚未有已載入完整圖資專案且經真實瀏覽器驗證的可用網址，就表示輸出仍未完成。
8. 若官方 Share 暫時不可用，必須先檢查官方 Viewer 是否支援以其他匿名可讀、CORS 可用的公開 project URL 載入；若合法、安全且不違反本技能版本定位，應主動使用可行替代方案，不得因單一服務或 token 缺失就直接停止。
9. 只有在**確實只剩必須由使用者本人完成、且模型無法合法代替的外部授權／登入／付費／機關核准**時，才可暫停。此時只能回報「尚未完成」與唯一阻礙，不得輸出完成式固定六項成果。
10. 一旦該外部阻礙解除，必須立即從受影響步驟繼續，重新發布、重新 QA、重新產生或同步更新正式成果後，再交付最終版。

**禁止行為：**
- 發現驗收不合格後只給建議、不實際修復；
- 修復資料後不重跑正式分析；
- 修好 project 後沿用舊的 report／summary／XLSX；
- 沒有可用 Viewer URL 卻仍交付固定六項並稱為完成；
- 用下載檔案連結取代「已載入完整專案的 GeoLibre URL」；
- 因某個 API／token 不可用就直接停止，而未先尋找技能允許的替代發布方式。

**最終判定原則：不合格 → 建議 → 實際修復 → 完整重跑 → 完整驗收 → 才能最終交付。**

## 7. 最終成果固定格式

遵守 `references/final-delivery-format.md`，一般完成回覆固定只顯示：

1. 直接在你的 GeoLibre 開啟這次分析
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
