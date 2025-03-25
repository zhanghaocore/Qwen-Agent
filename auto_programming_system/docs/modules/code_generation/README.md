# 代码生成模块

## 概述

代码生成模块是系统的核心组件，负责将结构化的需求描述转换为高质量的 Python 代码。该模块采用模板引擎和大语言模型相结合的方式，确保生成的代码符合最佳实践和项目规范。

## 文档结构

1. **[生成引擎](./code-generation.md)**
   - 代码生成流程
   - 模板系统
   - 代码优化

2. **[模板系统](./templates/README.md)**
   - 模板库
   - 模板语法
   - 自定义模板

3. **[代码优化](./optimization/README.md)**
   - 性能优化
   - 代码重构
   - 质量改进

## 核心功能

### 1. 代码生成引擎
- 需求到代码的转换
- 代码结构生成
- 依赖管理
- 注释生成

### 2. 模板系统
- 预定义模板库
- 模板继承和组合
- 动态模板生成
- 自定义模板支持

### 3. 代码优化
- 性能优化
- 代码重构
- 质量改进
- 最佳实践应用

## 使用示例

```python
from auto_programming_system.code_generation import CodeGenerator

# 创建生成器实例
generator = CodeGenerator()

# 准备需求描述
requirements = {
    "type": "function",
    "name": "calculate_column_averages",
    "description": "计算CSV文件每列的平均值",
    "parameters": {
        "input_file": "str",
        "output_file": "str"
    },
    "constraints": [
        "使用pandas处理CSV",
        "考虑内存使用",
        "添加错误处理"
    ]
}

# 生成代码
code = generator.generate(requirements)

# 查看生成的代码
print(code)
```

## 配置说明

代码生成器支持以下配置选项：

```python
config = {
    "generation": {
        "template_dir": "templates/",  # 模板目录
        "max_iterations": 3,           # 最大优化迭代次数
        "timeout": 60,                 # 生成超时时间（秒）
    },
    "optimization": {
        "enable_performance": True,    # 启用性能优化
        "enable_refactoring": True,    # 启用代码重构
        "enable_quality": True,        # 启用质量改进
    },
    "templates": {
        "default_style": "pep8",       # 默认代码风格
        "docstring_style": "google",   # 文档字符串风格
        "comment_style": "detailed",   # 注释风格
    }
}
```

## 最佳实践

1. **需求描述**
   - 提供清晰的需求描述
   - 明确指定约束条件
   - 包含必要的上下文信息

2. **模板使用**
   - 选择合适的模板
   - 自定义模板时保持一致性
   - 定期更新模板库

3. **代码优化**
   - 根据实际需求调整优化策略
   - 平衡代码质量和性能
   - 保持代码可维护性

## 常见问题

1. **Q: 如何自定义代码生成模板？**
   A: 可以通过继承基础模板并重写特定方法来创建自定义模板，详见[模板系统文档](./templates/README.md)。

2. **Q: 如何提高生成代码的质量？**
   A: 可以通过调整配置参数、使用更详细的模板、启用代码优化功能来提高代码质量。

3. **Q: 如何处理复杂的代码生成需求？**
   A: 系统支持将复杂需求分解为多个子任务，并分步生成和组合代码。

## 相关文档

- [需求分析模块](../requirement_analysis/README.md)
- [执行验证模块](../execution_validation/README.md)
- [优化模块](../optimization/README.md)
- [系统架构](../../architecture/core-modules.md) 