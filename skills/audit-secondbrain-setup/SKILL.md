---
name: audit-secondbrain-setup
description: 審計第二大腦安裝及設定技能 — 從零開始建置 Obsidian + MCP + CLAUDE.md 審計專屬 AI 知識管理系統。說「第二大腦安裝」「審計第二大腦設定」「secondbrain-setup」時載入。
---

# 審計第二大腦安裝及設定技能

> 版本：v3.2（擷取自合併版）
> 本技能包含環境檢查、Obsidian Vault 建立、MCP 連接、CLAUDE.md 班規設定、Templates 建立、Web Clipper 設定、每週知識重整排程、批次轉換腳本等完整安裝流程。

## 這個技能會幫你做什麼？

從零開始建置審計專屬的 AI 第二大腦系統，一次完成所有步驟：

- ✅ 環境檢查與工具安裝（Node.js、Pandoc、Tesseract OCR、Python 轉換套件、Selenium）
- ✅ 安裝 mcpvault MCP Server（讓 OpenCode 能讀寫筆記）
- ✅ 批次檔案轉換腳本（docx、xlsx、pdf、圖片 → md，輸入 `/資料處理` 即可執行）
- ✅ 建好三層資料夾結構（資料蒐集 → 資料處理 → 資料庫建置及產出）
- ✅ 設定好 OpenCode 的工作規則（CLAUDE.md）
- ✅ 建好常用的筆記模板
- ✅ 設定每週自動知識重整排程
- ✅ 查核意見自動分類（依查核主題、建議事項、查明處理事項、注意事項等）
- ✅ 法規 PCode 自動查詢工具（get_pcode.py）
- ✅ 設定每週自動知識重整排程

完成後，使用者只要做這些事：
1. **平時**：原始檔案（docx/pdf/圖片）放進 `資料蒐集/`
2. **轉換**：輸入 `/資料處理` 批次轉換成 MD 並自動分類
3. **生成調查計畫**：使用「生成調查計畫技能」
4. **生成工作底稿**：使用「生成工作底稿技能」
5. **每週日**：OpenCode 自動幫你整理成知識庫

## 先備條件

在使用這個技能之前，請確認：
- [ ] OpenCode 桌面版已安裝且能正常使用
- [ ] 電腦有網路連線
- [ ] Python 3.8 以上已安裝（若無則安裝流程會自動安裝）

---

## 安裝流程

### 步驟一：環境檢查

> 在開始前，先自動確認以下所有項目。如果有任何一項不符合，先告知使用者問題所在，引導解決後再繼續。**不要跳過任何一項檢查，不要假設環境正常。**

1. **確認作業系統**：執行系統指令確認是 Windows / macOS / Linux
2. **確認網路連線正常**
3. **檢查 Node.js 是否已安裝**：
   - Windows 重要提醒：OpenCode 的 bash 環境可能找不到 `node`
   - 先嘗試 `node --version`
   - 若失敗，嘗試 `export PATH="/c/Program Files/nodejs:$PATH" && node --version`
   - 若仍失敗，請安裝：
     - Windows：`winget install --id OpenJS.NodeJS --accept-source-agreements --accept-package-agreements`
     - macOS：`brew install node`
     - Linux：`sudo apt update && sudo apt install nodejs npm -y`
   - 安裝完成後，後續所有 node/npm/npx 指令都需要先加上 `export PATH="/c/Program Files/nodejs:$PATH"`（僅 Windows）
4. **檢查 npx 是否可用**：執行 `npx --version`（Windows 記得加 PATH）
5. **檢查 Pandoc 是否已安裝**（用於 docx 轉 md）：
   - 先嘗試 `pandoc --version`
   - 若失敗，嘗試以下路徑：
     - Windows（winget 安裝）：`%LOCALAPPDATA%\Microsoft\WinGet\Packages\JohnMacFarlane.Pandoc_Microsoft.Winget.Source_8wekyb3d8bbwe\pandoc-3.9.0.2\pandoc.exe --version`
   - 若仍失敗，請安裝：
     - Windows：`winget install --id JohnMacFarlane.Pandoc --accept-source-agreements --accept-package-agreements`
     - macOS：`brew install pandoc`
     - Linux：`sudo apt install pandoc -y`
   - 安裝後記錄 pandoc 的完整路徑（後續腳本會用到）
6. **檢查 Tesseract OCR 是否已安裝**（用於圖片文字辨識）：
   - 先嘗試 `tesseract --version`
   - 若失敗，檢查安裝路徑：`"C:\Program Files\Tesseract-OCR\tesseract.exe" --version`
   - 若仍失敗，請安裝：
     - Windows：`winget install --id UB-Mannheim.TesseractOCR --accept-source-agreements --accept-package-agreements`
     - macOS：`brew install tesseract`
     - Linux：`sudo apt install tesseract-ocr -y`
   - **安裝中文語系**（若無則下載）：
     ```bash
     python -c "import urllib.request; urllib.request.urlretrieve('https://github.com/tesseract-ocr/tessdata_fast/raw/main/chi_tra.traineddata', r'C:\Program Files\Tesseract-OCR\tessdata\chi_tra.traineddata')"
     python -c "import urllib.request; urllib.request.urlretrieve('https://github.com/tesseract-ocr/tessdata_fast/raw/main/chi_sim.traineddata', r'C:\Program Files\Tesseract-OCR\tessdata\chi_sim.traineddata')"
     ```
     macOS/Linux 下載至 `/usr/local/share/tessdata/` 或 `$(tesseract --print-parameters | grep tessdata_dir)`
7. **檢查 Python 轉換套件是否已安裝**：
   ```bash
   pip install pymupdf pytesseract pandas
   ```
8. **檢查 Selenium 及 webdriver-manager 是否已安裝**（用於法規 PCode 自動查詢驗證）：
   ```bash
   pip install selenium webdriver-manager
   ```
9. **檢查 Obsidian 是否已安裝**：
   - Windows：檢查 `"$env:LOCALAPPDATA\Obsidian\Obsidian.exe"` 或 `"$env:ProgramFiles\Obsidian\Obsidian.exe"`
   - macOS：檢查 `/Applications/Obsidian.app`
   - Linux：檢查 `which obsidian` 或 `/usr/bin/obsidian`

> 全部通過後，告知使用者環境狀態，並顯示 Obsidian 是否已安裝。

### 步驟二：詢問使用者基本資訊

> 🖐️ **需要使用者回答**：依序詢問以下問題，等使用者回答後再繼續。

1. 您的大名（**姓名**）是？
2. 您屬於什麼**職系**？（例如：財稅會計、會計審計、土木工程）
3. 您所在**單位**是？（例如：審計部、宜蘭縣審計室）
4. 您的**職稱**是？（例如：審計員、稽察、科長）
5. 您希望 OpenCode 用什麼**語言**回答？（預設：繁體中文）
6. 您有沒有其他偏好？（例如：回答要專業簡潔、要給我接續提問建議、要用白話文）

> 記下使用者的回答（姓名、職系、單位、職稱等），後續步驟會用到。

### 步驟三：安裝 Obsidian（如果未安裝）

> 🖐️ **需要手動操作（僅未安裝時）**：
> 1. 請使用者開啟瀏覽器，到 https://obsidian.md 下載安裝檔
> 2. 執行安裝檔，按照指示完成安裝
> 3. 安裝完成後先不要開啟 Obsidian，等下一步設定好資料夾再開

若已安裝則自動跳過。

### 步驟四：建立 Vault 資料夾

> 🖐️ **需要使用者回答**：請詢問使用者想要存放 Vault 的路徑（預設建議：`C:\Users\[使用者]\secondbrain` 或自行指定路徑）

請在使用者指定的路徑建立以下目錄結構：

```
[vault路徑]/
├── 資料蒐集/                     ← 原始資料（docx、xlsx、pdf、圖片等）
├── 資料處理/                     ← 批次轉換後的 MD 檔案
│   ├── 1.基本資料分析/           ← 分類：最近期→最舊時間 → 分析主題
│   ├── 2.法規或函示/             ← 分類：主題 → 頒布時間(新→舊) → 頒布機關
│   └── 3.查核意見/               ← 分類：查核主題 → 建議事項/查明處理事項/注意事項 → 洞察/前瞻/監督
├── 資料庫建置及產出/
│   ├── 調查計畫/                 ← 查核前之調查計畫
│   ├── 工作底稿/                 ← 依生成規則產出之工作底稿
│   └── 分析報告/                 ← 綜合分析報告（無特定格式）
├── 工作日誌/                     ← 每日工作紀錄與週報
├── Templates/                    ← 筆記模板
└── CLAUDE.md                     ← OpenCode 的班規（後續步驟建立）
```

建立完成後，記錄 vault 的完整路徑（後續步驟會用到）。

### 步驟五：用 Obsidian 開啟 Vault

> 🖐️ **需要手動操作**：
> 1. 請使用者開啟 Obsidian
> 2. 選擇「Open folder as vault」（開啟資料夾作為筆記庫）
> 3. 選擇剛才建立的 vault 資料夾
> 4. Obsidian 會開啟並顯示空的筆記庫

確認使用者已成功開啟 vault 後，繼續下一步。

### 步驟六：安裝 mcpvault MCP Server

mcpvault 讓 OpenCode 能搜尋、讀取、編輯你的筆記。**不需要 Obsidian 開著就能運作。不需要在 Obsidian 中安裝任何外掛。**

#### 6-1：全域安裝 mcpvault

```bash
# Windows（記得加 PATH）
export PATH="/c/Program Files/nodejs:$PATH" && npm install -g @bitbonsai/mcpvault

# macOS / Linux
npm install -g @bitbonsai/mcpvault
```

安裝完成後，確認全域安裝的路徑：
- Windows：通常在 `C:\Users\[使用者]\AppData\Roaming\npm\mcpvault.cmd`
- macOS / Linux：通常在 `/usr/local/bin/mcpvault` 或 `~/.npm-global/bin/mcpvault`

用 `which mcpvault` 或 `where.exe mcpvault` 確認實際路徑。

#### 6-2：寫入 MCP 設定檔

⚠️ **重要**：為了確保 OpenCode 能正確載入 MCP，請在**三個位置**都寫入設定。

**位置 1：使用者全域設定** `~/.claude/settings.json`
**位置 2：專案設定** `[工作目錄]/.claude/settings.local.json`
**位置 3：專案根目錄** `[工作目錄]/.mcp.json`

三個檔案內容相同：

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "C:\\Users\\[使用者]\\AppData\\Roaming\\npm\\mcpvault.cmd",
      "args": [
        "[vault完整路徑]"
      ]
    }
  }
}
```

> macOS / Linux 範例：`"command": "mcpvault"`，`"args": ["/Users/[使用者]/secondbrain"]`
> ⚠️ 路徑中如果有中文或空格，在 JSON 中用雙反斜線跳脫。例如：`"D:\\我的Vault\\secondbrain"`

### 步驟七：重啟 OpenCode 並驗證

> 🖐️ **需要手動操作**：請使用者完全關閉 OpenCode 桌面版，然後重新開啟。

重新開啟後，驗證 MCP 是否成功載入：
- 檢查工具清單中是否有 `mcp__obsidian__` 開頭的工具
- 若能回傳 vault 的資料夾結構，代表連接成功

如果 MCP 未成功載入，依序排查：
1. 確認 `~/.claude/settings.json` 中的 `command` 路徑是否正確
2. 確認 vault 路徑確實存在且可存取
3. 確認 `.mcp.json` 在 OpenCode 開啟的工作目錄下
4. 再次重啟 OpenCode

### 步驟八：在 vault 根目錄建立 CLAUDE.md

這是 OpenCode 每次開對話時都會自動讀取的「班規」。請根據步驟二使用者的回答，建立以下內容：

```markdown
# 我的第二大腦 — CLAUDE.md

## 關於我
- 姓名：[使用者回答的姓名]
- 職稱：[使用者回答的職稱]
- 我是[使用者回答的職系]人員
- 服務單位：[使用者回答的單位]
- 這個 vault 是我的專業第二大腦

## 語言偏好
- 所有回應請使用[使用者回答的語言]
- 筆記內容也用[使用者回答的語言]
- 回答要專業簡潔、具邏輯性、且要給我接續提問建議、要用白話文、並提醒我何時可使用 `/資料處理` 觸發指令

## 筆記庫結構（三層）

| 資料夾 | 用途 | 存什麼 |
|---|---|---|
| `資料蒐集/` | 原始資料 | docx、xlsx、pdf、圖片等原始檔案 |
| `資料處理/` | 轉換+分類 | 批次轉換後的 MD，依類型分至子資料夾 |
| `資料庫建置及產出/` | 產出文件 | 調查計畫、工作底稿、分析報告 |
| `工作日誌/` | 工作紀錄 | 每日工作紀錄、週計畫、知識重整週報 |
| `Templates/` | 模板 | 各種筆記的固定格式 |

## 資料處理子結構

資料處理/
├── 1.基本資料分析/     ← 分類：最近期→最舊時間 → 分析主題
├── 2.法規或函示/       ← 分類：主題 → 頒布時間(新→舊) → 頒布機關
└── 3.查核意見/         ← 分類：查核主題 → 建議事項/查明處理事項/注意事項 → 洞察/前瞻/監督

## 資料庫建置及產出子結構

資料庫建置及產出/
├── 調查計畫/           ← 依生成原則產出之調查計畫（含 MD + WORD）
├── 工作底稿/           ← 依生成原則產出之標準化底稿
└── 分析報告/           ← 綜合分析報告（無特定格式）

## 工作規則

### 新增筆記時
- 一律加上 frontmatter（title、date、tags）
- 根據內容判斷存到哪個資料夾：
  - 原始檔案（docx/xlsx/pdf/圖片）→ `資料蒐集/`
  - 轉換後的 MD → 一律放 `資料處理/`（依類型分至子資料夾），**不放** `資料庫建置及產出/`
    - 調查報告：完整報告→`1.基本資料分析/`，提取查核意見→`3.查核意見/`
    - 調查計畫、工作底稿原始稿、抽查報告等 → `1.基本資料分析/`
  - 每日/每週紀錄 → `工作日誌/`
- `資料庫建置及產出/` 僅放**依生成原則產出**之文件（調查計畫、工作底稿、爬蟲分析、二次分析等產出）

### 批次轉換規則
- 使用者輸入 `/資料處理` 時，執行以下完整流程（無需手動執行腳本）：
  1. **掃描**：僅掃描 `資料蒐集/` 目錄中所有 docx、xlsx、pdf、png、jpg 等原始檔案，**不掃描 vault 內其他目錄**
  2. **轉換**：將尚未轉換的原始檔案轉為 .md 格式：
     - docx → pandoc
     - xlsx → pandas + openpyxl（不經 pandoc，以確保表格結構穩定）
     - pdf → pymupdf
     - 圖片（png/jpg）→ Tesseract OCR
  3. **歸檔**：轉換後的 MD 檔直接存放至 `資料處理/` 下的對應子資料夾，**不可暫存於 `資料蒐集/`**
  4. **分類**：讀取每個 MD 檔內容進行類型判斷與歸檔：
     - **調查報告**（關鍵字：調查報告、查核報告、審計報告）：完整報告→`1.基本資料分析/`；提取「查核意見」章節→`3.查核意見/`
     - **法規或函示**（關鍵字：法規、條例、函、令）：→`2.法規或函示/`
     - **調查計畫、工作底稿原始稿、品質抽查報告**等：→`1.基本資料分析/`
     - **無法判斷類型者**：→`1.基本資料分析/`
  5. **提取查核意見**：若檔案類型為調查報告，自動掃描內容中「查核意見」章節（含 `#`、`##` 或 `**` 標題標記），將該章節內容獨立提取為一個 MD 檔存放至 `3.查核意見/`，並在每個意見末尾註記來源報告名稱
  6. **分類完成後**，自動執行重複性及冗餘資料清理：
     - 比對 `資料處理/` 下各子資料夾內 MD 檔的內容（跳過 frontmatter），刪除內容完全相同之重複檔案
     - 若同一份調查報告因多次提取產生多個相似檔案，保留檔名最完整或內容最完善者，其餘刪除
     - 清理後輸出摘要報告（含刪除檔案清冊、保留檔案清冊、各資料夾筆數統計）
  7. **清理完成後**，更新 `查核意見總整理` 與 `查核意見明細`（存入 `3.查核意見/`，檔名以民國曆日期後綴）
  8. **最後**，詢問使用者：「分類與清理已完成。是否刪除 `資料蒐集/` 中的所有原始檔案？」等待使用者確認後才執行刪除

### 轉換後檔案分類規則

| 類型 | 判斷關鍵字 | 歸檔目錄 |
|------|-----------|---------|
| **調查報告** | 調查報告、查核報告、審計報告、專案調查 | `1.基本資料分析/`（完整）+ `3.查核意見/`（意見章節） |
| **法規或函示** | 法、條例、規則、辦法、函、令、公告、解釋 | `2.法規或函示/` |
| **調查計畫** | 調查計畫、查核計畫、調查規劃 | `1.基本資料分析/` |
| **工作底稿原始稿** | 工作底稿、底稿、查核紀錄 | `1.基本資料分析/` |
| **品質抽查報告** | 抽查、抽核、品質查核 | `1.基本資料分析/` |
| **無法判斷** | 無明顯關鍵字 | `1.基本資料分析/` |

### 查核意見分類規則（依序）
- **第一層**：查核主題（主要分類）
- **第二層**：建議事項、查明處理事項、注意事項（次分類）
- **第三層**：洞察、前瞻、監督（再次分類）
- **第四層**：查核意見標題及其文章內容
- 每個意見最後需註記截取自哪一份調查報告的名稱
```

> 把 `[使用者回答的職系]`、`[使用者回答的單位]`、`[使用者回答的語言]`、`[vault路徑]` 替換為實際內容。

### 步驟九：建立法規 PCode 查詢工具（get_pcode.py）

> 💡 **這個工具為什麼重要？** 生成「相關法規及連結」時，法規的 PCode 必須正確。全國法規資料庫會檢查 Session 和 Cookies，直接用 requests 抓取容易被擋，故需使用 Selenium 模擬瀏覽器查詢。

在 vault 根目錄建立 `get_pcode.py`，內容如下：

```python
"""
全國法規資料庫 PCode 查詢工具
使用 Selenium 模擬瀏覽器，搜尋法規名稱並取得正確 PCode

用法：
    python get_pcode.py "法規名稱"

範例：
    python get_pcode.py "促進民間參與公共建設法"
    python get_pcode.py "公路法"

輸出：
    法規名稱、PCode、完整網址（法規全文頁面）

注意：
    需先安裝 Selenium 及瀏覽器驅動：
    pip install selenium webdriver-manager
"""

import sys
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def search_law_pcode(law_name: str) -> dict | None:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )

    try:
        print(f"正在搜尋：「{law_name}」...")
        driver.get("https://law.moj.gov.tw/")
        wait = WebDriverWait(driver, 15)

        search_box = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[type='text']")
            )
        )
        search_box.clear()
        search_box.send_keys(law_name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

        all_links = driver.find_elements(By.TAG_NAME, "a")
        target_url = None

        for link in all_links:
            href = link.get_attribute("href")
            if not href:
                continue
            if "Log=true" in href or "&Log=" in href:
                continue
            if "law.moj.gov.tw/LawClass/" not in href:
                continue
            pcode_match = re.search(r'pcode=([A-Z]\d+)', href)
            if pcode_match:
                pcode = pcode_match.group(1)
                target_url = f"https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode={pcode}"
                break

        if target_url:
            result = {
                "name": law_name,
                "pcode": re.search(r'pcode=([A-Z]\d+)', target_url).group(1),
                "url": target_url,
            }
            print(f"  ✅ 找到：{result['name']} → PCode：{result['pcode']}")
            return result
        else:
            print(f"  ❌ 找不到「{law_name}」的 PCode")
            return None

    except Exception as e:
        print(f"  ❌ 搜尋「{law_name}」時發生錯誤：{e}")
        return None
    finally:
        driver.quit()


def batch_search(law_names: list[str]) -> list[dict]:
    results = []
    for name in law_names:
        result = search_law_pcode(name)
        if result:
            results.append(result)
        print()
    return results


if __name__ == "__main__":
    if len(sys.argv) > 1:
        law_name = " ".join(sys.argv[1:])
        search_law_pcode(law_name)
    else:
        print("=" * 60)
        print("全國法規資料庫 PCode 批次查詢")
        print("=" * 60)
        law_list = [
            "審計法", "促進民間參與公共建設法", "公路法",
            "汽車運輸業管理規則", "身心障礙者權益保障法",
            "建築技術規則建築設計施工編", "空氣污染防制法",
            "停車場法", "民法", "政府採購法",
        ]
        results = batch_search(law_list)
        print("=" * 60)
        print("查詢結果總表")
        print("=" * 60)
        for r in results:
            print(f"{r['name']:<30} {r['pcode']:<15} {r['url']}")
```

> 建立完成後，告知使用者可以先測試：「執行 `python get_pcode.py "促進民間參與公共建設法"` 確認是否能正確取得 PCode。」

### 步驟十：建立筆記模板

在 `Templates/` 資料夾中建立以下三個模板（若已有同名檔案，跳過不覆蓋）：

**模板 1：工作日誌.md**
```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
week: <% tp.date.now("YYYY-[W]WW") %>
day: <% tp.date.now("dddd", 0, tp.file.title, "MM/DD（E）") %>
type: 工作日誌
tags:
  - 工作日誌
---

# <% tp.file.title %>

---

## 📋 今日工作

-

**案件進度**：

---

## 💡 今日反思

>

---

## 明日優先事項

1.
2.
3.
```

**模板 2：週計畫.md**
```markdown
---
week: <% tp.date.now("YYYY-[W]WW") %>
date_start: <% tp.date.now("YYYY-MM-DD", -tp.date.now("d") + 1) %>
date_end: <% tp.date.now("YYYY-MM-DD", 7 - tp.date.now("d")) %>
type: 週計畫
tags:
  - 週計畫
---

# <% tp.date.now("YYYY-[W]WW") %> 週計畫

> <% tp.date.now("MM/DD", -tp.date.now("d") + 1) %> – <% tp.date.now("MM/DD", 7 - tp.date.now("d")) %>

---

## 📋 本週工作重點

| 日期 | 案件/事項 | 進度 |
|------|------|------|
| | | |

---

## 📧 本週重要事項

- [ ]

---

## 本週每日連結

- [[<% tp.date.now("MM/DD", -tp.date.now("d") + 1) %>（一）]]
- [[<% tp.date.now("MM/DD", -tp.date.now("d") + 2) %>（二）]]
- [[<% tp.date.now("MM/DD", -tp.date.now("d") + 3) %>（三）]]
- [[<% tp.date.now("MM/DD", -tp.date.now("d") + 4) %>（四）]]
- [[<% tp.date.now("MM/DD", -tp.date.now("d") + 5) %>（五）]]
```

**模板 3：知識庫頁面.md**
```markdown
---
title: ""
type: 知識庫
source: ""
created: <% tp.date.now("YYYY-MM-DD") %>
tags: []
related: []
---

#

> 原始資料：
> 整理日期：<% tp.date.now("YYYY-MM-DD") %>

---

## 核心概念



---

## 與我工作的連結



---

## 內容缺口（待補）

- [ ]
```

### 步驟十一：建立知識庫初始檔案

在 `資料庫建置及產出/分析報告/` 中建立兩個初始檔案：

**index.md**
```markdown
---
title: 知識庫索引
type: index
updated: [今天日期]
---

# 知識庫索引

> 最後更新：[今天日期]
> 這是你的 AI 知識庫目錄。每次知識重整時會自動更新。

---

目前知識庫是空的。當你開始用 Web Clipper 收集法規、案例，
每週知識重整就會把資料消化成知識庫頁面，顯示在這裡。

| 頁面 | 一行摘要 |
|---|---|
| （等待第一次知識重整） | |
```

**log.md**
```markdown
---
title: 知識庫操作紀錄
type: log
---

# 知識庫操作紀錄

---

## [[今天日期]] 初始化 | 建立第二大腦

**操作類型：** 初始化

**建立的結構：**
- 資料蒐集/（原始資料）
- 資料處理/（已轉換分析）
- 資料庫建置及產出/（產出文件）
- 工作日誌/（工作紀錄）
- Templates/（模板）
- CLAUDE.md（工作規則）

**下一步：** 用 Web Clipper 開始收集你的第一份法規或案例！
```

### 步驟十二：引導使用者設定 Web Clipper 預設資料夾

> 🖐️ **需要手動操作**：請告知使用者以下步驟。

將 Obsidian Web Clipper 的預設存放位置改成 `資料蒐集/`：
1. 打開瀏覽器，點選 Web Clipper 的圖示（通常在網址列右邊）
2. 點選齒輪 ⚙ 進入設定
3. 找到「Vault」，確認選的是你的 vault
4. 找到「Folder」或「Location」（存放位置）
5. 改成 `資料蒐集`
6. 儲存設定

### 步驟十三：建立自動排程

建立一個每週日自動執行的知識重整任務：

- **任務 ID**：`weekly-knowledge-review`
- **排程**：每週日早上 9:17（cron：`17 9 * * 0`）
- **說明**：每週日自動知識重整

任務內容（prompt）如下：

```
請執行 Obsidian 筆記庫的每週知識重整，完成以下所有步驟：

第一步：盤點本週變動
- 搜尋 vault 中過去 7 天內新增或修改的筆記
- 分三類列出：資料處理/、資料庫建置及產出/、資料蒐集/

第二步：消化資料處理/ → 資料庫建置及產出/分析報告/
- 讀取資料處理/ 中本週新增的所有筆記完整內容
- 分析主題、找出跨篇關聯
- 為每個主題群產出一篇結構化的分析報告
- 存到資料庫建置及產出/分析報告/

第三步：資料庫建置及產出回流
- 讀取資料庫建置及產出/ 中本週新增或修改的筆記
- 檢查是否有新的概念值得補充

第四步：健康檢查（lint）
- 連結檢查：找出可以互相連結但尚未連結的筆記
- 知識缺口：根據主題分佈，建議該去找什麼資料
- 孤兒頁面：找出沒有任何連結的筆記

第五步：更新分析報告索引
- 分析報告目錄：加入本週新增的報告頁面
- 操作紀錄：新增本週重整紀錄

第六步：產出週報筆記
- 存到工作日誌/ 資料夾
- 檔名：YYYY-WXX 知識重整.md
- 內容：本週變動總覽、消化了什麼、健康檢查結果、下週建議

完成後通知使用者：「本週知識重整已完成，請查看週報筆記。」
```

### 步驟十四：建立歡迎筆記

在 vault 根目錄建立歡迎筆記 `歡迎來到你的第二大腦.md`，內容如下：

```markdown
---
title: 歡迎來到你的第二大腦
date: [今天日期]
type: 指南
tags:
  - 指南
---

# 歡迎來到你的第二大腦！

恭喜！你的 AI 知識管理系統已經設定完成。

---

## 你的筆記庫結構

| 資料夾 | 用途 | 你要做的事 |
|---|---|---|
| `資料蒐集/` | 原始資料 | 原始檔案（docx/xlsx/pdf/圖片）放這裡 |
| `資料處理/` | 轉換+分類 | 輸入 `/資料處理` 即可批次轉換，AI 自動分類 |
| `資料庫建置及產出/` | 產出文件 | 調查計畫、工作底稿、分析報告放這裡 |
| `工作日誌/` | 時間管理 | 每天的紀錄、每週的計畫 |

---

## 三層結構說明

```
資料蒐集/  →  資料處理/  →  資料庫建置及產出/
（原始檔）    （轉MD+分類）    （調查計畫/工作底稿/分析報告）
```

### 資料處理分類方式

| 子資料夾 | 分類規則 |
|---|---|
| `1.基本資料分析/` | 時間（最近→最舊）→ 分析主題 |
| `2.法規或函示/` | 主題 → 頒布時間（新→舊）→ 頒布機關 |
| `3.查核意見/` | 查核主題 → 建議事項/查明處理事項/注意事項 → 洞察/前瞻/監督 |

---

## 你每天只要做兩件事

### 1. 收集（10 秒）
看到法規、案例、查核資料 → 原始檔案放進 `資料蒐集/` → 完成。不用整理，先存再說。

### 2. 轉換 + 分類（自動）
輸入 `/資料處理` → AI 自動批次轉換成 MD → 讀取內容後分類至 `資料處理/` 對應資料夾

### 3. 收割（需要的時候）
跟我說「幫我從筆記庫整理出 XXX」，AI 會幫你從所有筆記中串接出你需要的文件。

---

## 查核報告搜尋與應用

| 你想做什麼 | 怎麼做 |
|---|---|
| 搜尋查核事實 | 說「搜尋查核報告中有關 XXX 的內容」 |
| 搜尋查核意見 | 說「搜尋查核意見中關於 XXX 的案例」 |
| 找工程缺失案例 | 說「列出工程缺失類型的查核報告」 |
| 找採購缺失案例 | 說「列出採購缺失類型的查核報告」 |
| 生成工作底稿 | 說「幫我根據 XXX 生成工作底稿」 |

---

## 每週自動發生的事

每週日早上，我會自動執行知識重整：
1. 把本週的資料消化成知識庫
2. 檢查知識庫的健康狀態
3. 產出一份週報放在工作日誌/

你不用做任何事，打開 Obsidian 就能看到結果。

---

## 常用指令

| 你說的話 | 我會做的事 |
|---|---|
| 「幫我新增到筆記」 | 把內容存到 Obsidian（自動判斷資料夾） |
| 「搜尋筆記有沒有 XXX」 | 搜尋整個 vault |
| 「跑一次知識重整」 | 手動觸發完整七步驟 |
| 「消化 資料處理/」 | 只消化本週新增的資料 |
| 「知識庫 lint」 | 只做健康檢查 |
| 「幫我寫今天的工作反思」 | 引導你口述，整理成筆記 |
| 「幫我分類查核報告」 | 逐份閱讀並移至對應分類資料夾 |
| 「幫我根據 XXX 生成工作底稿」 | 參考既有報告與生成原則，產出工作底稿 |

---

## 開始你的第一步

現在就試試看：
1. 對我說「幫我分類查核報告」
2. 看看 AI 如何幫你整理既有報告
3. 分類完成後，試試看搜尋某個缺失類型
```

### 步驟十五：最終驗證

逐一確認以下項目：

1. ✅ Node.js 已安裝，npx 可用
2. ✅ Pandoc 已安裝（支援 docx → md 轉換）
3. ✅ Tesseract OCR 已安裝（含中文語系）
4. ✅ Python 轉換套件已安裝（pymupdf、pytesseract、pandas）
5. ✅ Selenium 及 webdriver-manager 已安裝
6. ✅ mcpvault 已安裝，MCP 設定檔已寫入三個位置
7. ✅ 資料夾結構已建立
8. ✅ CLAUDE.md 已建立且包含使用者資訊
9. ✅ Templates/ 中有三個模板
10. ✅ get_pcode.py 已建立於 vault 根目錄
11. ✅ 分析報告/ 中有 index.md 和 log.md
12. ✅ 歡迎筆記已建立
13. ✅ 每週知識重整排程已設定

全部通過後，告知使用者：「審計第二大腦已完成安裝設定！」

---

## 批次轉換既有檔案（docx、xlsx、pdf、圖片 → md）

當使用者在 `資料蒐集/` 資料夾放置非 MD 檔案時，只需輸入 `/資料處理`，系統就會自動執行以下流程：

1. **掃描**：僅掃描 `資料蒐集/` 中的原始檔案，不掃描 vault 內其他目錄
2. **轉換**：依格式使用對應工具轉為 MD
3. **歸檔**：轉換後的 MD 直接存放至 `資料處理/` 下的對應子資料夾
4. **類型判斷**：依關鍵字判斷檔案類型並歸檔
5. **提取查核意見**：若為調查報告，自動提取「查核意見」章節
6. **清理**：比對內容刪除重複檔案
7. **更新查核意見總整理**與**查核意見明細**
8. **詢問**：是否刪除 `資料蒐集/` 中的所有原始檔案

### 查核意見章節提取方法

當檔案被判斷為**調查報告**時，自動提取「查核意見」章節：

1. **定位章節**：掃描 MD 內容，尋找標題中包含「查核意見」的行（支援 `# 查核意見`、`## 查核意見`、`**查核意見**` 等格式）
2. **提取範圍**：從「查核意見」標題下一行開始，至下一個同層級或更高層級標題為止（或檔尾）
3. **分割意見項目**：將提取出的內容依 `**一、**`、`**二、**` 等中編號粗體標題逐項分割，每項獨立為一個查核意見
4. **註記來源**：在每個分割出的意見末尾附加「（截取自：[報告名稱]）」
5. **存放**：獨立存為一個 MD 檔（檔名格式為 `[報告名稱]_查核意見.md`），放入 `資料處理/3.查核意見/`

### 查核意見總整理與查核意見明細（自動維護）

每次執行 `/資料處理` 並完成分類清理後，系統會自動：

1. **掃描** `資料處理/3.查核意見/` 下所有 MD 檔案（排除 `查核意見總整理` 及 `查核意見明細` 本身）
2. **提取**每個檔案中的查核意見：
   - 標題：以 `**` 包圍之中文編號粗體文字（如 `**一、...**`、`**二、...**`）
   - 內容：標題所在行後至下一個標題行或檔尾之全文
   - 出處：從 frontmatter 或檔案原始名稱取得
   - 年度：從檔名或內容中取得
3. **去重**：對每筆意見的**本文全文**計算 MD5 雜湊值，僅保留首次出現之條目；去重**跨所有檔案**
4. **分類**：依標題關鍵字自動判斷主題類型（工程品質、採購程序、財務管理等）及意見分類（查明處理事項/建議事項/注意事項）
5. **產生**兩份文件，存放於 `資料處理/3.查核意見/`：
   - `查核意見總整理(YYYYMMDD).md` — 摘要統計表（含主題類型、分類、年度、筆數、去重紀錄）
   - `查核意見明細(YYYYMMDD).md` — 逐條完整版（含編號、主題類型、分類、出處、年度、標題、內容）

### 清理摘要報告格式

每次執行 `/資料處理` 且完成重複清理後，自動輸出清理摘要報告，存放於 `資料處理/` 根目錄，檔名為 `清理摘要(YYYYMMDD).md`：

```markdown
---
date: [民國曆日期]
type: 清理摘要
---

# 清理摘要報告

**執行時間**：[民國曆日期]

---

## 資料夾筆數統計（清理後）

| 子資料夾 | 筆數 |
|---------|------|
| 1.基本資料分析/ | N |
| 2.法規或函示/ | N |
| 3.查核意見/ | N |
| **合計** | **N** |

---

## 刪除檔案清冊

| 檔名 | 來源資料夾 | 刪除原因 |
|------|-----------|---------|
| ... | ... | 內容重複 / 冗餘保留檔 |

---

## 保留檔案清冊

| 檔名 | 存放資料夾 | 檔案類型 |
|------|-----------|---------|
| ... | ... | 調查報告 / 法規 / ... |

---

## 查核意見更新紀錄

- 本次新增查核意見筆數：N
- 去重後保留筆數：N
- 更新後總整理檔名：查核意見總整理(YYMMDD).md
- 更新後明細檔名：查核意見明細(YYMMDD).md
```

### 轉換後檔案管理

- **原始檔案保留**：轉換不會自動刪除原始檔案，經使用者同意後才刪除 `資料蒐集/` 中所有檔案
- **手動新增檔案**：以後有新檔案，直接放到對應資料夾，再說「執行轉換腳本」即可
- **選擇性轉換**：可指定單一檔案，說「幫我把 XXX.docx 轉成 md」

### 設定指南排錯

當使用者說「審計第二大腦設定指南執行失敗了，幫我檢查哪裡出問題」，應自動：
1. 檢查 Node.js 是否正常
2. 檢查 mcpvault 是否正常運作
3. 檢查 vault 路徑是否正確
4. 找出問題並修復

### 轉換方式對照表

| 原始格式 | 轉換工具 | 說明 |
|---------|---------|------|
| docx | pandoc | 穩定支援格式與樣式 |
| xlsx | pandas + openpyxl | 逐工作表轉為 MD 表格，保留欄位結構 |
| pdf | pymupdf（fitz） | 提取純文字與表格 |
| 圖片（png/jpg） | Tesseract OCR | 辨識繁體/簡體中文 |

---

## 常見問題

| 問題 | 解法 |
|------|------|
| mcpvault 搜尋不到筆記 | 確認 vault 路徑正確，路徑中有中文或空格需用引號包住 |
| `npx: command not found` | 確認 Node.js 已安裝，重啟 OpenCode |
| 重啟後 MCP 工具仍不存在 | 確認設定檔中 `command` 使用完整路徑 |
| Windows bash 找不到 node | `export PATH="/c/Program Files/nodejs:$PATH"` |
| 設定檔寫了但沒生效 | 確認在三處都寫入（`~/.claude/settings.json`、`.claude/settings.local.json`、`.mcp.json`） |
| Obsidian 需要裝外掛嗎？ | **不需要**。mcpvault 直接讀寫 vault 資料夾的檔案，不經過 Obsidian app |
| pandoc 找不到 | 用完整路徑執行，或加入 PATH 環境變數 |
| PDF 轉 md 後格式亂掉 | PDF 非結構化格式，pymupdf 僅提取純文字。若需保留表格可用 pandas 輔助 |
| OCR 辨識率不佳 | 確認圖片解析度夠高，可先試用 Vision 功能直接讀圖 |
| 新檔案加入後如何轉換？ | 直接放進對應資料夾，對 OpenCode 說「執行轉換腳本」即可 |
| 生成法規連結時 pcode 錯誤怎麼辦？ | 使用 `python get_pcode.py "法規名稱"` 查詢正確 pcode |
| Selenium 啟動時報錯 ChromeDriver 問題 | 執行 `pip install --upgrade webdriver-manager` 或手動下載對應版本 |
| 全國法規資料庫搜尋不到法規 | 確認法規名稱正確（使用完整名稱），若仍搜尋不到可手動開啟 https://law.moj.gov.tw 查詢 |

---

## 更新紀錄

| 日期 | 版本 | 更新內容 |
|------|------|---------|
| 2026-07-29 | v1.0 | 自合併版（v3.2）拆分獨立為安裝設定技能，含環境檢查、MCP 連接、CLAUDE.md 建立、Templates、批次轉換、Web Clipper 設定、知識重整排程 |

## 相關連結

- [mcpvault GitHub](https://github.com/bitbonsai/mcpvault)
- [Obsidian 官網](https://obsidian.md)
