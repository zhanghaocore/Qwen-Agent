"""技术决策点模块的测试用例"""

import pytest
from datetime import datetime
from typing import Dict, Any, List

from technical_decision.decision_point import DecisionPoint, DecisionPointType

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

@pytest.mark.asyncio
async def test_decision_point_creation(sample_decision_point: DecisionPoint):
    """测试决策点创建"""
    assert sample_decision_point.id == "test_dp_1"
    assert sample_decision_point.type == DecisionPointType.DATA_PROCESSING
    assert sample_decision_point.confidence == 0.8
    assert isinstance(sample_decision_point.constraints, dict)
    assert len(sample_decision_point.dependencies) == 0

@pytest.mark.asyncio
async def test_decision_point_serialization(sample_decision_point: DecisionPoint):
    """测试决策点序列化"""
    data = sample_decision_point.to_dict()
    assert isinstance(data, dict)
    assert data["id"] == sample_decision_point.id
    assert data["type"] == sample_decision_point.type
    assert data["confidence"] == sample_decision_point.confidence
    
    # 测试反序列化
    new_dp = DecisionPoint.from_dict(data)
    assert new_dp.id == sample_decision_point.id
    assert new_dp.type == sample_decision_point.type
    assert new_dp.confidence == sample_decision_point.confidence