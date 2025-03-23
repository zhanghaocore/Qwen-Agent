# API参考文档

本文档详细介绍了全自动Python后端编程系统提供的API接口，以及如何通过编程方式集成和使用这些接口。

## 核心API端点

系统提供REST API用于集成和调用自动编程服务。

### 代码生成API

#### 生成代码

```
POST /api/v1/generate
```

通过自然语言描述生成代码。

**请求体参数：**

```json
{
  "description": "创建一个函数，接收CSV文件路径，读取内容并计算每列的平均值",
  "examples": [
    {
      "inputs": {"file_path": "data.csv"},
      "expected": {"column1": 10.5, "column2": 20.3}
    }
  ],
  "constraints": [
    "使用pandas库",
    "处理文件不存在的情况"
  ],
  "options": {
    "style": "functional",
    "security_level": "standard"
  }
}
```

**响应：**

```json
{
  "status": "success",
  "code": "import pandas as pd\n\ndef calculate_column_means(file_path):\n    \"\"\"读取CSV文件并计算每列的平均值\n    \n    Args:\n        file_path: CSV文件路径\n        \n    Returns:\n        字典，键为列名，值为平均值\n    \"\"\"\n    try:\n        df = pd.read_csv(file_path)\n        return df.mean().to_dict()\n    except FileNotFoundError:\n        print(f\"错误：文件 {file_path} 不存在\")\n        return {}\n",
  "validation": {
    "passed_tests": 2,
    "failed_tests": 0,
    "warnings": []
  }
}
```

#### 优化代码

```
POST /api/v1/optimize
```

优化现有代码。

**请求体参数：**

```json
{
  "code": "def process_data(data):\n    result = []\n    for i in range(len(data)):\n        if data[i] > 0:\n            result.append(data[i] * 2)\n    return result",
  "optimization_goals": ["performance", "readability"],
  "constraints": ["保持功能相同"],
  "validation_report": {
    "performance": {
      "execution_time": 0.05,
      "memory_usage": 15.2
    }
  }
}
```

**响应：**

```json
{
  "status": "success",
  "optimized_code": "def process_data(data):\n    \"\"\"将正数值翻倍并返回结果列表\"\"\"\n    return [x * 2 for x in data if x > 0]",
  "improvements": {
    "performance": {
      "execution_time": 0.02,
      "improvement": "60%"
    },
    "readability": {
      "before_lines": 5,
      "after_lines": 2,
      "improvement": "60%"
    }
  }
}
```

#### 验证代码

```
POST /api/v1/validate
```

测试代码并生成验证报告。

**请求体参数：**

```json
{
  "code": "def find_max(numbers):\n    if not numbers:\n        return None\n    max_val = numbers[0]\n    for num in numbers:\n        if num > max_val:\n            max_val = num\n    return max_val",
  "test_cases": [
    {"inputs": {"numbers": [1, 3, 5, 2]}, "expected": 5},
    {"inputs": {"numbers": [-1, -5, -3]}, "expected": -1},
    {"inputs": {"numbers": []}, "expected": null}
  ],
  "validation_options": {
    "run_performance_tests": true,
    "complexity_analysis": true
  }
}
```

**响应：**

```json
{
  "status": "success",
  "validation_report": {
    "test_results": [
      {"test_id": "test_001", "status": "passed", "execution_time": 0.001},
      {"test_id": "test_002", "status": "passed", "execution_time": 0.001},
      {"test_id": "test_003", "status": "passed", "execution_time": 0.001}
    ],
    "performance": {
      "average_execution_time": 0.001,
      "memory_usage": {"peak": 4.2, "average": 3.8}
    },
    "code_analysis": {
      "complexity": {"cyclomatic": 3, "cognitive": 2},
      "style_issues": []
    }
  }
}
```

## 编程接口

### Python SDK

系统提供Python SDK以编程方式调用其功能。

#### 安装

```bash
pip install autoprogrammer-sdk
```

#### 基本使用

```python
from autoprogrammer import CodeGenerator, CodeValidator, CodeOptimizer

# 初始化代码生成器
generator = CodeGenerator(api_key="your_api_key")

# 生成代码
result = generator.generate(
    description="创建一个函数，接收整数列表，返回所有偶数的和",
    constraints=["使用列表推导式"]
)

print(result.code)
# 输出: def sum_even_numbers(numbers):
#           return sum(num for num in numbers if num % 2 == 0)

# 验证生成的代码
validator = CodeValidator()
validation_report = validator.validate(
    code=result.code,
    test_cases=[
        {"inputs": {"numbers": [1, 2, 3, 4]}, "expected": 6},
        {"inputs": {"numbers": [2, 4, 6]}, "expected": 12}
    ]
)

print(f"通过测试: {validation_report.passed_count}/{validation_report.total_count}")

# 优化代码
optimizer = CodeOptimizer()
optimized_code = optimizer.optimize(
    code=result.code,
    optimization_goals=["performance"]
)

print(optimized_code)
```

#### 高级功能

```python
# 创建完整的应用程序
from autoprogrammer import ApplicationGenerator

app_gen = ApplicationGenerator(api_key="your_api_key")

app = app_gen.create_application(
    description="创建一个简单的待办事项REST API，支持添加、查看和完成任务",
    architecture="fastapi",
    database="sqlite",
    features=["authentication", "task_priority"]
)

# 获取生成的应用程序代码
app_code = app.get_code()

# 获取安装和启动说明
instructions = app.get_instructions()

# 导出为项目目录
app.export("./todo-app")
```

## WebSocket流式API

对于长时间运行的代码生成任务，系统提供WebSocket接口以流式方式接收结果。

### 建立连接

```javascript
const socket = new WebSocket('wss://api.autoprogrammer.example/stream/generate?api_key=your_api_key');

socket.onopen = () => {
  // 发送代码生成请求
  socket.send(JSON.stringify({
    description: "创建一个图像处理应用，能够应用滤镜并调整亮度和对比度",
    complexity: "high",
    architecture: "layered"
  }));
};

// 接收进度更新和结果
socket.onmessage = (event) => {
  const message = JSON.parse(event.data);
  
  if (message.type === 'progress') {
    console.log(`完成进度: ${message.percent}%`);
    console.log(`当前阶段: ${message.current_stage}`);
  } else if (message.type === 'result') {
    console.log('代码生成完成!');
    console.log(message.code);
  } else if (message.type === 'error') {
    console.error(`错误: ${message.message}`);
  }
};

socket.onclose = () => {
  console.log('连接关闭');
};
```

## CLI工具

系统提供命令行工具用于快速生成代码。

### 安装

```bash
pip install -U autoprogrammer-cli
```

### 使用示例

```bash
# 基本代码生成
autocode generate "创建一个函数计算斐波那契数列"

# 指定约束条件
autocode generate "创建一个Web爬虫获取新闻标题" --constraints "使用requests和BeautifulSoup" "处理网络错误"

# 从文件生成
autocode generate-from-file requirements.txt --output spider.py

# 代码优化
autocode optimize code.py --goals performance readability

# 验证代码
autocode validate math_functions.py --test-dir tests/
```

## 错误处理

所有API端点在发生错误时返回标准HTTP错误码和详细的错误信息。

### 常见错误码

| 错误码 | 含义 | 处理方法 |
|------|------|--------|
| 400 | 无效请求 | 检查请求参数是否完整和有效 |
| 401 | 未授权 | 确认API密钥正确并未过期 |
| 403 | 禁止访问 | 确认账户有权限访问该功能 |
| 404 | 资源不存在 | 检查请求的URL是否正确 |
| 429 | 请求过多 | 降低请求频率，遵循限流规则 |
| 500 | 服务器错误 | 稍后重试或联系支持团队 |

### 错误响应示例

```json
{
  "status": "error",
  "code": "invalid_description",
  "message": "需求描述过于模糊，请提供更详细的功能说明",
  "details": {
    "missing_information": ["输入数据类型", "预期输出格式"]
  },
  "request_id": "req_7a1b23c4d5"
}
```

## 限流和使用配额

API使用基于配额的限流机制：

- 免费账户：每日100次请求，最长生成时间30秒
- 专业账户：每日1000次请求，最长生成时间120秒
- 企业账户：定制配额

限流信息通过响应头返回：

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## 版本控制

API版本通过URL路径指定：`/api/v1/generate`

当前可用的API版本：

- v1: 稳定版本，提供基础功能
- v2: Beta版本，支持更多高级功能

## SDK可用语言

- Python: `pip install autoprogrammer-sdk`
- JavaScript/Node.js: `npm install autoprogrammer-js`
- Java: Maven/Gradle依赖：`com.autoprogrammer:sdk:1.0.0`
- Go: `go get github.com/autoprogrammer/sdk-go` 