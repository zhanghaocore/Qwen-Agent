"""
报告生成器模块
负责生成代码验证和分析的报告
"""

import time
import json
from typing import Dict, Any, List, Optional


class ReportGenerator:
    """报告生成器，生成代码验证和分析的详细报告"""
    
    def __init__(self):
        """初始化报告生成器"""
        pass
    
    def generate_report(
        self, 
        code: str, 
        test_results: Dict[str, Any], 
        code_analysis: Dict[str, Any],
        execution_time: float
    ) -> Dict[str, Any]:
        """
        生成综合报告
        
        Args:
            code: 原始代码
            test_results: 测试结果
            code_analysis: 代码分析结果
            execution_time: 执行时间
            
        Returns:
            综合报告
        """
        # 基本报告结构
        report = {
            "timestamp": int(time.time()),
            "execution_time": execution_time,
            "code_summary": self._generate_code_summary(code),
            "validation_results": test_results,
            "code_analysis": code_analysis,
            "recommendations": self._generate_recommendations(test_results, code_analysis)
        }
        
        # 添加验证摘要（如果不存在）
        if "validation_summary" not in test_results:
            passed_count = len(test_results.get("passed", []))
            failed_count = len(test_results.get("failed", []))
            error_count = len(test_results.get("errors", []))
            total_count = passed_count + failed_count + error_count
            
            report["validation_summary"] = {
                "total_tests": total_count,
                "passed_tests": passed_count,
                "failed_tests": failed_count,
                "error_tests": error_count,
                "pass_rate": passed_count / total_count if total_count > 0 else 0,
                "all_passed": passed_count == total_count and total_count > 0
            }
        else:
            report["validation_summary"] = test_results["validation_summary"]
        
        return report
    
    def _generate_code_summary(self, code: str) -> Dict[str, Any]:
        """
        生成代码摘要
        
        Args:
            code: 代码
            
        Returns:
            代码摘要
        """
        lines = code.split("\n")
        
        return {
            "code_length": len(code),
            "line_count": len(lines),
            "first_line": lines[0] if lines else "",
            "is_function": "def " in code,
            "is_class": "class " in code,
            "has_docstring": '"""' in code or "'''" in code
        }
    
    def _generate_recommendations(
        self, test_results: Dict[str, Any], code_analysis: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """
        生成改进建议
        
        Args:
            test_results: 测试结果
            code_analysis: 代码分析结果
            
        Returns:
            建议列表
        """
        recommendations = []
        
        # 基于测试结果的建议
        if test_results.get("failed") or test_results.get("errors"):
            recommendations.append({
                "type": "test_failure",
                "severity": "high",
                "message": "代码未通过所有测试，需要修复测试失败"
            })
            
            # 添加具体的测试失败建议
            for failure in test_results.get("failed", []):
                recommendations.append({
                    "type": "test_specific",
                    "severity": "medium",
                    "message": f"测试 {failure.get('test_id')} 失败: 期望 {failure.get('expected')}，实际 {failure.get('actual')}"
                })
        
        # 基于代码质量的建议
        quality = code_analysis.get("code_quality", {})
        
        if not quality.get("has_docstrings", True):
            recommendations.append({
                "type": "quality",
                "severity": "medium",
                "message": "代码缺少文档字符串，应添加描述性文档"
            })
            
        if not quality.get("has_type_annotations", True):
            recommendations.append({
                "type": "quality",
                "severity": "low",
                "message": "建议添加类型注解提高代码可读性和可维护性"
            })
            
        if not quality.get("has_error_handling", True):
            recommendations.append({
                "type": "quality",
                "severity": "medium",
                "message": "代码缺少异常处理，应添加适当的错误处理机制"
            })
        
        # 处理代码中的具体问题
        for issue in quality.get("issues", []):
            recommendations.append({
                "type": "issue",
                "severity": "medium",
                "message": f"代码问题: {issue}"
            })
        
        return recommendations 