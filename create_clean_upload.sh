#!/bin/bash

echo "📦 创建精简GitHub上传包（无大文件）"
echo "=================================="

# 创建临时目录
temp_dir="excel-data-processor-clean"
rm -rf "$temp_dir"
mkdir "$temp_dir"

echo "📁 复制项目文件（排除大文件）..."

# 复制所有需要的文件，但排除构建产物
rsync -av \
  --exclude='.git' \
  --exclude='dist/' \
  --exclude='build/' \
  --exclude='*.zip' \
  --exclude='__pycache__/' \
  --exclude='*.pyc' \
  --exclude='*.pyo' \
  --exclude='.DS_Store' \
  --exclude='excel-data-processor-upload' \
  --exclude='excel-data-processor-clean' \
  . "$temp_dir/"

# 检查文件大小
echo ""
echo "🔍 检查大文件（>1MB）："
find "$temp_dir" -type f -size +1M -exec ls -lh {} \; || echo "✅ 没有发现大文件"

# 计算总大小
total_size=$(du -sh "$temp_dir" | cut -f1)
echo ""
echo "📊 总大小: $total_size"

# 创建压缩包
echo ""
echo "🗜️  创建压缩包..."
zip -r "${temp_dir}.zip" "$temp_dir"

# 清理临时目录
rm -rf "$temp_dir"

# 检查压缩包大小
zip_size=$(ls -lh "${temp_dir}.zip" | awk '{print $5}')
echo ""
echo "✅ 精简上传包已创建: ${temp_dir}.zip"
echo "📊 压缩包大小: $zip_size"

if [[ $(stat -f%z "${temp_dir}.zip") -lt 25000000 ]]; then
    echo "✅ 文件大小符合GitHub 25MB限制"
else
    echo "⚠️  文件仍然超过25MB，需要进一步精简"
fi

echo ""
echo "📝 精简上传步骤："
echo "   1. 解压: unzip ${temp_dir}.zip"
echo "   2. 上传解压后的文件到GitHub"
echo "   3. 不包含构建产物，GitHub Actions会自动构建"