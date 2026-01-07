"""
主控制器，协调各个子系统
"""
from PySide6.QtCore import QObject, Signal

from ..views.main_window import MainWindow
from .data_controller import DataController


class MainController(QObject):
    """主控制器，协调各个子系统"""
    
    # 信号定义
    application_ready = Signal()
    
    def __init__(self, main_window: MainWindow):
        super().__init__()
        self.main_window = main_window
        
        # 创建子控制器
        self.data_controller = DataController()
        self.template_controller = None  # 将在后续任务中创建
        self.field_controller = None     # 将在后续任务中创建
        
        # 连接信号槽
        self._connect_signals()
        
        # 发出应用程序就绪信号
        self.application_ready.emit()
    
    def _connect_signals(self) -> None:
        """连接各组件的信号槽"""
        # 连接主窗口的视图切换信号
        self.main_window.view_changed.connect(self._on_view_changed)
        
        # 连接数据控制器的信号
        if self.data_controller:
            self.data_controller.error_occurred.connect(self._on_error_occurred)
            self.data_controller.file_loaded.connect(self._on_file_loaded)
            self.data_controller.headers_updated.connect(self._on_headers_updated)
            self.data_controller.configuration_changed.connect(self._on_configuration_changed)
            self.data_controller.preview_updated.connect(self._on_preview_updated)
            self.data_controller.processing_completed.connect(self._on_processing_completed)
        
        # 连接数据处理视图的信号
        data_view = self.main_window.get_data_processing_view()
        if data_view:
            data_view.file_import_requested.connect(self._on_file_import_requested)
            data_view.field_selection_changed.connect(self._on_field_selection_changed)
            data_view.custom_field_added.connect(self._on_custom_field_added)
            data_view.generate_requested.connect(self._on_generate_requested)
    
    def _on_view_changed(self, view_name: str) -> None:
        """处理视图切换事件"""
        print(f"视图已切换到: {view_name}")
        
        # 在后续任务中，这里将处理视图切换时的状态管理
        # 例如：保存当前视图的状态，加载新视图的状态等
    
    def _on_error_occurred(self, error_message: str) -> None:
        """处理错误事件"""
        print(f"错误: {error_message}")
        # 显示错误消息给用户
        data_view = self.main_window.get_data_processing_view()
        if data_view:
            data_view.show_error_message("错误", error_message)
    
    def _on_file_loaded(self, file_path: str) -> None:
        """处理文件加载完成事件"""
        print(f"文件已加载: {file_path}")
        data_view = self.main_window.get_data_processing_view()
        if data_view and self.data_controller:
            data_info = self.data_controller.get_data_info()
            data_view.update_file_info(file_path, data_info)
    
    def _on_headers_updated(self, headers: list) -> None:
        """处理表头更新事件"""
        print(f"表头已更新: {headers}")
        self._update_fields_list()
    
    def _on_configuration_changed(self) -> None:
        """处理配置变更事件"""
        print("配置已变更")
        self._update_fields_list()
    
    def _on_preview_updated(self, preview_data) -> None:
        """处理预览数据更新事件"""
        print("预览数据已更新")
        data_view = self.main_window.get_data_processing_view()
        if data_view:
            data_view.update_preview_table(preview_data)
    
    def _on_processing_completed(self, result) -> None:
        """处理数据处理完成事件"""
        data_view = self.main_window.get_data_processing_view()
        if data_view:
            if result.success:
                message = f"文件已成功生成！\n路径: {result.output_file_path}\n处理行数: {result.processed_rows}"
                if result.warnings:
                    message += f"\n\n警告:\n" + "\n".join(result.warnings)
                data_view.show_success_message("处理完成", message)
            else:
                data_view.show_error_message("处理失败", result.error_message or "未知错误")
    
    def _on_file_import_requested(self) -> None:
        """处理文件导入请求"""
        from PySide6.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "选择Excel或CSV文件",
            "",
            "Excel文件 (*.xlsx *.xls);;CSV文件 (*.csv);;所有支持的文件 (*.xlsx *.xls *.csv)"
        )
        
        if file_path and self.data_controller:
            self.data_controller.load_file(file_path)
    
    def _on_field_selection_changed(self, field_data: list) -> None:
        """处理字段选择变更"""
        if len(field_data) >= 2 and self.data_controller:
            field_name, is_selected = field_data[0], field_data[1]
            self.data_controller.set_field_selection(field_name, is_selected)
    
    def _on_custom_field_added(self, field_name: str, default_value: str) -> None:
        """处理自定义字段添加"""
        if self.data_controller:
            from ..models.data_model import CustomField
            custom_field = CustomField(name=field_name, default_value=default_value)
            self.data_controller.add_custom_field(custom_field)
    
    def _on_generate_requested(self) -> None:
        """处理生成文件请求"""
        data_view = self.main_window.get_data_processing_view()
        if data_view and self.data_controller:
            output_path = data_view.get_output_file_path()
            if output_path:
                self.data_controller.process_data(output_path)
    
    def _update_fields_list(self) -> None:
        """更新字段列表显示"""
        if self.data_controller:
            field_selections = self.data_controller.get_field_selections()
            data_view = self.main_window.get_data_processing_view()
            if data_view:
                data_view.update_fields_list(field_selections)
    
    def get_main_window(self) -> MainWindow:
        """获取主窗口实例"""
        return self.main_window
    
    def get_data_controller(self) -> DataController:
        """获取数据控制器实例"""
        return self.data_controller