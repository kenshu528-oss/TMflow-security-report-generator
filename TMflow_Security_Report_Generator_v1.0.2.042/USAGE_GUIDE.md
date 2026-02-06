# TMflow Security Report Generator 使用指南

## 快速開始

### 1. 啟動應用程式
```bash
python ui_modern.py
```

### 2. 配置 API 連接
- **API Token**: 已預設為專案 Token
- **Subdomain**: tm-robot
- **Organization**: Techman Robot
- 點擊 "Reconnect" 按鈕驗證連接

### 3. 選擇要生成報告的版本
- 在左側 "Select Projects & Versions" 區域
- 點擊版本前的 ☐ 切換為 ☑ 來選擇版本
- 可使用 "Select All" 或 "Clear All" 批量操作

### 4. 設定報告選項
- **Standard Report**: 標準報告
- **Detailed Report**: 詳細報告
- **Output**: 設定報告輸出路徑
- 檔名會自動包含時間戳記

### 5. 生成報告
- 點擊 "Generate Reports" 按鈕
- 觀察進度條和日誌訊息
- 報告完成後會顯示成功訊息

## 功能特色

### 🎯 主要功能
- **批量生成**: 支援同時生成多個版本的報告
- **雙格式支援**: Standard 和 Detailed 兩種報告格式
- **即時進度**: 進度條和詳細日誌顯示
- **配置管理**: 自動載入和儲存配置

### 🔧 技術特點
- **深色主題**: 現代化的深色介面設計
- **響應式佈局**: 支援視窗大小調整
- **錯誤處理**: 完善的錯誤提示和處理
- **背景處理**: 報告生成不會阻塞 UI

### 📁 檔案結構
```
TMflow-security-report-generator/
├── ui_modern.py          # 主要 UI 程式
├── generate_reports.py   # 命令列報告生成工具
├── config.txt           # 配置檔案 (不提交到 Git)
├── config.example.txt   # 配置檔案範例
├── reports/             # 報告輸出目錄
├── fs-reporter/         # 舊格式報告生成工具
├── fs-report/           # 新格式報告生成工具
└── README.md           # 專案說明

```

## 報告命名規則

生成的報告檔案會按照以下格式命名：
```
TMflow_[版本號]_[報告類型]_[YYYYMMDD_HHMMSS].pdf
```

範例：
- `TMflow_2.26.1200.0_Standard_20260203_143428.pdf`
- `TMflow_2.26.1200.0_Detailed_20260203_143448.pdf`

## 故障排除

### 常見問題

**Q: 報告生成失敗怎麼辦？**
A: 
1. 檢查網路連接
2. 確認 API Token 是否正確
3. 查看日誌區域的錯誤訊息
4. 嘗試點擊 "Reconnect" 重新連接

**Q: 找不到 fs-reporter 工具？**
A: 確保 `fs-reporter/main.py` 檔案存在於專案根目錄

**Q: 詳細報告生成失敗？**
A: 詳細報告可能需要 VPN 連接才能獲取完整的漏洞描述

**Q: 配置沒有儲存？**
A: 點擊 "Reconnect" 按鈕會自動儲存當前配置到 `config.txt`

### 日誌訊息說明

- ✅ 綠色勾號：操作成功
- ❌ 紅色叉號：操作失敗
- ⚠️ 警告符號：需要注意的訊息
- 🎉 慶祝符號：所有操作完成

## 進階使用

### 命令列模式
如果需要自動化或批次處理，可以使用命令列工具：
```bash
python generate_reports.py
```

### 自訂配置
編輯 `config.txt` 檔案來自訂預設設定：
```
API_TOKEN=your_token_here
SUBDOMAIN=your_subdomain
ORGANIZATION=Your Organization
OUTPUT_PATH=custom_output_path
```

### 版本管理
在 `ui_modern.py` 中的 `projects_data` 可以添加新的專案版本：
```python
"TMflow": [
    {"version": "新版本號", "project_id": "專案ID", "version_id": "版本ID", "selected": tk.BooleanVar()},
]
```

## 支援與回饋

如有問題或建議，請在 GitHub 專案頁面提出 Issue：
https://github.com/kenshu528-oss/TMflow-security-report-generator

---
**版本**: v1.0.2.002  
**最後更新**: 2026-02-03