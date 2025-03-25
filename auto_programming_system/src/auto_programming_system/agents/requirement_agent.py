from typing import Any, Dict, List, Optional
import re
from .base_agent import BaseAgent

class RequirementAgent(BaseAgent):
    """需求理解代理，负责解析和理解用户需求"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化需求理解代理
        
        Args:
            config: 代理配置信息
        """
        super().__init__(config)
        self.requirements = []
        self.questions = []
        
    async def process(self, input_data: str) -> Dict[str, Any]:
        """
        处理用户输入的需求
        
        Args:
            input_data: 用户输入的需求文本
            
        Returns:
            解析后的需求结构
        """
        # 1. 文本预处理
        processed_text = await self._preprocess_text(input_data)
        
        # 2. 需求分析
        requirements = await self._analyze_requirements(processed_text)
        
        # 3. 生成问题
        questions = await self._generate_questions(requirements)
        
        # 4. 更新上下文
        self.requirements = requirements
        self.questions = questions
        
        return {
            "requirements": requirements,
            "questions": questions,
            "context": self.get_context()
        }
    
    async def update_context(self, new_context: Dict[str, Any]) -> None:
        """
        更新代理上下文
        
        Args:
            new_context: 新的上下文信息
        """
        self.context.update(new_context)
        
    async def _preprocess_text(self, text: str) -> str:
        """
        预处理输入文本
        
        Args:
            text: 输入文本
            
        Returns:
            处理后的文本
        """
        # 获取预处理配置
        preprocessing_config = self.config.get("preprocessing", {})
        
        # 移除特殊字符
        if preprocessing_config.get("remove_special_chars", True):
            text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
        
        # 规范化空白字符
        if preprocessing_config.get("normalize_whitespace", True):
            text = re.sub(r'\s+', ' ', text)
        
        # 转换为小写
        if preprocessing_config.get("lowercase", False):
            text = text.lower()
        
        return text.strip()
    
    async def _analyze_requirements(self, text: str) -> List[Dict[str, Any]]:
        """
        分析需求文本
        
        Args:
            text: 处理后的文本
            
        Returns:
            需求列表
        """
        # 获取分析配置
        analysis_config = self.config.get("analysis", {})
        max_requirements = analysis_config.get("max_requirements", 10)
        min_confidence = analysis_config.get("min_confidence", 0.8)
        
        # 分割句子
        sentences = re.split(r'[。！？]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        requirements = []
        for sentence in sentences:
            # 识别功能需求
            if re.search(r'创建|实现|编写|开发|构建', sentence):
                requirement = {
                    "type": "functional",
                    "content": sentence,
                    "confidence": 0.9,
                    "keywords": self._extract_keywords(sentence)
                }
                requirements.append(requirement)
            
            # 识别非功能需求
            elif re.search(r'性能|安全|可靠|可用|可维护', sentence):
                requirement = {
                    "type": "non_functional",
                    "content": sentence,
                    "confidence": 0.85,
                    "keywords": self._extract_keywords(sentence)
                }
                requirements.append(requirement)
        
        # 按置信度排序并限制数量
        requirements.sort(key=lambda x: x["confidence"], reverse=True)
        return requirements[:max_requirements]
    
    async def _generate_questions(self, requirements: List[Dict[str, Any]]) -> List[str]:
        """
        根据需求生成问题
        
        Args:
            requirements: 需求列表
            
        Returns:
            问题列表
        """
        questions = []
        
        for req in requirements:
            # 根据需求类型生成不同的问题
            if req["type"] == "functional":
                questions.extend([
                    f"关于{req['content']}，是否需要考虑异常处理？",
                    f"对于{req['content']}，是否有特定的性能要求？",
                    f"在{req['content']}中，是否需要考虑并发处理？"
                ])
            else:
                questions.extend([
                    f"对于{req['content']}，是否有具体的量化指标？",
                    f"在{req['content']}方面，是否有特定的行业标准需要遵循？"
                ])
        
        return questions
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        提取文本中的关键词
        
        Args:
            text: 输入文本
            
        Returns:
            关键词列表
        """
        # 简单的关键词提取实现
        # TODO: 使用更复杂的NLP方法提取关键词
        words = text.split()
        return [w for w in words if len(w) > 1] 