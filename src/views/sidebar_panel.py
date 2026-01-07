"""
侧边栏导航组件
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                               QLabel, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont, QIcon


class SidebarPanel(QWidget):
    """侧边栏导航组件"""
    
    # 信号定义
    navigation_requested = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.setFixedWidth(200)
        self.current_view = "data_processing"
        
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self) -> None:
        """创建导航按钮，设置样式和布局"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(10)
        
        # 应用标题
        title_label = QLabel("Excel Data Processor")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("titleLabel")
        layout.addWidget(title_label)
        
        # 添加间距
        layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        # 数据处理按钮
        self.data_processing_btn = QPushButton("数据处理")
        self.data_processing_btn.setObjectName("navButton")
        self.data_processing_btn.clicked.connect(lambda: self.navigate_to("data_processing"))
        layout.addWidget(self.data_processing_btn)
        
        # 模板管理按钮
        self.template_management_btn = QPushButton("模板管理")
        self.template_management_btn.setObjectName("navButton")
        self.template_management_btn.clicked.connect(lambda: self.navigate_to("template_management"))
        layout.addWidget(self.template_management_btn)
        
        # 添加弹性空间
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # 设置默认选中状态
        self.update_button_states()
    
    def apply_styles(self) -> None:
        """应用样式表"""
        style = """
        SidebarPanel {
            background-color: #2c3e50;
        }
        
        #titleLabel {
            color: #ecf0f1;
            font-size: 14pt;
            font-weight: bold;
            padding: 10px;
        }
        
        #navButton {
            background-color: #34495e;
            color: #ecf0f1;
            border: none;
            padding: 12px 20px;
            text-align: left;
            font-size: 11pt;
            border-radius: 4px;
            margin: 2px 10px;
        }
        
        #navButton:hover {
            background-color: #3498db;
        }
        
        #navButton:pressed {
            background-color: #2980b9;
        }
        
        #navButton[selected="true"] {
            background-color: #3498db;
            font-weight: bold;
        }
        """
        self.setStyleSheet(style)
    
    def navigate_to(self, view_name: str) -> None:
        """导航到指定视图"""
        if self.current_view != view_name:
            self.current_view = view_name
            self.update_button_states()
            self.navigation_requested.emit(view_name)
    
    def update_button_states(self) -> None:
        """更新按钮选中状态"""
        # 重置所有按钮状态
        self.data_processing_btn.setProperty("selected", False)
        self.template_management_btn.setProperty("selected", False)
        
        # 设置当前选中按钮
        if self.current_view == "data_processing":
            self.data_processing_btn.setProperty("selected", True)
        elif self.current_view == "template_management":
            self.template_management_btn.setProperty("selected", True)
        
        # 刷新样式
        self.data_processing_btn.style().unpolish(self.data_processing_btn)
        self.data_processing_btn.style().polish(self.data_processing_btn)
        self.template_management_btn.style().unpolish(self.template_management_btn)
        self.template_management_btn.style().polish(self.template_management_btn)