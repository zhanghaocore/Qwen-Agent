"""
技术术语识别模块
负责识别文本中的技术术语和关键词
"""
import re
import json
import os
from typing import List, Dict, Any, Tuple


class TermExtractor:
    """技术术语识别器，标记可能的技术术语和关键词"""
    
    def __init__(self, dictionary_path=None):
        # 加载技术术语词典
        self.tech_dictionary = self._load_tech_dictionary(dictionary_path)
        
        # 常见编程模式匹配
        self.patterns = {
            'function': re.compile(r'\b(function|函数|方法)\b', re.IGNORECASE),
            'api': re.compile(r'\b(api|接口|endpoint|服务)\b', re.IGNORECASE),
            'database': re.compile(r'\b(database|数据库|表|schema|存储)\b', re.IGNORECASE),
            'auth': re.compile(r'\b(authentication|授权|认证|auth|登录|权限)\b', re.IGNORECASE),
            'format': re.compile(r'\b(json|xml|csv|yaml|格式|文件)\b', re.IGNORECASE),
        }
        
        # 复合术语模式(如'REST API', 'HTTP请求'等)
        self.compound_patterns = [
            (re.compile(r'\b(REST|RESTful)\s*(API|接口)\b', re.IGNORECASE), 'REST API'),
            (re.compile(r'\b(HTTP|HTTPS)\s*(请求|request)\b', re.IGNORECASE), 'HTTP请求'),
            (re.compile(r'\b(OAuth\s*2\.0|JWT)\s*(认证|authentication)\b', re.IGNORECASE), '认证机制'),
            (re.compile(r'\b(SQL|NoSQL)\s*(数据库|查询|database|query)\b', re.IGNORECASE), '数据库技术'),
            (re.compile(r'\b(JSON|XML)\s*(格式|数据|format|data)\b', re.IGNORECASE), '数据格式'),
        ]
    
    def _load_tech_dictionary(self, dictionary_path=None) -> Dict:
        """
        加载技术术语词典，如果提供路径则从文件加载，否则使用内置词典
        
        Args:
            dictionary_path: 词典文件路径
            
        Returns:
            技术术语词典
        """
        if dictionary_path and os.path.exists(dictionary_path):
            try:
                with open(dictionary_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load dictionary from {dictionary_path}: {e}")
        
        # 使用内置默认词典
        return {
            # 编程语言
            'python': {'type': 'programming_language', 'confidence': 1.0},
            'java': {'type': 'programming_language', 'confidence': 1.0},
            'javascript': {'type': 'programming_language', 'confidence': 1.0},
            'typescript': {'type': 'programming_language', 'confidence': 1.0},
            
            # 框架和库
            'django': {'type': 'framework', 'confidence': 1.0},
            'flask': {'type': 'framework', 'confidence': 1.0},
            'fastapi': {'type': 'framework', 'confidence': 1.0},
            'pytorch': {'type': 'library', 'confidence': 1.0},
            'tensorflow': {'type': 'library', 'confidence': 1.0},
            'pandas': {'type': 'library', 'confidence': 1.0},
            'numpy': {'type': 'library', 'confidence': 1.0},
            
            # 数据库
            'mysql': {'type': 'database', 'confidence': 1.0},
            'postgresql': {'type': 'database', 'confidence': 1.0},
            'mongodb': {'type': 'database', 'confidence': 1.0},
            'redis': {'type': 'database', 'confidence': 1.0},
            
            # API相关
            'rest': {'type': 'api_paradigm', 'confidence': 1.0},
            'restful': {'type': 'api_paradigm', 'confidence': 1.0},
            'api': {'type': 'api_concept', 'confidence': 1.0},
            'graphql': {'type': 'api_paradigm', 'confidence': 1.0},
            'http': {'type': 'protocol', 'confidence': 1.0},
            'https': {'type': 'protocol', 'confidence': 1.0},
            'get': {'type': 'http_method', 'confidence': 1.0},
            'post': {'type': 'http_method', 'confidence': 1.0},
            'put': {'type': 'http_method', 'confidence': 1.0},
            'delete': {'type': 'http_method', 'confidence': 1.0},
            
            # 数据格式
            'json': {'type': 'data_format', 'confidence': 1.0},
            'xml': {'type': 'data_format', 'confidence': 1.0},
            'csv': {'type': 'data_format', 'confidence': 1.0},
            'yaml': {'type': 'data_format', 'confidence': 1.0},
            
            # 认证和安全
            'oauth': {'type': 'auth_protocol', 'confidence': 1.0},
            'jwt': {'type': 'auth_token', 'confidence': 1.0},
            'token': {'type': 'auth_concept', 'confidence': 0.7},
            'authentication': {'type': 'security_concept', 'confidence': 0.9},
            'authorization': {'type': 'security_concept', 'confidence': 0.9},
            
            # 通用技术术语
            '用户': {'type': 'entity', 'confidence': 0.8},
            '管理': {'type': 'function', 'confidence': 0.8},
            '服务': {'type': 'component', 'confidence': 0.8},
            '认证': {'type': 'security_concept', 'confidence': 0.9},
            '授权': {'type': 'security_concept', 'confidence': 0.9},
            '数据库': {'type': 'database', 'confidence': 1.0},
            '接口': {'type': 'api_concept', 'confidence': 0.9},
        }
    
    def extract_tokens(self, text: str) -> List[str]:
        """
        对文本进行简单分词
        
        Args:
            text: 输入文本
            
        Returns:
            分词结果列表
        """
        # 简单的基于空格的分词，对于英文足够
        # 对于中文，我们使用一个简单的字符级分词方法
        tokens = []
        
        # 处理英文词
        for word in re.findall(r'\b\w+\b', text.lower()):
            if word and len(word) > 1:  # 忽略单字符token
                tokens.append(word)
        
        # 处理中文词（简单处理，实际项目中应使用专业中文分词工具）
        # 这里先尝试查找2-4个字符的中文短语
        for i in range(2, 5):
            for j in range(len(text) - i + 1):
                phrase = text[j:j+i]
                if re.match(r'^[\u4e00-\u9fff]+$', phrase):  # 只包含中文字符
                    tokens.append(phrase)
        
        return tokens
    
    def identify_compound_terms(self, text: str) -> List[Dict[str, Any]]:
        """
        识别文本中的复合技术术语
        
        Args:
            text: 输入文本
            
        Returns:
            识别的复合术语列表
        """
        compound_terms = []
        
        for pattern, term_type in self.compound_patterns:
            for match in pattern.finditer(text):
                compound_terms.append({
                    'term': match.group(0),
                    'positions': [(match.start(), match.end())],
                    'type': term_type,
                    'confidence': 0.9  # 复合术语通常有较高置信度
                })
                
        return compound_terms
    
    def identify_candidate_terms(self, tokens: List[str], text: str) -> List[Dict[str, Any]]:
        """
        识别潜在的新术语（使用上下文特征）
        
        Args:
            tokens: 分词结果
            text: 原始文本
            
        Returns:
            候选术语列表
        """
        candidates = []
        
        # 识别可能是术语的词组
        for token in tokens:
            # 检查词是否已经在词典中
            if token in self.tech_dictionary:
                continue
                
            # 基于模式识别潜在术语
            is_candidate = False
            term_type = 'unknown'
            confidence = 0.0
            
            # 根据上下文判断是否为潜在术语
            for category, pattern in self.patterns.items():
                for match in pattern.finditer(text.lower()):
                    # 检查该词是否出现在特定模式附近
                    window_start = max(0, match.start() - 50)
                    window_end = min(len(text), match.end() + 50)
                    context_window = text[window_start:window_end].lower()
                    
                    if token in context_window:
                        is_candidate = True
                        term_type = category
                        # 距离模式关键词越近，置信度越高
                        token_pos = context_window.find(token)
                        pattern_pos = context_window.find(match.group(0))
                        distance = abs(token_pos - pattern_pos)
                        confidence = max(confidence, 0.7 - (distance / 100))
            
            # 具有特定后缀的词更可能是技术术语
            tech_suffixes = ['service', 'manager', 'handler', 'controller', 'provider', 'factory', 'builder']
            for suffix in tech_suffixes:
                if token.endswith(suffix):
                    is_candidate = True
                    term_type = 'component'
                    confidence = max(confidence, 0.8)
            
            # 中文术语特征
            cn_suffixes = ['服务', '管理', '控制', '系统', '模块', '引擎', '接口']
            for suffix in cn_suffixes:
                if suffix in token:
                    is_candidate = True
                    term_type = 'component'
                    confidence = max(confidence, 0.8)
            
            if is_candidate:
                # 找到token在原文中的位置
                positions = []
                try:
                    for match in re.finditer(re.escape(token), text, re.IGNORECASE):
                        positions.append((match.start(), match.end()))
                except:
                    # 如果正则表达式有问题，使用简单的字符串查找
                    start = 0
                    while True:
                        start = text.lower().find(token.lower(), start)
                        if start == -1:
                            break
                        positions.append((start, start + len(token)))
                        start += len(token)
                
                if positions:
                    candidates.append({
                        'term': token,
                        'positions': positions,
                        'type': term_type,
                        'confidence': confidence
                    })
        
        return candidates
    
    def extract_technical_terms(self, text: str) -> List[Dict[str, Any]]:
        """
        从文本中提取技术术语
        
        Args:
            text: 输入文本
            
        Returns:
            识别的技术术语列表
        """
        if not text:
            return []
            
        # 分词
        tokens = self.extract_tokens(text)
        
        tech_terms = []
        
        # 1. 匹配已知术语
        for i, token in enumerate(tokens):
            if token.lower() in self.tech_dictionary:
                term_info = self.tech_dictionary[token.lower()]
                
                # 查找token在原文中的位置
                positions = []
                try:
                    for match in re.finditer(r'\b' + re.escape(token) + r'\b', text, re.IGNORECASE):
                        positions.append((match.start(), match.end()))
                except:
                    # 备用方法
                    start = 0
                    while True:
                        start = text.lower().find(token.lower(), start)
                        if start == -1:
                            break
                        positions.append((start, start + len(token)))
                        start += len(token)
                
                if not positions:
                    # 如果没找到完全匹配，尝试部分匹配
                    start = 0
                    while True:
                        start = text.lower().find(token.lower(), start)
                        if start == -1:
                            break
                        positions.append((start, start + len(token)))
                        start += len(token)
                
                if positions:
                    tech_terms.append({
                        'term': token,
                        'positions': positions,
                        'type': term_info['type'],
                        'confidence': term_info['confidence']
                    })
        
        # 2. 识别复合术语
        compound_terms = self.identify_compound_terms(text)
        tech_terms.extend(compound_terms)
        
        # 3. 识别潜在的新术语
        candidate_terms = self.identify_candidate_terms(tokens, text)
        
        # 过滤出高置信度的新术语
        new_terms = [term for term in candidate_terms if term['confidence'] > 0.5]
        tech_terms.extend(new_terms)
        
        return tech_terms
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        处理文本并提取技术术语
        
        Args:
            text: 输入文本
            
        Returns:
            包含提取结果的字典
        """
        tech_terms = self.extract_technical_terms(text)
        
        # 按置信度排序
        tech_terms.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        
        # 统计术语类型
        term_types = {}
        for term in tech_terms:
            term_type = term.get('type', 'unknown')
            term_types[term_type] = term_types.get(term_type, 0) + 1
        
        return {
            'original_text': text,
            'technical_terms': tech_terms,
            'term_count': len(tech_terms),
            'term_types': term_types
        } 