"""选项评估器模块

此模块负责评估技术选项的可行性和优劣。
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from .decision_point import DecisionPoint

class OptionEvaluator:
    """选项评估器类
    
    负责评估技术选项的可行性、优缺点和实现复杂度。
    """
    
    def __init__(self):
        """初始化选项评估器"""
        self._evaluation_cache: Dict[str, Dict[str, Any]] = {}
    
    async def evaluate_options(
        self,
        decision_point: DecisionPoint,
        options: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """评估技术选项
        
        Args:
            decision_point: 决策点实例
            options: 待评估的技术选项列表
            
        Returns:
            评估后的选项列表，包含评分和决策理由
        """
        evaluated_options = []
        
        for option in options:
            # 检查缓存
            cache_key = f"{decision_point.id}_{option['id']}"
            if cache_key in self._evaluation_cache:
                evaluated_options.append(self._evaluation_cache[cache_key])
                continue
            
            # 计算选项得分
            score = self._calculate_option_score(decision_point, option)
            
            # 生成决策理由
            reasoning = self._generate_decision_reasoning(decision_point, option, score)
            
            # 构建评估结果
            evaluation = {
                **option,
                "score": score,
                "reasoning": reasoning,
                "evaluated_at": datetime.now().isoformat()
            }
            
            # 更新缓存
            self._evaluation_cache[cache_key] = evaluation
            evaluated_options.append(evaluation)
        
        # 按得分排序
        evaluated_options.sort(key=lambda x: x["score"], reverse=True)
        return evaluated_options
    
    def _calculate_option_score(self, decision_point: DecisionPoint, option: Dict[str, Any]) -> float:
        """计算选项得分
        
        基于多个维度计算选项的得分：
        1. 实现复杂度（权重：0.3）
        2. 优点数量（权重：0.4）
        3. 缺点数量（权重：0.3）
        """
        # 实现复杂度得分（越低越好）
        complexity_score = 1 - option["complexity"]
        
        # 优点得分
        pros_score = len(option["pros"]) / 5  # 假设最多5个优点
        
        # 缺点得分（越少越好）
        cons_score = 1 - (len(option["cons"]) / 5)  # 假设最多5个缺点
        
        # 计算加权总分
        total_score = (
            0.3 * complexity_score +
            0.4 * pros_score +
            0.3 * cons_score
        )
        
        return round(total_score, 2)
    
    def _generate_decision_reasoning(
        self,
        decision_point: DecisionPoint,
        option: Dict[str, Any],
        score: float
    ) -> str:
        """生成决策理由
        
        基于选项的得分和特点生成决策理由。
        """
        reasoning_parts = []
        
        # 添加总体评价
        if score >= 0.8:
            reasoning_parts.append("这是一个非常优秀的技术选择")
        elif score >= 0.6:
            reasoning_parts.append("这是一个不错的选择")
        else:
            reasoning_parts.append("这个选项存在一些限制")
        
        # 添加优点分析
        if option["pros"]:
            reasoning_parts.append("主要优点包括：")
            for pro in option["pros"]:
                reasoning_parts.append(f"- {pro}")
        
        # 添加缺点分析
        if option["cons"]:
            reasoning_parts.append("需要注意的限制：")
            for con in option["cons"]:
                reasoning_parts.append(f"- {con}")
        
        # 添加复杂度分析
        complexity_desc = {
            0.8: "实现复杂度较高",
            0.6: "实现复杂度中等",
            0.4: "实现复杂度较低",
            0.2: "实现复杂度很低"
        }
        reasoning_parts.append(complexity_desc.get(
            round(option["complexity"] * 5) / 5,
            "实现复杂度适中"
        ))
        
        # 添加实现时间分析
        reasoning_parts.append(f"预计实现时间：{option['implementation_time']}")
        
        # 添加依赖分析
        if option["dependencies"]:
            reasoning_parts.append("需要添加的依赖：")
            for dep in option["dependencies"]:
                reasoning_parts.append(f"- {dep}")
        
        return "\n".join(reasoning_parts)
    
    def _check_constraints(self, decision_point: DecisionPoint, option: Dict[str, Any]) -> bool:
        """检查选项是否满足约束条件"""
        constraints: Dict[str, Any] = decision_point.constraints
        
        # 检查依赖约束
        if "dependencies" in constraints:
            required_deps = set(constraints["dependencies"])
            option_deps = set(dep.split(">=")[0] for dep in option["dependencies"])
            if not option_deps.issubset(required_deps):
                return False
        
        # 检查复杂度约束
        if "complexity" in constraints:
            max_complexity = float(constraints["complexity"])
            if option["complexity"] > max_complexity:
                return False
        
        # 检查实现时间约束
        if "implementation_time" in constraints:
            time_levels = {"较短": 1, "中等": 2, "较长": 3}
            max_time = time_levels.get(constraints["implementation_time"], 2)
            option_time = time_levels.get(option["implementation_time"], 2)
            if option_time > max_time:
                return False
        
        return True 