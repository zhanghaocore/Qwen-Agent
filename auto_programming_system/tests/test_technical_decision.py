"""技术决策模块的测试用例"""

import pytest
from datetime import datetime
from typing import Dict, Any, List

from agents.technical_decision import TechnicalDecisionAgent

@pytest.fixture
def technical_decision_agent():
    """创建技术决策代理实例"""
    return TechnicalDecisionAgent()

@pytest.fixture
def sample_requirements():
    """创建示例需求列表"""
    return [
        "处理CSV文件并计算每列的平均值",
        "将处理后的数据保存到数据库",
        "优化数据处理性能"
    ]

@pytest.fixture
def sample_constraints():
    """创建示例约束条件"""
    return [
        "使用Python标准库",
        "内存使用不超过1GB",
        "处理时间不超过30秒"
    ]

@pytest.mark.asyncio
async def test_decision_point_creation(technical_decision_agent: TechnicalDecisionAgent, sample_requirements: List[str], sample_constraints: List[str]):
    """测试决策点创建"""
    decision_points = await technical_decision_agent._identify_decision_points(sample_requirements, sample_constraints)
    
    assert isinstance(decision_points, list)
    assert len(decision_points) > 0
    
    for point in decision_points:
        assert "type" in point
        assert "content" in point
        assert "confidence" in point
        assert "dependencies" in point
        assert "constraints" in point
        assert "features" in point

@pytest.mark.asyncio
async def test_decision_point_serialization(technical_decision_agent: TechnicalDecisionAgent, sample_requirements: List[str], sample_constraints: List[str]):
    """测试决策点序列化"""
    decision_points = await technical_decision_agent._identify_decision_points(sample_requirements, sample_constraints)
    
    for point in decision_points:
        # 验证所有必要字段都存在
        assert all(key in point for key in ["type", "content", "confidence", "dependencies", "constraints", "features"])
        
        # 验证字段类型
        assert isinstance(point["type"], str)
        assert isinstance(point["content"], str)
        assert isinstance(point["confidence"], float)
        assert isinstance(point["dependencies"], list)
        assert isinstance(point["constraints"], list)
        assert isinstance(point["features"], dict)

@pytest.mark.asyncio
async def test_option_generation(technical_decision_agent: TechnicalDecisionAgent, sample_requirements: List[str], sample_constraints: List[str]):
    """测试选项生成"""
    decision_points = await technical_decision_agent._identify_decision_points(sample_requirements, sample_constraints)
    options = await technical_decision_agent._generate_alternatives(decision_points[0])
    
    assert isinstance(options, list)
    assert len(options) > 0
    
    for option in options:
        assert "option" in option
        assert "description" in option
        assert "pros" in option
        assert "cons" in option
        assert "implementation_complexity" in option
        assert "decision_point" in option

@pytest.mark.asyncio
async def test_option_evaluation(technical_decision_agent: TechnicalDecisionAgent, sample_requirements: List[str], sample_constraints: List[str]):
    """测试选项评估"""
    decision_points = await technical_decision_agent._identify_decision_points(sample_requirements, sample_constraints)
    options = await technical_decision_agent._generate_alternatives(decision_points[0])
    evaluation = await technical_decision_agent._evaluate_alternatives(options, sample_requirements, sample_constraints)
    
    assert "best_option" in evaluation
    assert "all_options" in evaluation
    assert "context" in evaluation
    
    for option in evaluation["all_options"]:
        assert "score" in option
        assert "reasoning" in option
        assert isinstance(option["score"], float)
        assert isinstance(option["reasoning"], str)

@pytest.mark.asyncio
async def test_constraint_checking(technical_decision_agent: TechnicalDecisionAgent, sample_requirements: List[str], sample_constraints: List[str]):
    """测试约束检查"""
    decision_points = await technical_decision_agent._identify_decision_points(sample_requirements, sample_constraints)
    options = await technical_decision_agent._generate_alternatives(decision_points[0])
    
    for option in options:
        score = technical_decision_agent._calculate_option_score(option, sample_requirements, sample_constraints)
        assert isinstance(score, float)
        assert 0 <= score <= 1

@pytest.mark.asyncio
async def test_decision_reasoning_generation(technical_decision_agent: TechnicalDecisionAgent, sample_requirements: List[str], sample_constraints: List[str]):
    """测试决策理由生成"""
    decision_points = await technical_decision_agent._identify_decision_points(sample_requirements, sample_constraints)
    options = await technical_decision_agent._generate_alternatives(decision_points[0])
    
    for option in options:
        score = technical_decision_agent._calculate_option_score(option, sample_requirements, sample_constraints)
        reasoning = technical_decision_agent._generate_decision_reasoning(option, score)
        
        assert isinstance(reasoning, str)
        assert len(reasoning) > 0
        assert option["option"] in reasoning
        assert option["implementation_complexity"] in reasoning

@pytest.mark.asyncio
async def test_option_score_calculation(technical_decision_agent: TechnicalDecisionAgent, sample_requirements: List[str], sample_constraints: List[str]):
    """测试选项得分计算"""
    decision_points = await technical_decision_agent._identify_decision_points(sample_requirements, sample_constraints)
    options = await technical_decision_agent._generate_alternatives(decision_points[0])
    
    for option in options:
        score = technical_decision_agent._calculate_option_score(option, sample_requirements, sample_constraints)
        
        assert isinstance(score, float)
        assert 0 <= score <= 1
        
        # 验证得分计算逻辑
        complexity_score = 0.2 if option["implementation_complexity"] == "very_low" else \
                         0.15 if option["implementation_complexity"] == "low" else \
                         0.1 if option["implementation_complexity"] == "medium" else 0.05
        
        pros_score = min(len(option["pros"]) * 0.1, 0.4)
        cons_score = min(len(option["cons"]) * 0.05, 0.3)
        
        expected_score = round(0.3 + complexity_score + pros_score - cons_score, 2)
        assert abs(score - expected_score) < 0.01 