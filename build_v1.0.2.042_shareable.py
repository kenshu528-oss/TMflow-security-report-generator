#!/usr/bin/env python3
"""
TMflow Security Report Generator v1.0.2.042 可分享版本建置腳本
清空預設專案資料，提供乾淨版本供同事使用
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_shareable_exe():
    """建立可分享版本執行檔"""
    print("=== TMflow Security Report Generator v1.0.2.042 可分享版本建置 ===")
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
    print("正在建立可分享版本執行檔...")
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "TMflow_Security_Report_Generator_v1.0.2.042",
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
            print("✅ 可分享版本執行檔建立成功！")
        else:
            print(f"❌ 建立失敗:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ 建立執行檔失敗: {e}")
        return False
    
    # 創建發布包
    print("正在創建可分享版本發布包...")
    dist_dir = Path("TMflow_Security_Report_Generator_v1.0.2.042")
    
    # 如果目錄存在，先清理
    if dist_dir.exists():
        try:
            shutil.rmtree(dist_dir)
        except PermissionError:
            import time
            timestamp = int(time.time())
            dist_dir = Path(f"TMflow_Security_Report_Generator_v1.0.2.042_{timestamp}")
            print(f"⚠️ 原目錄被佔用，使用新目錄: {dist_dir.name}")
    
    dist_dir.mkdir()
    
    # 複製執行檔
    exe_path = Path("dist/TMflow_Security_Report_Generator_v1.0.2.042.exe")
    if exe_path.exists():
        shutil.copy2(exe_path, dist_dir / "TMflow_Security_Report_Generator_v1.0.2.042.exe")
        print("✅ 可分享版本執行檔已複製")
    else:
        print("❌ 找不到可分享版本執行檔")
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
    
    # 創建可分享版本使用說明
    usage_content = """# TMflow Security Report Generator v1.0.2.042 可分享版本使用說明

## 版本特色
- ✅ 乾淨的專案清單（無預設資料）
- ✅ 完整的報告生成功能
- ✅ 無彈出視窗問題
- ✅ 同事友好的分享版本

## 使用步驟
1. **啟動應用程式**: 執行 TMflow_Security_Report_Generator_v1.0.2.042.exe
2. **載入專案資料**: 點擊左上角的「🔄 Refresh」按鈕
3. **等待載入完成**: 系統會從 API 載入所有可用的專案和版本
4. **選擇版本**: 勾選要生成報告的版本（建議選擇 TMflow 2.26.1200.0）
5. **設定報告類型**: 選擇 Standard Report 和/或 Detailed Report
6. **生成報告**: 點擊「Generate Reports」按鈕
7. **等待完成**: 報告會儲存在 reports 目錄中

## 首次使用指引
- **空專案清單**: 這是正常的，表示這是乾淨的分享版本
- **點擊 Refresh**: 這會從 Finite State API 載入實際的專案資料
- **API 連接**: 已預設配置，通常無需修改
- **輸出目錄**: 預設為 reports 資料夾

## 報告生成說明
- **版本選擇**: 勾選 1 個版本會生成 2 份報告（Standard + Detailed）
- **檔案命名**: 自動包含版本號和時間戳記
- **儲存位置**: reports 目錄中
- **生成時間**: 每個報告約需 30-60 秒

## 技術說明
- **有效版本 ID**: 使用已驗證的版本 ID 確保報告生成成功
- **直接整合架構**: 無彈出視窗，穩定可靠
- **API 整合**: 動態載入最新的專案和版本資料
- **錯誤處理**: 完善的錯誤提示和日誌記錄

## 常見問題
**Q: 為什麼專案清單是空的？**
A: 這是可分享版本的特色，點擊 Refresh 按鈕即可載入資料。

**Q: API 連接燈號是紅色的？**
A: 這不影響報告生成功能，系統使用直接整合架構。

**Q: 如何選擇要生成的版本？**
A: 點擊版本列表中的勾選框，選中的版本會顯示 ☑ 符號。

**Q: 報告生成失敗怎麼辦？**
A: 檢查日誌區域的錯誤訊息，通常重試即可解決。

## 版本歷程
- **v1.0.2.042**: 可分享版本，清空預設專案資料
- **v1.0.2.041**: 版本 ID 修正版，確保報告生成成功
- **v1.0.2.040**: 執行檔依賴完整修正版
- **v1.0.2.037**: 激進重構，直接整合架構

---
**維護者**: kenshu528-oss  
**專案**: https://github.com/kenshu528-oss/TMflow-security-report-generator
"""
    
    with open(dist_dir / "使用說明_v1.0.2.042_可分享版本.txt", "w", encoding="utf-8") as f:
        f.write(usage_content)
    print("✅ 已創建可分享版本使用說明")
    
    print()
    print("🎉 v1.0.2.042 可分享版本建置完成！")
    print(f"📁 發布包位置: {dist_dir.absolute()}")
    print()
    print("🎯 可分享版本特色:")
    print("- 清空預設專案資料，提供乾淨的分享版本")
    print("- 保持完整的報告生成功能")
    print("- 同事友好，無開發者測試資料")
    print("- 完整的使用說明和操作指引")
    print()
    print("📋 分享說明:")
    print("- 適合分享給同事和其他開發者使用")
    print("- 啟動後點擊 Refresh 即可載入專案資料")
    print("- 包含完整的 API 配置，可直接使用")
    print("- 所有功能與 v1.0.2.041 完全相同")
    
    return True

if __name__ == "__main__":
    build_shareable_exe()