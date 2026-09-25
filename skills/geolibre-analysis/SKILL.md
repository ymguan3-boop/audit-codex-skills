---
name: geolibre-analysis
description: |
  GeoLibre GIS 空間分析的通用 Codex 技能。當使用者要求使用 GeoLibre、進行 GIS／空間分析、
  尋找風險點位，或需要互動地圖與結構化成果時使用。若使用者沒有想法，先提供 16 個以上主題分類，
  再依所選主題提供 3～5 個可直接執行的分析建議。解析或建立使用者自己的 GitHub GeoLibre 綁定，
  逐步確認分析規格，透過 GitHub MCP、Python 與 GeoLibre 工具執行可重現分析，最後交付經驗證的
  GeoLibre 地圖；若可使用瀏覽器自動化，另提供真正的 GeoLibre 畫面截圖，以及 XLSX、GeoJSON、
  分析摘要與報告。後續使用時優先沿用已儲存的綁定，不要重複詢問 GitHub 路徑。
---

# GeoLibre 分析技能

當使用者以中文溝通時，預設使用繁體中文。

這是一個**多人可共用的通用技能**。不得把技能作者本人的 GitHub 帳號或倉庫硬編碼成執行目標。

本技能分成三個階段：

1. **綁定／首次導入（BINDING / ONBOARDING）**：尋找、驗證或建立目前使用者自己的 GitHub GeoLibre，並記住其位置。
2. **需求探索（DISCOVERY）**：透過漸進式提問，把已有想法或「沒有想法」整理成完整 GIS 分析規格。
3. **執行（EXECUTION）**：只有在使用者最後明確確認後，才使用 GitHub MCP 對已綁定的 GeoLibre 專案執行分析並驗證成果。

## 0. 一律先解析 GeoLibre 綁定

在開始 GIS 提問或執行前，先解析出有效的 `geolibre_profile`。

載入 `references/onboarding-and-binding.md`。

解析順序：

1. 若可存取，先讀取本機快取 `$CODEX_HOME/geolibre-profile.json`；若不存在，再嘗試 `~/.codex/geolibre-profile.json`。
2. 若目前倉庫含有 `.geolibre/skill-profile.json`，讀取該檔。
3. 若 GitHub 已連線，搜尋目前授權使用者可存取的倉庫，尋找標記 `geolibre_skill_profile_version`。
4. **不要只依賴程式碼搜尋索引。** 若搜尋不到標記或結果可能尚未更新，列出可存取的候選倉庫，直接檢查其標準路徑 `.geolibre/skill-profile.json`。直到範圍內所有合理候選倉庫都已檢查，或找到有效 profile 為止。
5. 若只找到一個有效 profile，直接使用並更新本機快取。
6. 若找到多個 profile，列出其 repo 與 Pages URL，讓使用者選擇；之後記住該選擇。
7. 若完全找不到，進入首次導入流程。
8. 若使用者直接提供 GitHub repository URL 或路徑，驗證後直接綁定。

若已有有效的已儲存 profile，**不要再次詢問 GitHub 路徑**。

正式 profile 位於使用者自己的 GeoLibre 倉庫：

`.geolibre/skill-profile.json`

本機快取只是加速工具。GitHub 內的 profile 才是主要依據。

## 1. 首次使用導入流程

如果找不到有效的 GeoLibre profile：

- 若 GitHub 尚未連線，引導使用者先連接 GitHub／MCP。
- 若使用者沒有 GitHub 帳號，引導其建立帳號。帳號註冊、身分驗證、CAPTCHA、passkey、條款同意或其他需真人操作的步驟，必須由使用者自行完成；不得假裝已自動完成。
- 若目前工具可以建立 repository，可主動提出自動建立一個名為 `GeoLibre` 的專用 repository；若名稱衝突，使用安全的不重複名稱。
- 若無法直接建立 repository，有瀏覽器自動化時可協助操作；否則只要求使用者完成最少必要的 GitHub UI 步驟來建立空白 repository，使用者回報完成後立即繼續。
- 預設建議使用獨立的 GeoLibre repository；若使用者選擇，也支援把 GeoLibre 放在既有 repository 的 `GeoLibre/` 子目錄。
- 安裝前立即驗證官方上游。正式來源為 `opengeos/GeoLibre`；不得未經說明改用非官方 fork。
- 若能解析穩定版本，優先採用最新穩定公開版本；必要時才改用最新 `main`。記錄 upstream repo、ref/tag、已知 commit SHA 與安裝時間。
- 優先透過 GitHub Actions 建置原始碼，不要透過 MCP 一個檔案一個檔案上傳數千個來源檔。
- 將網頁版本部署到 GitHub Pages。
- 只有在 repository、原始碼與 Pages 驗證成功後，才建立正式 profile 與本機快取。

使用 `assets/geolibre-bootstrap-pages.yml` 作為部署模板，並依實際 branch／path 調整佔位值。

若目前 GitHub 憑證無法啟用 GitHub Pages，只要求使用者完成一次必要 UI 操作：

`Repository → Settings → Pages → Build and deployment → Source: GitHub Actions`

完成後接續驗證部署，不要重新開始整個導入流程。

## 2. 綁定資料模型

維護一份 `geolibre_profile`，至少包含：

- `geolibre_skill_profile_version`
- `github_owner`
- `repo_full_name`
- `default_branch`
- `install_mode`：`standalone_repo` 或 `subdirectory`
- `source_path`：GeoLibre 原始碼位置，例如 `.` 或 `GeoLibre`
- `web_root`：公開／靜態 GeoLibre 網頁根目錄；可與 `source_path` 不同，例如 `GeoLibre-Web`
- `analysis_root`
- `task_script_root`
- `task_manifest_path`
- `pages_url`
- `pages_base_path`
- `upstream_repo`：通常為 `opengeos/GeoLibre`
- `upstream_ref`
- `upstream_commit`（若已知）
- `last_verified_at`

Profile schema／範例：`assets/geolibre-profile.example.json`。

每次執行前只做輕量驗證：

- repository 仍存在；
- 使用者仍具有必要讀寫權限；
- 正式 profile 仍相符；
- 核心原始碼／建置檔仍存在。

若上述檢查通過，不要重新執行完整導入流程。

## 3. GIS 分析的對話狀態

維護內部 `analysis_spec`，包含：

- `topic`
- `analysis_goal`
- `geographic_scope`
- `time_range`
- `target_features`
- `input_layers`
- `spatial_rules`
- `thresholds`
- `filters`
- `data_source_preference`
- `outputs`
- `task_id`
- `confirmed`

使用者已提供的欄位，不要重複詢問。

## 3A. 進入流程

若使用者的需求很模糊，例如「使用 GeoLibre 技能」、「幫我做 GIS 分析」或「我沒想法」，
不要立刻開始寫程式。

若使用者已經提供具體 GIS 問題，直接略過發想階段，只補問分析規格中尚缺的必要欄位。

若使用者尚未提供具體題目，只問：

- **A. 有，我直接描述需求**
- **B. 還沒有，請先給我主題讓我選**

若使用者選 B，顯示 `references/topic-catalog.md` 中的精簡主題選單。
選定主題後，提供 3～5 個完整、可直接執行的分析題目，讓使用者選一個或自行輸入。
一旦題目選定，除非使用者主動要求，不要再回到主題選單。

## 4. 使用者沒有想法時

若使用者表示沒有想法，或在進入流程中選擇 B，顯示 `references/topic-catalog.md` 的精簡編號主題選單。
先顯示 12～17 個短主題名稱，不要一次展開所有範例。

選定主題後：

1. 提供 3～5 個符合該主題、可直接執行的分析建議。
2. 讓使用者選擇其中一個，或自行輸入需求。
3. 將選擇轉成 `analysis_goal`。
4. 之後只詢問尚缺、且會影響決策的必要參數。

使用者仍在探索題目時，不要開始執行分析。

## 5. 漸進式需求確認

每回合以少量問題為原則，最好一次詢問 1～3 個彼此相關的問題。

至少確認：

1. **在哪裡？** 縣市、鄉鎮市區、指定範圍或使用者上傳的邊界。
2. **什麼期間？** 若分析與時間有關，確認年份或日期範圍。
3. **要找什麼？** 道路、地籍、建物、事件、公共設施、邊坡、河川等。
4. **什麼空間關係？** within／intersects／nearest／buffer／density／overlap／network relationship 等。
5. **門檻是多少？** 距離、次數、排序、風險級別、時間窗等。
6. **使用哪些資料？** 除非使用者另有要求，優先採用免費／公開資料與既有已驗證專案資料來源。
7. **要輸出什麼？** 預設至少提供 GeoLibre 地圖與結構化表格；必要時確認 CSV／XLSX／GeoJSON／報告／截圖。

若有合理預設值，先提出建議，再讓使用者接受或修改。

若指定的公開圖層不存在或無法取得，說明缺口、提出替代來源後再繼續。不得默默刪除已確認的分析條件。

## 6. 執行前確認關卡

分析規格完整後，顯示精簡的**分析設定摘要**：

- 分析主題
- 分析目標
- GeoLibre 綁定位置（只顯示 repo，不可暴露 credentials）
- 範圍
- 時間
- 使用圖層
- 空間條件與門檻
- 篩選條件
- 輸出成果

然後詢問：

- **確認執行**
- **修改設定**
- **取消**

只有清楚無歧義的最終同意，例如 `確認執行`、`開始分析` 或 `執行`，才可設定 `confirmed=true`。

單純選擇主題或中途回答「可以」，除非很明確是在核准最後摘要，否則都不算正式執行授權。

## 7. 確認後執行

當 `confirmed=true` 後，載入：

- `references/github-mcp-protocol.md`
- `references/performance-and-publishing.md`
- `references/output-contract.md`
- `references/report-writing-standard.md`

在產生任務程式時就套用效能規則，不要等成果完成後才補做最佳化。

實際執行目標必須來自 `geolibre_profile`，不得把特定 repository 硬編碼進技能。

流程模式：

`GitHub MCP -> user's GeoLibre repo -> GitHub Actions -> Python GIS analysis -> GeoLibre-ready outputs -> published/accessible results`

在安全前提下重用既有專案資料與程式。不要不必要地覆寫其他分析成果或上游 GeoLibre 原始碼。

## 8. 必要成果契約

在 `<analysis_root>/<task_id>/` 下，依 `references/output-contract.md` 產出完整成果。

最低成果包括：

- `map.geolibre.json` — 輕量的預設 GeoLibre 瀏覽專案
- `overview.geojson` — 當結果超過大型成果門檻時產生
- `result.geojson` — 完整、正式的向量分析結果
- `result.csv`
- `result.xlsx` — 當成果適合表格化時產生
- `summary.json`
- `report.md`
- `performance.json`
- `index.html` — 能正確處理 URL encoding 的穩定公開入口
- `map-overview.png` — 可使用瀏覽器自動化時，從真正 GeoLibre 頁面擷取的畫面
- 可選 `map-detail-01.png`、`map-detail-02.png` — 用於重要群聚或細節

GeoLibre 地圖首次開啟時，必須對準有意義的結果範圍，並預設顯示最重要的 overview／result 圖層。
若結果很大，預設 project 不得把完整分析資料全部內嵌進去。

XLSX 適用時，至少包含：

- 分析結果
- 統計摘要
- 分析參數
- 資料來源

結果表格應盡量包含可讀名稱、行政區、座標／幾何識別碼、判斷值，以及能說明「為什麼這筆被選中」的明確原因欄位。

## 9. 驗證

不能只因為檔案已 commit，就宣稱分析成功。

在宣告分析完成前：

1. 驗證任務程式與 manifest。
2. 確認 GitHub Action 已完成，或預期成果檔確實已產生。
3. 檢查 `summary.json` 與 `report.md`。
4. 確認 `map.geolibre.json` 確實包含或引用預期結果。
5. 檢查 `performance.json`，並要求 project 大小、inline layer 與 initial-load 的硬性預算全部通過。
6. 若結果很大，確認預設地圖使用 `overview.geojson` 或其他刻意設計的輕量摘要，而不是直接載入完整分析資料集。
7. 若成果需要公開部署，確認已儲存的公開 GeoLibre URL 仍能正常載入。
8. 若可使用瀏覽器自動化，開啟實際 GeoLibre URL 並加上 `loading=true`，等待
   `data-geolibre-load-state=ready`，檢查 `data-geolibre-load-errors`，並核對圖層面板與畫面上實際可見的圖徵；`ready` 與效能預算通過不等於圖層已畫出。成功後再擷取畫面。
   不得把另外用 matplotlib 或其他方式畫出的靜態地圖，冒充成 GeoLibre 實際畫面截圖。
9. 比對 XLSX 的結果資料列數與正式 GeoJSON feature count；若不同，必須說明原因。
10. 說明資料限制、替代來源，以及任何僅供顯示使用的簡化處理。

若執行失敗，先檢查 logs，採用最小必要修正後重試；不得為了讓流程通過而弱化使用者已確認的分析條件。

## 10. 變更控管

使用者最後確認分析設定，代表授權進行該任務所需的 repository 變更。

以下情況必須重新取得明確確認：

- 刪除既有專案檔案；
- 覆寫與目前任務無關的分析成果；
- 修改與任務無關的 repository 全域基礎架構；
- 新增付費或私有資料來源；
- 變更已確認的 GIS 判斷條件；
- 把使用者已綁定的 GeoLibre repository 替換成另一個 repository。

一般任務所需的腳本、manifest、輸出檔，以及正常 profile 更新，不需要第二次確認。

## 11. 完整正式報告與逐項交付

`report.md` 必須遵守 `references/report-writing-standard.md` 的**強制格式**。這份格式以既有完整 GeoLibre 分析報告為基準，優先確保方法、分類、資料品質、限制、來源與交付資訊完整，不得為了「白話化」而把正式報告退化成摘要版、簡報版或只有主要發現的短文。

### report.md 不可省略的固定骨架

標題後先放任務摘要，再依序保留以下章節，章名不得任意改名或被其他章節取代：

1. `## 方法`
2. `## 分類`
3. `## 資料品質`
4. `## 重要限制`
5. `## 資料來源`
6. `## 交付檔案`

開頭任務摘要至少列出 task id、範圍、期間、主要空間門檻、核心判斷條件、可分析筆數、正式結果數與重要子結果數。

完成上述固定骨架後，才可依新版成果契約追加「主要發現」、「圖層—圖資—檔案對照」、「地圖圖層說明」、「效能與發布驗證」、「瀏覽器畫面驗證」、「後續查核建議」與「總結」。**追加內容只能補強，不得取代原本固定章節。**

相交與鄰近、空間群聚與時間重複、查核優先與法定風險不得混稱。若某固定章節本案不適用，也要保留章節並明確寫出不適用原因。若 Pages 把 Markdown 當原始文字顯示，另產生可讀的 `report.html` 或等效入口。

在宣告報告完成前，必須逐項驗證 `report.md` 有標題、任務摘要、方法、分類、資料品質、重要限制、資料來源與交付檔案；任一缺漏都視為報告未完成。

最終回覆必須逐項列出**實際驗證存在**的地圖入口、主結果 GeoJSON／CSV／XLSX、重要子集、範圍圖、摘要、報告、效能檢查、確實產出的截圖／overview；每項附可開啟連結、筆數或範圍、對應的圖層／用途，說明來源與限制。未產出、未發布或未通過瀏覽器圖層驗證者要明示，不能當成已交付。詳見 `references/output-contract.md` 與 `references/report-writing-standard.md`。
