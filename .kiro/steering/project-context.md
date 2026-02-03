# TMflow 安全報告生成器專案背景

## 專案概述
這是一個基於 Finite State 平台 API 的 TMflow 產品安全報告生成工具。專案整合了兩種報告格式：
- **fs-reporter**: 舊格式 PDF 報告生成工具
- **fs-report**: 新格式多種格式報告生成工具（HTML、CSV、XLSX）

## 重要配置信息
- **組織名稱**: "Techman Robot" (不是 "Tm-Robot")
- **API Token**: svza5d5kdulphw7kj2iba2lqyacs4nmhlwuhlykv7r33z3nxgvkq
- **子域名**: tm-robot
- **TMflow 2.26.1200 版本 ID**: 1936462473699050499

## 專案結構說明
- `FS Doc/` 資料夾：僅供參考的範例和教學文檔
- 根目錄的 `fs-reporter/` 和 `fs-report/`：實際開發使用的工具
- `reports/` 目錄：報告輸出位置
- `generate_reports.py`：自動化報告生成腳本

## 報告命名規則
所有報告必須包含時間戳記，格式：`TMflow_[版本號]_[報告類型]_[YYYYMMDD_HHMMSS].pdf`

## 開發注意事項
1. 使用 Poetry 管理 Python 依賴
2. 報告生成需要網路連接到 Finite State API
3. 詳細報告可能需要 VPN 連接才能獲取完整的漏洞描述
4. 所有敏感信息（如 API Token）應放在 config.txt 中，不要提交到 Git

## GitHub 資訊
- 使用者名稱: kenshu528-oss
- 建議的 repository 名稱: tmflow-security-report-generator