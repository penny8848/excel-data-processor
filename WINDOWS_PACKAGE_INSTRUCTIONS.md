# Windows构建包使用说明

## 📦 包含文件

这个构建包包含了在Windows系统上构建exe文件的所有必要文件：

### 核心文件
- `src/` - 完整的Python源代码
- `run.py` - 应用程序入口文件
- `requirements.txt` - Python依赖列表

### 构建脚本
- `build_exe_windows.py` - Python构建脚本（推荐）
- `build_windows.bat` - 批处理构建脚本（一键运行）
- `excel_processor_windows.spec` - PyInstaller配置文件

### 辅助文件
- `create_icon.py` - 图标创建脚本
- `WINDOWS_BUILD_GUIDE.md` - 详细构建指南
- `README_WINDOWS.md` - Windows版本说明

## 🚀 三种构建方法

### 方法1: 一键构建（最简单）

1. **准备环境**
   - 在Windows系统上安装Python 3.8+
   - 下载地址: https://www.python.org/downloads/
   - ⚠️ 安装时务必勾选"Add Python to PATH"

2. **解压文件**
   - 将构建包解压到任意目录
   - 例如: `C:\ExcelDataProcessor\`

3. **一键构建**
   - 双击 `build_windows.bat` 文件
   - 等待自动完成（约5-15分钟）

4. **获取结果**
   - exe文件: `dist\ExcelDataProcessor.exe`
   - 分发包: `ExcelDataProcessor_Windows_Distribution\`

### 方法2: Python脚本构建

```cmd
# 1. 打开命令提示符
# 2. 导航到项目目录
cd C:\path\to\extracted\folder

# 3. 运行构建脚本
python build_exe_windows.py

# 4. 等待完成
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
dir dist\ExcelDataProcessor.exe
```

## 📋 构建要求

### 系统要求
- **操作系统**: Windows 7/8/10/11 (推荐64位)
- **Python**: 3.8或更高版本
- **内存**: 至少4GB RAM
- **磁盘**: 至少2GB可用空间
- **网络**: 用于下载Python包

### 软件准备
1. **安装Python**
   - 访问 https://www.python.org/downloads/
   - 下载最新的Python 3.x版本
   - 安装时勾选"Add Python to PATH"

2. **验证安装**
   ```cmd
   python --version
   pip --version
   ```

## 🎯 预期结果

构建成功后，您将得到：

```
📁 dist\
└── ExcelDataProcessor.exe (约100-150MB)

📁 ExcelDataProcessor_Windows_Distribution\
├── ExcelDataProcessor.exe
└── README.txt
```

### 文件特性
- **大小**: 约100-150MB（包含所有依赖）
- **类型**: Windows可执行文件
- **依赖**: 无需安装Python或其他软件
- **兼容**: Windows 7及以上版本

## 🔧 常见问题

### Q: Python命令不识别
**A**: 重新安装Python，确保勾选"Add Python to PATH"

### Q: 构建过程中断
**A**: 检查网络连接，重新运行构建脚本

### Q: exe文件很大
**A**: 这是正常的，包含了完整的Python环境和所有依赖

### Q: 杀毒软件报警
**A**: 这是误报，PyInstaller打包的文件常被误报

### Q: 构建失败
**A**: 查看错误信息，通常是依赖安装问题

## 📖 详细文档

- `WINDOWS_BUILD_GUIDE.md` - 完整的构建指南
- `README_WINDOWS.md` - Windows版本使用说明

## 🚀 分发说明

构建完成后：

1. **测试exe文件**
   - 双击运行 `ExcelDataProcessor.exe`
   - 测试基本功能

2. **准备分发**
   - 使用 `ExcelDataProcessor_Windows_Distribution` 文件夹
   - 包含exe文件和使用说明

3. **分发方式**
   - 压缩成zip文件分发
   - 或创建安装程序
   - 或直接复制exe文件

## ⚠️ 重要提醒

1. **首次运行较慢**: exe文件首次启动需要解压，约10-30秒
2. **安全警告**: Windows可能显示安全警告，选择"仍要运行"
3. **杀毒软件**: 可能被误报为病毒，添加到白名单
4. **系统兼容**: 在目标系统上测试运行

## 📞 技术支持

如果遇到问题：

1. **检查Python版本**: `python --version`
2. **检查依赖**: `pip list`
3. **查看错误日志**: 运行时的错误信息
4. **重新构建**: 清理后重新执行构建

---

**构建包版本**: 1.0  
**更新日期**: 2025年1月7日  
**支持系统**: Windows 7/8/10/11