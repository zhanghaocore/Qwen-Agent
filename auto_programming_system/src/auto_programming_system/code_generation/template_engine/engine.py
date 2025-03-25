"""
智能模板引擎模块
负责根据上下文渲染代码模板
"""

import os
import jinja2
from typing import Dict, Any, List, Optional


class SmartTemplateEngine:
    """智能模板引擎，根据上下文渲染代码模板"""
    
    def __init__(self, templates_dir: str):
        """
        初始化模板引擎
        
        Args:
            templates_dir: 模板目录路径
        """
        self.templates_dir = templates_dir
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(templates_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def generate(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        生成代码
        
        Args:
            template_name: 模板名称
            context: 模板上下文
            
        Returns:
            生成的代码
            
        Raises:
            ValueError: 模板不存在
        """
        # 添加.py.jinja扩展名（如果没有）
        if not template_name.endswith(".py.jinja"):
            template_name = f"{template_name}.py.jinja"
        
        try:
            template = self.env.get_template(template_name)
            return template.render(**context)
        except jinja2.exceptions.TemplateNotFound:
            fallback_code = self._generate_fallback_code(context)
            return fallback_code
    
    def _generate_fallback_code(self, context: Dict[str, Any]) -> str:
        """
        在模板不存在时生成备用代码
        
        Args:
            context: 模板上下文
            
        Returns:
            生成的备用代码
        """
        # 生成简单的函数定义
        function_name = context.get("function_name", "process_data")
        description = context.get("description", "处理数据")
        parameters = context.get("parameters", [])
        return_type = context.get("return_type", "Any")
        
        # 生成参数字符串
        param_list = []
        for param in parameters:
            param_name = param.get("name", "param")
            param_type = param.get("type", "Any")
            param_list.append(f"{param_name}: {param_type}")
        
        param_str = ", ".join(param_list)
        
        # 生成函数定义
        code = f'''"""
{description}
"""

from typing import Any, List, Dict

def {function_name}({param_str}) -> {return_type}:
    """
    {description}
    
    Args:
        {param_str.replace(": ", ": ")}
        
    Returns:
        处理结果
    """
    # 基本实现
    pass
'''
        return code 