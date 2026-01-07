#!/bin/bash

# Excel Data Processor GitHub仓库设置脚本

echo "🚀 Excel Data Processor GitHub仓库设置"
echo "========================================"
echo

# 检查是否已经是Git仓库
if [ ! -d ".git" ]; then
    echo "📁 初始化Git仓库..."
    git init
    echo "✅ Git仓库初始化完成"
else
    echo "✅ 已存在Git仓库"
fi

# 创建.gitignore文件
echo "📝 创建.gitignore文件..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
test_data.xlsx
*.log
temp/
tmp/

# Build artifacts (keep some for reference)
# Uncomment if you don't want to track build files
# build_exe.py
# build_windows.bat
# excel_processor*.spec
EOF

echo "✅ .gitignore文件创建完成"

# 添加所有文件
echo "📦 添加文件到Git..."
git add .
echo "✅ 文件添加完成"

# 创建初始提交
echo "💾 创建初始提交..."
git commit -m "Initial commit: Excel Data Processor with Windows build support

Features:
- Complete Python desktop application for Excel data processing
- PySide6 GUI with modern interface
- Support for Excel (.xlsx, .xls) and CSV files
- Field selection and custom field management
- Data preview functionality
- Windows executable build support via GitHub Actions
- Cross-platform build scripts

Build Support:
- macOS executable (PyInstaller)
- Windows executable (GitHub Actions)
- Comprehensive build documentation
- Automated CI/CD pipeline"

echo "✅ 初始提交完成"

# 显示下一步说明
echo
echo "🎯 下一步操作："
echo "1. 在GitHub上创建新仓库"
echo "2. 复制仓库URL"
echo "3. 运行以下命令连接远程仓库："
echo
echo "   git remote add origin https://github.com/YOUR_USERNAME/excel-data-processor.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo
echo "4. 推送完成后，GitHub Actions将自动开始构建Windows exe文件"
echo "5. 在GitHub仓库的Actions标签页查看构建进度"
echo "6. 构建完成后在Artifacts中下载exe文件"
echo

# 显示仓库状态
echo "📊 当前仓库状态："
git status --short
echo
echo "📋 文件统计："
echo "Python文件: $(find . -name "*.py" | wc -l)"
echo "文档文件: $(find . -name "*.md" | wc -l)"
echo "配置文件: $(find . -name "*.yml" -o -name "*.yaml" -o -name "*.json" -o -name "*.txt" | wc -l)"
echo
echo "🎉 GitHub仓库设置完成！"