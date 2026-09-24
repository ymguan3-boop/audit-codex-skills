# Gemini Live 程式語音助理

把 Gemini Live 即時語音接入網頁程式，讓助理在使用者授權下讀取程式狀態或畫面、呼叫宿主明確註冊的功能，並以語音回覆。

## 內容

- `SKILL.md`：移植與驗收流程。
- `references/host-contract.md`：宿主狀態、工具、權限與畫面介面。
- `references/source-map.md`：上帝之眼現有程式與可移植部分對照。
- `assets/portable/`：瀏覽器 Live 客戶端、PCM Worklet、宿主工具轉接、短效權杖後端及使用者授權的分頁畫面範本。
- `tests/portable.test.mjs`：工具白名單、風險確認、權杖回應與會話啟停的離線測試。

## 使用

將 `skills/gemini-live-app-assistant/` 複製到 Codex 技能目錄，於目標程式專案中要求 Codex 使用 `$gemini-live-app-assistant`。依宿主契約註冊可用功能與狀態，再接入登入、權杖端點及前端語音 UI。

助理只會呼叫宿主程式註冊並驗證過的功能。要查看畫面，目標程式需提供新鮮、已授權且適當遮蔽的畫面影格；分頁擷取須由使用者主動授權。安裝技能本身不會自動授予程式操作權限。

## 安全與限制

- Gemini API 長期金鑰留在後端；瀏覽器只使用短效 Live 權杖。
- 高風險操作由宿主程式要求使用者確認；未知工具拒絕執行。
- 若沒有取得新鮮畫面或程式狀態，助理必須如實說明無法確認。
- 範本仍需依目標程式的框架、身分驗證、功能介面及當期 Gemini Live 規格調整，並執行真實端到端驗收。
- 原專案的地圖資料及第三方素材不包含於本技能。

範本授權與原作者聲明見 [NOTICE](assets/portable/NOTICE.md)。
