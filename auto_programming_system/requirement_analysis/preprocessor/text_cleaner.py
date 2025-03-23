"""
文本清洗模块
负责对原始需求文本进行清洗和基础预处理
"""
import re
from typing import Dict, List, Any


class TextCleaner:
    """文本清洗类，负责处理原始输入文本"""
    
    def __init__(self):
        # 配置正则表达式规则
        self.rules = {
            'multiple_spaces': re.compile(r'\s+'),
            # 修改特殊字符规则，更好地保留常见标点
            'special_chars': re.compile(r'[^\w\s\.,;:!?()[\]{}"\'\-+]'),
            'urls': re.compile(r'https?://\S+'),
            'emails': re.compile(r'\S+@\S+\.\S+'),
        }
        
        # 技术术语保护列表，清洗时保留
        self.tech_terms = [
            'API', 'REST', 'RESTful', 'JSON', 'XML', 'HTTP', 'HTTPS', 'GET', 'POST',
            'PUT', 'DELETE', 'SQL', 'NoSQL', 'Python', 'Java', 'JavaScript', 
            'TypeScript', 'Flask', 'Django', 'FastAPI', 'Spring', 'Express',
            'CSV', 'DataFrame', 'OAuth', 'JWT', 'GraphQL', 'MongoDB', 'MySQL',
            'PostgreSQL', 'Redis', 'Docker', 'Kubernetes', 'Git', 'GitHub'
        ]
        
    def clean_text(self, text: str) -> str:
        """
        清洗文本，移除无关字符，标准化空白字符
        
        Args:
            text: 原始文本
            
        Returns:
            清洗后的文本
        """
        # 如果输入为空，直接返回
        if not text or not text.strip():
            return ""
            
        # 保存技术术语（临时替换为标记，以防被规则清洗掉）
        protected_terms = {}
        for i, term in enumerate(self.tech_terms):
            # 使用大小写不敏感匹配，但保留原文大小写
            pattern = re.compile(r'\b{}\b'.format(re.escape(term)), re.IGNORECASE)
            matches = list(pattern.finditer(text))
            
            for match_idx, match in enumerate(matches):
                match_text = match.group(0)  # 获取实际匹配的文本
                placeholder = f"__TECH_TERM_{i}_{match_idx}__"
                protected_terms[placeholder] = term  # 存储标准化的技术术语
                text = text[:match.start()] + placeholder + text[match.end():]
        
        # 标准化空白字符
        text = self.rules['multiple_spaces'].sub(' ', text)
        
        # 处理特殊字符，但保留必要标点
        text = self.rules['special_chars'].sub('', text)
        
        # 恢复保护的技术术语（使用正确的大小写形式）
        for placeholder, term in protected_terms.items():
            text = text.replace(placeholder, term)
            
        # 去除首尾空白
        text = text.strip()
            
        return text
    
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
            'has_urls': bool(self.rules['urls'].search(text)),
            'has_emails': bool(self.rules['emails'].search(text)),
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