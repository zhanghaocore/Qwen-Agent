# 开发指南

本文档提供了全自动Python后端编程系统的开发指南，帮助开发者快速上手和实现功能。

## 环境准备

### 1. 基础环境
```bash
# 创建并激活conda环境
conda create -n qwen-agent python=3.8
conda activate qwen-agent

# 安装基础依赖
pip install -r requirements.txt
```

### 2. 开发工具
- VSCode/Cursor (推荐)
- Git
- Docker (可选，用于容器化部署)

## 项目结构

```
auto_programming_system/
├── src/                    # 源代码目录
│   ├── __init__.py        # 包初始化文件
│   ├── __main__.py        # 主程序入口
│   ├── common/            # 公共组件
│   ├── agents/            # AI代理
│   ├── requirement_analysis/  # 需求分析模块
│   ├── technical_decision/    # 技术决策模块
│   ├── code_generation/       # 代码生成模块
│   ├── execution_validation/  # 执行验证模块
│   └── optimization/          # 优化模块
├── tests/                  # 测试目录
│   ├── __init__.py
│   ├── conftest.py        # 测试配置
│   ├── test_requirement_analysis/
│   ├── test_technical_decision/
│   ├── test_code_generation/
│   ├── test_execution_validation/
│   └── test_optimization/
├── docs/                   # 文档目录
│   ├── architecture/       # 架构文档
│   ├── api_reference/     # API参考
│   ├── development/       # 开发指南
│   ├── examples/         # 示例文档
│   ├── modules/          # 模块文档
│   ├── product/          # 产品文档
│   └── test_results/     # 测试结果
├── examples/              # 示例代码
│   ├── basic_usage/
│   ├── advanced_features/
│   └── integration/
├── scripts/               # 工具脚本
├── setup.py              # 项目配置
├── requirements.txt      # 依赖列表
├── requirements-dev.txt  # 开发依赖
└── README.md            # 项目说明
```

## 开发流程

### 1. 需求分析模块
```python
# 示例：实现需求分析
from src.requirement_analysis.analyzer import RequirementAnalyzer

analyzer = RequirementAnalyzer()
requirements = analyzer.analyze("用户需求文本")
```

### 2. 技术决策模块
```python
# 示例：实现技术决策
from src.technical_decision.decision_maker import DecisionMaker

decision_maker = DecisionMaker()
decisions = decision_maker.make_decisions(requirements)
```

### 3. 代码生成模块
```python
# 示例：实现代码生成
from src.code_generation.generator import CodeGenerator

generator = CodeGenerator()
code = generator.generate(decisions)
```

### 4. 执行验证模块
```python
# 示例：实现代码验证
from src.execution_validation.validator import CodeValidator

validator = CodeValidator()
validation_result = validator.validate(code)
```

### 5. 优化模块
```python
# 示例：实现代码优化
from src.optimization.optimizer import CodeOptimizer

optimizer = CodeOptimizer()
optimized_code = optimizer.optimize(code, validation_result)
```

## 调试方法

### 1. 日志调试
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 在代码中使用
logger.debug("调试信息")
logger.info("普通信息")
logger.warning("警告信息")
logger.error("错误信息")
```

### 2. 断点调试
- 在VSCode/Cursor中设置断点
- 使用调试模式运行代码
- 查看变量值和调用栈

### 3. 单元测试
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_requirement_analysis.py

# 运行特定测试用例
pytest tests/test_requirement_analysis.py::test_analyze_requirements
```

## 代码规范

### 1. 命名规范
- 类名：使用大驼峰命名法（PascalCase）
- 函数名：使用小写字母和下划线（snake_case）
- 变量名：使用小写字母和下划线（snake_case）
- 常量名：使用大写字母和下划线（UPPER_SNAKE_CASE）

### 2. 注释规范
```python
def process_requirements(requirements: str) -> dict:
    """
    处理用户需求文本。

    Args:
        requirements (str): 用户输入的需求文本

    Returns:
        dict: 处理后的结构化需求

    Raises:
        ValueError: 当需求文本为空时
    """
    if not requirements:
        raise ValueError("需求文本不能为空")
    # 处理逻辑
```

### 3. 代码格式
```bash
# 使用black格式化代码
black src/

# 使用isort整理导入
isort src/
```

## 常见问题

### 1. 环境问题
Q: 如何解决依赖安装失败？
A: 尝试以下步骤：
1. 更新pip: `pip install --upgrade pip`
2. 清理缓存: `pip cache purge`
3. 重新安装: `pip install -r requirements.txt`

### 2. 运行问题
Q: 如何解决模块导入错误？
A: 确保：
1. 在正确的虚拟环境中
2. PYTHONPATH包含项目根目录
3. 所有依赖已正确安装

### 3. 测试问题
Q: 如何解决测试失败？
A: 检查：
1. 测试数据是否正确
2. 环境变量是否设置
3. 依赖是否完整

## 开发建议

### 1. 功能实现
- 先实现核心功能
- 保持代码简洁
- 添加必要的注释
- 编写单元测试

### 2. 代码质量
- 遵循代码规范
- 及时重构代码
- 保持代码可读性
- 避免代码重复

### 3. 测试覆盖
- 编写单元测试
- 进行集成测试
- 进行端到端测试
- 保持测试覆盖率

## 相关文档

- [架构文档](../architecture/README.md)
- [API参考](../api-reference.md)
- [测试文档](../test_results/README.md)
- [示例文档](../examples/README.md) 