# 官方 Share 模式成果契約

## 本機／對話成果

每次分析至少產生：

- `map.geolibre.json`
- `result.geojson`
- `result.csv`
- `result.xlsx`
- `summary.json`
- `report.md`

可視需要產生：
- `overview.geojson`
- `performance.json`
- `viewer-qa.json`
- QA screenshots

## 官方託管成果

官方 Share 僅負責：
- GeoLibre project JSON
- Project Gallery metadata
- 官方 project/raw/viewer URL

不要宣稱 share.geolibre.app 託管：
- XLSX
- CSV
- Markdown report
- summary.json
- 任意本機來源資料

## GeoLibre project

官方-only 模式優先採用 inline GeoJSON，以單一 project 完成可視化。

若 project 接近 50 MiB：
- 先移除非必要欄位、做幾何簡化或 overview；
- 若仍過大，不得硬上傳；
- 改用大型資料的公開 URL 或切回自架技能。

## QA

只有官方 viewer 桌面 + Android 都通過，才能把「直接在官方 GeoLibre 開啟」標成已驗證。

## 交叉驗證

- summary.result_count = result.geojson feature count
- XLSX 分析結果列數 = result_count，或 report 解釋差異
- report 統計 = summary
- share project 內正式結果筆數與 report 一致
