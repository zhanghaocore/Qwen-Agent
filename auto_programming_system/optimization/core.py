"""
优化模块的核心类
负责基于验证结果和反馈持续改进生成的代码
"""

import json
from typing import Dict, Any, List, Optional, Tuple

from auto_programming_system.optimization.feedback_analyzer.analyzer import FeedbackAnalyzer
from auto_programming_system.optimization.optimization_strategy.strategy import OptimizationStrategySelector
from auto_programming_system.optimization.variant_generator.generator import CodeVariantGenerator
from auto_programming_system.optimization.evaluator.evaluator import VariantEvaluator
from auto_programming_system.optimization.version_control.controller import VersionController


class CodeOptimizer:
    """代码优化器，根据反馈改进代码"""
    
    def __init__(self, max_optimization_rounds: int = 3):
        """
        初始化代码优化器
        
        Args:
            max_optimization_rounds: 最大优化轮数，防止无限循环
        """
        self.max_optimization_rounds = max_optimization_rounds
        self.feedback_analyzer = FeedbackAnalyzer()
        self.strategy_selector = OptimizationStrategySelector()
        self.variant_generator = CodeVariantGenerator()
        self.evaluator = VariantEvaluator()
        self.version_controller = VersionController()
    
    def optimize(self, code: str, validation_report: Dict[str, Any]) -> str:
        """
        优化代码
        
        Args:
            code: 原始代码
            validation_report: 验证报告
            
        Returns:
            优化后的代码
        """
        # 记录初始版本
        current_code = code
        self.version_controller.add_version(current_code, "initial")
        
        for round_num in range(self.max_optimization_rounds):
            # 1. 分析反馈
            optimization_targets = self.feedback_analyzer.analyze(current_code, validation_report)
            
            # 检查是否还需要优化
            if not optimization_targets["optimization_targets"]:
                break
                
            # 2. 选择优化策略
            strategies = self.strategy_selector.select_strategies(optimization_targets)
            
            # 3. 生成代码变体
            variants = self.variant_generator.generate_variants(
                current_code, strategies
            )
            
            # 如果没有生成变体，结束优化
            if not variants:
                break
                
            # 4. 评估变体
            evaluation_results = self.evaluator.evaluate_variants(variants)
            
            # 5. 选择最佳变体
            best_variant = self._select_best_variant(evaluation_results)
            
            # 记录新版本
            self.version_controller.add_version(
                best_variant, f"optimization_round_{round_num + 1}"
            )
            
            # 更新当前代码
            current_code = best_variant
        
        return current_code
    
    def _select_best_variant(self, evaluation_results: List[Dict[str, Any]]) -> str:
        """
        从评估结果中选择最佳变体
        
        Args:
            evaluation_results: 变体评估结果列表
            
        Returns:
            最佳变体的代码
        """
        # 按综合评分排序
        sorted_results = sorted(
            evaluation_results, 
            key=lambda x: x["overall_score"], 
            reverse=True
        )
        
        # 返回评分最高的变体
        if sorted_results:
            return sorted_results[0]["code"]
            
        # 如果没有评估结果，返回空字符串
        return ""
