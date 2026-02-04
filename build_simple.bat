@echo off
echo === TMflow Security Report Generator 簡易打包工具 ===
echo.

echo 正在安裝 PyInstaller...
pip install pyinstaller

echo.
echo 正在建立執行檔...
pyinstaller --onefile --windowed --name "TMflow_Security_Report_Generator" --add-data "fs-reporter;fs-reporter" --add-data "fs-report;fs-report" --add-data "config.example.txt;." ui_modern.py

echo.
echo 正在創建發布資料夾...
if exist "TMflow_Security_Report_Generator_v1.0.2.002" rmdir /s /q "TMflow_Security_Report_Generator_v1.0.2.002"
mkdir "TMflow_Security_Report_Generator_v1.0.2.002"

echo 複製檔案...
copy "dist\TMflow_Security_Report_Generator.exe" "TMflow_Security_Report_Generator_v1.0.2.002\"
copy "README.md" "TMflow_Security_Report_Generator_v1.0.2.002\"
copy "USAGE_GUIDE.md" "TMflow_Security_Report_Generator_v1.0.2.002\"
copy "config.example.txt" "TMflow_Security_Report_Generator_v1.0.2.002\"
copy "CHANGELOG.md" "TMflow_Security_Report_Generator_v1.0.2.002\"
copy "LICENSE" "TMflow_Security_Report_Generator_v1.0.2.002\"

echo 複製工具目錄...
xcopy "fs-reporter" "TMflow_Security_Report_Generator_v1.0.2.002\fs-reporter" /E /I /Q
xcopy "fs-report" "TMflow_Security_Report_Generator_v1.0.2.002\fs-report" /E /I /Q

echo 創建 reports 目錄...
mkdir "TMflow_Security_Report_Generator_v1.0.2.002\reports"

echo.
echo 🎉 打包完成！
echo 📁 發布包位置: TMflow_Security_Report_Generator_v1.0.2.002
echo.
echo 📋 接下來的步驟:
echo 1. 測試執行檔是否正常運作
echo 2. 將整個資料夾壓縮成 ZIP 檔案
echo 3. 分享給同仁使用
echo.
pause