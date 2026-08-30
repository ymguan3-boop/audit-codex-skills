---
name: fjudsearch
description: 司法院裁判書系統（FJUD）判決查詢 — 說「查判決」「裁判書查詢」「fjudsearch」「司法查詢」時載入
---

# 司法院裁判書系統（FJUD）判決查詢

## 可用工具
1. **websearch** — 搜尋判決字號、案情關鍵字、當事人
2. **webfetch** — 直接抓取判決頁面
3. **Playwright MCP**（playwright_browser_*） — 瀏覽器操作 FJUD 系統

## 查詢網站

| 網站 | 網址 | 說明 |
|------|------|------|
| FJUD 裁判書查詢 | `https://judgment.judicial.gov.tw` | 主系統，含各級法院裁判書 |
| 憲法法庭 | `https://cons.judicial.gov.tw` | 憲法判決、暫時處分 |
| 司法院主網 | `https://www.judicial.gov.tw` | 法學資料檢索 |
| 司法院法學資料檢索 | `https://law.judicial.gov.tw` | 判決、判例、決議、座談會 |

## 搜尋流程

### Step 1 — 用判決字號直接搜尋
```
"{年度}年{種類}字第{號}"
```

常見字號格式：
| 字號範例 | 說明 |
|---------|------|
| 115年憲判字第2號 | 憲法法庭判決 |
| 114年度司促字第3973號 | 支付命令 |
| 113年度訴字第123號 | 民事訴訟 |
| 112年度易字第456號 | 刑事訴訟 |
| 111年度簡字第78號 | 簡易案件 |
| 110年度交訴字第90號 | 交通案件 |

### Step 2 — 用關鍵字搜尋
```
"{當事人姓名}" "判決" site:judgment.judicial.gov.tw
"{公司名稱}" "民事判決"
"{廠商名}" "支付命令"
```

### Step 3 — 直接操作 FJUD 網站（Playwright）
```
playwright_browser_navigate "https://judgment.judicial.gov.tw"
```
操作步驟：
1. 在搜尋框輸入關鍵字（當事人、公司名、字號）
2. 可依法院別、案件類別、審級篩選
3. 點擊案號查看判決全文
4. 支援 PDF 下載

### Step 4 — 下載判決
FJUD 支援 PDF 下載，可用 Playwright 點擊下載按鈕取得全文。

## 查詢策略

| 情境 | 建議查詢方式 |
|------|------------|
| 已知字號 | 直接 websearch 或 FJUD 查字號 |
| 查公司涉訟紀錄 | websearch 公司名 + 判決/支付命令 |
| 查個人前科或官司 | websearch 姓名 + 判決 |
| 查特定法律見解 | 法學資料檢索 law.judicial.gov.tw |
| 查近期憲法判決 | cons.judicial.gov.tw |

## 注意事項
- FJUD 有反爬機制，headless 模式可能被阻擋
- 建議使用非 headless 模式（show_browser=true）操作官方網站
- 部分舊判決或簡易判決（如支付命令）可能只有摘要
- 憲法法庭判決可從 cons.judicial.gov.tw 下載完整 PDF
- 下級審判決可透過引用字號反查上級審
- 支付命令（司促）屬非訟程序，未經言詞辯論，證據力較低
- 裁判書公開原則上不包括少年及家事案件

## 應用範例
```
# 查公司是否被聲請支付命令
websearch "{公司名} 支付命令 法院"

# 查特定法律見解
websearch "{法律問題} 最高法院 判決"

# 查廠商涉訟紀錄
websearch "{統編} 判決 site:judgment.judicial.gov.tw"
```
