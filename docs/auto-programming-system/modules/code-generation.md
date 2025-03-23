# 代码生成模块

代码生成模块是系统的核心引擎，负责将结构化任务描述转换为高质量的Python代码。

## 模块架构

代码生成模块由以下核心组件组成：

1. **模板选择器**：选择最适合当前任务的代码模板
2. **上下文构建器**：准备代码生成所需的上下文信息
3. **代码生成引擎**：渲染模板或调用LLM生成代码
4. **代码格式化器**：确保生成的代码符合PEP8等规范
5. **静态分析器**：检查代码质量和潜在问题

## 模板引擎设计

```python
class SmartTemplateEngine:
    def __init__(self):
        self.jinja_env = Environment(
            loader=PackageLoader('autoprogrammer', 'templates'),
            autoescape=select_autoescape(['py']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        self.register_custom_filters()
        
    def register_custom_filters(self):
        """注册自定义Jinja2过滤器"""
        self.jinja_env.filters['camelcase'] = lambda s: ''.join(
            word.capitalize() for word in s.split('_')
        )
        self.jinja_env.filters['docstring'] = self._format_docstring
    
    def generate(self, template_name: str, context: dict) -> str:
        """生成代码"""
        template = self.jinja_env.get_template(f"{template_name}.py.jinja")
        return template.render(**self._enrich_context(context))
    
    def _enrich_context(self, context: dict) -> dict:
        """增强上下文"""
        enriched = context.copy()
        
        # 添加类型注释
        if 'inputs' in enriched:
            for input_param in enriched['inputs']:
                if 'type' not in input_param:
                    input_param['type'] = self._infer_type(input_param)
        
        # 添加导入语句
        enriched['imports'] = self._generate_imports(enriched)
        
        return enriched
```

## 代码模板示例

系统包含多种代码模板，每种对应不同类型的功能：

### 数据处理函数模板

```python
# {{ template_info.name }}: {{ template_info.description }}
{% for import_stmt in imports %}
{{ import_stmt }}
{% endfor %}

def {{ function_name }}({% for param in inputs %}{{ param.name }}: {{ param.type }}{% if not loop.last %}, {% endif %}{% endfor %}) -> {{ outputs.type }}:
    """
    {{ function_description }}
    
    {% for param in inputs %}
    Args:
        {{ param.name }}: {{ param.description }}
    {% endfor %}
    
    Returns:
        {{ outputs.description }}
    """
    {% for step in steps %}
    # {{ step.description }}
    {% if step.action == 'clean_null_values' %}
    data = data.dropna(thresh=len(data.columns) * {{ step.params.threshold }})
    {% elif step.action == 'normalize_columns' %}
    for column in [{% for col in step.params.columns %}"{{ col }}"{% if not loop.last %}, {% endif %}{% endfor %}]:
        if column in data:
            data[column] = (data[column] - data[column].mean()) / data[column].std()
    {% endif %}
    {% endfor %}
    
    return data
```

## 代码质量检查规则

系统使用以下规则检查生成的代码质量：

```yaml
code_rules:
  complexity:
    max_cyclomatic: 15        # 最大圈复杂度
    max_nesting: 3            # 最大嵌套深度
  style:
    enforce_pep8: true        # 确保符合PEP8规范
    line_length: 120          # 最大行长度
  safety:
    forbidden_functions:      # 禁止使用的函数
      - eval
      - exec
      - os.system
    avoid_global_state: true  # 避免全局状态
  performance:
    prefer_list_comprehension: true  # 优先使用列表推导式
```

## 代码生成策略

系统支持多种代码生成策略，根据任务复杂度自动选择：

1. **模板渲染**：简单任务直接使用模板渲染
2. **模板+LLM融合**：中等复杂度任务使用模板基础结构，LLM填充复杂逻辑
3. **纯LLM生成**：复杂任务直接使用大模型生成全部代码
4. **组件组合**：将任务分解为多个组件，单独生成后组合

## LLM代码生成

对于复杂任务，系统使用LLM生成代码：

```python
class LLMCodeGenerator:
    def __init__(self, model="gpt-4"):
        self.client = OpenAI()
        self.model = model
    
    def generate(self, spec: dict) -> str:
        """使用LLM生成代码"""
        prompt = self._build_prompt(spec)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert Python developer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1500
        )
        
        return self._extract_code(response.choices[0].message.content)
    
    def _build_prompt(self, spec: dict) -> str:
        """构建LLM提示"""
        prompt = f"Write a Python function that {spec['function_description']}.\n\n"
        
        prompt += "Input parameters:\n"
        for param in spec['inputs']:
            prompt += f"- {param['name']}: {param['type']} - {param['description']}\n"
        
        prompt += f"\nOutput: {spec['outputs']['type']} - {spec['outputs']['description']}\n\n"
        
        if 'constraints' in spec:
            prompt += "Additional requirements:\n"
            for constraint in spec['constraints']:
                prompt += f"- {constraint}\n"
        
        prompt += "\nReturn only the Python code without explanations."
        
        return prompt
```

## 代码注释生成

系统自动添加代码注释，提高可读性：

```python
def add_code_comments(code: str, spec: dict) -> str:
    """为生成的代码添加有意义的注释"""
    # 解析抽象语法树
    tree = ast.parse(code)
    
    # 为函数添加文档字符串
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            node.body.insert(0, ast.Expr(
                value=ast.Constant(
                    value=generate_docstring(node, spec)
                )
            ))
    
    # 为复杂逻辑添加行注释
    # ...省略实现...
    
    return ast.unparse(tree)
```

## 默认库包含

系统根据任务类型自动包含常用库：

| 任务类型 | 默认库 |
|---------|-------|
| 数据处理 | pandas, numpy |
| Web API | fastapi, pydantic |
| 数据库操作 | sqlalchemy, sqlite3 |
| 算法实现 | collections, heapq | 