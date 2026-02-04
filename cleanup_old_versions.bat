@echo off
echo === TMflow Security Report Generator 清理腳本 ===
echo.

echo 正在嘗試刪除舊版本資料夾...
if exist "TMflow_Security_Report_Generator_v1.0.2.002" (
    echo 嘗試刪除 TMflow_Security_Report_Generator_v1.0.2.002...
    rmdir /s /q "TMflow_Security_Report_Generator_v1.0.2.002" 2>nul
    if exist "TMflow_Security_Report_Generator_v1.0.2.002" (
        echo ❌ 無法刪除 TMflow_Security_Report_Generator_v1.0.2.002 (檔案可能被佔用)
        echo 💡 請關閉所有相關程式後手動刪除此資料夾
    ) else (
        echo ✅ 已刪除 TMflow_Security_Report_Generator_v1.0.2.002
    )
) else (
    echo ✅ TMflow_Security_Report_Generator_v1.0.2.002 已不存在
)

echo.
echo 正在檢查其他可清理的檔案...

REM 刪除 PyInstaller 產生的檔案
if exist "*.spec" (
    echo 刪除 PyInstaller spec 檔案...
    del /q "*.spec" 2>nul
)

if exist "__pycache__" (
    echo 刪除 Python 快取檔案...
    rmdir /s /q "__pycache__" 2>nul
)

echo.
echo === 清理完成 ===
echo.
echo 📁 保留的重要檔案和資料夾:
echo   ✅ TMflow_Security_Report_Generator_v1.0.2.003/ (最新版本)
echo   ✅ fs-reporter/ (報告生成工具)
echo   ✅ fs-report/ (新格式報告工具)
echo   ✅ reports/ (報告輸出目錄)
echo   ✅ 所有主要程式檔案和文檔
echo.
echo 🎉 專案目錄已清理完成！
pause