# 示例文档

本文档提供了全自动Python后端编程系统的使用示例和最佳实践。

## 快速开始

### 1. 基础示例
```python
from src import AutoProgrammingSystem

# 创建系统实例
system = AutoProgrammingSystem()

# 输入需求
requirements = """
创建一个用户管理系统，包含以下功能：
1. 用户注册和登录
2. 用户信息管理
3. 权限控制
4. 数据持久化
"""

# 生成代码
result = system.generate(requirements)

# 查看生成的代码
print(result.code)

# 查看生成报告
print(result.report)
```

### 2. 高级配置
```python
from src import AutoProgrammingSystem, Config

# 创建配置
config = Config(
    framework="fastapi",
    database="postgresql",
    auth_method="jwt",
    code_style="pep8",
    test_framework="pytest"
)

# 创建系统实例
system = AutoProgrammingSystem(config=config)

# 生成代码
result = system.generate(requirements)
```

## 功能示例

### 1. 需求分析
```python
from src.requirement_analysis import RequirementAnalyzer

# 创建分析器
analyzer = RequirementAnalyzer()

# 分析需求
requirements = """
创建一个RESTful API服务，提供以下功能：
1. 商品管理（CRUD）
2. 订单管理
3. 用户认证
4. 数据验证
"""

# 获取结构化需求
structured_requirements = analyzer.analyze(requirements)
print(structured_requirements)
```

### 2. 技术决策
```python
from src.technical_decision import DecisionMaker

# 创建决策器
decision_maker = DecisionMaker()

# 获取技术决策
decisions = decision_maker.make_decisions(structured_requirements)
print(decisions)
```

### 3. 代码生成
```python
from src.code_generation import CodeGenerator

# 创建生成器
generator = CodeGenerator()

# 生成代码
code = generator.generate(decisions)
print(code)
```

### 4. 执行验证
```python
from src.execution_validation import CodeValidator

# 创建验证器
validator = CodeValidator()

# 验证代码
result = validator.validate(code)
print(result)
```

### 5. 代码优化
```python
from src.optimization import CodeOptimizer

# 创建优化器
optimizer = CodeOptimizer()

# 优化代码
optimized_code = optimizer.optimize(code, result)
print(optimized_code)
```

## 最佳实践

### 1. 需求描述
```python
# 好的需求描述
requirements = """
创建一个博客系统，包含以下功能：
1. 文章管理
   - 创建、编辑、删除文章
   - 支持Markdown格式
   - 文章分类和标签
2. 用户系统
   - 用户注册和登录
   - 个人资料管理
3. 评论系统
   - 文章评论
   - 评论管理
4. 搜索功能
   - 文章搜索
   - 标签搜索
"""

# 不好的需求描述
bad_requirements = "做个博客系统"  # 过于简单
```

### 2. 配置优化
```python
# 推荐的配置
config = Config(
    framework="fastapi",  # 现代、高性能的Web框架
    database="postgresql",  # 功能强大的关系型数据库
    auth_method="jwt",  # 标准的认证方式
    code_style="pep8",  # Python标准代码风格
    test_framework="pytest",  # 流行的测试框架
    logging_level="INFO",  # 适当的日志级别
    max_retries=3,  # 合理的重试次数
    timeout=30  # 合理的超时时间
)
```

### 3. 错误处理
```python
from src import AutoProgrammingSystem, Config
from src.exceptions import GenerationError

try:
    system = AutoProgrammingSystem()
    result = system.generate(requirements)
except GenerationError as e:
    print(f"生成错误: {e}")
    # 处理错误
except Exception as e:
    print(f"未知错误: {e}")
    # 处理错误
```

### 4. 结果处理
```python
# 检查生成结果
if result.success:
    # 保存代码
    with open("generated_code.py", "w") as f:
        f.write(result.code)
    
    # 保存报告
    with open("generation_report.md", "w") as f:
        f.write(result.report)
    
    # 运行测试
    if result.run_tests():
        print("测试通过")
    else:
        print("测试失败")
else:
    print(f"生成失败: {result.error}")
```

## 常见场景

### 1. Web API服务
```python
requirements = """
创建一个RESTful API服务，提供以下功能：
1. 用户管理
   - 注册、登录、注销
   - 个人信息管理
2. 商品管理
   - 商品CRUD
   - 商品分类
3. 订单管理
   - 创建订单
   - 订单状态管理
4. 支付集成
   - 支付宝支付
   - 微信支付
"""
```

### 2. 数据处理服务
```python
requirements = """
创建一个数据处理服务，提供以下功能：
1. 数据导入
   - 支持CSV、Excel格式
   - 数据验证和清洗
2. 数据处理
   - 数据转换
   - 数据聚合
3. 数据导出
   - 多种格式支持
   - 自定义导出模板
4. 任务调度
   - 定时任务
   - 任务监控
"""
```

### 3. 机器学习服务
```python
requirements = """
创建一个机器学习服务，提供以下功能：
1. 模型训练
   - 数据预处理
   - 模型训练
   - 模型评估
2. 模型部署
   - 模型保存
   - 模型加载
   - 预测服务
3. 模型管理
   - 版本控制
   - 性能监控
4. API接口
   - 训练接口
   - 预测接口
"""
```

## 相关文档

- [开发指南](../development/README.md)
- [测试文档](../test_results/README.md)
- [API参考](../api-reference.md) 