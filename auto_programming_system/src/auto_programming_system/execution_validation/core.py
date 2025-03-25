"""
执行验证模块的核心类
负责安全测试代码并验证其正确性
"""

import json
import time
from typing import Dict, Any, List, Optional, Union

from src.execution_validation.sandbox.safe_sandbox import SafeSandbox
from src.execution_validation.test_generator.generator import TestGenerator
from src.execution_validation.validator.validator import CodeValidator as ValidationExecutor
from src.execution_validation.analyzer.analyzer import CodeAnalyzer
from src.execution_validation.reporter.reporter import ReportGenerator


class CodeValidator:
    """代码验证器，测试生成的代码并验证其正确性"""
    
    def __init__(self, security_level: str = "standard"):
        """
        初始化代码验证器
        
        Args:
            security_level: 安全级别 ("relaxed", "standard", "strict")
        """
        self.security_level = security_level
        
        # 根据安全级别设置超时时间
        timeout_map = {
            "relaxed": 60,    # 宽松模式：60秒
            "standard": 30,   # 标准模式：30秒
            "strict": 15      # 严格模式：15秒
        }
        timeout = timeout_map.get(security_level, 30)  # 默认30秒
        
        self.sandbox = SafeSandbox(timeout=timeout)
        self.test_generator = TestGenerator()
        self.validator = ValidationExecutor()
        self.analyzer = CodeAnalyzer()
        self.reporter = ReportGenerator()
    
    def validate(self, code: str, custom_tests: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        验证生成的代码
        
        Args:
            code: 要验证的Python代码
            custom_tests: 用户自定义的测试用例
            
        Returns:
            验证结果报告
        """
        start_time = time.time()
        
        # 1. 生成测试用例
        tests = custom_tests or self.test_generator.generate_tests(code)
        
        # 2. 在沙箱中执行验证
        validation_results = self.validator.validate_in_sandbox(
            code, tests, self.sandbox
        )
        
        # 3. 分析代码质量
        code_analysis = self.analyzer.analyze(code)
        
        # 4. 生成报告
        report = self.reporter.generate_report(
            code=code,
            test_results=validation_results,
            code_analysis=code_analysis,
            execution_time=time.time() - start_time
        )
        
        return report
    
    def validate_with_expected_output(
        self, code: str, inputs: List[Dict[str, Any]], expected_outputs: List[Any]
    ) -> Dict[str, Any]:
        """
        使用预期输出验证代码
        
        Args:
            code: 要验证的Python代码
            inputs: 输入值列表
            expected_outputs: 预期输出值列表
            
        Returns:
            验证结果报告
        """
        if len(inputs) != len(expected_outputs):
            raise ValueError("输入和预期输出的数量必须相同")
        
        # 构建测试用例
        tests = [
            {"inputs": inputs[i], "expected": expected_outputs[i]} 
            for i in range(len(inputs))
        ]
        
        # 执行验证
        return self.validate(code, tests)
