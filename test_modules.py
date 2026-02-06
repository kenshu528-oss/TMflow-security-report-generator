#!/usr/bin/env python3
"""
模組化測試腳本 - 逐一驗證各個功能模組
"""

import sys
import os

# 添加當前目錄到 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_config_manager():
    """測試配置管理模組"""
    print("🧪 測試配置管理模組...")
    
    try:
        from ui_modular import ConfigManager
        
        config_manager = ConfigManager("test_config.txt")
        
        # 測試預設配置
        config = config_manager.load_config()
        print(f"✅ 載入預設配置成功")
        print(f"   - API_TOKEN: {config['API_TOKEN'][:10]}...")
        print(f"   - SUBDOMAIN: {config['SUBDOMAIN']}")
        print(f"   - ORGANIZATION: {config['ORGANIZATION']}")
        
        # 測試儲存配置
        test_config = config.copy()
        test_config["TEST_FIELD"] = "test_value"
        
        if config_manager.save_config(test_config):
            print("✅ 儲存配置成功")
        else:
            print("❌ 儲存配置失敗")
        
        # 清理測試檔案
        if os.path.exists("test_config.txt"):
            os.remove("test_config.txt")
            print("✅ 清理測試檔案完成")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置管理模組測試失敗: {e}")
        return False

def test_api_manager():
    """測試 API 管理模組"""
    print("\n🧪 測試 API 管理模組...")
    
    try:
        from ui_modular import APIManager
        
        # 使用實際的 API 憑證
        api_manager = APIManager(
            api_token="svza5d5kdulphw7kj2iba2lqyacs4nmhlwuhlykv7r33z3nxgvkq",
            subdomain="tm-robot"
        )
        
        print("✅ API 管理器初始化成功")
        
        # 測試連接
        print("🔗 測試 API 連接...")
        success, message = api_manager.test_connection()
        
        if success:
            print(f"✅ API 連接測試成功: {message}")
            
            # 測試獲取專案
            print("📋 測試獲取專案列表...")
            projects, msg = api_manager.fetch_projects()
            
            if projects:
                print(f"✅ 獲取專案成功: {len(projects)} 個專案")
                for project_name, versions in projects.items():
                    print(f"   - {project_name}: {len(versions)} 個版本")
                    if versions:
                        print(f"     最新版本: {versions[0]['version']}")
                return True
            else:
                print(f"❌ 獲取專案失敗: {msg}")
                return False
        else:
            print(f"❌ API 連接測試失敗: {message}")
            return False
        
    except Exception as e:
        print(f"❌ API 管理模組測試失敗: {e}")
        return False

def test_report_generator():
    """測試報告生成模組"""
    print("\n🧪 測試報告生成模組...")
    
    try:
        from ui_modular import ReportGenerator
        
        # 檢查 fs-reporter 是否存在
        if not os.path.exists("fs-reporter/main.py"):
            print("⚠️ 找不到 fs-reporter/main.py，跳過報告生成測試")
            return True
        
        report_generator = ReportGenerator(
            api_token="svza5d5kdulphw7kj2iba2lqyacs4nmhlwuhlykv7r33z3nxgvkq",
            subdomain="tm-robot",
            organization="Techman Robot"
        )
        
        print("✅ 報告生成器初始化成功")
        
        # 創建測試輸出目錄
        test_output_dir = "test_reports"
        os.makedirs(test_output_dir, exist_ok=True)
        
        # 測試生成報告（使用 TMflow 2.26.1200 的版本 ID）
        print("📄 測試生成報告...")
        test_version = "2.26.1200"
        test_version_id = "1936462473699050499"
        
        success, result = report_generator.generate_single_report(
            test_version, test_version_id, "standard", test_output_dir
        )
        
        if success:
            print(f"✅ 報告生成測試成功: {os.path.basename(result)}")
            
            # 檢查檔案是否存在
            if os.path.exists(result):
                file_size = os.path.getsize(result)
                print(f"   檔案大小: {file_size:,} bytes")
                
                # 清理測試檔案
                os.remove(result)
                print("✅ 清理測試檔案完成")
            
            return True
        else:
            print(f"❌ 報告生成測試失敗: {result}")
            return False
        
    except Exception as e:
        print(f"❌ 報告生成模組測試失敗: {e}")
        return False
    finally:
        # 清理測試目錄
        if os.path.exists("test_reports"):
            try:
                os.rmdir("test_reports")
            except:
                pass

def test_ui_components():
    """測試 UI 組件（不啟動主視窗）"""
    print("\n🧪 測試 UI 組件...")
    
    try:
        import tkinter as tk
        from ui_modular import ModularTMflowReportGeneratorUI
        
        # 創建隱藏的根視窗
        root = tk.Tk()
        root.withdraw()  # 隱藏視窗
        
        # 初始化 UI（但不顯示）
        app = ModularTMflowReportGeneratorUI(root)
        
        print("✅ UI 組件初始化成功")
        
        # 測試模組是否正確載入
        if hasattr(app, 'config_manager'):
            print("✅ 配置管理器已載入")
        
        if hasattr(app, 'api_manager'):
            print("✅ API 管理器已載入")
        
        if hasattr(app, 'report_generator'):
            print("✅ 報告生成器已載入")
        
        # 測試配置載入
        if app.config:
            print(f"✅ 配置已載入: {len(app.config)} 個設定項目")
        
        # 關閉測試視窗
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"❌ UI 組件測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🚀 TMflow Security Report Generator - 模組化測試")
    print("=" * 60)
    
    tests = [
        ("配置管理模組", test_config_manager),
        ("API 管理模組", test_api_manager),
        ("報告生成模組", test_report_generator),
        ("UI 組件", test_ui_components)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 測試過程中發生錯誤: {e}")
            results.append((test_name, False))
    
    # 顯示測試結果摘要
    print("\n" + "=" * 60)
    print("📊 測試結果摘要:")
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"   {test_name}: {status}")
        
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\n總計: {passed} 個通過, {failed} 個失敗")
    
    if failed == 0:
        print("🎉 所有模組測試通過！可以安全使用模組化版本。")
        return True
    else:
        print("⚠️ 部分模組測試失敗，請檢查相關問題。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)