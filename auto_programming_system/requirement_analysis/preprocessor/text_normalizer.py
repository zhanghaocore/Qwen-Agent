"""
文本规范化器

负责文本格式的标准化处理，包括数字、日期、时间和缩写的标准化。
"""

import re
from typing import Dict, Any, Optional
from datetime import datetime


class TextNormalizer:
    """
    文本规范化器类，用于标准化文本格式。
    
    功能包括：
    - 数字格式标准化
    - 日期格式标准化
    - 时间格式标准化
    - 缩写展开
    - 大小写规范化
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化文本规范化器。
        
        参数:
            config: 可选的配置参数字典
        """
        self.config = config or {}
        self._init_patterns()
    
    def _init_patterns(self):
        """初始化正则表达式模式。"""
        # 数字格式模式
        self.number_pattern = re.compile(r'\b\d+[,.]?\d*\b')
        
        # 日期格式模式（多种日期格式）
        self.date_patterns = [
            # MM/DD/YYYY 或 DD/MM/YYYY
            re.compile(r'\b(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})\b'),
            # YYYY/MM/DD
            re.compile(r'\b(\d{4})[/.-](\d{1,2})[/.-](\d{1,2})\b'),
            # Month DD, YYYY 或 DD Month YYYY
            re.compile(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})\b', re.IGNORECASE),
            re.compile(r'\b(\d{1,2})(?:st|nd|rd|th)?\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?,?\s+(\d{4})\b', re.IGNORECASE),
            # 中文日期格式: YYYY年MM月DD日
            re.compile(r'\b(\d{4})年(\d{1,2})月(\d{1,2})日\b')
        ]
        
        # 时间格式模式
        self.time_pattern = re.compile(r'\b(\d{1,2}):(\d{2})(?::(\d{2}))?\s*(am|pm|AM|PM)?\b')
        
        # 缩写词典
        self.abbreviations = {
            'e.g.': 'for example',
            'i.e.': 'that is',
            'etc.': 'et cetera',
            'vs.': 'versus',
            'approx.': 'approximately',
            'dept.': 'department',
            'est.': 'established',
            'govt.': 'government',
            'intl.': 'international',
            'mgmt.': 'management',
            'min.': 'minimum',
            'max.': 'maximum',
            'misc.': 'miscellaneous',
            'org.': 'organization',
            'pct.': 'percent',
            'qty.': 'quantity',
            'temp.': 'temperature',
            'vol.': 'volume'
        }
    
    def normalize(self, text: str) -> str:
        """
        规范化文本格式。
        
        参数:
            text: 输入文本
            
        返回:
            规范化后的文本
        """
        if not text:
            return ""
        
        # 复制文本，避免修改原始文本
        normalized_text = text
        
        # 根据配置决定执行哪些规范化操作
        if self.config.get('normalize_numbers', True):
            normalized_text = self._normalize_numbers(normalized_text)
        
        if self.config.get('normalize_dates', True):
            normalized_text = self._normalize_dates(normalized_text)
        
        if self.config.get('normalize_times', True):
            normalized_text = self._normalize_times(normalized_text)
        
        if self.config.get('expand_abbreviations', False):
            normalized_text = self._expand_abbreviations(normalized_text)
        
        return normalized_text
    
    def _normalize_numbers(self, text: str) -> str:
        """将数字格式标准化。"""
        def replace_number(match):
            number_str = match.group(0)
            # 移除千位分隔符
            number_str = number_str.replace(',', '')
            try:
                number = float(number_str)
                # 整数和小数处理
                if number.is_integer():
                    return str(int(number))
                else:
                    return str(number)
            except ValueError:
                return number_str
        
        return self.number_pattern.sub(replace_number, text)
    
    def _normalize_dates(self, text: str) -> str:
        """将日期格式标准化为ISO格式(YYYY-MM-DD)。"""
        normalized_text = text
        
        # 处理各种日期格式
        for pattern in self.date_patterns:
            normalized_text = pattern.sub(self._date_replacer, normalized_text)
        
        return normalized_text
    
    def _date_replacer(self, match) -> str:
        """日期格式替换器。"""
        try:
            # 根据匹配组数和模式确定日期格式
            groups = match.groups()
            
            if len(groups) == 3:
                # 检查第一组是否是月份名称
                if groups[0].lower() in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                                       'jul', 'aug', 'sep', 'oct', 'nov', 'dec']:
                    # Month DD, YYYY
                    month_map = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
                               'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
                    month = month_map[groups[0].lower()[:3]]
                    day = int(groups[1])
                    year = int(groups[2])
                    
                # 检查第二组是否是月份名称
                elif groups[1].lower() in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                                         'jul', 'aug', 'sep', 'oct', 'nov', 'dec']:
                    # DD Month YYYY
                    day = int(groups[0])
                    month_map = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
                               'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
                    month = month_map[groups[1].lower()[:3]]
                    year = int(groups[2])
                    
                # 检查第一组是否是四位数年份
                elif len(groups[0]) == 4:
                    # YYYY/MM/DD 或 YYYY年MM月DD日
                    year = int(groups[0])
                    month = int(groups[1])
                    day = int(groups[2])
                    
                else:
                    # MM/DD/YYYY 或 DD/MM/YYYY
                    # 根据配置决定是美式(MM/DD/YYYY)还是欧式(DD/MM/YYYY)日期
                    if self.config.get('date_format', 'US') == 'US':
                        month = int(groups[0])
                        day = int(groups[1])
                    else:
                        day = int(groups[0])
                        month = int(groups[1])
                    
                    year = int(groups[2])
                    # 处理两位数年份
                    if year < 100:
                        year = 2000 + year if year < 50 else 1900 + year
                
                # 验证日期有效性
                datetime(year, month, day)
                
                # 返回ISO格式日期
                return f"{year:04d}-{month:02d}-{day:02d}"
            
            # 原样返回无法解析的日期
            return match.group(0)
            
        except (ValueError, IndexError):
            # 日期无效或解析错误，返回原始字符串
            return match.group(0)
    
    def _normalize_times(self, text: str) -> str:
        """将时间格式标准化为24小时制(HH:MM[:SS])。"""
        def replace_time(match):
            hour = int(match.group(1))
            minute = int(match.group(2))
            second = int(match.group(3)) if match.group(3) else 0
            am_pm = match.group(4)
            
            # 处理12小时制转24小时制
            if am_pm:
                if am_pm.lower() == 'pm' and hour < 12:
                    hour += 12
                elif am_pm.lower() == 'am' and hour == 12:
                    hour = 0
            
            # 格式化时间
            if second:
                return f"{hour:02d}:{minute:02d}:{second:02d}"
            else:
                return f"{hour:02d}:{minute:02d}"
        
        return self.time_pattern.sub(replace_time, text)
    
    def _expand_abbreviations(self, text: str) -> str:
        """展开文本中的缩写。"""
        for abbr, expansion in self.abbreviations.items():
            # 使用单词边界确保只替换完整的缩写
            pattern = r'\b' + re.escape(abbr) + r'\b'
            text = re.sub(pattern, expansion, text)
        
        return text
    
    def normalize_text_case(self, text: str) -> str:
        """
        规范化文本大小写，技术术语保持原样
        
        Args:
            text: 输入文本
            
        Returns:
            规范化后的文本
        """
        # 保留特定技术术语的大小写
        tech_terms = [
            'API', 'REST', 'JSON', 'XML', 'HTTP', 'HTTPS', 'SQL', 'NoSQL', 
            'OAuth', 'JWT', 'GET', 'POST', 'PUT', 'DELETE', 'URL', 'HTML',
            'CSS', 'JavaScript', 'Python', 'Django', 'Flask', 'FastAPI'
        ]
        
        # 创建技术术语的替换标记
        term_markers = {}
        for i, term in enumerate(tech_terms):
            placeholder = f"__TECH_TERM_{i}__"
            term_markers[placeholder] = term
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            text = pattern.sub(placeholder, text)
        
        # 规范化文本大小写
        # 这里我们简单地处理句子首字母大写
        sentences = re.split(r'(?<=[.!?])\s+', text)
        normalized_sentences = []
        
        for sentence in sentences:
            if sentence:
                # 首字母大写
                normalized = sentence[0].upper() + sentence[1:].lower()
                normalized_sentences.append(normalized)
        
        result = ' '.join(normalized_sentences)
        
        # 恢复技术术语
        for placeholder, term in term_markers.items():
            result = result.replace(placeholder, term)
            
        return result
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        处理文本并返回规范化结果
        
        Args:
            text: 输入文本
            
        Returns:
            包含规范化文本的字典
        """
        if not text:
            return {
                'original_text': '',
                'normalized_text': '',
                'normalization_applied': False
            }
            
        normalized_text = self.normalize(text)
        
        return {
            'original_text': text,
            'normalized_text': normalized_text,
            'normalization_applied': text != normalized_text
        } 