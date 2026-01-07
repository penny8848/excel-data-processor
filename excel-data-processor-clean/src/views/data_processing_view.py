"""
数据处理主视图
"""
import pandas as pd
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLabel, QGroupBox,
                               QListWidget, QTableWidget, QSplitter,
                               QListWidgetItem, QTableWidgetItem,
                               QCheckBox, QFileDialog, QMessageBox,
                               QDialog, QLineEdit, QComboBox, QTextEdit,
                               QDialogButtonBox, QFormLayout)
from PySide6.QtCore import Signal, Qt
from typing import Optional, List

from ..models.data_model import CustomField, FieldSelection, FieldType


class DataProcessingView(QWidget):
    """数据处理主视图"""
    
    # 信号定义
    file_import_requested = Signal()
    field_selection_changed = Signal(list)
    custom_field_added = Signal(str, str)
    generate_requested = Signal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.apply_styles()
        self.connect_signals()
    
    def setup_ui(self) -> None:
        """创建UI组件和布局"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # 创建标题
        title_label = QLabel("数据处理")
        title_label.setObjectName("pageTitle")
        main_layout.addWidget(title_label)
        
        # 创建主要内容区域
        content_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(content_splitter)
        
        # 左侧控制面板
        left_panel = self.create_control_panel()
        content_splitter.addWidget(left_panel)
        
        # 右侧预览面板
        right_panel = self.create_preview_panel()
        content_splitter.addWidget(right_panel)
        
        # 设置分割器比例
        content_splitter.setStretchFactor(0, 1)
        content_splitter.setStretchFactor(1, 2)
        
        # 底部操作按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.generate_btn = QPushButton("生成Excel文件")
        self.generate_btn.setObjectName("primaryButton")
        self.generate_btn.setEnabled(False)  # 初始状态禁用
        button_layout.addWidget(self.generate_btn)
        
        main_layout.addLayout(button_layout)
    
    def create_control_panel(self) -> QWidget:
        """创建左侧控制面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 文件导入区域
        import_group = QGroupBox("文件导入")
        import_layout = QVBoxLayout(import_group)
        
        self.import_btn = QPushButton("选择Excel/CSV文件")
        self.import_btn.setObjectName("importButton")
        import_layout.addWidget(self.import_btn)
        
        self.file_info_label = QLabel("未选择文件")
        self.file_info_label.setObjectName("fileInfoLabel")
        import_layout.addWidget(self.file_info_label)
        
        layout.addWidget(import_group)
        
        # 字段选择区域
        fields_group = QGroupBox("字段选择")
        fields_layout = QVBoxLayout(fields_group)
        
        # 字段列表
        self.fields_list = QListWidget()
        self.fields_list.setObjectName("fieldsList")
        fields_layout.addWidget(self.fields_list)
        
        # 字段操作按钮
        field_buttons_layout = QHBoxLayout()
        self.select_all_btn = QPushButton("全选")
        self.select_all_btn.setEnabled(False)
        self.select_none_btn = QPushButton("全不选")
        self.select_none_btn.setEnabled(False)
        
        field_buttons_layout.addWidget(self.select_all_btn)
        field_buttons_layout.addWidget(self.select_none_btn)
        fields_layout.addLayout(field_buttons_layout)
        
        layout.addWidget(fields_group)
        
        # 自定义字段区域
        custom_group = QGroupBox("自定义字段")
        custom_layout = QVBoxLayout(custom_group)
        
        self.add_field_btn = QPushButton("添加新字段")
        self.add_field_btn.setEnabled(False)
        custom_layout.addWidget(self.add_field_btn)
        
        layout.addWidget(custom_group)
        
        # 添加弹性空间
        layout.addStretch()
        
        return panel
    
    def create_preview_panel(self) -> QWidget:
        """创建右侧预览面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 预览标题
        preview_label = QLabel("数据预览")
        preview_label.setObjectName("sectionTitle")
        layout.addWidget(preview_label)
        
        # 预览表格
        self.preview_table = QTableWidget()
        self.preview_table.setObjectName("previewTable")
        layout.addWidget(self.preview_table)
        
        # 预览信息
        self.preview_info_label = QLabel("请先导入数据文件")
        self.preview_info_label.setObjectName("previewInfo")
        layout.addWidget(self.preview_info_label)
        
        return panel
    
    def apply_styles(self) -> None:
        """应用样式表"""
        style = """
        #pageTitle {
            font-size: 18pt;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        #sectionTitle {
            font-size: 12pt;
            font-weight: bold;
            color: #34495e;
            margin-bottom: 5px;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        
        #importButton {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        }
        
        #importButton:hover {
            background-color: #2980b9;
        }
        
        #primaryButton {
            background-color: #27ae60;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 5px;
            font-weight: bold;
            font-size: 11pt;
        }
        
        #primaryButton:hover {
            background-color: #229954;
        }
        
        #primaryButton:disabled {
            background-color: #95a5a6;
        }
        
        #fieldsList {
            border: 1px solid #bdc3c7;
            border-radius: 3px;
            background-color: white;
        }
        
        #previewTable {
            border: 1px solid #bdc3c7;
            border-radius: 3px;
            background-color: white;
            gridline-color: #ecf0f1;
        }
        
        #fileInfoLabel, #previewInfo {
            color: #7f8c8d;
            font-style: italic;
        }
        
        QPushButton {
            padding: 6px 12px;
            border-radius: 3px;
            border: 1px solid #bdc3c7;
            background-color: #ecf0f1;
        }
        
        QPushButton:hover {
            background-color: #d5dbdb;
        }
        
        QPushButton:disabled {
            color: #95a5a6;
            background-color: #f8f9fa;
        }
        """
        self.setStyleSheet(style)
    
    def connect_signals(self) -> None:
        """连接信号槽"""
        self.import_btn.clicked.connect(self.file_import_requested.emit)
        self.generate_btn.clicked.connect(self.generate_requested.emit)
        self.select_all_btn.clicked.connect(self._on_select_all)
        self.select_none_btn.clicked.connect(self._on_select_none)
        self.add_field_btn.clicked.connect(self._on_add_custom_field)
        self.fields_list.itemChanged.connect(self._on_field_item_changed)
    
    def _on_select_all(self) -> None:
        """全选字段"""
        for i in range(self.fields_list.count()):
            item = self.fields_list.item(i)
            if item and hasattr(item, 'setCheckState'):
                item.setCheckState(Qt.Checked)
    
    def _on_select_none(self) -> None:
        """全不选字段"""
        for i in range(self.fields_list.count()):
            item = self.fields_list.item(i)
            if item and hasattr(item, 'setCheckState'):
                item.setCheckState(Qt.Unchecked)
    
    def _on_field_item_changed(self, item: QListWidgetItem) -> None:
        """字段选择状态改变"""
        if hasattr(item, 'field_name'):
            field_name = item.field_name
            is_selected = item.checkState() == Qt.Checked
            self.field_selection_changed.emit([field_name, is_selected])
    
    def _on_add_custom_field(self) -> None:
        """添加自定义字段"""
        dialog = CustomFieldDialog(self)
        if dialog.exec() == QDialog.Accepted:
            field_name, default_value = dialog.get_field_data()
            self.custom_field_added.emit(field_name, default_value)
    
    def update_file_info(self, file_path: str, data_info: dict) -> None:
        """更新文件信息显示"""
        file_name = file_path.split('/')[-1] if '/' in file_path else file_path.split('\\')[-1]
        info_text = f"{file_name} ({data_info.get('rows', 0)} 行, {data_info.get('columns', 0)} 列)"
        self.file_info_label.setText(info_text)
        
        # 启用相关按钮
        self.select_all_btn.setEnabled(True)
        self.select_none_btn.setEnabled(True)
        self.add_field_btn.setEnabled(True)
    
    def update_fields_list(self, field_selections: List[FieldSelection]) -> None:
        """更新字段列表"""
        self.fields_list.clear()
        
        for field_selection in field_selections:
            item = QListWidgetItem(field_selection.field_name)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked if field_selection.is_selected else Qt.Unchecked)
            
            # 添加字段名称属性，用于信号处理
            item.field_name = field_selection.field_name
            
            # 根据字段类型设置不同的显示样式
            if field_selection.field_type == FieldType.CUSTOM:
                item.setText(f"🔧 {field_selection.field_name}")
                item.setToolTip("自定义字段")
            else:
                item.setText(f"📊 {field_selection.field_name}")
                item.setToolTip("原始字段")
            
            self.fields_list.addItem(item)
    
    def update_preview_table(self, preview_data: Optional[pd.DataFrame]) -> None:
        """更新预览表格"""
        if preview_data is None or preview_data.empty:
            self.preview_table.clear()
            self.preview_table.setRowCount(0)
            self.preview_table.setColumnCount(0)
            self.preview_info_label.setText("没有可预览的数据")
            self.generate_btn.setEnabled(False)
            return
        
        # 设置表格尺寸
        rows, cols = preview_data.shape
        self.preview_table.setRowCount(rows)
        self.preview_table.setColumnCount(cols)
        
        # 设置表头
        self.preview_table.setHorizontalHeaderLabels(list(preview_data.columns))
        
        # 填充数据
        for i in range(rows):
            for j in range(cols):
                value = preview_data.iloc[i, j]
                # 处理NaN值
                if pd.isna(value):
                    display_value = ""
                else:
                    display_value = str(value)
                
                item = QTableWidgetItem(display_value)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # 设置为只读
                self.preview_table.setItem(i, j, item)
        
        # 调整列宽
        self.preview_table.resizeColumnsToContents()
        
        # 更新信息标签
        self.preview_info_label.setText(f"预览数据 (前 {rows} 行，共 {cols} 列)")
        
        # 启用生成按钮
        self.generate_btn.setEnabled(True)
    
    def show_error_message(self, title: str, message: str) -> None:
        """显示错误消息"""
        QMessageBox.critical(self, title, message)
    
    def show_success_message(self, title: str, message: str) -> None:
        """显示成功消息"""
        QMessageBox.information(self, title, message)
    
    def get_output_file_path(self) -> Optional[str]:
        """获取输出文件路径"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存Excel文件",
            "",
            "Excel文件 (*.xlsx);;CSV文件 (*.csv)"
        )
        return file_path if file_path else None


class CustomFieldDialog(QDialog):
    """自定义字段添加对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加自定义字段")
        self.setModal(True)
        self.resize(400, 300)
        
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self) -> None:
        """创建UI"""
        layout = QVBoxLayout(self)
        
        # 创建表单
        form_layout = QFormLayout()
        
        # 字段名称
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("请输入字段名称")
        form_layout.addRow("字段名称:", self.name_edit)
        
        # 字段类型
        self.type_combo = QComboBox()
        self.type_combo.addItems(["text", "number", "date"])
        form_layout.addRow("字段类型:", self.type_combo)
        
        # 默认值
        self.default_edit = QLineEdit()
        self.default_edit.setPlaceholderText("请输入默认值")
        form_layout.addRow("默认值:", self.default_edit)
        
        # 描述
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)
        self.description_edit.setPlaceholderText("字段描述（可选）")
        form_layout.addRow("描述:", self.description_edit)
        
        layout.addLayout(form_layout)
        
        # 按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        layout.addWidget(button_box)
        
        self.ok_button = button_box.button(QDialogButtonBox.Ok)
        self.ok_button.setText("添加")
        self.ok_button.setEnabled(False)
        
        button_box.button(QDialogButtonBox.Cancel).setText("取消")
        
        # 连接按钮信号
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
    
    def connect_signals(self) -> None:
        """连接信号"""
        self.name_edit.textChanged.connect(self._validate_input)
    
    def _validate_input(self) -> None:
        """验证输入"""
        name = self.name_edit.text().strip()
        self.ok_button.setEnabled(bool(name))
    
    def get_field_data(self) -> tuple:
        """获取字段数据"""
        return (
            self.name_edit.text().strip(),
            self.default_edit.text().strip()
        )
    
    def get_custom_field(self) -> CustomField:
        """获取自定义字段对象"""
        return CustomField(
            name=self.name_edit.text().strip(),
            default_value=self.default_edit.text().strip(),
            field_type=self.type_combo.currentText(),
            description=self.description_edit.toPlainText().strip()
        )