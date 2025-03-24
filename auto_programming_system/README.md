# 全自动Python后端编程系统

## 系统目标
实现自然语言到可执行Python代码的端到端转换，无需人工干预地将用户需求转化为高质量的Python后端代码。

## 核心特性
- **自然语言需求解析**：将非结构化文本转换为结构化编程任务
- **智能代码生成**：基于需求自动生成符合最佳实践的Python代码
- **安全沙箱执行**：在隔离环境中验证生成代码的正确性和安全性
- **迭代优化机制**：基于执行结果和性能指标不断改进生成的代码

## 架构概览

系统由四个核心模块组成，相互协作完成从需求到代码的转换过程：

1. **需求分析系统**：解析自然语言，提取关键信息
2. **代码生成引擎**：根据结构化描述生成Python代码
3. **执行验证环境**：在安全沙箱中测试和验证代码
4. **迭代优化机制**：通过反馈循环持续改进代码质量

## 快速开始
```bash
# 安装依赖
pip install -r requirements.txt

# 运行基本示例
python -m auto_programming_system --input "创建一个处理CSV文件的函数，计算每列的平均值"

# 高级用例（带约束）
python -m auto_programming_system --input "开发一个REST API端点，接收JSON数据并存储到SQLite" --constraints "使用FastAPI,遵循SOLID原则"
```

## 使用场景

- **原型快速开发**：迅速将想法转化为可执行代码
- **教学辅助工具**：为编程学习者提供代码范例和解释
- **自动化测试生成**：根据函数描述自动生成测试用例
- **代码重构助手**：识别并优化现有代码中的问题

## 目录结构
```
auto_programming_system/
├── requirement_analysis/  # 需求分析模块
├── code_generation/       # 代码生成模块
├── execution_validation/  # 执行验证模块
├── optimization/          # 迭代优化模块
├── common/                # 共享组件
├── templates/             # 代码模板
├── tests/                 # 单元测试
├── examples/              # 使用示例
└── docs/                  # 项目文档
```

## 开发指南

详细的开发指南请参考 `docs/development/`。

## 许可证

MIT
