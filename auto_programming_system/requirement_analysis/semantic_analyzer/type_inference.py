"""
类型推断系统
负责从需求文本中推断变量和参数的类型
"""

from typing import Dict, Any, List, Optional, Union

class TypeInferenceSystem:
    """类型推断系统"""
    
    def __init__(self):
        """初始化类型推断系统"""
        self.type_hints = {
            "id": "int",
            "name": "str",
            "email": "str",
            "phone": "str",
            "date": "datetime.date",
            "time": "datetime.time",
            "timestamp": "datetime.datetime",
            "price": "float",
            "quantity": "int",
            "status": "str",
            "is_": "bool",
            "has_": "bool",
            "url": "str",
            "file": "str",
            "path": "str",
            "content": "str",
            "data": "dict",
            "list": "list",
            "count": "int",
            "total": "float",
            "average": "float",
            "min": "float",
            "max": "float"
        }
    
    def infer_type(self, variable_name: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        推断变量类型
        
        Args:
            variable_name: 变量名
            context: 上下文信息，可用于更准确的推断
            
        Returns:
            推断出的类型名称
        """
        # 1. 检查变量名中的类型提示
        for hint, type_name in self.type_hints.items():
            if variable_name.lower().startswith(hint) or variable_name.lower().endswith(hint):
                return type_name
        
        # 2. 使用上下文进行推断
        if context:
            # 从上下文中获取类型信息
            type_info = context.get("type_hints", {}).get(variable_name)
            if type_info:
                return type_info
            
            # 从示例值推断类型
            example_value = context.get("examples", {}).get(variable_name)
            if example_value is not None:
                return self._infer_type_from_value(example_value)
        
        # 默认返回字符串类型
        return "str"
    
    def _infer_type_from_value(self, value: Any) -> str:
        """
        从值推断类型
        
        Args:
            value: 任意值
            
        Returns:
            推断出的类型名称
        """
        if isinstance(value, bool):
            return "bool"
        elif isinstance(value, int):
            return "int"
        elif isinstance(value, float):
            return "float"
        elif isinstance(value, list):
            return "list"
        elif isinstance(value, dict):
            return "dict"
        elif isinstance(value, (set, frozenset)):
            return "set"
        elif isinstance(value, tuple):
            return "tuple"
        else:
            return "str"
    
    def suggest_type_annotations(self, function_params: List[str], context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        为函数参数生成类型注解建议
        
        Args:
            function_params: 函数参数名列表
            context: 上下文信息
            
        Returns:
            参数名到类型注解的映射
        """
        annotations = {}
        for param in function_params:
            annotations[param] = self.infer_type(param, context)
        return annotations 