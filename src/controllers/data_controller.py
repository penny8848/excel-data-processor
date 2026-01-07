"""
数据控制器，管理数据处理逻辑
"""
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
from PySide6.QtCore import QObject, Signal

from ..services.data_service import DataService, DataValidationError, FileReadError
from ..models.data_model import (
    DataConfiguration, CustomField, FieldSelection, 
    FieldType, ProcessingResult
)


class DataController(QObject):
    """数据控制器，协调数据服务和数据模型"""
    
    # 信号定义
    file_loaded = Signal(str)  # 文件加载完成
    headers_updated = Signal(list)  # 表头更新
    configuration_changed = Signal()  # 配置变更
    preview_updated = Signal(object)  # 预览数据更新，传递DataFrame
    processing_completed = Signal(object)  # 处理完成，传递ProcessingResult
    error_occurred = Signal(str)  # 错误发生
    
    def __init__(self):
        super().__init__()
        
        # 初始化服务和模型
        self.data_service = DataService()
        self.configuration = DataConfiguration()
        
        # 连接数据服务的信号
        self._connect_data_service_signals()
    
    def _connect_data_service_signals(self) -> None:
        """连接数据服务的信号"""
        self.data_service.file_loaded.connect(self._on_file_loaded)
        self.data_service.headers_parsed.connect(self._on_headers_parsed)
        self.data_service.error_occurred.connect(self.error_occurred)
    
    def load_file(self, file_path: str) -> bool:
        """
        加载文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否加载成功
        """
        try:
            success = self.data_service.load_file(file_path)
            if success:
                # 更新配置中的文件路径
                self.configuration.file_path = file_path
            return success
        except Exception as e:
            self.error_occurred.emit(f"加载文件失败: {str(e)}")
            return False
    
    def _on_file_loaded(self, file_path: str) -> None:
        """处理文件加载完成事件"""
        self.file_loaded.emit(file_path)
    
    def _on_headers_parsed(self, headers: List[str]) -> None:
        """处理表头解析完成事件"""
        # 更新配置中的原始表头
        self.configuration.original_headers = headers.copy()
        
        # 清除之前的字段选择，重新初始化
        self.configuration.field_selections.clear()
        
        # 为每个原始字段创建选择项（默认全选）
        for header in headers:
            self.configuration.add_original_field(header, selected=True)
        
        # 发出信号
        self.headers_updated.emit(headers)
        self.configuration_changed.emit()
        
        # 更新预览
        self._update_preview()
    
    def get_headers(self) -> List[str]:
        """获取当前表头"""
        return self.data_service.get_headers()
    
    def get_data_info(self) -> Dict[str, Any]:
        """获取数据信息"""
        return self.data_service.get_data_info()
    
    def set_field_selection(self, field_name: str, selected: bool) -> bool:
        """
        设置字段选择状态
        
        Args:
            field_name: 字段名称
            selected: 是否选中
            
        Returns:
            bool: 设置是否成功
        """
        success = self.configuration.set_field_selection(field_name, selected)
        if success:
            self.configuration_changed.emit()
            self._update_preview()
        return success
    
    def add_custom_field(self, custom_field: CustomField) -> bool:
        """
        添加自定义字段
        
        Args:
            custom_field: 自定义字段
            
        Returns:
            bool: 添加是否成功
        """
        try:
            self.configuration.add_custom_field(custom_field, selected=True)
            self.configuration_changed.emit()
            self._update_preview()
            return True
        except ValueError as e:
            self.error_occurred.emit(str(e))
            return False
    
    def remove_custom_field(self, field_name: str) -> bool:
        """
        移除自定义字段
        
        Args:
            field_name: 字段名称
            
        Returns:
            bool: 移除是否成功
        """
        success = self.configuration.remove_custom_field(field_name)
        if success:
            self.configuration_changed.emit()
            self._update_preview()
        return success
    
    def get_field_selections(self) -> List[FieldSelection]:
        """获取字段选择列表"""
        return self.configuration.field_selections.copy()
    
    def get_selected_field_names(self) -> List[str]:
        """获取选中的字段名称列表"""
        return self.configuration.get_all_selected_field_names()
    
    def _update_preview(self) -> None:
        """更新预览数据"""
        try:
            preview_data = self.generate_preview_data()
            self.preview_updated.emit(preview_data)
        except Exception as e:
            self.error_occurred.emit(f"更新预览失败: {str(e)}")
    
    def generate_preview_data(self, rows: int = 5) -> Optional[pd.DataFrame]:
        """
        生成预览数据
        
        Args:
            rows: 预览行数
            
        Returns:
            Optional[pd.DataFrame]: 预览数据
        """
        if not self.data_service.has_data():
            return None
        
        # 获取原始数据
        original_data = self.data_service.get_data_preview(rows)
        if original_data is None:
            return None
        
        # 获取选中的原始字段
        selected_original_fields = self.configuration.get_selected_original_fields()
        
        # 创建结果DataFrame
        if selected_original_fields:
            # 过滤选中的原始字段
            result_data = original_data[selected_original_fields].copy()
        else:
            # 如果没有选中原始字段，创建空DataFrame
            result_data = pd.DataFrame(index=original_data.index)
        
        # 添加自定义字段
        selected_custom_fields = self.configuration.get_selected_custom_fields()
        for custom_field in selected_custom_fields:
            # 根据字段类型生成默认值
            if custom_field.field_type == "number":
                try:
                    default_value = float(custom_field.default_value) if custom_field.default_value else 0.0
                except ValueError:
                    default_value = 0.0
            else:
                default_value = custom_field.default_value
            
            # 添加列
            result_data[custom_field.name] = default_value
        
        return result_data
    
    def process_data(self, output_file_path: str) -> ProcessingResult:
        """
        处理数据并输出到文件
        
        Args:
            output_file_path: 输出文件路径
            
        Returns:
            ProcessingResult: 处理结果
        """
        try:
            # 检查是否有数据
            if not self.data_service.has_data():
                return ProcessingResult(
                    success=False,
                    error_message="没有可处理的数据"
                )
            
            # 获取完整数据
            full_data = self.data_service.get_full_data()
            if full_data is None:
                return ProcessingResult(
                    success=False,
                    error_message="无法获取数据"
                )
            
            # 获取选中的原始字段
            selected_original_fields = self.configuration.get_selected_original_fields()
            
            # 创建结果DataFrame
            if selected_original_fields:
                result_data = full_data[selected_original_fields].copy()
            else:
                result_data = pd.DataFrame(index=full_data.index)
            
            # 添加自定义字段
            selected_custom_fields = self.configuration.get_selected_custom_fields()
            warnings = []
            
            for custom_field in selected_custom_fields:
                try:
                    # 根据字段类型处理默认值
                    if custom_field.field_type == "number":
                        try:
                            default_value = float(custom_field.default_value) if custom_field.default_value else 0.0
                        except ValueError:
                            default_value = 0.0
                            warnings.append(f"自定义字段 '{custom_field.name}' 的默认值无法转换为数字，使用0")
                    else:
                        default_value = custom_field.default_value
                    
                    # 添加列
                    result_data[custom_field.name] = default_value
                    
                except Exception as e:
                    warnings.append(f"处理自定义字段 '{custom_field.name}' 时出错: {str(e)}")
            
            # 保存到文件
            output_path = Path(output_file_path)
            if output_path.suffix.lower() == '.csv':
                result_data.to_csv(output_file_path, index=False, encoding='utf-8-sig')
            else:
                result_data.to_excel(output_file_path, index=False)
            
            # 创建处理结果
            result = ProcessingResult(
                success=True,
                output_file_path=output_file_path,
                processed_rows=len(result_data),
                warnings=warnings
            )
            
            self.processing_completed.emit(result)
            return result
            
        except Exception as e:
            result = ProcessingResult(
                success=False,
                error_message=f"处理数据时发生错误: {str(e)}"
            )
            self.processing_completed.emit(result)
            return result
    
    def clear_data(self) -> None:
        """清除所有数据"""
        self.data_service.clear_data()
        self.configuration.clear()
        self.configuration_changed.emit()
        self.preview_updated.emit(None)
    
    def has_data(self) -> bool:
        """检查是否有数据"""
        return self.data_service.has_data()
    
    def get_configuration(self) -> DataConfiguration:
        """获取当前配置"""
        return self.configuration
    
    def set_configuration(self, config: DataConfiguration) -> None:
        """设置配置"""
        self.configuration = config
        self.configuration_changed.emit()
        self._update_preview()