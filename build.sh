#!/bin/bash

echo "=== Excel Data Processor 打包工具 ==="
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 安装依赖
echo "安装依赖包..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "依赖安装失败"
    exit 1
fi

# 清理旧的构建文件
echo "清理旧的构建文件..."
rm -rf build dist *.spec

# 使用PyInstaller构建
echo "开始构建可执行文件..."
pyinstaller excel_processor.spec

# 检查结果
if [ -f "dist/ExcelDataProcessor" ]; then
    echo
    echo "✅ 构建成功！"
    echo "📁 输出路径: dist/ExcelDataProcessor"
    echo
    echo "使用说明:"
    echo "1. 可执行文件位于 dist/ 目录中"
    echo "2. 可以将 ExcelDataProcessor 复制到任何位置运行"
    echo "3. 首次运行可能需要一些时间来解压"
    
    # 设置执行权限
    chmod +x dist/ExcelDataProcessor
    echo "4. 已设置执行权限"
else
    echo "❌ 构建失败"
    exit 1
fi

echo