#!/usr/bin/env python3
"""
TMflow Security Report Generator 打包腳本
使用 PyInstaller 創建 .exe 執行檔
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """安裝 PyInstaller"""
    print("正在安裝 PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller 安裝成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller 安裝失敗: {e}")
        return False

def create_spec_file():
    """創建 PyInstaller spec 檔案"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['ui_modern.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('fs-reporter', 'fs-reporter'),
        ('fs-report', 'fs-report'),
        ('config.example.txt', '.'),
        ('README.md', '.'),
        ('USAGE_GUIDE.md', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        'requests',
        'threading',
        'subprocess',
        'json',
        'datetime',
        'os',
        'sys',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TMflow_Security_Report_Generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''
    
    with open('tmflow_generator.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Spec 檔案已創建")

def build_executable():
    """建立執行檔"""
    print("正在建立執行檔...")
    print("這可能需要幾分鐘時間，請耐心等待...")
    
    try:
        # 使用 spec 檔案建立
        cmd = [
            "pyinstaller",
            "--clean",
            "--noconfirm",
            "tmflow_generator.spec"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 執行檔建立成功！")
            return True
        else:
            print(f"❌ 建立失敗:")
            print(result.stderr)
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 建立執行檔失敗: {e}")
        return False

def create_distribution_package():
    """創建發布包"""
    print("正在創建發布包...")
    
    # 創建發布目錄
    dist_dir = Path("TMflow_Security_Report_Generator_v1.0.2.002")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    dist_dir.mkdir()
    
    # 複製執行檔
    exe_path = Path("dist/TMflow_Security_Report_Generator.exe")
    if exe_path.exists():
        shutil.copy2(exe_path, dist_dir / "TMflow_Security_Report_Generator.exe")
    
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
    
    # 複製工具目錄
    if Path("fs-reporter").exists():
        shutil.copytree("fs-reporter", dist_dir / "fs-reporter")
    
    if Path("fs-report").exists():
        shutil.copytree("fs-report", dist_dir / "fs-report")
    
    # 創建 reports 目錄
    (dist_dir / "reports").mkdir(exist_ok=True)
    
    # 創建安裝說明
    install_guide = f"""# TMflow Security Report Generator v1.0.2.002

## 安裝說明

1. 解壓縮此資料夾到任意位置
2. 複製 config.example.txt 為 config.txt
3. 編輯 config.txt 填入您的 API 資訊
4. 執行 TMflow_Security_Report_Generator.exe

## 系統需求

- Windows 10 或更新版本
- 網路連接（用於 Finite State API）

## 檔案說明

- TMflow_Security_Report_Generator.exe - 主程式
- config.example.txt - 配置檔案範例
- fs-reporter/ - PDF 報告生成工具
- fs-report/ - 多格式報告生成工具
- reports/ - 報告輸出目錄
- README.md - 詳細說明文件
- USAGE_GUIDE.md - 使用指南

## 技術支援

GitHub: https://github.com/kenshu528-oss/TMflow-security-report-generator
"""
    
    with open(dist_dir / "安裝說明.txt", "w", encoding="utf-8") as f:
        f.write(install_guide)
    
    print(f"✅ 發布包已創建: {dist_dir}")
    return dist_dir

def main():
    """主函數"""
    print("=== TMflow Security Report Generator 打包工具 ===")
    print()
    
    # 檢查必要檔案
    if not Path("ui_modern.py").exists():
        print("❌ 找不到 ui_modern.py")
        return
    
    # 安裝 PyInstaller
    if not install_pyinstaller():
        return
    
    # 創建 spec 檔案
    create_spec_file()
    
    # 建立執行檔
    if not build_executable():
        return
    
    # 創建發布包
    dist_dir = create_distribution_package()
    
    print()
    print("🎉 打包完成！")
    print(f"📁 發布包位置: {dist_dir.absolute()}")
    print()
    print("📋 接下來的步驟:")
    print("1. 測試執行檔是否正常運作")
    print("2. 將整個資料夾壓縮成 ZIP 檔案")
    print("3. 分享給同仁使用")
    print()
    print("⚠️  注意事項:")
    print("- 確保同仁的電腦有網路連接")
    print("- 提醒同仁設定正確的 config.txt")
    print("- 第一次執行可能需要較長時間")

if __name__ == "__main__":
    main()