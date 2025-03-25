"""技术选项生成器模块的测试用例"""

import pytest
from datetime import datetime
from typing import Dict, Any, List

from technical_decision.decision_point import DecisionPoint, DecisionPointType
from technical_decision.option_generator import OptionGenerator

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
async def test_option_generation(sample_decision_point: DecisionPoint):
    """测试选项生成"""
    generator = OptionGenerator()
    options = await generator.generate_options(sample_decision_point)
    
    assert isinstance(options, list)
    assert len(options) > 0
    
    # 验证选项结构
    for option in options:
        assert "id" in option
        assert "name" in option
        assert "description" in option
        assert "pros" in option
        assert "cons" in option
        assert "complexity" in option
        assert "implementation_time" in option
        assert "dependencies" in option
        
        # 验证字段类型
        assert isinstance(option["id"], str)
        assert isinstance(option["name"], str)
        assert isinstance(option["description"], str)
        assert isinstance(option["pros"], list)
        assert isinstance(option["cons"], list)
        assert isinstance(option["complexity"], float)
        assert isinstance(option["implementation_time"], str)
        assert isinstance(option["dependencies"], list)
        
        # 验证值范围
        assert 0 <= option["complexity"] <= 1
        assert len(option["pros"]) > 0
        assert len(option["cons"]) > 0
        assert len(option["dependencies"]) > 0

@pytest.mark.asyncio
async def test_option_caching(sample_decision_point: DecisionPoint):
    """测试选项缓存"""
    generator = OptionGenerator()
    
    # 第一次生成选项
    options1 = await generator.generate_options(sample_decision_point)
    
    # 第二次生成选项（应该从缓存中获取）
    options2 = await generator.generate_options(sample_decision_point)
    
    # 验证两次结果相同
    assert options1 == options2
    
    # 验证缓存键存在
    cache_key = f"{sample_decision_point.type}_{sample_decision_point.id}"
    assert cache_key in generator._options_cache
    assert generator._options_cache[cache_key] == options1

@pytest.mark.asyncio
async def test_data_processing_options(sample_decision_point: DecisionPoint):
    """测试数据处理选项生成"""
    generator = OptionGenerator()
    options = generator._generate_data_processing_options(sample_decision_point)
    
    assert len(options) == 2  # pandas 和 numpy
    
    pandas_option = next(opt for opt in options if opt["id"] == "pandas")
    numpy_option = next(opt for opt in options if opt["id"] == "numpy")
    
    # 验证 pandas 选项
    assert pandas_option["name"] == "Pandas"
    assert "数据处理" in pandas_option["description"]
    assert len(pandas_option["pros"]) == 4
    assert len(pandas_option["cons"]) == 3
    assert pandas_option["complexity"] == 0.7
    assert pandas_option["implementation_time"] == "中等"
    assert "pandas>=2.0.0" in pandas_option["dependencies"]
    
    # 验证 numpy 选项
    assert numpy_option["name"] == "NumPy"
    assert "数值计算" in numpy_option["description"]
    assert len(numpy_option["pros"]) == 4
    assert len(numpy_option["cons"]) == 3
    assert numpy_option["complexity"] == 0.5
    assert numpy_option["implementation_time"] == "较短"
    assert "numpy>=1.24.0" in numpy_option["dependencies"]