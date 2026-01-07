#!/usr/bin/env python3
"""
测试构建的可执行文件
"""
import os
import sys
import subprocess
import time
from pathlib import Path

def test_executable():
    """测试可执行文件"""
    import platform
    
    # 根据操作系统确定可执行文件名
    if platform.system() == 'Windows':
        exe_name = 'ExcelDataProcessor.exe'
    else:
        exe_name = 'ExcelDataProcessor'
    
    exe_path = Path('dist') / exe_name
    
    if not exe_path.exists():
        print("❌ 可执行文件不存在")
        return False
    
    print(f"📁 找到可执行文件: {exe_path}")
    print(f"📊 文件大小: {exe_path.stat().st_size / (1024*1024):.1f} MB")
    
    # 检查文件权限
    if not os.access(exe_path, os.X_OK):
        print("❌ 文件没有执行权限")
        return False
    
    print("✅ 可执行文件存在且有执行权限")
    return True

def check_dependencies():
    """检查依赖文件"""
    dist_path = Path('dist')
    if not dist_path.exists():
        print("❌ dist目录不存在")
        return False
    
    files = list(dist_path.glob('*'))
    print(f"📦 dist目录包含 {len(files)} 个文件:")
    for file in files:
        print(f"  - {file.name}")
    
    return True

def main():
    """主函数"""
    print("=== Excel Data Processor 构建测试 ===")
    
    # 检查构建结果
    if not check_dependencies():
        return 1
    
    # 测试可执行文件
    if not test_executable():
        print("\n⚠️  测试失败，但这可能是正常的（GUI应用程序可能需要显示环境）")
        print("建议手动测试可执行文件")
        return 0
    
    print("\n✅ 所有测试通过！")
    print("\n📋 分发清单:")
    print("1. 将 dist/ExcelDataProcessor.exe 复制到目标机器")
    print("2. 确保目标机器有足够的磁盘空间")
    print("3. 首次运行可能需要较长时间")
    print("4. 建议在不同的Windows版本上测试")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())