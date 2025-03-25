"""
动态问题生成器的单元测试
"""

import pytest
from datetime import datetime
from typing import Dict, Any

from ..advanced_analysis.dynamic_question_generator import (
    DynamicQuestionGenerator,
    QuestionQualityMetrics
)
from ..advanced_analysis.question_bank import (
    QuestionBankManager,
    Question,
    QuestionType,
    QuestionDifficulty
)

@pytest.fixture
def question_bank():
    """创建问题库管理器实例"""
    return QuestionBankManager()

@pytest.fixture
def generator(question_bank):
    """创建动态问题生成器实例"""
    return DynamicQuestionGenerator(question_bank)

@pytest.fixture
def sample_context():
    """创建示例上下文"""
    return {
        "tags": ["性能", "架构"],
        "keywords": ["系统", "数据", "处理"],
        "answered_questions": ["q1", "q2"],
        "stage": "initial"
    }

def test_initialization(generator, question_bank):
    """测试初始化"""
    assert generator.question_bank == question_bank
    assert isinstance(generator.quality_metrics, dict)

def test_base_questions_initialization(generator, question_bank):
    """测试基础问题集初始化"""
    questions = question_bank.get_all_questions()
    assert len(questions) > 0
    
    # 检查问题类型分布
    type_counts = {}
    for q in questions:
        type_counts[q.type] = type_counts.get(q.type, 0) + 1
    
    assert QuestionType.FUNCTIONAL in type_counts
    assert QuestionType.TECHNICAL in type_counts
    assert QuestionType.SECURITY in type_counts

def test_generate_questions(generator, sample_context):
    """测试问题生成"""
    questions = generator.generate_questions(
        context=sample_context,
        domain="通用",
        stage="initial",
        count=3
    )
    
    assert len(questions) <= 3
    assert all(isinstance(q, Question) for q in questions)
    assert all(q.metadata.get("quality_score") is not None for q in questions)

def test_filter_questions_by_context(generator, sample_context):
    """测试基于上下文的问题过滤"""
    questions = generator.question_bank.get_all_questions()
    filtered = generator._filter_questions_by_context(
        questions, sample_context, "initial"
    )
    
    assert len(filtered) <= len(questions)
    assert all(q.metadata.get("stage") == "initial" for q in filtered)

def test_question_relevance(generator, sample_context):
    """测试问题相关性判断"""
    question = Question(
        id="test_q",
        type=QuestionType.TECHNICAL,
        difficulty=QuestionDifficulty.MEDIUM,
        content="系统需要处理多少数据？",
        answer="需要评估数据规模",
        tags=["性能", "数据"],
        domain="通用",
        dependencies=[],
        created_at=datetime.now(),
        updated_at=datetime.now(),
        version=1,
        metadata={"stage": "initial"}
    )
    
    assert generator._is_question_relevant(question, sample_context)

def test_quality_metrics_calculation(generator):
    """测试质量指标计算"""
    question = Question(
        id="test_q",
        type=QuestionType.TECHNICAL,
        difficulty=QuestionDifficulty.MEDIUM,
        content="系统需要处理多少数据？",
        answer="需要评估数据规模",
        tags=["性能", "数据"],
        domain="通用",
        dependencies=[],
        created_at=datetime.now(),
        updated_at=datetime.now(),
        version=1,
        metadata={"stage": "initial"}
    )
    
    metrics = generator._calculate_quality_metrics(question)
    assert isinstance(metrics, QuestionQualityMetrics)
    assert 0 <= metrics.clarity <= 1
    assert 0 <= metrics.relevance <= 1
    assert 0 <= metrics.complexity <= 1
    assert 0 <= metrics.uniqueness <= 1
    assert 0 <= metrics.coverage <= 1

def test_quality_score_calculation(generator):
    """测试质量分数计算"""
    question = Question(
        id="test_q",
        type=QuestionType.TECHNICAL,
        difficulty=QuestionDifficulty.MEDIUM,
        content="系统需要处理多少数据？",
        answer="需要评估数据规模",
        tags=["性能", "数据"],
        domain="通用",
        dependencies=[],
        created_at=datetime.now(),
        updated_at=datetime.now(),
        version=1,
        metadata={"stage": "initial"}
    )
    
    score = generator._calculate_quality_score(question)
    assert 0 <= score <= 1

def test_recommend_questions(generator, sample_context):
    """测试问题推荐"""
    recommendations = generator.recommend_questions(
        context=sample_context,
        domain="通用",
        stage="initial",
        count=3
    )
    
    assert len(recommendations) <= 3
    assert all(isinstance(q, Question) for q in recommendations)
    
    # 检查推荐顺序
    if len(recommendations) > 1:
        scores = [generator._calculate_quality_score(q) for q in recommendations]
        assert scores == sorted(scores, reverse=True)

def test_context_relevance_calculation(generator, sample_context):
    """测试上下文相关性计算"""
    question = Question(
        id="test_q",
        type=QuestionType.TECHNICAL,
        difficulty=QuestionDifficulty.MEDIUM,
        content="系统需要处理多少数据？",
        answer="需要评估数据规模",
        tags=["性能", "数据"],
        domain="通用",
        dependencies=[],
        created_at=datetime.now(),
        updated_at=datetime.now(),
        version=1,
        metadata={"stage": "initial"}
    )
    
    relevance = generator._calculate_context_relevance(question, sample_context)
    assert 0 <= relevance <= 1

def test_keyword_extraction(generator):
    """测试关键词提取"""
    text = "系统需要处理大量数据并保证性能"
    keywords = generator._extract_keywords(text)
    
    assert isinstance(keywords, list)
    assert all(isinstance(k, str) for k in keywords)
    assert all(len(k) > 2 for k in keywords)
    assert len(set(keywords)) == len(keywords)  # 检查去重 