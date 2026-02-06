# 配置檔案說明 - TMflow Security Report Generator v1.0.2.020

## 配置檔案概述

TMflow Security Report Generator 使用 `config.txt` 檔案來儲存所有設定，包括 API 連接資訊、報告設定、UI 偏好和專案資料。

## 配置檔案結構

### 1. Finite State API 連接配置
```ini
API_TOKEN=your_api_token_here          # 您的 Finite State API Token
SUBDOMAIN=your_subdomain_here          # 您的組織子域名
ORGANIZATION=Your Organization Name    # 您的組織名稱
API_TIMEOUT=30                        # API 請求逾時時間（秒）
API_RETRY_COUNT=3                     # API 請求重試次數
```

### 2. 報告生成設定
```ini
OUTPUT_PATH=reports                   # 報告輸出路徑
STANDARD_REPORT=True                  # 是否生成標準報告
DETAILED_REPORT=True                  # 是否生成詳細報告
REPORT_NAME_FORMAT={project_name}_{version}_{report_type}_{timestamp}
TIMESTAMP_FORMAT=%Y%m%d_%H%M%S        # 時間戳記格式
```

### 3. UI 設定
```ini
WINDOW_WIDTH=900                      # 視窗寬度
WINDOW_HEIGHT=550                     # 視窗高度
THEME=dark                           # 主題（dark/light）
AUTO_SAVE_CONFIG=True                # 自動儲存配置
LOG_MAX_LINES=1000                   # 日誌最大行數
```

### 4. 專案資料（自動管理）
```ini
PROJECTS_DATA={}                     # 專案資料快取
SELECTED_VERSIONS=[]                 # 已選擇的版本
LAST_REFRESH_TIME=                   # 最後更新時間
CACHE_EXPIRY_HOURS=24               # 快取過期時間（小時）
```

### 5. 進階設定
```ini
DEBUG_MODE=False                     # 除錯模式
VERBOSE_LOGGING=False                # 詳細日誌
BACKUP_CONFIG=True                   # 備份配置檔案
```

## 設定步驟

### 初次設定
1. 複製 `config.example.txt` 為 `config.txt`
2. 編輯 `config.txt`，填入您的 API 資訊：
   - `API_TOKEN`: 從 Finite State 平台取得的 API Token
   - `SUBDOMAIN`: 您的組織子域名（例如：tm-robot）
   - `ORGANIZATION`: 您的組織名稱（例如：Techman Robot）

### 自動配置
程式會自動：
- 載入配置檔案
- 驗證 API 連接
- 快取專案資料
- 儲存使用者選擇

## 配置檔案位置

- **開發環境**: 與程式檔案同目錄的 `config.txt`
- **執行檔環境**: 與 `.exe` 檔案同目錄的 `config.txt`

## 安全注意事項

⚠️ **重要**: `config.txt` 包含敏感的 API Token 資訊
- 請勿將 `config.txt` 提交到版本控制系統
- 請妥善保管您的 API Token
- 建議定期更換 API Token

## 故障排除

### 配置載入失敗
- 檢查 `config.txt` 是否存在
- 檢查檔案格式是否正確
- 檢查檔案權限

### API 連接失敗
- 驗證 `API_TOKEN` 是否正確
- 驗證 `SUBDOMAIN` 是否正確
- 檢查網路連接

### 專案資料問題
- 刪除 `PROJECTS_DATA` 行，讓程式重新載入
- 檢查 API Token 權限
- 確認組織有可存取的專案

## 配置備份

程式會自動建立配置備份：
- `config.txt.backup` - 最近一次的備份
- 建議手動備份重要配置

## 版本相容性

- **v1.0.2.020**: 新增進階配置選項
- **v1.0.2.019**: 基本配置支援
- **向下相容**: 舊版配置檔案會自動升級

---

如有問題，請參考 `USAGE_GUIDE.md` 或聯繫技術支援。