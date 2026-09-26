# GeoLibre 一般版分析成果契約

一般版與 GitHub 版使用**相同的分析正確性、表格交叉驗證、正式報告與畫面 QA 標準**；主要差異只有發布位置：一般版的互動地圖使用官方 `share.geolibre.app` / `web.geolibre.app`，不建立使用者 GitHub Pages。

## 必要成果套件

每次分析至少產生：

- `map.geolibre.json` — GeoLibre project
- `result.geojson` — 完整正式向量結果
- `result.csv`
- `result.xlsx`
- `summary.json`
- `report.md`

適用時另外產生：

- `overview.geojson` — 大型結果的輕量預覽
- 輸入證據／重要子集 GeoJSON
- `performance.json` — project 大小與首次載入預算
- `viewer-qa.json` 與真實瀏覽器 QA 截圖
- `report.html` — Markdown 不易直接閱讀時的 HTML 版本

這些內部技術成果不必全部出現在一般最終回覆；使用者介面固定只顯示六項。

## XLSX 要求

與 GitHub 版一致。若結果適合表格化，必須建立真正 XLSX，至少包含：

1. **分析結果**：每列對應一個正式結果，包含可讀名稱、行政區／座標識別、判斷值、觸發原因、必要距離／次數／年份與來源 id。
2. **統計摘要**：結果總筆數、唯一 feature 數、風險／分類統計及有意義的行政區統計。
3. **分析參數**：範圍、期間、空間門檻、CRS、分類／評分邏輯、產生時間。
4. **資料來源**：提供單位、URL/service、資料日期、取得日期、CRS、用途及限制。

工作簿至少要有標題列、自動篩選、凍結第一列、合理欄寬與正確日期／數值格式。

## GeoLibre project 要求

- 正式結果／overview 預設可見。
- 初始 camera 對準結果範圍。
- Popup 能說明 feature 為何被選中。
- Metadata 記錄資料來源、參數、產生時間與限制。
- 中文 viewer URL 使用 `locale=zh-TW`。
- 小中型 GeoJSON 優先 inline，避免 Share project 指向本機或不可公開來源。
- project JSON 必須低於官方 Share 50 MiB 上限。

## 官方 Share 發布

- `share.geolibre.app` 只保存 project JSON，不保存 XLSX、CSV、Markdown report 或其他本機檔案。
- 第 3～6 項固定成果以對話附件／工作區檔案交付。
- 外部資料 URL 必須匿名可讀、HTTPS 且 CORS 正常；否則改 inline 或停止發布。
- 個資、未公開公務資料、敏感設施／資安資料未經機關核准，不得預設上傳官方 Share。

## 完成前交叉驗證

- `summary.json.result_count` = `result.geojson` feature count。
- XLSX「分析結果」列數 = result count；不同時 report 必須說明。
- report 統計 = summary。
- map project 內正式結果筆數與 report 一致。
- report.md 的 Viewer QA 狀態 = 最新 viewer QA。
- 公開資料來源、替代來源與限制均已揭露。

## 真實瀏覽器驗收

一般版與 GitHub 版採相同畫面驗收項目，只把目標網址改為官方 `web.geolibre.app`。

官方 viewer 必須分別測試：

1. 桌面 Chromium
2. Android 手機 viewport

兩者都必須：

- 非白屏；
- App root 已掛載；
- `data-geolibre-load-state=ready`；
- `data-geolibre-load-errors=[]`；
- 存在可見 map canvas；
- canvas 有實際像素／圖徵內容；
- 預期主結果圖層名稱存在於 UI／圖層面板。

任何一個裝置模式失敗，都不得把官方 Viewer 標示為已驗證完成。

## 正式分析報告

`report.md` 必須遵守 `report-writing-standard.md`，固定保留：任務摘要、方法、分類、資料品質、重要限制、資料來源、交付檔案；新版補充章節只能追加，不能取代。

## 使用者最終成果

固定只顯示以下六項，名稱與 GitHub 版一致：

1. **直接在你的 GeoLibre 開啟這次分析**
2. **GeoLibre 分析專案檔 map.geolibre.json**
3. **Excel 完整分析表 result.xlsx**
4. **CSV 查核結果 result.csv**
5. **分析報告 report.md**
6. **結果摘要 summary.json**

差異只有連結位置：第 1 項指向官方 `web.geolibre.app`，第 2 項指向 `share.geolibre.app` 的 raw project URL；第 3～6 項為對話附件／工作區檔案。
