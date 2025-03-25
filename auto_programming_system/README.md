# 全自动Python后端编程系统

## 系统目标

实现自然语言到可执行Python代码的端到端转换，无需人工干预地将用户需求转化为高质量的Python后端代码。

## 核心特性

- **自然语言需求解析**：将非结构化文本转换为结构化编程任务
- **多层次需求挖掘**：通过逐步推理深入分析复杂需求
- **智能代码生成**：基于需求自动生成符合最佳实践的Python代码
- **安全沙箱执行**：在隔离环境中验证生成代码的正确性和安全性
- **迭代优化机制**：基于执行结果和性能指标不断改进生成的代码
- **智能技术决策**：自动识别技术决策点并提供最优解决方案

## 架构概览

系统由四个核心模块组成，相互协作完成从需求到代码的转换过程：

1. **需求分析系统**：解析自然语言，提取关键信息
   - **基础分析**：基本的文本处理和需求解析
   - **高级分析**：多层次需求挖掘和逐步推理
2. **技术决策**：提供技术栈选择建议和备选方案分析
   - **决策点识别**：自动识别需求中的技术决策点
   - **选项生成**：基于决策点生成可行的技术选项
   - **选项评估**：评估每个选项的优劣和适用性
   - **决策记录**：记录和追踪技术决策过程
3. **代码生成引擎**：根据结构化描述生成Python代码
4. **执行验证环境**：在安全沙箱中测试和验证代码
5. **迭代优化机制**：通过反馈循环持续改进代码质量

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

# 运行技术决策测试
python -m pytest auto_programming_system/tests/test_technical_decision.py
```

## 使用场景

- **原型快速开发**：迅速将想法转化为可执行代码
- **复杂需求分析**：深入理解和分解复杂的系统需求
- **技术选型建议**：获取针对需求的技术栈推荐和架构建议
- **教学辅助工具**：为编程学习者提供代码范例和解释
- **自动化测试生成**：根据函数描述自动生成测试用例
- **代码重构助手**：识别并优化现有代码中的问题
- **技术决策支持**：自动识别和评估技术决策点

## 文档

- [用户指南](docs/product/user-guide.md)：系统使用说明和最佳实践
- [API参考](docs/api-reference.md)：详细的API文档和示例
- [技术决策示例](docs/examples/technical_decision_examples.md)：技术决策模块的使用示例
- [开发计划](docs/modules/requirement_analysis/development-plan.md)：项目开发计划和进度

## 目录结构

```text
auto_programming_system/
├── agents/                    # 智能代理模块
│   ├── base_agent.py         # 基础代理类
│   ├── requirement_agent.py  # 需求分析代理
│   ├── technical_agent.py    # 技术决策代理
│   └── code_agent.py         # 代码生成代理
├── requirement_analysis/      # 需求分析模块
│   ├── basic_analysis/       # 基础分析
│   └── advanced_analysis/    # 高级分析
├── technical_decision/       # 技术决策模块
│   ├── decision_point.py     # 决策点定义
│   ├── option_generator.py   # 选项生成器
│   ├── evaluator.py          # 选项评估器
│   ├── recorder.py           # 决策记录器
│   ├── validator.py          # 决策验证器
│   └── README.md            # 模块文档
├── code_generation/          # 代码生成模块
│   ├── templates/           # 代码模板
│   ├── generators/          # 生成器
│   └── optimizers/          # 优化器
├── execution/               # 执行验证模块
│   ├── runner.py           # 代码运行器
│   ├── validator.py        # 结果验证器
│   └── profiler.py         # 性能分析器
├── tests/                  # 测试目录
│   ├── test_requirement_analysis/
│   ├── test_technical_decision/
│   └── test_code_generation/
├── docs/                   # 文档目录
│   ├── modules/           # 模块文档
│   ├── api/               # API文档
│   ├── product/           # 产品文档
│   └── examples/          # 示例文档
├── examples/              # 示例代码
├── requirements.txt       # 项目依赖
└── README.md             # 项目说明
```

## 特色功能

### 多层次需求挖掘框架

高级需求分析模块通过多层次需求挖掘框架，实现复杂需求的深入理解：

1. **领域分类**：自动识别需求所属领域
2. **关键问题提取**：基于领域知识提出关键问题
3. **逐层推理**：每个答案触发更精细的子问题，不断深化理解
4. **技术决策**：提供技术栈选择建议和备选方案分析
5. **完整性检查**：确保所有必要需求维度都已覆盖

### 智能技术决策系统

技术决策模块提供全面的决策支持：

1. **决策点识别**：
   - 自动识别需求中的技术决策点
   - 分析决策点之间的依赖关系
   - 提取决策约束和上下文信息

2. **选项生成**：
   - 基于决策点生成可行的技术选项
   - 考虑项目规模和团队能力
   - 支持自定义选项生成规则

3. **选项评估**：
   - 多维度评估（性能、可维护性、可扩展性）
   - 考虑项目约束和团队能力
   - 提供详细的评估理由和风险分析

4. **决策记录**：
   - 记录决策过程和理由
   - 追踪决策历史
   - 支持决策验证和审计

## 开发状态

- **需求分析模块**：已完成基础功能，支持多层次需求挖掘
- **技术决策模块**：已完成核心功能，测试覆盖率75%
- **代码生成模块**：开发中，支持基本代码生成
- **执行验证模块**：开发中，支持基本代码验证

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进系统。在提交代码前，请确保：

1. 所有测试通过
2. 代码符合PEP 8规范
3. 添加了必要的文档和注释
4. 更新了相关的测试用例

## 许可证

MIT License
