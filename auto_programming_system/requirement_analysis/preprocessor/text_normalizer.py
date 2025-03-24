"""
文本规范化模块
负责统一文本格式，如数字表示、单位等
"""
import re
import datetime
from typing import Dict, Any, Match, List, Tuple


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
        # 匹配带单位的数字，支持更多格式和空格变化
        self.number_with_unit_pattern = re.compile(
            r'(\d+(?:\.\d+)?)\s*([KkMmBbGgTt][Bb]?|[kmbt])\b', 
            re.IGNORECASE
        )
        
        # 日期模式，支持多种格式
        self.date_patterns = [
            # MM/DD/YYYY or DD/MM/YYYY or YYYY/MM/DD
            re.compile(r'\b(\d{1,4})[/\-](\d{1,2})[/\-](\d{1,4})\b'),
            
            # Month DD, YYYY
            re.compile(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2})(?:st|nd|rd|th)?,\s*(\d{2,4})\b', re.IGNORECASE),
            
            # DD Month YYYY
            re.compile(r'\b(\d{1,2})(?:st|nd|rd|th)?\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?,\s*(\d{2,4})\b', re.IGNORECASE),
            
            # YYYY年MM月DD日 (中文日期)
            re.compile(r'\b(\d{2,4})年\s*(\d{1,2})月\s*(\d{1,2})日\b'),
        ]
        
        # 时间模式，支持更多格式
        self.time_pattern = re.compile(
            r'\b(\d{1,2}):(\d{2})(?::(\d{2}))?\s*(am|pm|AM|PM|a\.m\.|p\.m\.)?\b'
        )
        
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
        if not text:
            return text
            
        # 替换带单位的数字
        def replace_number_with_unit(match: Match) -> str:
            try:
                number = float(match.group(1))
                unit = match.group(2).lower()
                
                # 处理单位变体，如K/k -> kb, M/m -> mb等
                base_unit = unit[0].lower()
                if base_unit in 'kmgbt' and (len(unit) == 1 or unit == base_unit):
                    # 保持原样返回
                    return match.group(0)
                    
                # 标准化单位格式
                normalized_unit = base_unit
                if len(unit) > 1 and unit[1] == 'b':
                    normalized_unit += 'b'
                
                if normalized_unit in self.number_units:
                    # 转换为标准值
                    value = number * self.number_units[normalized_unit]
                    
                    # 使用适当的格式化
                    if value.is_integer():
                        return f"{int(value)}"
                    else:
                        return f"{value}"
                
                # 不在转换规则中，保持原样
                return match.group(0)
            except:
                # 出现异常，保持原样
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
    
    def _parse_date_parts(self, parts: Tuple[str, str, str]) -> Tuple[int, int, int]:
        """
        解析日期部分并确定年月日顺序
        
        Args:
            parts: 包含日期部分的元组
            
        Returns:
            标准化的(年, 月, 日)元组
        """
        # 尝试检测日期格式
        part1, part2, part3 = parts
        
        # 第一部分是年份的情况 (YYYY-MM-DD)
        if len(part1) == 4 and part1.isdigit() and 1900 <= int(part1) <= 2100:
            year, month, day = int(part1), int(part2), int(part3)
        # 最后一部分是年份的情况 (MM-DD-YYYY 或 DD-MM-YYYY)
        elif len(part3) == 4 and part3.isdigit() and 1900 <= int(part3) <= 2100:
            # 假设是MM-DD-YYYY (美式日期)
            month, day, year = int(part1), int(part2), int(part3)
            # 验证月份和日期合理性，如果不合理，可能是DD-MM-YYYY (欧式日期)
            if month > 12 and day <= 12:
                day, month = month, day
        # 所有部分都是两位数，采用通用规则
        else:
            # 尝试将2位数年份转为4位数
            if len(part3) == 2:
                year = 2000 + int(part3) if int(part3) < 50 else 1900 + int(part3)
            else:
                year = int(part3)
                
            # 假设是月/日/年格式
            month, day = int(part1), int(part2)
            
            # 验证月份和日期合理性，如果不合理，可能是日/月/年
            if month > 12 and day <= 12:
                day, month = month, day
        
        # 确保月份和日期在有效范围内
        if month > 12:
            month = 12
        if day > 31:
            day = 31
            
        return year, month, day
    
    def normalize_dates(self, text: str) -> str:
        """
        将不同格式的日期转换为标准格式 (YYYY-MM-DD)
        
        Args:
            text: 输入文本
            
        Returns:
            日期格式标准化后的文本
        """
        if not text:
            return ""
        
        normalized = text
        
        # 改进：完善日期格式匹配模式，处理更多的日期表示方式
        
        # 匹配 MM/DD/YYYY 或 DD/MM/YYYY 格式（取决于地区）
        # 示例: 03/25/2023, 25/03/2023
        date_pattern1 = re.compile(r'\b(0?[1-9]|1[0-2])/(0?[1-9]|[12][0-9]|3[01])/(\d{4})\b')
        date_pattern2 = re.compile(r'\b(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[0-2])/(\d{4})\b')
        
        # 匹配 YYYY/MM/DD 格式
        # 示例: 2023/03/25
        date_pattern3 = re.compile(r'\b(\d{4})/(0?[1-9]|1[0-2])/(0?[1-9]|[12][0-9]|3[01])\b')
        
        # 匹配 Month DD, YYYY 格式
        # 示例: March 25, 2023
        months = {
            'january': '01', 'february': '02', 'march': '03',
            'april': '04', 'may': '05', 'june': '06',
            'july': '07', 'august': '08', 'september': '09',
            'october': '10', 'november': '11', 'december': '12',
            'jan': '01', 'feb': '02', 'mar': '03',
            'apr': '04', 'jun': '06', 'jul': '07',
            'aug': '08', 'sep': '09', 'oct': '10',
            'nov': '11', 'dec': '12'
        }
        month_pattern = r'(?:' + '|'.join([re.escape(m) for m in months.keys()]) + r')'
        date_pattern4 = re.compile(
            fr'\b({month_pattern})\s+(0?[1-9]|[12][0-9]|3[01])(?:st|nd|rd|th)?,?\s+(\d{{4}})\b',
            re.IGNORECASE
        )
        
        # 匹配 DD Month YYYY 格式
        # 示例: 25 March 2023
        date_pattern5 = re.compile(
            fr'\b(0?[1-9]|[12][0-9]|3[01])\s+({month_pattern})(?:\s+|,\s+)(\d{{4}})\b',
            re.IGNORECASE
        )
        
        # 匹配中文日期格式
        # 示例: 2023年3月25日
        date_pattern6 = re.compile(r'\b(\d{4})年\s*(\d{1,2})月\s*(\d{1,2})日\b')
        
        # 匹配 ISO 8601 日期格式 (YYYY-MM-DD)
        date_pattern7 = re.compile(r'\b(\d{4})-(\d{2})-(\d{2})\b')
        
        def replace_date1(match):
            # MM/DD/YYYY -> YYYY-MM-DD
            month, day, year = match.groups()
            # 验证日期的有效性
            try:
                d = datetime.date(int(year), int(month), int(day))
                return f"{year}-{int(month):02d}-{int(day):02d}"
            except ValueError:
                return match.group(0)  # 保持原始格式
        
        def replace_date2(match):
            # DD/MM/YYYY -> YYYY-MM-DD
            day, month, year = match.groups()
            try:
                d = datetime.date(int(year), int(month), int(day))
                return f"{year}-{int(month):02d}-{int(day):02d}"
            except ValueError:
                return match.group(0)
        
        def replace_date3(match):
            # YYYY/MM/DD -> YYYY-MM-DD
            year, month, day = match.groups()
            try:
                d = datetime.date(int(year), int(month), int(day))
                return f"{year}-{int(month):02d}-{int(day):02d}"
            except ValueError:
                return match.group(0)
        
        def replace_date4(match):
            # Month DD, YYYY -> YYYY-MM-DD
            month_name, day, year = match.groups()
            month_num = months.get(month_name.lower())
            if month_num:
                try:
                    d = datetime.date(int(year), int(month_num), int(day))
                    return f"{year}-{month_num}-{int(day):02d}"
                except ValueError:
                    return match.group(0)
            return match.group(0)
        
        def replace_date5(match):
            # DD Month YYYY -> YYYY-MM-DD
            day, month_name, year = match.groups()
            month_num = months.get(month_name.lower())
            if month_num:
                try:
                    d = datetime.date(int(year), int(month_num), int(day))
                    return f"{year}-{month_num}-{int(day):02d}"
                except ValueError:
                    return match.group(0)
            return match.group(0)
        
        def replace_date6(match):
            # 2023年3月25日 -> 2023-03-25
            year, month, day = match.groups()
            try:
                d = datetime.date(int(year), int(month), int(day))
                return f"{year}-{int(month):02d}-{int(day):02d}"
            except ValueError:
                return match.group(0)
        
        def replace_date7(match):
            # YYYY-MM-DD - 验证格式
            year, month, day = match.groups()
            try:
                d = datetime.date(int(year), int(month), int(day))
                # 已经是标准格式，但确保月和日是两位数
                return f"{year}-{int(month):02d}-{int(day):02d}"
            except ValueError:
                return match.group(0)
        
        # 应用所有格式转换
        normalized = date_pattern1.sub(replace_date1, normalized)
        normalized = date_pattern2.sub(replace_date2, normalized)
        normalized = date_pattern3.sub(replace_date3, normalized)
        normalized = date_pattern4.sub(replace_date4, normalized)
        normalized = date_pattern5.sub(replace_date5, normalized)
        normalized = date_pattern6.sub(replace_date6, normalized)
        normalized = date_pattern7.sub(replace_date7, normalized)
        
        return normalized
    
    def normalize_times(self, text: str) -> str:
        """
        规范化时间格式为24小时制
        
        Args:
            text: 输入文本
            
        Returns:
            规范化后的文本
        """
        if not text:
            return text
            
        def replace_time_format(match: Match) -> str:
            try:
                hour, minute, second, am_pm = match.groups()
                hour = int(hour)
                
                # 验证分钟合法性
                minute = int(minute)
                if not (0 <= minute < 60):
                    minute = 0
                
                # 转换为24小时制
                if am_pm:
                    am_pm = am_pm.lower().replace('.', '')
                    if am_pm in ('pm', 'p.m', 'p.m.') and hour < 12:
                        hour += 12
                    elif am_pm in ('am', 'a.m', 'a.m.') and hour == 12:
                        hour = 0
                    
                hour_str = str(hour).zfill(2)
                minute_str = str(minute).zfill(2)
                
                if second:
                    # 验证秒合法性
                    sec = int(second)
                    if not (0 <= sec < 60):
                        sec = 0
                    second_str = str(sec).zfill(2)
                    return f"{hour_str}:{minute_str}:{second_str}"
                else:
                    return f"{hour_str}:{minute_str}"
            except:
                # 如果解析失败，保持原样
                return match.group(0)
                
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
        if not text:
            return text
            
        # 应用各种规范化处理
        result = text
        result = self.normalize_numbers(result)
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