"""
Text cleaning utility module.
"""

import re
from typing import Dict, Any

class TextCleaner:
    """Text cleaning utility class."""
    
    def clean_text(self, text: str) -> str:
        """
        Clean the input text by removing extra whitespace and normalizing line endings.
        
        Args:
            text: Input text to clean
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Normalize line endings
        text = text.replace('\r\n', '\n')
        return text.strip()

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
        cleaned_text = self.clean_text(text)
        metadata = self.extract_metadata(text)
        
        return {
            'original_text': text,
            'cleaned_text': cleaned_text,
            'metadata': metadata
        } 