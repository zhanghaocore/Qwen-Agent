"""
优化策略选择器模块
负责根据反馈选择合适的代码优化策略
"""

from typing import Dict, Any, List, Optional


class OptimizationStrategySelector:
    """优化策略选择器，选择合适的代码优化策略"""
    
    def __init__(self):
        """初始化优化策略选择器"""
        pass
    
    def select_strategies(self, optimization_targets: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        选择优化策略
        
        Args:
            optimization_targets: 优化目标
            
        Returns:
            选择的策略列表
        """
        strategies = []
        targets = optimization_targets.get("optimization_targets", [])
        
        for target in targets:
            # 根据目标类型选择策略
            if target["type"] == "test_failure":
                strategy = self._create_test_failure_strategy(target)
                strategies.append(strategy)
            elif target["type"] == "error":
                strategy = self._create_error_strategy(target)
                strategies.append(strategy)
        
        return strategies
    
    def _create_test_failure_strategy(self, target: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建测试失败的修复策略
        
        Args:
            target: 优化目标
            
        Returns:
            优化策略
        """
        inputs = target.get("inputs", {})
        expected = target.get("expected")
        actual = target.get("actual")
        
        # 确定失败原因的策略
        comparison_strategy = self._determine_comparison_strategy(expected, actual)
        
        return {
            "type": "test_failure_fix",
            "target_id": target.get("test_id"),
            "inputs": inputs,
            "expected": expected,
            "actual": actual,
            "comparison_strategy": comparison_strategy,
            "description": f"修复测试失败: {target.get('description')}",
            "strategy_details": {
                "approach": comparison_strategy,
                "focus_area": "function_logic"
            }
        }
    
    def _create_error_strategy(self, target: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建错误修复策略
        
        Args:
            target: 优化目标
            
        Returns:
            优化策略
        """
        error_type = target.get("error_type", "runtime_error")
        
        strategy_type = "generic_error_fix"
        focus_area = "error_handling"
        
        # 根据错误类型调整策略
        if error_type == "name_error":
            strategy_type = "name_error_fix"
            focus_area = "variable_declaration"
        elif error_type == "type_error":
            strategy_type = "type_error_fix"
            focus_area = "type_handling"
        elif error_type == "index_error":
            strategy_type = "index_error_fix"
            focus_area = "boundary_check"
        elif error_type == "key_error":
            strategy_type = "key_error_fix"
            focus_area = "dictionary_handling"
        elif error_type == "attribute_error":
            strategy_type = "attribute_error_fix"
            focus_area = "object_attribute"
        
        return {
            "type": strategy_type,
            "target_id": target.get("test_id"),
            "inputs": target.get("inputs", {}),
            "error_message": target.get("error_message", ""),
            "description": f"修复错误: {target.get('description')}",
            "strategy_details": {
                "error_type": error_type,
                "focus_area": focus_area
            }
        }
    
    def _determine_comparison_strategy(self, expected: Any, actual: Any) -> str:
        """
        确定值比较的优化策略
        
        Args:
            expected: 期望值
            actual: 实际值
            
        Returns:
            比较策略
        """
        # 如果一个是None而另一个不是
        if (expected is None and actual is not None) or (expected is not None and actual is None):
            return "null_handling"
            
        # 如果类型不同
        if type(expected) != type(actual):
            return "type_conversion"
            
        # 数字比较
        if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
            # 如果符号相反
            if (expected > 0 and actual < 0) or (expected < 0 and actual > 0):
                return "sign_correction"
            # 如果差一个常数
            if abs(abs(expected) - abs(actual)) <= 1:
                return "off_by_one"
            # 如果是倍数关系
            if expected != 0 and actual != 0 and (expected / actual).is_integer():
                return "scaling_factor"
            return "numeric_logic"
            
        # 字符串比较
        if isinstance(expected, str) and isinstance(actual, str):
            # 如果大小写不同
            if expected.lower() == actual.lower():
                return "case_sensitivity"
            # 如果有空格差异
            if expected.strip() == actual.strip():
                return "whitespace_handling"
            # 如果是子字符串
            if expected in actual or actual in expected:
                return "string_extraction"
            return "string_manipulation"
            
        # 列表比较
        if isinstance(expected, list) and isinstance(actual, list):
            # 如果长度不同
            if len(expected) != len(actual):
                return "collection_size"
            # 如果元素相同但顺序不同
            if sorted(expected) == sorted(actual):
                return "sorting_order"
            return "collection_processing"
            
        # 字典比较
        if isinstance(expected, dict) and isinstance(actual, dict):
            # 如果键集不同
            if set(expected.keys()) != set(actual.keys()):
                return "key_handling"
            return "dictionary_processing"
            
        # 默认策略
        return "logic_correction" 