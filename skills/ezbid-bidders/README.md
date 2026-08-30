# ezbid.tw 投標廠商資料抓取

從台灣政府採購與標案情報站（ezbid.tw）抓取各標案的投標廠商列表，並存入本地 SQLite 資料庫。

## 資料來源

| 項目 | 說明 |
|------|------|
| **網站名稱** | 台灣政府採購與標案情報站 |
| **網址** | https://ezbid.tw |
| **資料來源** | 政府電子採購網（PCC） |
| **資料庫總量** | 5,560,438 筆 |
| **更新頻率** | 每日三次 |

### 為何選擇 ezbid.tw？

| 平台 | 投標廠商列表 | 備註 |
|------|-------------|------|
| **ezbid.tw** | ✅ 有 | 資料來源為 PCC，有預算過濾、分類功能 |
| **bid.twincn.com** | ❌ 無（查無資料） | 僅有得標廠商，無完整投標列表 |
| **pcc.mlwmlw.org** | ❌ 無 | 僅有得標廠商 |
| **PCC 官方** | ✅ 有 | 無法直接存取（反爬機制） |

ezbid.tw 是目前唯一可穩定存取完整投標廠商列表的第三方平台。

## 功能

- 從 ezbid.tw 抓取各標案的投標廠商列表
- 解析廠商名稱、是否得標、投標金額、價差等資訊
- 將資料存入本地 SQLite 資料庫
- 支援批次抓取與單筆測試

## 安裝

### 1. 安裝依賴

```bash
pip install playwright
playwright install chromium
```

### 2. 設定資料庫路徑

預設資料庫路徑為腳本同層目錄的 `政府採購決標資訊研析系統.db`，可透過 `--db` 參數指定。

## 使用方式

### 抓取所有標案

```bash
python fetch_bidders.py
```

### 限制抓取筆數

```bash
python fetch_bidders.py --limit 10
```

### 測試模式（僅抓取1筆）

```bash
python fetch_bidders.py --test
```

### 指定資料庫路徑

```bash
python fetch_bidders.py --db /path/to/database.db
```

## 資料庫結構

### 投標廠商資料表

| 欄位名稱 | 類型 | 說明 |
|---------|------|------|
| id | INTEGER | 自動編號（主鍵） |
| 標案案號 | TEXT | 標案編號 |
| 機關代碼 | TEXT | 機關統一編碼 |
| 機關名稱 | TEXT | 機關名稱 |
| 標案名稱 | TEXT | 標案名稱 |
| 廠商名稱 | TEXT | 投標廠商名稱 |
| 是否得標 | TEXT | 是/否 |
| 投標金額 | REAL | 投標金額 |
| 價差 | TEXT | 與底價或預算價差 |
| 更新時間 | TIMESTAMP | 更新時間 |

### SQL 範例

```sql
-- 查詢特定標案的所有投標廠商
SELECT * FROM 投標廠商 WHERE 標案案號 = 'TA1080521';

-- 查詢特定廠商的所有投標紀錄
SELECT * FROM 投標廠商 WHERE 廠商名稱 LIKE '%將丞%';

-- 統計各廠商得標次數
SELECT 廠商名稱, COUNT(*) as 得標次數 
FROM 投標廠商 
WHERE 是否得標 = '是' 
GROUP BY 廠商名稱 
ORDER BY 得標次數 DESC;
```

## 檔案結構

```
ezbid-bidders/
├── SKILL.md                 # opencode 技能說明文件
├── README.md                # 本文件
├── fetch_bidders.py         # 主要抓取腳本
└── requirements.txt         # Python 依賴
```

## 注意事項

1. **請求頻率**：每次請求間隔 1 秒，避免過度請求
2. **頁面渲染**：ezbid.tw 需要 JavaScript 渲染，必須使用 Playwright
3. **資料更新**：ezbid.tw 每日更新三次，抓取資料可能有延遲
4. **錯誤處理**：抓取過程中如遇到錯誤，會記錄至 log 檔案

## 授權條款

MIT License

## 資料來源聲明

本工具抓取之資料來自 [台灣政府採購與標案情報站](https://ezbid.tw)，該平台資料來源為 [政府電子採購網](https://web.pcc.gov.tw)。資料僅供研究參考使用。
