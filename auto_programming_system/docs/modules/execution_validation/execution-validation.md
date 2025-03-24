# 执行验证环境

执行验证环境负责安全地运行生成的代码，验证其正确性和性能，并提供详细的反馈报告。

## 模块架构

执行验证模块由以下核心组件组成：

1. **安全沙箱**：隔离环境中执行代码
2. **测试生成器**：自动生成测试用例
3. **验证执行器**：运行测试并收集结果
4. **代码分析器**：分析代码性能和质量
5. **报告生成器**：生成详细的验证报告

## 沙箱安全策略

```python
from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins

class SafeSandbox:
    def __init__(self, security_level="standard"):
        self.security_level = security_level
        self.allowed_builtins = self._get_allowed_builtins()
        self.import_whitelist = self._get_import_whitelist()
        self.max_execution_time = self._get_execution_timeout()
        
    def _get_allowed_builtins(self):
        """获取允许的内置函数"""
        standard_safe = {
            'len', 'str', 'int', 'float', 'list', 'dict', 'set',
            'tuple', 'bool', 'sum', 'range', 'map', 'filter', 'zip',
            'enumerate', 'sorted', 'min', 'max', 'all', 'any',
            'abs', 'round', 'pow', 'type', 'isinstance'
        }
        
        if self.security_level == "relaxed":
            return standard_safe | {'open'}
        
        return standard_safe
    
    def _get_import_whitelist(self):
        """获取允许导入的模块"""
        standard_imports = {
            'math', 'datetime', 'collections', 'itertools',
            'functools', 're', 'json', 'csv'
        }
        
        if self.security_level == "data_science":
            return standard_imports | {'pandas', 'numpy'}
        
        return standard_imports
    
    def execute(self, code: str, inputs: dict) -> dict:
        """在沙箱中执行代码"""
        # 创建受限环境
        restricted_globals = {
            '__builtins__': self._create_safe_builtins(),
            '_getattr_': self._create_getattr_guard(),
            '_write_': self._create_write_guard()
        }
        
        # 编译受限代码
        byte_code = compile_restricted(code, '<generated>', 'exec')
        
        # 使用超时装饰器限制执行时间
        with timeout(self.max_execution_time):
            # 执行代码
            exec(byte_code, restricted_globals)
            
            # 提取并调用生成的主函数
            main_func = self._find_main_function(restricted_globals)
            if main_func:
                result = main_func(**inputs)
                return {'status': 'success', 'result': result}
            
        return {'status': 'error', 'message': 'No executable function found'}
```

## 测试用例生成

系统使用多种策略自动生成测试用例：

```python
class TestGenerator:
    def __init__(self):
        self.strategies = [
            EdgeCaseStrategy(),
            RandomDataStrategy(),
            HypothesisBasedStrategy()
        ]
    
    def generate_test_cases(self, spec: dict) -> list:
        """根据任务规范生成测试用例"""
        test_cases = []
        
        for strategy in self.strategies:
            test_cases.extend(strategy.generate(spec))
            
        # 去重和筛选测试用例
        return self._filter_test_cases(test_cases)
    
    def _filter_test_cases(self, test_cases: list) -> list:
        """过滤和排序测试用例，确保覆盖范围和多样性"""
        # 实现测试用例筛选逻辑
        return sorted_unique_tests
```

### 测试策略实现

```python
class EdgeCaseStrategy:
    """边界情况测试策略"""
    
    def generate(self, spec: dict) -> list:
        test_cases = []
        
        # 为每个输入参数生成边界值
        for param in spec['inputs']:
            if param['type'] == 'int' or param['type'] == 'float':
                test_cases.append(self._generate_numeric_edge_cases(param, spec))
            elif param['type'].startswith('List'):
                test_cases.append(self._generate_list_edge_cases(param, spec))
            # 其他类型的边界情况处理...
            
        return test_cases

class HypothesisBasedStrategy:
    """基于假设驱动的测试策略"""
    
    def generate(self, spec: dict) -> list:
        from hypothesis import strategies as st
        
        # 定义参数策略
        param_strategies = {}
        for param in spec['inputs']:
            param_strategies[param['name']] = self._get_strategy_for_type(param['type'])
        
        # 使用Hypothesis生成测试用例
        @given(**param_strategies)
        def property_test(**kwargs):
            # 属性测试定义
            pass
            
        # 运行属性测试并收集示例
        return self._collect_examples(property_test)
```

## 验证流程

执行验证环境使用以下流程验证生成的代码：

1. **静态分析**：在执行前进行代码静态分析
   - 语法检查
   - 安全漏洞扫描
   - 复杂度分析

2. **动态测试**：在沙箱中运行测试用例
   - 功能正确性测试
   - 边界条件测试
   - 输入输出验证

3. **性能评估**：测量代码性能指标
   - 执行时间
   - 内存使用
   - 资源消耗

## 验证报告格式

系统生成结构化的验证报告：

```json
{
  "validation_summary": {
    "status": "passed",  // "passed", "partial", "failed"
    "passed_tests": 18,
    "failed_tests": 2,
    "overall_score": 0.9
  },
  "test_results": [
    {
      "test_id": "test_001",
      "inputs": {"data": [1, 2, 3], "operation": "sum"},
      "expected": 6,
      "actual": 6,
      "status": "passed",
      "execution_time": 0.003
    },
    {
      "test_id": "test_002",
      "inputs": {"data": [], "operation": "sum"},
      "expected": 0,
      "actual": null,
      "status": "failed",
      "error": "TypeError: 'NoneType' object is not iterable"
    }
  ],
  "code_analysis": {
    "complexity": {
      "cyclomatic": 4,
      "halstead": 12.5,
      "maintenance_index": 65
    },
    "style_issues": [
      {"line": 15, "message": "Line too long (125 > 120 characters)"}
    ]
  },
  "performance": {
    "average_execution_time": 0.005,
    "memory_usage": {
      "peak": 128.5,
      "average": 52.3
    }
  },
  "security_scan": {
    "issues": []
  }
}
```

## 验证器扩展点

系统支持自定义验证规则和测试策略：

```python
class ValidationExtensionManager:
    def __init__(self):
        self.test_strategies = {}
        self.validation_rules = {}
        
    def register_test_strategy(self, name: str, strategy_class):
        """注册自定义测试策略"""
        self.test_strategies[name] = strategy_class
        
    def register_validation_rule(self, name: str, rule_class):
        """注册自定义验证规则"""
        self.validation_rules[name] = rule_class
        
    def create_validator(self, config: dict) -> CodeValidator:
        """创建自定义验证器"""
        validator = CodeValidator()
        
        # 添加配置的测试策略
        for strategy_name in config.get('test_strategies', []):
            if strategy_name in self.test_strategies:
                validator.add_test_strategy(
                    self.test_strategies[strategy_name]()
                )
        
        # 添加配置的验证规则
        for rule_name in config.get('validation_rules', []):
            if rule_name in self.validation_rules:
                validator.add_validation_rule(
                    self.validation_rules[rule_name]()
                )
        
        return validator
```

## 错误修复建议

系统能够为验证过程中发现的问题提供修复建议：

```python
class ErrorAnalyzer:
    def analyze(self, code: str, error: Exception, test_case: dict) -> dict:
        """分析错误并提供修复建议"""
        if isinstance(error, TypeError):
            return self._analyze_type_error(code, error, test_case)
        elif isinstance(error, IndexError):
            return self._analyze_index_error(code, error, test_case)
        elif isinstance(error, ZeroDivisionError):
            return self._analyze_zero_division(code, error, test_case)
        # 其他错误类型分析
        
        return {
            "error_type": type(error).__name__,
            "message": str(error),
            "suggestion": "检查代码逻辑和输入验证"
        }
    
    def _analyze_type_error(self, code: str, error: TypeError, test_case: dict) -> dict:
        """分析类型错误"""
        # 使用AST分析代码
        # 定位可能的问题位置
        # 提供修复建议
        
        return {
            "error_type": "TypeError",
            "message": str(error),
            "line": problematic_line,
            "suggestion": "添加类型检查或转换",
            "fix_example": "if not isinstance(data, list): data = []"
        }
``` 