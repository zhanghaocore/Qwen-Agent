"""
反馈分析器模块
负责分析验证结果以确定需要改进的地方
"""

from typing import Dict, Any, List, Optional


class FeedbackAnalyzer:
    """反馈分析器，分析验证结果以确定优化目标"""
    
    def __init__(self):
        """初始化反馈分析器"""
        pass
    
    def analyze(self, code: str, validation_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析验证结果
        
        Args:
            code: 原始代码
            validation_report: 验证报告
            
        Returns:
            优化目标字典
        """
        # 提取基本信息
        summary = validation_report.get("validation_summary", {})
        passed_tests = validation_report.get("passed", [])
        failed_tests = validation_report.get("failed", [])
        errors = validation_report.get("errors", [])
        
        # 初始化优化目标
        optimization_targets = []
        
        # 如果所有测试都通过，不需要优化
        if summary.get("all_passed", False):
            return {"optimization_targets": optimization_targets}
        
        # 分析测试失败
        for test in failed_tests:
            target = self._analyze_test_failure(test, code)
            if target:
                optimization_targets.append(target)
        
        # 分析错误
        for error in errors:
            target = self._analyze_error(error, code)
            if target:
                optimization_targets.append(target)
        
        return {
            "optimization_targets": optimization_targets,
            "test_statistics": {
                "total": summary.get("total_tests", 0),
                "passed": summary.get("passed_tests", 0),
                "failed": summary.get("failed_tests", 0),
                "errors": summary.get("error_tests", 0)
            }
        }
    
    def _analyze_test_failure(self, test: Dict[str, Any], code: str) -> Optional[Dict[str, Any]]:
        """
        分析测试失败
        
        Args:
            test: 测试失败信息
            code: 原始代码
            
        Returns:
            优化目标或None
        """
        inputs = test.get("inputs", {})
        expected = test.get("expected")
        actual = test.get("actual")
        test_id = test.get("test_id", "unknown")
        
        # 返回优化目标
        return {
            "type": "test_failure",
            "test_id": test_id,
            "inputs": inputs,
            "expected": expected,
            "actual": actual,
            "description": f"修复测试 {test_id} 失败: 输入={inputs}, 期望={expected}, 实际={actual}"
        }
    
    def _analyze_error(self, error: Dict[str, Any], code: str) -> Optional[Dict[str, Any]]:
        """
        分析执行错误
        
        Args:
            error: 错误信息
            code: 原始代码
            
        Returns:
            优化目标或None
        """
        inputs = error.get("inputs", {})
        error_message = error.get("error", "")
        test_id = error.get("test_id", "unknown")
        
        # 尝试确定错误类型
        error_type = "runtime_error"
        if "name" in error_message.lower() and "not defined" in error_message.lower():
            error_type = "name_error"
        elif "type" in error_message.lower():
            error_type = "type_error"
        elif "index" in error_message.lower():
            error_type = "index_error"
        elif "key" in error_message.lower():
            error_type = "key_error"
        elif "attribute" in error_message.lower():
            error_type = "attribute_error"
        
        # 返回优化目标
        return {
            "type": "error",
            "error_type": error_type,
            "test_id": test_id,
            "inputs": inputs,
            "error_message": error_message,
            "description": f"修复测试 {test_id} 错误: {error_message}"
        } 