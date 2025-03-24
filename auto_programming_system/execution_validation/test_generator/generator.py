"""
测试生成器模块
负责为生成的代码自动创建测试用例
"""

import ast
import re
from typing import Dict, Any, List, Optional, Tuple, Union


class TestGenerator:
    """测试生成器，为生成的代码创建测试用例"""
    
    def __init__(self):
        """初始化测试生成器"""
        pass
    
    def generate_tests(self, code: str) -> List[Dict[str, Any]]:
        """
        为代码生成测试用例
        
        Args:
            code: 要测试的代码
            
        Returns:
            测试用例列表
        """
        # 解析代码，获取函数定义
        function_info = self._extract_function_info(code)
        
        if not function_info:
            return []
        
        # 生成测试用例
        return self._generate_test_cases(function_info)
    
    def _extract_function_info(self, code: str) -> Optional[Dict[str, Any]]:
        """
        从代码中提取函数信息
        
        Args:
            code: Python代码
            
        Returns:
            函数信息字典或None
        """
        try:
            # 解析代码
            tree = ast.parse(code)
            
            # 查找第一个函数定义
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # 提取函数名
                    function_name = node.name
                    
                    # 提取参数
                    params = []
                    for arg in node.args.args:
                        param_name = arg.arg
                        # 尝试获取类型注解
                        param_type = None
                        if arg.annotation and isinstance(arg.annotation, ast.Name):
                            param_type = arg.annotation.id
                        
                        params.append({
                            "name": param_name,
                            "type": param_type
                        })
                    
                    # 提取返回类型
                    return_type = None
                    if node.returns and isinstance(node.returns, ast.Name):
                        return_type = node.returns.id
                    
                    # 提取文档字符串
                    docstring = ast.get_docstring(node)
                    
                    return {
                        "function_name": function_name,
                        "parameters": params,
                        "return_type": return_type,
                        "docstring": docstring
                    }
            
            return None
        except SyntaxError:
            return None
    
    def _generate_test_cases(self, function_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        根据函数信息生成测试用例
        
        Args:
            function_info: 函数信息字典
            
        Returns:
            测试用例列表
        """
        test_cases = []
        
        # 从文档字符串中提取示例
        examples = self._extract_examples_from_docstring(function_info.get("docstring", ""))
        if examples:
            test_cases.extend(examples)
        
        # 如果没有示例，则生成基本测试用例
        if not test_cases:
            # 为每个参数生成合适的测试值
            basic_tests = self._generate_basic_tests(function_info)
            test_cases.extend(basic_tests)
        
        return test_cases
    
    def _extract_examples_from_docstring(self, docstring: Optional[str]) -> List[Dict[str, Any]]:
        """
        从文档字符串中提取示例
        
        Args:
            docstring: 函数文档字符串
            
        Returns:
            测试用例列表
        """
        if not docstring:
            return []
        
        examples = []
        
        # 查找示例部分
        example_pattern = r'>>>(.+?)\n(.+?)(?:\n\n|$)'
        matches = re.findall(example_pattern, docstring, re.DOTALL)
        
        for call, output in matches:
            # 解析函数调用
            call = call.strip()
            output = output.strip()
            
            # 提取函数名和参数
            match = re.match(r'(\w+)\((.*)\)', call)
            if match:
                function_name = match.group(1)
                args_str = match.group(2).strip()
                
                # 简单解析参数（实际应用中应该更加严谨）
                inputs = {}
                if args_str:
                    # 假设参数都是简单的值或键值对
                    if "=" in args_str:
                        # 关键字参数
                        for pair in args_str.split(","):
                            if "=" in pair:
                                key, value = pair.split("=", 1)
                                inputs[key.strip()] = self._parse_value(value.strip())
                    else:
                        # 位置参数，使用indices作为键
                        for i, value in enumerate(args_str.split(",")):
                            inputs[f"param{i+1}"] = self._parse_value(value.strip())
                
                # 解析预期输出
                expected = self._parse_value(output)
                
                examples.append({
                    "inputs": inputs,
                    "expected": expected
                })
        
        return examples
    
    def _generate_basic_tests(self, function_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        生成基本测试用例
        
        Args:
            function_info: 函数信息
            
        Returns:
            测试用例列表
        """
        test_cases = []
        
        # 为每个参数准备适当的测试值
        inputs = {}
        for param in function_info["parameters"]:
            param_name = param["name"]
            param_type = param.get("type")
            
            # 根据参数类型生成测试值
            inputs[param_name] = self._generate_test_value(param_type)
        
        # 添加一个基本测试用例（假设返回空值）
        test_cases.append({
            "inputs": inputs,
            "expected": None  # 实际应用中应该更智能地预测函数输出
        })
        
        return test_cases
    
    def _parse_value(self, value_str: str) -> Any:
        """
        解析值字符串
        
        Args:
            value_str: 值字符串
            
        Returns:
            解析后的值
        """
        try:
            # 尝试作为Python表达式求值
            return eval(value_str, {"__builtins__": {}})
        except:
            # 如果无法求值，则返回原始字符串
            return value_str
    
    def _generate_test_value(self, type_hint: Optional[str]) -> Any:
        """
        根据类型提示生成测试值
        
        Args:
            type_hint: 类型提示
            
        Returns:
            生成的测试值
        """
        if not type_hint:
            return "test"
            
        type_hint = type_hint.lower()
        
        if "int" in type_hint:
            return 42
        elif "float" in type_hint:
            return 3.14
        elif "bool" in type_hint:
            return True
        elif "list" in type_hint:
            return [1, 2, 3]
        elif "dict" in type_hint:
            return {"key": "value"}
        elif "str" in type_hint:
            return "test"
        else:
            return "test"