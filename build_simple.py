#!/usr/bin/env python3
"""
TMflow Security Report Generator 簡易打包腳本
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_simple_exe():
    """使用簡單的 PyInstaller 命令建立執行檔"""
    print("=== TMflow Security Report Generator 簡易打包 ===")
    print()
    
    # 安裝 PyInstaller
    print("正在安裝 PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller 安裝成功")
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller 安裝失敗: {e}")
        return False
    
    # 建立執行檔
    print("正在建立執行檔...")
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "TMflow_Security_Report_Generator",
        "ui_modern.py"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 執行檔建立成功！")
        else:
            print(f"❌ 建立失敗:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ 建立執行檔失敗: {e}")
        return False
    
    # 創建發布包
    print("正在創建發布包...")
    dist_dir = Path("TMflow_Security_Report_Generator_v1.0.2.003")
    
    # 如果目錄存在，嘗試刪除，如果失敗就重命名
    if dist_dir.exists():
        try:
            shutil.rmtree(dist_dir)
        except PermissionError:
            # 如果無法刪除（可能執行檔正在運行），創建新的目錄名
            import time
            timestamp = int(time.time())
            dist_dir = Path(f"TMflow_Security_Report_Generator_v1.0.2.003_{timestamp}")
            print(f"⚠️ 原目錄被佔用，使用新目錄: {dist_dir.name}")
    
    dist_dir.mkdir()
    
    # 複製執行檔
    exe_path = Path("dist/TMflow_Security_Report_Generator.exe")
    if exe_path.exists():
        shutil.copy2(exe_path, dist_dir / "TMflow_Security_Report_Generator.exe")
        print("✅ 執行檔已複製")
    else:
        print("❌ 找不到執行檔")
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
    
    # 創建使用說明
    usage_text = """# TMflow Security Report Generator v1.0.2.003

## 快速開始

1. 複製 config.example.txt 為 config.txt
2. 編輯 config.txt 填入您的 API 資訊：
   ```
   API_TOKEN=your_api_token_here
   SUBDOMAIN=tm-robot
   ORGANIZATION=Techman Robot
   OUTPUT_PATH=reports
   ```
3. 執行 TMflow_Security_Report_Generator.exe

## 系統需求

- Windows 10 或更新版本
- 網路連接（用於 Finite State API）

## 注意事項

- 第一次啟動可能需要較長時間
- 確保 fs-reporter 和 fs-report 資料夾在同一目錄
- 報告會輸出到 reports 資料夾

## 技術支援

GitHub: https://github.com/kenshu528-oss/TMflow-security-report-generator
"""
    
    with open(dist_dir / "使用說明.txt", "w", encoding="utf-8") as f:
        f.write(usage_text)
    
    print("✅ 已創建使用說明")
    
    print()
    print("🎉 打包完成！")
    print(f"📁 發布包位置: {dist_dir.absolute()}")
    print()
    print("📋 測試步驟:")
    print("1. 進入發布包資料夾")
    print("2. 複製 config.example.txt 為 config.txt")
    print("3. 編輯 config.txt 填入 API 資訊")
    print("4. 執行 TMflow_Security_Report_Generator.exe")
    print()
    print("✅ 如果測試成功，可以將整個資料夾壓縮成 ZIP 分享給同仁")
    
    return True

if __name__ == "__main__":
    build_simple_exe()