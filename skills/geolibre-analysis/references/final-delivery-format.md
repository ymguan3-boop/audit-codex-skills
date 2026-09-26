# GeoLibre 最終回覆固定格式（一般版）

一般版與 GitHub 版的使用者輸出項目名稱與順序相同；只把地圖與 project 驗證網址改成官方 GeoLibre。

## 固定六項

1. **直接在你的 GeoLibre 開啟這次分析**
2. **GeoLibre 分析專案檔 map.geolibre.json**
3. **Excel 完整分析表 result.xlsx**
4. **CSV 查核結果 result.csv**
5. **分析報告 report.md**
6. **結果摘要 summary.json**

## 固定範本

```md
## 成果已發布至官方 GeoLibre

[直接在你的 GeoLibre 開啟這次分析](<official-viewer-url>)

[GeoLibre 分析專案檔 map.geolibre.json](<share-raw-json-url>)

[Excel 完整分析表 result.xlsx](<chat-attachment-or-workspace-link>)

[CSV 查核結果 result.csv](<chat-attachment-or-workspace-link>)

[分析報告 report.md](<chat-attachment-or-workspace-link>)

[結果摘要 summary.json](<chat-attachment-or-workspace-link>)
```

## 規則

- 固定六項，不主動增加第 7 項技術檔。
- 第 1 項是必要成果：必須是「已載入本次完整圖資專案」的 GeoLibre Viewer URL，且已通過桌面＋Android 真實瀏覽器 QA；不得以 map.geolibre.json 下載連結替代。
- 第 2 項必須是 `share.geolibre.app` 可讀的 raw project URL。
- 第 3～6 項不是官方 Share 託管，必須如實用對話附件／工作區檔案交付。
- QA 未通過時，不得使用「已發布完成」語氣，也不得輸出固定六項作為最終成果；必須回到修復流程，修復後重跑、重新產檔與重新 QA。
- 不得因一般版不用 GitHub，就刪除 Excel、CSV、正式報告或 summary；輸出內容與 GitHub 版保持一致。


## 不完整成果禁止交付閘門

- 只要固定六項任何一項缺失、無法開啟、未驗證或仍指向舊版成果，**整體就不是最終成果**。
- 此時不得用固定六項範本回覆使用者；必須先依 SKILL.md 的強制修復規則處理。
- 修復成功後，必須重新產生／同步全部受影響檔案與 Viewer URL，重新做桌面＋Android QA，再從頭檢查六項。
- 尤其第 1 項「直接在你的 GeoLibre 開啟這次分析」缺失時，不得改成只給 project 下載檔。
- 若官方 Share 不可用，先尋找官方 Viewer 支援且匿名可讀、CORS 可用的合法 project URL 載入方式；可行時應主動採用。
- 只有剩下使用者本人必須完成的外部授權時，才允許回覆未完成狀態；不得稱為最終交付。
