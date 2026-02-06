# TMflow Security Report Generator - 專案結構說明

## 📁 專案目錄結構

```
TMflow-security-report-generator/
├── 📂 .git/                          # Git 版本控制
├── 📂 .github/                       # GitHub 配置
├── 📂 .kiro/                         # Kiro IDE 配置
│   └── 📂 steering/                  # 開發指導原則
│       ├── communication-preferences.md
│       ├── development-principles.md
│       ├── testing-guidelines.md
│       ├── troubleshooting-guidelines.md
│       └── version-workflow.md
├── 📂 FS Doc/                        # Finite State 文檔和範例報告
├── 📂 fs-report/                     # 報告生成工具（多格式支援）
├── 📂 fs-reporter/                   # 報告生成工具（PDF 專用）
├── 📂 reports/                       # 報告輸出目錄
│
├── 📂 TMflow_Security_Report_Generator_v1.0.2.042/  # 可分享版本
├── 📂 TMflow_Security_Report_Generator_v1.0.2.043/  # 自動連線版本
├── 📂 TMflow_Security_Report_Generator_v1.0.2.044/  # 最新版本（狀態修正）
│
├── 📄 ui_modular.py                  # 主程式（模組化架構）
├── 📄 test_modules.py                # 模組化測試工具
│
├── 📄 build_modular.py               # 通用模組化建置腳本
├── 📄 build_v1.0.2.042_shareable.py  # v1.0.2.042 建置腳本
├── 📄 build_v1.0.2.043_auto_connect.py  # v1.0.2.043 建置腳本
├── 📄 build_v1.0.2.044_status_fix.py    # v1.0.2.044 建置腳本
├── 📄 TMflow_Security_Report_Generator_v1.0.2.044.spec  # PyInstaller 規格檔
│
├── 📄 config.txt                     # 配置檔案（包含 API 憑證）
├── 📄 config.example.txt             # 配置範本
├── 📄 requirements.txt               # Python 依賴套件
│
├── 📄 CHANGELOG.md                   # 更新日誌
├── 📄 README.md                      # 專案說明
├── 📄 LICENSE                        # 授權條款
├── 📄 PROJECT_SPECIFICATION.md       # 專案規格
├── 📄 CONFIG_GUIDE.md                # 配置指南
├── 📄 USAGE_GUIDE.md                 # 使用指南
├── 📄 UI_SPECIFICATION.md            # UI 設計規格
├── 📄 UI_ISSUES_LOG.md               # UI 問題記錄
│
├── 📄 cleanup_project.py             # 專案清理腳本
└── 📄 .gitignore                     # Git 忽略規則
```

## 📋 核心檔案說明

### 主程式
- **ui_modular.py**: 當前使用的主程式，採用模組化架構設計
  - APIManager: API 連接管理
  - ReportGenerator: 報告生成管理
  - ConfigManager: 配置檔案管理
  - ModularTMflowReportGeneratorUI: 主 UI 介面

### 建置腳本
- **build_modular.py**: 通用模組化建置腳本
- **build_v1.0.2.042_shareable.py**: 可分享版本建置腳本（清空預設專案清單）
- **build_v1.0.2.043_auto_connect.py**: 自動連線版本建置腳本
- **build_v1.0.2.044_status_fix.py**: 最新版本建置腳本（API 連接狀態修正）

### 測試工具
- **test_modules.py**: 模組化測試工具，可獨立測試各個功能模組

### 配置檔案
- **config.txt**: 實際使用的配置檔案（包含 API Token 等敏感資訊）
- **config.example.txt**: 配置範本，用於分享和參考

### 文檔
- **CHANGELOG.md**: 詳細的版本更新記錄
- **README.md**: 專案概述和快速開始指南
- **PROJECT_SPECIFICATION.md**: 完整的專案規格說明
- **CONFIG_GUIDE.md**: 配置檔案詳細說明
- **USAGE_GUIDE.md**: 使用者操作指南
- **UI_SPECIFICATION.md**: UI 設計規格和模組定義
- **UI_ISSUES_LOG.md**: UI 問題追蹤和解決記錄

## 📦 發布版本

### v1.0.2.042 - 可分享版本
- 清空預設專案清單
- 適合分享給同事使用
- 包含完整的報告生成功能

### v1.0.2.043 - 自動連線優化版
- 啟動時自動測試 API 連接
- 簡化日誌訊息
- 改善使用者體驗

### v1.0.2.044 - API 連接狀態修正版（最新）
- 修正 API 連接狀態顯示邏輯
- 完善按鈕文字和狀態同步
- 實現正確的斷線功能
- 執行檔大小：51.3 MB

## 🛠️ 工具資料夾

### fs-reporter/
- Finite State 官方報告生成工具
- 支援 PDF 格式報告
- 包含完整的報告模板和樣式

### fs-report/
- 多格式報告生成工具
- 支援 HTML、CSV、XLSX 等格式
- 提供更多自訂選項

### FS Doc/
- Finite State 平台文檔
- 範例報告和參考資料
- API 規格說明

## 🔧 開發指導原則

位於 `.kiro/steering/` 目錄：

1. **communication-preferences.md**: 溝通偏好和語言規範
2. **development-principles.md**: 開發原則和代碼風格
3. **testing-guidelines.md**: 測試策略和檢查清單
4. **troubleshooting-guidelines.md**: 問題排除指南
5. **version-workflow.md**: 版本管理工作流程

## 📊 清理統計

最近一次清理（2026-02-05）：
- 刪除項目數：63
- 釋放空間：1368.6 MB
- 刪除內容：
  - 17 個舊版本資料夾
  - 7 個舊版本建置腳本
  - 12 個測試檔案
  - 2 個測試 PDF
  - 4 個舊版本 UI 檔案
  - 8 個舊版本 spec 檔案
  - 6 個舊版本說明文件
  - 4 個舊版本工具腳本
  - 3 個建置資料夾

## 🎯 版本策略

- **保留最新 3 個版本**：v1.0.2.042, v1.0.2.043, v1.0.2.044
- **定期清理**：刪除舊版本和測試檔案
- **版本命名**：使用 `v1.0.2.XXX` 格式
- **進版原則**：每次修改都必須進版

## 📝 維護建議

1. **定期清理**：每 5-10 個版本執行一次清理
2. **保留重要版本**：穩定版本和里程碑版本
3. **文檔更新**：每次進版都要更新 CHANGELOG.md
4. **測試驗證**：清理前確保最新版本功能正常

---

**最後更新**: 2026-02-05  
**當前版本**: v1.0.2.044  
**專案狀態**: 穩定運行
