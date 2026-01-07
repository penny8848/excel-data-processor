#!/usr/bin/env python3
"""
构建exe可执行文件的脚本
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
    spec_files = [f for f in os.listdir('.') if f.endswith('.spec') and f != 'excel_processor.spec']
    for spec_file in spec_files:
        os.remove(spec_file)
        print(f"清理文件: {spec_file}")

def check_dependencies():
    """检查必要的依赖"""
    required_packages = ['PySide6', 'pandas', 'openpyxl']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"缺少依赖包: {', '.join(missing_packages)}")
        return False
    return True

def install_dependencies():
    """安装依赖"""
    print("安装依赖包...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"依赖安装失败: {e}")
        return False

def create_icon():
    """创建图标"""
    if not os.path.exists('icon.ico'):
        print("创建应用程序图标...")
        try:
            subprocess.run([sys.executable, 'create_icon.py'], check=True)
        except subprocess.CalledProcessError:
            print("图标创建失败，将使用默认图标")

def build_exe():
    """构建exe文件"""
    print("开始构建exe文件...")
    
    # 检查spec文件是否存在
    if not os.path.exists('excel_processor.spec'):
        print("错误: 未找到 excel_processor.spec 文件")
        return False
    
    # 尝试不同的PyInstaller路径
    pyinstaller_paths = [
        'pyinstaller',
        os.path.expanduser('~/Library/Python/3.9/bin/pyinstaller'),
        '/usr/local/bin/pyinstaller'
    ]
    
    pyinstaller_cmd = None
    for path in pyinstaller_paths:
        try:
            subprocess.run([path, '--version'], check=True, capture_output=True)
            pyinstaller_cmd = path
            print(f"找到PyInstaller: {path}")
            break
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    if not pyinstaller_cmd:
        print("错误: 未找到PyInstaller命令")
        return False
    
    try:
        subprocess.run([pyinstaller_cmd, 'excel_processor.spec'], check=True)
        print("exe文件构建完成！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False

def verify_build():
    """验证构建结果"""
    # 根据操作系统确定可执行文件名
    import platform
    if platform.system() == 'Windows':
        exe_name = 'ExcelDataProcessor.exe'
    else:
        exe_name = 'ExcelDataProcessor'
    
    exe_path = os.path.join('dist', exe_name)
    if os.path.exists(exe_path):
        file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
        print(f"\n✅ 构建成功！")
        print(f"📁 输出路径: {exe_path}")
        print(f"📊 文件大小: {file_size:.1f} MB")
        return True
    else:
        print("❌ 构建失败，未找到输出文件")
        return False

def main():
    """主函数"""
    print("=== Excel Data Processor 打包工具 ===")
    
    # 检查是否在正确的目录
    if not os.path.exists('run.py'):
        print("错误: 请在项目根目录运行此脚本")
        return 1
    
    # 清理构建目录
    clean_build_dirs()
    
    # 安装依赖
    if not install_dependencies():
        return 1
    
    # 检查依赖
    if not check_dependencies():
        print("请先安装所有依赖包")
        return 1
    
    # 创建图标
    create_icon()
    
    # 构建exe
    if not build_exe():
        return 1
    
    # 验证构建结果
    if not verify_build():
        return 1
    
    print(f"\n使用说明:")
    print(f"1. 可执行文件位于 dist/ 目录中")
    print(f"2. 可以将 ExcelDataProcessor.exe 复制到任何位置运行")
    print(f"3. 首次运行可能需要一些时间来解压")
    print(f"4. 确保目标机器有足够的磁盘空间和内存")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())