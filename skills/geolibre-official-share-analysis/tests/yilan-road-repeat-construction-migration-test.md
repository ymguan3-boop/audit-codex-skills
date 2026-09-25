# 遷移測試：宜蘭縣道路工程重複施工分析

## 測試目標

驗證既有 GeoLibre 分析成果是否能在不使用使用者 GitHub Pages 的情況下，改由官方 share.geolibre.app + web.geolibre.app 呈現。

測試來源：
- 任務：yilan-road-repeat-construction-audit-2026-09
- 原成果：既有 map.geolibre.json / result.xlsx / result.csv / report.md / summary.json

## 新技能 preflight

結果：**PASS**

檢查結果：

- map.geolibre.json 約 63,051 字元，遠低於官方 Share 50 MiB project 上限。
- project 共 2 個 GeoJSON 圖層。
- repeat-hotspots：inline GeoJSON，2 features。
- construction-events：inline GeoJSON，53 features。
- 沒有 source.data 外部 GeoJSON URL。
- 沒有需要 GitHub Pages 才能載入的分析資料檔。
- 因圖資已 inline，Share server 只保存 project JSON 的限制不會導致本案圖層遺失。
- 原 Excel / CSV / report.md / summary.json 可由新技能直接產生為對話附件，不必放在 GitHub。

## 預期官方成果

若 Share token 已設定，流程應為：

1. 使用 assets/share-project.py 對 project 執行 preflight。
2. POST /api/projects，上傳 visibility=unlisted。
3. 取得 rawJsonUrl / projectUrl。
4. 以 web.geolibre.app + rawJsonUrl 建立官方 viewer URL。
5. 桌面 Playwright 驗證。
6. Android viewport Playwright 驗證。
7. QA 通過後交付固定 6 項成果。

## 目前阻塞

狀態：**AUTH SETUP REQUIRED**

原因：
- share.geolibre.app 的 POST /api/projects 是 authenticated endpoint。
- 新技能刻意不保存、也不硬編碼使用者 token。
- 目前測試環境沒有 GEOLIBRE_SHARE_TOKEN。
- ChatGPT Plugin Directory 目前也沒有 GeoLibre connector 可直接代替官方 Share 驗證。

這不是 GitHub 依賴；是官方 GeoLibre Share 自己要求的帳號／Bearer credential。

## 一次性設定方式

使用者到：
https://share.geolibre.app/settings

建立個人 API token，至少需要能讀寫自己的 projects。
若要直接 public 發布，再允許 public sharing scope。

Token 應存成 Codex／執行環境 secret：
GEOLIBRE_SHARE_TOKEN

禁止把 token 貼入聊天、提交 GitHub 或寫入 SKILL.md。

## 測試結論

- 架構可行：PASS。
- 本案例資料結構可直接遷移：PASS。
- GitHub Pages 可從執行流程移除：PASS。
- 官方 viewer 可作唯一互動地圖入口：PASS（依官方 Share / Viewer 合約）。
- XLSX / CSV / report.md / summary.json 可保持相同輸出：PASS，但改為對話附件，不是 share.geolibre.app 託管。
- 實際官方 Share 上傳：PENDING，一次性 token 設定後才能完成。
