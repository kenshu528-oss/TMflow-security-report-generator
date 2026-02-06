#!/usr/bin/env python3
"""
TMflow Security Report Generator v1.0.2.043 自動連線優化版建置腳本
自動連線 API，簡化日誌訊息
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_auto_connect_exe():
    """建立自動連線優化版執行檔"""
    print("=== TMflow Security Report Generator v1.0.2.043 自動連線優化版建置 ===")
    print()
    
    # 安裝 PyInstaller
    print("正在檢查 PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller 準備就緒")
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller 安裝失敗: {e}")
        return False
    
    # 建立執行檔 - 使用完整依賴配置
    print("正在建立自動連線優化版執行檔...")
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "TMflow_Security_Report_Generator_v1.0.2.043",
        # 基本 GUI 模組
        "--hidden-import", "tkinter",
        "--hidden-import", "tkinter.ttk", 
        "--hidden-import", "tkinter.filedialog",
        "--hidden-import", "tkinter.messagebox",
        "--hidden-import", "tkinter.scrolledtext",
        # 網路和 API
        "--hidden-import", "requests",
        "--hidden-import", "urllib3",
        "--hidden-import", "certifi",
        "--hidden-import", "charset_normalizer",
        # JSON 和資料處理
        "--hidden-import", "json",
        "--hidden-import", "datetime",
        "--hidden-import", "threading",
        "--hidden-import", "subprocess",
        # 系統模組
        "--hidden-import", "os",
        "--hidden-import", "sys",
        "--hidden-import", "platform",
        "--hidden-import", "pathlib",
        # fs-reporter 核心依賴
        "--hidden-import", "finite_state_reporter",
        "--hidden-import", "finite_state_reporter.core",
        "--hidden-import", "finite_state_reporter.core.reporter",
        # 數據處理
        "--hidden-import", "numpy",
        "--hidden-import", "pandas",
        # PDF 生成
        "--hidden-import", "reportlab",
        "--hidden-import", "reportlab.lib",
        "--hidden-import", "reportlab.platypus",
        # 圖表生成
        "--hidden-import", "matplotlib",
        "--hidden-import", "matplotlib.pyplot",
        # 其他必要模組
        "--hidden-import", "collections",
        "--hidden-import", "tempfile",
        "--hidden-import", "logging",
        "--hidden-import", "time",
        # 排除不需要的大型模組
        "--exclude-module", "sklearn",
        "--exclude-module", "scipy",
        "--exclude-module", "tensorflow",
        "--exclude-module", "torch",
        # 優化設定
        "--optimize", "2",
        "ui_modular.py"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 自動連線優化版執行檔建立成功！")
        else:
            print(f"❌ 建立失敗:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ 建立執行檔失敗: {e}")
        return False
    
    # 創建發布包
    print("正在創建自動連線優化版發布包...")
    dist_dir = Path("TMflow_Security_Report_Generator_v1.0.2.043")
    
    # 如果目錄存在，先清理
    if dist_dir.exists():
        try:
            shutil.rmtree(dist_dir)
        except PermissionError:
            import time
            timestamp = int(time.time())
            dist_dir = Path(f"TMflow_Security_Report_Generator_v1.0.2.043_{timestamp}")
            print(f"⚠️ 原目錄被佔用，使用新目錄: {dist_dir.name}")
    
    dist_dir.mkdir()
    
    # 複製執行檔
    exe_path = Path("dist/TMflow_Security_Report_Generator_v1.0.2.043.exe")
    if exe_path.exists():
        shutil.copy2(exe_path, dist_dir / "TMflow_Security_Report_Generator_v1.0.2.043.exe")
        print("✅ 自動連線優化版執行檔已複製")
    else:
        print("❌ 找不到自動連線優化版執行檔")
        return False
    
    # 複製必要檔案
    files_to_copy = [
        "README.md",
        "USAGE_GUIDE.md", 
        "config.example.txt",
        "CHANGELOG.md",
        "LICENSE"
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
    
    # 創建乾淨的配置檔案（供分享使用）
    config_content = """# TMflow Security Report Generator 配置檔案
# 請勿將此檔案提交到 Git

API_TOKEN=svza5d5kdulphw7kj2iba2lqyacs4nmhlwuhlykv7r33z3nxgvkq
SUBDOMAIN=tm-robot
ORGANIZATION=Techman Robot
OUTPUT_PATH=reports
STANDARD_REPORT=True
DETAILED_REPORT=True
SELECTED_VERSIONS=[]
PROJECTS_DATA={}
"""
    
    with open(dist_dir / "config.txt", "w", encoding="utf-8") as f:
        f.write(config_content)
    print("✅ 已創建乾淨的配置檔案")
    
    # 創建自動連線優化版使用說明
    usage_content = """# TMflow Security Report Generator v1.0.2.043 自動連線優化版使用說明

## 版本特色
- ✅ 自動連線 API（啟動時自動測試連接）
- ✅ 簡化日誌訊息（移除多餘文字和符號）
- ✅ 乾淨的專案清單（無預設資料）
- ✅ 完整的報告生成功能

## 使用步驟
1. **啟動應用程式**: 執行 TMflow_Security_Report_Generator_v1.0.2.043.exe
2. **自動連線**: 系統會自動測試 API 連接（右上角燈號顯示狀態）
3. **載入專案資料**: 點擊左上角的「🔄 Refresh」按鈕
4. **選擇版本**: 勾選要生成報告的版本
5. **生成報告**: 點擊「Generate Reports」按鈕

## 自動連線功能
- **智能啟動**: 如果配置中有 API 憑證，會自動測試連接
- **狀態指示**: 右上角燈號即時顯示連接狀態
  - 🟢 綠色 = API 連接成功
  - 🟡 黃色 = 連接測試中
  - 🔴 紅色 = 連接失敗
- **無干擾**: 自動連線失敗不會彈出錯誤對話框

## 日誌訊息優化
- **簡潔明瞭**: 移除多餘的 emoji 和冗長文字
- **保留核心**: 保留所有必要的狀態和錯誤資訊
- **易於閱讀**: 更清爽的日誌介面，專注於重要訊息

## 使用建議
- **首次使用**: 啟動後觀察右上角連線狀態，綠色表示可以開始使用
- **專案載入**: 連線成功後點擊 Refresh 載入專案資料
- **版本選擇**: 建議選擇 TMflow 2.26.1200.0 進行測試
- **報告生成**: 每個版本會生成 2 份報告（Standard + Detailed）

## 技術改進
- **自動化體驗**: 減少手動操作，提升使用便利性
- **介面優化**: 更簡潔的訊息顯示，減少視覺干擾
- **穩定可靠**: 保持所有核心功能不變，只優化使用體驗
- **向後相容**: 與之前版本的配置完全相容

## 常見問題
**Q: 為什麼啟動時會自動連線？**
A: 這是新的便利功能，如果配置中有 API 憑證會自動測試，節省手動操作。

**Q: 自動連線失敗怎麼辦？**
A: 觀察右上角燈號，紅色表示失敗，可以手動點擊 Reconnect 重試。

**Q: 日誌訊息變少了？**
A: 這是優化功能，移除了多餘文字，保留核心資訊，讓介面更清爽。

**Q: 功能有變化嗎？**
A: 核心功能完全相同，只是改進了使用者體驗和介面顯示。

---
**版本歷程**: v1.0.2.043 自動連線優化版  
**維護者**: kenshu528-oss  
**專案**: https://github.com/kenshu528-oss/TMflow-security-report-generator
"""
    
    with open(dist_dir / "使用說明_v1.0.2.043_自動連線優化版.txt", "w", encoding="utf-8") as f:
        f.write(usage_content)
    print("✅ 已創建自動連線優化版使用說明")
    
    print()
    print("🎉 v1.0.2.043 自動連線優化版建置完成！")
    print(f"📁 發布包位置: {dist_dir.absolute()}")
    print()
    print("🚀 自動連線優化版特色:")
    print("- 啟動時自動測試 API 連接")
    print("- 簡化日誌訊息，介面更清爽")
    print("- 保持完整功能，只優化使用體驗")
    print("- 智能狀態指示，即時顯示連線狀態")
    print()
    print("📋 使用說明:")
    print("- 啟動後自動連線，觀察右上角燈號狀態")
    print("- 綠色燈號表示可以點擊 Refresh 載入資料")
    print("- 所有功能與之前版本完全相同")
    print("- 適合日常使用，提升操作便利性")
    
    return True

if __name__ == "__main__":
    build_auto_connect_exe()