"""
文本预处理器主模块
整合清洗、分割、术语识别和规范化功能
"""
from typing import Dict, Any, List, Optional
import re
import json

from .text_cleaner import TextCleaner
from .sentence_splitter import SentenceSplitter
from .term_extractor import TermExtractor
from .text_normalizer import TextNormalizer


class PreprocessedText:
    """
    预处理后的文本模型
    存储预处理的各个阶段的结果和元数据
    """
    
    def __init__(self, original_text: str):
        """
        初始化预处理文本对象
        
        Args:
            original_text: 原始文本
        """
        self.original_text = original_text
        self.cleaned_text = ""
        self.sentences = []
        self.tokens = []
        self.tagged_tokens = []
        self.technical_terms = []
        self.normalized_text = ""
        self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将对象转换为字典表示
        
        Returns:
            代表当前对象的字典
        """
        return {
            'original_text': self.original_text,
            'cleaned_text': self.cleaned_text,
            'sentences': self.sentences,
            'tokens': self.tokens,
            'tagged_tokens': self.tagged_tokens,
            'technical_terms': self.technical_terms,
            'normalized_text': self.normalized_text,
            'metadata': self.metadata
        }
    
    def to_json(self) -> str:
        """
        将对象转换为JSON字符串
        
        Returns:
            JSON格式的字符串表示
        """
        def convert_to_serializable(obj):
            if isinstance(obj, dict):
                return {k: convert_to_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_serializable(item) for item in obj]
            elif isinstance(obj, tuple):
                return list(obj)
            else:
                return obj
                
        serializable_dict = convert_to_serializable(self.to_dict())
        return json.dumps(serializable_dict, ensure_ascii=False, indent=2)


class TextProcessor:
    """
    文本预处理器类
    整合文本清洗、句子分割、术语识别和文本规范化功能
    """
    
    def __init__(self, tech_dictionary_path: Optional[str] = None):
        """
        初始化文本预处理器
        
        Args:
            tech_dictionary_path: 技术术语词典路径（可选）
        """
        self.cleaner = TextCleaner()
        self.splitter = SentenceSplitter()
        self.term_extractor = TermExtractor(tech_dictionary_path)
        self.normalizer = TextNormalizer()
    
    def process(self, text: str) -> str:
        """
        处理文本并返回规范化后的文本
        
        Args:
            text: 原始输入文本
            
        Returns:
            预处理后的文本字符串
        """
        # 调用 preprocess 方法获取完整的预处理结果
        result = self.preprocess(text)
        
        # 返回规范化后的文本
        return result.normalized_text or result.cleaned_text or text
    
    def preprocess(self, text: str) -> PreprocessedText:
        """
        预处理文本
        
        Args:
            text: 原始输入文本
            
        Returns:
            预处理后的文本对象
        """
        if not text or not text.strip():
            return PreprocessedText("")
            
        result = PreprocessedText(text)
        
        # 1. 文本清洗
        cleaning_result = self.cleaner.process(text)
        result.cleaned_text = cleaning_result['cleaned_text']
        result.metadata.update({
            'original_length': len(text),
            'cleaned_length': len(result.cleaned_text),
        })
        result.metadata.update(cleaning_result['metadata'])
        
        # 2. 句子分割
        splitting_result = self.splitter.process(result.cleaned_text)
        result.sentences = splitting_result['sentences']
        result.metadata.update({
            'sentence_count': splitting_result['sentence_count'],
            'avg_sentence_length': splitting_result['avg_sentence_length']
        })
        
        # 3. 术语识别
        term_result = self.term_extractor.process(result.cleaned_text)
        result.technical_terms = term_result['technical_terms']
        result.metadata.update({
            'term_count': term_result['term_count'],
            'term_types': term_result['term_types']
        })
        
        # 4. 文本规范化
        normalizing_result = self.normalizer.process(result.cleaned_text)
        result.normalized_text = normalizing_result['normalized_text']
        result.metadata.update({
            'normalization_applied': normalizing_result['normalization_applied']
        })
        
        # 5. 分词 (简单基于空格的分词，实际应用中可能需要更复杂的分词)
        result.tokens = self._tokenize(result.normalized_text)
        result.metadata['token_count'] = len(result.tokens)
        
        return result
    
    def _tokenize(self, text: str) -> List[str]:
        """
        简单的文本分词
        
        Args:
            text: 要分词的文本
            
        Returns:
            分词结果列表
        """
        if not text:
            return []
            
        # 英文分词 - 基于空格和标点
        tokens = []
        
        # 移除标点符号，分割成token
        # 保留字母、数字和中文字符
        cleaned_text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
        
        # 按空格分割
        for token in cleaned_text.split():
            if token:
                tokens.append(token)
        
        return tokens
    
    def process_batch(self, texts: List[str]) -> List[PreprocessedText]:
        """
        批量预处理多个文本
        
        Args:
            texts: 文本列表
            
        Returns:
            预处理后的文本对象列表
        """
        return [self.preprocess(text) for text in texts]
    
    def to_dict(self, preprocessed: PreprocessedText) -> Dict[str, Any]:
        """
        将预处理文本对象转换为字典
        
        Args:
            preprocessed: 预处理后的文本对象
            
        Returns:
            包含预处理结果的字典
        """
        return preprocessed.to_dict()
    
    def to_json(self, preprocessed: PreprocessedText) -> str:
        """
        将预处理文本对象转换为JSON字符串
        
        Args:
            preprocessed: 预处理后的文本对象
            
        Returns:
            JSON格式的字符串
        """
        return preprocessed.to_json() 