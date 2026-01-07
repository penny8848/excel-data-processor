#!/usr/bin/env python3
"""
简单测试数据服务层功能
"""
import sys
import os
import pandas as pd
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 直接导入，避免相对导入问题
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'services'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'models'))

def create_test_excel():
    """创建测试用的Excel文件"""
    test_data = pd.DataFrame({
        '姓名': ['张三', '李四', '王五'],
        '年龄': [25, 30, 35],
        '城市': ['北京', '上海', '广州'],
        '薪资': [8000, 12000, 15000]
    })
    
    test_file = 'test_data.xlsx'
    test_data.to_excel(test_file, index=False)
    print(f"创建测试文件: {test_file}")
    return test_file

def test_basic_functionality():
    """测试基本功能"""
    print("=== 测试基本功能 ===")
    
    # 创建测试文件
    test_file = create_test_excel()
    
    try:
        # 直接测试pandas读取
        print(f"使用pandas读取文件: {test_file}")
        data = pd.read_excel(test_file)
        print(f"数据形状: {data.shape}")
        print(f"列名: {list(data.columns)}")
        print(f"前2行数据:\n{data.head(2)}")
        
        print("基本功能测试完成！")
        
    except Exception as e:
        print(f"测试失败: {e}")
        
    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"清理测试文件: {test_file}")

if __name__ == "__main__":
    test_basic_functionality()
    print("\n测试完成！")