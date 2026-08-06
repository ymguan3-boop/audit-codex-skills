# 審計輔助技能 for Codex

本儲存庫提供兩個可重用的 Codex 技能資料夾：

- **審計輔助技能 for Codex**：審計第二大腦、調查計畫與工作底稿等 3 個審計技能。
- **3d-builder**：Blender 精確建模 + Hunyuan3D-2 AI 生成的混合 3D 建模技能。

---

## 資料夾一：審計輔助技能 for Codex

此資料夾包含 3 個審計工作技能，可搭配第二大腦與 Codex 工作流程使用。

### 1. 生成調查計畫

| 項目 | 內容 |
|------|------|
| 檔案 | `審計輔助技能 for Codex/audit-investigation-plan.md` |
| 用途 | 依使用者提供的調查主題，產出完整調查計畫及配套文件 |
| 產出 | 調查計畫、法規連結、調閱資料清單與缺失評估問卷 |
| 觸發詞 | `生成調查計畫`、`調查計畫`、`investigation-plan` |

### 2. 審計第二大腦安裝及設定

| 項目 | 內容 |
|------|------|
| 檔案 | `審計輔助技能 for Codex/audit-secondbrain-setup.md` |
| 用途 | 建置 Obsidian + MCP 的審計專屬 AI 第二大腦 |
| 包含 | Vault、CLAUDE.md、Templates、Web Clipper、MCP 連線與知識整理流程 |
| 觸發詞 | `第二大腦安裝`、`審計第二大腦設定`、`secondbrain-setup` |

### 3. 生成工作底稿

| 項目 | 內容 |
|------|------|
| 檔案 | `審計輔助技能 for Codex/audit-working-paper.md` |
| 用途 | 根據查核事實資料產出標準化審計工作底稿 |
| 產出 | 標題、依據、查核事實與擬議處理意見四階段工作底稿 |
| 觸發詞 | `生成工作底稿`、`工作底稿`、`working-paper` |

---

## 資料夾二：3d-builder（Blender + Hunyuan3D-2 混合建模）

此技能採用**混合建模策略**：Blender 負責精確結構，Hunyuan3D-2 負責有機/複雜物件，結合兩者優勢加速產出。

### 物件分類決策樹

```
物件描述
  │
  ├─ 結構性物件（建築、牆、柱、門窗）→ Blender Python
  ├─ 有機/複雜形狀（雕塑、裝置藝術）→ Hunyuan3D-2
  ├─ 家具/設備（桌椅、電腦、車輛）→ Hunyuan3D-2
  └─ 場景環境（天空、草地）→ Blender/Shader
```

### 完整規則與參考資料

- [SKILL.md](./3d-builder/SKILL.md)
- [模式參考](./3d-builder/references/modes.md)
- [品質檢核](./3d-builder/references/quality-gate.md)

---

## 審計技能快速使用

在已安裝技能的 Codex 工作階段中，可以用自然語言指定需求，例如：

```text
請使用調查計畫技能，幫我產出「宜蘭縣政府辦理某公共工程」的調查計畫，
包含相關法規、調閱資料清單及缺失評估問卷。
```

```text
請使用工作底稿技能，根據我提供的查核事實，
產出四階段審計工作底稿，並同步整理查核意見分類。
```

---

## 3D Builder 快速使用指令

在已安裝 3D 技能的 Codex 工作階段中，可直接使用 `$3d-builder`。

### 旋轉展示家具產品

```text
使用 $3d-builder
製作一個可旋轉展示家具產品的 3D 網站。
使用 Blender 建立一張北歐風單椅，匯出 GLB；
使用 React + Three.js 實作滑鼠與觸控旋轉、縮放、重設視角、
材質顏色切換、產品尺寸標註與手機版響應式介面。
```

### 自由參觀室內設計展示空間

```text
使用 $3d-builder
製作一個可自由參觀的室內設計展示空間。
使用 Blender 建立客廳、餐廳與臥室模型；
使用 React + Three.js 實作第一人稱／軌道相機、房間切換、
家具資訊熱點、日夜燈光切換、鍵盤與觸控操作，
並加入載入進度提示、GLB 載入失敗的替代畫面與 production build 測試。
```

### 混合建模（Blender + Hunyuan3D-2）

```text
使用 $3d-builder
製作一個辦公室室內展示空間。
使用 Blender 建立牆壁、樓板、門窗等結構件；
使用 Hunyuan3D-2 生成辦公桌椅、電腦、裝置藝術等裝飾件；
使用 React + Three.js 實作互動瀏覽與資訊面板。
```

### 其他常見指令

```text
使用 $3d-builder
製作一個可自由探索的數位展覽館，包含展品熱點、導覽路線、
展品資訊面板、字幕、音訊控制與手機版操作。

使用 $3d-builder
製作一個瀏覽器 3D 收集遊戲，包含角色移動、碰撞、互動物件、
任務狀態、HUD、存檔，以及桌面鍵盤與手機觸控控制。

使用 $3d-builder
製作一段可在網頁播放的 3D 角色動畫，包含 Idle、Walk、Open
等 GLB 動畫片段，並提供播放、暫停、重播、時間軸拖曳與字幕。
```

---

## 一般使用情境

### 3D 產品展示

Blender 建立產品模型、材質與動畫，匯出 GLB；Three.js 提供旋轉、縮放、材質切換、零件拆解與熱點；React 管理規格面板、產品變體與行動版介面。

### 建築及室內設計空間

Blender 建築結構 + Hunyuan3D-2 家具/裝飾；Three.js 提供第一人稱漫遊、軌道相機、房間切換與測量；React 管理樓層導覽、材質方案及設計說明。

### 數位展覽

Blender 製作展間 + Hunyuan3D-2 展品；Three.js 處理導覽、聚焦、動畫與互動熱點；React 管理展品卡片、字幕、語言切換與無障礙資訊。

### 3D 遊戲

Blender 製作場景 + Hunyuan3D-2 角色/道具；Three.js 執行遊戲迴圈、相機、輸入、碰撞與互動；React 管理 HUD、任務、圖鑑與存檔。

### 3D 動畫

Blender 製作骨架、表情、鏡頭與命名動畫；Three.js 使用 `AnimationMixer` 播放與混合 GLB 動畫；React 提供播放、暫停、重播、時間軸與字幕控制。

---

## 通用技術流程

```text
需求與參考圖
    -> 分類物件（Blender vs Hunyuan3D-2）
    -> Blender 建立結構件 + Hunyuan3D-2 生成裝飾件
    -> 匯出 GLB
    -> React / TypeScript 建立頁面與 UI
    -> Three.js 載入 GLB、建立場景與互動
    -> 進行效能、手機、鍵盤／觸控與錯誤回復測試
    -> 部署至靜態網站或 Web App 主機
```

---

## 建議的資料夾結構

```text
audit-codex-skills/
├── README.md
├── 審計輔助技能 for Codex/
│   ├── audit-investigation-plan.md
│   ├── audit-secondbrain-setup.md
│   └── audit-working-paper.md
└── 3d-builder/
    ├── SKILL.md
    ├── agents/openai.yaml
    └── references/
        ├── modes.md
        └── quality-gate.md
```

---

## 使用建議

1. 審計工作先使用「審計輔助技能 for Codex」資料夾中的 3 個技能。
2. 3D 網站、空間展示或遊戲製作使用 `$3d-builder`。
3. 複雜有機物件（雕塑、裝飾）優先使用 Hunyuan3D-2 生成，結構件用 Blender。
4. 3D 專案應先建立一個代表性模型與互動，再擴充完整資產集合。
5. 完成前確認瀏覽器可顯示場景、GLB 有錯誤替代畫面、相機可重設、手機控制可操作，且 production build 通過。

---

## 版本紀錄

| 日期 | 版本 | 內容 |
|------|------|------|
| 2026-08-06 | v2.0 | 技能更名為 3d-builder，整合 Hunyuan3D-2 混合建模策略 |
| 2026-08-04 | v1.2 | 將 3 個審計技能整理至「審計輔助技能 for Codex」資料夾，並保留 Blender + React + Three.js 技能資料夾 |
| 2026-07-29 | v1.0 | 建立審計輔助技能集合 |
