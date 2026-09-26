# GeoLibre GitHub 版技能

這是需要 GitHub 自架、GitHub Pages、GitHub Actions、長期公開網址與完整 Git 版本留痕時使用的**進階版**技能。

固定使用指令：

```
使用 GeoLibre GitHub 版技能
```

如果使用者只說「使用 GeoLibre 技能」，**不要**啟用本版，應使用一般版 `geolibre-analysis`。

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

`ymguan3-boop/audit-codex-skills/skills/geolibre-github-analysis/`

安裝時將整個 `geolibre-github-analysis` 資料夾複製／同步到 Codex 個人技能目錄。

一般版請安裝：

`ymguan3-boop/audit-codex-skills/skills/geolibre-analysis/`

## 適合 GitHub 版的情況

- 所有成果都要有長期公開 URL；
- 需要 Git commit / GitHub Actions / GitHub Pages 留痕；
- 大型資料或多檔案需要長期託管；
- 需要機關內部固定網址或自有部署；
- 不希望 GeoLibre project 上傳官方 Share。

詳細安裝與比較請見同層 `安裝與版本比較.md`。
