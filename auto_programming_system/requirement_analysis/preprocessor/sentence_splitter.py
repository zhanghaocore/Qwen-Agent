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
        # 针对中文和英文分别处理
        self.sentence_boundary_en = re.compile(r'(?<=[.!?])\s+')
        self.sentence_boundary_cn = re.compile(r'(?<=[。！？])')
        
        # 技术术语和缩写字典，避免错误分割
        self.abbreviations = {
            'e.g.': True, 'i.e.': True, 'etc.': True,
            'vs.': True, 'Mr.': True, 'Mrs.': True,
            'Dr.': True, 'Prof.': True, 'Fig.': True,
            'v.': True, 'et al.': True, 'No.': True,
            'Inc.': True, 'Ltd.': True, 'Co.': True,
            'St.': True, 'Ave.': True, 'Jan.': True,
            'Feb.': True, 'Mar.': True, 'Apr.': True,
            'Jun.': True, 'Jul.': True, 'Aug.': True,
            'Sep.': True, 'Oct.': True, 'Nov.': True,
            'Dec.': True, 'a.m.': True, 'p.m.': True,
        }
        
        # 列表项模式 (例如：1. 项目 2. 项目)
        self.list_item_pattern = re.compile(r'(\d+\.\s+|\*\s+|[\-•]\s+)')
        
        # 复杂句子结构
        self.complex_boundary = re.compile(r'(?<=[.!?。！？])\s*(?=[A-Z\u4e00-\u9fff])')
        
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
                # 只替换完整的缩写，不替换部分匹配
                temp_segment = re.sub(r'\b' + re.escape(abbr) + r'\b', marker, temp_segment)
        
        # 现在分割临时版本
        parts = re.split(r'(?<=[.!?])\s+(?=[A-Z])', temp_segment)
        
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
        # 这里处理三种情况:
        # 1. 文本中没有列表项 -> 保持原样返回
        # 2. 只有列表项 -> 每个列表项作为单独句子
        # 3. 引言+列表项 -> 引言作为一个句子，每个列表项作为单独句子
        
        if not text:
            return []
            
        # 处理换行，可能表示列表项
        text = text.replace('\r', '').replace('\n', ' ')
            
        # 查找列表项的起始位置
        matches = list(self.list_item_pattern.finditer(text))
        if not matches:
            return [text]  # 没有列表项，返回原文本
            
        # 分割列表项
        result = []
        
        # 处理第一句话（如果有列表项前的内容）
        if matches[0].start() > 0:
            intro = text[:matches[0].start()].strip()
            if intro:  # 只有非空引言才加入结果
                result.append(intro)
        
        # 处理每个列表项
        for i, match in enumerate(matches):
            start = match.start()
            # 如果这是最后一个列表项，取到文本结尾
            if i == len(matches) - 1:
                end = len(text)
            else:
                end = matches[i+1].start()
            
            item_text = text[start:end].strip()
            if item_text:  # 只添加非空列表项
                result.append(item_text)
        
        # 如果没有找到有效的列表项，返回原文本
        return result if result else [text]
    
    def clean_and_merge_sentences(self, sentences: List[str]) -> List[str]:
        """
        清理句子列表，删除空句子，合并短句子
        
        Args:
            sentences: 初步分割的句子列表
            
        Returns:
            清理后的句子列表
        """
        # 过滤空句子
        filtered = [s.strip() for s in sentences if s and s.strip()]
        
        if not filtered:
            return []
        
        # 如果只有一个句子，直接返回
        if len(filtered) == 1:
            return filtered
            
        # 合并过短的句子片段
        result = []
        temp_sentence = filtered[0]  # 从第一个句子开始
        
        for i in range(1, len(filtered)):
            current = filtered[i]
            
            # 如果当前句子很短，并且不是列表项或特殊格式
            if (len(current) < 15 and 
                not self.list_item_pattern.match(current) and
                not current.startswith(('•', '-', '*'))):
                # 合并到前一个句子
                temp_sentence = temp_sentence + " " + current
            else:
                # 添加积累的句子
                result.append(temp_sentence)
                temp_sentence = current
        
        # 添加最后一个句子
        if temp_sentence:
            result.append(temp_sentence)
            
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
            
        # 处理纯标点文本
        if re.match(r'^[^\w\u4e00-\u9fff]+$', text.strip()):
            return []
            
        # 去除多余空白
        cleaned_text = re.sub(r'\s+', ' ', text.strip())
        
        # 先检查文本是否包含句号等标点，如果没有则直接作为一个句子返回
        if not re.search(r'[.!?。！？]', cleaned_text):
            return [cleaned_text]
        
        # 分割句子 (同时处理中英文标点)
        sentences = []
        
        # 首先按照复杂边界进行分割
        segments = self.complex_boundary.split(cleaned_text)
        
        # 进一步处理每个分段
        for segment in segments:
            # 处理缩写
            if self.contains_abbreviation(segment):
                corrected = self.fix_abbreviation_splits(segment)
                sentences.extend(corrected)
            else:
                sentences.append(segment)
        
        # 处理列表项
        list_processed = []
        for sentence in sentences:
            if self.list_item_pattern.search(sentence):
                list_processed.extend(self.process_list_items(sentence))
            else:
                list_processed.append(sentence)
        
        # 最终清理：删除空句子，合并过短片段
        merged_sentences = self.clean_and_merge_sentences(list_processed)
        
        # 确保所有句子都有实质内容
        final_sentences = []
        for s in merged_sentences:
            # 移除只包含标点符号和空格的句子
            if re.search(r'[A-Za-z0-9\u4e00-\u9fff]', s):
                final_sentences.append(s)
                
        return final_sentences if final_sentences else [cleaned_text]
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        处理文本并返回分割后的句子和元数据
        
        Args:
            text: 输入文本
            
        Returns:
            包含句子列表和元数据的字典
        """
        sentences = self.split_into_sentences(text)
        
        avg_length = 0
        if sentences:
            avg_length = sum(len(s) for s in sentences) / len(sentences)
        
        return {
            'original_text': text,
            'sentences': sentences,
            'sentence_count': len(sentences),
            'avg_sentence_length': avg_length
        } 