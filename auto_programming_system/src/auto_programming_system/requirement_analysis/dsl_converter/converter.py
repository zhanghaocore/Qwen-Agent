"""
DSL转换器模块
负责将语义分析结果转换为领域特定语言(DSL)表示
"""

from typing import Dict, Any, List, Optional


class DSLConverter:
    """DSL转换器，将语义分析结果转换为规范格式"""
    
    def __init__(self):
        """初始化DSL转换器"""
        pass
    
    def convert(self, semantic_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        将语义分析结果转换为规范格式
        
        Args:
            semantic_result: 语义分析结果
            
        Returns:
            规范化的DSL表示
        """
        # 基本实现 - 直接从语义结果构建规范
        specification = {
            "function_type": semantic_result.get("function_type", "function"),
            "function_name": self._generate_function_name(semantic_result["description"]),
            "description": semantic_result.get("description", ""),
            "parameters": semantic_result.get("parameters", []),
            "return_type": semantic_result.get("return_type", "Any"),
            "return_description": semantic_result.get("return_description", ""),
            "constraints": [],
            "examples": []
        }
        
        return specification
    
    def _generate_function_name(self, description: str) -> str:
        """
        根据描述生成函数名
        
        Args:
            description: 函数描述
            
        Returns:
            生成的函数名
        """
        # 简单实现 - 根据描述提取关键词作为函数名
        words = []
        
        if "计算" in description:
            words.append("calculate")
        elif "转换" in description:
            words.append("convert")
        elif "处理" in description:
            words.append("process")
        elif "过滤" in description or "筛选" in description:
            words.append("filter")
        elif "查找" in description or "搜索" in description:
            words.append("find")
        else:
            words.append("process")
            
        # 添加可能的对象
        if "列表" in description:
            words.append("list")
        elif "字符串" in description:
            words.append("string")
        elif "文件" in description:
            words.append("file")
        elif "数据" in description:
            words.append("data")
            
        # 拼接函数名
        return "_".join(words) 