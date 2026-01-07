#!/usr/bin/env python3
"""
Windows专用构建脚本 - 构建exe可执行文件
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build_dirs():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"清理目录: {dir_name}")
    
    # 清理.spec文件（除了我们的配置文件）
    spec_files = [f for f in os.listdir('.') if f.endswith('.spec') and f != 'excel_processor_windows.spec']
    for spec_file in spec_files:
        os.remove(spec_file)
        print(f"清理文件: {spec_file}")

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("错误: 需要Python 3.8或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    print(f"✅ Python版本: {sys.version}")
    return True

def check_windows_system():
    """检查是否在Windows系统上"""
    import platform
    if platform.system() != 'Windows':
        print("警告: 当前不在Windows系统上，构建的exe可能无法在Windows上运行")
        return False
    print(f"✅ 操作系统: {platform.system()} {platform.release()}")
    return True

def install_dependencies():
    """安装依赖"""
    print("安装依赖包...")
    try:
        # 升级pip
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                      check=True)
        
        # 安装依赖
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("✅ 依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False

def check_dependencies():
    """检查必要的依赖"""
    required_packages = ['PySide6', 'pandas', 'openpyxl']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"缺少依赖包: {', '.join(missing_packages)}")
        return False
    return True

def create_windows_icon():
    """创建Windows图标"""
    if not os.path.exists('icon.ico'):
        print("创建Windows应用程序图标...")
        try:
            subprocess.run([sys.executable, 'create_icon.py'], check=True)
        except subprocess.CalledProcessError:
            print("图标创建失败，将使用默认图标")

def build_exe():
    """构建Windows exe文件"""
    print("开始构建Windows exe文件...")
    
    # 检查spec文件是否存在
    spec_file = 'excel_processor_windows.spec'
    if not os.path.exists(spec_file):
        print(f"创建Windows专用spec文件: {spec_file}")
        create_windows_spec_file()
    
    # 查找PyInstaller
    pyinstaller_cmd = find_pyinstaller()
    if not pyinstaller_cmd:
        print("❌ 未找到PyInstaller，尝试安装...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
            pyinstaller_cmd = find_pyinstaller()
        except subprocess.CalledProcessError:
            print("❌ PyInstaller安装失败")
            return False
    
    if not pyinstaller_cmd:
        print("❌ 无法找到或安装PyInstaller")
        return False
    
    print(f"✅ 使用PyInstaller: {pyinstaller_cmd}")
    
    try:
        # 构建exe
        result = subprocess.run([pyinstaller_cmd, spec_file], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ exe文件构建完成！")
            return True
        else:
            print("❌ 构建失败")
            print("错误输出:", result.stderr)
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return False

def find_pyinstaller():
    """查找PyInstaller命令"""
    commands = ['pyinstaller', 'pyinstaller.exe']
    
    for cmd in commands:
        try:
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return cmd
        except FileNotFoundError:
            continue
    
    return None

def create_windows_spec_file():
    """创建Windows专用的spec文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

# 项目根目录
project_root = Path.cwd()
src_path = project_root / 'src'

block_cipher = None

a = Analysis(
    ['run.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        # 添加src目录下的所有Python文件
        (str(src_path), 'src'),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtWidgets', 
        'PySide6.QtGui',
        'pandas',
        'openpyxl',
        'numpy',
        'xlsxwriter',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'IPython',
        'jupyter',
        'notebook',
        'tkinter',
        'PyQt5',
        'PyQt6',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ExcelDataProcessor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if Path('icon.ico').exists() else None,
)'''
    
    with open('excel_processor_windows.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)

def verify_build():
    """验证构建结果"""
    exe_path = os.path.join('dist', 'ExcelDataProcessor.exe')
    if os.path.exists(exe_path):
        file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
        print(f"\n🎉 构建成功！")
        print(f"📁 输出路径: {exe_path}")
        print(f"📊 文件大小: {file_size:.1f} MB")
        
        # 检查文件是否可执行
        if os.access(exe_path, os.X_OK):
            print("✅ 文件具有执行权限")
        else:
            print("⚠️  文件可能缺少执行权限")
        
        return True
    else:
        print("❌ 构建失败，未找到输出文件")
        return False

def create_distribution_package():
    """创建分发包"""
    if not os.path.exists('dist/ExcelDataProcessor.exe'):
        return False
    
    print("创建分发包...")
    
    # 创建分发目录
    dist_dir = 'ExcelDataProcessor_Windows_Distribution'
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)
    
    # 复制exe文件
    shutil.copy2('dist/ExcelDataProcessor.exe', 
                 os.path.join(dist_dir, 'ExcelDataProcessor.exe'))
    
    # 创建使用说明
    readme_content = """# Excel Data Processor - Windows版本

## 🚀 快速开始

双击 `ExcelDataProcessor.exe` 即可启动应用程序。

## 📋 功能特性

- ✅ 支持Excel (.xlsx, .xls) 和CSV文件导入
- ✅ 字段选择和管理
- ✅ 自定义字段添加
- ✅ 实时数据预览
- ✅ Excel文件输出
- ✅ 现代化GUI界面

## 🖥️ 系统要求

- Windows 7/8/10/11 (64位推荐)
- 至少 2GB 内存
- 至少 200MB 可用磁盘空间

## 🔧 故障排除

1. **应用程序无法启动**
   - 确保您的Windows系统是64位
   - 尝试以管理员身份运行

2. **安全警告**
   - Windows可能显示"未知发布者"警告
   - 点击"更多信息" -> "仍要运行"

3. **文件导入问题**
   - 确保Excel/CSV文件格式正确
   - 检查文件是否被其他程序占用

## 📞 技术支持

如遇问题，请检查：
- 文件格式是否正确
- 系统是否满足最低要求
- 是否有足够的磁盘空间

---
构建日期: """ + str(__import__('datetime').datetime.now().strftime('%Y年%m月%d日')) + """
版本: 1.0.0
"""
    
    with open(os.path.join(dist_dir, 'README.txt'), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ 分发包已创建: {dist_dir}/")
    return True

def main():
    """主函数"""
    print("=== Excel Data Processor Windows构建工具 ===")
    print()
    
    # 检查环境
    if not check_python_version():
        return 1
    
    check_windows_system()  # 警告但不阻止
    
    # 检查是否在正确的目录
    if not os.path.exists('run.py'):
        print("❌ 错误: 请在项目根目录运行此脚本")
        return 1
    
    # 清理构建目录
    clean_build_dirs()
    
    # 安装依赖
    if not install_dependencies():
        return 1
    
    # 检查依赖
    if not check_dependencies():
        print("❌ 请先安装所有依赖包")
        return 1
    
    # 创建图标
    create_windows_icon()
    
    # 构建exe
    if not build_exe():
        return 1
    
    # 验证构建结果
    if not verify_build():
        return 1
    
    # 创建分发包
    create_distribution_package()
    
    print(f"\n🎉 Windows exe构建完成！")
    print(f"\n📋 使用说明:")
    print(f"1. exe文件位于 dist/ 目录中")
    print(f"2. 分发包位于 ExcelDataProcessor_Windows_Distribution/ 目录中")
    print(f"3. 可以将整个分发包复制给其他用户")
    print(f"4. 双击 ExcelDataProcessor.exe 即可运行")
    print(f"5. 首次运行可能需要一些时间")
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        input("\n按Enter键退出...")
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n构建被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n构建过程中发生错误: {e}")
        input("按Enter键退出...")
        sys.exit(1)