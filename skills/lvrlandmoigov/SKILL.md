---
name: lvrlandmoigov
description: 內政部不動產交易實價登錄查詢 — 說「實價登錄」「查房價」「查實登」「房價查詢」「lvrlandmoigov」時載入
---

# 內政部不動產交易實價登錄（lvr.land.moi.gov.tw）查詢方法

## 資料概覽

| 交易類型 | 更新頻率 | 說明 |
|---------|---------|------|
| 買賣 | 每月1/11/21日 | 成屋買賣交易 |
| 預售屋 | 每月1/11/21日 | 預售屋交易（含建案名稱） |
| 租賃 | 每月1/11/21日 | 房屋租賃交易 |

## 可用工具

1. **websearch** — 快速取得區域行情概況、建案價格區間
2. **webfetch** — 抓取第三方彙整平台結構化資料
3. **Playwright MCP**（playwright_browser_*）— 瀏覽器操作 opendata.vip 或官方站直接查詢

## 第三方自動化查詢平台（推薦）

### opendata.vip（內政部預售屋實價登錄整合）
| 項目 | 說明 |
|------|------|
| 網址 | `https://www.opendata.vip/tool/landmoi?city={縣市}&zone={行政區}` |
| 資料範圍 | 109年1月~最新（全台） |
| 涵蓋欄位 | 建案名稱、交易日期、戶別、總價(萬)、單價(萬/坪)、總坪數、房型 |
| 特點 | 無需驗證、結構化表格、支援建案名稱搜尋 |

URL 格式範例:
- 宜蘭縣全區: `https://www.opendata.vip/tool/landmoi?city=宜蘭縣&zone=全區`
- 宜蘭市: `https://www.opendata.vip/tool/landmoi?city=宜蘭縣&zone=宜蘭市`
- 新竹縣竹北市: `https://www.opendata.vip/tool/landmoi?city=新竹縣&zone=竹北市`

**使用方式**：
1. 用 `webfetch` 直接抓取上述 URL，解析 HTML 表格
2. 或使用 Playwright 導航至該頁面，擷取表格資料
3. 如需查詢特定建案，在頁面搜尋框輸入建案名稱

### 各大房仲平台（提供買賣/預售成交行情）
| 平台 | 網址 | 特點 |
|------|------|------|
| 樂居 leju | `https://www.leju.com.tw/price_list/{縣市}?area={郵遞區號}` | 區域均價、價格走勢、成交量 |
| 樂屋網 rakuya | `https://realtyprice.rakuya.com.tw/realprice/result?zipcode={郵遞區號}` | 詳細歷史成交紀錄 |
| 永慶房仲網 | `https://evertrust.yungching.com.tw/regionall/{縣市}/{行政區}` | 實價登錄3.0，地圖查詢 |
| 信義房屋 | `https://www.sinyi.com.tw/tradeinfo/pre-sale/{縣市}/{郵遞區號}-zip` | 預售屋專區 |
| 5168實價登錄比價王 | `https://community.houseprice.tw/list/{縣市}_city/{行政區}_zip` | 建案列表+均價 |
| 591新建案 | `https://newhouse.591.com.tw/list?regionid={ID}&sectionid={ID}` | 預售屋/新成屋建案開價 |

## 查詢流程

### 快速查詢（websearch）
```
"{縣市}{行政區}" 預售屋 實價登錄 單價
"{路段}" 實價登錄 成交行情
"{建案名稱}" 實價登錄 成交
```

### 結構化查詢（webfetch + opendata.vip）
```
webfetch https://www.opendata.vip/tool/landmoi?city=宜蘭縣&zone=宜蘭市
```
回傳結構化 HTML 表格，包含完整欄位可進一步解析。

### 進階查詢（Playwright）
1. 導航至 opendata.vip 或任一房仲平台
2. 填寫查詢條件（縣市、行政區、路段、建案名稱）
3. 擷取結果表格
4. 關閉瀏覽器

## 預售屋資料欄位對照

| opendata.vip 欄位 | 說明 |
|-----------------|------|
| 建案名稱 | 預售屋建案名稱（含建商資訊） |
| 交易日期 | 實際交易日期（年月日） |
| 戶別 | 棟別+戶號/樓層 |
| 總價(萬) | 交易總價（萬元），含車位 |
| 單價(萬) | 每坪單價（萬元/坪） |
| 總坪數 | 建物移轉總面積（坪） |
| 房型 | 幾房幾廳幾衛（如 3房2廳2衛） |

## 資料來源
- [內政部不動產交易實價查詢服務網](https://lvr.land.moi.gov.tw) — 官方來源，每月1/11/21日更新
- [opendata.vip](https://www.opendata.vip/tool/landmoi) — 第三方內政部資料自動化整合平台
- [內政部資料開放平臺](https://data.moi.gov.tw) — 原始開放資料集下載

## 注意事項
- 實價登錄資料有約1~2個月的申報揭露延遲
- 含車位交易之單價計算方式不一，opendata.vip 顯示為含車位單價
- 預售屋均價為各戶型平均值，實際高低樓層、特殊戶型可能有較大差異
- 特殊交易（親友間買賣、持分交易）已被篩除，但仍需注意備註欄
- 官方網站（lvr.land.moi.gov.tw）有 CAPTCHA 驗證機制，headless 瀏覽器可能受阻
- 優先使用 opendata.vip 或各房仲平台取得結構化資料

## 使用範例

### 查詢某區域預售屋行情
```
webfetch "https://www.opendata.vip/tool/landmoi?city=宜蘭縣&zone=全區"
```

### 查詢特定建案
```
websearch "皇程首賦 宜蘭 實價登錄 成交"
```

### 查詢某路段近3年成交行情
```
websearch "宜蘭市中山路 實價登錄 近3年 成交"

# 或用樂屋網:
webfetch "https://realtyprice.rakuya.com.tw/realprice/result?zipcode=260&search=route&keyword=中山路一段"
```
