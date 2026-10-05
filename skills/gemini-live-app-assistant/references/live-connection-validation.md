# 瀏覽器短效權杖與設定故障驗證

適用：Gemini Live 移植、連線失敗、quota錯誤、連線成功但無語音／逐字稿。2026-10-05核對；版本、模型、限制可能改變，執行前核對官方文件與宿主實際安裝SDK。此程序不需要將長期Key放入瀏覽器。

## 1. 分層證據

依序記錄：token provisioning → WebSocket transport → setupComplete → output audio → input ASR → function call → host action result → assistant reply。每一層各自通過，不能以token HTTP200或WebSocket open當作語音驗收成功。

只保存時間、模型、SDK版本、API版本、設定差異、階段、去敏後HTTP/close code與reason、音訊片段數、逐字稿是否收到。禁止記錄API Key、完整auth_tokens名稱、含access_token的URL、Authorization、使用者私密語音或未授權畫面。

## 2. 短效權杖路徑

- 後端保管長期Key，以已驗證請求取得短效token，回應no-store；核對uses、newSessionExpireTime及expireTime。每次新會話取得新的單次token，停止／取消後不用已消耗token重連。
- 驗證瀏覽器收到的是token.name，通常為auth_tokens/開頭，不能送錯整份JSON或長期Key。
- 區分後端長期Key控制組與瀏覽器短效token組。同一模型及最小設定，前者成功不證明後者路徑正確。
- 目前官方短效token文件指定v1beta；raw WebSocket需使用短效token的Constrained方法及access_token，而非標準Key的BidiGenerateContent與key。本範本預設：

```text
wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContentConstrained
```

查詢參數由程式附加，不在紀錄中輸出值。使用SDK時檢查它實際選出的method與版本。部分SDK仍印v1alpha的舊警告；不可只憑警告降版，須比對官方當期規格和相同設定的真實瀏覽器結果。若採proxy或Vertex，核對該架構的官方路徑，不硬套此Developer API範例。
- token取得後立即連線；setupComplete之前close/error須立即拒絕啟動、清除timer並停止麥克風，不能一直顯示「連線中」。晚到連線在stop後立即關閉。

## 3. 最小設定與單一變因對照

使用相同專案Key、網路、API版本及模型，先測最小AUDIO回應，傳送不含私密內容的「請說語音測試成功」。每個設定測試使用新token；最多2次同條件確認，避免無限重試。

|對照|驗證內容|
|---|---|
|基本組|setupComplete、至少1個音訊片段、可理解的回應|
|輸入逐字稿|先inputAudioTranscription={}，實際送16kHz PCM並收到ASR|
|輸出逐字稿|實際收到output transcription，與音訊相符|
|函式工具|只加一個read-only宿主工具；呼叫、回傳、回覆各有證據|
|聲線|單獨加入受支援voice；實際播放，不只檢查聲線名稱|
|系統／風格|單獨加入提示，確認仍連線且回答符合|
|搜尋／額外工具|最後單獨加該功能；基本組成功而加功能失敗則隔離此設定|

每次只改一項，失敗先退回最後成功設定；記錄差異再決定相容策略。模型不可用、401、429、setup設定錯誤、網路中斷需分開診斷。看到quota文字，不直接推論所有模型或整個Key的共用額度耗盡，也不要求使用者先等一天／換Key。

## 4. 已重現案例及修正方式

上帝之眼2026-10-04的v23紀錄：相同Key及v1beta下，3.8、3.1及2.5控制組基本音訊成功；輸入逐字稿、函式工具、聲線、提示各單獨成功，僅加入Google Search時立即close1011 quota exceeded。移除啟動設定的搜尋工具後，兩款指定模型各4項合成語音圖資抽測通過。結論只支持該案例與搜尋設定相關，不能推定所有quota都是此原因，亦無資料判定哪個子額度耗盡。

修正：啟動會話保留已驗工具；搜尋需求透過已註冊宿主工具按需執行既有搜尋服務，回傳來源與日期。新外部服務、外送權限或費用仍依宿主授權，不自行新增。不要直接把所有進階工具永久禁用。

同案3.1加入languageCodes/customVocabulary後可連線但沒有ASR；改成基本inputAudioTranscription={}才收到ASR。語言提示留在系統指令，進階逐字稿欄位依模型能力個別加回驗證，不全域強制另一模型的設定。

案例來源：[上帝之眼v23驗收](https://github.com/ymguan3-boop/good-open-source-collection/blob/main/gods-eye-taiwan-desktop/docs/browser-v23-followup-20261004.md)。這是既有案例證據，不表示本次替每個新宿主完成了實測。

## 5. 驗收關卡

1. 離線：權杖端點身份驗證、無Key、uses/期限、正確Constrained路徑、取消、pre-setup close/error、未知工具與資源釋放。執行node --test skills/gemini-live-app-assistant/tests/portable.test.mjs；這只驗證替身流程。
2. 真實服務：短效token與最小設定通過；模型每款至少2例（明確需求／需追問），工具結果及語音回覆相符。合成PCM可驗ASR，但須標示非實體麥克風。
3. 實體：麥克風收音、喇叭播放、打斷、字幕、聲線自然度、停止／重啟、不持續占用麥克風。
4. 失敗：提供階段、已測控制組、單一設定差異、確定原因與仍未知項；不虛構API剩餘額度，沒有公開數字接口時顯示「未提供」及AI Studio入口。

記錄格式：模型｜SDK/API版本｜transport｜設定差異｜token/setup/audio/ASR/tool各結果｜去敏錯誤｜修正後重測｜未驗項目。

## 官方核對入口

- [Ephemeral tokens](https://ai.google.dev/gemini-api/docs/live-api/ephemeral-tokens)
- [官方JS SDK Live實作](https://github.com/googleapis/js-genai/blob/main/src/live.ts)：短效token選擇Constrained方法；核對安裝版本，main並非固定版本。
- [Live WebSocket](https://ai.google.dev/gemini-api/docs/live-api/get-started-websocket)
- [Rate limits](https://ai.google.dev/gemini-api/docs/rate-limits)
