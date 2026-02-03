# TMflow Security Report Generator v1.0.2

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

這是 Techman Robot TMflow 產品的安全報告生成工具，基於 Finite State 平台 API 自動生成專業的安全分析報告。

## 功能特色

- 🔒 **安全分析**: 全面的韌體安全漏洞分析
- 📊 **多種格式**: 支援 PDF、HTML、CSV、XLSX 格式
- 🤖 **自動化**: 一鍵生成標準和詳細報告
- ⏰ **時間戳記**: 自動添加時間戳避免文件混淆
- 🏢 **企業級**: 專業報告格式適合企業使用

## 目錄結構

```
FS ReportGenerator_v1.0.2/
├── fs-reporter/          # PDF 報告生成工具（舊格式）
├── fs-report/           # HTML/CSV/XLSX 報告生成工具（新格式）
├── reports/             # 生成的報告輸出目錄
├── FS Doc/              # 範例和教學文檔（參考用）
├── config.txt           # 配置文件
├── generate_reports.py  # 自動報告生成腳本
└── README.md           # 本文件
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

### 3. 生成報告

#### 方法一：使用自動腳本（推薦）
```bash
python generate_reports.py
```

#### 方法二：手動生成單個報告
```bash
# 標準報告
python fs-reporter/main.py -t [TOKEN] -s [SUBDOMAIN] -pvi [VERSION_ID] -n "Your Organization" -o "reports/report_name.pdf"

# 詳細報告
python fs-reporter/main.py -t [TOKEN] -s [SUBDOMAIN] -pvi [VERSION_ID] -n "Your Organization" -d -o "reports/report_name.pdf"
```

## 配置說明

編輯 `config.txt` 文件（從 `config.example.txt` 複製）：

```txt
TOKEN = "your-finite-state-api-token"
SUBDOMAIN = "your-subdomain"
ORGANIZATION = "Your Organization Name"
VERSION_2_26_1200 = "your-version-id"
```

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