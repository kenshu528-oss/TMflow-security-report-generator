# TMflow Security Report Generator 部署指南

## 🎯 為同仁創建執行檔

### 方法一：使用 Python 打包腳本（推薦）

```bash
# 執行打包腳本
python build_exe.py
```

### 方法二：使用批次檔（Windows）

```bash
# 執行批次檔
build_simple.bat
```

### 方法三：手動使用 PyInstaller

```bash
# 安裝 PyInstaller
pip install pyinstaller

# 建立執行檔
pyinstaller --onefile --windowed --name "TMflow_Security_Report_Generator" --add-data "fs-reporter;fs-reporter" --add-data "fs-report;fs-report" --add-data "config.example.txt;." ui_modern.py
```

## 📦 發布包內容

打包完成後會產生以下結構：

```
TMflow_Security_Report_Generator_v1.0.2.002/
├── TMflow_Security_Report_Generator.exe  # 主程式
├── fs-reporter/                          # PDF 報告工具
├── fs-report/                           # 多格式報告工具
├── reports/                             # 報告輸出目錄
├── config.example.txt                   # 配置檔案範例
├── README.md                            # 專案說明
├── USAGE_GUIDE.md                       # 使用指南
├── CHANGELOG.md                         # 更新日誌
├── LICENSE                              # 授權條款
└── 安裝說明.txt                          # 安裝說明
```

## 👥 分享給同仁

### 1. 創建 ZIP 檔案
將整個 `TMflow_Security_Report_Generator_v1.0.2.002` 資料夾壓縮成 ZIP 檔案。

### 2. 提供給同仁的說明

**安裝步驟：**
1. 解壓縮 ZIP 檔案到任意位置
2. 複製 `config.example.txt` 為 `config.txt`
3. 編輯 `config.txt` 填入 API 資訊：
   ```
   API_TOKEN=your_api_token_here
   SUBDOMAIN=tm-robot
   ORGANIZATION=Techman Robot
   OUTPUT_PATH=reports
   ```
4. 執行 `TMflow_Security_Report_Generator.exe`

**系統需求：**
- Windows 10 或更新版本
- 網路連接（用於 Finite State API）
- 不需要安裝 Python

## 🔧 故障排除

### 常見問題

**Q: 執行檔無法啟動？**
A: 
- 檢查是否有防毒軟體阻擋
- 確保所有檔案都在同一個資料夾中
- 嘗試以系統管理員身分執行

**Q: 報告生成失敗？**
A:
- 檢查 `config.txt` 中的 API Token 是否正確
- 確保有網路連接
- 檢查 `fs-reporter` 和 `fs-report` 資料夾是否完整

**Q: 執行檔很大？**
A: 
- 這是正常的，因為包含了 Python 執行環境和所有依賴
- 大小約 50-100MB 是正常範圍

### 進階配置

**自訂輸出路徑：**
同仁可以修改 `config.txt` 中的 `OUTPUT_PATH` 來改變報告輸出位置。

**網路代理設定：**
如果公司使用代理伺服器，可能需要額外的網路設定。

## 📋 檢查清單

部署前請確認：

- [ ] 執行檔能正常啟動
- [ ] API 連接測試成功
- [ ] 能夠載入專案和版本列表
- [ ] 能夠生成測試報告
- [ ] 所有必要檔案都包含在發布包中
- [ ] 提供了完整的使用說明

## 🔄 更新流程

當有新版本時：
1. 重新打包新版本
2. 更新版本號
3. 提供更新說明
4. 通知同仁下載新版本

## 📞 技術支援

- **GitHub**: https://github.com/kenshu528-oss/TMflow-security-report-generator
- **Issues**: 在 GitHub 上提交問題報告
- **文檔**: 參考 README.md 和 USAGE_GUIDE.md

---

**注意**: 請確保同仁了解 API Token 的保密性，不要在不安全的環境中使用或分享。