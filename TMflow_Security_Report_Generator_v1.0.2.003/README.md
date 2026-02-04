# TMflow Security Report Generator v1.0.2.002

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![GUI](https://img.shields.io/badge/GUI-tkinter-orange.svg)

這是 Techman Robot TMflow 產品的安全報告生成工具，基於 Finite State 平台 API 自動生成專業的安全分析報告。提供現代化圖形介面和命令列兩種使用方式。

## 🚀 快速開始

### 圖形化介面 (推薦)
```bash
# 啟動現代化 GUI 應用程式
python ui_modern.py
```

### 命令列模式
```bash
# 使用自動化腳本生成報告
python generate_reports.py
```

## 📋 功能特色

### 🎯 圖形化介面
- **現代化深色主題**: 專業的視覺設計
- **實際 API 整合**: 直接從 Finite State 平台載入專案和版本
- **動態資料更新**: Refresh 按鈕載入最新的專案資料
- **批量報告生成**: 同時處理多個版本
- **即時進度顯示**: 進度條和詳細日誌
- **智能配置管理**: 自動載入和儲存設定
- **錯誤處理機制**: 完善的錯誤提示和恢復

### 📊 報告格式
- **Standard Report**: 標準安全報告
- **Detailed Report**: 詳細漏洞分析報告
- **自動時間戳**: 所有報告包含生成時間
- **PDF 格式**: 專業的報告輸出格式

### 🔧 技術特點
- **實際 API 調用**: 直接連接 Finite State 平台獲取最新資料
- **雙工具整合**: fs-reporter (PDF) + fs-report (多格式)
- **正確的認證**: 使用 X-Authorization header 和正確的 API 端點
- **背景處理**: API 調用和報告生成不阻塞介面
- **配置檔案**: 安全的設定管理
- **多執行緒**: 背景處理不阻塞介面

## 目錄結構

```
TMflow-security-report-generator/
├── ui_modern.py          # 🎨 現代化圖形介面 (主要)
├── generate_reports.py   # 🤖 命令列自動化腳本
├── fs-reporter/          # 📄 PDF 報告生成工具（舊格式）
├── fs-report/           # 📊 HTML/CSV/XLSX 報告生成工具（新格式）
├── reports/             # 📁 生成的報告輸出目錄
├── config.txt           # ⚙️ 配置文件 (不提交到 Git)
├── config.example.txt   # 📋 配置文件範例
├── USAGE_GUIDE.md       # 📖 詳細使用指南
├── UI_Design_Document.md # 🎨 UI 設計文件
└── FS Doc/              # 📚 範例和教學文檔（參考用）
```

## 安裝

### 1. 克隆專案
```bash
git clone https://github.com/kenshu528-oss/tmflow-security-report-generator.git
cd tmflow-security-report-generator
```

### 2. 安裝依賴
```bash
pip install -r requirements.txt
```

### 3. 配置設定
```bash
cp config.example.txt config.txt
# 編輯 config.txt 填入您的 API 資訊
```

### 3. 使用應用程式

#### 🎨 圖形化介面（推薦新手）
```bash
python ui_modern.py
```
- 現代化深色主題介面
- 直觀的操作流程
- 即時進度和日誌顯示
- 詳細使用說明請參考 [USAGE_GUIDE.md](USAGE_GUIDE.md)

#### 🤖 命令列模式（適合自動化）
```bash
python generate_reports.py
```

#### 🔧 手動生成單個報告
```bash
# 標準報告
python fs-reporter/main.py -t [TOKEN] -s [SUBDOMAIN] -pvi [VERSION_ID] -n "Techman Robot" -o "reports/report_name.pdf"

# 詳細報告
python fs-reporter/main.py -t [TOKEN] -s [SUBDOMAIN] -pvi [VERSION_ID] -n "Techman Robot" -d -o "reports/report_name.pdf"
```

## 配置說明

編輯 `config.txt` 文件（從 `config.example.txt` 複製）：

```txt
API_TOKEN=your-finite-state-api-token
SUBDOMAIN=your-subdomain
ORGANIZATION=Techman Robot
OUTPUT_PATH=reports
```

**注意**: 
- 配置檔案會被 `.gitignore` 忽略，不會提交到 Git
- 圖形介面會自動載入和儲存配置
- 點擊 "Reconnect" 按鈕會驗證並儲存當前設定

## 版本信息

### 支援的 TMflow 版本
- **TMflow 2.26.1200.0**: 已測試並支援
- **TMflow 3.12.1300.0**: 待配置版本 ID

## 貢獻

歡迎提交 Issue 和 Pull Request！

### 開發設置
```bash
# 安裝開發依賴
pip install -r requirements.txt

# 運行測試
pytest

# 代碼格式化
black .
```

## 授權

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 文件

## 支援

- 📧 Email: [您的郵箱]
- 🐛 Issues: [GitHub Issues](https://github.com/kenshu528-oss/tmflow-security-report-generator/issues)
- 📖 Wiki: [專案 Wiki](https://github.com/kenshu528-oss/tmflow-security-report-generator/wiki)

## 報告類型

### 1. 標準報告 (Standard)
- 基本風險分析
- 組件統計
- 漏洞嚴重程度分布
- 許可證分析

### 2. 詳細報告 (Detailed)
- 包含標準報告所有內容
- 詳細的 CVE 發現列表
- 可達性分析
- 漏洞描述（需要 VPN 連接）

## 文件命名規則

```
TMflow_[版本號]_[報告類型]_[時間戳記].pdf
```

範例：
- `TMflow_2.26.1200.0_Standard_20260203_143428.pdf`
- `TMflow_2.26.1200.0_Detailed_20260203_143448.pdf`

## 注意事項

1. **FS Doc 目錄**：僅供參考，包含範例和教學文檔
2. **開發文件**：實際開發請使用根目錄下的工具
3. **時間戳記**：所有報告都會自動添加時間戳記避免混淆
4. **組織名稱**：報告中顯示為 "Techman Robot"

## 支援

如有問題，請檢查：
1. Python 環境和依賴套件
2. API Token 是否有效
3. 網路連接是否正常
4. 版本 ID 是否正確