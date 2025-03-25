"""
问题库管理器的单元测试
"""

import os
import json
import pytest
from datetime import datetime
from typing import Dict, Any

from ..advanced_analysis.question_bank import (
    QuestionBankManager,
    Question,
    QuestionType,
    QuestionDifficulty
)


@pytest.fixture
def temp_storage_path(tmp_path):
    """创建临时存储路径"""
    storage_path = tmp_path / "question_bank"
    storage_path.mkdir()
    return str(storage_path)


@pytest.fixture
def question_bank(temp_storage_path):
    """创建问题库管理器实例"""
    return QuestionBankManager(storage_path=temp_storage_path)


@pytest.fixture
def sample_question():
    """创建示例问题"""
    return Question(
        id="test_question_1",
        type=QuestionType.FUNCTIONAL,
        difficulty=QuestionDifficulty.MEDIUM,
        content="如何实现用户认证功能？",
        answer="可以使用JWT或Session进行用户认证...",
        tags=["认证", "安全", "用户管理"],
        domain="web应用",
        dependencies=[],
        created_at=datetime.now(),
        updated_at=datetime.now(),
        version=1,
        metadata={"priority": "high", "category": "auth"}
    )


def test_add_question(question_bank, sample_question):
    """测试添加问题"""
    question_bank.add_question(sample_question)
    assert question_bank.get_question(sample_question.id) == sample_question


def test_update_question(question_bank, sample_question):
    """测试更新问题"""
    question_bank.add_question(sample_question)
    
    # 更新问题内容
    sample_question.content = "更新后的问题内容"
    question_bank.update_question(sample_question)
    
    updated_question = question_bank.get_question(sample_question.id)
    assert updated_question.content == "更新后的问题内容"
    assert updated_question.version == 2  # 版本号应该增加


def test_delete_question(question_bank, sample_question):
    """测试删除问题"""
    question_bank.add_question(sample_question)
    question_bank.delete_question(sample_question.id)
    assert question_bank.get_question(sample_question.id) is None


def test_search_questions(question_bank, sample_question):
    """测试搜索问题"""
    question_bank.add_question(sample_question)
    
    # 测试关键词搜索
    results = question_bank.search_questions("认证")
    assert len(results) == 1
    assert results[0].id == sample_question.id
    
    # 测试类型过滤
    results = question_bank.search_questions("", question_type=QuestionType.FUNCTIONAL)
    assert len(results) == 1
    
    # 测试难度过滤
    results = question_bank.search_questions("", difficulty=QuestionDifficulty.MEDIUM)
    assert len(results) == 1
    
    # 测试领域过滤
    results = question_bank.search_questions("", domain="web应用")
    assert len(results) == 1
    
    # 测试标签过滤
    results = question_bank.search_questions("", tags=["认证"])
    assert len(results) == 1


def test_get_questions_by_domain(question_bank, sample_question):
    """测试按领域获取问题"""
    question_bank.add_question(sample_question)
    results = question_bank.get_questions_by_domain("web应用")
    assert len(results) == 1
    assert results[0].id == sample_question.id


def test_get_questions_by_type(question_bank, sample_question):
    """测试按类型获取问题"""
    question_bank.add_question(sample_question)
    results = question_bank.get_questions_by_type(QuestionType.FUNCTIONAL)
    assert len(results) == 1
    assert results[0].id == sample_question.id


def test_get_questions_by_difficulty(question_bank, sample_question):
    """测试按难度获取问题"""
    question_bank.add_question(sample_question)
    results = question_bank.get_questions_by_difficulty(QuestionDifficulty.MEDIUM)
    assert len(results) == 1
    assert results[0].id == sample_question.id


def test_get_questions_by_tags(question_bank, sample_question):
    """测试按标签获取问题"""
    question_bank.add_question(sample_question)
    results = question_bank.get_questions_by_tags(["认证"])
    assert len(results) == 1
    assert results[0].id == sample_question.id


def test_question_dependencies(question_bank):
    """测试问题依赖关系"""
    # 创建依赖问题
    dep_question = Question(
        id="dep_question_1",
        type=QuestionType.TECHNICAL,
        difficulty=QuestionDifficulty.EASY,
        content="依赖问题",
        answer="依赖问题的答案",
        tags=["依赖"],
        domain="web应用",
        dependencies=[],
        created_at=datetime.now(),
        updated_at=datetime.now(),
        version=1,
        metadata={}
    )
    
    # 创建主问题
    main_question = Question(
        id="main_question_1",
        type=QuestionType.FUNCTIONAL,
        difficulty=QuestionDifficulty.MEDIUM,
        content="主问题",
        answer="主问题的答案",
        tags=["主问题"],
        domain="web应用",
        dependencies=["dep_question_1"],
        created_at=datetime.now(),
        updated_at=datetime.now(),
        version=1,
        metadata={}
    )
    
    question_bank.add_question(dep_question)
    question_bank.add_question(main_question)
    
    # 测试获取依赖
    dependencies = question_bank.get_question_dependencies(main_question.id)
    assert len(dependencies) == 1
    assert dependencies[0].id == dep_question.id


def test_persistence(question_bank, sample_question, temp_storage_path):
    """测试问题持久化"""
    # 添加问题
    question_bank.add_question(sample_question)
    
    # 创建新的问题库管理器实例
    new_question_bank = QuestionBankManager(storage_path=temp_storage_path)
    
    # 验证问题是否被正确加载
    loaded_question = new_question_bank.get_question(sample_question.id)
    assert loaded_question is not None
    assert loaded_question.content == sample_question.content
    assert loaded_question.type == sample_question.type
    assert loaded_question.difficulty == sample_question.difficulty
    assert loaded_question.tags == sample_question.tags
    assert loaded_question.domain == sample_question.domain
    assert loaded_question.version == sample_question.version 