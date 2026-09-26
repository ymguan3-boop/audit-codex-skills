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
| Excel / CSV / report / summary | 對話附件／工作區檔案 | GitHub 長期公開檔案 |
| 長期版本留痕 | 一般 | **完整 Git commit / Actions / Pages** |
| 大型資料 | Project JSON 受官方 Share 50 MiB 上限影響 | **較適合大型、多檔案成果** |
| Token／流程效率 | **較省、步驟較少** | 較多 GitHub / CI / Pages 步驟 |
| 適合對象 | **一般使用者、同事、快速分析** | 正式稽核留存、固定公開網址、長期維護 |

## 安裝路徑

GitHub 資料夾：

`ymguan3-boop/audit-codex-skills/skills/geolibre-analysis/`

安裝時將整個 `geolibre-analysis` 資料夾複製／同步到 Codex 個人技能目錄，不要只下載 SKILL.md，因為本技能還需要 `assets/` 與 `references/`。

GitHub 版請安裝：

`ymguan3-boop/audit-codex-skills/skills/geolibre-github-analysis/`

## 一次性設定

一般版正式上傳官方 GeoLibre Share 前，需要 `GEOLIBRE_SHARE_TOKEN`。Token 應存於執行環境 secret，不要貼在聊天或提交 GitHub。

詳細安裝與比較請見同層 `安裝與版本比較.md`。
