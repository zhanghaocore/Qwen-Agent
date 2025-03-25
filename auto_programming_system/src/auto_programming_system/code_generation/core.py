"""
代码生成模块的核心类
负责将结构化任务描述转换为Python代码
"""

import os
from typing import Dict, Any, List, Optional, Tuple

from src.code_generation.template_engine.engine import SmartTemplateEngine
from src.code_generation.context_builder.builder import ContextBuilder
from src.code_generation.code_formatter.formatter import CodeFormatter
from src.code_generation.static_analyzer.analyzer import StaticAnalyzer


class CodeGenerator:
    """代码生成器，根据结构化规范生成Python代码"""
    
    def __init__(self, templates_dir: Optional[str] = None):
        """
        初始化代码生成器
        
        Args:
            templates_dir: 代码模板目录，未指定则使用默认目录
        """
        # 使用默认模板目录或自定义目录
        if templates_dir is None:
            package_dir = os.path.dirname(os.path.dirname(__file__))
            templates_dir = os.path.join(package_dir, "templates")
        
        self.template_engine = SmartTemplateEngine(templates_dir)
        self.context_builder = ContextBuilder()
        self.code_formatter = CodeFormatter()
        self.static_analyzer = StaticAnalyzer()
    
    def generate(self, specification: Dict[str, Any]) -> str:
        """
        根据规范生成代码
        
        Args:
            specification: 结构化的任务规范
            
        Returns:
            生成的Python代码
            
        Raises:
            ValueError: 如果规范无效或代码生成失败
        """
        # 1. 构建模板上下文
        context = self.context_builder.build(specification)
        
        # 2. 选择合适的模板并生成代码
        template_name = self._select_template(specification)
        raw_code = self.template_engine.generate(template_name, context)
        
        # 3. 格式化代码
        formatted_code = self.code_formatter.format(raw_code)
        
        # 4. 静态分析检查
        issues = self.static_analyzer.analyze(formatted_code)
        if issues:
            # 记录问题但不阻止返回代码
            print(f"警告: 代码存在以下问题: {issues}")
        
        return formatted_code
    
    def _select_template(self, specification: Dict[str, Any]) -> str:
        """
        基于规范选择最合适的模板
        
        Args:
            specification: 任务规范
            
        Returns:
            模板名称
        """
        # 根据任务类型选择模板
        task_type = specification.get("function_type", "").lower()
        
        if "api" in task_type or "服务" in task_type or "endpoint" in task_type:
            return "apis/fastapi_endpoint"
        
        if "class" in task_type or "类" in task_type:
            return "classes/basic_class"
        
        # 默认生成函数
        return "functions/basic_function"
