# 全自动Python后端编程系统

## 系统目标
实现自然语言到可执行Python代码的端到端转换，无需人工干预地将用户需求转化为高质量的Python后端代码。

## 核心特性
- **自然语言需求解析**：将非结构化文本转换为结构化编程任务
- **多层次需求挖掘**：通过逐步推理深入分析复杂需求
- **智能代码生成**：基于需求自动生成符合最佳实践的Python代码
- **安全沙箱执行**：在隔离环境中验证生成代码的正确性和安全性
- **迭代优化机制**：基于执行结果和性能指标不断改进生成的代码

## 架构概览

系统由四个核心模块组成，相互协作完成从需求到代码的转换过程：

1. **需求分析系统**：解析自然语言，提取关键信息
   - **基础分析**：基本的文本处理和需求解析
   - **高级分析**：多层次需求挖掘和逐步推理
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

# 高级需求分析（使用逐步推理）
python -m pytest auto_programming_system/tests/test_advanced_requirement_analysis.py
```

## 使用场景

- **原型快速开发**：迅速将想法转化为可执行代码
- **复杂需求分析**：深入理解和分解复杂的系统需求
- **技术选型建议**：获取针对需求的技术栈推荐和架构建议
- **教学辅助工具**：为编程学习者提供代码范例和解释
- **自动化测试生成**：根据函数描述自动生成测试用例
- **代码重构助手**：识别并优化现有代码中的问题

## 目录结构
```
auto_programming_system/
├── requirement_analysis/         # 需求分析模块
│   ├── advanced_analysis/        # 高级需求分析模块（多层次需求挖掘）
│   ├── preprocessor/             # 文本预处理模块
│   ├── semantic_analyzer/        # 语义分析模块
│   ├── dsl_converter/            # DSL转换模块
│   └── validator/                # 规范验证模块
├── code_generation/              # 代码生成模块
├── execution_validation/         # 执行验证模块
├── optimization/                 # 迭代优化模块
├── common/                       # 共享组件
├── templates/                    # 代码模板
├── tests/                        # 单元测试和集成测试
│   ├── requirement_analysis/     # 需求分析模块测试
│   ├── test_integration.py      # 集成测试
│   ├── test_advanced_requirement_analysis.py  # 高级需求分析测试
│   └── test_code_generation.py   # 代码生成测试
├── examples/                     # 使用示例
└── docs/                         # 项目文档
    └── modules/                  # 模块文档
        └── requirement_analysis/ # 需求分析模块文档
```

## 特色功能

### 多层次需求挖掘框架

高级需求分析模块通过多层次需求挖掘框架，实现复杂需求的深入理解：

1. **领域分类**：自动识别需求所属领域
2. **关键问题提取**：基于领域知识提出关键问题
3. **逐层推理**：每个答案触发更精细的子问题，不断深化理解
4. **技术决策**：提供技术栈选择建议和备选方案分析
5. **完整性检查**：确保所有必要需求维度都已覆盖

### 技术栈推荐

系统可根据需求特点推荐合适的技术栈组合，包括：

- 前后端框架选择
- 数据库和存储方案
- 部署和运维策略
- 安全实施方案

## 开发指南

详细的开发指南请参考 `docs/development/`。

## 许可证

MIT
