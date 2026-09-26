---
name: geolibre-github-analysis
description: |
  GeoLibre GitHub 自架版 GIS 分析技能。只有當使用者明確說「使用 GeoLibre GitHub 版技能」、
  「GeoLibre GitHub 版」或明確要求 GitHub repository、GitHub Pages、GitHub Actions、
  長期公開網址／完整 Git 版本留痕時使用。若使用者只說「使用 GeoLibre 技能」、
  「使用 GeoLibre」或「幫我用 GeoLibre 分析」，不得觸發本技能，應交由預設一般版
  geolibre-analysis 處理。本版自架 GeoLibre 不會自動追蹤上游新版；只有使用者明確要求更新時，
  才同步 opengeos/GeoLibre 並重新 build、部署與執行桌面＋Android Viewer QA。
---

# GeoLibre GitHub 自架版分析技能

當使用者以中文溝通時，預設使用繁體中文。

## 觸發規則（GitHub 版）

本技能不是預設 GeoLibre 技能。

只有以下情況才觸發：

- 使用者明確輸入「**使用 GeoLibre GitHub 版技能**」；
- 使用者明確指定「GeoLibre GitHub 版／GitHub 自架版」；
- 使用者要求以 GitHub repository、GitHub Pages、GitHub Actions 做長期公開、版本追蹤或成果留存。

若使用者只說：

- 「使用 GeoLibre 技能」
- 「使用 GeoLibre」
- 「幫我用 GeoLibre 分析」
- 「GeoLibre，我沒想法」

一律**不要**啟用本技能，應交由預設的一般版 `geolibre-analysis` 處理。


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

## 1A. GeoLibre 上游版本更新政策

GitHub 自架版必須視為**固定版本部署**。首次安裝後，不得在一般 GIS 分析任務中自動追蹤或自動升級 `opengeos/GeoLibre`。

只有在使用者明確要求下列意思時才更新上游：

- `更新 GeoLibre GitHub 版`
- `同步 GeoLibre 官方最新版`
- 明確要求升級目前自架 GeoLibre

更新流程：

1. 查詢官方 `opengeos/GeoLibre` Releases／tags。
2. 比對 profile 中的 `upstream_ref`、`upstream_commit` 與最新穩定版。
3. 告知目前版本與目標版本；若為 major version 升級或存在已知 breaking change，先取得使用者確認。
4. 備份／保留目前可回復的 commit。
5. 同步官方穩定 tag 或經使用者指定的 ref。
6. 重新 build 與部署 GitHub Pages。
7. 重新執行自架＋官方 Viewer 的桌面與 Android 真實畫面 QA。
8. 只有 QA 通過後，更新 profile 的 `upstream_ref`、`upstream_commit`、`last_verified_at`。

**更新 Skill 本身不等於更新 GeoLibre 開源程式；兩者必須分開管理。**

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


## 6A. 驗收失敗後的自動修復與完整重跑


### 強制規則：驗收不合格不得交付半成品

以下規則屬於**不可跳過的完成閘門**，優先級高於「先給使用者目前可用成果」的方便性考量：

1. 只要分析、檔案一致性、發布、Viewer、瀏覽器畫面或固定六項成果中的任何一項未符合技能規則，**不得直接進入最終成果回覆，也不得把現有檔案包裝成「完成版」交付**。
2. 必須先主動告知使用者：
   - 哪一項未通過；
   - 原因；
   - 對正式成果的影響；
   - 建議採取的最小修正方式。
3. 告知後不得停在建議。只要現有工具、公開資料、替代來源、其他可用執行環境或官方支援的替代載入方式可以解決，就必須**自行繼續處理到解決**。
4. 修復成功後，必須從**最早受影響的分析／產檔／發布步驟重新執行**，並重建所有受影響的正式成果；不得只補缺少的單一檔案或網址。
5. 修復後必須重新跑完整驗收。若又發現新問題，重複「建議 → 修復 → 重跑 → 全驗收」循環，直到全部通過。
6. 前一版、初篩版、失敗版、缺網址版、未完成 QA 版一律視為 **superseded／已由新版取代**，不得再作為最終交付。
7. **「直接在你的 GeoLibre 開啟這次分析」是必要成果，不是可選項。** 若尚未有已載入完整圖資專案且經真實瀏覽器驗證的可用網址，就表示輸出仍未完成。
8. 若官方 Share 暫時不可用，必須先檢查官方 Viewer 是否支援以其他匿名可讀、CORS 可用的公開 project URL 載入；若合法、安全且不違反本技能版本定位，應主動使用可行替代方案，不得因單一服務或 token 缺失就直接停止。
9. 只有在**確實只剩必須由使用者本人完成、且模型無法合法代替的外部授權／登入／付費／機關核准**時，才可暫停。此時只能回報「尚未完成」與唯一阻礙，不得輸出完成式固定六項成果。
10. 一旦該外部阻礙解除，必須立即從受影響步驟繼續，重新發布、重新 QA、重新產生或同步更新正式成果後，再交付最終版。

**禁止行為：**
- 發現驗收不合格後只給建議、不實際修復；
- 修復資料後不重跑正式分析；
- 修好 project 後沿用舊的 report／summary／XLSX；
- 沒有可用 Viewer URL 卻仍交付固定六項並稱為完成；
- 用下載檔案連結取代「已載入完整專案的 GeoLibre URL」；
- 因某個 API／token 不可用就直接停止，而未先尋找技能允許的替代發布方式。

**最終判定原則：不合格 → 建議 → 實際修復 → 完整重跑 → 完整驗收 → 才能最終交付。**

## 7. 確認後執行

當 `confirmed=true` 後，載入：

- `references/github-mcp-protocol.md`
- `references/performance-and-publishing.md`
- `references/output-contract.md`
- `references/report-writing-standard.md`
- `references/final-delivery-format.md`

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

最終回覆對使用者顯示的成果清單必須遵守 `references/final-delivery-format.md`，固定只顯示以下 6 項，順序與名稱不得自行擴充：

1. **直接在你的 GeoLibre 開啟這次分析**（同一項內固定提供「自架主要入口」與「官方 GeoLibre 備援入口」）
2. **GeoLibre 分析專案檔 map.geolibre.json**
3. **Excel 完整分析表 result.xlsx**
4. **CSV 查核結果 result.csv**
5. **分析報告 report.md**
6. **結果摘要 summary.json**


### 雙入口真實畫面驗證（強制完成條件）

在宣告 GeoLibre 分析完成前，必須對下列兩個入口做**真實瀏覽器畫面驗證**：

1. 自架 GitHub Pages GeoLibre
2. 官方 `https://web.geolibre.app/` 備援入口

兩個入口都必須使用同一份已發布的 `map.geolibre.json`。不得只檢查 HTTP 200、GitHub Pages deploy、`loading=ready` 或檔案存在。

每個入口至少驗證：

- App 不是白屏，根節點有實際內容；
- `data-geolibre-load-state=ready`；
- `data-geolibre-load-errors` 為空；
- 地圖 canvas 實際存在且不是全白／空畫布；
- 預期的主結果圖層名稱可在 UI／圖層面板找到；
- 畫面實際有地圖像素／圖徵內容，不是只有空殼 UI。

**至少一個入口必須同時通過桌面 Chromium 與 Android 手機 viewport 的上述全部檢查，否則不得宣告任務完成、不得把入口交付為可用成果，必須繼續修正。**

若目前聊天環境沒有瀏覽器自動化，必須改用可執行真實瀏覽器的方式（例如 GitHub Actions + Playwright）完成驗證，並保存 QA JSON 與截圖作為內部證據。不得把「沒有瀏覽器工具」當成跳過畫面驗證的理由。

若只有一個入口通過：最終回覆只把通過者標示為可用入口，另一個入口明確標示為「畫面驗證失敗／暫不可用」，但仍維持同一成果項目內顯示。

Repository 內部仍可正常產生並驗證 `result.geojson`、`overview.geojson`、`events.geojson`、`performance.json`、`source-snapshot.json`、`source-diagnostics.json`、`report.html`、截圖等完整成果，但**除非使用者明確要求完整技術清單，不得把這些檔案主動追加到一般最終回覆**。

最終回覆可在固定成果清單前用 1～3 個短段落說明分析結論與重要限制；成果清單標題固定為「## 成果已回寫你的自架 GeoLibre」。如果固定六項中的某一項未產出或無法開啟，保留該項位置並註明狀態，不得用其他技術檔案替代。詳見 `references/output-contract.md`、`references/report-writing-standard.md` 與 `references/final-delivery-format.md`。
