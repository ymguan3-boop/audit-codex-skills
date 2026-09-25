# 官方 Share / Project Gallery 協定

## 官方角色

- `share.geolibre.app`：GeoLibre Project Gallery 與 Project → Share 的官方後端。
- `web.geolibre.app`：官方 Web viewer。

## 驗證與 token

使用 Bearer token：
`Authorization: Bearer <GEOLIBRE_SHARE_TOKEN>`

Token 必須由使用者在官方 Share 服務建立／授權。
禁止把 token 寫入 repository 或聊天輸出。

## 建立專案

`POST https://share.geolibre.app/api/projects`

Request body：

```json
{
  "filename": "analysis.geolibre.json",
  "content": "{\"version\":\"0.2.0\", ...}",
  "visibility": "unlisted"
}
```

`content` 是序列化後的 GeoLibre project JSON 字串。

預設 `visibility=unlisted`。
只有使用者明確要求公開出現在 Gallery 才使用 `public`。

## 回傳值

API project 物件可包含：
- `rawJsonUrl`
- `projectUrl`
- `viewerUrl`
- `id`
- `slug`
- `visibility`

優先使用 `rawJsonUrl` 組官方 viewer：

`https://web.geolibre.app/?url=<encodeURIComponent(rawJsonUrl)>&layout=viewer&loading=true&locale=zh-TW`

## Server 限制

- project JSON 上限：50 MiB。
- Share server 只保存 project，不保存使用者本機圖資檔案。
- local file source 在他人瀏覽器無法讀取。
- 遠端 data source 必須是收件者可匿名存取的 HTTPS URL，並允許 CORS。
- 小中型分析成果優先 inline 進 project，避免外部託管依賴。

## 更新既有專案

若後續要覆寫同一官方專案：
1. 保存 API 回傳的 project id。
2. 使用 `PUT /api/projects/{id}/content` 建立新版本。
3. 可用 expectedVersion 做版本提示。
4. 不建立無限重複 project，除非使用者要保留多個獨立成果。

## 分享前 preflight

必須檢查：
- JSON 可解析；
- project 有有效名稱／filename；
- project size < 50 MiB；
- 預設可見結果圖層存在；
- inline GeoJSON 是 FeatureCollection；
- 無 file://、localhost、127.0.0.1、本機絕對路徑；
- 外部 URL 為 HTTPS；
- 若外部 URL 未驗證匿名可讀，改 inline 或停止發布。

## 瀏覽器 QA

上傳後必須用官方 viewer 真實開啟。

桌面與 Android viewport 都要確認：
- HTTP 正常；
- App 已掛載；
- load-state=ready；
- load-errors=[]；
- 有可見 canvas；
- 非白屏；
- 預期主圖層名稱存在；
- 地圖 canvas 有實際像素。

任何一種裝置失敗，都先修正再交付。
