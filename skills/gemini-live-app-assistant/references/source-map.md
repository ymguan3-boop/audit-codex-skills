# 上帝之眼現有能力與移植對照

| 能力 | 目前來源 | 移植處置 |
| --- | --- | --- |
| 會話生命週期、停止與工具取消 | `src/voice/session.js` | 可參考結構；保留取消與晚到結果防護 |
| Gemini Live WebSocket、PCM 收發、逐字稿、工具回覆 | `src/voice/geminiLiveSession.js`、`src/voice/pcm-capture.worklet.js` | 範本已抽去地圖專用提示；整合時核對當期 Live 規格 |
| 短效權杖 | `server/providers/gemini.js` | 後端持有 API key；新程式自接驗證／限速 |
| 地圖工具 schema、操作執行 | `src/voice/actionSchemas.js`、`src/voice/gevActions.js` | 不直接複製；每個宿主建立自己的 action registry |
| 程式狀態事件 | `src/voice/sessionCommands.js` 與 Gemini adapter 的 `sendMapEvent` | 目前是結構化文字事件，不等於畫面視覺串流 |
| 真正畫布截圖 | `src/voice/realtimeViewport.js` | 屬另一個 Realtime 通道；Gemini adapter **尚未接入**。只擷取 Cesium canvas，非完整 UI，移植需重新授權／設計 |

注意：原始 Gemini adapter 的 system instruction 含台灣地圖、行車路線及相機環繞等業務規則；可移植核心不可把這些規則硬塞進別的程式。原始 token 路由直接回傳本程式所有工具宣告；新程式須維護自己的 allowlist 與權限。原始程式的語音畫面／工具端到端驗收尚未等同於此技能在別的程式可直接使用。

