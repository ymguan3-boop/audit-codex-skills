# 審計輔助技能 for Codex

審計專用之 OpenCode 技能包，含三個獨立技能，適用於審計人員日常查核工作之 AI 輔助：

- **審計第二大腦安裝及設定** — 建置 Obsidian + MCP 知識管理系統
- **生成調查計畫** — 依主題產出完整調查計畫及配套文件
- **生成工作底稿** — 依查核事實產出標準化四階段底稿

---

## 技能總覽

### 1. 審計第二大腦安裝及設定技能

| 項目 | 內容 |
|------|------|
| 檔名 | `audit-secondbrain-setup.md` |
| 用途 | 從零開始建置審計專屬的 AI 第二大腦系統 |
| 包含 | 環境檢查（Node.js、Pandoc、Tesseract、Python）、Obsidian Vault 建立、mcpvault MCP 連接、CLAUDE.md 班規設定、Templates、Web Clipper 設定、每週知識重整排程、批次檔案轉換腳本 |
| 產出 | 完整 Obsidian Vault + OpenCode MCP 連線 + 自動化知識管理系統 |
| 觸發詞 | `第二大腦安裝`、`審計第二大腦設定`、`secondbrain-setup` |

### 2. 生成調查計畫技能

| 項目 | 內容 |
|------|------|
| 檔名 | `audit-investigation-plan.md` |
| 用途 | 依使用者提供之調查主題，產出完整調查計畫及三份配套文件 |
| 包含 | 11 章節調查計畫格式（壹~拾+附件規劃矩陣）、相關法規及連結（含 PCode 自動查詢驗證）、調閱資料清單（動態生成）、缺失評估問卷（6 欄位格式） |
| 產出 | 調查計畫 + 三份配套文件（每份均含 MD 及 WORD 檔） |
| 觸發詞 | `生成調查計畫`、`調查計畫`、`investigation-plan` |

### 3. 生成工作底稿技能

| 項目 | 內容 |
|------|------|
| 檔名 | `audit-working-paper.md` |
| 用途 | 根據查核事實資料，產出標準化審計工作底稿 |
| 包含 | 四階段結構（標題、依據、查核事實、擬議處理意見）、查核意見分類規則（四層分類）、查核意見章節提取方法、查核意見總整理自動維護機制 |
| 產出 | 標準化工作底稿（每份均含 MD 及 WORD 檔） |
| 觸發詞 | `生成工作底稿`、`工作底稿`、`working-paper` |

---

## 使用方式

### 註冊技能

將技能檔路徑加入 OpenCode 設定檔（`opencode.json`）的 `skills` 區塊：

```json
{
  "skills": {
    "allow": [
      "C:\\Users\\[使用者]\\Documents\\Codexskill\\audit-secondbrain-setup.md",
      "C:\\Users\\[使用者]\\Documents\\Codexskill\\audit-investigation-plan.md",
      "C:\\Users\\[使用者]\\Documents\\Codexskill\\audit-working-paper.md"
    ]
  }
}
```

### 技能依賴關係

```
審計第二大腦安裝及設定（基礎設施）
        │
        ├──→ 生成調查計畫（需已有 Vault + CLAUDE.md）
        │
        └──→ 生成工作底稿（需已有 Vault + CLAUDE.md + 查核意見資料）
```

**建議流程**：
1. 先執行「審計第二大腦安裝及設定」建立 Vault 及 MCP 連線
2. 有調查需求時執行「生成調查計畫」
3. 有查核事實資料時執行「生成工作底稿」

### 使用範例

```
使用者：「請幫我生成一份宜蘭縣政府辦理羅東轉運站委託經營執行情形調查計畫」
→ 載入技能 audit-investigation-plan → 產出調查計畫 + 法規連結 + 調閱清單 + 缺失問卷

使用者：「請幫我根據羅東轉運站委託經營缺失生成工作底稿」
→ 載入技能 audit-working-paper → 產出四階段工作底稿
```

---

## 檔案結構

```
audit-codex-skills/
├── README.md                          # 本檔案
├── audit-secondbrain-setup.md         # 技能一：第二大腦安裝及設定
├── audit-investigation-plan.md        # 技能二：生成調查計畫
└── audit-working-paper.md             # 技能三：生成工作底稿
```

---

## 版本紀錄

| 日期 | 版本 | 內容 |
|------|------|------|
| 2026-07-29 | v1.0 | 自審計第二大腦設定指南（v3.2）拆分為三個獨立技能 |
