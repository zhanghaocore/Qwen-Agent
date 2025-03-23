"""
文本预处理器主模块
整合清洗、分割、术语识别和规范化功能
"""
from typing import Dict, Any, List

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
        self.original_text = original_text
        self.cleaned_text = ""
        self.sentences = []
        self.tokens = []
        self.tagged_tokens = []
        self.technical_terms = []
        self.normalized_text = ""
        self.metadata = {}


class TextPreprocessor:
    """
    文本预处理器类
    整合文本清洗、句子分割、术语识别和文本规范化功能
    """
    
    def __init__(self, tech_dictionary_path=None):
        """
        初始化文本预处理器
        
        Args:
            tech_dictionary_path: 技术术语词典路径（可选）
        """
        self.cleaner = TextCleaner()
        self.splitter = SentenceSplitter()
        self.term_extractor = TermExtractor(tech_dictionary_path)
        self.normalizer = TextNormalizer()
    
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
        
        # 简单分词 (实际应用中可能需要更复杂的分词)
        result.tokens = result.normalized_text.split()
        
        return result
    
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
        return {
            'original_text': preprocessed.original_text,
            'cleaned_text': preprocessed.cleaned_text,
            'sentences': preprocessed.sentences,
            'tokens': preprocessed.tokens,
            'technical_terms': preprocessed.technical_terms,
            'normalized_text': preprocessed.normalized_text,
            'metadata': preprocessed.metadata
        } 