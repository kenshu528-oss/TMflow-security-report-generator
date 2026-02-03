#!/usr/bin/env python3
"""
TMflow 報告生成腳本
自動生成 Standard 和 Detailed 報告
"""

import os
import subprocess
import sys
from datetime import datetime

# 配置信息
TOKEN = "svza5d5kdulphw7kj2iba2lqyacs4nmhlwuhlykv7r33z3nxgvkq"
SUBDOMAIN = "tm-robot"
ORGANIZATION = "Techman Robot"

# 版本信息
VERSIONS = {
    "2.26.1200.0": "1936462473699050499",
    # 可以添加更多版本
}

def generate_timestamp():
    """生成時間戳記"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def generate_report(version_name, version_id, report_type="standard", output_dir="reports"):
    """生成報告"""
    timestamp = generate_timestamp()
    
    # 確保輸出目錄存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 構建文件名
    report_suffix = "Standard" if report_type == "standard" else "Detailed"
    filename = f"TMflow_{version_name}_{report_suffix}_{timestamp}.pdf"
    output_path = os.path.join(output_dir, filename)
    
    # 構建命令
    cmd = [
        "python", "fs-reporter/main.py",
        "-t", TOKEN,
        "-s", SUBDOMAIN,
        "-pvi", version_id,
        "-n", ORGANIZATION,
        "-o", output_path
    ]
    
    # 如果是詳細報告，添加 -d 參數
    if report_type == "detailed":
        cmd.insert(-2, "-d")
    
    print(f"正在生成 {report_suffix} 報告: {filename}")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ {report_suffix} 報告生成成功: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"❌ {report_suffix} 報告生成失敗:")
        print(f"錯誤: {e.stderr}")
        return None

def main():
    """主函數"""
    print("=== TMflow 報告生成工具 ===")
    
    # 檢查 fs-reporter 是否存在
    if not os.path.exists("fs-reporter/main.py"):
        print("❌ 錯誤: 找不到 fs-reporter/main.py")
        print("請確保 fs-reporter 工具已正確安裝")
        sys.exit(1)
    
    # 生成所有版本的報告
    for version_name, version_id in VERSIONS.items():
        print(f"\n--- 處理版本: {version_name} ---")
        
        # 生成標準報告
        generate_report(version_name, version_id, "standard")
        
        # 生成詳細報告
        generate_report(version_name, version_id, "detailed")
    
    print("\n=== 報告生成完成 ===")

if __name__ == "__main__":
    main()