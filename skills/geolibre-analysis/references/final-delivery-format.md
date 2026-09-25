# GeoLibre 最終回覆固定格式

本文件規定**完成分析後，ChatGPT／Codex 對使用者顯示的最終成果清單格式**。

這是使用者介面的固定格式，與 repository 內部實際產生的完整成果套件不同。內部仍可產生 overview、performance、source snapshot、diagnostics、截圖等檔案供驗證與重現，但除非使用者特別要求，**不得把這些技術檔案全部列進最終回覆**。

## 核心原則

1. 最終回覆保持精簡。
2. 分析結論可在成果清單前用 1～3 個短段落說明。
3. 成果清單固定以「成果已回寫你的自架 GeoLibre」為標題。
4. 成果清單固定只顯示 6 項。
5. 不加表格，不加第二份技術檔案清單，不另外展開 overview、performance、source-snapshot、source-diagnostics、events、roads-context、截圖等內部成果。
6. 若六項中的某項未產出或無法開啟，保留該項位置並清楚標示「未產出」或「尚未驗證」，不得用其他檔案替代。
7. 如果使用者明確要求完整技術交付清單，才可在固定六項之後額外補充。
8. 自架 GeoLibre／GitHub Pages 為主要入口；官方 GeoLibre 只作相容性備援，不列入固定成果清單。

## 固定六項

順序、名稱固定如下：

1. **直接在你的 GeoLibre 開啟這次分析**（同一項內必須同時提供「自架主要入口」與「官方 GeoLibre 備援入口」）
2. **GeoLibre 分析專案檔 map.geolibre.json**
3. **Excel 完整分析表 result.xlsx**
4. **CSV 查核結果 result.csv**
5. **分析報告 report.md**
6. **結果摘要 summary.json**

不得自行增加：
- result.geojson
- overview.geojson
- events.geojson
- roads-context.geojson
- performance.json
- source-snapshot.json
- source-diagnostics.json
- report.html
- map-overview.png
- GitHub Actions / Pages build status
- commit SHA

以上資料仍應依成果契約正常產生、驗證或保存，只是不主動顯示在一般最終回覆。

## 固定輸出範本

分析結論說明結束後，使用以下格式：

```md
## 成果已回寫你的自架 GeoLibre

[直接在你的 GeoLibre 開啟這次分析](<analysis-entry-url>)  
[官方 GeoLibre 備援入口](https://web.geolibre.app/?url=<URL-ENCODED-PROJECT-URL>&layout=viewer&locale=zh-TW)

[GeoLibre 分析專案檔 map.geolibre.json](<map-project-url>)

[Excel 完整分析表 result.xlsx](<xlsx-url>)

[CSV 查核結果 result.csv](<csv-url>)

[分析報告 report.md](<report-url>)

[結果摘要 summary.json](<summary-url>)
```

若介面會自動顯示外連箭頭，不需要手動加入「↗」。

## 不應出現在一般最終回覆的內容

除非使用者主動詢問，不要在固定成果清單後再追加：

- 「另外新增 source-snapshot.json」
- 「效能檢查 performance.json」
- 「overview.geojson」
- 「events.geojson」
- 「道路中心線脈絡」
- 「瀏覽器截圖尚未驗證」
- 「Pages build/deploy 成功」
- 「內部診斷檔」

若其中有會實質影響使用者解讀結果的重大異常，只在成果清單之前以一句話說明，不把它變成額外交付清單。

## 驗收

最終回覆前確認：

- 有簡短分析結論；
- 有「成果已回寫你的自架 GeoLibre」；
- 六項成果名稱及順序完全一致；
- 第 1 項同時有自架主要入口與官方 GeoLibre 備援入口，備援入口以相同 map.geolibre.json 組成官方 web.geolibre.app 的 url 參數；
- 六項連結指向本次 task 的實際成果；
- 沒有主動列出第 7 項技術檔案；
- 沒有用大表格取代固定六項；
- 沒有把 repository 內部驗證檔當成使用者主要交付成果。

若不符合，最終回覆視為格式驗收失敗。
