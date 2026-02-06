# TMflow Security Report Generator v1.0.2.009

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![Status](https://img.shields.io/badge/status-stable-success.svg)
![GUI](https://img.shields.io/badge/GUI-tkinter-orange.svg)
![Size](https://img.shields.io/badge/executable-137.7MB-blue.svg)

基於 Finite State 平台 API 的 TMflow 產品安全報告生成工具，提供現代化圖形介面和命令列兩種使用方式，支援批量生成專業的安全分析報告。

## 🚀 快速開始

### 圖形化介面 (推薦)
```bash
# 啟動現代化 GUI 應用程式
python ui_modern.py
```

### 執行檔版本
```bash
# 使用預建的執行檔 (無需 Python 環境)
./TMflow_Security_Report_Generator_v1.0.2.009/TMflow_Security_Report_Generator.exe
```

### 命令列模式
```bash
# 使用自動化腳本生成報告
python generate_reports.py
```

## 📋 功能特色

### 🎯 現代化圖形介面
- **深色主題設計**: 專業的視覺體驗，護眼舒適
- **實時 API 整合**: 直接從 Finite State 平台載入最新專案資料
- **智能專案管理**: 
  - 支援 TMflow 和 TM AI+ Trainer 兩個專案
  - 21+ 個 TMflow 版本，3 個 TM AI+ Trainer 版本
  - 版本按時間降序排列，最新版本優先顯示
- **批量報告生成**: 
  - 同時選擇多個版本進行報告生成
  - Standard 和 Detailed 兩種報告類型
  - 智能進度追蹤和狀態顯示
- **配置持久化**: 
  - 自動保存 API 配置和專案資料
  - 應用程式重啟後恢復選擇狀態
  - 智能配置驗證和錯誤處理

### 📊 專業報告格式
- **Standard Report**: 標準安全概覽報告
- **Detailed Report**: 詳細漏洞分析報告
- **自動時間戳**: 格式 `TMflow_{版本號}_{類型}_{YYYYMMDD_HHMMSS}.pdf`
- **專業 PDF 輸出**: 包含圖表、統計和詳細分析

### 🔧 技術優勢
- **混合架構**: 
  - 開發環境：直接整合 fs-reporter 核心功能
  - 執行檔環境：優化的 subprocess 調用
  - 智能環境檢測和自動切換
- **無跳出視窗**: 使用 pythonw.exe + 多重視窗隱藏技術
- **檔案大小優化**: 執行檔僅 137.7MB (相比早期版本減少 76%)
- **雙工具整合**: fs-reporter (PDF) + fs-report (多格式)
- **完整錯誤處理**: 網路異常、API 錯誤、生成失敗的完整處理

## 🏗️ 系統架構

```
TMflow Security Report Generator v1.0.2.009
├── 🖥️  GUI Layer (tkinter + 深色主題)
├── 🔄 Business Logic (API 客戶端 + 狀態管理)  
├── 📊 Report Generation (混合架構)
│   ├── fs-reporter (PDF 生成)
│   └── fs-report (多格式支援)
└── 💾 Data Layer (配置 + 快取 + 輸出)
```

## 📁 專案結構

```
TMflow-security-report-generator/
├── ui_modern.py                    # 🎨 現代化圖形介面 (主要)
├── generate_reports.py             # 🤖 命令列自動化腳本
├── build_simple.py                 # 🔧 執行檔建置腳本
├── fs-reporter/                    # 📄 PDF 報告生成工具
├── fs-report/                      # 📊 多格式報告生成工具
├── reports/                        # 📁 報告輸出目錄
├── config.txt                      # ⚙️ 配置檔案 (不提交)
├── config.example.txt              # 📋 配置檔案範例
├── TMflow_Security_Report_Generator_v1.0.2.009/  # 🚀 部署包
├── docs/                          # 📚 文檔
│   ├── USAGE_GUIDE.md             # 📖 使用指南
│   ├── PROJECT_SPECIFICATION.md   # 📋 專案規格
│   └── CHANGELOG.md               # 📝 更新日誌
└── FS Doc/                        # 📚 範例文檔（參考用）
```

## ⚡ 快速安裝

### 方式一：使用執行檔 (推薦)
1. 下載 `TMflow_Security_Report_Generator_v1.0.2.009.zip`
2. 解壓縮到任意位置
3. 編輯 `config.txt` 填入 API 資訊
4. 執行 `TMflow_Security_Report_Generator.exe`

### 方式二：從原始碼安裝
```bash
# 1. 克隆專案
git clone https://github.com/kenshu528-oss/tmflow-security-report-generator.git
cd tmflow-security-report-generator

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 配置設定
cp config.example.txt config.txt
# 編輯 config.txt 填入您的 API 資訊

# 4. 啟動應用程式
python ui_modern.py
```

## 🎯 使用方式

### 🖥️ 圖形化介面 (推薦)
```bash
python ui_modern.py
```
**特色功能**:
- 深色主題專業介面
- 實時載入 TMflow 和 TM AI+ Trainer 專案
- 批量選擇版本生成報告
- 即時進度追蹤和詳細日誌
- 自動配置保存和恢復

### 🤖 命令列模式
```bash
python generate_reports.py
```

### 🔧 手動生成報告
```bash
# 標準報告
python fs-reporter/main.py -t [TOKEN] -s [SUBDOMAIN] -pvi [VERSION_ID] -n "Techman Robot" -o "reports/report.pdf"

# 詳細報告  
python fs-reporter/main.py -t [TOKEN] -s [SUBDOMAIN] -pvi [VERSION_ID] -n "Techman Robot" -d -o "reports/report.pdf"
```

## ⚙️ 配置說明

編輯 `config.txt` 檔案：
```ini
# TMflow Security Report Generator 配置檔案
# Finite State API 配置
API_TOKEN=your_api_token_here
SUBDOMAIN=tm-robot
ORGANIZATION=Techman Robot

# 報告設定
OUTPUT_PATH=reports
STANDARD_REPORT=True
DETAILED_REPORT=True

# 系統資料 (自動管理)
SELECTED_VERSIONS=[]
PROJECTS_DATA={}
```

**重要提醒**:
- 配置檔案不會提交到 Git (已加入 .gitignore)
- GUI 會自動載入和儲存所有配置
- 支援專案資料快取和選擇狀態持久化

## 📊 支援的專案和版本

### TMflow 專案 (21+ 版本)
- **最新版本**: 3.12.1600.0, 3.12.1500.0, 2.26.1600.0, 2.26.1500.0
- **穩定版本**: 2.26.1200.0 (版本 ID: 1936462473699050499)
- **特殊版本**: Vision 系列、DNN 系列、redistributable 版本

### TM AI+ Trainer 專案 (3 版本)
- 2.26.1100.0, 2.26.1000.0, 2025-12-19

## 🚀 建置執行檔

```bash
# 建立優化的執行檔 (137.7MB)
python build_simple.py

# 生成的檔案位於
TMflow_Security_Report_Generator_v1.0.2.009/
├── TMflow_Security_Report_Generator.exe  # 主程式
├── fs-reporter/                          # PDF 工具
├── fs-report/                           # 多格式工具  
├── config.txt                           # 配置檔案
└── 使用說明.txt                          # 使用指南
```

## 📋 報告類型和格式

### Standard Report (標準報告)
- **內容**: 安全概覽、組件統計、漏洞分布
- **檔案大小**: ~400KB
- **生成時間**: 15-30 秒

### Detailed Report (詳細報告)  
- **內容**: 包含標準報告 + 詳細 CVE 清單 + 可達性分析
- **檔案大小**: ~400KB
- **生成時間**: 15-30 秒

### 檔名格式
```
TMflow_{版本號}_{報告類型}_{YYYYMMDD_HHMMSS}.pdf
```
**範例**: `TMflow_2.26.1200.0_Standard_20260204_120530.pdf`

## 🔧 技術規格

### 系統需求
- **作業系統**: Windows 10+, macOS 10.15+, Linux
- **Python**: 3.11+ (開發環境)
- **記憶體**: 最少 512MB
- **磁碟空間**: 200MB
- **網路**: 需連接 Finite State API

### 效能指標
- **啟動時間**: < 3 秒
- **API 響應**: < 10 秒  
- **報告生成**: 15-30 秒/報告
- **執行檔大小**: 137.7MB (優化後)

## 🆕 v1.0.2.009 新功能

### ✨ 主要改進
- **檔案大小優化**: 從 571MB 減少到 137.7MB (減少 76%)
- **混合架構**: 智能環境檢測 + 自動切換生成方式
- **無跳出視窗**: 完全解決執行檔環境的視窗彈出問題
- **狀態持久化**: 專案資料和選擇狀態自動保存恢復

### 🔧 技術優化
- 最小化 PyInstaller 依賴打包
- 智能路徑檢測和環境適應
- 優化的 subprocess 調用機制
- 完整的錯誤處理和恢復機制

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request！

### 開發環境設置
```bash
# 安裝開發依賴
pip install -r requirements.txt

# 代碼格式化
black .

# 建置測試
python build_simple.py
```

### 版本管理
- 每次修改必須更新版本號
- 更新 `ui_modern.py`, `build_simple.py`, `CHANGELOG.md`
- 遵循 `v1.0.2.XXX` 格式

## 📞 技術支援

- **GitHub**: https://github.com/kenshu528-oss/tmflow-security-report-generator
- **Issues**: [回報問題](https://github.com/kenshu528-oss/tmflow-security-report-generator/issues)
- **文檔**: [專案 Wiki](https://github.com/kenshu528-oss/tmflow-security-report-generator/wiki)

## 📄 授權條款

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

---

**版本**: v1.0.2.009 | **狀態**: 穩定版 | **更新**: 2026-02-04