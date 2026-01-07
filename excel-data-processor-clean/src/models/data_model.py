"""
数据模型，定义数据结构和状态
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


class FieldType(Enum):
    """字段类型枚举"""
    ORIGINAL = "original"  # 原始字段
    CUSTOM = "custom"      # 自定义字段


@dataclass
class CustomField:
    """自定义字段模型"""
    name: str
    default_value: str = ""
    field_type: str = "text"  # text, number, date, formula
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'default_value': self.default_value,
            'field_type': self.field_type,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CustomField':
        """从字典创建实例"""
        return cls(
            name=data['name'],
            default_value=data.get('default_value', ''),
            field_type=data.get('field_type', 'text'),
            description=data.get('description', '')
        )


@dataclass
class FieldSelection:
    """字段选择模型"""
    field_name: str
    is_selected: bool = True
    field_type: FieldType = FieldType.ORIGINAL
    custom_field: Optional[CustomField] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {
            'field_name': self.field_name,
            'is_selected': self.is_selected,
            'field_type': self.field_type.value
        }
        if self.custom_field:
            result['custom_field'] = self.custom_field.to_dict()
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FieldSelection':
        """从字典创建实例"""
        custom_field = None
        if 'custom_field' in data and data['custom_field']:
            custom_field = CustomField.from_dict(data['custom_field'])
        
        return cls(
            field_name=data['field_name'],
            is_selected=data.get('is_selected', True),
            field_type=FieldType(data.get('field_type', 'original')),
            custom_field=custom_field
        )


@dataclass
class DataConfiguration:
    """数据配置模型，包含字段选择和自定义字段"""
    file_path: Optional[str] = None
    original_headers: List[str] = field(default_factory=list)
    field_selections: List[FieldSelection] = field(default_factory=list)
    custom_fields: List[CustomField] = field(default_factory=list)
    
    def get_selected_original_fields(self) -> List[str]:
        """获取选中的原始字段"""
        return [
            fs.field_name for fs in self.field_selections
            if fs.is_selected and fs.field_type == FieldType.ORIGINAL
        ]
    
    def get_selected_custom_fields(self) -> List[CustomField]:
        """获取选中的自定义字段"""
        return [
            fs.custom_field for fs in self.field_selections
            if fs.is_selected and fs.field_type == FieldType.CUSTOM and fs.custom_field
        ]
    
    def get_all_selected_field_names(self) -> List[str]:
        """获取所有选中字段的名称"""
        field_names = []
        for fs in self.field_selections:
            if fs.is_selected:
                if fs.field_type == FieldType.ORIGINAL:
                    field_names.append(fs.field_name)
                elif fs.field_type == FieldType.CUSTOM and fs.custom_field:
                    field_names.append(fs.custom_field.name)
        return field_names
    
    def add_original_field(self, field_name: str, selected: bool = True) -> None:
        """添加原始字段"""
        # 检查是否已存在
        for fs in self.field_selections:
            if fs.field_name == field_name and fs.field_type == FieldType.ORIGINAL:
                fs.is_selected = selected
                return
        
        # 添加新字段
        self.field_selections.append(
            FieldSelection(
                field_name=field_name,
                is_selected=selected,
                field_type=FieldType.ORIGINAL
            )
        )
    
    def add_custom_field(self, custom_field: CustomField, selected: bool = True) -> None:
        """添加自定义字段"""
        # 检查名称是否已存在
        if self.is_field_name_exists(custom_field.name):
            raise ValueError(f"字段名称 '{custom_field.name}' 已存在")
        
        # 添加到自定义字段列表
        self.custom_fields.append(custom_field)
        
        # 添加到字段选择列表
        self.field_selections.append(
            FieldSelection(
                field_name=custom_field.name,
                is_selected=selected,
                field_type=FieldType.CUSTOM,
                custom_field=custom_field
            )
        )
    
    def remove_custom_field(self, field_name: str) -> bool:
        """移除自定义字段"""
        # 从自定义字段列表中移除
        self.custom_fields = [cf for cf in self.custom_fields if cf.name != field_name]
        
        # 从字段选择列表中移除
        original_count = len(self.field_selections)
        self.field_selections = [
            fs for fs in self.field_selections
            if not (fs.field_name == field_name and fs.field_type == FieldType.CUSTOM)
        ]
        
        return len(self.field_selections) < original_count
    
    def is_field_name_exists(self, field_name: str) -> bool:
        """检查字段名称是否已存在"""
        # 检查原始字段
        if field_name in self.original_headers:
            return True
        
        # 检查自定义字段
        for cf in self.custom_fields:
            if cf.name == field_name:
                return True
        
        return False
    
    def set_field_selection(self, field_name: str, selected: bool) -> bool:
        """设置字段选择状态"""
        for fs in self.field_selections:
            if fs.field_name == field_name:
                fs.is_selected = selected
                return True
        return False
    
    def clear(self) -> None:
        """清除所有配置"""
        self.file_path = None
        self.original_headers.clear()
        self.field_selections.clear()
        self.custom_fields.clear()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典，用于序列化"""
        return {
            'file_path': self.file_path,
            'original_headers': self.original_headers.copy(),
            'field_selections': [fs.to_dict() for fs in self.field_selections],
            'custom_fields': [cf.to_dict() for cf in self.custom_fields]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DataConfiguration':
        """从字典创建实例，用于反序列化"""
        config = cls(
            file_path=data.get('file_path'),
            original_headers=data.get('original_headers', []).copy(),
        )
        
        # 恢复自定义字段
        for cf_data in data.get('custom_fields', []):
            config.custom_fields.append(CustomField.from_dict(cf_data))
        
        # 恢复字段选择
        for fs_data in data.get('field_selections', []):
            config.field_selections.append(FieldSelection.from_dict(fs_data))
        
        return config


@dataclass
class ProcessingResult:
    """数据处理结果模型"""
    success: bool
    output_file_path: Optional[str] = None
    processed_rows: int = 0
    error_message: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'success': self.success,
            'output_file_path': self.output_file_path,
            'processed_rows': self.processed_rows,
            'error_message': self.error_message,
            'warnings': self.warnings.copy()
        }