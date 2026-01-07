#!/bin/bash

# Excel数据处理器 - GitHub自动设置脚本
# 此脚本将帮助您快速设置GitHub仓库并推送代码

echo "🚀 Excel数据处理器 - GitHub自动设置"
echo "=================================="

# 检查是否已有远程仓库
if git remote get-url origin 2>/dev/null; then
    echo "✅ 检测到已配置的远程仓库"
    git remote -v
    echo ""
    read -p "是否要推送到现有仓库？(y/n): " push_existing
    if [[ $push_existing == "y" || $push_existing == "Y" ]]; then
        echo "📤 推送代码到GitHub..."
        git push -u origin main
        if [ $? -eq 0 ]; then
            echo "✅ 代码推送成功！"
            echo "🔗 请访问您的GitHub仓库查看Actions构建进度"
        else
            echo "❌ 推送失败，请检查权限或网络连接"
        fi
    fi
    exit 0
fi

# 获取用户GitHub信息
echo "请提供您的GitHub信息："
read -p "GitHub用户名: " github_username
read -p "仓库名称 [excel-data-processor]: " repo_name

# 设置默认仓库名
if [ -z "$repo_name" ]; then
    repo_name="excel-data-processor"
fi

# 构建仓库URL
repo_url="https://github.com/${github_username}/${repo_name}.git"

echo ""
echo "📋 配置信息："
echo "   用户名: $github_username"
echo "   仓库名: $repo_name"
echo "   仓库URL: $repo_url"
echo ""

# 确认信息
read -p "信息是否正确？(y/n): " confirm
if [[ $confirm != "y" && $confirm != "Y" ]]; then
    echo "❌ 操作已取消"
    exit 1
fi

echo ""
echo "⚠️  重要提醒："
echo "   1. 请确保您已在GitHub上创建了仓库: $repo_name"
echo "   2. 仓库应该是空的（不要初始化README、.gitignore等）"
echo "   3. 如果需要认证，请准备好GitHub用户名和密码/令牌"
echo ""

read -p "已创建GitHub仓库并准备好推送？(y/n): " ready
if [[ $ready != "y" && $ready != "Y" ]]; then
    echo ""
    echo "📝 请按以下步骤操作："
    echo "   1. 访问: https://github.com/new"
    echo "   2. Repository name: $repo_name"
    echo "   3. Description: Excel数据处理器 - 支持字段选择和自定义字段的桌面应用"
    echo "   4. 选择 Public"
    echo "   5. 不要勾选任何初始化选项"
    echo "   6. 点击 Create repository"
    echo ""
    echo "创建完成后，重新运行此脚本"
    exit 0
fi

# 添加远程仓库并推送
echo "🔗 添加远程仓库..."
git remote add origin "$repo_url"

echo "📤 推送代码到GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 成功！代码已推送到GitHub"
    echo ""
    echo "📊 下一步："
    echo "   1. 访问: https://github.com/${github_username}/${repo_name}"
    echo "   2. 点击 'Actions' 标签查看构建进度"
    echo "   3. 构建完成后从 'Artifacts' 下载Windows exe文件"
    echo ""
    echo "⏱️  预计构建时间: 10-20分钟"
    echo "📦 最终文件: ExcelDataProcessor.exe (~100-150MB)"
else
    echo ""
    echo "❌ 推送失败"
    echo ""
    echo "🔧 可能的解决方案："
    echo "   1. 检查GitHub用户名和仓库名是否正确"
    echo "   2. 确保仓库已创建且为空"
    echo "   3. 检查网络连接"
    echo "   4. 可能需要GitHub个人访问令牌进行认证"
    echo ""
    echo "💡 手动操作命令："
    echo "   git remote add origin $repo_url"
    echo "   git push -u origin main"
fi