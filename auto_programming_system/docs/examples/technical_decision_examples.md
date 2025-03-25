# 技术决策模块示例代码

本文档提供了技术决策模块的使用示例，包括决策点识别、选项生成、评估和记录等功能。

## 1. 基本使用

### 1.1 识别决策点

```python
from autoprogrammer.decisions import DecisionPointIdentifier

# 初始化决策点识别器
identifier = DecisionPointIdentifier()

# 识别决策点
requirement = """
创建一个高性能的数据处理系统，需要处理大量CSV文件，并支持实时数据分析。
系统需要能够处理至少100GB的数据，并支持多用户并发访问。
"""

decision_points = identifier.identify(requirement)

# 打印识别结果
for point in decision_points:
    print(f"决策点: {point.description}")
    print(f"类型: {point.type}")
    print(f"约束: {point.constraints}")
    print("---")
```

### 1.2 生成技术选项

```python
from autoprogrammer.decisions import OptionGenerator

# 初始化选项生成器
generator = OptionGenerator()

# 为决策点生成选项
decision_point = decision_points[0]  # 数据处理框架决策点
options = generator.generate_options(decision_point)

# 打印生成的选项
for option in options:
    print(f"选项: {option.name}")
    print(f"描述: {option.description}")
    print(f"优点: {option.pros}")
    print(f"缺点: {option.cons}")
    print("---")
```

### 1.3 评估技术选项

```python
from autoprogrammer.decisions import OptionEvaluator

# 初始化选项评估器
evaluator = OptionEvaluator()

# 评估选项
option = options[0]  # pandas + dask选项
evaluation = evaluator.evaluate(option, decision_point)

# 打印评估结果
print(f"评分: {evaluation.score}")
print(f"详细分析: {evaluation.reasoning}")
print(f"风险: {evaluation.risks}")
print(f"建议: {evaluation.recommendation}")
```

### 1.4 记录技术决策

```python
from autoprogrammer.decisions import DecisionRecorder

# 初始化决策记录器
recorder = DecisionRecorder()

# 记录决策
decision_record = recorder.record_decision(
    decision_point=decision_point,
    selected_option=option,
    reasoning=evaluation.reasoning,
    context={
        "project_id": "proj_001",
        "decision_date": "2024-03-26",
        "decision_maker": "system"
    }
)

# 打印记录结果
print(f"决策记录ID: {decision_record.id}")
print(f"决策时间: {decision_record.timestamp}")
print(f"决策状态: {decision_record.status}")
```

## 2. 高级用法

### 2.1 自定义评估标准

```python
# 定义自定义评估标准
custom_criteria = {
    "performance": 0.4,    # 性能权重
    "maintainability": 0.3,  # 可维护性权重
    "scalability": 0.3     # 可扩展性权重
}

# 使用自定义标准评估选项
evaluation = evaluator.evaluate(
    option=option,
    decision_point=decision_point,
    criteria=custom_criteria
)
```

### 2.2 批量决策处理

```python
from autoprogrammer.decisions import DecisionPipeline

# 创建决策流水线
pipeline = DecisionPipeline()

# 处理多个决策点
decision_points = identifier.identify(requirement)
results = pipeline.process(decision_points)

# 打印处理结果
for result in results:
    print(f"决策点: {result.decision_point.description}")
    print(f"选择的选项: {result.selected_option.name}")
    print(f"决策理由: {result.reasoning}")
    print("---")
```

### 2.3 决策历史查询

```python
from autoprogrammer.decisions import DecisionHistory

# 初始化决策历史查询器
history = DecisionHistory()

# 查询特定项目的决策历史
project_decisions = history.get_project_decisions("proj_001")

# 打印决策历史
for decision in project_decisions:
    print(f"决策时间: {decision.timestamp}")
    print(f"决策点: {decision.decision_point.description}")
    print(f"选择的选项: {decision.selected_option.name}")
    print("---")
```

## 3. 最佳实践

### 3.1 错误处理

```python
from autoprogrammer.decisions import DecisionError

try:
    # 识别决策点
    decision_points = identifier.identify(requirement)
    
    # 生成选项
    options = generator.generate_options(decision_points[0])
    
    # 评估选项
    evaluation = evaluator.evaluate(options[0], decision_points[0])
    
except DecisionError as e:
    print(f"决策处理错误: {e.message}")
    print(f"错误类型: {e.type}")
    print(f"建议解决方案: {e.suggestion}")
```

### 3.2 性能优化

```python
# 使用缓存优化选项生成
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_options(decision_point_id):
    return generator.generate_options(decision_point_id)

# 使用异步处理提高性能
import asyncio

async def process_decisions_async(decision_points):
    tasks = []
    for point in decision_points:
        task = asyncio.create_task(generator.generate_options_async(point))
        tasks.append(task)
    return await asyncio.gather(*tasks)
```

### 3.3 决策验证

```python
from autoprogrammer.decisions import DecisionValidator

# 初始化决策验证器
validator = DecisionValidator()

# 验证决策的合理性
validation_result = validator.validate_decision(
    decision_point=decision_point,
    selected_option=option,
    evaluation=evaluation
)

if validation_result.is_valid:
    print("决策验证通过")
    print(f"置信度: {validation_result.confidence}")
else:
    print("决策验证失败")
    print(f"问题: {validation_result.issues}")
```

## 4. 集成示例

### 4.1 与需求分析模块集成

```python
from autoprogrammer.requirements import RequirementAnalyzer
from autoprogrammer.decisions import DecisionPipeline

# 初始化需求分析器
analyzer = RequirementAnalyzer()

# 分析需求
requirement = "创建一个高性能的数据处理系统..."
analysis_result = analyzer.analyze(requirement)

# 使用分析结果进行技术决策
pipeline = DecisionPipeline()
decisions = pipeline.process(analysis_result.decision_points)

# 生成技术方案
technical_solution = {
    "requirements": analysis_result,
    "decisions": decisions,
    "implementation_plan": generate_implementation_plan(decisions)
}
```

### 4.2 与代码生成模块集成

```python
from autoprogrammer.code_generation import CodeGenerator
from autoprogrammer.decisions import DecisionRecorder

# 记录技术决策
recorder = DecisionRecorder()
decision_record = recorder.record_decision(...)

# 使用决策结果生成代码
generator = CodeGenerator()
code = generator.generate_code(
    requirement=requirement,
    technical_decisions=decision_record
)

# 验证生成的代码
validation_result = generator.validate_code(code)
```

## 5. 调试与测试

### 5.1 调试决策过程

```python
from autoprogrammer.decisions import DecisionDebugger

# 初始化调试器
debugger = DecisionDebugger()

# 启用详细日志
debugger.enable_logging()

# 处理决策
with debugger.trace():
    decisions = pipeline.process(decision_points)

# 获取调试信息
debug_info = debugger.get_debug_info()
print(f"决策过程耗时: {debug_info.execution_time}")
print(f"内存使用: {debug_info.memory_usage}")
```

### 5.2 单元测试

```python
import pytest
from autoprogrammer.decisions import DecisionPoint, Option, Evaluation

def test_decision_point_creation():
    point = DecisionPoint(
        id="test_001",
        type="data_processing",
        description="测试决策点"
    )
    assert point.id == "test_001"
    assert point.type == "data_processing"

def test_option_evaluation():
    option = Option(
        name="test_option",
        description="测试选项"
    )
    evaluation = evaluator.evaluate(option, decision_point)
    assert 0 <= evaluation.score <= 1
    assert len(evaluation.reasoning) > 0

def test_decision_recording():
    record = recorder.record_decision(
        decision_point=decision_point,
        selected_option=option,
        reasoning="测试决策"
    )
    assert record.id is not None
    assert record.timestamp is not None
``` 