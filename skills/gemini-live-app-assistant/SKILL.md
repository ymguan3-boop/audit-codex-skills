---
name: gemini-live-app-assistant
description: 將 Gemini Live 即時語音助理接入網頁程式，使其在使用者授權下讀取目前程式狀態／畫面、呼叫已註冊功能並以語音回覆；適用於移植、擴充或驗收跨程式語音控制。
---

# Gemini Live 程式助理

此技能抽取「上帝之眼」的語音連線模式，不複製其地圖專用指令。把 Gemini 連線、宿主程式功能、畫面取用分成三個邊界。先閱讀 [宿主契約](references/host-contract.md)；若要從上帝之眼移植，再閱讀 [來源對照](references/source-map.md)。可複製 `assets/portable/` 的範本作起點，但必須依目標程式補上宿主功能、授權、UI 和測試。

## 工作流程

1. 盤點目標程式的功能與狀態來源，建立受控 action registry。每個工具要有參數 schema、結果格式、風險等級與可取消方式；不以 DOM 任意點擊或模型自寫程式碼取代工具。
2. 後端保管 Gemini API key，經已驗證的使用者請求換取短效 Live token。瀏覽器只持有短效 token；模型名稱及通訊格式以整合當時的 [官方 Live 文件](https://ai.google.dev/gemini-api/docs/live-api/get-started-websocket)核對，不把本專案常數當成永久規格。
3. 前端建立可明確開關的會話：麥克風 AudioWorklet → PCM 16-bit／16 kHz → Live；處理逐字稿、音訊播放、工具呼叫／回覆、打斷、逾時、停止與資源釋放。
4. 「看目前畫面」分兩層：先送結構化程式狀態；需要視覺辨識時，經使用者明確開啟畫面分享，再由宿主提供**當前且已遮蔽敏感資料**的 JPEG 畫面。不得把舊影格稱為即時畫面，也不得默認擷取整個桌面。靜態網頁的 canvas 擷取不等於整個程式 UI；來源與涵蓋範圍要對使用者說明。
5. 只讓模型呼叫已註冊、經參數驗證的功能；具刪除、外送、付費或不可逆影響的動作須由宿主再次確認。工具回覆須明示成功／失敗，助理不得在失敗時宣稱完成。
6. 做離線測試（權限拒絕、連線失敗、取消、過期影格、工具錯誤、未知工具、重複呼叫、慢速網路），再用測試金鑰做端到端語音／畫面／操作驗收；沒有完成真實驗收時標為未驗證。

## 可移植資產

- [宿主轉接範本](assets/portable/host-bridge.mjs)：動態工具清單、狀態讀取、權限與執行邊界。
- [Gemini Live 瀏覽器範本](assets/portable/gemini-live-client.mjs) 與 [PCM Worklet](assets/portable/pcm-capture.worklet.js)：短效權杖、語音、文字、工具回覆、可選畫面影格。
- [分頁畫面範本](assets/portable/tab-frame.mjs)：使用者點擊授權後只接受瀏覽器分頁分享，供 `getFrame` 使用；不適合包含敏感 UI 的畫面。
- [短效權杖後端範本](assets/portable/token-handler.mjs)：以 Web Request／Response 介面示範後端換權杖；須接入目標程式的登入、限速與環境變數。

以上資產是跨程式起點，不宣稱已替新程式取得麥克風、擷取畫面或接通所有功能。不得複製 `.env`、真實金鑰、地圖供應商 URL、使用者資料或本專案的應用專用工具清單。

移植範本改寫自本專案的 MIT 程式碼；若複製到別的程式，保留 [原作者授權聲明](assets/portable/NOTICE.md)。本技能沒有附帶原專案資料集或第三方影像。

