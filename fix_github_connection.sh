#!/bin/bash

echo "🔧 修复GitHub连接问题"
echo "===================="

# 检查是否有SSH密钥
if [ -f ~/.ssh/id_rsa.pub ]; then
    echo "✅ 检测到SSH密钥"
    echo "📋 您的SSH公钥："
    cat ~/.ssh/id_rsa.pub
    echo ""
    echo "📝 请将上面的SSH公钥添加到GitHub："
    echo "   1. 访问: https://github.com/settings/keys"
    echo "   2. 点击 'New SSH key'"
    echo "   3. 粘贴上面的公钥内容"
    echo "   4. 点击 'Add SSH key'"
    echo ""
    read -p "已添加SSH密钥到GitHub？(y/n): " ssh_added
    
    if [[ $ssh_added == "y" || $ssh_added == "Y" ]]; then
        echo "🔄 切换到SSH连接..."
        git remote set-url origin git@github.com:penny8848/excel-data-processor.git
        echo "📤 尝试推送..."
        git push origin main --force
    fi
else
    echo "❌ 未找到SSH密钥"
    echo "🔑 生成SSH密钥..."
    ssh-keygen -t rsa -b 4096 -C "your_email@example.com" -f ~/.ssh/id_rsa -N ""
    
    echo "✅ SSH密钥已生成"
    echo "📋 您的SSH公钥："
    cat ~/.ssh/id_rsa.pub
    echo ""
    echo "📝 请将上面的SSH公钥添加到GitHub："
    echo "   1. 访问: https://github.com/settings/keys"
    echo "   2. 点击 'New SSH key'"
    echo "   3. 粘贴上面的公钥内容"
    echo "   4. 点击 'Add SSH key'"
    echo ""
    echo "添加完成后，重新运行此脚本"
fi