# 需求分析模块

需求分析模块是全自动编程系统的入口，负责将自然语言需求转换为结构化的编程任务描述。

## 模块架构

需求分析模块由以下子组件组成：

1. **文本预处理器**：清洗和标准化输入文本
2. **语义分析器**：理解需求的意图和实体
3. **DSL转换器**：将语义理解转换为领域特定语言
4. **规范验证器**：确保生成的规范完整且一致

## 自然语言处理流程

```python
class NLPAnalyzer:
    def __init__(self):
        self.pipeline = [
            Tokenization(),
            EntityRecognition(
                patterns={
                    'INPUT': r'\b(输入|参数)\b',
                    'OUTPUT': r'\b(输出|返回)\b',
                    'FUNCTION_TYPE': r'\b(创建|开发|实现|设计)\s+[a-z]+(函数|方法|API|服务)',
                    'CONSTRAINTS': r'\b(必须|应该|需要|用|使用)\s+[^\s,]+'
                }
            ),
            IntentClassification()
        ]
    
    def analyze(self, text: str) -> dict:
        results = {}
        for processor in self.pipeline:
            results.update(processor.process(text))
        return self._format_output(results)
        
    def _format_output(self, results: dict) -> dict:
        """将分析结果格式化为标准DSL规范"""
        return {
            "function_type": self._determine_function_type(results),
            "inputs": self._extract_inputs(results),
            "outputs": self._extract_outputs(results),
            "constraints": results.get("CONSTRAINTS", [])
        }
```

## DSL规范示例

系统将自然语言转换为以下结构化格式：

```json
{
  "function_type": "data_processing",
  "inputs": [
    {"name": "raw_data", "type": "List[Dict]", "description": "原始数据列表"}
  ],
  "outputs": {
    "type": "DataFrame",
    "description": "处理后的结构化数据"
  },
  "steps": [
    {"action": "clean_null_values", "params": {"threshold": 0.8}},
    {"action": "normalize_columns", "params": {"columns": ["price", "quantity"]}}
  ],
  "constraints": [
    "使用pandas库",
    "处理过程不应修改原始数据"
  ]
}
```

## 需求分类

系统支持以下几类需求的分析：

1. **数据处理函数**：处理、转换和清洗数据
2. **API端点**：实现Web服务接口
3. **算法实现**：搜索、排序、优化等算法
4. **工具函数**：辅助功能和通用工具
5. **数据库操作**：查询、存储和检索数据

## 功能类型推断

系统通过关键词和上下文分析确定所需功能的类型：

| 关键词 | 推断功能类型 |
|-------|------------|
| "处理CSV/JSON/数据" | 数据处理函数 |
| "API/端点/服务" | Web API端点 |
| "算法/排序/搜索" | 算法实现 |
| "数据库/存储/查询" | 数据库操作 |

## 约束提取

系统识别并提取以下类型的约束条件：

1. **技术栈约束**：如"使用FastAPI"、"基于SQLAlchemy"
2. **性能约束**：如"必须在O(n)时间内完成"
3. **设计约束**：如"遵循SOLID原则"、"采用工厂模式"
4. **兼容性约束**：如"支持Python 3.8及以上版本"

## 输入/输出类型推断

系统基于上下文自动推断参数和返回值的类型：

```python
def infer_type(description: str) -> str:
    """根据描述推断Python类型"""
    type_patterns = {
        r'\b(列表|数组|list)\b': 'List',
        r'\b(字典|dict|map|映射)\b': 'Dict',
        r'\b(字符串|string|文本)\b': 'str',
        r'\b(整数|int|integer|数字)\b': 'int',
        r'\b(浮点|float|小数)\b': 'float',
        r'\b(布尔|bool|boolean|真假)\b': 'bool',
        r'\b(dataframe|表格|数据帧)\b': 'DataFrame'
    }
    
    for pattern, type_name in type_patterns.items():
        if re.search(pattern, description, re.I):
            return type_name
    
    return 'Any'  # 默认类型
```

## 错误处理

系统实现了健壮的错误处理机制：

1. **歧义检测**：识别和解决需求中的歧义
2. **信息不足处理**：检测并请求缺失信息
3. **异常情况**：处理格式错误和无法解析的需求 