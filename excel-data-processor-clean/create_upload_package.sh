#!/bin/bash

echo "📦 创建GitHub上传包"
echo "=================="

# 创建临时目录
temp_dir="excel-data-processor-upload"
rm -rf "$temp_dir"
mkdir "$temp_dir"

# 复制所有需要的文件（排除.git目录）
echo "📁 复制项目文件..."
rsync -av --exclude='.git' --exclude="$temp_dir" . "$temp_dir/"

# 创建压缩包
echo "🗜️  创建压缩包..."
zip -r "${temp_dir}.zip" "$temp_dir"

# 清理临时目录
rm -rf "$temp_dir"

echo "✅ 上传包已创建: ${temp_dir}.zip"
echo ""
echo "📝 手动上传步骤："
echo "   1. 访问: https://github.com/penny8848/excel-data-processor"
echo "   2. 点击 'uploading an existing file'"
echo "   3. 解压 ${temp_dir}.zip"
echo "   4. 拖拽所有文件到GitHub页面"
echo "   5. 提交更改"
echo ""
echo "⚠️  注意：确保上传所有文件，特别是 .github/workflows/ 目录"