# audit-codex-skills

個人 Codex 技能集合，主要用於政府審計、地方情資、資料蒐集、第二大腦維護、簡報、3D 與影音製作。

## 目錄

- `skills/`：Codex 個人技能，共 31 個（已清理：移除頂層重複 `3d-builder/` 與舊版 `審計輔助技能 for Codex/`，僅保留 `skills/` 內最新版）。
- `.github/`：GitHub 設定。

## 技能索引

### 審計與第二大腦

| 技能 | 功能 | 快速指令 |
|---|---|---|
| `audit-secondbrain-setup` | 建置或修復 Obsidian、MCP、CLAUDE.md 與審計第二大腦設定。 | `第二大腦安裝`、`審計第二大腦設定` |
| `audit-working-paper` | 依查核事實及案例產出四階段審計工作底稿，並產出 MD 與 Word。 | `生成工作底稿`、`working-paper` |
| `audit-investigation-plan` | 依調查主題產出調查計畫，並可接續產出法規、調閱資料清單及缺失評估問卷。 | `生成調查計畫`、`investigation-plan` |
| `audit-info-publish` | 參考審計部近 2 年類似案例，撰寫正式重要審計資訊發布稿。 | `寫審計資訊`、`audit-info-publish` |
| `audit-report-builder`（資料夾：`build_reportskill`） | 彙整調查計畫與工作底稿，產出完整調查報告。 | `彙整調查報告`、`audit-report` |
| `gov-intelligence` | 蒐集地方政府與公共議題資訊，分析事件脈絡、風險及審計切入點。 | `情資分析`、`地方情資`、`gov-intelligence` |

### 採購、司法與資料蒐集

| 技能 | 功能 | 快速指令 |
|---|---|---|
| `pccsearch` | 查詢政府電子採購網標案資料。 | `搜標案`、`查標案`、`pccsearch` |
| `ezbid-bidders` | 從 ezbid.tw 抓取標案投標廠商列表。 | `抓投標廠商`、`ezbid-bidders` |
| `pcic-export` | 從公共工程雲端服務網匯出宜蘭縣所屬機關標案 Excel。 | `匯出標案`、`pcic-export` |
| `fjudsearch` | 查詢司法院裁判書系統判決。 | `查判決`、`fjudsearch` |
| `lvrlandmoigov` | 查詢內政部不動產交易實價登錄資料。 | `實價登錄`、`查房價`、`lvrlandmoigov` |

### 地圖、3D 與互動場景

| 技能 | 功能 | 快速指令 |
|---|---|---|
| `qgisskill` | 自動化 QGIS 安裝、臺灣行政區圖資下載、圖層設定及地址資料載入。 | `QGIS 技能`、`qgisskill` |
| `gis-3d-model-builder` | 整合正射影像、地形、道路、工程及 GIS 資料，建立可追溯 3D 模型。 | `GIS 3D 建模`、`gis-3d-model-builder` |
| `3d-builder` | 使用 Blender、AI 3D 或 Three.js 建立、驗證及交付 3D 資產與互動場景。 | `做 3D 模型`、`Blender 建模`、`3d-builder` |

### 簡報與教學教材

| 技能 | 功能 | 快速指令 |
|---|---|---|
| `html-slide-builder` | 將教材、講義、PDF 或主題轉成 Reveal.js HTML 互動簡報（含 Firebase 互動）。 | `做 HTML 簡報`、`html-slide-builder` |
| `soil-html-deck` | SOIL 風格單檔可攜式 HTML 簡報（HTML 變體）。 | `SOIL HTML 簡報`、`soil-html-deck` |
| `soil-image-deck` | SOIL 風格圖片式投影片（全頁點陣圖→PPTX，視覺衝擊變體）。 | `圖片簡報`、`soil-image-deck` |
| `soil-teaching-deck` | SOIL 風格可編輯教學型 PowerPoint（可編輯文字、認知負荷分析變體）。 | `教學簡報`、`soil-teaching-deck` |

> `soil-*` 三款為同 SOIL 設計系統不同輸出變體（HTML / 圖片 / 教學），非重複，依輸出需求擇一。

### 影音剪輯（基礎）

| 技能 | 功能 | 快速指令 |
|---|---|---|
| `video-use` | 對話式通用影片編輯（轉錄、剪輯、調色、疊圖、字幕；含 `manim-video`）。 | `編輯影片`、`加字幕`、`video-use` |
| `chatgpt-short-video-editor` | 垂直短影音專用剪輯（Reel/Short/TikTok 垂直流程，依賴 `video-use`）。 | `剪短影音`、`做 Reel` |
| `chatgpt-video-editing-setup` | 短影音環境安裝/修復/驗證（FFmpeg、字型、ElevenLabs）。 | `設定短影音環境`、`video editing setup` |
| `separate2allmakevideos` | 多段分鏡合成為完整旁白影片（逐場旁白、SRT、混音、YouTube 描述）。 | `多段影片合成`、`separate2allmakevideos` |

> 基礎四款為同域分工（通用 vs 垂直 vs 環境 vs 多段合成），非重複，依任務擇一；`video-use` 為最通用（33 檔/738KB）。

### 影片生成（依風格）

| 技能 | 功能 | 快速指令 |
|---|---|---|
| `3d-animation-short-generator` | 從故事概念規劃角色、場景、分鏡及聲音，製作 3D 動畫短片。 | `做 3D 動畫短片` |
| `brand-promo-video-generator` | 將品牌、產品、網站或 App 資料整理成宣傳短片流程。 | `做品牌宣傳片` |
| `co-op-game-intro-generator` | 製作雙人合作遊戲選單或開場動畫。 | `做合作遊戲開場` |
| `handdrawn-live-video-generator` | 製作手繪發光動畫與實景融合的單場景短片。 | `做手繪風格實景影片` |
| `minimalist-product-ad-generator` | 將產品照片與賣點轉成極簡電商廣告短片。 | `做極簡產品廣告` |
| `music-video-subtitle-generator` | 規劃 MV、歌詞字幕、節拍文字及鏡頭提示詞。 | `做 MV 字幕` |
| `paper-collage-explainer-generator` | 將知識或觀點轉成紙張拼貼風格解說影片。 | `做拼貼畫解說影片` |
| `papercraft-stop-motion-explainer` | 以紙藝、立體紙景及定格動畫解釋知識主題。 | `做紙藝定格解說動畫` |

### 互動寵物

| 技能 | 功能 | 快速指令 |
|---|---|---|
| `hatch-pet` | 製作、修復、驗證及封裝 Codex v2 動態寵物或品牌吉祥物。 | `做 Codex pet`、`hatch-pet` |

## 使用方式

1. 將本倉庫的 `skills/<技能名稱>/` 複製到 Codex 的個人技能目錄。
2. 在 Codex 輸入快速指令，或直接描述工作目標與輸入資料。
3. 審計第二大腦的原始資料請放在 `資料蒐集/`；使用 `/資料處理` 批次轉換、分類、去重並更新查核意見索引。
4. 需要工作底稿、調查計畫或分析報告時，應讓技能將生成文件存入第二大腦的對應產出目錄。

## 同步範圍與清理紀要

本次同步來源為使用者本機 Codex 個人技能目錄，包含每個技能的 `SKILL.md`、參考資料、腳本、模板及必要資產。排除 `.system`、`.git`、`.venv`、`node_modules`、快取、編譯輸出及其他可由環境重新產生的檔案，不包含本機密碼或 API 金鑰。

**清理（2026-08-30）：**
- 刪除頂層重複 `3d-builder/`（與 `skills/3d-builder/` 內容重複，保留 `skills/` 內最新版 3d-builder）。
- 刪除舊版 `審計輔助技能 for Codex/`（內含 `audit-investigation-plan.md` 等 3 檔舊版文件，已由 `skills/audit-investigation-plan`、`skills/audit-working-paper`、`skills/audit-secondbrain-setup` 取代）。
- `skills/` 內 31 個技能經比對 `name` 皆唯一，無功能完全重複；`soil-*` 三款與 `video-use` 系列為同域不同輸出/流程的變體，予以保留並重新分類如下。

最後同步日期：2026-08-30（清理後重新分類版）
