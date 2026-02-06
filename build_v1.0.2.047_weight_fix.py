#!/usr/bin/env python3
"""
TMflow Security Report Generator - 建置腳本 v1.0.2.047
UI 佈局比例修正版 (權重修正)
"""

import os
import shutil
import subprocess
import sys

def build_executable():
    """建立執行檔"""
    
    print("=" * 60)
    print("TMflow Security Report Generator v1.0.2.047")
    print("UI 佈局比例修正版 (權重修正) - 建置腳本")
    print("=" * 60)
    print()
    
    # 版本資訊
    version = "v1.0.2.047"
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
    print("🔨 開始建立執行檔...")
    print()
    
    pyinstaller_cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        f'--name=TMflow_Security_Report_Generator_{version}',
        '--hidden-import=finite_state_reporter',
        '--hidden-import=finite_state_reporter.core',
        '--hidden-import=finite_state_reporter.core.reporter',
        '--hidden-import=finite_state_reporter.pdf',
        '--hidden-import=finite_state_reporter.pdf.styles',
        '--hidden-import=finite_state_reporter.pdf.flowables',
        '--hidden-import=finite_state_reporter.pdf.page_templates',
        '--hidden-import=finite_state_reporter.pdf.colors',
        '--hidden-import=reportlab',
        '--hidden-import=reportlab.pdfgen',
        '--hidden-import=reportlab.pdfgen.canvas',
        '--hidden-import=reportlab.lib',
        '--hidden-import=reportlab.lib.pagesizes',
        '--hidden-import=reportlab.lib.styles',
        '--hidden-import=reportlab.lib.units',
        '--hidden-import=reportlab.lib.colors',
        '--hidden-import=reportlab.platypus',
        '--hidden-import=matplotlib',
        '--hidden-import=matplotlib.pyplot',
        '--hidden-import=numpy',
        '--hidden-import=pandas',
        '--hidden-import=PIL',
        '--exclude-module=sklearn',
        '--exclude-module=scipy',
        '--exclude-module=pytest',
        '--exclude-module=IPython',
        '--exclude-module=notebook',
        '--optimize=2',
        '--strip',
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
UI 佈局比例修正版 (權重修正)

=== 快速開始 ===

1. 編輯 config.txt 檔案，填入您的 API Token
2. 雙擊執行 {exe_name}
3. 應用程式會自動連接 API
4. 點擊 "Refresh" 載入專案資料
5. 選擇要生成報告的版本
6. 點擊 "Generate Reports" 生成報告

=== 版本特色 ===

✅ UI 佈局比例修正（權重修正）
   - 修正 grid 權重設定錯誤（60/40 → 3/2）
   - 正確實現 60:40 的左右比例
   - 視窗放大後保持正確比例

✅ 繼承所有功能
   - 按鈕文字國際化（v1.0.2.045）
   - API 連接狀態完整顯示（v1.0.2.044）
   - 啟動自動連線功能（v1.0.2.043）
   - 完整的報告生成功能

=== 詳細說明 ===

請參閱以下文檔：
- README.md - 專案概述和快速開始
- USAGE_GUIDE.md - 詳細使用指南
- CHANGELOG.md - 完整更新記錄

=== 技術支援 ===

如有問題，請查看：
1. USAGE_GUIDE.md 中的常見問題
2. CHANGELOG.md 中的已知問題
3. GitHub Issues

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
    print("   2. 驗證 UI 佈局比例")
    print("   3. 確認視窗放大後比例為 60:40")
    print()
    
    return True

if __name__ == "__main__":
    success = build_executable()
    sys.exit(0 if success else 1)
