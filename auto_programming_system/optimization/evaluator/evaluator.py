"""
变体评估器模块
负责评估生成的代码变体
"""

import time
from typing import Dict, Any, List, Optional

from auto_programming_system.execution_validation.core import CodeValidator
from auto_programming_system.execution_validation.sandbox.safe_sandbox import SafeSandbox
from auto_programming_system.execution_validation.analyzer.analyzer import CodeAnalyzer


class VariantEvaluator:
    """变体评估器，评估代码变体的质量"""
    
    def __init__(self, security_level: str = "standard"):
        """
        初始化变体评估器
        
        Args:
            security_level: 安全级别
        """
        self.security_level = security_level
        self.sandbox = SafeSandbox(security_level)
        self.validator = CodeValidator()
        self.analyzer = CodeAnalyzer()
    
    def evaluate_variants(self, variants: List[str]) -> List[Dict[str, Any]]:
        """
        评估代码变体
        
        Args:
            variants: 代码变体列表
            
        Returns:
            评估结果列表
        """
        results = []
        
        for i, variant in enumerate(variants):
            # 评估当前变体
            result = self.evaluate_single_variant(variant)
            result["variant_id"] = i + 1
            result["code"] = variant
            results.append(result)
        
        # 按综合评分排序
        return sorted(results, key=lambda x: x["overall_score"], reverse=True)
    
    def evaluate_single_variant(self, variant: str) -> Dict[str, Any]:
        """
        评估单个代码变体
        
        Args:
            variant: 代码变体
            
        Returns:
            评估结果
        """
        # 生成测试用例（使用默认测试生成器）
        tests = []
        
        # 开始计时
        start_time = time.time()
        
        # 在沙箱中验证代码
        validation_results = self.validator.validate_in_sandbox(
            variant, tests, self.sandbox
        )
        
        # 分析代码质量
        code_analysis = self.analyzer.analyze(variant)
        
        # 计算执行时间
        execution_time = time.time() - start_time
        
        # 计算综合评分
        overall_score = self._calculate_overall_score(validation_results, code_analysis, execution_time)
        
        return {
            "validation_results": validation_results,
            "code_analysis": code_analysis,
            "execution_time": execution_time,
            "overall_score": overall_score
        }
    
    def _calculate_overall_score(
        self, validation_results: Dict[str, Any], code_analysis: Dict[str, Any], execution_time: float
    ) -> float:
        """
        计算综合评分
        
        Args:
            validation_results: 验证结果
            code_analysis: 代码分析结果
            execution_time: 执行时间
            
        Returns:
            综合评分
        """
        # 提取测试通过率
        summary = validation_results.get("validation_summary", {})
        pass_rate = summary.get("pass_rate", 0.0)
        all_passed = summary.get("all_passed", False)
        
        # 提取代码质量评分
        quality_score = code_analysis.get("code_quality", {}).get("score", 0.0)
        
        # 计算执行时间评分（越快越好）
        time_score = 1.0 / (1.0 + execution_time) if execution_time > 0 else 1.0
        
        # 测试通过率最重要，然后是代码质量，最后是执行时间
        score = (pass_rate * 0.7) + (quality_score * 0.2) + (time_score * 0.1)
        
        # 如果所有测试都通过，给一个奖励
        if all_passed:
            score += 0.1
            
        # 确保分数在0-1之间
        return min(max(score, 0.0), 1.0) 