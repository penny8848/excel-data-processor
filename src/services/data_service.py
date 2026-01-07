"""
数据服务层，负责文件读取、数据验证和处理
"""
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from PySide6.QtCore import QObject, Signal


class DataValidationError(Exception):
    """数据验证错误"""
    pass


class FileReadError(Exception):
    """文件读取错误"""
    pass


class DataService(QObject):
    """数据服务类，处理Excel/CSV文件的读取和验证"""
    
    # 信号定义
    file_loaded = Signal(str)  # 文件加载完成信号，传递文件路径
    data_validated = Signal(bool)  # 数据验证完成信号，传递验证结果
    headers_parsed = Signal(list)  # 表头解析完成信号，传递表头列表
    error_occurred = Signal(str)  # 错误发生信号，传递错误信息
    
    def __init__(self):
        super().__init__()
        self._current_data: Optional[pd.DataFrame] = None
        self._current_file_path: Optional[str] = None
        self._headers: List[str] = []
        
        # 支持的文件格式
        self.supported_formats = {'.xlsx', '.xls', '.csv'}
    
    def load_file(self, file_path: str) -> bool:
        """
        加载Excel或CSV文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 加载是否成功
            
        Raises:
            FileReadError: 文件读取失败时抛出
        """
        try:
            # 验证文件路径
            path = Path(file_path)
            if not path.exists():
                raise FileReadError(f"文件不存在: {file_path}")
            
            if not path.is_file():
                raise FileReadError(f"路径不是文件: {file_path}")
            
            # 检查文件格式
            file_extension = path.suffix.lower()
            if file_extension not in self.supported_formats:
                raise FileReadError(
                    f"不支持的文件格式: {file_extension}。"
                    f"支持的格式: {', '.join(self.supported_formats)}"
                )
            
            # 根据文件类型读取数据
            if file_extension in {'.xlsx', '.xls'}:
                self._current_data = pd.read_excel(file_path)
            elif file_extension == '.csv':
                # 尝试不同的编码格式
                encodings = ['utf-8', 'gbk', 'gb2312', 'latin1']
                for encoding in encodings:
                    try:
                        self._current_data = pd.read_csv(file_path, encoding=encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    raise FileReadError(f"无法解码CSV文件，尝试的编码: {', '.join(encodings)}")
            
            # 验证数据
            if not self._validate_data():
                return False
            
            # 解析表头
            self._parse_headers()
            
            # 保存文件路径
            self._current_file_path = file_path
            
            # 发出信号
            self.file_loaded.emit(file_path)
            self.data_validated.emit(True)
            self.headers_parsed.emit(self._headers)
            
            return True
            
        except (FileReadError, DataValidationError) as e:
            self.error_occurred.emit(str(e))
            return False
        except Exception as e:
            error_msg = f"读取文件时发生未知错误: {str(e)}"
            self.error_occurred.emit(error_msg)
            return False
    
    def _validate_data(self) -> bool:
        """
        验证加载的数据
        
        Returns:
            bool: 验证是否通过
            
        Raises:
            DataValidationError: 数据验证失败时抛出
        """
        if self._current_data is None:
            raise DataValidationError("没有数据需要验证")
        
        # 检查数据是否为空
        if self._current_data.empty:
            raise DataValidationError("文件中没有数据")
        
        # 检查是否有列
        if len(self._current_data.columns) == 0:
            raise DataValidationError("文件中没有列")
        
        # 检查数据行数
        if len(self._current_data) == 0:
            raise DataValidationError("文件中没有数据行")
        
        # 检查列名是否有重复
        duplicate_columns = self._current_data.columns[self._current_data.columns.duplicated()]
        if len(duplicate_columns) > 0:
            raise DataValidationError(f"发现重复的列名: {list(duplicate_columns)}")
        
        return True
    
    def _parse_headers(self) -> None:
        """解析表头信息"""
        if self._current_data is None:
            self._headers = []
            return
        
        # 获取列名并转换为字符串
        self._headers = [str(col) for col in self._current_data.columns]
        
        # 处理空列名
        for i, header in enumerate(self._headers):
            if header.startswith('Unnamed:') or header.strip() == '':
                self._headers[i] = f"列{i+1}"
    
    def get_headers(self) -> List[str]:
        """
        获取当前数据的表头列表
        
        Returns:
            List[str]: 表头列表
        """
        return self._headers.copy()
    
    def get_data_preview(self, rows: int = 5) -> Optional[pd.DataFrame]:
        """
        获取数据预览
        
        Args:
            rows: 预览行数，默认5行
            
        Returns:
            Optional[pd.DataFrame]: 预览数据，如果没有数据则返回None
        """
        if self._current_data is None:
            return None
        
        return self._current_data.head(rows)
    
    def get_full_data(self) -> Optional[pd.DataFrame]:
        """
        获取完整数据
        
        Returns:
            Optional[pd.DataFrame]: 完整数据，如果没有数据则返回None
        """
        if self._current_data is None:
            return None
        
        return self._current_data.copy()
    
    def get_data_info(self) -> Dict[str, Any]:
        """
        获取数据基本信息
        
        Returns:
            Dict[str, Any]: 数据信息字典
        """
        if self._current_data is None:
            return {
                'rows': 0,
                'columns': 0,
                'file_path': None,
                'headers': []
            }
        
        return {
            'rows': len(self._current_data),
            'columns': len(self._current_data.columns),
            'file_path': self._current_file_path,
            'headers': self._headers.copy()
        }
    
    def clear_data(self) -> None:
        """清除当前数据"""
        self._current_data = None
        self._current_file_path = None
        self._headers = []
    
    def has_data(self) -> bool:
        """
        检查是否有数据
        
        Returns:
            bool: 是否有数据
        """
        return self._current_data is not None and not self._current_data.empty