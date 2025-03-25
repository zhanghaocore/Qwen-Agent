"""
领域分类工具的单元测试
"""

import pytest
from src.requirement_analysis.advanced_analysis.tools import DomainClassifierTool

@pytest.fixture
def classifier():
    """创建领域分类器实例"""
    return DomainClassifierTool()

def test_domain_classification_basic(classifier):
    """测试基本的领域分类功能"""
    # 测试Web应用分类
    text = "开发一个电商网站，需要用户登录、商品展示、购物车和支付功能"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "web应用" in result.lower()
    
    # 测试数据处理分类
    text = "需要处理大量用户数据，进行数据清洗和分析，生成报表"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "数据处理" in result.lower()
    
    # 测试API服务分类
    text = "提供RESTful API服务，支持用户认证和限流"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "api服务" in result.lower()

def test_fuzzy_matching(classifier):
    """测试模糊匹配功能"""
    # 测试同义词匹配
    text = "开发一个门户网站，需要用户认证和权限管理"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "web应用" in result.lower()
    
    # 测试编辑距离匹配
    text = "开发一个电商网战，需要用户登入和商品展示"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "web应用" in result.lower()
    
    # 测试关键词匹配
    text = "需要处理和分析用户数据，生成统计报表"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "数据处理" in result.lower()

def test_feature_extraction(classifier):
    """测试特征提取功能"""
    # 测试Web应用特征提取
    text = "开发一个电商网站，需要用户登录、商品展示、购物车和支付功能，支持响应式设计"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "基础特征" in result.lower()
    assert "功能特征" in result.lower()
    assert "展示特征" in result.lower()
    
    # 测试数据处理特征提取
    text = "需要处理大量用户数据，进行数据清洗和分析，生成可视化报表"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "处理类型" in result.lower()
    assert "分析功能" in result.lower()
    assert "可视化" in result.lower()

def test_multi_domain_detection(classifier):
    """测试多领域检测功能"""
    # 测试Web应用+数据处理
    text = "开发一个数据分析平台，提供Web界面展示数据，支持数据导入导出"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "web应用" in result.lower()
    assert "数据处理" in result.lower()
    
    # 测试API服务+数据处理
    text = "提供数据分析API服务，支持数据查询和统计"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "api服务" in result.lower()
    assert "数据处理" in result.lower()

def test_domain_weights(classifier):
    """测试领域权重计算"""
    # 测试Web应用权重
    text = "开发一个电商网站，需要用户登录、商品展示、购物车和支付功能"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "web应用" in result.lower()
    
    # 测试数据处理权重
    text = "需要处理大量用户数据，进行数据清洗和分析，生成报表"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "数据处理" in result.lower()

def test_feature_coverage(classifier):
    """测试特征覆盖率计算"""
    # 测试高覆盖率场景
    text = "开发一个电商网站，需要用户登录、商品展示、购物车和支付功能，支持响应式设计，需要SEO优化"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "web应用" in result.lower()
    
    # 测试低覆盖率场景
    text = "开发一个简单的网站"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "web应用" in result.lower()

def test_edge_cases(classifier):
    """测试边界情况"""
    # 测试空文本
    result = classifier.call('{"requirement_text": ""}')
    assert "error" not in result.lower()
    
    # 测试特殊字符
    text = "开发一个网站！@#￥%……&*（）"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "web应用" in result.lower()
    
    # 测试超长文本
    text = "开发一个网站" * 100
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "web应用" in result.lower()

def test_invalid_input(classifier):
    """测试无效输入处理"""
    # 测试无效JSON
    with pytest.raises(Exception):
        classifier.call("invalid json")
    
    # 测试缺少必要参数
    with pytest.raises(Exception):
        classifier.call('{"other_param": "value"}')
    
    # 测试参数类型错误
    with pytest.raises(Exception):
        classifier.call('{"requirement_text": 123}')

def test_semantic_matching(classifier):
    """测试语义匹配功能"""
    # 测试同义词匹配
    text = "开发一个门户站点，需要用户认证和权限管理"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "web应用" in result.lower()
    
    # 测试相关概念匹配
    text = "开发一个在线商城，需要会员管理和订单处理"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "web应用" in result.lower()

def test_regex_matching(classifier):
    """测试正则表达式匹配功能"""
    # 测试数字匹配
    text = "处理1000条用户数据，生成报表"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "数据处理" in result.lower()
    
    # 测试版本号匹配
    text = "开发网站版本2.0，支持新功能"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "web应用" in result.lower()

def test_phrase_matching(classifier):
    """测试短语匹配功能"""
    # 测试完整短语匹配
    text = "开发一个电商网站，需要用户登录功能"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "web应用" in result.lower()
    
    # 测试部分短语匹配
    text = "开发网站，需要登录"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "web应用" in result.lower()

def test_context_matching(classifier):
    """测试上下文匹配功能"""
    # 测试完整上下文匹配
    text = "开发一个电商网站，需要用户登录、商品展示、购物车和支付功能"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "web应用" in result.lower()
    
    # 测试分散上下文匹配
    text = "开发网站。需要用户登录。需要商品展示。需要购物车。需要支付功能。"
    result = classifier.call('{"requirement_text": "' + text + '"}')
    assert "web应用" in result.lower() 