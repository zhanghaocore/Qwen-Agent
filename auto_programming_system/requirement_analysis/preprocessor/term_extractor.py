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
            'function': re.compile(r'\b(function|函数|方法|功能|处理|计算|生成|创建|执行)\b', re.IGNORECASE),
            'api': re.compile(r'\b(api|接口|endpoint|服务|微服务|网关|路由)\b', re.IGNORECASE),
            'database': re.compile(r'\b(database|数据库|表|schema|存储|db|数据集|记录|字段|条目)\b', re.IGNORECASE),
            'auth': re.compile(r'\b(authentication|授权|认证|auth|登录|权限|验证|用户认证|鉴权)\b', re.IGNORECASE),
            'format': re.compile(r'\b(json|xml|csv|yaml|excel|格式|文件|数据格式|配置文件)\b', re.IGNORECASE),
            'web': re.compile(r'\b(web|网站|页面|前端|后端|网页|http|浏览器|客户端|服务端)\b', re.IGNORECASE),
            'data': re.compile(r'\b(data|数据|集合|列表|字典|结构|对象|实体|属性)\b', re.IGNORECASE),
            'algorithm': re.compile(r'\b(algorithm|算法|计算|排序|搜索|优化|效率)\b', re.IGNORECASE),
            'security': re.compile(r'\b(security|安全|加密|解密|保护|防护|漏洞|攻击)\b', re.IGNORECASE),
            'performance': re.compile(r'\b(performance|性能|优化|加速|提速|效率|响应时间|吞吐量)\b', re.IGNORECASE),
        }
        
        # 复合术语模式(如'REST API', 'HTTP请求'等)，使用更宽松的匹配
        self.compound_patterns = [
            (re.compile(r'\b(REST|RESTful)[-\s]*(API|接口)\b', re.IGNORECASE), 'REST API'),
            (re.compile(r'\b(HTTP|HTTPS)[-\s]*(请求|request|调用|访问)\b', re.IGNORECASE), 'HTTP请求'),
            (re.compile(r'\b(OAuth\s*2\.0|JWT|Token)[-\s]*(认证|authentication|鉴权)\b', re.IGNORECASE), '认证机制'),
            (re.compile(r'\b(SQL|NoSQL)[-\s]*(数据库|查询|database|query)\b', re.IGNORECASE), '数据库技术'),
            (re.compile(r'\b(JSON|XML|YAML)[-\s]*(格式|数据|format|data|解析|转换)\b', re.IGNORECASE), '数据格式'),
            (re.compile(r'\b(用户|user|account)[-\s]*(认证|authentication|auth|登录|注册)\b', re.IGNORECASE), '用户认证'),
            (re.compile(r'\b(数据|data)[-\s]*(处理|processing|分析|清洗|转换|提取)\b', re.IGNORECASE), '数据处理'),
            (re.compile(r'\b(API|接口)[-\s]*(文档|documentation|说明|规范)\b', re.IGNORECASE), 'API文档'),
            (re.compile(r'\b(数据库|DB)[-\s]*(连接|connection|访问|操作)\b', re.IGNORECASE), '数据库连接'),
            (re.compile(r'\b(文件|file)[-\s]*(上传|下载|传输|读取|写入)\b', re.IGNORECASE), '文件操作'),
            (re.compile(r'\b(安全|security)[-\s]*(检查|验证|校验|审计)\b', re.IGNORECASE), '安全验证'),
            (re.compile(r'\b(缓存|cache)[-\s]*(机制|策略|管理|失效)\b', re.IGNORECASE), '缓存管理'),
            (re.compile(r'\b(负载|load)[-\s]*(均衡|balancing|分发)\b', re.IGNORECASE), '负载均衡'),
            (re.compile(r'\b(分布式|distributed)[-\s]*(系统|计算|架构|服务)\b', re.IGNORECASE), '分布式系统'),
            (re.compile(r'\b(大数据|big\s*data)[-\s]*(分析|处理|存储)\b', re.IGNORECASE), '大数据处理'),
            (re.compile(r'\b(机器学习|ML)[-\s]*(模型|算法|训练|预测)\b', re.IGNORECASE), '机器学习'),
            (re.compile(r'\b(深度学习|DL|神经网络)[-\s]*(模型|算法|训练)\b', re.IGNORECASE), '深度学习'),
            (re.compile(r'\b(自然语言处理|NLP)[-\s]*(模型|算法|分析)\b', re.IGNORECASE), 'NLP'),
            (re.compile(r'\b(云|cloud)[-\s]*(服务|计算|存储|部署)\b', re.IGNORECASE), '云计算'),
            (re.compile(r'\b(容器|container)[-\s]*(编排|管理|部署)\b', re.IGNORECASE), '容器技术'),
            (re.compile(r'\b(微服务|microservice)[-\s]*(架构|设计|通信)\b', re.IGNORECASE), '微服务架构'),
            (re.compile(r'\b(版本|version)[-\s]*(控制|管理|跟踪)\b', re.IGNORECASE), '版本控制'),
            (re.compile(r'\b(持续|continuous)[-\s]*(集成|部署|发布|交付)\b', re.IGNORECASE), 'CI/CD'),
            (re.compile(r'\b(测试|test)[-\s]*(自动化|框架|用例|覆盖)\b', re.IGNORECASE), '测试自动化'),
            (re.compile(r'\b(代码|code)[-\s]*(质量|检查|审计|规范)\b', re.IGNORECASE), '代码质量'),
        ]
        
        # 添加更多技术词组合模式
        self.tech_combinations = [
            ('python', ['开发', '编程', '脚本', '库', '框架', '模块', '包', '函数', '类', '对象', '异步']),
            ('api', ['rest', 'restful', 'http', 'json', 'xml', '设计', '开发', '文档', '测试', '版本', '认证']),
            ('数据库', ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', '查询', '连接', '事务', '索引', '存储', '备份']),
            ('认证', ['oauth', 'jwt', 'token', '用户', '登录', '权限', '会话', '安全', '加密', '授权']),
            ('web', ['前端', '后端', '全栈', 'http', 'html', 'css', 'javascript', '路由', '控制器', '视图', '模板']),
            ('数据', ['处理', '分析', '清洗', '可视化', '挖掘', '加载', '转换', '集成', '管道', '存储', '收集']),
            ('服务', ['微服务', '云', '部署', '扩展', '监控', '负载均衡', '高可用', '容器', '调度', '网关']),
            ('安全', ['加密', '认证', '授权', '攻击', '防护', '漏洞', '扫描', '审计', '合规', '风险']),
            ('测试', ['单元', '集成', '系统', '性能', '负载', '自动化', '覆盖率', '回归', 'mock', '断言']),
            ('部署', ['自动化', '持续', '容器', '环境', '配置', '发布', '回滚', '蓝绿', '金丝雀', '基础设施']),
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
            
            # Python标准库
            'os': {'type': 'python_module', 'confidence': 1.0},
            'sys': {'type': 'python_module', 'confidence': 1.0},
            'datetime': {'type': 'python_module', 'confidence': 1.0},
            'json': {'type': 'python_module', 'confidence': 1.0},
            'csv': {'type': 'python_module', 'confidence': 1.0},
            're': {'type': 'python_module', 'confidence': 1.0},
            'math': {'type': 'python_module', 'confidence': 1.0},
            'random': {'type': 'python_module', 'confidence': 1.0},
            'collections': {'type': 'python_module', 'confidence': 1.0},
            'itertools': {'type': 'python_module', 'confidence': 1.0},
            'functools': {'type': 'python_module', 'confidence': 1.0},
            'pathlib': {'type': 'python_module', 'confidence': 1.0},
            'typing': {'type': 'python_module', 'confidence': 1.0},
            'io': {'type': 'python_module', 'confidence': 1.0},
            'logging': {'type': 'python_module', 'confidence': 1.0},
            'argparse': {'type': 'python_module', 'confidence': 1.0},
            'threading': {'type': 'python_module', 'confidence': 1.0},
            'multiprocessing': {'type': 'python_module', 'confidence': 1.0},
            'subprocess': {'type': 'python_module', 'confidence': 1.0},
            'asyncio': {'type': 'python_module', 'confidence': 1.0},
            'unittest': {'type': 'python_module', 'confidence': 1.0},
            'pytest': {'type': 'testing_tool', 'confidence': 1.0},
            
            # Python数据处理
            'dataframe': {'type': 'data_concept', 'confidence': 1.0},
            'series': {'type': 'data_concept', 'confidence': 0.9},
            'matplotlib': {'type': 'visualization_library', 'confidence': 1.0},
            'seaborn': {'type': 'visualization_library', 'confidence': 1.0},
            'plotly': {'type': 'visualization_library', 'confidence': 1.0},
            'scipy': {'type': 'scientific_library', 'confidence': 1.0},
            'statsmodels': {'type': 'statistical_library', 'confidence': 1.0},
            'nltk': {'type': 'nlp_library', 'confidence': 1.0},
            'spacy': {'type': 'nlp_library', 'confidence': 1.0},
            'transformers': {'type': 'nlp_library', 'confidence': 1.0},
            'huggingface': {'type': 'ai_platform', 'confidence': 1.0},
            'keras': {'type': 'deep_learning_library', 'confidence': 1.0},
            'pyspark': {'type': 'big_data_library', 'confidence': 1.0},
            'dask': {'type': 'parallel_computing_library', 'confidence': 1.0},
            'xgboost': {'type': 'ml_library', 'confidence': 1.0},
            'lightgbm': {'type': 'ml_library', 'confidence': 1.0},
            
            # Web技术
            'http': {'type': 'protocol', 'confidence': 1.0},
            'https': {'type': 'protocol', 'confidence': 1.0},
            'rest': {'type': 'api_style', 'confidence': 1.0},
            'restful': {'type': 'api_style', 'confidence': 1.0},
            'graphql': {'type': 'api_style', 'confidence': 1.0},
            'oauth': {'type': 'authentication', 'confidence': 1.0},
            'jwt': {'type': 'authentication', 'confidence': 1.0},
            'wsgi': {'type': 'web_interface', 'confidence': 1.0},
            'asgi': {'type': 'web_interface', 'confidence': 1.0},
            'ajax': {'type': 'web_technique', 'confidence': 1.0},
            'json': {'type': 'data_format', 'confidence': 1.0},
            'xml': {'type': 'data_format', 'confidence': 1.0},
            'yaml': {'type': 'data_format', 'confidence': 1.0},
            'html': {'type': 'markup_language', 'confidence': 1.0},
            'css': {'type': 'style_language', 'confidence': 1.0},
            'jinja2': {'type': 'template_engine', 'confidence': 1.0},
            'sqlalchemy': {'type': 'orm_library', 'confidence': 1.0},
            'alembic': {'type': 'migration_tool', 'confidence': 1.0},
            'websocket': {'type': 'communication_protocol', 'confidence': 1.0},
            'api': {'type': 'interface_concept', 'confidence': 1.0},
            'microservice': {'type': 'architecture_style', 'confidence': 1.0},
            'mvc': {'type': 'architecture_pattern', 'confidence': 1.0},
            'mvt': {'type': 'architecture_pattern', 'confidence': 1.0},
            'crud': {'type': 'operation_concept', 'confidence': 1.0},
            'middleware': {'type': 'software_component', 'confidence': 1.0},
            
            # 中文术语
            '函数': {'type': 'programming_concept', 'confidence': 1.0},
            '类': {'type': 'programming_concept', 'confidence': 1.0},
            '方法': {'type': 'programming_concept', 'confidence': 1.0},
            '变量': {'type': 'programming_concept', 'confidence': 1.0},
            '参数': {'type': 'programming_concept', 'confidence': 1.0},
            '返回值': {'type': 'programming_concept', 'confidence': 1.0},
            '异常': {'type': 'programming_concept', 'confidence': 1.0},
            '接口': {'type': 'programming_concept', 'confidence': 1.0},
            '数据库': {'type': 'database_concept', 'confidence': 1.0},
            '表': {'type': 'database_concept', 'confidence': 0.9},
            '字段': {'type': 'database_concept', 'confidence': 0.9},
            '查询': {'type': 'database_operation', 'confidence': 0.9},
            '事务': {'type': 'database_concept', 'confidence': 1.0},
            '索引': {'type': 'database_concept', 'confidence': 1.0},
            '算法': {'type': 'computer_science', 'confidence': 1.0},
            '数据结构': {'type': 'computer_science', 'confidence': 1.0},
            '数据分析': {'type': 'data_science', 'confidence': 1.0},
            '机器学习': {'type': 'ai', 'confidence': 1.0},
            '深度学习': {'type': 'ai', 'confidence': 1.0},
            '神经网络': {'type': 'ai', 'confidence': 1.0},
            '模型': {'type': 'data_science', 'confidence': 0.9},
            '训练': {'type': 'ml_process', 'confidence': 0.9},
            '前端': {'type': 'web_development', 'confidence': 1.0},
            '后端': {'type': 'web_development', 'confidence': 1.0},
            '全栈': {'type': 'web_development', 'confidence': 1.0},
            '服务器': {'type': 'infrastructure', 'confidence': 1.0},
            '客户端': {'type': 'infrastructure', 'confidence': 1.0},
            '云计算': {'type': 'infrastructure', 'confidence': 1.0},
            '容器': {'type': 'infrastructure', 'confidence': 1.0},
            '微服务': {'type': 'architecture', 'confidence': 1.0},
            '端口': {'type': 'networking', 'confidence': 0.9},
            '协议': {'type': 'networking', 'confidence': 0.9},
            '加密': {'type': 'security', 'confidence': 1.0},
            '认证': {'type': 'security', 'confidence': 1.0},
            '授权': {'type': 'security', 'confidence': 1.0},
            '权限': {'type': 'security', 'confidence': 0.9},
            '登录': {'type': 'user_operation', 'confidence': 0.9},
            '注册': {'type': 'user_operation', 'confidence': 0.9},
            '测试': {'type': 'software_development', 'confidence': 0.9},
            '部署': {'type': 'devops', 'confidence': 1.0},
            '集成': {'type': 'devops', 'confidence': 0.9},
            '上线': {'type': 'devops', 'confidence': 0.9},
            '优化': {'type': 'performance', 'confidence': 0.9},
            '监控': {'type': 'operations', 'confidence': 1.0},
            '日志': {'type': 'operations', 'confidence': 1.0},

            # DevOps和工具
            'git': {'type': 'version_control', 'confidence': 1.0},
            'github': {'type': 'collaboration_platform', 'confidence': 1.0},
            'gitlab': {'type': 'collaboration_platform', 'confidence': 1.0},
            'docker': {'type': 'containerization', 'confidence': 1.0},
            'kubernetes': {'type': 'orchestration', 'confidence': 1.0},
            'jenkins': {'type': 'ci_cd', 'confidence': 1.0},
            'travis': {'type': 'ci_cd', 'confidence': 1.0},
            'circleci': {'type': 'ci_cd', 'confidence': 1.0},
            'ansible': {'type': 'configuration_management', 'confidence': 1.0},
            'terraform': {'type': 'infrastructure_as_code', 'confidence': 1.0},
            'aws': {'type': 'cloud_platform', 'confidence': 1.0},
            'azure': {'type': 'cloud_platform', 'confidence': 1.0},
            'gcp': {'type': 'cloud_platform', 'confidence': 1.0},
            'lambda': {'type': 'serverless', 'confidence': 0.9},
            'serverless': {'type': 'architecture', 'confidence': 1.0},
            'prometheus': {'type': 'monitoring', 'confidence': 1.0},
            'grafana': {'type': 'visualization', 'confidence': 1.0},
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