"""
文本清洗器

负责清理文本中的无关字符、标准化空白字符等基础清洗工作。
"""

import re
from typing import Dict, Any, Optional


class TextCleaner:
    """
    文本清洗器类，用于文本的基础清洗工作。
    
    功能包括：
    - 移除多余空白字符
    - 标准化换行和缩进
    - 移除特殊控制字符
    - 保留必要的标点符号
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化文本清洗器。
        
        参数:
            config: 可选的配置参数字典
        """
        self.config = config or {}
        self._init_patterns()
    
    def _init_patterns(self):
        """初始化正则表达式模式。"""
        # 匹配多余的空白字符
        self.whitespace_pattern = re.compile(r'\s+')
        # 匹配需要移除的控制字符
        self.control_char_pattern = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]')
    
    def clean(self, text: str) -> str:
        """
        清洗输入文本。
        
        参数:
            text: 输入文本
            
        返回:
            清洗后的文本
        """
        if not text:
            return ""
        
        # 移除控制字符
        cleaned_text = self.control_char_pattern.sub('', text)
        
        # 标准化空白字符
        cleaned_text = self.whitespace_pattern.sub(' ', cleaned_text)
        
        # 去除首尾空白
        cleaned_text = cleaned_text.strip()
        
        return cleaned_text

    def extract_metadata(self, text: str) -> Dict[str, Any]:
        """
        提取文本的元数据信息
        
        Args:
            text: 原始文本
            
        Returns:
            包含元数据的字典
        """
        metadata = {
            'length': len(text),
            'word_count': len(text.split()),
            'has_code': bool(re.search(r'```|def |class |import |function|return', text)),
            'has_urls': bool(re.search(r'https?://\S+', text)),
            'has_emails': bool(re.search(r'\S+@\S+\.\S+', text)),
        }
        return metadata
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        处理文本并返回清洗结果和元数据
        
        Args:
            text: 原始文本
            
        Returns:
            包含清洗后文本和元数据的字典
        """
        cleaned_text = self.clean(text)
        metadata = self.extract_metadata(text)
        
        return {
            'original_text': text,
            'cleaned_text': cleaned_text,
            'metadata': metadata
        } 