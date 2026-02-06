#!/usr/bin/env python3
"""
TMflow Security Report Generator 模組化版本打包腳本 v1.0.2.039
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_modular_exe():
    """建立模組化版本的執行檔"""
    print("=== TMflow Security Report Generator 模組化版本打包 ===")
    print()
    
    # 安裝 PyInstaller
    print("正在安裝 PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller 安裝成功")
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller 安裝失敗: {e}")
        return False
    
    # 建立執行檔 - 激進重構版本，包含完整 fs-reporter 依賴
    print("正在建立激進重構執行檔...")
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "TMflow_Security_Report_Generator_Modular",
        # 基本模組
        "--hidden-import", "tkinter",
        "--hidden-import", "tkinter.ttk", 
        "--hidden-import", "tkinter.filedialog",
        "--hidden-import", "tkinter.messagebox",
        "--hidden-import", "tkinter.scrolledtext",
        "--hidden-import", "requests",
        "--hidden-import", "subprocess",
        "--hidden-import", "json",
        "--hidden-import", "threading",
        # fs-reporter 核心依賴 - 激進重構必需
        "--hidden-import", "finite_state_reporter",
        "--hidden-import", "finite_state_reporter.core",
        "--hidden-import", "finite_state_reporter.core.reporter",
        "--hidden-import", "finite_state_reporter.pdf",
        "--hidden-import", "finite_state_reporter.pdf.styles",
        "--hidden-import", "finite_state_reporter.pdf.colors",
        "--hidden-import", "finite_state_reporter.pdf.flowables",
        "--hidden-import", "finite_state_reporter.pdf.page_templates",
        # 報告生成依賴
        "--hidden-import", "reportlab",
        "--hidden-import", "reportlab.lib",
        "--hidden-import", "reportlab.lib.units",
        "--hidden-import", "reportlab.platypus",
        "--hidden-import", "matplotlib",
        "--hidden-import", "matplotlib.pyplot",
        # 激進重構必需的數據處理依賴
        "--hidden-import", "numpy",
        "--hidden-import", "pandas",
        "--hidden-import", "PIL",
        "--hidden-import", "PIL.Image",
        "--hidden-import", "collections",
        "--hidden-import", "tempfile",
        "--hidden-import", "logging",
        # 排除不需要的模組
        "--exclude-module", "sklearn",
        # 優化設定
        "--optimize", "2",
        "--strip",
        "ui_modular.py"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 模組化執行檔建立成功！")
        else:
            print(f"❌ 建立失敗:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ 建立執行檔失敗: {e}")
        return False
    
    # 創建發布包
    print("正在創建模組化發布包...")
    dist_dir = Path("TMflow_Security_Report_Generator_v1.0.2.039")
    
    # 如果目錄存在，嘗試刪除
    if dist_dir.exists():
        try:
            shutil.rmtree(dist_dir)
        except PermissionError:
            import time
            timestamp = int(time.time())
            dist_dir = Path(f"TMflow_Security_Report_Generator_v1.0.2.039_{timestamp}")
            print(f"⚠️ 原目錄被佔用，使用新目錄: {dist_dir.name}")
    
    dist_dir.mkdir()
    
    # 複製執行檔
    exe_path = Path("dist/TMflow_Security_Report_Generator_Modular.exe")
    if exe_path.exists():
        shutil.copy2(exe_path, dist_dir / "TMflow_Security_Report_Generator_Modular.exe")
        print("✅ 模組化執行檔已複製")
    else:
        print("❌ 找不到模組化執行檔")
        return False
    
    # 複製必要檔案
    files_to_copy = [
        "README.md",
        "USAGE_GUIDE.md", 
        "config.example.txt",
        "CHANGELOG.md",
        "LICENSE",
        "ui_modular.py",  # 包含原始碼供參考
        "test_modules.py"  # 包含測試腳本
    ]
    
    for file_name in files_to_copy:
        if Path(file_name).exists():
            shutil.copy2(file_name, dist_dir / file_name)
            print(f"✅ 已複製 {file_name}")
    
    # 複製工具目錄
    if Path("fs-reporter").exists():
        shutil.copytree("fs-reporter", dist_dir / "fs-reporter")
        print("✅ 已複製 fs-reporter")
    
    if Path("fs-report").exists():
        shutil.copytree("fs-report", dist_dir / "fs-report")
        print("✅ 已複製 fs-report")
    
    # 創建 reports 目錄
    (dist_dir / "reports").mkdir(exist_ok=True)
    print("✅ 已創建 reports 目錄")
    
    # 創建模組化版本說明
    usage_text = """# TMflow Security Report Generator v1.0.2.035 (Modular)

## 模組化架構特色

這個版本採用全新的模組化架構，將功能拆分為獨立的模組：

### 核心模組
- **APIManager**: 負責所有 Finite State API 相關操作
- **ReportGenerator**: 負責報告生成功能
- **ConfigManager**: 負責配置檔案管理
- **ModularTMflowReportGeneratorUI**: 主 UI 介面

### 優勢
- 🏗️ **模組化設計**: 每個功能模組獨立，易於維護和測試
- 🧪 **可測試性**: 每個模組都可以獨立測試
- 🔧 **易於除錯**: 問題定位更精確
- 📈 **可擴展性**: 新功能可以作為新模組添加

## 快速開始

1. 複製 config.example.txt 為 config.txt
2. 編輯 config.txt 填入您的 API 資訊：
   ```
   API_TOKEN=your_api_token_here
   SUBDOMAIN=tm-robot
   ORGANIZATION=Techman Robot
   OUTPUT_PATH=reports
   ```
3. 執行 TMflow_Security_Report_Generator_Modular.exe

## 測試功能

包含的 test_modules.py 可以用來測試各個模組：

```bash
python test_modules.py
```

這會逐一測試：
- 配置管理模組
- API 管理模組  
- 報告生成模組
- UI 組件

## 開發模式

如果您想要修改或擴展功能，可以直接運行：

```bash
python ui_modular.py
```

## 系統需求

- Windows 10 或更新版本
- 網路連接（用於 Finite State API）

## 技術架構

基於 v1.0.2.017 的穩定架構，疊加 v1.0.2.031 務實解決方案：
- 保持所有原有功能
- 使用最簡單可靠的 subprocess 方式生成報告
- 模組間低耦合，高內聚
- 統一的錯誤處理和日誌記錄

## 注意事項

- 第一次啟動可能需要較長時間
- 確保 fs-reporter 和 fs-report 資料夾在同一目錄
- 報告會輸出到 reports 資料夾
- 所有模組都經過獨立測試驗證

## 技術支援

GitHub: https://github.com/kenshu528-oss/TMflow-security-report-generator
"""
    
    with open(dist_dir / "模組化版本說明.txt", "w", encoding="utf-8") as f:
        f.write(usage_text)
    
    print("✅ 已創建模組化版本說明")
    
    print()
    print("🎉 模組化版本打包完成！")
    print(f"📁 發布包位置: {dist_dir.absolute()}")
    print()
    print("📋 測試步驟:")
    print("1. 進入發布包資料夾")
    print("2. 執行 python test_modules.py 測試各模組")
    print("3. 複製 config.example.txt 為 config.txt")
    print("4. 編輯 config.txt 填入 API 資訊")
    print("5. 執行 TMflow_Security_Report_Generator_Modular.exe")
    print()
    print("✅ 模組化架構便於問題定位和功能擴展")
    
    return True

if __name__ == "__main__":
    build_modular_exe()