---
name: pccsearch
description: 政府電子採購網（PCC）標案查詢 — 說「搜標案」「查標案」「pccsearch」「政府採購」時載入
---

# 政府電子採購網（PCC）標案查詢

## 可用工具
1. **websearch** — 快速取得標案概況、廠商得標紀錄
2. **webfetch** — 直接抓取第三方彙整平台頁面
3. **Playwright MCP**（playwright_browser_*） — 瀏覽器操作第三方平台

## 關鍵第三方平台（均串接 PCC 官方資料）

| 平台 | 網址 | 特點 |
|------|------|------|
| 開放政府標案 | `https://pcc.mlwmlw.org/merchants/{統編}` | 快速查統編所有標案，附決標公告 XML 連結 |
| 台灣標案網 | `https://bid.twincn.com/lm.aspx?q={廠商名}` | 得標/未得標分類，含金額、廠商列表 |
| BidAcumen | `https://bidacumen.com/s/v-{廠商名}_{統編}` | 較完整歷史紀錄 |
| 政府資料開放平臺 | `https://data.gov.tw/dataset/15008` | 每月決標資料集 CSV 下載 |

## 搜尋流程

### Step 1 — 用 websearch 初步搜尋
```
"{廠商名}" 得標 決標
"{廠商名}" site:bid.twincn.com
"{廠商名}" 標案 統編:{統編}
```

### Step 2 — 用 webfetch 抓取第三方平台
```
webfetch https://pcc.mlwmlw.org/merchants/{統編}
webfetch https://bid.twincn.com/lm.aspx?q={URL編碼後的廠商名}&t=1
```

### Step 3 — 用 Playwright 操作 bid.twincn.com
```
playwright_browser_navigate "https://bid.twincn.com/lm.aspx?q={URL編碼後的廠商名}&t=1"
```
- 點擊標案列可查看得標金額、未得標廠商名單
- 支援多頁瀏覽

### Step 4 — 交叉比對
- pcc.mlwmlw.org：資料簡潔，適合快速看統編所有標案
- bid.twincn.com：得標/未得標分類及完整金額
- BidAcumen：歷史資料最完整

## 查詢要點

| 查詢方式 | 優點 | 缺點 |
|---------|------|------|
| 統編查詢 | 最精準，避免同名混淆 | 需先知道統編 |
| 廠商名稱查詢 | 方便快速 | 同名廠商可能混淆 |
| 標案名稱/關鍵字 | 可跨廠商查同類型標案 | 結果較發散 |
| 金額區間 | 篩選重大採購 | 需搭配其他條件 |

## 注意事項
- PCC 官方網站（web.pcc.gov.tw）有嚴格反爬機制（Attack ID 20000051），headless 瀏覽器無法直接存取
- 請優先使用第三方彙整平台而非直接連 PCC
- 101 年前的歷史標案可能不在開放資料範圍內
- 統編查詢比廠商名稱更精準（避免同名不同廠商混淆）
- 得標/未得標都要看 — 未得標案件同樣是投標行為紀錄
- 廠商如有更名，舊名稱也要查

## 應用範例
```
# 查詢廠商所有標案
webfetch "https://pcc.mlwmlw.org/merchants/統編"

# 查詢特定類型採購
websearch "道路養護 決標 宜蘭縣 114年"

# 比價分析
websearch "{標案編號} 決標公告 金額"
```
