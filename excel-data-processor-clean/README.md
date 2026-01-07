# Excel Data Processor

基于 PySide6 的现代化 Excel 数据处理桌面应用程序。

## 功能特性

- 📊 支持 Excel (.xlsx) 和 CSV 文件导入
- 🔧 灵活的字段选择和自定义字段添加
- 📋 模板管理，保存和重用处理配置
- 👀 实时数据预览
- 🎨 现代化用户界面设计
- ⚡ 高性能数据处理

## 技术栈

- **UI框架**: PySide6 (Qt6)
- **数据处理**: pandas
- **架构模式**: MVC (Model-View-Controller)
- **测试框架**: pytest + pytest-qt + Hypothesis

## 安装和运行

### 环境要求

- Python 3.8+
- pip

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行应用程序

```bash
python run.py
```

或者

```bash
python -m src.main
```

### 开发模式安装

```bash
pip install -e .
```

## 项目结构

```
excel-data-processor/
├── src/                    # 源代码目录
│   ├── controllers/        # 控制器层
│   ├── models/            # 数据模型层
│   ├── services/          # 服务层
│   ├── views/             # 视图层
│   └── main.py           # 应用程序入口
├── tests/                 # 测试目录
├── templates/             # 模板存储目录
├── requirements.txt       # 依赖列表
├── setup.py              # 安装配置
└── run.py                # 启动脚本
```

## 开发指南

### 架构设计

应用程序采用 MVC 架构模式：

- **Model**: 数据模型和业务逻辑
- **View**: 用户界面组件
- **Controller**: 协调模型和视图的交互

### 信号槽机制

使用 Qt 的信号槽机制实现组件间通信，确保松耦合的设计。

## 许可证

MIT License