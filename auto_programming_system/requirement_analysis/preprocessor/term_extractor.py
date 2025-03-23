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
            'function': re.compile(r'\b(function|函数|方法|功能)\b', re.IGNORECASE),
            'api': re.compile(r'\b(api|接口|endpoint|服务|微服务)\b', re.IGNORECASE),
            'database': re.compile(r'\b(database|数据库|表|schema|存储|db)\b', re.IGNORECASE),
            'auth': re.compile(r'\b(authentication|授权|认证|auth|登录|权限|验证)\b', re.IGNORECASE),
            'format': re.compile(r'\b(json|xml|csv|yaml|格式|文件|数据格式)\b', re.IGNORECASE),
            'web': re.compile(r'\b(web|网站|页面|前端|后端|网页|http)\b', re.IGNORECASE),
        }
        
        # 复合术语模式(如'REST API', 'HTTP请求'等)，使用更宽松的匹配
        self.compound_patterns = [
            (re.compile(r'\b(REST|RESTful)[-\s]*(API|接口)\b', re.IGNORECASE), 'REST API'),
            (re.compile(r'\b(HTTP|HTTPS)[-\s]*(请求|request)\b', re.IGNORECASE), 'HTTP请求'),
            (re.compile(r'\b(OAuth\s*2\.0|JWT)[-\s]*(认证|authentication)\b', re.IGNORECASE), '认证机制'),
            (re.compile(r'\b(SQL|NoSQL)[-\s]*(数据库|查询|database|query)\b', re.IGNORECASE), '数据库技术'),
            (re.compile(r'\b(JSON|XML)[-\s]*(格式|数据|format|data)\b', re.IGNORECASE), '数据格式'),
            (re.compile(r'\b(用户|user)[-\s]*(认证|authentication|auth)\b', re.IGNORECASE), '用户认证'),
            (re.compile(r'\b(数据|data)[-\s]*(处理|processing)\b', re.IGNORECASE), '数据处理'),
            (re.compile(r'\b(API|接口)[-\s]*(文档|documentation)\b', re.IGNORECASE), 'API文档'),
        ]
        
        # 添加更多技术词组合模式
        self.tech_combinations = [
            ('python', ['开发', '编程', '脚本', '库', '框架']),
            ('api', ['rest', 'restful', 'http', 'json', '设计', '开发']),
            ('数据库', ['sql', 'mysql', 'postgresql', 'mongodb', 'redis']),
            ('认证', ['oauth', 'jwt', '用户', '登录', '权限']),
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
            'go': {'type': 'programming_language', 'confidence': 1.0},
            'rust': {'type': 'programming_language', 'confidence': 1.0},
            'c++': {'type': 'programming_language', 'confidence': 1.0},
            'c#': {'type': 'programming_language', 'confidence': 1.0},
            'php': {'type': 'programming_language', 'confidence': 1.0},
            'ruby': {'type': 'programming_language', 'confidence': 1.0},
            
            # 框架和库
            'django': {'type': 'framework', 'confidence': 1.0},
            'flask': {'type': 'framework', 'confidence': 1.0},
            'fastapi': {'type': 'framework', 'confidence': 1.0},
            'spring': {'type': 'framework', 'confidence': 1.0},
            'express': {'type': 'framework', 'confidence': 1.0},
            'react': {'type': 'framework', 'confidence': 1.0},
            'vue': {'type': 'framework', 'confidence': 1.0},
            'angular': {'type': 'framework', 'confidence': 1.0},
            'pytorch': {'type': 'library', 'confidence': 1.0},
            'tensorflow': {'type': 'library', 'confidence': 1.0},
            'pandas': {'type': 'library', 'confidence': 1.0},
            'numpy': {'type': 'library', 'confidence': 1.0},
            'scikit-learn': {'type': 'library', 'confidence': 1.0},
            
            # 数据库
            'mysql': {'type': 'database', 'confidence': 1.0},
            'postgresql': {'type': 'database', 'confidence': 1.0},
            'mongodb': {'type': 'database', 'confidence': 1.0},
            'redis': {'type': 'database', 'confidence': 1.0},
            'sqlite': {'type': 'database', 'confidence': 1.0},
            'elasticsearch': {'type': 'database', 'confidence': 1.0},
            'cassandra': {'type': 'database', 'confidence': 1.0},
            
            # API相关
            'rest': {'type': 'api_paradigm', 'confidence': 1.0},
            'restful': {'type': 'api_paradigm', 'confidence': 1.0},
            'api': {'type': 'api_concept', 'confidence': 1.0},
            'graphql': {'type': 'api_paradigm', 'confidence': 1.0},
            'http': {'type': 'protocol', 'confidence': 1.0},
            'https': {'type': 'protocol', 'confidence': 1.0},
            'websocket': {'type': 'protocol', 'confidence': 1.0},
            'get': {'type': 'http_method', 'confidence': 1.0},
            'post': {'type': 'http_method', 'confidence': 1.0},
            'put': {'type': 'http_method', 'confidence': 1.0},
            'delete': {'type': 'http_method', 'confidence': 1.0},
            'crud': {'type': 'api_concept', 'confidence': 1.0},
            
            # 数据格式
            'json': {'type': 'data_format', 'confidence': 1.0},
            'xml': {'type': 'data_format', 'confidence': 1.0},
            'csv': {'type': 'data_format', 'confidence': 1.0},
            'yaml': {'type': 'data_format', 'confidence': 1.0},
            'protobuf': {'type': 'data_format', 'confidence': 1.0},
            
            # 认证和安全
            'oauth': {'type': 'auth_protocol', 'confidence': 1.0},
            'jwt': {'type': 'auth_token', 'confidence': 1.0},
            'token': {'type': 'auth_concept', 'confidence': 0.7},
            'authentication': {'type': 'security_concept', 'confidence': 0.9},
            'authorization': {'type': 'security_concept', 'confidence': 0.9},
            'ssl': {'type': 'security_protocol', 'confidence': 1.0},
            'tls': {'type': 'security_protocol', 'confidence': 1.0},
            
            # 部署和运维
            'docker': {'type': 'container', 'confidence': 1.0},
            'kubernetes': {'type': 'orchestration', 'confidence': 1.0},
            'ci/cd': {'type': 'devops', 'confidence': 1.0},
            'jenkins': {'type': 'devops_tool', 'confidence': 1.0},
            'github': {'type': 'version_control', 'confidence': 1.0},
            'gitlab': {'type': 'version_control', 'confidence': 1.0},
            
            # 通用技术术语
            '用户': {'type': 'entity', 'confidence': 0.8},
            '管理': {'type': 'function', 'confidence': 0.8},
            '服务': {'type': 'component', 'confidence': 0.8},
            '认证': {'type': 'security_concept', 'confidence': 0.9},
            '授权': {'type': 'security_concept', 'confidence': 0.9},
            '数据库': {'type': 'database', 'confidence': 1.0},
            '接口': {'type': 'api_concept', 'confidence': 0.9},
            '微服务': {'type': 'architecture', 'confidence': 1.0},
            '云': {'type': 'infrastructure', 'confidence': 0.8},
            '缓存': {'type': 'performance', 'confidence': 0.9},
            '算法': {'type': 'concept', 'confidence': 0.9},
            '登录': {'type': 'security_concept', 'confidence': 0.9},
            '注册': {'type': 'security_concept', 'confidence': 0.9},
        }
    
    def extract_tokens(self, text: str) -> List[str]:
        """
        对文本进行简单分词
        
        Args:
            text: 输入文本
            
        Returns:
            分词结果列表
        """
        # 英文分词
        english_tokens = []
        for word in re.findall(r'\b\w+\b', text.lower()):
            if word and len(word) > 1:  # 忽略单字符token
                english_tokens.append(word)
        
        # 中文分词（简单方法）
        chinese_tokens = []
        
        # 单字符中文词
        for char in re.findall(r'[\u4e00-\u9fff]', text):
            if char:
                chinese_tokens.append(char)
        
        # 多字符中文词组（2-4个字符）
        for i in range(2, 5):
            for j in range(len(text) - i + 1):
                phrase = text[j:j+i]
                if re.match(r'^[\u4e00-\u9fff]+$', phrase):  # 只包含中文字符
                    chinese_tokens.append(phrase)
        
        # 合并结果
        return english_tokens + chinese_tokens
    
    def identify_compound_terms(self, text: str) -> List[Dict[str, Any]]:
        """
        识别文本中的复合技术术语
        
        Args:
            text: 输入文本
            
        Returns:
            识别的复合术语列表
        """
        compound_terms = []
        
        # 使用模式识别复合术语
        for pattern, term_type in self.compound_patterns:
            for match in pattern.finditer(text):
                compound_terms.append({
                    'term': match.group(0),
                    'positions': [(match.start(), match.end())],
                    'type': term_type,
                    'confidence': 0.9  # 复合术语通常有较高置信度
                })
        
        # 识别技术词组合
        lower_text = text.lower()
        for base_term, combinations in self.tech_combinations:
            if base_term in lower_text:
                base_pos = lower_text.find(base_term)
                # 查找前后50个字符窗口
                window_start = max(0, base_pos - 50)
                window_end = min(len(text), base_pos + len(base_term) + 50)
                window = text[window_start:window_end].lower()
                
                for comb_term in combinations:
                    if comb_term in window:
                        # 构建组合术语名称
                        compound_name = f"{base_term}-{comb_term}"
                        compound_terms.append({
                            'term': compound_name,
                            'positions': [(window_start, window_end)],
                            'type': 'compound_term',
                            'confidence': 0.8
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
            if token.lower() in self.tech_dictionary:
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
                    
                    if token.lower() in context_window:
                        is_candidate = True
                        term_type = category
                        # 距离模式关键词越近，置信度越高
                        token_pos = context_window.find(token.lower())
                        pattern_pos = context_window.find(match.group(0).lower())
                        distance = abs(token_pos - pattern_pos)
                        confidence = max(confidence, 0.7 - (distance / 100))
            
            # 具有特定后缀的词更可能是技术术语
            tech_suffixes = ['service', 'manager', 'handler', 'controller', 'provider', 
                            'factory', 'builder', 'processor', 'client', 'server']
            for suffix in tech_suffixes:
                if token.lower().endswith(suffix):
                    is_candidate = True
                    term_type = 'component'
                    confidence = max(confidence, 0.8)
            
            # 中文术语特征
            cn_suffixes = ['服务', '管理', '控制', '系统', '模块', '引擎', '接口', '框架', '平台', '工具']
            for suffix in cn_suffixes:
                if suffix in token:
                    is_candidate = True
                    term_type = 'component'
                    confidence = max(confidence, 0.8)
            
            # 检查是否是常见技术术语的一部分（部分匹配）
            for dict_term in self.tech_dictionary:
                if (len(dict_term) > 3 and  # 只考虑足够长的术语
                    ((dict_term in token.lower()) or (token.lower() in dict_term))):
                    is_candidate = True
                    term_type = self.tech_dictionary[dict_term]['type']
                    # 匹配度越高置信度越高
                    match_ratio = min(len(token), len(dict_term)) / max(len(token), len(dict_term))
                    confidence = max(confidence, 0.6 + 0.3 * match_ratio)
            
            if is_candidate:
                # 找到token在原文中的位置
                positions = []
                try:
                    # 首先尝试完全匹配
                    for match in re.finditer(re.escape(token), text, re.IGNORECASE):
                        positions.append((match.start(), match.end()))
                except:
                    pass
                
                if not positions:
                    # 备用方法：简单的字符串查找
                    start = 0
                    while True:
                        start = text.lower().find(token.lower(), start)
                        if start == -1:
                            break
                        positions.append((start, start + len(token)))
                        start += 1  # 增量较小，允许重叠匹配
                
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
            # 检查字典，使用小写进行匹配
            token_lower = token.lower()
            if token_lower in self.tech_dictionary:
                term_info = self.tech_dictionary[token_lower]
                
                # 查找token在原文中的位置，尝试使用不同的匹配策略
                positions = []
                try:
                    # 策略1: 精确边界匹配
                    for match in re.finditer(r'\b' + re.escape(token) + r'\b', text, re.IGNORECASE):
                        positions.append((match.start(), match.end()))
                except:
                    pass
                
                if not positions:
                    try:
                        # 策略2: 非边界的精确匹配
                        for match in re.finditer(re.escape(token), text, re.IGNORECASE):
                            positions.append((match.start(), match.end()))
                    except:
                        pass
                
                if not positions:
                    # 策略3: 简单的字符串搜索
                    start = 0
                    while True:
                        start = text.lower().find(token_lower, start)
                        if start == -1:
                            break
                        positions.append((start, start + len(token)))
                        start += 1  # 增量较小，允许重叠匹配
                
                if positions:
                    # 找到了匹配位置
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
        
        # 去重，基于术语名称和类型
        unique_terms = {}
        for term in tech_terms:
            key = (term['term'].lower(), term.get('type', 'unknown'))
            # 保留置信度最高的结果
            if key not in unique_terms or term['confidence'] > unique_terms[key]['confidence']:
                unique_terms[key] = term
        
        return list(unique_terms.values())
    
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