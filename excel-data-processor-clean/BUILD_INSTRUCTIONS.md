# Excel Data Processor 打包说明

本文档说明如何将Python应用程序打包成可执行文件。

## 系统要求

- Python 3.8 或更高版本
- pip 包管理器
- 足够的磁盘空间（约500MB用于依赖和构建）

## 快速开始

### Windows 用户

1. 打开命令提示符（cmd）或PowerShell
2. 导航到项目目录
3. 运行构建脚本：
   ```cmd
   build.bat
   ```

### macOS/Linux 用户

1. 打开终端
2. 导航到项目目录
3. 运行构建脚本：
   ```bash
   chmod +x build.sh
   ./build.sh
   ```

### 手动构建

如果自动脚本不工作，可以手动执行以下步骤：

1. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

2. **清理旧文件**（可选）：
   ```bash
   # Windows
   rmdir /s build dist
   del *.spec
   
   # macOS/Linux
   rm -rf build dist *.spec
   ```

3. **构建可执行文件**：
   ```bash
   pyinstaller excel_processor.spec
   ```

## 构建选项说明

### 使用spec文件（推荐）

项目包含预配置的 `excel_processor.spec` 文件，包含以下优化：

- **单文件打包**：生成单个可执行文件
- **无控制台窗口**：GUI应用程序模式
- **依赖优化**：排除不必要的模块以减小文件大小
- **隐藏导入**：确保所有必要的模块被包含

### 命令行选项

如果不使用spec文件，可以使用以下命令：

```bash
pyinstaller --onefile --windowed --name=ExcelDataProcessor \
    --hidden-import=PySide6.QtCore \
    --hidden-import=PySide6.QtWidgets \
    --hidden-import=PySide6.QtGui \
    --hidden-import=pandas \
    --hidden-import=openpyxl \
    run.py
```

参数说明：
- `--onefile`: 打包成单个exe文件
- `--windowed`: 不显示控制台窗口
- `--name`: 指定可执行文件名称
- `--hidden-import`: 确保特定模块被包含
- `--icon`: 指定图标文件（可选）

## 输出文件

构建成功后，可执行文件将位于：
- Windows: `dist/ExcelDataProcessor.exe`
- macOS/Linux: `dist/ExcelDataProcessor`

## 文件大小优化

生成的可执行文件可能较大（100-200MB），这是正常的，因为它包含了：
- Python解释器
- PySide6 GUI框架
- pandas数据处理库
- 其他依赖库

### 减小文件大小的方法

1. **使用虚拟环境**：
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   pyinstaller excel_processor.spec
   ```

2. **排除不必要的模块**：
   在spec文件中的 `excludes` 列表中添加不需要的模块。

3. **使用UPX压缩**（已在spec中启用）：
   可以进一步减小文件大小，但可能影响启动速度。

## 分发说明

### 单文件分发
- 优点：只需分发一个exe文件
- 缺点：首次启动较慢（需要解压）

### 目录分发
如果需要更快的启动速度，可以修改spec文件，将 `onefile=False`：

```python
exe = EXE(
    pyz,
    a.scripts,
    [],  # 不包含 a.binaries, a.zipfiles, a.datas
    exclude_binaries=True,
    name='ExcelDataProcessor',
    # ... 其他选项
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ExcelDataProcessor'
)
```

## 故障排除

### 常见问题

1. **ModuleNotFoundError**：
   - 在spec文件的 `hiddenimports` 中添加缺失的模块

2. **文件过大**：
   - 使用虚拟环境
   - 排除不必要的模块
   - 启用UPX压缩

3. **启动缓慢**：
   - 考虑使用目录分发而不是单文件
   - 这是正常现象，特别是首次运行

4. **权限问题**：
   - 确保有写入dist目录的权限
   - 在某些系统上可能需要管理员权限

### 调试模式

如果遇到问题，可以启用调试模式：

```bash
pyinstaller --debug=all excel_processor.spec
```

这将显示详细的调试信息。

## 测试

构建完成后，建议进行以下测试：

1. **基本功能测试**：
   - 启动应用程序
   - 导入Excel/CSV文件
   - 选择字段
   - 添加自定义字段
   - 生成输出文件

2. **不同环境测试**：
   - 在没有安装Python的机器上测试
   - 测试不同的操作系统版本

3. **性能测试**：
   - 测试大文件处理
   - 测试启动时间

## 自动化构建

可以将构建过程集成到CI/CD流水线中：

```yaml
# GitHub Actions 示例
name: Build Executable
on: [push, pull_request]
jobs:
  build:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Build executable
      run: pyinstaller excel_processor.spec
    - name: Upload artifact
      uses: actions/upload-artifact@v2
      with:
        name: ExcelDataProcessor
        path: dist/
```

## 许可证和分发

确保在分发可执行文件时遵守所有依赖库的许可证要求。主要依赖库的许可证：

- PySide6: LGPL
- pandas: BSD
- openpyxl: MIT

建议在分发时包含一个LICENSE文件，说明所使用的开源库及其许可证。