"""
动态问题生成器
实现基于上下文的动态问题生成、质量评估和推荐算法
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import uuid
import json
from enum import Enum

from .question_bank import Question, QuestionType, QuestionDifficulty, QuestionBankManager

class QuestionQuality(Enum):
    """问题质量等级"""
    EXCELLENT = 5
    GOOD = 4
    AVERAGE = 3
    POOR = 2
    UNACCEPTABLE = 1

@dataclass
class QuestionQualityMetrics:
    """问题质量指标"""
    clarity: float  # 清晰度 (0-1)
    relevance: float  # 相关性 (0-1)
    complexity: float  # 复杂度 (0-1)
    uniqueness: float  # 独特性 (0-1)
    coverage: float  # 覆盖度 (0-1)
    timestamp: datetime  # 评估时间

class DynamicQuestionGenerator:
    """动态问题生成器"""
    
    def __init__(self, question_bank: QuestionBankManager):
        """
        初始化动态问题生成器
        
        Args:
            question_bank: 问题库管理器实例
        """
        self.question_bank = question_bank
        self.quality_metrics: Dict[str, QuestionQualityMetrics] = {}
        self._initialize_base_questions()
    
    def _initialize_base_questions(self):
        """初始化基础问题集"""
        base_questions = [
            # 功能需求相关
            Question(
                id=str(uuid.uuid4()),
                type=QuestionType.FUNCTIONAL,
                difficulty=QuestionDifficulty.MEDIUM,
                content="这个功能的主要目标是什么？",
                answer="需要明确功能的核心目标和价值",
                tags=["目标", "功能分析"],
                domain="通用",
                dependencies=[],
                created_at=datetime.now(),
                updated_at=datetime.now(),
                version=1,
                metadata={"stage": "initial"}
            ),
            Question(
                id=str(uuid.uuid4()),
                type=QuestionType.FUNCTIONAL,
                difficulty=QuestionDifficulty.MEDIUM,
                content="用户使用这个功能的主要场景是什么？",
                answer="需要了解用户的使用场景和上下文",
                tags=["场景", "用户分析"],
                domain="通用",
                dependencies=[],
                created_at=datetime.now(),
                updated_at=datetime.now(),
                version=1,
                metadata={"stage": "initial"}
            ),
            
            # 技术需求相关
            Question(
                id=str(uuid.uuid4()),
                type=QuestionType.TECHNICAL,
                difficulty=QuestionDifficulty.MEDIUM,
                content="系统需要处理的数据量大概是多少？",
                answer="需要评估数据规模，包括用户数量、数据量、并发量等",
                tags=["性能", "架构"],
                domain="通用",
                dependencies=[],
                created_at=datetime.now(),
                updated_at=datetime.now(),
                version=1,
                metadata={"stage": "initial"}
            ),
            Question(
                id=str(uuid.uuid4()),
                type=QuestionType.TECHNICAL,
                difficulty=QuestionDifficulty.MEDIUM,
                content="系统对响应时间有什么要求？",
                answer="需要明确性能要求，包括响应时间、并发处理能力等",
                tags=["性能", "要求"],
                domain="通用",
                dependencies=[],
                created_at=datetime.now(),
                updated_at=datetime.now(),
                version=1,
                metadata={"stage": "initial"}
            ),
            
            # 安全需求相关
            Question(
                id=str(uuid.uuid4()),
                type=QuestionType.SECURITY,
                difficulty=QuestionDifficulty.MEDIUM,
                content="系统需要处理哪些敏感数据？",
                answer="需要识别敏感数据，并确定相应的安全保护措施",
                tags=["安全", "数据"],
                domain="通用",
                dependencies=[],
                created_at=datetime.now(),
                updated_at=datetime.now(),
                version=1,
                metadata={"stage": "initial"}
            ),
            Question(
                id=str(uuid.uuid4()),
                type=QuestionType.SECURITY,
                difficulty=QuestionDifficulty.MEDIUM,
                content="系统需要满足哪些安全合规要求？",
                answer="需要明确安全合规要求，如数据保护、访问控制等",
                tags=["安全", "合规"],
                domain="通用",
                dependencies=[],
                created_at=datetime.now(),
                updated_at=datetime.now(),
                version=1,
                metadata={"stage": "initial"}
            ),
            
            # 可维护性相关
            Question(
                id=str(uuid.uuid4()),
                type=QuestionType.PERFORMANCE,
                difficulty=QuestionDifficulty.MEDIUM,
                content="系统需要支持哪些扩展功能？",
                answer="需要明确系统的可扩展性要求",
                tags=["维护", "扩展"],
                domain="通用",
                dependencies=[],
                created_at=datetime.now(),
                updated_at=datetime.now(),
                version=1,
                metadata={"stage": "initial"}
            ),
            Question(
                id=str(uuid.uuid4()),
                type=QuestionType.PERFORMANCE,
                difficulty=QuestionDifficulty.MEDIUM,
                content="系统需要支持哪些监控和日志功能？",
                answer="需要明确系统的可观测性要求",
                tags=["维护", "监控"],
                domain="通用",
                dependencies=[],
                created_at=datetime.now(),
                updated_at=datetime.now(),
                version=1,
                metadata={"stage": "initial"}
            ),
        ]
        
        for question in base_questions:
            self.question_bank.add_question(question)
    
    def generate_questions(
        self,
        context: Dict[str, Any],
        domain: str,
        stage: str,
        count: int = 5
    ) -> List[Question]:
        """
        根据上下文生成问题
        
        Args:
            context: 上下文信息
            domain: 领域
            stage: 当前阶段
            count: 需要生成的问题数量
            
        Returns:
            生成的问题列表
        """
        # 1. 从问题库中获取相关问题
        base_questions = self.question_bank.get_questions_by_domain(domain)
        
        # 2. 根据上下文和阶段过滤问题
        filtered_questions = self._filter_questions_by_context(
            base_questions, context, stage
        )
        
        # 3. 评估问题质量
        quality_questions = self._evaluate_questions(filtered_questions)
        
        # 4. 根据质量分数排序
        sorted_questions = sorted(
            quality_questions,
            key=lambda x: self._calculate_quality_score(x),
            reverse=True
        )
        
        # 5. 返回指定数量的问题
        return sorted_questions[:count]
    
    def _filter_questions_by_context(
        self,
        questions: List[Question],
        context: Dict[str, Any],
        stage: str
    ) -> List[Question]:
        """
        根据上下文过滤问题
        
        Args:
            questions: 问题列表
            context: 上下文信息
            stage: 当前阶段
            
        Returns:
            过滤后的问题列表
        """
        filtered_questions = []
        
        for question in questions:
            # 检查问题是否适合当前阶段
            if question.metadata.get("stage") != stage:
                continue
                
            # 检查问题是否与上下文相关
            if self._is_question_relevant(question, context):
                filtered_questions.append(question)
        
        return filtered_questions
    
    def _is_question_relevant(
        self,
        question: Question,
        context: Dict[str, Any]
    ) -> bool:
        """
        判断问题是否与上下文相关
        
        Args:
            question: 问题
            context: 上下文信息
            
        Returns:
            是否相关
        """
        # 1. 检查标签匹配
        context_tags = context.get("tags", [])
        if any(tag in context_tags for tag in question.tags):
            return True
            
        # 2. 检查关键词匹配
        context_keywords = context.get("keywords", [])
        question_keywords = self._extract_keywords(question.content)
        if any(keyword in question_keywords for keyword in context_keywords):
            return True
            
        # 3. 检查依赖关系
        if question.dependencies:
            for dep in question.dependencies:
                if dep in context.get("answered_questions", []):
                    return True
        
        return False
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        从文本中提取关键词
        
        Args:
            text: 输入文本
            
        Returns:
            关键词列表
        """
        # 简单的关键词提取实现
        words = text.lower().split()
        # 过滤停用词和短词
        keywords = [w for w in words if len(w) > 2]
        return list(set(keywords))  # 去重
    
    def _evaluate_questions(
        self,
        questions: List[Question]
    ) -> List[Question]:
        """
        评估问题质量
        
        Args:
            questions: 问题列表
            
        Returns:
            评估后的问题列表
        """
        evaluated_questions = []
        
        for question in questions:
            # 计算质量指标
            metrics = self._calculate_quality_metrics(question)
            self.quality_metrics[question.id] = metrics
            
            # 根据质量指标更新问题
            question.metadata["quality_score"] = self._calculate_quality_score(question)
            evaluated_questions.append(question)
        
        return evaluated_questions
    
    def _calculate_quality_metrics(self, question: Question) -> QuestionQualityMetrics:
        """
        计算问题质量指标
        
        Args:
            question: 问题
            
        Returns:
            质量指标
        """
        # 1. 清晰度评估
        clarity = self._evaluate_clarity(question)
        
        # 2. 相关性评估
        relevance = self._evaluate_relevance(question)
        
        # 3. 复杂度评估
        complexity = self._evaluate_complexity(question)
        
        # 4. 独特性评估
        uniqueness = self._evaluate_uniqueness(question)
        
        # 5. 覆盖度评估
        coverage = self._evaluate_coverage(question)
        
        return QuestionQualityMetrics(
            clarity=clarity,
            relevance=relevance,
            complexity=complexity,
            uniqueness=uniqueness,
            coverage=coverage,
            timestamp=datetime.now()
        )
    
    def _evaluate_clarity(self, question: Question) -> float:
        """评估问题清晰度"""
        # 基于问题长度、标点符号使用等特征
        text = question.content
        words = text.split()
        sentences = text.split('.')
        
        # 计算平均句子长度
        avg_sentence_length = len(words) / max(len(sentences), 1)
        
        # 计算标点符号使用
        punctuation_count = sum(1 for c in text if c in '.,!?;:')
        
        # 综合评分
        clarity_score = min(1.0, (
            0.4 * (1.0 - abs(avg_sentence_length - 15) / 15) +  # 句子长度评分
            0.3 * (1.0 - abs(punctuation_count - len(sentences)) / len(sentences)) +  # 标点使用评分
            0.3 * (1.0 - len(words) / 50)  # 问题长度评分
        ))
        
        return max(0.0, min(1.0, clarity_score))
    
    def _evaluate_relevance(self, question: Question) -> float:
        """评估问题相关性"""
        # 基于问题标签、关键词等特征
        tags = question.tags
        keywords = self._extract_keywords(question.content)
        
        # 计算标签覆盖率
        tag_coverage = len(tags) / 5  # 假设理想标签数为5
        
        # 计算关键词覆盖率
        keyword_coverage = len(keywords) / 10  # 假设理想关键词数为10
        
        # 综合评分
        relevance_score = 0.6 * tag_coverage + 0.4 * keyword_coverage
        
        return max(0.0, min(1.0, relevance_score))
    
    def _evaluate_complexity(self, question: Question) -> float:
        """评估问题复杂度"""
        # 基于问题长度、依赖关系等特征
        text = question.content
        words = text.split()
        dependencies = question.dependencies
        
        # 计算问题长度复杂度
        length_complexity = min(1.0, len(words) / 30)  # 假设30个词为理想长度
        
        # 计算依赖复杂度
        dependency_complexity = min(1.0, len(dependencies) / 3)  # 假设3个依赖为理想数量
        
        # 综合评分
        complexity_score = 0.7 * length_complexity + 0.3 * dependency_complexity
        
        return max(0.0, min(1.0, complexity_score))
    
    def _evaluate_uniqueness(self, question: Question) -> float:
        """评估问题独特性"""
        # 基于问题内容、标签等特征
        text = question.content
        tags = question.tags
        
        # 计算问题内容独特性
        content_uniqueness = len(set(text.split())) / len(text.split())
        
        # 计算标签独特性
        tag_uniqueness = len(set(tags)) / len(tags)
        
        # 综合评分
        uniqueness_score = 0.7 * content_uniqueness + 0.3 * tag_uniqueness
        
        return max(0.0, min(1.0, uniqueness_score))
    
    def _evaluate_coverage(self, question: Question) -> float:
        """评估问题覆盖度"""
        # 基于问题类型、领域等特征
        question_type = question.type
        domain = question.domain
        
        # 计算类型覆盖度
        type_coverage = 1.0 if question_type in [
            QuestionType.FUNCTIONAL,
            QuestionType.TECHNICAL,
            QuestionType.SECURITY,
            QuestionType.PERFORMANCE
        ] else 0.5
        
        # 计算领域覆盖度
        domain_coverage = 1.0 if domain != "通用" else 0.5
        
        # 综合评分
        coverage_score = 0.6 * type_coverage + 0.4 * domain_coverage
        
        return max(0.0, min(1.0, coverage_score))
    
    def _calculate_quality_score(self, question: Question) -> float:
        """
        计算问题质量总分
        
        Args:
            question: 问题
            
        Returns:
            质量分数 (0-1)
        """
        metrics = self.quality_metrics.get(question.id)
        if not metrics:
            return 0.0
        
        # 加权计算总分
        total_score = (
            0.3 * metrics.clarity +
            0.25 * metrics.relevance +
            0.15 * metrics.complexity +
            0.15 * metrics.uniqueness +
            0.15 * metrics.coverage
        )
        
        return max(0.0, min(1.0, total_score))
    
    def recommend_questions(
        self,
        context: Dict[str, Any],
        domain: str,
        stage: str,
        count: int = 5
    ) -> List[Question]:
        """
        推荐问题
        
        Args:
            context: 上下文信息
            domain: 领域
            stage: 当前阶段
            count: 需要推荐的问题数量
            
        Returns:
            推荐的问题列表
        """
        # 1. 生成候选问题
        candidate_questions = self.generate_questions(
            context=context,
            domain=domain,
            stage=stage,
            count=count * 2  # 生成更多候选问题
        )
        
        # 2. 根据质量分数和上下文相关性排序
        sorted_questions = sorted(
            candidate_questions,
            key=lambda x: (
                self._calculate_quality_score(x),
                self._calculate_context_relevance(x, context)
            ),
            reverse=True
        )
        
        # 3. 返回推荐的问题
        return sorted_questions[:count]
    
    def _calculate_context_relevance(
        self,
        question: Question,
        context: Dict[str, Any]
    ) -> float:
        """
        计算问题与上下文的相关性
        
        Args:
            question: 问题
            context: 上下文信息
            
        Returns:
            相关性分数 (0-1)
        """
        # 1. 标签匹配度
        context_tags = context.get("tags", [])
        tag_matches = sum(1 for tag in question.tags if tag in context_tags)
        tag_score = tag_matches / max(len(question.tags), 1)
        
        # 2. 关键词匹配度
        context_keywords = context.get("keywords", [])
        question_keywords = self._extract_keywords(question.content)
        keyword_matches = sum(1 for keyword in question_keywords if keyword in context_keywords)
        keyword_score = keyword_matches / max(len(question_keywords), 1)
        
        # 3. 依赖关系匹配度
        context_questions = context.get("answered_questions", [])
        dependency_matches = sum(1 for dep in question.dependencies if dep in context_questions)
        dependency_score = dependency_matches / max(len(question.dependencies), 1)
        
        # 综合评分
        relevance_score = (
            0.4 * tag_score +
            0.4 * keyword_score +
            0.2 * dependency_score
        )
        
        return max(0.0, min(1.0, relevance_score)) 