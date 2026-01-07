"""
Excel Data Processor 应用程序入口
"""
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from .views.main_window import MainWindow
from .controllers.main_controller import MainController


def main():
    """应用程序主函数"""
    # 创建应用程序实例
    app = QApplication(sys.argv)
    
    # 设置应用程序属性
    app.setApplicationName("Excel Data Processor")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Excel Data Processor Team")
    
    # 设置高DPI支持
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    try:
        # 创建主窗口
        main_window = MainWindow()
        
        # 创建主控制器
        main_controller = MainController(main_window)
        
        # 显示主窗口
        main_window.show()
        
        # 运行应用程序
        return app.exec()
        
    except Exception as e:
        print(f"应用程序启动失败: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())