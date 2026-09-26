# GeoLibre 一般版技能

這是目前的**預設 GeoLibre 技能**。

固定使用指令：

```
使用 GeoLibre 技能
```

只要使用者沒有明確說「GitHub 版」，所有 GeoLibre 分析一律優先使用本版。

本版特色：
- 不要求使用者擁有 GitHub。
- 不建立 GitHub Pages。
- 不需要 GitHub Actions 作為成果發布流程。
- 互動地圖使用官方 `share.geolibre.app` + `web.geolibre.app`。
- Excel、CSV、report.md、summary.json 直接以對話附件／工作區檔案交付。
- 流程比 GitHub 版短，適合一般使用者與大量日常分析。

## 兩個版本簡要比較

| 比較項目 | GeoLibre 一般版 | GeoLibre GitHub 版 |
|---|---|---|
| 固定指令 | **使用 GeoLibre 技能** | **使用 GeoLibre GitHub 版技能** |
| 預設路由 | **是** | 否，必須明確點名 GitHub 版 |
| 使用者 GitHub | 不需要 | 需要 |
| 地圖呈現 | 官方 share.geolibre.app + web.geolibre.app | 自架 GitHub Pages，官方 Viewer 作備援 |
| GitHub Pages / Actions | 不需要 | 需要 |
| GeoLibre 程式版本 | 官方 Web／Share 由官方維護更新 | **自架副本不會自動更新，需手動／主動同步官方上游** |
| Excel / CSV / report / summary | 對話附件／工作區檔案 | GitHub 長期公開檔案 |
| 長期版本留痕 | 一般 | **完整 Git commit / Actions / Pages** |
| 大型資料 | Project JSON 受官方 Share 50 MiB 上限影響 | **較適合大型、多檔案成果** |
| Token／流程效率 | **較省、步驟較少** | 較多 GitHub / CI / Pages 步驟 |
| 適合對象 | **一般使用者、同事、快速分析** | 正式稽核留存、固定公開網址、長期維護 |

## 固定輸出成果（兩版相同）

一般版與 GitHub 版對使用者顯示的成果名稱、順序固定一致：

1. **直接在你的 GeoLibre 開啟這次分析**
2. **GeoLibre 分析專案檔 map.geolibre.json**
3. **Excel 完整分析表 result.xlsx**
4. **CSV 查核結果 result.csv**
5. **分析報告 report.md**
6. **結果摘要 summary.json**

差別只在發布／驗證位置：一般版第 1、2 項使用官方 GeoLibre Share / Web Viewer；GitHub 版以自架 GitHub Pages 為主、官方 Viewer 為備援。其餘成果內容與驗收邏輯維持一致。

## 安裝路徑

GitHub 資料夾：

`ymguan3-boop/audit-codex-skills/skills/geolibre-analysis/`

安裝時將整個 `geolibre-analysis` 資料夾複製／同步到 Codex 個人技能目錄，不要只下載 SKILL.md，因為本技能還需要 `assets/` 與 `references/`。

GitHub 版請安裝：

`ymguan3-boop/audit-codex-skills/skills/geolibre-github-analysis/`

## 執行依賴檢核

一般版執行分析時**不使用 GitHub MCP、不建立 GitHub repository、不使用 GitHub Pages，也不以 GitHub Actions 作為分析或發布必要流程**。

README 中仍會出現 GitHub 字樣的原因只有兩種：

1. 本技能目前放在 GitHub 供下載／版本管理；
2. 說明何時應切換到另一套 `geolibre-github-analysis`。

這些都不是一般版任務執行依賴。

## 台灣公部門使用注意

一般版會把 `.geolibre.json` project 上傳到官方 `share.geolibre.app`。因此：

- 公開資料、開放資料、已去識別且可公開的分析成果，可優先使用一般版。
- 個人資料、未公開公務資料、敏感設施位置、資安／關鍵基礎設施資料或其他受限資料，**不得預設上傳官方 Share**。
- 遇到上述資料時，先依機關內部資安、個資、雲端與資料分級規範確認是否允許第三方服務；未確認前只做本機分析，不發布。
- 若資料不能送外部服務，應改用本機／機關自架 GeoLibre；若機關已核准 GitHub 雲端環境，才考慮 GitHub 版。

## 一次性設定

一般版正式上傳官方 GeoLibre Share 前，需要 `GEOLIBRE_SHARE_TOKEN`。Token 應存於執行環境 secret，不要貼在聊天或提交 GitHub。

詳細安裝與比較請見同層 `安裝與版本比較.md`。


> 版本更新補充：一般版直接使用官方 Web／Share，不維護使用者自己的 GeoLibre 程式副本；因此不需要做 GitHub 自架版的手動 upstream 同步。
