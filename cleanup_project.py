#!/usr/bin/env python3
"""
專案清理腳本 - 刪除多餘的測試檔案、舊版本建置腳本和備份資料夾
"""

import os
import shutil

def main():
    print("🧹 開始清理專案資料夾...")
    
    # 要刪除的舊版本資料夾（保留最新的 3 個版本）
    old_version_folders = [
        "TMflow_Security_Report_Generator_v1.0.2.008",
        "TMflow_Security_Report_Generator_v1.0.2.009",
        "TMflow_Security_Report_Generator_v1.0.2.010",
        "TMflow_Security_Report_Generator_v1.0.2.011",
        "TMflow_Security_Report_Generator_v1.0.2.012",
        "TMflow_Security_Report_Generator_v1.0.2.013",
        "TMflow_Security_Report_Generator_v1.0.2.014",
        "TMflow_Security_Report_Generator_v1.0.2.015",
        "TMflow_Security_Report_Generator_v1.0.2.019",
        "TMflow_Security_Report_Generator_v1.0.2.031",
        "TMflow_Security_Report_Generator_v1.0.2.035",
        "TMflow_Security_Report_Generator_v1.0.2.036",
        "TMflow_Security_Report_Generator_v1.0.2.037",
        "TMflow_Security_Report_Generator_v1.0.2.038",
        "TMflow_Security_Report_Generator_v1.0.2.039",
        "TMflow_Security_Report_Generator_v1.0.2.040",
        "TMflow_Security_Report_Generator_v1.0.2.041",
        # 保留 v1.0.2.042, v1.0.2.043, v1.0.2.044
    ]
    
    # 要刪除的舊版本建置腳本
    old_build_scripts = [
        "build_api_functional.py",
        "build_exe.py",
        "build_executable.py",
        "build_simple.py",
        "build_ui_demo.py",
        "build_v1.0.2.040_fixed.py",
        "build_v1.0.2.041_final.py",
        # 保留最新的 3 個建置腳本
    ]
    
    # 要刪除的測試檔案
    test_files = [
        "test_api_032.py",
        "test_api_connection.py",
        "test_api_functional.py",
        "test_api_simple.py",
        "test_direct_integration.py",
        "test_direct_integration_v2.py",
        "test_exe_report_generation.py",
        "test_single_version_selection.py",
        "test_v1.0.2.039_final.py",
        "test_v1.0.2.040_final.py",
        "test_version_selection.py",
        "final_simple_test.py",
        # 保留 test_modules.py（模組化測試工具）
    ]
    
    # 要刪除的測試生成的 PDF
    test_pdfs = [
        "test_direct_integration_20260205_105432.pdf",
        "test_direct_v2_20260205_110150.pdf",
    ]
    
    # 要刪除的舊版本 UI 檔案
    old_ui_files = [
        "ui_api_functional.py",
        "ui_architecture_demo.py",
        "ui_executable.py",
        "ui_modern.py",
        # 保留 ui_modular.py（當前使用的版本）
    ]
    
    # 要刪除的舊版本 spec 檔案
    old_spec_files = [
        "TMflow_Security_Report_Generator_Modular_v1.0.2.039.spec",
        "TMflow_Security_Report_Generator_Modular.spec",
        "TMflow_Security_Report_Generator_v1.0.2.040.spec",
        "TMflow_Security_Report_Generator_v1.0.2.041.spec",
        "TMflow_Security_Report_Generator_v1.0.2.042.spec",
        "TMflow_Security_Report_Generator_v1.0.2.043.spec",
        "TMflow_Security_Report_Generator.spec",
        "ui_modular.spec",
        # 保留 v1.0.2.044.spec（最新版本）
    ]
    
    # 要刪除的說明文件
    old_docs = [
        "v1.0.2.028_改善說明.md",
        "v1.0.2.031_務實解決方案.md",
        "v1.0.2.032_API修正說明.md",
        "UI_Design_Document.md",  # 已整合到 UI_SPECIFICATION.md
        "DEPLOYMENT_GUIDE.md",  # 舊版部署指南
        "DEPLOYMENT_SUMMARY.md",  # 舊版部署摘要
    ]
    
    # 要刪除的工具腳本
    old_tools = [
        "run_python_gui.py",
        "run_python_version.py",
        "generate_reports.py",  # 舊版命令列工具
        "cleanup_old_versions.py",  # 舊版清理腳本
    ]
    
    # 要刪除的 PyInstaller 建置資料夾
    build_folders = [
        "build",
        "dist",
        "__pycache__",
    ]
    
    deleted_count = 0
    total_size = 0
    
    # 刪除舊版本資料夾
    print("\n📁 刪除舊版本資料夾...")
    for folder in old_version_folders:
        if os.path.exists(folder):
            folder_size = get_folder_size(folder)
            shutil.rmtree(folder)
            deleted_count += 1
            total_size += folder_size
            print(f"  ✅ 已刪除: {folder} ({folder_size / (1024*1024):.1f} MB)")
    
    # 刪除舊版本建置腳本
    print("\n🔨 刪除舊版本建置腳本...")
    for file in old_build_scripts:
        if os.path.exists(file):
            file_size = os.path.getsize(file)
            os.remove(file)
            deleted_count += 1
            total_size += file_size
            print(f"  ✅ 已刪除: {file}")
    
    # 刪除測試檔案
    print("\n🧪 刪除測試檔案...")
    for file in test_files:
        if os.path.exists(file):
            file_size = os.path.getsize(file)
            os.remove(file)
            deleted_count += 1
            total_size += file_size
            print(f"  ✅ 已刪除: {file}")
    
    # 刪除測試 PDF
    print("\n📄 刪除測試生成的 PDF...")
    for file in test_pdfs:
        if os.path.exists(file):
            file_size = os.path.getsize(file)
            os.remove(file)
            deleted_count += 1
            total_size += file_size
            print(f"  ✅ 已刪除: {file}")
    
    # 刪除舊版本 UI 檔案
    print("\n🖥️ 刪除舊版本 UI 檔案...")
    for file in old_ui_files:
        if os.path.exists(file):
            file_size = os.path.getsize(file)
            os.remove(file)
            deleted_count += 1
            total_size += file_size
            print(f"  ✅ 已刪除: {file}")
    
    # 刪除舊版本 spec 檔案
    print("\n📋 刪除舊版本 spec 檔案...")
    for file in old_spec_files:
        if os.path.exists(file):
            file_size = os.path.getsize(file)
            os.remove(file)
            deleted_count += 1
            total_size += file_size
            print(f"  ✅ 已刪除: {file}")
    
    # 刪除說明文件
    print("\n📝 刪除舊版本說明文件...")
    for file in old_docs:
        if os.path.exists(file):
            file_size = os.path.getsize(file)
            os.remove(file)
            deleted_count += 1
            total_size += file_size
            print(f"  ✅ 已刪除: {file}")
    
    # 刪除工具腳本
    print("\n🔧 刪除舊版本工具腳本...")
    for file in old_tools:
        if os.path.exists(file):
            file_size = os.path.getsize(file)
            os.remove(file)
            deleted_count += 1
            total_size += file_size
            print(f"  ✅ 已刪除: {file}")
    
    # 刪除建置資料夾
    print("\n🗂️ 刪除建置資料夾...")
    for folder in build_folders:
        if os.path.exists(folder):
            folder_size = get_folder_size(folder)
            shutil.rmtree(folder)
            deleted_count += 1
            total_size += folder_size
            print(f"  ✅ 已刪除: {folder} ({folder_size / (1024*1024):.1f} MB)")
    
    # 顯示清理結果
    print(f"\n✨ 清理完成！")
    print(f"📊 刪除項目數: {deleted_count}")
    print(f"💾 釋放空間: {total_size / (1024*1024):.1f} MB")
    
    # 顯示保留的檔案
    print("\n📋 保留的重要檔案:")
    print("  ✅ ui_modular.py - 當前主程式")
    print("  ✅ build_v1.0.2.042_shareable.py - 可分享版本建置腳本")
    print("  ✅ build_v1.0.2.043_auto_connect.py - 自動連線版本建置腳本")
    print("  ✅ build_v1.0.2.044_status_fix.py - 最新版本建置腳本")
    print("  ✅ build_modular.py - 通用模組化建置腳本")
    print("  ✅ test_modules.py - 模組化測試工具")
    print("  ✅ TMflow_Security_Report_Generator_v1.0.2.042/ - 可分享版本")
    print("  ✅ TMflow_Security_Report_Generator_v1.0.2.043/ - 自動連線版本")
    print("  ✅ TMflow_Security_Report_Generator_v1.0.2.044/ - 最新版本")
    print("  ✅ TMflow_Security_Report_Generator_v1.0.2.044.spec - 最新 spec 檔案")
    print("  ✅ fs-reporter/ - 報告生成工具")
    print("  ✅ fs-report/ - 報告模板工具")
    print("  ✅ config.txt - 配置檔案")
    print("  ✅ CHANGELOG.md - 更新日誌")
    print("  ✅ README.md - 專案說明")
    print("  ✅ UI_SPECIFICATION.md - UI 設計規格")
    print("  ✅ UI_ISSUES_LOG.md - UI 問題記錄")

def get_folder_size(folder_path):
    """計算資料夾大小"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
    except:
        pass
    return total_size

if __name__ == "__main__":
    main()
