@echo off
chcp 65001 >nul
echo ========================================
echo   Excel Data Processor Windows构建工具
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.8或更高版本
    echo.
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ 找到Python
python --version

echo.
echo 🚀 开始构建Windows exe文件...
echo.

REM 运行Python构建脚本
python build_exe_windows.py

echo.
echo 构建完成！
pause