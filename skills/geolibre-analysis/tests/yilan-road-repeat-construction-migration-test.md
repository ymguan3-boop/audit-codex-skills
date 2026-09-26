# 遷移測試：宜蘭縣道路工程重複施工分析

## 測試目標

驗證既有 GitHub 自架成果是否能改由預設的一般版 `geolibre-analysis`，在不使用使用者 GitHub Pages 的情況下，改由官方 share.geolibre.app + web.geolibre.app 呈現。

## Preflight 結果

結果：**PASS**

- map.geolibre.json 約 63 KB，遠低於官方 Share 50 MiB 上限。
- project 2 個 GeoJSON 圖層。
- repeat-hotspots：inline GeoJSON，2 features。
- construction-events：inline GeoJSON，53 features。
- 無 source.data 外部 GeoJSON URL。
- 無本機檔案路徑。
- Excel / CSV / report.md / summary.json 可由一般版直接產生為對話附件。

## 目前尚需的一次性設定

正式呼叫 `POST /api/projects` 需要官方 GeoLibre Share Bearer token。

環境變數：

`GEOLIBRE_SHARE_TOKEN`

Token 不得寫入 GitHub、SKILL.md 或聊天內容。

## 結論

- 一般版架構可行：PASS。
- 本案例 share-readiness：PASS。
- GitHub Pages 可從一般版執行流程移除：PASS。
- 固定六項成果可維持：PASS。
- 正式官方 Share 上傳與 viewer QA：需在使用者完成一次性 token 設定後執行。
