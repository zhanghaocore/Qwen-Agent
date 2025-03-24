"""
语义分析器模块
负责分析预处理后的需求文本，提取关键概念和关系
"""

from typing import Dict, Any, List, Optional


class SemanticAnalyzer:
    """语义分析器，将预处理文本转换为语义表示"""
    
    def __init__(self):
        """初始化语义分析器"""
        pass
    
    def analyze(self, text: str, original_text: str = None) -> Dict[str, Any]:
        """
        分析预处理后的文本，提取语义信息
        
        Args:
            text: 预处理后的需求文本
            original_text: 原始需求文本（如果None则使用预处理文本）
            
        Returns:
            包含语义信息的字典
        """
        # 使用原始文本作为描述，如果未提供则使用预处理文本
        description = original_text if original_text is not None else text
        
        # 基本实现 - 提取函数类型和功能描述
        result = {
            "function_type": "function",
            "description": description,
            "parameters": [],
            "return_type": "Any",
            "return_description": "函数返回值"
        }
        
        # 简单的参数提取逻辑
        if "接收" in text and "返回" in text:
            param_text = text.split("接收")[1].split("返回")[0].strip()
            if "," in param_text or "，" in param_text:
                params = param_text.replace("，", ",").split(",")
                for i, p in enumerate(params):
                    param_type = "str"
                    if "整数" in p or "数字" in p:
                        param_type = "int"
                    elif "列表" in p or "数组" in p:
                        param_type = "List"
                    result["parameters"].append({
                        "name": f"param{i+1}",
                        "type": param_type,
                        "description": p.strip()
                    })
            else:
                param_type = "str"
                if "整数" in param_text or "数字" in param_text:
                    param_type = "int"
                elif "列表" in param_text or "数组" in param_text:
                    param_type = "List"
                result["parameters"].append({
                    "name": "param1",
                    "type": param_type,
                    "description": param_text.strip()
                })
        
        return result 