---
name: github-mcp-setup
description: MCP 至 GitHub 設定技能 — 設定 GitHub 遠端 MCP、Git/gh 工具、瀏覽器或終端機登入、推送驗證及完整疑難排解。說「連接 GitHub」「GitHub MCP」「github-mcp-setup」時載入。
---

# MCP 至 GitHub 設定技能

> 版本：v1.0（2026-10-07）
> 實戰驗證環境：Windows + OpenCode，遠端 MCP `https://api.githubcopilot.com/mcp/`。
> 本技能記錄實際踩雷後整理出的**正確步驟**，請依序執行，不要跳過帳號檢查。

## 這個技能會幫你做什麼？

- ✅ 檢查 Git / GitHub CLI 是否已安裝（缺則以 winget 補裝）
- ✅ 確認 GitHub **帳號身分**（避免多帳號登錯，見步驟零）
- ✅ 建立 GitHub 認證（二選一：終端機 `gh auth login`，或純瀏覽器 PAT 流程）
- ✅ 寫入 OpenCode GitHub 遠端 MCP 設定（PAT 模式）
- ✅ 設定 Git 使用者資訊（由 GitHub profile 自動帶入）
- ✅ 推送驗證（Contents API 或 git push）並回報 commit
- ✅ 用完即撤銷 token 的收尾流程

## 先備條件

- [ ] 已有 GitHub 帳號，且知道正確的帳號名稱（例如 `ymguan3-boop`）
- [ ] 電腦有網路連線
- [ ] （純瀏覽器流程）可開啟 github.com 並登入

---

## 步驟零：確認帳號身分（強制，不可跳過）

> **多人實測最大坑：瀏覽器登入了錯誤的帳號。** 例如倉庫在 `ymguan3-boop` 名下，
> 但瀏覽器登入的是另一個帳號（如 `cd010011`），則任何授權都寫不進目標倉庫
>（讀公開檔可能 404 偽裝、寫入 403），且錯誤訊息不會告訴你是帳號問題。

1. 先問使用者：**目標倉庫在哪個帳號/組織名下？**（例如 `ymguan3-boop/audit-codex-skills`）
2. 每次拿到任何 token 後，第一件事就是驗身分（**只印 login，不印 token**）：
   ```powershell
   $H = @{Authorization="Bearer $tok"; Accept="application/vnd.github+json"}
   (Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $H).login
   ```
3. 若回傳的 login 與目標倉庫擁有者不符 → **停止**，請使用者切換瀏覽器帳號後重做授權。

## 步驟一：檢查 Git 與 GitHub CLI

```powershell
& "C:\Program Files\Git\cmd\git.exe" --version
& "C:\Program Files\GitHub CLI\gh.exe" --version
& "C:\Program Files\GitHub CLI\gh.exe" auth status
```

未安裝時以 winget 補裝（會跳 UAC，按允許）：

```powershell
winget install --id Git.Git --accept-source-agreements --accept-package-agreements
winget install --id GitHub.cli --accept-source-agreements --accept-package-agreements
```

## 步驟二：建立 GitHub 認證（依使用者偏好二選一）

### 方式 A：終端機 `gh auth login`（最穩，推薦可開終端機者）

使用者在**可互動的** PowerShell 執行：

```powershell
gh auth login --web --git-protocol https
```

流程：終端機顯示一次性驗證碼 → 瀏覽器自動開啟 `github.com/login/device` →
輸入驗證碼授權 → 回終端機以 `gh auth status` 確認看到
`Logged in to github.com account <正確帳號>`。

> ⚠️ Agent 的 shell 非互動式，跑 `gh auth login` 會卡住逾時，**必須由使用者親自執行**。

### 方式 B：純瀏覽器 PAT 流程（不開終端機）

1. 瀏覽器確認右上角是**正確帳號**後，開
   `https://github.com/settings/personal-access-tokens/new`（細粒度 token）。
2. 逐項設定（缺一即 403/404）：
   - Token name：如 `opencode-push`；期限選短（7 天）
   - **Repository access：Only select repositories → 勾選目標倉庫**
    （若勾到別的倉庫，對目標倉庫讀寫一律 404/403）
   - **Repository permissions → Contents：Read and write**
    （預設 No access，這是最常見出錯點）
3. Generate token 並複製（`github_pat_` 開頭，約 93 字元）。
4. Token 傳遞（三選一，**不要只用看的，要驗長度**）：
   - `setx GITHUB_PERSONAL_ACCESS_TOKEN "貼上"`（使用者終端機，最乾淨）
   - 存記事本/Word 告知路徑，由 Agent 讀取（讀到後驗 `TOKEN_LEN` 約 93）
   - 直接貼對話（最後手段；用完立即到設定頁刪除該 token）
5. Agent 驗證（只印 login 與長度，不印 token 本體）：
   ```powershell
   (Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $H).login
   ```

### 不要用的方式

- ❌ 自行拼裝 OAuth 裝置流程（`POST github.com/login/device/code`）：
  實測未知 client_id 一律 404；即使從 gh 主程式挖出可用 ID，
  拿到的 token 也可能是 GitHub App 綁定型，對未安裝該 App 的倉庫
  讀檔 404、寫入 403 `Resource not accessible by integration`。
- ❌ OpenCode `/mcps` 對 GitHub 遠端直接按登入：
  會報 `Incompatible auth server: does not support dynamic client registration`，
  GitHub OAuth 不支援動態客戶端註冊，必須用 PAT 模式（步驟三）。

## 步驟三：寫入 OpenCode GitHub 遠端 MCP 設定

全域設定檔 `~/.config/opencode/opencode.json`（Windows：
`C:\Users\[使用者]\.config\opencode\opencode.json`）：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "github": {
      "type": "remote",
      "url": "https://api.githubcopilot.com/mcp/",
      "enabled": true,
      "oauth": false,
      "headers": {
        "Authorization": "Bearer {env:GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

要點：

- `oauth: false` 是關鍵，關掉 OpenCode 自動 OAuth 探索（否則撞上動態註冊錯誤），
  改走 PAT 標頭；`{env:...}` 讓 token 留在環境變數，不寫死在設定檔。
- 寫入後**完全重啟 OpenCode**，再到 `/mcps` 確認 `github` 顯示已連接。
- token 到期或撤銷後 MCP 會斷線，重做方式 B 換 token 並更新環境變數即可。

## 步驟四：設定 Git 使用者資訊

由 GitHub profile 自動帶入（附 fallback），免手問：

```powershell
$me = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $H
$nm = $me.name; if ([string]::IsNullOrEmpty($nm)) { $nm = $me.login }
& "C:\Program Files\Git\cmd\git.exe" config --global user.name $nm
& "C:\Program Files\Git\cmd\git.exe" config --global user.email "$($me.id)+$($me.login)@users.noreply.github.com"
```

## 步驟五：推送驗證

以 Contents API 更新一檔為驗證（把 `<PATH>`、`訊息`、`本機檔`換掉）：

```powershell
$path = "<倉庫路徑，如 skills/xxx/SKILL.md>"
$cur = Invoke-RestMethod -Uri "https://api.github.com/repos/<擁有者>/<倉庫>/contents/$path?ref=main" -Headers $H
$bytes = [IO.File]::ReadAllBytes("<本機檔完整路徑>")
$b64 = [Convert]::ToBase64String($bytes)
$put = @{message="<commit 訊息>"; content=$b64; sha=$cur.sha; branch="main"} | ConvertTo-Json
$res = Invoke-RestMethod -Uri "https://api.github.com/repos/<擁有者>/<倉庫>/contents/$path" -Method Put -Body $put -ContentType "application/json" -Headers $H
$res.commit.sha  # 回報此值
```

> 注意：Windows PowerShell 5.1 **不支援 `??`** 運算子，寫腳本請用 `if` 代替；
> 檔名含中文請用 `Get-ChildItem -Filter "*.txt"` 等萬用字元避開編碼問題。

## 步驟六：收尾（撤銷 token）

1. Agent 刪除本機暫存（含 token 的 txt/docx、暫存檔），**保留** gh 標準登入檔與環境變數
   （MCP 持續連線需要；token 到期再換）。
2. 若 token 是貼在對話或僅一次性用途，請使用者到
   `https://github.com/settings/personal-access-tokens` 刪除該 token。
3. 回報完成格式（含 commit sha 與 `/mcps` 狀態）。

---

## 常見問題（詳細）

| 現象 | 原因 | 解法 |
|---|---|---|
| `/mcps` 按登入報 `does not support dynamic client registration` | GitHub 不支援動態客戶端註冊 | 改步驟三 PAT 模式（`oauth:false` + Bearer 標頭） |
| 公開檔 GET 404、PUT 403 `Resource not accessible by personal access token` | PAT 的 Repository access 沒勾目標倉庫，或 Contents 非 Read and write | 回 token 設定頁修正（先備：帳號正確）；**改完等數分鐘才會全域生效**，期間 404/403 交錯出現屬正常，重試即可 |
| PUT 403 `Resource not accessible by integration` | 拿到的是 GitHub App 綁定型 token，該 App 未安裝於目標倉庫或無 contents 權限 | 棄用裝置流程拼裝，改方式 A 或 B |
| `gh auth login` 在 Agent shell 卡住 | 非互動式 shell 無法回答提示 | 必須使用者親自開 PowerShell 執行 |
| `??` 報 ParserError | Windows PowerShell 5.1 不支援 null-coalescing | 改 `if ([string]::IsNullOrEmpty(...))` |
| 中文檔名在 shell 變亂碼 | 主控台編碼轉換 | 用萬用字元（`*.txt`）或 ASCII 檔名傳遞 |
| `.txt` 存檔 0 位元組 | 貼上後未存檔或存到別處 | 全機搜當日 `.txt`；改存 Word 或直接貼對話 |
| 同一 URL 一下 200 一下 404 | PAT 權限異動後端 propagation 中 | 等數分鐘後重試；重試迴圈以成功為準，不要只試一次就下結論 |
| `422 For 'properties/sha', nil is not a string` | 前一步 GET 失敗導致 sha 為空就 PUT | 先確保 GET 拿到 sha 再 PUT |

## 完成回報格式

```md
## GitHub 連接完成

- Git：已安裝 / 已補裝（版本）
- GitHub CLI：已安裝 / 已補裝（版本）
- 認證方式：gh 終端機登入 / 瀏覽器 PAT（帳號：xxx）
- Git 使用者資訊：已設定（name / noreply email）
- GitHub MCP：opencode.json 已寫入，/mcps 狀態
- 推送驗證：成功（commit sha）/ 未執行
- token 收尾：已刪暫存 / 已撤銷 / 環境變數保留至到期
```

## 更新紀錄

| 日期 | 版本 | 更新內容 |
|---|---|---|
| 2026-10-07 | v1.0 | 初版：實戰驗證（多帳號、PAT 權限、propagation、動態註冊限制、PS5.1 相容）後整理 |
