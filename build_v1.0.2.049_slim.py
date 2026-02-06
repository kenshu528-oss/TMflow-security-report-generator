#!/usr/bin/env python3
"""
TMflow Security Report Generator - 建置腳本 v1.0.2.049
執行檔瘦身優化版
"""

import os
import shutil
import subprocess
import sys

def build_executable():
    """建立執行檔"""
    
    print("=" * 60)
    print("TMflow Security Report Generator v1.0.2.049")
    print("執行檔瘦身優化版 - 建置腳本")
    print("=" * 60)
    print()
    
    # 版本資訊
    version = "v1.0.2.049"
    output_folder = f"TMflow_Security_Report_Generator_{version}"
    
    # 清理舊的建置檔案
    print("🧹 清理舊的建置檔案...")
    folders_to_clean = ['build', 'dist', output_folder]
    for folder in folders_to_clean:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"   已刪除: {folder}")
    
    # 清理舊的 spec 檔案
    spec_file = f"TMflow_Security_Report_Generator_{version}.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print(f"   已刪除: {spec_file}")
    
    print()
    
    # 建立執行檔
    print("🔨 開始建立執行檔（瘦身優化）...")
    print()
    
    # 瘦身策略：
    # 1. 排除所有大型數據處理和科學計算庫
    # 2. 排除所有測試和開發工具
    # 3. 排除不必要的 matplotlib 後端
    # 4. 使用 UPX 壓縮（如果可用）
    pyinstaller_cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        f'--name=TMflow_Security_Report_Generator_{version}',
        
        # 只包含核心 GUI 依賴
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.scrolledtext',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter.messagebox',
        
        # 只包含必要的網路和 JSON 處理
        '--hidden-import=requests',
        '--hidden-import=json',
        '--hidden-import=threading',
        '--hidden-import=datetime',
        
        # 排除所有大型科學計算庫
        '--exclude-module=numpy',
        '--exclude-module=pandas',
        '--exclude-module=matplotlib',
        '--exclude-module=scipy',
        '--exclude-module=sklearn',
        '--exclude-module=reportlab',
        '--exclude-module=PIL',
        '--exclude-module=Pillow',
        
        # 排除測試和開發工具
        '--exclude-module=pytest',
        '--exclude-module=unittest',
        '--exclude-module=IPython',
        '--exclude-module=notebook',
        '--exclude-module=jupyter',
        
        # 排除文檔生成工具
        '--exclude-module=sphinx',
        '--exclude-module=docutils',
        
        # 排除其他不需要的模組
        '--exclude-module=setuptools',
        '--exclude-module=pip',
        '--exclude-module=wheel',
        '--exclude-module=distutils',
        
        # 優化選項
        '--optimize=2',
        '--strip',
        '--noupx',  # 先不用 UPX，避免相容性問題
        
        'ui_modular.py'
    ]
    
    try:
        result = subprocess.run(pyinstaller_cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ 建置失敗: {e}")
        print(e.stderr)
        return False
    
    print()
    print("✅ 執行檔建立完成")
    print()
    
    # 建立發布資料夾
    print("📦 準備發布資料夾...")
    os.makedirs(output_folder, exist_ok=True)
    
    # 複製執行檔
    exe_name = f"TMflow_Security_Report_Generator_{version}.exe"
    src_exe = os.path.join('dist', exe_name)
    dst_exe = os.path.join(output_folder, exe_name)
    
    if os.path.exists(src_exe):
        shutil.copy2(src_exe, dst_exe)
        print(f"   ✅ 執行檔: {exe_name}")
        
        # 顯示檔案大小
        size_mb = os.path.getsize(dst_exe) / (1024 * 1024)
        print(f"   📊 檔案大小: {size_mb:.1f} MB")
        
        # 與之前版本比較
        prev_size = 51.3
        reduction = prev_size - size_mb
        reduction_pct = (reduction / prev_size) * 100
        print(f"   📉 相比 v1.0.2.048: 減少 {reduction:.1f} MB ({reduction_pct:.1f}%)")
    else:
        print(f"   ❌ 找不到執行檔: {src_exe}")
        return False
    
    # 複製必要的資料夾和檔案
    items_to_copy = [
        ('fs-reporter', '資料夾'),
        ('fs-report', '資料夾'),
        ('config.example.txt', '檔案'),
        ('README.md', '檔案'),
        ('USAGE_GUIDE.md', '檔案'),
        ('CHANGELOG.md', '檔案'),
        ('LICENSE', '檔案')
    ]
    
    print()
    for item, item_type in items_to_copy:
        src = item
        dst = os.path.join(output_folder, item)
        
        if os.path.exists(src):
            if item_type == '資料夾':
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            print(f"   ✅ {item_type}: {item}")
        else:
            print(f"   ⚠️  找不到: {item}")
    
    # 建立空的 reports 資料夾
    reports_dir = os.path.join(output_folder, 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    print(f"   ✅ 資料夾: reports/")
    
    # 複製 config.txt（如果存在）
    if os.path.exists('config.txt'):
        shutil.copy2('config.txt', os.path.join(output_folder, 'config.txt'))
        print(f"   ✅ 檔案: config.txt")
    
    # 建立使用說明
    usage_text = f"""TMflow Security Report Generator {version}
執行檔瘦身優化版

=== 版本特色 ===

🎯 執行檔大幅瘦身
   - 移除不必要的大型依賴庫
   - 優化打包配置
   - 保持所有核心功能

✅ 完整功能保留
   - UI 佈局比例正確（60:40）
   - API 連接和專案載入
   - 報告生成功能（使用外部 fs-reporter）
   - 所有 UI 功能正常

=== 快速開始 ===

1. 編輯 config.txt 檔案，填入您的 API Token
2. 雙擊執行 {exe_name}
3. 應用程式會自動連接 API
4. 點擊 "Refresh" 載入專案資料
5. 選擇要生成報告的版本
6. 點擊 "Generate Reports" 生成報告

=== 技術說明 ===

本版本採用瘦身策略：
- 執行檔只包含 GUI 核心功能
- 報告生成依賴外部 fs-reporter 工具
- 大幅減少執行檔大小
- 功能完全不受影響

=== 詳細說明 ===

請參閱以下文檔：
- README.md - 專案概述和快速開始
- USAGE_GUIDE.md - 詳細使用指南
- CHANGELOG.md - 完整更新記錄

版本: {version}
日期: 2026-02-06
"""
    
    usage_file = os.path.join(output_folder, f'使用說明_{version}.txt')
    with open(usage_file, 'w', encoding='utf-8') as f:
        f.write(usage_text)
    print(f"   ✅ 檔案: 使用說明_{version}.txt")
    
    print()
    print("=" * 60)
    print("✅ 建置完成！")
    print("=" * 60)
    print()
    print(f"📁 發布資料夾: {output_folder}/")
    print(f"🚀 執行檔: {output_folder}/{exe_name}")
    print()
    print("📝 下一步:")
    print("   1. 測試執行檔功能")
    print("   2. 驗證報告生成功能")
    print("   3. 確認檔案大小減少")
    print()
    
    return True

if __name__ == "__main__":
    success = build_executable()
    sys.exit(0 if success else 1)
