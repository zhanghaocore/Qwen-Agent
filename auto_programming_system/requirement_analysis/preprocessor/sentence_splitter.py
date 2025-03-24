"""
句子分割器

负责将文本分割为语义完整的句子。
"""

import re
from typing import List, Dict, Any, Optional


class SentenceSplitter:
    """
    句子分割器类，用于将文本分割为语义完整的句子。
    
    功能包括：
    - 基于标点符号的句子分割
    - 列表项处理
    - 特殊标点和缩写处理
    - 多语言支持（英文和中文）
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化句子分割器。
        
        参数:
            config: 可选的配置参数字典
        """
        self.config = config or {}
        self._init_patterns()
    
    def _init_patterns(self):
        """初始化正则表达式模式。"""
        # 英文句子分割模式
        self.eng_sentence_pattern = re.compile(
            r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s'
        )
        
        # 中文句子分割模式
        self.chn_sentence_pattern = re.compile(
            r'(?<=[。！？；])'
        )
        
        # 列表项模式
        self.list_item_pattern = re.compile(
            r'\n\s*[-*]\s+|\n\s*\d+\.\s+'
        )
    
    def split(self, text: str) -> List[str]:
        """
        将文本分割为句子。
        
        参数:
            text: 输入文本
            
        返回:
            句子列表
        """
        if not text:
            return []
        
        # 处理换行
        text = re.sub(r'\n{2,}', '\n', text)
        
        # 预处理列表项
        list_items = self.list_item_pattern.findall(text)
        for item in list_items:
            text = text.replace(item, ' __LIST_ITEM__ ')
        
        # 分割英文句子
        sentences = self.eng_sentence_pattern.split(text)
        
        # 进一步处理中文句子
        result = []
        for sentence in sentences:
            if re.search('[\u4e00-\u9fff]', sentence):  # 包含中文字符
                chinese_sentences = self.chn_sentence_pattern.split(sentence)
                result.extend([s.strip() for s in chinese_sentences if s.strip()])
            else:
                result.append(sentence.strip())
        
        # 处理列表项
        result = [re.sub(r'__LIST_ITEM__', '', s).strip() for s in result]
        
        # 移除空字符串
        result = [s for s in result if s]
        
        return result
    
    def contains_abbreviation(self, segment: str) -> bool:
        """
        检查文本片段是否包含常见缩写
        
        Args:
            segment: 文本片段
            
        Returns:
            如果包含缩写返回True，否则返回False
        """
        for abbr in self.config.get('abbreviations', {}):
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
        
        for i, abbr in enumerate(self.config.get('abbreviations', {})):
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
                # 合并到前一个句子，确保中间有一个空格
                temp_sentence = temp_sentence.rstrip() + " " + current.lstrip()
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
            
        # 统一处理空格，去除多余空白，但保留单个空格
        cleaned_text = re.sub(r'\s+', ' ', text.strip())
        
        # 先检查文本是否包含句号等标点，如果没有则直接作为一个句子返回
        if not re.search(r'[.!?。！？]', cleaned_text):
            return [cleaned_text]
        
        # 分割句子 (同时处理中英文标点)
        sentences = []
        
        # 首先按照复杂边界进行分割
        # 改进：对中英文标点分别处理，确保空格一致性
        segments = self.config.get('complex_boundary', re.compile(r'(?<=[.!?。！？])(?:\s*)(?=[A-Z\u4e00-\u9fff])')).split(cleaned_text)
        
        # 进一步处理每个分段
        for segment in segments:
            # 处理中文标点（特殊处理，因为中文标点通常不带空格）
            # 拆分中文标点后的句子，同时确保每个句子都是清理过的
            if re.search(r'[。！？]', segment) and re.search(r'[\u4e00-\u9fff]', segment):
                cn_segments = re.split(r'(?<=[。！？])(?!["\')\]】}])', segment)
                for cn_seg in cn_segments:
                    if cn_seg.strip():
                        sentences.append(cn_seg.strip())
            # 处理缩写
            elif self.contains_abbreviation(segment):
                corrected = self.fix_abbreviation_splits(segment)
                sentences.extend([s.strip() for s in corrected if s.strip()])
            else:
                sentences.append(segment.strip())
        
        # 处理列表项
        list_processed = []
        for sentence in sentences:
            if self.list_item_pattern.search(sentence):
                list_items = self.process_list_items(sentence)
                list_processed.extend([item.strip() for item in list_items if item.strip()])
            else:
                list_processed.append(sentence.strip())
        
        # 最终清理：删除空句子，合并过短片段
        merged_sentences = self.clean_and_merge_sentences(list_processed)
        
        # 确保所有句子都有实质内容
        final_sentences = []
        for s in merged_sentences:
            # 移除只包含标点符号和空格的句子
            if re.search(r'[A-Za-z0-9\u4e00-\u9fff]', s):
                # 确保最终句子都经过了空格标准化
                final_s = re.sub(r'\s+', ' ', s.strip())
                final_sentences.append(final_s)
                
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
        
        # 计算元数据
        avg_length = 0
        if sentences:
            avg_length = sum(len(s) for s in sentences) / len(sentences)
            
        return {
            'sentences': sentences,
            'sentence_count': len(sentences),
            'avg_sentence_length': avg_length
        } 