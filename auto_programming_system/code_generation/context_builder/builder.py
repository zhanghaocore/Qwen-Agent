"""
上下文构建器模块
负责构建模板渲染所需的上下文
"""

from typing import Dict, Any, List, Optional


class ContextBuilder:
    """上下文构建器，为代码模板创建渲染上下文"""
    
    def __init__(self):
        """初始化上下文构建器"""
        pass
    
    def build(self, specification: Dict[str, Any]) -> Dict[str, Any]:
        """
        构建模板上下文
        
        Args:
            specification: 任务规范
            
        Returns:
            模板上下文
        """
        # 基本实现，简单地复制规范
        context = specification.copy()
        
        # 添加导入语句
        context["imports"] = self._generate_imports(specification)
        
        # 添加实现
        if "implementation" not in context:
            context["implementation"] = self._generate_implementation(specification)
        
        return context
    
    def _generate_imports(self, specification: Dict[str, Any]) -> List[str]:
        """
        生成导入语句
        
        Args:
            specification: 任务规范
            
        Returns:
            导入语句列表
        """
        imports = ["from typing import Any, List, Dict, Optional"]
        
        # 根据约束添加导入
        constraints = specification.get("constraints", [])
        for constraint in constraints:
            if "math" in constraint.lower():
                imports.append("import math")
            elif "json" in constraint.lower():
                imports.append("import json")
            elif "random" in constraint.lower():
                imports.append("import random")
            elif "datetime" in constraint.lower():
                imports.append("import datetime")
        
        return imports
    
    def _generate_implementation(self, specification: Dict[str, Any]) -> str:
        """
        生成函数实现
        
        Args:
            specification: 任务规范
            
        Returns:
            函数实现代码
        """
        # 这里只返回一个简单的占位实现
        # 实际应用中，这部分应该基于规范生成真正的代码
        return "# 实现函数逻辑\npass" 