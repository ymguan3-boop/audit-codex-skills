---
name: ezbid-bidders
description: ezbid.tw 投標廠商資料抓取 — 從台灣政府採購與標案情報站抓取各標案的投標廠商列表。說「抓投標廠商」「投標廠商資料」「ezbid-bidders」「投標廠商列表」時載入
---

# ezbid.tw 投標廠商資料抓取

## 快速指令

**「抓取投標廠商資料」**

一句話完成：自動從 ezbid.tw 抓取各標案的投標廠商列表，並存入本地資料庫。

## 功能

從 ezbid.tw（台灣政府採購與標案情報站）抓取投標廠商資料。

| 步驟 | 說明 |
|------|------|
| 1. 讀取標案清單 | 從本地資料庫取得所有標案案號 |
| 2. 導航至 ezbid.tw | 逐一訪問各標案詳細頁面 |
| 3. 解析投標廠商 | 使用 Playwright 渲染頁面並解析廠商列表 |
| 4. 儲存資料 | 將投標廠商資料存入本地資料庫 |

## 使用方式

### 便捷指令（推薦）

在 opencode 中直接說：

```
抓投標廠商資料
```

AI 會自動：
1. 執行 `fetch_bidders.py` 腳本
2. 從 ezbid.tw 抓取所有標案的投標廠商
3. 將資料存入 `投標廠商` 資料表
4. 回報抓取結果

### 方法二：直接執行腳本

```bash
python skills/ezbid-bidders/fetch_bidders.py              # 抓取所有標案
python skills/ezbid-bidders/fetch_bidders.py --limit 10    # 僅抓取前10筆
python skills/ezbid-bidders/fetch_bidders.py --test        # 測試模式（僅抓取1筆）
```

### 方法三：抓取單一標案

```python
from skills.ezbid_bidders.fetch_bidders import fetch_tender_bidders

# 抓取特定標案的投標廠商
bidders = fetch_tender_bidders(page, agency_code="3.76.42.54", tender_id="TA1080521")
```

## 檔案結構

```
ezbid-bidders/
├── SKILL.md                 # 技能說明文件
├── README.md                # 詳細說明文件
├── fetch_bidders.py         # 主要抓取腳本
└── requirements.txt         # Python 依賴
```

## 資料庫結構

投標廠商資料表欄位：

| 欄位名稱 | 類型 | 說明 |
|---------|------|------|
| id | INTEGER | 自動編號 |
| 標案案號 | TEXT | 標案編號 |
| 機關代碼 | TEXT | 機關統一編碼 |
| 機關名稱 | TEXT | 機關名稱 |
| 標案名稱 | TEXT | 標案名稱 |
| 廠商名稱 | TEXT | 投標廠商名稱 |
| 是否得標 | TEXT | 是/否 |
| 投標金額 | REAL | 投標金額 |
| 價差 | TEXT | 與底價或預算價差 |
| 更新時間 | TIMESTAMP | 更新時間 |

## 依賴

- Python 3.10+
- playwright
- Chromium（透過 playwright install 安裝）

## 注意事項

- ezbid.tw 資料來源為政府電子採購網（PCC），每日更新三次
- 每次請求間隔 1 秒，避免過度請求
- 抓取過程中如遇到錯誤，會記錄至 log 檔案
