"""
主窗口类，管理整体布局和导航
"""
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, 
                               QVBoxLayout, QStackedWidget)
from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QFont

from .sidebar_panel import SidebarPanel
from .data_processing_view import DataProcessingView
from .template_management_view import TemplateManagementView


class MainWindow(QMainWindow):
    """主窗口类，管理整体布局和导航"""
    
    # 信号定义
    view_changed = Signal(str)  # 视图切换信号
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel Data Processor")
        self.setMinimumSize(1200, 800)
        
        # 创建中央部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建主要组件
        self.sidebar = SidebarPanel()
        self.stacked_widget = QStackedWidget()
        
        # 创建视图
        self.data_processing_view = DataProcessingView()
        self.template_management_view = TemplateManagementView()
        
        # 设置UI
        self.setup_ui()
        self.connect_signals()
        
        # 默认显示数据处理视图
        self.switch_view("data_processing")
    
    def setup_ui(self) -> None:
        """创建侧边栏和内容区域，应用样式表和布局"""
        # 创建主布局
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 添加侧边栏
        main_layout.addWidget(self.sidebar)
        
        # 添加视图到堆叠部件
        self.stacked_widget.addWidget(self.data_processing_view)
        self.stacked_widget.addWidget(self.template_management_view)
        
        # 添加堆叠部件到主布局
        main_layout.addWidget(self.stacked_widget, 1)
        
        # 应用现代化样式表
        self.apply_modern_style()
    
    def apply_modern_style(self) -> None:
        """应用现代化的UI设计风格和配色方案"""
        style = """
        QMainWindow {
            background-color: #f5f5f5;
        }
        
        QWidget {
            font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
            font-size: 10pt;
        }
        
        /* 侧边栏样式 */
        SidebarPanel {
            background-color: #2c3e50;
            border-right: 1px solid #34495e;
        }
        
        /* 主内容区域样式 */
        QStackedWidget {
            background-color: #ffffff;
            border: none;
        }
        """
        self.setStyleSheet(style)
    
    def connect_signals(self) -> None:
        """连接信号槽"""
        self.sidebar.navigation_requested.connect(self.switch_view)
    
    def switch_view(self, view_name: str) -> None:
        """切换到指定视图"""
        if view_name == "data_processing":
            self.stacked_widget.setCurrentWidget(self.data_processing_view)
        elif view_name == "template_management":
            self.stacked_widget.setCurrentWidget(self.template_management_view)
        
        # 发出视图切换信号
        self.view_changed.emit(view_name)
    
    def get_data_processing_view(self) -> DataProcessingView:
        """获取数据处理视图实例"""
        return self.data_processing_view
    
    def get_template_management_view(self) -> TemplateManagementView:
        """获取模板管理视图实例"""
        return self.template_management_view