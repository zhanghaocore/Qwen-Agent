"""
句子分割模块
负责将文本分割为语义完整的句子
"""
import re
from typing import List, Dict, Any


class SentenceSplitter:
    """句子分割类，将文本分割为语义完整的句子"""
    
    def __init__(self):
        # 基本句子边界正则 - 修复正则表达式以改进句子分割
        # 这个正则匹配句号、问号、感叹号后跟空格的情况，无需限制下一个字符为大写
        self.sentence_boundary = re.compile(r'(?<=[.!?])\s+')
        
        # 技术术语和缩写字典，避免错误分割
        self.abbreviations = {
            'e.g.': True, 'i.e.': True, 'etc.': True,
            'vs.': True, 'Mr.': True, 'Mrs.': True,
            'Dr.': True, 'Prof.': True, 'Fig.': True,
            'v.': True, 'et al.': True, 'No.': True,
        }
        
        # 列表项模式 (例如：1. 项目 2. 项目)
        self.list_item_pattern = re.compile(r'(\d+\.\s+|\*\s+|[\-•]\s+)')
        
    def contains_abbreviation(self, segment: str) -> bool:
        """
        检查文本片段是否包含常见缩写
        
        Args:
            segment: 文本片段
            
        Returns:
            如果包含缩写返回True，否则返回False
        """
        for abbr in self.abbreviations:
            if abbr in segment:
                return True
        return False
    
    def fix_abbreviation_splits(self, segment: str) -> List[str]:
        """
        修复由于缩写导致的错误分割
        
        Args:
            segment: 包含缩写的文本片段
            
        Returns:
            修复后的句子列表
        """
        # 创建一个临时版本，替换缩写以防被错误分割
        temp_segment = segment
        abbr_markers = {}
        
        for i, abbr in enumerate(self.abbreviations):
            if abbr in segment:
                marker = f"__ABBR_{i}__"
                abbr_markers[marker] = abbr
                temp_segment = temp_segment.replace(abbr, marker)
        
        # 现在分割临时版本
        parts = self.sentence_boundary.split(temp_segment)
        
        # 恢复缩写
        result = []
        for part in parts:
            for marker, abbr in abbr_markers.items():
                part = part.replace(marker, abbr)
            result.append(part)
            
        return result
    
    def process_list_items(self, text: str) -> List[str]:
        """
        处理文本中的列表项，将它们分割为独立句子
        
        Args:
            text: 输入文本
            
        Returns:
            包含处理后列表项的句子列表
        """
        # 查找列表项的起始位置
        matches = list(self.list_item_pattern.finditer(text))
        if not matches:
            return [text]
            
        # 分割列表项
        result = []
        start = 0
        
        # 处理第一句话（如果有列表项前的内容）
        if matches[0].start() > 0:
            result.append(text[:matches[0].start()].strip())
        
        # 处理每个列表项
        for i, match in enumerate(matches):
            start = match.start()
            # 如果这是最后一个列表项，取到文本结尾
            if i == len(matches) - 1:
                end = len(text)
            else:
                end = matches[i+1].start()
            
            item_text = text[start:end].strip()
            if item_text:
                result.append(item_text)
        
        return result
    
    def clean_and_merge_sentences(self, sentences: List[str]) -> List[str]:
        """
        清理句子列表，删除空句子，合并短句子
        
        Args:
            sentences: 初步分割的句子列表
            
        Returns:
            清理后的句子列表
        """
        # 过滤空句子
        filtered = [s.strip() for s in sentences if s.strip()]
        
        if not filtered:
            return []
            
        # 合并过短的句子片段
        result = []
        current = filtered[0]
        
        for i in range(1, len(filtered)):
            # 如果当前句子非常短，且不是列表项，则与当前句子合并
            if len(filtered[i]) < 15 and not self.list_item_pattern.match(filtered[i]):
                current += " " + filtered[i]
            else:
                result.append(current.strip())
                current = filtered[i]
        
        # 添加最后一个句子
        if current:
            result.append(current.strip())
            
        return result
    
    def split_into_sentences(self, text: str) -> List[str]:
        """
        将文本分割为句子
        
        Args:
            text: 输入文本
            
        Returns:
            句子列表
        """
        if not text or not text.strip():
            return []
            
        # 先检查文本是否包含句号等标点，如果没有则直接作为一个句子返回
        if not re.search(r'[.!?]', text):
            return [text]
            
        # 基础规则：句号、问号、感叹号后跟空格
        basic_split = self.sentence_boundary.split(text)
        
        # 处理特殊情况：技术术语缩写、编号列表等
        refined_sentences = []
        for segment in basic_split:
            # 处理缩写
            if self.contains_abbreviation(segment):
                corrected = self.fix_abbreviation_splits(segment)
                refined_sentences.extend(corrected)
            else:
                refined_sentences.append(segment)
        
        # 处理列表项
        list_processed = []
        for sentence in refined_sentences:
            list_processed.extend(self.process_list_items(sentence))
        
        # 最终清理：删除空句子，合并过短片段
        return self.clean_and_merge_sentences(list_processed)
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        处理文本并返回分割后的句子和元数据
        
        Args:
            text: 输入文本
            
        Returns:
            包含句子列表和元数据的字典
        """
        sentences = self.split_into_sentences(text)
        
        return {
            'original_text': text,
            'sentences': sentences,
            'sentence_count': len(sentences),
            'avg_sentence_length': sum(len(s) for s in sentences) / len(sentences) if sentences else 0
        } 