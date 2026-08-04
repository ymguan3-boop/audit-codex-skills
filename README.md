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

---

## Blender + React + Three.js 常見使用情境

本儲存庫新增的 `blender-react-threejs-3d-builder` 技能，適合把 Blender 製作的 3D 資產，轉換成可互動、可部署的 React + Three.js 網站或應用程式。

### 1. 3D 產品展示

適合家具、機械、家電、汽車、珠寶與消費性產品：

- Blender 建立產品模型、材質與燈光，匯出 GLB。
- Three.js 提供旋轉、縮放、平移、材質切換、零件拆解與互動標註。
- React 管理規格面板、產品變體、按鈕、詢價或購買流程。
- 可增加 AR 入口、產品動畫、爆炸圖與多角度導覽。

### 2. 建築及室內設計空間展示

適合建築提案、室內設計、樣品屋、展售中心與公共空間：

- Blender 建立建築、家具、材質、燈光預設與樓層結構。
- Three.js 提供第一人稱漫遊、軌道相機、房間切換、測量與熱點。
- React 顯示樓層導覽、材質方案、空間標籤、家具清單與設計說明。
- 可加入相機 Waypoint、日夜光照切換與平面圖導覽。

### 3. 數位展覽與虛擬博物館

適合文化資產、藝術展覽、校園展示與線上策展：

- Blender 製作展間、展品、展牆與導覽場景。
- Three.js 處理展場移動、展品聚焦、動畫、影音播放與互動熱點。
- React 管理展品卡片、導覽路線、字幕、語言切換與無障礙資訊。
- 可設計自由探索、策展人導覽與時間軸三種模式。

### 4. 3D 遊戲與互動體驗

適合瀏覽器 RPG、收集遊戲、教育遊戲、解謎與品牌互動活動：

- Blender 製作角色、道具、場景、碰撞輔助物件與待機／移動動畫。
- Three.js 執行遊戲迴圈、相機、輸入、碰撞、特效、動畫與物件互動。
- React 管理 HUD、選單、圖鑑、任務、存檔與遊戲狀態。
- 建議先建立一個可玩的代表性角色與場景，再擴充資產數量。

### 5. 3D 動畫與互動敘事

適合產品動畫、角色展示、教學模擬、互動故事與線上發表：

- Blender 製作骨架、表情、鏡頭與命名動畫片段。
- Three.js 以 `AnimationMixer` 播放、混合、循環與同步多個 GLB 動畫。
- React 提供播放、暫停、重播、時間軸、字幕與章節控制。
- 可加入鏡頭轉場、互動分支與語音／音樂控制。

### 通用技術流程

```text
需求與參考圖
    -> Blender 建模、材質、燈光、動畫
    -> 匯出 GLB（模型與動畫）
    -> React / TypeScript 建立頁面與 UI
    -> Three.js 載入 GLB、建立場景與互動
    -> 效能、手機、鍵盤／觸控與錯誤回復測試
    -> 部署至靜態網站或 Web App 主機
```

### 建議的專案分層

```text
public/models/             GLB 模型與貼圖
src/3d/asset-registry.ts   模型網址、比例、相機與互動設定
src/3d/create-experience   Three.js 場景、燈光、相機與 renderer
src/3d/interaction-controller  射線互動、距離判定與輸入
src/components/            React UI、選單與資訊面板
tools/                     Blender Python 建模與匯出工具
tests/                     資產、載入、互動與 production build 測試
```

完整的可重用規則、品質門檻與各種模式做法，請參考 [blender-react-threejs-3d-builder](./blender-react-threejs-3d-builder/SKILL.md)。


## 版本紀錄
