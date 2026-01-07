# Excel Data Processor - Windows构建指南

## 🎯 目标

本指南将帮助您在Windows系统上构建Excel Data Processor的exe可执行文件。

## 📋 前置要求

### 系统要求
- **操作系统**: Windows 7/8/10/11 (推荐64位)
- **内存**: 至少4GB RAM
- **磁盘空间**: 至少2GB可用空间
- **网络**: 用于下载依赖包

### 软件要求
- **Python 3.8+**: [下载地址](https://www.python.org/downloads/)
- **Git** (可选): 用于获取源代码

## 🚀 快速开始

### 方法1: 使用批处理文件（推荐）

1. **获取项目文件**
   - 将所有项目文件复制到Windows系统
   - 确保包含所有源代码和构建脚本

2. **运行构建**
   ```cmd
   # 双击运行
   build_windows.bat
   
   # 或在命令行中运行
   build_windows.bat
   ```

3. **等待完成**
   - 构建过程需要5-15分钟
   - 会自动下载和安装依赖

4. **获取结果**
   - exe文件: `dist\ExcelDataProcessor.exe`
   - 分发包: `ExcelDataProcessor_Windows_Distribution\`

### 方法2: 使用Python脚本

```cmd
# 打开命令提示符或PowerShell
cd path\to\project

# 运行构建脚本
python build_exe_windows.py
```

### 方法3: 手动构建

```cmd
# 1. 安装依赖
pip install -r requirements.txt

# 2. 安装PyInstaller
pip install pyinstaller

# 3. 构建exe
pyinstaller excel_processor_windows.spec

# 4. 查看结果
dir dist\
```

## 📁 输出文件

构建成功后，您将得到：

```
dist\
└── ExcelDataProcessor.exe          # 主要可执行文件

ExcelDataProcessor_Windows_Distribution\
├── ExcelDataProcessor.exe          # 可执行文件
└── README.txt                      # 使用说明
```

## 🔧 详细步骤

### 步骤1: 准备Python环境

1. **下载Python**
   - 访问 https://www.python.org/downloads/
   - 下载Python 3.8或更高版本
   - **重要**: 安装时勾选"Add Python to PATH"

2. **验证安装**
   ```cmd
   python --version
   pip --version
   ```

### 步骤2: 准备项目文件

确保您有以下文件：
```
项目根目录\
├── src\                           # 源代码目录
├── run.py                         # 启动文件
├── requirements.txt               # 依赖列表
├── build_exe_windows.py          # Windows构建脚本
├── build_windows.bat             # 批处理构建脚本
├── excel_processor_windows.spec  # PyInstaller配置
└── create_icon.py                # 图标创建脚本
```

### 步骤3: 执行构建

选择以下任一方法：

**方法A: 双击批处理文件**
- 双击 `build_windows.bat`
- 按照提示操作

**方法B: 命令行执行**
```cmd
# 打开命令提示符
# 导航到项目目录
cd C:\path\to\your\project

# 执行构建
python build_exe_windows.py
```

### 步骤4: 验证结果

1. **检查文件**
   ```cmd
   dir dist\ExcelDataProcessor.exe
   ```

2. **测试运行**
   ```cmd
   dist\ExcelDataProcessor.exe
   ```

3. **检查功能**
   - 应用程序能正常启动
   - 界面显示正常
   - 能导入Excel/CSV文件

## 🛠️ 故障排除

### 常见问题

#### 1. Python未找到
**错误**: `'python' 不是内部或外部命令`

**解决方案**:
- 重新安装Python，确保勾选"Add Python to PATH"
- 或手动添加Python到系统PATH

#### 2. 依赖安装失败
**错误**: `pip install` 失败

**解决方案**:
```cmd
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### 3. PyInstaller构建失败
**错误**: 构建过程中出现错误

**解决方案**:
```cmd
# 清理缓存
pip cache purge

# 重新安装PyInstaller
pip uninstall pyinstaller
pip install pyinstaller

# 手动构建
pyinstaller --clean excel_processor_windows.spec
```

#### 4. exe文件过大
**问题**: 生成的exe文件超过200MB

**解决方案**:
- 这是正常现象，包含了所有依赖
- 可以使用UPX压缩（已在配置中启用）
- 考虑使用目录分发而非单文件

#### 5. 运行时错误
**错误**: exe文件无法启动或崩溃

**解决方案**:
```cmd
# 在命令行中运行查看错误信息
dist\ExcelDataProcessor.exe

# 或构建调试版本
pyinstaller --debug=all excel_processor_windows.spec
```

### 高级故障排除

#### 启用详细日志
```cmd
# 构建时启用详细输出
pyinstaller --log-level DEBUG excel_processor_windows.spec
```

#### 检查依赖
```cmd
# 列出已安装的包
pip list

# 检查特定包
pip show PySide6 pandas openpyxl
```

#### 测试最小环境
```cmd
# 创建虚拟环境测试
python -m venv test_env
test_env\Scripts\activate
pip install -r requirements.txt
python run.py
```

## 📊 性能优化

### 减小文件大小

1. **排除不必要的模块**
   - 编辑 `excel_processor_windows.spec`
   - 在 `excludes` 列表中添加不需要的模块

2. **使用UPX压缩**
   ```python
   # 在spec文件中
   upx=True,
   upx_exclude=[],
   ```

3. **虚拟环境构建**
   ```cmd
   # 使用干净的虚拟环境
   python -m venv build_env
   build_env\Scripts\activate
   pip install -r requirements.txt
   pyinstaller excel_processor_windows.spec
   ```

### 提高启动速度

1. **目录分发**
   - 修改spec文件使用目录分发
   - 启动更快但文件更多

2. **预编译**
   ```cmd
   # 预编译Python文件
   python -m compileall src\
   ```

## 🚀 自动化构建

### 批处理脚本增强

创建 `auto_build.bat`:
```batch
@echo off
echo 开始自动构建...

REM 清理旧文件
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

REM 构建
python build_exe_windows.py

REM 测试
if exist dist\ExcelDataProcessor.exe (
    echo 构建成功！
    echo 正在测试...
    timeout /t 2 /nobreak >nul
    start dist\ExcelDataProcessor.exe
) else (
    echo 构建失败！
)

pause
```

### PowerShell脚本

创建 `Build.ps1`:
```powershell
# Excel Data Processor 构建脚本
Write-Host "开始构建 Excel Data Processor..." -ForegroundColor Green

# 检查Python
try {
    $pythonVersion = python --version
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python未安装或未添加到PATH" -ForegroundColor Red
    exit 1
}

# 执行构建
try {
    python build_exe_windows.py
    Write-Host "✅ 构建完成" -ForegroundColor Green
} catch {
    Write-Host "❌ 构建失败" -ForegroundColor Red
    exit 1
}

# 检查结果
if (Test-Path "dist\ExcelDataProcessor.exe") {
    $size = (Get-Item "dist\ExcelDataProcessor.exe").Length / 1MB
    Write-Host "📁 文件大小: $([math]::Round($size, 1)) MB" -ForegroundColor Cyan
    
    # 询问是否测试运行
    $test = Read-Host "是否测试运行? (y/n)"
    if ($test -eq "y" -or $test -eq "Y") {
        Start-Process "dist\ExcelDataProcessor.exe"
    }
} else {
    Write-Host "❌ 未找到输出文件" -ForegroundColor Red
}

Read-Host "按Enter键退出"
```

## 📦 分发准备

### 创建安装包

使用NSIS或Inno Setup创建Windows安装程序：

1. **下载NSIS**: https://nsis.sourceforge.io/
2. **创建安装脚本**
3. **生成安装程序**

### 数字签名

为了避免Windows安全警告：

1. **获取代码签名证书**
2. **使用signtool签名**
   ```cmd
   signtool sign /f certificate.p12 /p password dist\ExcelDataProcessor.exe
   ```

### 病毒扫描

在分发前进行病毒扫描：
- 使用VirusTotal在线扫描
- 本地杀毒软件扫描

## 📋 检查清单

构建完成后，请检查：

- [ ] exe文件能正常启动
- [ ] 界面显示正确
- [ ] 能导入Excel文件
- [ ] 能导入CSV文件
- [ ] 字段选择功能正常
- [ ] 自定义字段功能正常
- [ ] 数据预览正确
- [ ] 能生成输出文件
- [ ] 文件大小合理（<200MB）
- [ ] 在不同Windows版本上测试

## 🎯 下一步

1. **测试**: 在多个Windows系统上测试
2. **优化**: 根据反馈优化性能
3. **分发**: 创建安装包或直接分发
4. **维护**: 建立更新机制

---

**最后更新**: 2025年1月7日
**适用版本**: Excel Data Processor v1.0
**支持系统**: Windows 7/8/10/11