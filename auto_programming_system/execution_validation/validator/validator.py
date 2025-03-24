"""
代码验证器模块
负责验证生成代码是否符合预期
"""

import ast
from typing import Dict, Any, List, Optional, Union

from auto_programming_system.execution_validation.sandbox.safe_sandbox import SafeSandbox


class CodeValidator:
    """代码验证器，验证代码是否符合预期"""
    
    def __init__(self):
        """初始化代码验证器"""
        pass
    
    def validate_in_sandbox(
        self, code: str, tests: List[Dict[str, Any]], sandbox: SafeSandbox
    ) -> Dict[str, Any]:
        """
        在沙箱中验证代码
        
        Args:
            code: 要验证的代码
            tests: 测试用例列表
            sandbox: 安全沙箱
            
        Returns:
            验证结果
        """
        results = {
            "passed": [],
            "failed": [],
            "errors": []
        }
        
        # 提取函数名
        function_name = self._extract_function_name(code)
        
        if not function_name:
            results["errors"].append("无法从代码中提取函数名")
            return self._generate_summary(results)
        
        # 执行每个测试用例
        for i, test in enumerate(tests):
            test_id = f"test_{i+1}"
            inputs = test.get("inputs", {})
            expected = test.get("expected")
            
            try:
                # 调用函数
                actual = sandbox.call_function(code, function_name, [], inputs)
                
                # 验证结果
                if self._compare_values(actual, expected):
                    results["passed"].append({
                        "test_id": test_id,
                        "inputs": inputs,
                        "expected": expected,
                        "actual": actual
                    })
                else:
                    results["failed"].append({
                        "test_id": test_id,
                        "inputs": inputs,
                        "expected": expected,
                        "actual": actual,
                        "reason": "结果与预期不符"
                    })
            except Exception as e:
                results["errors"].append({
                    "test_id": test_id,
                    "inputs": inputs,
                    "expected": expected,
                    "error": str(e)
                })
        
        return self._generate_summary(results)
    
    def _extract_function_name(self, code: str) -> Optional[str]:
        """
        从代码中提取函数名
        
        Args:
            code: Python代码
            
        Returns:
            函数名或None
        """
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    return node.name
            return None
        except:
            return None
    
    def _compare_values(self, actual: Any, expected: Any) -> bool:
        """
        比较实际值和预期值
        
        Args:
            actual: 实际值
            expected: 预期值
            
        Returns:
            是否相等
        """
        # 处理None特殊情况
        if expected is None:
            return actual is None
            
        # 处理数值类型
        if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
            # 浮点数比较需要考虑精度
            if isinstance(expected, float) or isinstance(actual, float):
                return abs(actual - expected) < 1e-6
            return actual == expected
            
        # 列表比较
        if isinstance(expected, list) and isinstance(actual, list):
            if len(expected) != len(actual):
                return False
            return all(self._compare_values(a, e) for a, e in zip(actual, expected))
            
        # 字典比较
        if isinstance(expected, dict) and isinstance(actual, dict):
            if set(expected.keys()) != set(actual.keys()):
                return False
            return all(self._compare_values(actual[k], expected[k]) for k in expected)
            
        # 默认比较
        return actual == expected
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成验证结果摘要
        
        Args:
            results: 验证结果
            
        Returns:
            包含摘要的结果
        """
        num_passed = len(results["passed"])
        num_failed = len(results["failed"])
        num_errors = len(results["errors"])
        total_tests = num_passed + num_failed + num_errors
        
        results["validation_summary"] = {
            "total_tests": total_tests,
            "passed_tests": num_passed,
            "failed_tests": num_failed,
            "error_tests": num_errors,
            "pass_rate": num_passed / total_tests if total_tests > 0 else 0,
            "all_passed": num_passed == total_tests and total_tests > 0
        }
        
        return results 