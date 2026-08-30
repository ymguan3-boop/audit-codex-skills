---
name: qgisskill
description: QGIS 地圖自動化 — 說「QGIS 技能」「qgisskill」時載入，安裝 QGIS、下載台灣縣市/鄉鎮資料、設定圖層樣式、載入地址資料
---

當使用者說「qgisskill」或「QGIS 技能」時，依序執行以下完整流程：

## 步驟 1：確認 / 安裝 QGIS

1. 檢查 PATH 及常見安裝路徑是否有 `qgis-ltr-bin.exe`
2. 若未安裝，從 [OSGeo4W 官網](https://download.osgeo.org/osgeo4w/v2/osgeo4w-setup.exe) 下載安裝程式
3. 使用 `osgeo4w-setup.exe --quiet-mode --auto-detect --packages qgis-ltr` 靜默安裝
4. 確認安裝完成後將 `qgis-ltr-bin.exe` 路徑記錄為 `QGIS_EXE`

## 步驟 2：下載宜蘭縣界及鄉鎮市資料

從 g0v/twgeojson GitHub 下載 GeoJSON：

1. 下載 twCounty2010.geo.json（全台縣市界線）
2. 下載 twTown2010.geo.json（全台鄉鎮市區界線）
3. 用 Python 篩選出 COUNTYNAME 包含「宜蘭」的 feature
4. 分別儲存為 `yilan.geo.json` 及 `yilan_townships.geo.json`

## 步驟 3：建立 QGIS 專案

1. 關閉已開啟的 QGIS（若有的話）
2. 用 PyQGIS 建立專案檔（`yilan.qgs`）：
   - 加入 OpenStreetMap XYZ Tiles 底圖
   - 加入 宜蘭縣界（yilan.geo.json）
   - 加入 宜蘭縣鄉鎮市（yilan_townships.geo.json）
   - 設定 CRS 為 EPSG:4326
   - 設定畫布範圍為宜蘭縣界範圍（外加 5% 邊距）
3. 將 GeoJSON 複製到與 .qgs 同目錄（用相對路徑）

## 步驟 4：設定圖層樣式

在 QGS 檔案中，**直接編輯 XML** 設定圖層樣式：

### 宜蘭縣界
| 屬性 | 值 |
|------|------|
| 填色透明度 | 30% |
| 符號透明度 | 0.3 |
| 邊框顏色 | 黑色 (0,0,0) |
| 邊框寬度 | 1.5mm |
| 邊框透明度 | 無 (255) |

### 宜蘭縣鄉鎮市
| 屬性 | 值 |
|------|------|
| 填色透明度 | 30% |
| 符號透明度 | 0.3 |
| 邊框顏色 | 紅色 (255,0,0) |
| 邊框寬度 | 1.2mm |
| 邊框透明度 | 無 (255) |

## 步驟 5：詢問載入地址資料

通知使用者「宜蘭縣地圖已準備好」，詢問：
> 「請問您是否要載入一個 xlsx 或 csv 檔案來進行地址點位分析？檔案中需包含名稱及地址欄位。」

若使用者回答「是」，執行以下流程：

### 5a 讀取檔案
- 讀取 xlsx 或 csv 檔案，解析欄位名稱
- 自動偵測編碼（UTF-8 with BOM / Big5 / UTF-8）
- 自動比對欄位：尋找名稱欄（name/名稱/瓦斯行名稱/…）及地址欄（address/地址/瓦斯行地址/…）

### 5b 地址解析（地理編碼）
- 從地址字串中自動擷取鄉/鎮/市關鍵字（如「冬山鄉」、「蘇澳鎮」）
- 若地址缺少「宜蘭縣」前綴則自動補上
- 用 Nominatim API 查詢該鄉鎮的中心點座標（限宜蘭縣境內）
- 加入 ±0.015 度（約 1.5km）的亂數位移，避免同鄉鎮點位完全重疊

### 5c 加入圖層
- 將地址點位以 delimitedtext 方式加入 QGIS 專案
- 設定欄位：X=lon, Y=lat, CRS=EPSG:4326
- 在圖層屬性中設定依「類型」分類樣式（如瓦斯行 vs 儲存場用不同顏色）

## 步驟 6：啟動 QGIS

關閉既有 QGIS 行程，以專案檔重新啟動，並將視窗移至 (0,0) 位置、大小 1700x1000。

## 注意事項

- Nominatim 有每秒 1 次查詢限制，查詢間隔需大於 1.1 秒
- 若 Nominatim 查詢失敗，改用鄉鎮中心點預設值（見 town_coords.json）
- 宜蘭縣 12 鄉鎮預設中心點座標使用 `town_coords.json`
- QGS 專案檔可直接以 Python xml.etree.ElementTree 編輯，或使用 PyQGIS 的 QgsProject
- QGIS 3.44+ 安裝路徑預設為 `C:\Program Files\QGIS 3.44.x\bin\qgis-ltr-bin.exe`
