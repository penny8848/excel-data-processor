# Excel Data Processor 部署指南

## 构建可执行文件

### 方法一：使用自动化脚本（推荐）

#### Windows
```cmd
# 运行构建脚本
python build_exe.py

# 或使用批处理文件
build.bat
```

#### macOS/Linux
```bash
# 设置执行权限并运行
chmod +x build.sh
./build.sh

# 或直接使用Python脚本
python3 build_exe.py
```

### 方法二：手动构建

1. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

2. **构建可执行文件**：
   ```bash
   pyinstaller excel_processor.spec
   ```

## 构建输出

成功构建后，你将得到：
- `dist/ExcelDataProcessor.exe` (Windows)
- `dist/ExcelDataProcessor` (macOS/Linux)

## 文件大小和性能

- **预期文件大小**: 100-200 MB
- **首次启动时间**: 5-15 秒（需要解压）
- **后续启动时间**: 2-5 秒
- **内存使用**: 50-100 MB

## 系统要求

### 最低要求
- **操作系统**: Windows 7/8/10/11, macOS 10.14+, Linux (Ubuntu 18.04+)
- **内存**: 2 GB RAM
- **磁盘空间**: 500 MB 可用空间
- **处理器**: x64 架构

### 推荐配置
- **内存**: 4 GB RAM 或更多
- **磁盘空间**: 1 GB 可用空间
- **处理器**: 多核处理器

## 分发选项

### 选项1：单文件分发（默认）
- **优点**: 只需分发一个exe文件
- **缺点**: 首次启动较慢
- **适用**: 简单分发，用户不频繁使用

### 选项2：目录分发
修改 `excel_processor.spec` 文件：
```python
# 将 onefile 改为 False
exe = EXE(
    pyz,
    a.scripts,
    [],  # 移除 a.binaries, a.zipfiles, a.datas
    exclude_binaries=True,
    # ... 其他配置
)

# 添加 COLLECT
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

- **优点**: 启动速度快
- **缺点**: 需要分发整个目录
- **适用**: 频繁使用，性能要求高

## 测试部署

### 自动测试
```bash
python test_build.py
```

### 手动测试清单

1. **基本功能测试**：
   - [ ] 应用程序能正常启动
   - [ ] 界面显示正常
   - [ ] 能够导入Excel文件
   - [ ] 能够导入CSV文件
   - [ ] 字段选择功能正常
   - [ ] 自定义字段功能正常
   - [ ] 能够生成输出文件

2. **兼容性测试**：
   - [ ] 在目标操作系统上运行
   - [ ] 在没有Python的机器上运行
   - [ ] 处理不同格式的Excel文件
   - [ ] 处理不同编码的CSV文件

3. **性能测试**：
   - [ ] 处理大文件（>10MB）
   - [ ] 处理大量字段（>50列）
   - [ ] 处理大量行数（>10000行）

## 常见问题解决

### 构建问题

1. **ModuleNotFoundError**：
   ```bash
   # 在 excel_processor.spec 的 hiddenimports 中添加缺失模块
   hiddenimports=[
       'PySide6.QtCore',
       'PySide6.QtWidgets',
       'PySide6.QtGui',
       'pandas',
       'openpyxl',
       'missing_module_name',  # 添加这里
   ],
   ```

2. **文件过大**：
   ```bash
   # 使用虚拟环境减小大小
   python -m venv build_env
   build_env\Scripts\activate  # Windows
   source build_env/bin/activate  # macOS/Linux
   pip install -r requirements.txt
   pyinstaller excel_processor.spec
   ```

3. **UPX压缩错误**：
   ```python
   # 在 spec 文件中禁用 UPX
   upx=False,
   ```

### 运行时问题

1. **启动缓慢**：
   - 这是正常现象，特别是首次运行
   - 考虑使用目录分发

2. **权限错误**：
   - 确保用户有执行权限
   - 在某些系统上可能需要管理员权限

3. **缺少DLL**：
   - 安装 Microsoft Visual C++ Redistributable
   - 使用 `--collect-all` 选项重新构建

## 高级配置

### 自定义图标
1. 准备 ICO 格式图标文件
2. 将其命名为 `icon.ico` 放在项目根目录
3. 重新构建

### 添加版本信息
创建 `version.txt` 文件：
```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [StringStruct(u'CompanyName', u'Your Company'),
           StringStruct(u'FileDescription', u'Excel Data Processor'),
           StringStruct(u'FileVersion', u'1.0.0.0'),
           StringStruct(u'InternalName', u'ExcelDataProcessor'),
           StringStruct(u'LegalCopyright', u'Copyright (C) 2024'),
           StringStruct(u'OriginalFilename', u'ExcelDataProcessor.exe'),
           StringStruct(u'ProductName', u'Excel Data Processor'),
           StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

在 spec 文件中添加：
```python
exe = EXE(
    # ... 其他参数
    version='version.txt',
    # ... 其他参数
)
```

## 持续集成

### GitHub Actions 示例
创建 `.github/workflows/build.yml`：
```yaml
name: Build Executable

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Build executable
      run: python build_exe.py
    
    - name: Test executable
      run: python test_build.py
    
    - name: Upload artifact
      uses: actions/upload-artifact@v3
      with:
        name: ExcelDataProcessor-Windows
        path: dist/ExcelDataProcessor.exe

  build-macos:
    runs-on: macos-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Build executable
      run: python3 build_exe.py
    
    - name: Upload artifact
      uses: actions/upload-artifact@v3
      with:
        name: ExcelDataProcessor-macOS
        path: dist/ExcelDataProcessor
```

## 许可证合规

确保在分发时包含所有必要的许可证文件：

1. 创建 `LICENSES` 目录
2. 包含所有依赖库的许可证
3. 创建总体许可证文件

主要依赖库许可证：
- **PySide6**: LGPL v3
- **pandas**: BSD 3-Clause
- **openpyxl**: MIT
- **PyInstaller**: GPL v2 (仅构建时)

## 支持和维护

### 日志记录
在生产版本中启用日志：
```python
import logging
logging.basicConfig(
    filename='excel_processor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### 错误报告
考虑集成错误报告系统，如 Sentry 或自定义错误收集。

### 更新机制
考虑实现自动更新功能或提供更新检查。