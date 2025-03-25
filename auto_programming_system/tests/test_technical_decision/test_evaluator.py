"""技术选项评估器模块的测试用例"""

import pytest
from datetime import datetime
from typing import Dict, Any, List

from technical_decision.decision_point import DecisionPoint, DecisionPointType
from technical_decision.evaluator import OptionEvaluator

@pytest.fixture
def sample_decision_point() -> DecisionPoint:
    """创建示例决策点"""
    return DecisionPoint(
        id="test_dp_1",
        type=DecisionPointType.DATA_PROCESSING,
        description="处理CSV文件并计算每列的平均值",
        confidence=0.8,
        constraints={
            "dependencies": ["pandas", "numpy"],
            "complexity": 0.7,
            "implementation_time": "中等"
        },
        dependencies=[],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@pytest.fixture
def sample_options() -> List[Dict[str, Any]]:
    """创建示例技术选项"""
    return [
        {
            "id": "pandas",
            "name": "Pandas",
            "description": "使用 Pandas 进行数据处理和分析",
            "pros": [
                "强大的数据处理能力",
                "丰富的数据分析功能",
                "良好的性能优化",
                "广泛的数据格式支持"
            ],
            "cons": [
                "内存占用较大",
                "学习曲线较陡",
                "某些操作可能较慢"
            ],
            "complexity": 0.7,
            "implementation_time": "中等",
            "dependencies": ["pandas>=2.0.0"]
        },
        {
            "id": "numpy",
            "name": "NumPy",
            "description": "使用 NumPy 进行数值计算和数组操作",
            "pros": [
                "高效的数值计算",
                "内存效率高",
                "底层优化好",
                "基础库依赖少"
            ],
            "cons": [
                "功能相对简单",
                "缺少高级数据分析功能",
                "需要自己实现一些常用功能"
            ],
            "complexity": 0.5,
            "implementation_time": "较短",
            "dependencies": ["numpy>=1.24.0"]
        }
    ]

@pytest.mark.asyncio
async def test_option_evaluation(sample_decision_point: DecisionPoint, sample_options: List[Dict[str, Any]]):
    """测试选项评估"""
    evaluator = OptionEvaluator()
    evaluated_options = await evaluator.evaluate_options(sample_decision_point, sample_options)
    
    assert isinstance(evaluated_options, list)
    assert len(evaluated_options) == len(sample_options)
    
    # 验证评估结果
    for option in evaluated_options:
        assert "score" in option
        assert "reasoning" in option
        assert "evaluated_at" in option
        assert isinstance(option["score"], float)
        assert isinstance(option["reasoning"], str)
        assert isinstance(option["evaluated_at"], str)
    
    # 验证排序
    scores = [option["score"] for option in evaluated_options]
    assert scores == sorted(scores, reverse=True)

@pytest.mark.asyncio
async def test_constraint_checking(sample_decision_point: DecisionPoint, sample_options: List[Dict[str, Any]]):
    """测试约束检查"""
    evaluator = OptionEvaluator()
    
    # 测试满足约束的选项
    valid_option = {
        **sample_options[0],
        "complexity": 0.6,
        "implementation_time": "较短",
        "dependencies": ["pandas"]
    }
    assert evaluator._check_constraints(sample_decision_point, valid_option)
    
    # 测试不满足约束的选项
    invalid_option = {
        **sample_options[0],
        "complexity": 0.8,
        "implementation_time": "较长",
        "dependencies": ["pandas", "scipy"]
    }
    assert not evaluator._check_constraints(sample_decision_point, invalid_option)

@pytest.mark.asyncio
async def test_decision_reasoning_generation(sample_decision_point: DecisionPoint, sample_options: List[Dict[str, Any]]):
    """测试决策理由生成"""
    evaluator = OptionEvaluator()
    option = sample_options[0]
    score = evaluator._calculate_option_score(sample_decision_point, option)
    reasoning = evaluator._generate_decision_reasoning(sample_decision_point, option, score)
    
    assert isinstance(reasoning, str)
    assert len(reasoning) > 0
    
    # 验证理由包含必要信息
    assert "主要优点包括" in reasoning
    assert "需要注意的限制" in reasoning
    assert "实现复杂度" in reasoning
    assert "预计实现时间" in reasoning
    assert "需要添加的依赖" in reasoning

@pytest.mark.asyncio
async def test_option_score_calculation(sample_decision_point: DecisionPoint, sample_options: List[Dict[str, Any]]):
    """测试选项得分计算"""
    evaluator = OptionEvaluator()
    
    for option in sample_options:
        score = evaluator._calculate_option_score(sample_decision_point, option)
        assert isinstance(score, float)
        assert 0 <= score <= 1
        
        # 验证得分计算逻辑
        complexity_score = 1 - option["complexity"]
        pros_score = len(option["pros"]) / 5
        cons_score = 1 - (len(option["cons"]) / 5)
        expected_score = round(
            0.3 * complexity_score +
            0.4 * pros_score +
            0.3 * cons_score,
            2
        )
        assert score == expected_score