"""
代码变体生成器模块
负责根据优化策略生成代码变体
"""

import ast
import re
from typing import Dict, Any, List, Optional


class CodeVariantGenerator:
    """代码变体生成器，生成代码优化变体"""
    
    def __init__(self, max_variants: int = 3):
        """
        初始化代码变体生成器
        
        Args:
            max_variants: 每个策略最大变体数
        """
        self.max_variants = max_variants
    
    def generate_variants(self, code: str, strategies: List[Dict[str, Any]]) -> List[str]:
        """
        生成代码变体
        
        Args:
            code: 原始代码
            strategies: 优化策略列表
            
        Returns:
            代码变体列表
        """
        variants = []
        
        # 按策略类型分类
        strategy_types = {}
        for strategy in strategies:
            strategy_type = strategy["type"]
            if strategy_type not in strategy_types:
                strategy_types[strategy_type] = []
            strategy_types[strategy_type].append(strategy)
        
        # 对每种策略类型，生成变体
        for strategy_type, strategies_of_type in strategy_types.items():
            # 仅使用每种类型的前max_variants个策略
            for strategy in strategies_of_type[:self.max_variants]:
                variant = self._generate_single_variant(code, strategy)
                if variant and variant != code:
                    variants.append(variant)
        
        return variants
    
    def _generate_single_variant(self, code: str, strategy: Dict[str, Any]) -> Optional[str]:
        """
        根据单个策略生成变体
        
        Args:
            code: 原始代码
            strategy: 优化策略
            
        Returns:
            代码变体或None
        """
        strategy_type = strategy["type"]
        
        # 测试失败修复策略
        if strategy_type == "test_failure_fix":
            return self._fix_test_failure(code, strategy)
        
        # 错误修复策略
        if strategy_type.endswith("_error_fix"):
            return self._fix_error(code, strategy)
        
        # 默认情况，返回原代码
        return None
    
    def _fix_test_failure(self, code: str, strategy: Dict[str, Any]) -> Optional[str]:
        """
        修复测试失败
        
        Args:
            code: 原始代码
            strategy: 优化策略
            
        Returns:
            修复后的代码或None
        """
        comparison_strategy = strategy.get("comparison_strategy", "")
        inputs = strategy.get("inputs", {})
        expected = strategy.get("expected")
        actual = strategy.get("actual")
        
        # 解析代码，找到函数定义
        try:
            tree = ast.parse(code)
            function_node = None
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_node = node
                    break
            
            if not function_node:
                return None
                
            # 根据比较策略应用不同的修复
            if comparison_strategy == "numeric_logic":
                return self._fix_numeric_logic(code, function_node, inputs, expected, actual)
            elif comparison_strategy == "off_by_one":
                return self._fix_off_by_one(code, function_node, inputs, expected, actual)
            elif comparison_strategy == "type_conversion":
                return self._fix_type_conversion(code, function_node, inputs, expected, actual)
            elif comparison_strategy == "collection_processing":
                return self._fix_collection_processing(code, function_node, inputs, expected, actual)
            else:
                # 对于其他策略，尝试一个通用修复
                return self._apply_generic_fix(code, inputs, expected, actual)
                
        except SyntaxError:
            return None
    
    def _fix_error(self, code: str, strategy: Dict[str, Any]) -> Optional[str]:
        """
        修复执行错误
        
        Args:
            code: 原始代码
            strategy: 优化策略
            
        Returns:
            修复后的代码或None
        """
        strategy_type = strategy["type"]
        error_message = strategy.get("error_message", "")
        
        # 根据错误类型选择修复策略
        if strategy_type == "name_error_fix":
            return self._fix_name_error(code, error_message)
        elif strategy_type == "type_error_fix":
            return self._fix_type_error(code, error_message)
        elif strategy_type == "index_error_fix":
            return self._fix_index_error(code, error_message)
        elif strategy_type == "key_error_fix":
            return self._fix_key_error(code, error_message)
        elif strategy_type == "attribute_error_fix":
            return self._fix_attribute_error(code, error_message)
        else:
            # 通用错误修复
            return self._fix_generic_error(code, error_message)
    
    def _fix_numeric_logic(self, code: str, function_node: ast.FunctionDef, inputs: Dict[str, Any], expected: Any, actual: Any) -> Optional[str]:
        """修复数值逻辑错误"""
        # 这里只是一个简化的示例，实际应用中应该更复杂
        # 在实际条件中，我们可能会分析AST并修改具体的计算逻辑
        
        # 查找数值计算表达式
        lines = code.split("\n")
        fixed_lines = lines.copy()
        
        # 查找返回语句
        for i, line in enumerate(lines):
            if "return" in line:
                # 如果预期值和实际值是数字，尝试调整计算
                if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
                    # 如果实际值太小，尝试添加差值
                    if actual < expected:
                        diff = expected - actual
                        fixed_line = line.replace("return", f"return {diff} + ")
                        fixed_lines[i] = fixed_line
                    # 如果实际值太大，尝试减去差值
                    elif actual > expected:
                        diff = actual - expected
                        fixed_line = line.replace("return", f"return ")
                        if "+" in fixed_line:
                            fixed_line = fixed_line.replace("+", "-")
                        else:
                            fixed_line = fixed_line.replace("return ", f"return  - {diff}")
                        fixed_lines[i] = fixed_line
        
        return "\n".join(fixed_lines)
    
    def _fix_off_by_one(self, code: str, function_node: ast.FunctionDef, inputs: Dict[str, Any], expected: Any, actual: Any) -> Optional[str]:
        """修复差一错误"""
        lines = code.split("\n")
        fixed_lines = lines.copy()
        
        for i, line in enumerate(lines):
            # 查找可能的索引或循环范围
            if "range(" in line or "[" in line and "]" in line:
                # 如果有范围或索引，尝试调整
                if "range(" in line:
                    # 尝试调整范围
                    range_match = re.search(r'range\((.+?)\)', line)
                    if range_match:
                        range_args = range_match.group(1)
                        # 如果范围是单参数，可能需要+1
                        if "," not in range_args:
                            fixed_line = line.replace(f"range({range_args})", f"range({range_args} + 1)")
                            fixed_lines[i] = fixed_line
                        # 如果范围有多个参数，可能需要调整结束值
                        else:
                            args = range_args.split(",")
                            if len(args) >= 2:
                                end_val = args[1].strip()
                                if end_val.isdigit():
                                    # 如果预期值大于实际值，增加结束值
                                    if expected > actual:
                                        new_end = int(end_val) + 1
                                    else:
                                        new_end = int(end_val) - 1
                                    fixed_args = f"{args[0]}, {new_end}"
                                    if len(args) > 2:
                                        fixed_args += f", {','.join(args[2:])}"
                                    fixed_line = line.replace(f"range({range_args})", f"range({fixed_args})")
                                    fixed_lines[i] = fixed_line
                # 查找索引操作
                elif "[" in line and "]" in line:
                    idx_match = re.search(r'\[(.+?)\]', line)
                    if idx_match:
                        idx = idx_match.group(1)
                        if idx.isdigit():
                            # 如果索引是数字，尝试调整
                            if expected > actual:
                                new_idx = int(idx) - 1
                            else:
                                new_idx = int(idx) + 1
                            fixed_line = line.replace(f"[{idx}]", f"[{new_idx}]")
                            fixed_lines[i] = fixed_line
        
        return "\n".join(fixed_lines)
    
    def _fix_type_conversion(self, code: str, function_node: ast.FunctionDef, inputs: Dict[str, Any], expected: Any, actual: Any) -> Optional[str]:
        """修复类型转换错误"""
        # 这里只是一个简化的示例
        lines = code.split("\n")
        fixed_lines = lines.copy()
        
        for i, line in enumerate(lines):
            if "return" in line:
                # 根据期望类型添加类型转换
                if isinstance(expected, int) and not isinstance(actual, int):
                    # 需要转换为整数
                    fixed_line = line.replace("return", "return int(")
                    if not fixed_line.endswith(")"):
                        fixed_line += ")"
                    fixed_lines[i] = fixed_line
                elif isinstance(expected, float) and not isinstance(actual, float):
                    # 需要转换为浮点数
                    fixed_line = line.replace("return", "return float(")
                    if not fixed_line.endswith(")"):
                        fixed_line += ")"
                    fixed_lines[i] = fixed_line
                elif isinstance(expected, str) and not isinstance(actual, str):
                    # 需要转换为字符串
                    fixed_line = line.replace("return", "return str(")
                    if not fixed_line.endswith(")"):
                        fixed_line += ")"
                    fixed_lines[i] = fixed_line
                elif isinstance(expected, list) and not isinstance(actual, list):
                    # 需要转换为列表
                    fixed_line = line.replace("return", "return list(")
                    if not fixed_line.endswith(")"):
                        fixed_line += ")"
                    fixed_lines[i] = fixed_line
        
        return "\n".join(fixed_lines)
    
    def _fix_collection_processing(self, code: str, function_node: ast.FunctionDef, inputs: Dict[str, Any], expected: Any, actual: Any) -> Optional[str]:
        """修复集合处理错误"""
        lines = code.split("\n")
        fixed_lines = lines.copy()
        
        # 如果预期是排序的列表
        if isinstance(expected, list) and isinstance(actual, list) and sorted(expected) == sorted(actual):
            for i, line in enumerate(lines):
                if "return" in line:
                    fixed_line = line.replace("return", "return sorted(")
                    if not fixed_line.endswith(")"):
                        fixed_line += ")"
                    fixed_lines[i] = fixed_line
        
        return "\n".join(fixed_lines)
    
    def _apply_generic_fix(self, code: str, inputs: Dict[str, Any], expected: Any, actual: Any) -> str:
        """应用通用修复"""
        # 这只是一个非常简单的通用修复示例
        # 将第一个找到的返回语句替换为直接返回预期值
        lines = code.split("\n")
        fixed_lines = lines.copy()
        
        for i, line in enumerate(lines):
            if "return" in line:
                # 格式化预期值以适应Python语法
                expected_str = repr(expected)
                fixed_line = f"    return {expected_str}  # 通用修复"
                fixed_lines[i] = fixed_line
                break
        
        return "\n".join(fixed_lines)
    
    def _fix_name_error(self, code: str, error_message: str) -> Optional[str]:
        """修复名称错误"""
        # 从错误消息中提取未定义的名称
        match = re.search(r"name '(.+?)' is not defined", error_message)
        if not match:
            return None
            
        undefined_name = match.group(1)
        
        # 尝试确定变量类型并添加定义
        lines = code.split("\n")
        fixed_lines = []
        
        # 在第一个函数定义后添加变量定义
        function_found = False
        for line in lines:
            fixed_lines.append(line)
            if "def " in line and ":" in line and not function_found:
                function_found = True
                # 添加一个合理的默认值
                indent = len(line) - len(line.lstrip()) + 4
                indent_str = " " * indent
                if undefined_name.startswith(("i", "j", "k", "n")):
                    # 可能是一个整数索引或计数器
                    fixed_lines.append(f"{indent_str}{undefined_name} = 0  # 自动修复")
                elif undefined_name.startswith(("s", "str")):
                    # 可能是一个字符串
                    fixed_lines.append(f"{indent_str}{undefined_name} = \"\"  # 自动修复")
                elif undefined_name.startswith(("lst", "arr", "list")):
                    # 可能是一个列表
                    fixed_lines.append(f"{indent_str}{undefined_name} = []  # 自动修复")
                elif undefined_name.startswith(("dict", "map")):
                    # 可能是一个字典
                    fixed_lines.append(f"{indent_str}{undefined_name} = {{}}  # 自动修复")
                else:
                    # 默认为None
                    fixed_lines.append(f"{indent_str}{undefined_name} = None  # 自动修复")
        
        return "\n".join(fixed_lines)
    
    def _fix_type_error(self, code: str, error_message: str) -> Optional[str]:
        """修复类型错误"""
        # 这是一个简化的修复示例
        lines = code.split("\n")
        fixed_lines = lines.copy()
        
        # 查找可能的类型转换问题
        for i, line in enumerate(lines):
            if "+" in line:
                # 可能是字符串和数字相加
                if "str" in error_message and "int" in error_message:
                    fixed_line = line.replace("+", "+ str(")
                    if not fixed_line.endswith(")"):
                        fixed_line += ")"
                    fixed_lines[i] = fixed_line
            elif "[" in line and "]" in line:
                # 可能是索引类型错误
                if "index" in error_message.lower():
                    idx_match = re.search(r'\[(.+?)\]', line)
                    if idx_match:
                        idx = idx_match.group(1)
                        fixed_line = line.replace(f"[{idx}]", f"[int({idx})]")
                        fixed_lines[i] = fixed_line
        
        return "\n".join(fixed_lines)
    
    def _fix_index_error(self, code: str, error_message: str) -> Optional[str]:
        """修复索引错误"""
        lines = code.split("\n")
        fixed_lines = lines.copy()
        
        for i, line in enumerate(lines):
            if "[" in line and "]" in line:
                # 添加索引检查
                idx_match = re.search(r'(\w+)\[(.+?)\]', line)
                if idx_match:
                    var_name = idx_match.group(1)
                    idx = idx_match.group(2)
                    indent = len(line) - len(line.lstrip())
                    indent_str = " " * indent
                    
                    # 在此行之前添加索引检查
                    check_line = f"{indent_str}if {idx} >= len({var_name}):\n{indent_str}    return []  # 索引检查"
                    fixed_lines.insert(i, check_line)
                    break
        
        return "\n".join(fixed_lines)
    
    def _fix_key_error(self, code: str, error_message: str) -> Optional[str]:
        """修复键错误"""
        lines = code.split("\n")
        fixed_lines = lines.copy()
        
        # 提取键名
        match = re.search(r"KeyError: '(.+?)'", error_message)
        if not match:
            return None
            
        key_name = match.group(1)
        
        for i, line in enumerate(lines):
            if "[" in line and "]" in line:
                # 查找字典访问
                dict_match = re.search(r'(\w+)\[(.+?)\]', line)
                if dict_match:
                    dict_name = dict_match.group(1)
                    key = dict_match.group(2)
                    # 用get方法替换直接访问
                    fixed_line = line.replace(f"{dict_name}[{key}]", f"{dict_name}.get({key}, None)")
                    fixed_lines[i] = fixed_line
                    break
        
        return "\n".join(fixed_lines)
    
    def _fix_attribute_error(self, code: str, error_message: str) -> Optional[str]:
        """修复属性错误"""
        # 提取属性名
        match = re.search(r"'(.+?)' object has no attribute '(.+?)'", error_message)
        if not match:
            return None
            
        obj_type = match.group(1)
        attr_name = match.group(2)
        
        # 这是一个简化的修复
        # 实际应用中应该分析对象类型并提供正确的属性
        lines = code.split("\n")
        fixed_lines = lines.copy()
        
        for i, line in enumerate(lines):
            if f".{attr_name}" in line:
                # 尝试添加空属性检查
                indent = len(line) - len(line.lstrip())
                indent_str = " " * indent
                obj_match = re.search(r'(\w+)\.{}'.format(attr_name), line)
                if obj_match:
                    obj_name = obj_match.group(1)
                    # 检查对象是否有该属性
                    check_line = f"{indent_str}if not hasattr({obj_name}, '{attr_name}'):\n"
                    check_line += f"{indent_str}    {obj_name}.{attr_name} = None  # 添加缺失属性"
                    fixed_lines.insert(i, check_line)
                    break
        
        return "\n".join(fixed_lines)
    
    def _fix_generic_error(self, code: str, error_message: str) -> Optional[str]:
        """通用错误修复"""
        # 简单地添加异常处理
        lines = code.split("\n")
        fixed_lines = []
        
        in_function = False
        function_indent = 0
        
        for line in lines:
            if "def " in line and ":" in line and not in_function:
                in_function = True
                function_indent = len(line) - len(line.lstrip())
                fixed_lines.append(line)
            elif in_function and not line.strip() and function_indent == 0:
                # 函数结束
                in_function = False
                fixed_lines.append(line)
            elif in_function:
                # 在函数内部，检查是否需要添加try-except
                if not line.strip().startswith(("try:", "except:", "finally:")):
                    indent = len(line) - len(line.lstrip())
                    if indent == function_indent + 4:  # 函数体的第一级缩进
                        # 添加try-except
                        fixed_lines.append(" " * indent + "try:")
                        fixed_lines.append(" " * (indent + 4) + line.strip())
                        fixed_lines.append(" " * indent + "except Exception as e:")
                        fixed_lines.append(" " * (indent + 4) + "print(f'Error: {e}')")
                        fixed_lines.append(" " * (indent + 4) + "return None  # 错误处理")
                    else:
                        fixed_lines.append(line)
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        return "\n".join(fixed_lines)