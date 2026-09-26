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

## 開源程式版本更新（重要）

GitHub 自架版安裝的是某一個時間點的 GeoLibre 上游程式碼，**不會因官方 `opengeos/GeoLibre` 發布新版而自動更新**。

因此：

- 自架站平常分析時維持已驗證的版本，不自動升級。
- 要更新 GeoLibre 開源程式，必須由使用者**手動／主動觸發**。
- 建議固定指令：`更新 GeoLibre GitHub 版`。
- 更新時先查官方 Releases／tag，優先採最新穩定版，不直接追未驗證的開發版。
- 更新前記錄目前 `upstream_ref`／`upstream_commit`；更新後重新 build、部署 GitHub Pages，並重新做桌面＋Android 的自架與官方 Viewer QA。
- 若新版造成 project schema、圖層樣式或 URL 載入方式不相容，必須修復並通過 QA 後，才能把新版標成可用。
- 技能本身的更新與 GeoLibre 上游程式更新是兩件不同的事；更新 Skill 不代表自架 GeoLibre 已升級。

## 適合 GitHub 版的情況

- 所有成果都要有長期公開 URL；
- 需要 Git commit / GitHub Actions / GitHub Pages 留痕；
- 大型資料或多檔案需要長期託管；
- 需要機關內部固定網址或自有部署；
- 不希望 GeoLibre project 上傳官方 Share。

詳細安裝與比較請見同層 `安裝與版本比較.md`。
