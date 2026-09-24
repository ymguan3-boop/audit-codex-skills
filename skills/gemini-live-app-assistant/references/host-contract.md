# 宿主程式契約

## 最小介面

```js
const host = createHostBridge({
  getState: async ({ signal }) => ({ page: '地圖', selectedLayers: [] }),
  getFrame: async ({ signal }) => ({ mimeType: 'image/jpeg', data: '<base64>', fresh: true }),
  actions: [{
    name: 'open_layer',
    description: '開啟已介接圖層',
    parameters: { type: 'object', properties: { id: { type: 'string' } }, required: ['id'] },
    risk: 'low',
    validate: ({ id }) => typeof id === 'string' && id.length < 80 || '圖層 ID 不合法',
    run: async ({ id }, { signal }) => ({ ok: true, layerId: id }),
  }],
  confirm: async ({ action, args }) => true,
});
```

`getState` 回傳小而明確的 JSON：目前頁面、可見功能、選取物件、已啟用圖層、載入／錯誤狀態及資料時間。遮蔽金鑰、個資、私人訊息與隱藏視窗內容；對即時資料標明觀測時間及來源。`getFrame` 可省略；若提供，必須是使用者目前授權範圍內**新鮮**影格。失敗、背景分頁或無法遮蔽時回傳 `null`，不要回傳快取舊影格。

`actions` 逐項註冊可操作功能。不要宣稱「全部功能」已涵蓋，除非宿主的功能清冊與工具清冊已對照通過。對重要操作建議回傳 `{ ok, message?, data?, observedAt? }`；失敗回傳 `{ ok:false, error }`。高風險工具須 `risk:'confirm'` 並接 `confirm`，不允許模型自己批准。要允許停止長任務時，`run` 必須處理 AbortSignal；不能取消的動作需明示。

整合時由後端掛載 `createGeminiTokenHandler`，依宿主登入與權限完成 `authorize`，另加每位使用者的限速；長期金鑰只從後端環境變數讀取。前端在使用者點擊啟動後建立 `createGeminiLiveClient({ host, onEvent })`，把 `connecting/listening/speaking/idle/error` 接到可見 UI；關閉按鈕呼叫 `stop()`。需要視覺輸入時，另由使用者明確切換 `setVisualSharing(true)`，並顯示分享指示燈。僅「看目前畫面一次」則可在授權後呼叫 `shareFrame()`；結構化狀態用 `sendState()`。完整工具宣告應與宿主 registry 一致，新增／移除工具後重新建立 Live 會話。

## 畫面來源與效能

- 單一 canvas 截圖只涵蓋畫布，不涵蓋 DOM 面板；需看完整網頁時由宿主提供合規的分層 UI 狀態或在使用者授權後採用頁面／分頁擷取。不可假設瀏覽器能無提示擷取整個桌面。
- `tab-frame.mjs` 僅為使用者授權的分頁擷取起點：瀏覽器可能讓使用者選到別的分頁，宿主應清楚顯示分享對象與停止按鈕；含密碼、金鑰、私人聊天或第三方資料的頁面不得直接分享。需要精準遮蔽時，優先由宿主輸出專用、已遮蔽的畫面，而不是擷取整個分頁。
- 優先按需送畫面；若啟用連續影格，最多每秒 1 張，限制尺寸／編碼大小、網路積壓和頻寬。畫面含個資時應停用或遮蔽。
- 關閉語音時應停止麥克風軌、影格計時器、播放節點、WebSocket 與未完成工具。UI 顯示「連線中、聆聽、說話中、錯誤、已關閉」。
- 對看不到或不確定的畫面內容說「無法確認」，不以語音模型推測當作已觀察事實。

## 驗收矩陣

| 案例 | 必須可見的結果 |
| --- | --- |
| 開啟／關閉／重開 | 狀態正確、麥克風燈號正確、舊連線與軌道已釋放 |
| 問目前畫面 | 答案與當前狀態／新鮮影格一致；未授權畫面時明說無法看畫面 |
| 呼叫每個已註冊工具 | 參數驗證、權限、執行結果與助理敘述一致 |
| 未知／高風險工具 | 拒絕執行或等待宿主確認 |
| 延遲／斷線／取消 | 不堆積影格、不執行過期動作、不遺留麥克風 |
| 真實端到端 | 用測試帳號核對語音輸入→Gemini→工具→畫面狀態→語音回覆 |

## 官方規格核對

開始移植時檢查 [Live API 能力](https://ai.google.dev/gemini-api/docs/live-api/capabilities)、[短效權杖](https://ai.google.dev/gemini-api/docs/live-api/ephemeral-tokens)及[WebSocket 入門](https://ai.google.dev/gemini-api/docs/live-api/get-started-websocket)。模型、會話限制與計費會變，不把此文件視為永久 API 規格。

