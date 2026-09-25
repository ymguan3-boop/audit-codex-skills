# GeoLibre Official Share Analysis

這是 `geolibre-analysis` 的 GitHub-free 執行變體。

差異：
- 不綁定使用者 GitHub。
- 不建立 GitHub Pages。
- 不使用 GitHub Actions 發布分析成果。
- 互動地圖上傳官方 `share.geolibre.app`。
- 使用官方 `web.geolibre.app` 呈現。
- XLSX / CSV / report.md / summary.json 直接作為對話附件交付。

第一次使用需要使用者準備 GeoLibre Share token，並以環境變數 `GEOLIBRE_SHARE_TOKEN` 提供；不得把 token 寫進技能或 repository。

原本 `geolibre-analysis` 保留不變，待此技能實測穩定後再決定是否取代。
