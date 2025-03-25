"""
问题库管理模块
实现问题的存储、检索、分类和版本控制功能
"""

from typing import Dict, List, Any, Optional
import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum


class QuestionType(Enum):
    """问题类型枚举"""
    FUNCTIONAL = "functional"  # 功能性问题
    TECHNICAL = "technical"    # 技术性问题
    BUSINESS = "business"      # 业务性问题
    SECURITY = "security"      # 安全性问题
    PERFORMANCE = "performance"  # 性能问题
    OTHER = "other"           # 其他类型


class QuestionDifficulty(Enum):
    """问题难度枚举"""
    EASY = "easy"             # 简单
    MEDIUM = "medium"         # 中等
    HARD = "hard"             # 困难
    EXPERT = "expert"         # 专家级


@dataclass
class Question:
    """问题数据类"""
    id: str                    # 问题ID
    type: QuestionType         # 问题类型
    difficulty: QuestionDifficulty  # 问题难度
    content: str               # 问题内容
    answer: str                # 问题答案
    tags: List[str]            # 问题标签
    domain: str                # 所属领域
    dependencies: List[str]    # 依赖的其他问题ID
    created_at: datetime       # 创建时间
    updated_at: datetime       # 更新时间
    version: int               # 版本号
    metadata: Dict[str, Any]   # 元数据


class QuestionBankManager:
    """问题库管理器"""
    
    def __init__(self, storage_path: str = "data/question_bank"):
        """
        初始化问题库管理器
        
        Args:
            storage_path: 问题库存储路径
        """
        self.storage_path = storage_path
        self.questions: Dict[str, Question] = {}
        self._ensure_storage_path()
        self._load_questions()
    
    def _ensure_storage_path(self) -> None:
        """确保存储路径存在"""
        os.makedirs(self.storage_path, exist_ok=True)
    
    def _load_questions(self) -> None:
        """从存储加载所有问题"""
        question_file = os.path.join(self.storage_path, "questions.json")
        if os.path.exists(question_file):
            with open(question_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for q_data in data:
                    q_data['type'] = QuestionType(q_data['type'])
                    q_data['difficulty'] = QuestionDifficulty(q_data['difficulty'])
                    q_data['created_at'] = datetime.fromisoformat(q_data['created_at'])
                    q_data['updated_at'] = datetime.fromisoformat(q_data['updated_at'])
                    question = Question(**q_data)
                    self.questions[question.id] = question
    
    def _save_questions(self) -> None:
        """保存所有问题到存储"""
        question_file = os.path.join(self.storage_path, "questions.json")
        data = []
        for question in self.questions.values():
            q_dict = asdict(question)
            q_dict['type'] = q_dict['type'].value
            q_dict['difficulty'] = q_dict['difficulty'].value
            q_dict['created_at'] = q_dict['created_at'].isoformat()
            q_dict['updated_at'] = q_dict['updated_at'].isoformat()
            data.append(q_dict)
        
        with open(question_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_question(self, question: Question) -> None:
        """
        添加新问题
        
        Args:
            question: 要添加的问题对象
        """
        self.questions[question.id] = question
        self._save_questions()
    
    def get_question(self, question_id: str) -> Optional[Question]:
        """
        获取指定ID的问题
        
        Args:
            question_id: 问题ID
            
        Returns:
            问题对象，如果不存在则返回None
        """
        return self.questions.get(question_id)
    
    def update_question(self, question: Question) -> None:
        """
        更新问题
        
        Args:
            question: 更新后的问题对象
        """
        if question.id in self.questions:
            question.version += 1
            question.updated_at = datetime.now()
            self.questions[question.id] = question
            self._save_questions()
    
    def delete_question(self, question_id: str) -> None:
        """
        删除问题
        
        Args:
            question_id: 要删除的问题ID
        """
        if question_id in self.questions:
            del self.questions[question_id]
            self._save_questions()
    
    def search_questions(self, 
                        query: str,
                        question_type: Optional[QuestionType] = None,
                        difficulty: Optional[QuestionDifficulty] = None,
                        domain: Optional[str] = None,
                        tags: Optional[List[str]] = None) -> List[Question]:
        """
        搜索问题
        
        Args:
            query: 搜索关键词
            question_type: 问题类型过滤
            difficulty: 难度过滤
            domain: 领域过滤
            tags: 标签过滤
            
        Returns:
            匹配的问题列表
        """
        results = []
        for question in self.questions.values():
            # 应用过滤条件
            if question_type and question.type != question_type:
                continue
            if difficulty and question.difficulty != difficulty:
                continue
            if domain and question.domain != domain:
                continue
            if tags and not all(tag in question.tags for tag in tags):
                continue
            
            # 关键词匹配
            if (query.lower() in question.content.lower() or
                query.lower() in question.answer.lower() or
                query.lower() in ' '.join(question.tags).lower()):
                results.append(question)
        
        return results
    
    def get_questions_by_domain(self, domain: str) -> List[Question]:
        """
        获取指定领域的所有问题
        
        Args:
            domain: 领域名称
            
        Returns:
            该领域的问题列表
        """
        return [q for q in self.questions.values() if q.domain == domain]
    
    def get_questions_by_type(self, question_type: QuestionType) -> List[Question]:
        """
        获取指定类型的所有问题
        
        Args:
            question_type: 问题类型
            
        Returns:
            该类型的问题列表
        """
        return [q for q in self.questions.values() if q.type == question_type]
    
    def get_all_questions(self) -> List[Question]:
        """
        获取所有问题
        
        Returns:
            所有问题的列表
        """
        return list(self.questions.values())
    
    def get_questions_by_difficulty(self, difficulty: QuestionDifficulty) -> List[Question]:
        """
        获取指定难度的所有问题
        
        Args:
            difficulty: 问题难度
            
        Returns:
            该难度的问题列表
        """
        return [q for q in self.questions.values() if q.difficulty == difficulty]
    
    def get_questions_by_tags(self, tags: List[str]) -> List[Question]:
        """
        获取包含指定标签的所有问题
        
        Args:
            tags: 标签列表
            
        Returns:
            包含所有指定标签的问题列表
        """
        return [q for q in self.questions.values() 
                if all(tag in q.tags for tag in tags)]
    
    def get_question_dependencies(self, question_id: str) -> List[Question]:
        """
        获取问题的所有依赖问题
        
        Args:
            question_id: 问题ID
            
        Returns:
            依赖问题列表
        """
        question = self.get_question(question_id)
        if not question:
            return []
        
        dependencies = []
        for dep_id in question.dependencies:
            dep_question = self.get_question(dep_id)
            if dep_question:
                dependencies.append(dep_question)
        
        return dependencies 