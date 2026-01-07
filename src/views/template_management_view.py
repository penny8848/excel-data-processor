"""
模板管理视图
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLabel, QListWidget,
                               QTextEdit, QGroupBox, QSplitter)
from PySide6.QtCore import Signal, Qt


class TemplateManagementView(QWidget):
    """模板管理视图"""
    
    # 信号定义
    template_save_requested = Signal(str)
    template_load_requested = Signal(str)
    template_delete_requested = Signal(str)
    
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
        title_label = QLabel("模板管理")
        title_label.setObjectName("pageTitle")
        main_layout.addWidget(title_label)
        
        # 创建主要内容区域
        content_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(content_splitter)
        
        # 左侧模板列表
        left_panel = self.create_template_list_panel()
        content_splitter.addWidget(left_panel)
        
        # 右侧模板详情
        right_panel = self.create_template_detail_panel()
        content_splitter.addWidget(right_panel)
        
        # 设置分割器比例
        content_splitter.setStretchFactor(0, 1)
        content_splitter.setStretchFactor(1, 1)
    
    def create_template_list_panel(self) -> QWidget:
        """创建模板列表面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 模板列表组
        list_group = QGroupBox("已保存的模板")
        list_layout = QVBoxLayout(list_group)
        
        # 模板列表
        self.template_list = QListWidget()
        self.template_list.setObjectName("templateList")
        list_layout.addWidget(self.template_list)
        
        # 模板操作按钮
        button_layout = QHBoxLayout()
        
        self.load_btn = QPushButton("加载模板")
        self.load_btn.setEnabled(False)
        self.delete_btn = QPushButton("删除模板")
        self.delete_btn.setEnabled(False)
        
        button_layout.addWidget(self.load_btn)
        button_layout.addWidget(self.delete_btn)
        list_layout.addLayout(button_layout)
        
        layout.addWidget(list_group)
        
        # 新建模板组
        new_group = QGroupBox("保存当前配置")
        new_layout = QVBoxLayout(new_group)
        
        self.save_btn = QPushButton("保存为新模板")
        self.save_btn.setObjectName("primaryButton")
        self.save_btn.setEnabled(False)
        new_layout.addWidget(self.save_btn)
        
        layout.addWidget(new_group)
        
        # 添加弹性空间
        layout.addStretch()
        
        return panel
    
    def create_template_detail_panel(self) -> QWidget:
        """创建模板详情面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 详情标题
        detail_label = QLabel("模板详情")
        detail_label.setObjectName("sectionTitle")
        layout.addWidget(detail_label)
        
        # 模板信息显示
        self.template_info = QTextEdit()
        self.template_info.setObjectName("templateInfo")
        self.template_info.setReadOnly(True)
        self.template_info.setPlainText("请选择一个模板查看详情")
        layout.addWidget(self.template_info)
        
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
        
        #templateList {
            border: 1px solid #bdc3c7;
            border-radius: 3px;
            background-color: white;
        }
        
        #templateInfo {
            border: 1px solid #bdc3c7;
            border-radius: 3px;
            background-color: #f8f9fa;
            font-family: "Consolas", "Monaco", monospace;
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
        self.save_btn.clicked.connect(lambda: self.template_save_requested.emit(""))
        self.load_btn.clicked.connect(lambda: self.template_load_requested.emit(""))
        self.delete_btn.clicked.connect(lambda: self.template_delete_requested.emit(""))