# 迭代优化机制

迭代优化机制负责基于验证结果和反馈持续改进生成的代码，使其达到更高的质量和性能水平。

## 模块架构

优化模块由以下核心组件组成：

1. **反馈解析器**：解析验证报告和反馈信息
2. **优化策略引擎**：确定代码需要哪些改进
3. **代码变体生成器**：生成改进版本的代码
4. **变体评估系统**：评估生成变体的质量
5. **版本控制器**：管理代码的多个版本和演化历史

## 反馈分析流程

```python
class FeedbackAnalyzer:
    def __init__(self):
        self.analyzers = {
            'performance': PerformanceAnalyzer(),
            'errors': ErrorAnalyzer(),
            'style': StyleAnalyzer(),
            'complexity': ComplexityAnalyzer()
        }
    
    def analyze(self, code: str, validation_report: dict) -> dict:
        """分析验证报告并生成优化建议"""
        optimization_targets = {}
        
        # 针对每个维度进行分析
        for aspect, analyzer in self.analyzers.items():
            if aspect in validation_report:
                aspect_feedback = analyzer.analyze(
                    code, validation_report[aspect]
                )
                if aspect_feedback:
                    optimization_targets[aspect] = aspect_feedback
        
        return {
            'code': code,
            'validation_report': validation_report,
            'optimization_targets': optimization_targets,
            'priority': self._determine_priority(optimization_targets)
        }
    
    def _determine_priority(self, targets: dict) -> list:
        """确定优化的优先级"""
        # 首先修复错误，然后改进性能，最后处理风格问题
        priorities = []
        
        if 'errors' in targets:
            priorities.append('errors')
        if 'performance' in targets:
            priorities.append('performance')
        if 'complexity' in targets:
            priorities.append('complexity')
        if 'style' in targets:
            priorities.append('style')
            
        return priorities
```

## 遗传算法优化

系统使用遗传算法生成和筛选代码变体：

```python
class GeneticOptimizer:
    def __init__(self, population_size=10, generations=5):
        self.population_size = population_size
        self.generations = generations
        self.mutation_operators = [
            RenamingMutator(),
            LoopOptimizationMutator(),
            DataStructureMutator(),
            AlgorithmReplacementMutator()
        ]
    
    def optimize(self, code: str, optimization_targets: dict) -> str:
        """使用遗传算法优化代码"""
        # 初始化种群
        population = self._initialize_population(code)
        
        # 进化多代
        for generation in range(self.generations):
            # 评估种群
            fitness_scores = self._evaluate_population(
                population, optimization_targets
            )
            
            # 选择最佳个体
            elite = self._select_elite(population, fitness_scores)
            
            # 生成下一代
            next_generation = [elite[0]]  # 保留最佳个体
            
            while len(next_generation) < self.population_size:
                # 交叉和变异
                parent1, parent2 = self._select_parents(population, fitness_scores)
                child = self._crossover(parent1, parent2)
                child = self._mutate(child, optimization_targets)
                next_generation.append(child)
            
            population = next_generation
        
        # 返回最佳个体
        return self._get_best_individual(population, optimization_targets)
    
    def _mutate(self, code: str, targets: dict) -> str:
        """应用变异操作符"""
        # 选择合适的变异操作符
        applicable_mutators = [
            m for m in self.mutation_operators
            if m.is_applicable(code, targets)
        ]
        
        if not applicable_mutators:
            return code
            
        # 随机选择一个变异操作符
        mutator = random.choice(applicable_mutators)
        return mutator.apply(code, targets)
```

## 优化策略

系统实现了多种代码优化策略：

### 1. 性能优化策略

```python
class PerformanceOptimizer:
    def optimize(self, code: str, targets: dict) -> str:
        """优化代码性能"""
        optimizations = []
        
        # 数据结构优化
        if 'data_structure' in targets.get('performance', {}):
            optimizations.append(self._optimize_data_structures(code))
            
        # 算法复杂度优化
        if 'algorithm_complexity' in targets.get('performance', {}):
            optimizations.append(self._optimize_algorithm(code))
            
        # 缓存优化
        if 'caching' in targets.get('performance', {}):
            optimizations.append(self._add_caching(code))
            
        # 合并所有优化
        for opt in optimizations:
            code = self._apply_optimization(code, opt)
            
        return code
    
    def _optimize_data_structures(self, code: str) -> dict:
        """优化数据结构选择"""
        replacements = []
        
        # 例如，将列表替换为集合进行成员检查
        if re.search(r'if \w+ in \w+:', code) and 'list(' in code:
            replacements.append({
                'pattern': r'(\w+) = list\((.*?)\)',
                'replacement': r'\1 = set(\2)'
            })
            
        return {'type': 'data_structure', 'replacements': replacements}
```

### 2. 代码复杂度优化策略

```python
class ComplexityOptimizer:
    def optimize(self, code: str, targets: dict) -> str:
        """优化代码复杂度"""
        tree = ast.parse(code)
        transformer = ComplexityReducingTransformer()
        transformed_tree = transformer.visit(tree)
        return ast.unparse(transformed_tree)

class ComplexityReducingTransformer(ast.NodeTransformer):
    def visit_If(self, node):
        self.generic_visit(node)
        
        # 简化嵌套条件
        if isinstance(node.body[0], ast.If) and not node.orelse:
            # 合并条件: if A: if B: X  => if A and B: X
            nested_if = node.body[0]
            combined_test = ast.BoolOp(
                op=ast.And(),
                values=[node.test, nested_if.test]
            )
            return ast.If(
                test=combined_test,
                body=nested_if.body,
                orelse=nested_if.orelse
            )
            
        return node
```

### 3. 代码风格优化策略

```python
class StyleOptimizer:
    def optimize(self, code: str, targets: dict) -> str:
        """优化代码风格"""
        # 使用Black格式化
        import black
        
        try:
            return black.format_str(
                code, mode=black.FileMode()
            )
        except Exception:
            # 如果Black格式化失败，使用自定义格式化
            return self._custom_format(code)
    
    def _custom_format(self, code: str) -> str:
        """自定义代码格式化"""
        formatted = []
        indent = 0
        
        for line in code.split('\n'):
            # 处理缩进
            stripped = line.lstrip()
            
            # 减少缩进: 右括号、结束关键字等
            if stripped.startswith((')', ']', '}')):
                indent -= 4
                
            # 添加格式化后的行
            formatted.append(' ' * indent + stripped)
            
            # 增加缩进: 左括号、开始关键字等
            if stripped.endswith((':', '(', '[', '{')):
                indent += 4
                
        return '\n'.join(formatted)
```

## 代码版本管理

系统使用轻量级版本控制跟踪代码演化：

```python
class CodeVersionControl:
    def __init__(self):
        self.versions = []
        self.current_index = -1
        
    def commit(self, code: str, message: str) -> int:
        """保存代码版本"""
        version_id = len(self.versions)
        timestamp = datetime.datetime.now().isoformat()
        
        self.versions.append({
            'id': version_id,
            'code': code,
            'message': message,
            'timestamp': timestamp,
            'metrics': self._calculate_metrics(code)
        })
        
        self.current_index = version_id
        return version_id
    
    def checkout(self, version_id: int) -> str:
        """获取特定版本的代码"""
        if 0 <= version_id < len(self.versions):
            self.current_index = version_id
            return self.versions[version_id]['code']
        raise ValueError(f"Version ID {version_id} does not exist")
    
    def get_diff(self, from_version: int, to_version: int) -> str:
        """获取版本间的差异"""
        if 0 <= from_version < len(self.versions) and 0 <= to_version < len(self.versions):
            from difflib import unified_diff
            
            from_code = self.versions[from_version]['code'].splitlines()
            to_code = self.versions[to_version]['code'].splitlines()
            
            diff = unified_diff(
                from_code, to_code,
                fromfile=f'v{from_version}',
                tofile=f'v{to_version}',
                lineterm=''
            )
            
            return '\n'.join(diff)
            
        raise ValueError("Invalid version IDs")
    
    def get_history(self) -> list:
        """获取版本历史"""
        return [{
            'id': v['id'],
            'message': v['message'],
            'timestamp': v['timestamp'],
            'metrics': v['metrics']
        } for v in self.versions]
```

## 优化指标

系统使用以下指标评估代码质量改进：

| 指标类别 | 指标名称 | 描述 |
|---------|----------|------|
| 性能 | 执行时间 | 代码执行所需的平均时间 |
| 性能 | 内存使用 | 代码执行期间的内存峰值 |
| 复杂度 | 圈复杂度 | 代码的分支和决策路径数量 |
| 复杂度 | 维护指数 | 代码的可维护性评分 |
| 风格 | PEP8符合度 | 符合PEP8标准的程度 |
| 风格 | 文档完整性 | 文档字符串的覆盖率和质量 |
| 可靠性 | 测试通过率 | 通过的测试用例百分比 |
| 可靠性 | 错误处理覆盖 | 包含错误处理的代码比例 |

## LLM辅助优化

对于复杂的优化任务，系统使用大型语言模型提供辅助：

```python
class LLMOptimizationAssistant:
    def __init__(self, model="gpt-4"):
        self.client = OpenAI()
        self.model = model
        
    def optimize(self, code: str, validation_report: dict) -> str:
        """使用LLM优化代码"""
        prompt = self._build_optimization_prompt(code, validation_report)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert Python developer focusing on code optimization."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=2000
        )
        
        return self._extract_optimized_code(response.choices[0].message.content)
    
    def _build_optimization_prompt(self, code: str, report: dict) -> str:
        """构建优化提示"""
        prompt = "I need to optimize the following Python code based on validation feedback.\n\n"
        prompt += f"```python\n{code}\n```\n\n"
        
        prompt += "Validation report:\n"
        if 'test_results' in report:
            prompt += f"- Passed tests: {report['validation_summary']['passed_tests']}\n"
            prompt += f"- Failed tests: {report['validation_summary']['failed_tests']}\n"
            
            # 添加失败的测试用例详情
            if report['validation_summary']['failed_tests'] > 0:
                prompt += "\nFailed test cases:\n"
                for test in [t for t in report['test_results'] if t['status'] == 'failed']:
                    prompt += f"- Input: {test['inputs']}, Expected: {test['expected']}, Got: {test['actual']}"
                    if 'error' in test:
                        prompt += f", Error: {test['error']}"
                    prompt += "\n"
        
        if 'code_analysis' in report:
            prompt += "\nCode analysis issues:\n"
            if 'complexity' in report['code_analysis']:
                prompt += f"- Complexity: {report['code_analysis']['complexity']}\n"
            if 'style_issues' in report['code_analysis']:
                prompt += "- Style issues:\n"
                for issue in report['code_analysis']['style_issues']:
                    prompt += f"  - Line {issue['line']}: {issue['message']}\n"
        
        if 'performance' in report:
            prompt += f"\nPerformance metrics:\n"
            prompt += f"- Average execution time: {report['performance']['average_execution_time']} seconds\n"
            if 'memory_usage' in report['performance']:
                prompt += f"- Peak memory usage: {report['performance']['memory_usage']['peak']} MB\n"
                
        prompt += "\nPlease optimize this code to address the issues in the validation report. Focus on:\n"
        prompt += "1. Fixing any bugs or errors\n"
        prompt += "2. Improving performance\n"
        prompt += "3. Reducing complexity\n"
        prompt += "4. Enhancing readability and style\n\n"
        prompt += "Return only the optimized code without explanations."
        
        return prompt
``` 