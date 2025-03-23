"""
文本规范化模块
负责统一文本格式，如数字表示、单位等
"""
import re
from typing import Dict, Any


class TextNormalizer:
    """文本规范化类，统一文本格式，如数字表示、单位等"""
    
    def __init__(self):
        # 数字单位转换规则
        self.number_units = {
            'k': 1000,
            'm': 1000000,
            'b': 1000000000,
            'kb': 1024,
            'mb': 1024 * 1024,
            'gb': 1024 * 1024 * 1024,
            'tb': 1024 * 1024 * 1024 * 1024,
        }
        
        # 常见简写及全称
        self.abbreviations = {
            'db': 'database',
            'dbs': 'databases',
            'auth': 'authentication',
            'app': 'application',
            'apps': 'applications',
            'info': 'information',
            'config': 'configuration',
            'admin': 'administrator',
            'dev': 'development',
            'prod': 'production',
            'func': 'function',
            'param': 'parameter',
            'params': 'parameters',
            'var': 'variable',
            'vars': 'variables',
            'obj': 'object',
            'lib': 'library',
            'libs': 'libraries',
            'dir': 'directory',
            'dirs': 'directories',
            'repo': 'repository',
            'repos': 'repositories',
            'impl': 'implementation',
            'sec': 'second',
            'secs': 'seconds',
            'min': 'minute',
            'mins': 'minutes',
            'hr': 'hour',
            'hrs': 'hours',
        }
        
        # 编译正则表达式
        self.number_with_unit_pattern = re.compile(
            r'(\d+(?:\.\d+)?)\s*(k|m|b|kb|mb|gb|tb)\b', 
            re.IGNORECASE
        )
        
        self.date_patterns = [
            # MM/DD/YYYY or DD/MM/YYYY
            re.compile(r'\b(\d{1,2})[/\-](\d{1,2})[/\-](\d{2,4})\b'),
            # Month DD, YYYY
            re.compile(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{1,2})(?:st|nd|rd|th)?,\s+(\d{2,4})\b', re.IGNORECASE),
        ]
        
        self.time_pattern = re.compile(r'\b(\d{1,2}):(\d{2})(?::(\d{2}))?\s*(am|pm)?\b', re.IGNORECASE)
        
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        
        self.url_pattern = re.compile(r'(https?://[^\s]+)')
        
        self.word_pattern = re.compile(r'\b([a-zA-Z]+)\b')
    
    def normalize_numbers(self, text: str) -> str:
        """
        标准化文本中的数字表示
        
        Args:
            text: 输入文本
            
        Returns:
            规范化后的文本
        """
        # 替换带单位的数字
        def replace_number_with_unit(match):
            number = float(match.group(1))
            unit = match.group(2).lower()
            
            if unit in self.number_units:
                # 转换为标准值
                value = number * self.number_units[unit]
                
                # 使用适当的格式化
                if value.is_integer():
                    return f"{int(value)}"
                else:
                    return f"{value}"
            
            return match.group(0)
            
        return self.number_with_unit_pattern.sub(replace_number_with_unit, text)
    
    def expand_abbreviations(self, text: str) -> str:
        """
        展开文本中的常见缩写
        
        Args:
            text: 输入文本
            
        Returns:
            规范化后的文本
        """
        def replace_abbreviation(match):
            word = match.group(1).lower()
            if word in self.abbreviations:
                return self.abbreviations[word]
            return match.group(1)
            
        return self.word_pattern.sub(replace_abbreviation, text)
    
    def normalize_dates(self, text: str) -> str:
        """
        规范化日期格式为ISO格式 (YYYY-MM-DD)
        
        Args:
            text: 输入文本
            
        Returns:
            规范化后的文本
        """
        result = text
        
        # 处理 MM/DD/YYYY 或 DD/MM/YYYY 格式
        # 注意：这里有歧义，我们假设是MM/DD/YYYY格式
        def replace_date_format(match):
            month, day, year = match.groups()
            
            # 确保年份有4位
            if len(year) == 2:
                year = '20' + year if int(year) < 50 else '19' + year
                
            # 确保月和日有两位数
            month = month.zfill(2)
            day = day.zfill(2)
            
            return f"{year}-{month}-{day}"
            
        result = self.date_patterns[0].sub(replace_date_format, result)
        
        # 处理 Month DD, YYYY 格式
        month_to_num = {
            'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
            'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
            'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
        }
        
        def replace_text_date(match):
            month, day, year = match.groups()
            month_num = month_to_num.get(month.lower()[:3], '01')
            
            # 确保年份有4位
            if len(year) == 2:
                year = '20' + year if int(year) < 50 else '19' + year
                
            # 确保日有两位数
            day = day.zfill(2)
            
            return f"{year}-{month_num}-{day}"
            
        result = self.date_patterns[1].sub(replace_text_date, result)
        
        return result
    
    def normalize_times(self, text: str) -> str:
        """
        规范化时间格式为24小时制
        
        Args:
            text: 输入文本
            
        Returns:
            规范化后的文本
        """
        def replace_time_format(match):
            hour, minute, second, am_pm = match.groups()
            hour = int(hour)
            
            # 转换为24小时制
            if am_pm and am_pm.lower() == 'pm' and hour < 12:
                hour += 12
            elif am_pm and am_pm.lower() == 'am' and hour == 12:
                hour = 0
                
            hour_str = str(hour).zfill(2)
            minute_str = minute
            
            if second:
                return f"{hour_str}:{minute_str}:{second}"
            else:
                return f"{hour_str}:{minute_str}"
                
        return self.time_pattern.sub(replace_time_format, text)
    
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
    
    def normalize(self, text: str) -> str:
        """
        规范化文本
        
        Args:
            text: 输入文本
            
        Returns:
            规范化后的文本
        """
        # 应用各种规范化处理
        result = self.normalize_numbers(text)
        result = self.normalize_dates(result)
        result = self.normalize_times(result)
        
        # 展开缩写这一步是可选的，一些缩写可能是技术术语
        # 所以默认不展开，除非特别指定
        # result = self.expand_abbreviations(result)
        
        # 规范化文本大小写通常不需要对于技术需求，因为可能会改变技术术语
        # 因此默认不对大小写做处理
        # result = self.normalize_text_case(result)
        
        return result
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        处理文本并返回规范化结果
        
        Args:
            text: 输入文本
            
        Returns:
            包含规范化文本的字典
        """
        normalized_text = self.normalize(text)
        
        return {
            'original_text': text,
            'normalized_text': normalized_text,
            'normalization_applied': text != normalized_text
        } 