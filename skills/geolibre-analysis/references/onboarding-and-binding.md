# GeoLibre 首次導入與持久綁定

當目前沒有有效、已儲存的 GeoLibre profile 時，分析前先使用本流程。

## A. 先自動尋找既有綁定，避免打擾使用者

依序嘗試：

1. 本機快取：`$CODEX_HOME/geolibre-profile.json`；若不存在，退回 `~/.codex/geolibre-profile.json`。
2. 目前 repo：`.geolibre/skill-profile.json`。
3. 透過已連線 GitHub 搜尋精確標記 `geolibre_skill_profile_version`。
4. 因 GitHub code search 索引可能落後最新 commit，**若搜尋不到 profile，列出可存取的 repository，並直接向每個合理候選 repository 讀取 `.geolibre/skill-profile.json`**。404 只代表「尚未綁定」，應繼續檢查，不要因此詢問使用者。優先檢查使用者擁有或可 push 的 repository。
5. 若有疑似名為 GeoLibre 的 repository，檢查：
   - `.geolibre/skill-profile.json`
   - 含 GeoLibre workspace metadata 的 `package.json`
   - 或 `<source_path>/package.json` 加上官方 upstream 結構。

若找到一個有效 profile，自動綁定。

若找到多個 profile，依 repository 與 Pages URL 列出，讓使用者選擇。

完成上述檢查前，不要先詢問 GitHub 路徑。

## B. 使用者的 GitHub 已有 GeoLibre

只有在自動探索失敗後，才詢問 repository URL／路徑。

驗證：

- repository 可存取；
- 已授權使用者具備執行所需的寫入權限；
- 確認 default branch；
- 確認 GeoLibre 原始碼位於 repo 根目錄或子目錄；
- 檢查 GeoLibre 原始碼特徵；
- 可取得時，檢查 Pages 狀態／URL。

若 GeoLibre 原始碼存在，但沒有 profile，建立 `.geolibre/skill-profile.json` 並寫入本機快取。

## C. GitHub 尚未連線

若存在 GitHub connector／MCP 但尚未連線，先引導使用者完成連線。

若使用者表示沒有 GitHub 帳號：

1. 引導使用者前往 GitHub 註冊。
2. 說明帳號建立／驗證必須由使用者自行完成。
3. 使用者完成並返回後，連線 GitHub／MCP，再從 repository 設定繼續。

不得謊稱技能已替使用者建立或驗證 GitHub 身分。

## D. 尚未有 GeoLibre repository

預設建議：建立一個獨立 repository，通常為 `<owner>/GeoLibre`。

原因：Pages URL、升級、權限與分析隔離都較簡單。

支援兩種安裝模式：

### 1. standalone_repo（預設）

- Repo：`<owner>/GeoLibre` 或不衝突的替代名稱。
- `source_path = "."`
- 預設 `web_root = "GeoLibre-Web"`；只有在安裝方式直接把 app 發布於 repository Pages 根目錄時例外。
- `analysis_root = "<web_root>/analysis"`
- `task_script_root = "scripts/geolibre_tasks"`
- `task_manifest_path = "<web_root>/tasks/current-task.json"`

### 2. subdirectory

- 使用者提供的既有 repo。
- `source_path = "GeoLibre"`（或使用者明確選定的路徑）。
- 獨立偵測既有公開 web 目錄。**不要假設它一定在 `source_path` 裡。**
- 例如原始碼可能在 `GeoLibre/`，但公開網頁位於 repository 根目錄下的 `GeoLibre-Web/`。
- `web_root = <detected published web directory>`
- `analysis_root = "<web_root>/analysis"`
- `task_script_root = "scripts/geolibre_tasks"`，除非 repository 已存在另一個明確的任務程式目錄。
- `task_manifest_path = "<web_root>/tasks/current-task.json"`

若工具可以建立 repository，使用者同意後即可執行。

若無法直接建立：

- 有瀏覽器自動化時協助操作；或
- 只請使用者完成一個最少必要 UI 動作：建立空白 repository。

完成後立即繼續，不要重新詢問已完成的設定問題。

## E. 驗證官方 upstream

官方來源：

`https://github.com/opengeos/GeoLibre`

安裝／更新前：

1. 取得官方 repository metadata；
2. 可取得時解析最新穩定 release；
3. 否則使用 `main`；
4. 可取得時記錄選定 ref/tag 與 commit SHA。

不得默默切換到 fork。

## F. 將最新 GeoLibre 導入使用者 repository

不要透過 MCP 一個檔案一個檔案複製數千個原始碼檔案。

建議流程：

1. 建立正式 profile，並將 status 設為 `provisioning`。
2. 將 `assets/geolibre-bootstrap-pages.yml` 複製／調整到使用者的 `.github/workflows/geolibre-bootstrap-pages.yml`。
3. 透過 commit profile／workflow 或 workflow dispatch 觸發流程。
4. Workflow 依已記錄的 ref clone `opengeos/GeoLibre`，並同步到 `source_path`。
5. 保留技能擁有的路徑，例如 `.geolibre/`、分析成果、task scripts 與 skill workflows。
6. 使用 Node.js 22+ 建置。
7. 將 `GEOLIBRE_APP_BASE` 設為 GitHub Pages base path。
8. 將 `apps/geolibre-desktop/dist` 部署到 GitHub Pages。
9. 驗證 repository 原始碼與公開網站。
10. 將技能 asset `assets/optimize-project.py` 複製到 `.geolibre/tools/optimize-project.py`。
11. 確認分析 workflow 在每個 task script 執行後呼叫 optimizer。
12. 從 `assets/geolibre-profile.example.json` 加入預設 performance-budget 區塊。
13. 將 profile status 更新為 `ready`。

GeoLibre 官方 Vite 設定支援 `GEOLIBRE_APP_BASE`，因此 repository project-site 使用子路徑時應採用它。

## G. 啟用 GitHub Pages

只有在目前 credential／tool 具有所需 Pages／admin 權限時，才嘗試自動啟用。

若無法自動啟用，只要求使用者完成一次：

`Repository → Settings → Pages → Build and deployment → Source = GitHub Actions`

使用者完成後：

- 重新執行／接續 workflow；
- 驗證 Pages URL；
- 把 URL 儲存到 profile。

不要再要求使用者重新建立 repository。

## H. 持久 profile

正式路徑：

`.geolibre/skill-profile.json`

使用與 `assets/geolibre-profile.example.json` 相容的結構。

驗證成功後：

- 建立／更新正式 profile；
- 允許時寫入本機快取；
- 設定 `status = "ready"`；
- 更新 `last_verified_at`。

本機快取可以同時保存多個 profile 與一個 active profile。
不得儲存 access token、PAT、secret、API key 或 cookie。

## I. 後續使用

後續每次使用時：

1. 載入本機快取；
2. 對正式 profile 做輕量 repository 驗證；
3. 自動使用該 profile；
4. 只有需要時才更新 `last_verified_at`。

只有以下情況才重新導入：

- repository 已刪除或無法存取；
- 已失去寫入權限；
- 正式 profile 損壞；
- `source_path` 已不再包含 GeoLibre；
- 使用者明確要求綁定另一個 GeoLibre 專案。
