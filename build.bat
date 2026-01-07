@echo off
echo === Excel Data Processor 打包工具 ===
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 安装依赖
echo 安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo 依赖安装失败
    pause
    exit /b 1
)

REM 清理旧的构建文件
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec

REM 使用PyInstaller构建
echo 开始构建exe文件...
pyinstaller excel_processor.spec

REM 检查结果
if exist "dist\ExcelDataProcessor.exe" (
    echo.
    echo ✅ 构建成功！
    echo 📁 输出路径: dist\ExcelDataProcessor.exe
    echo.
    echo 使用说明:
    echo 1. 可执行文件位于 dist\ 目录中
    echo 2. 可以将 ExcelDataProcessor.exe 复制到任何位置运行
    echo 3. 首次运行可能需要一些时间来解压
) else (
    echo ❌ 构建失败
)

echo.
pause