#!/usr/bin/env python3
"""
TMflow Security Report Generator v1.0.2.044 建置腳本
API 連接狀態顯示修正版
"""

import os
import shutil
import subprocess
import sys
from datetime import datetime

def main():
    print("🚀 開始建置 TMflow Security Report Generator v1.0.2.044")
    print("📋 版本特色：API 連接狀態顯示修正版")
    
    # 版本資訊
    version = "v1.0.2.044"
    folder_name = f"TMflow_Security_Report_Generator_{version}"
    
    try:
        # 1. 建立版本資料夾
        print(f"\n📁 建立版本資料夾: {folder_name}")
        if os.path.exists(folder_name):
            shutil.rmtree(folder_name)
        os.makedirs(folder_name)
        
        # 2. 複製必要檔案
        print("📋 複製必要檔案...")
        files_to_copy = [
            "ui_modular.py",
            "config.example.txt", 
            "config.txt",
            "LICENSE",
            "README.md",
            "USAGE_GUIDE.md",
            "CHANGELOG.md"
        ]
        
        for file in files_to_copy:
            if os.path.exists(file):
                shutil.copy2(file, folder_name)
                print(f"  ✅ {file}")
            else:
                print(f"  ⚠️ {file} 不存在，跳過")
        
        # 3. 複製工具資料夾
        print("📁 複製工具資料夾...")
        folders_to_copy = ["fs-reporter", "fs-report"]
        
        for folder in folders_to_copy:
            if os.path.exists(folder):
                dest_folder = os.path.join(folder_name, folder)
                shutil.copytree(folder, dest_folder)
                print(f"  ✅ {folder}")
            else:
                print(f"  ⚠️ {folder} 不存在，跳過")
        
        # 4. 建立 reports 資料夾
        reports_folder = os.path.join(folder_name, "reports")
        os.makedirs(reports_folder, exist_ok=True)
        print(f"  ✅ reports 資料夾已建立")
        
        # 5. 使用 PyInstaller 建立執行檔
        print("\n🔨 使用 PyInstaller 建立執行檔...")
        
        pyinstaller_cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--name", f"TMflow_Security_Report_Generator_{version}",
            "--distpath", folder_name,
            "--workpath", "build",
            "--specpath", ".",
            
            # 包含必要的隱藏導入
            "--hidden-import", "finite_state_reporter",
            "--hidden-import", "finite_state_reporter.core",
            "--hidden-import", "finite_state_reporter.core.reporter",
            "--hidden-import", "requests",
            "--hidden-import", "json",
            "--hidden-import", "datetime",
            "--hidden-import", "os",
            "--hidden-import", "sys",
            "--hidden-import", "threading",
            "--hidden-import", "tkinter",
            "--hidden-import", "tkinter.ttk",
            "--hidden-import", "tkinter.filedialog",
            "--hidden-import", "tkinter.messagebox",
            "--hidden-import", "tkinter.scrolledtext",
            
            # 報告生成相關依賴
            "--hidden-import", "reportlab",
            "--hidden-import", "reportlab.pdfgen",
            "--hidden-import", "reportlab.pdfgen.canvas",
            "--hidden-import", "matplotlib",
            "--hidden-import", "matplotlib.pyplot",
            "--hidden-import", "numpy",
            "--hidden-import", "pandas",
            
            # 系統模組
            "--hidden-import", "subprocess",
            "--hidden-import", "tempfile",
            "--hidden-import", "logging",
            "--hidden-import", "collections",
            "--hidden-import", "PIL",
            "--hidden-import", "PIL.Image",
            
            # 排除不需要的大型模組
            "--exclude-module", "sklearn",
            "--exclude-module", "scipy",
            "--exclude-module", "tensorflow",
            "--exclude-module", "torch",
            
            # 優化選項
            "--optimize", "2",
            "--strip",
            
            "ui_modular.py"
        ]
        
        print("執行 PyInstaller 命令...")
        result = subprocess.run(pyinstaller_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ PyInstaller 建置成功")
        else:
            print("❌ PyInstaller 建置失敗")
            print("錯誤輸出:", result.stderr)
            return False
        
        # 6. 建立使用說明檔案
        print("\n📝 建立使用說明檔案...")
        usage_content = f"""# TMflow Security Report Generator {version}

## 版本特色 - API 連接狀態顯示修正版

### 🔧 主要修正
- **修正 API 連接狀態顯示**: 解決連接成功時狀態文字和按鈕顯示問題
- **狀態同步**: 確保狀態指示器、文字標籤、按鈕文字完全同步
- **按鈕邏輯**: 連接成功時顯示 "Connected" 和 "Disconnect" 按鈕
- **斷線功能**: 正確實現手動斷開連接功能

### ✅ 繼承功能
- **自動連線**: 啟動時自動測試 API 連接
- **簡化日誌**: 保持簡潔的日誌訊息
- **清空專案清單**: 預設空清單，適合分享使用
- **完整報告生成**: 所有報告生成功能正常

### 🎯 使用流程
1. **啟動應用程式** → 自動測試 API 連接
2. **查看連線狀態** → 右上角顯示連接狀態和對應按鈕
3. **點擊 Refresh** → 載入專案資料
4. **選擇版本** → 勾選要生成報告的版本
5. **生成報告** → 點擊 Generate Reports 開始生成

### 🔗 API 連接狀態說明
- **紅色圓點 + "Disconnected" + "Reconnect"**: 未連接或連接失敗
- **黃色圓點**: 連接測試中
- **綠色圓點 + "Connected" + "Disconnect"**: 連接成功

### ⚠️ 重要說明
- 此版本修正了 v1.0.2.043 中的狀態顯示問題
- 所有核心功能保持不變
- 向後相容所有配置和操作

## 系統需求
- Windows 10/11
- 網路連接（用於 API 通訊）

## 使用方法
1. 執行 TMflow_Security_Report_Generator_{version}.exe
2. 確認 API 連接狀態（右上角）
3. 點擊 Refresh 載入專案資料
4. 選擇要生成報告的版本
5. 點擊 Generate Reports 開始生成

## 檔案說明
- TMflow_Security_Report_Generator_{version}.exe: 主程式執行檔
- fs-reporter/: 報告生成工具
- fs-report/: 報告模板工具  
- config.txt: 配置檔案
- reports/: 報告輸出目錄

## 技術支援
如有問題請參考 CHANGELOG.md 或聯繫開發團隊。

---
建置時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
版本: {version}
"""
        
        with open(os.path.join(folder_name, f"使用說明_{version}.txt"), "w", encoding="utf-8") as f:
            f.write(usage_content)
        
        # 7. 顯示建置結果
        print(f"\n🎉 建置完成！")
        print(f"📁 版本資料夾: {folder_name}")
        
        # 檢查執行檔大小
        exe_path = os.path.join(folder_name, f"TMflow_Security_Report_Generator_{version}.exe")
        if os.path.exists(exe_path):
            exe_size = os.path.getsize(exe_path)
            exe_size_mb = exe_size / (1024 * 1024)
            print(f"📊 執行檔大小: {exe_size_mb:.1f} MB")
        
        print(f"✅ {version} 建置成功！")
        return True
        
    except Exception as e:
        print(f"❌ 建置過程發生錯誤: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🚀 建置完成，可以進行測試和發布！")
    else:
        print("\n❌ 建置失敗，請檢查錯誤訊息")
        sys.exit(1)