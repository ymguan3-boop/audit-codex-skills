# build_reportskill — 審計機關調查報告自動彙整工具

從**調查計畫**與**工作底稿**（.doc/.docx）自動產出符合審計機關格式之調查報告（.docx）。

## 特色

- 支援 .doc 與 .docx 輸入格式
- 自動依使用者格式規格套用縮排、粗體、字型、行高
- 自動從工作底稿去重、分節（依各公所）
- 支援多份工作底稿同時彙入
- 柒、查核意見保留特殊格式（township heading、注意事項、首筆粗體）
- 表格自動保留並套用 12pt 表身字型

## 格式規格

| 層級 | 左縮排 | 首行縮排 | 粗體 | 字型大小 |
|------|--------|----------|------|----------|
| **TITLE** | 0 | 0 | ✓ | 18pt |
| **L1**（壹、貳…） | 0 | 0 | ✓ | 16pt |
| **L2**（一、二…） | 1字元(320twips) | -2字元 | ✓ | 16pt |
| **L3**（(一)(二)） | 3字元(960twips) | -2字元 | ✓ | 16pt |
| **L4**（1.2.3.） | 6字元(1920twips) | -2字元 | ✓ | 16pt |
| **Body** | 4字元(1280twips) | 2字元(640twips) | ✗ | 16pt |
| **Table title** | 置中 | — | ✗ | 14pt |
| **Table body** | — | — | ✗ | 12pt |
| **Source note** | — | — | ✗ | 10pt |

- 字型：標楷體
- 固定行高：28pt
- 全形括號自動轉換

## 安裝

```powershell
# 複製至 opencode skill 目錄
cp -Recurse build_reportskill "$env:USERPROFILE\.config\opencode\skills\audit-report-builder"

# 相依套件
pip install python-docx lxml pywin32
```

## 使用方式

### 命令列

```powershell
python build_report.py `
  --plan "調查計畫.doc" `
  --workpapers "工作底稿(1).docx" `
  --workpapers "工作底稿(2).docx" `
  --output "調查報告_完成.docx"
```

### 參數說明

| 參數 | 說明 |
|------|------|
| `--plan` | 調查計畫檔案路徑（.doc 或 .docx） |
| `--workpapers` | 工作底稿檔案路徑，可重複指定多份 |
| `--template` | (選用) 自訂 Word 樣板路徑 |
| `--output` | (選用) 輸出檔案路徑，預設為「調查報告_彙整完成.docx」 |

### 做為 opencode 技能

載入 `SKILL.md` 後，opencode 會自動引導輸入調查計畫及工作底稿檔案。

## 產出章節結構

1. 壹、查核緣起（含調查對象及範圍）
2. 貳、查核依據
3. 參、查核範圍（含表1採購案件明細）
4. 肆、查核限制（固定文句）
5. 伍、查核重點
6. 陸、查核事實（去重＋工作底稿表格）
7. 柒、查核意見（依公所分節）
8. 捌、擬議處理意見（含聯絡資訊）
9. 玖、附錄（工作底稿索引＋調查計畫）

## 檔案結構

```
build_reportskill/
├── build_report.py          # 主程式
├── SKILL.md                 # opencode 技能描述
├── README.md                # 本使用說明
└── template/
    └── 調查報告.docx         # Word 樣板
```

## 環境需求

- Python 3.8+
- python-docx, lxml, pywin32 (optional, for .doc support)
- Windows (for pywin32 .doc 讀取)
