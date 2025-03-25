"""
高级需求分析工具
实现多层次需求挖掘所需的各种工具
"""

from typing import Dict, List, Any, Optional
import json
import re
from difflib import SequenceMatcher
from datetime import datetime
import uuid

from .question_bank import (
    QuestionBankManager,
    Question,
    QuestionType,
    QuestionDifficulty
)


class DomainClassifierTool:
    """对初始需求进行领域分类，确定适用的问题库和分析策略"""
    
    description = "基于初始需求文本，识别其所属的应用领域，返回领域类型和关键特征"
    parameters = [{
        'name': 'requirement_text',
        'type': 'string',
        'description': '用户的初始需求描述文本',
        'required': True
    }]
    
    def __init__(self):
        """初始化领域分类工具"""
        # 定义领域特征模式
        self.feature_patterns = {
            "web应用": {
                "基础特征": [
                    "网站", "前端", "后端", "页面", "UI", "网页", "浏览器",
                    "响应式", "单页面", "多页面", "网站", "门户", "电商",
                    "博客", "论坛", "社区", "内容管理", "CMS", "企业官网"
                ],
                "功能特征": [
                    "认证", "授权", "登录", "注册", "表单", "搜索",
                    "上传", "下载", "评论", "分享", "支付", "购物车",
                    "订单", "会员", "积分", "优惠券", "商品管理", "库存管理"
                ],
                "技术特征": [
                    "SEO", "CDN", "缓存", "会话", "Cookie", "HTTPS",
                    "API", "WebSocket", "前后端分离", "微服务", "容器化",
                    "CI/CD", "自动化部署", "监控告警", "日志分析", "性能优化"
                ],
                "展示特征": [
                    "数据展示", "图表", "仪表盘", "列表", "表格",
                    "菜单", "导航", "轮播", "布局", "响应式设计",
                    "移动适配", "暗黑模式", "主题切换", "动画效果"
                ],
                "用户体验": [
                    "交互", "动画", "主题", "多语言", "国际化",
                    "本地化", "自适应", "移动优先", "无障碍", "性能优化",
                    "加载优化", "错误处理", "用户反馈", "操作引导"
                ]
            },
            "数据处理": {
                "基础特征": [
                    "数据", "分析", "处理", "统计", "报表", "图表",
                    "excel", "计算", "汇总", "ETL", "数据仓库", "数据湖",
                    "数据治理", "数据质量", "数据安全", "数据挖掘"
                ],
                "处理类型": [
                    "数据清洗", "ETL", "转换", "过滤", "聚合",
                    "归一化", "标准化", "去重", "合并", "数据脱敏",
                    "数据加密", "数据压缩", "数据备份", "数据恢复"
                ],
                "分析功能": [
                    "数据挖掘", "预测分析", "统计分析", "相关性分析",
                    "趋势分析", "异常检测", "模式识别", "机器学习",
                    "深度学习", "自然语言处理", "计算机视觉", "推荐系统"
                ],
                "可视化": [
                    "数据可视化", "报表生成", "图表展示", "仪表板",
                    "实时监控", "趋势图", "散点图", "热力图", "地图",
                    "3D可视化", "交互式图表", "动态报表", "自定义报表"
                ],
                "数据特征": [
                    "实时数据", "历史数据", "结构化数据", "非结构化数据",
                    "时序数据", "流数据", "批量数据", "大数据", "高维数据",
                    "稀疏数据", "缺失数据", "噪声数据", "多源数据"
                ]
            },
            "API服务": {
                "基础特征": [
                    "API", "接口", "服务", "微服务", "端点", "REST",
                    "HTTP", "RPC", "WebService", "网关", "服务网格",
                    "API网关", "服务编排", "服务治理", "服务注册"
                ],
                "服务特性": [
                    "认证", "授权", "限流", "熔断", "降级", "负载均衡",
                    "服务发现", "配置中心", "服务监控", "链路追踪",
                    "性能分析", "错误处理", "重试机制", "超时控制"
                ],
                "接口特征": [
                    "RESTful", "GraphQL", "SOAP", "gRPC", "WebSocket",
                    "异步", "实时", "批量", "流式", "长连接", "短连接",
                    "心跳检测", "断线重连", "消息队列", "事件驱动"
                ],
                "安全特征": [
                    "加密", "签名", "令牌", "OAuth", "JWT", "HTTPS",
                    "SSL", "TLS", "防重放", "防篡改", "防注入",
                    "访问控制", "审计日志", "安全扫描", "漏洞检测"
                ],
                "管理特征": [
                    "监控", "日志", "追踪", "文档", "测试", "版本",
                    "部署", "网关", "限流", "熔断", "降级", "重试",
                    "超时", "负载均衡", "服务发现", "配置管理"
                ]
            }
        }
        
        # 定义通用应用特征
        self.general_features = {
            "性能需求": [
                "高性能", "低延迟", "高并发", "实时", "响应时间",
                "吞吐量", "负载", "性能指标", "QPS", "TPS", "IOPS",
                "CPU使用率", "内存使用", "网络带宽", "磁盘IO"
            ],
            "安全需求": [
                "安全", "加密", "认证", "授权", "审计", "防攻击",
                "数据安全", "访问控制", "漏洞扫描", "入侵检测",
                "防火墙", "WAF", "DDoS防护", "数据脱敏"
            ],
            "可靠性": [
                "高可用", "容错", "备份", "恢复", "监控", "告警",
                "日志", "追踪", "故障转移", "负载均衡", "服务降级",
                "熔断", "限流", "重试", "超时"
            ],
            "扩展性": [
                "可扩展", "模块化", "插件", "微服务", "分布式",
                "集群", "水平扩展", "垂直扩展", "服务网格",
                "容器化", "云原生", "弹性伸缩", "负载均衡"
            ],
            "维护性": [
                "易维护", "文档", "测试", "部署", "版本控制",
                "持续集成", "持续部署", "自动化", "监控告警",
                "日志分析", "性能分析", "问题诊断", "运维管理"
            ]
        }
        
        # 定义领域特征权重
        self.domain_weights = {
            "web应用": {
                "基础特征": 1.0,
                "功能特征": 0.9,
                "技术特征": 0.8,
                "展示特征": 0.7,
                "用户体验": 0.8
            },
            "数据处理": {
                "基础特征": 1.0,
                "处理类型": 0.9,
                "分析功能": 0.8,
                "可视化": 0.7,
                "数据特征": 0.9
            },
            "API服务": {
                "基础特征": 1.0,
                "服务特性": 0.9,
                "接口特征": 0.8,
                "安全特征": 0.7,
                "管理特征": 0.6
            }
        }
        
        # 定义匹配策略权重
        self.match_strategy_weights = {
            "exact_match": 1.0,
            "word_match": 0.8,
            "edit_distance": 0.6,
            "keyword_match": 0.7,
            "semantic_match": 0.5
        }
    
    def call(self, params: str, **kwargs) -> str:
        """执行领域分类"""
        try:
            # 验证输入参数
            if not params or not isinstance(params, str):
                raise ValueError("输入参数不能为空且必须是字符串")
            
            # 解析JSON
            try:
                params_dict = json.loads(params)
            except json.JSONDecodeError as e:
                raise ValueError(f"输入参数必须是有效的JSON格式: {str(e)}")
            
            # 验证必要参数
            if 'requirement_text' not in params_dict:
                raise ValueError("缺少必要参数：requirement_text")
            
            requirement_text = params_dict['requirement_text']
            if not isinstance(requirement_text, str):
                raise ValueError("requirement_text必须是字符串类型")
            
            # 执行领域分类
            domains = self._classify_domain(requirement_text)
            
            # 提取关键特征
            key_features = self._extract_key_features(requirement_text, domains)
            
            return json.dumps({
                'primary_domain': domains[0] if domains else None,
                'secondary_domains': domains[1:] if len(domains) > 1 else [],
                'key_features': key_features
            }, ensure_ascii=False)
            
        except Exception as e:
            raise ValueError(str(e))
    
    def _classify_domain(self, text: str) -> List[str]:
        """分析文本并返回领域分类结果
        
        Args:
            text: 需求文本
            
        Returns:
            按置信度排序的领域列表
        """
        # 计算每个领域的得分
        domain_scores = {}
        text_lower = text.lower()
        
        # 预处理：检查强特征词
        strong_features = {
            "web应用": ["网站", "前端", "页面", "ui", "web", "电商", "商城", "购物", "商品", "界面", "展示", "平台"],
            "数据处理": ["数据分析", "数据处理", "数据挖掘", "etl", "数据清洗", "数据统计", "可视化", "报表"],
            "API服务": ["api", "接口", "微服务", "restful", "rpc"]
        }
        
        # 根据强特征词初步判断领域
        initial_domains = []
        domain_feature_counts = {}  # 记录每个领域匹配的特征数量
        
        for domain, features in strong_features.items():
            matched_features = [feature for feature in features if feature in text_lower]
            if matched_features:
                initial_domains.append(domain)
                domain_feature_counts[domain] = len(matched_features)
        
        # 如果找到多个领域，设置较低的阈值
        threshold = 0.02 if len(initial_domains) > 1 else 0.04
        
        # 特殊处理：Web应用和数据处理的组合场景
        if "web应用" in initial_domains and "数据处理" in initial_domains:
            web_features = ["界面", "展示", "前端", "页面", "平台"]
            data_features = ["数据分析", "数据处理", "数据挖掘", "可视化"]
            
            web_count = sum(1 for f in web_features if f in text_lower)
            data_count = sum(1 for f in data_features if f in text_lower)
            
            # 如果Web特征更显著，将其设为主要领域
            if web_count >= data_count:
                initial_domains.remove("web应用")
                initial_domains.append("web应用")  # 将Web应用放在最后，提高其权重
        
        for domain, features in self.feature_patterns.items():
            domain_score = 0
            total_weight = 0
            feature_counts = {}  # 记录每个类别的特征匹配数
            
            for category, patterns in features.items():
                category_weight = self.domain_weights.get(domain, {}).get(category, 0.5)
                category_score = 0
                matched_features = 0
                
                for pattern in patterns:
                    pattern_lower = pattern.lower()
                    # 使用多种匹配策略
                    if pattern_lower in text_lower:  # 直接匹配
                        matched_features += 1
                        category_score += self.match_strategy_weights["exact_match"]
                    elif self._fuzzy_match(pattern_lower, text_lower):  # 模糊匹配
                        matched_features += 1
                        category_score += self._calculate_match_score(pattern_lower, text_lower)
                
                # 记录特征匹配数
                feature_counts[category] = matched_features
                
                # 归一化类别得分
                if patterns:
                    category_score = (category_score / len(patterns)) * category_weight
                    domain_score += category_score
                    total_weight += category_weight
            
            # 计算特征覆盖率
            coverage_score = self._calculate_coverage_score(feature_counts, domain)
            
            # 归一化领域得分
            if total_weight > 0:
                domain_score = (domain_score / total_weight) * (1 + coverage_score)
                # 如果是初步判断的领域，根据匹配的特征数量提高得分
                if domain in initial_domains:
                    feature_count_bonus = domain_feature_counts.get(domain, 1)
                    domain_score *= (1 + 0.2 * feature_count_bonus)
                domain_scores[domain] = domain_score
        
        # 按得分排序并返回领域列表
        sorted_domains = sorted(
            domain_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # 返回得分大于阈值的领域
        domains = [domain for domain, score in sorted_domains if score > threshold]
        
        # 如果没有匹配到任何领域，根据关键词判断返回默认领域
        if not domains:
            if any(kw in text_lower for kw in ["数据分析", "数据处理", "数据挖掘", "etl", "数据清洗", "可视化", "报表"]):
                return ["数据处理"]
            elif any(kw in text_lower for kw in ["api", "接口", "微服务", "restful", "rpc"]):
                return ["API服务"]
            else:
                return ["web应用"]
        
        # 如果是Web应用和数据处理的组合场景，确保两个领域都被返回
        if "web应用" in initial_domains and "数据处理" in initial_domains:
            if "web应用" in domains and "数据处理" not in domains:
                domains.append("数据处理")
            elif "数据处理" in domains and "web应用" not in domains:
                domains.append("web应用")
        
        return domains
    
    def _fuzzy_match(self, pattern: str, text: str) -> bool:
        """使用多种匹配策略检查模式是否在文本中
        
        Args:
            pattern: 要匹配的模式
            text: 要搜索的文本
            
        Returns:
            是否匹配成功
        """
        # 1. 完全匹配
        if pattern in text:
            return True
            
        # 2. 分词匹配
        pattern_words = set(pattern.split())
        text_words = set(text.split())
        if len(pattern_words) > 0 and pattern_words.issubset(text_words):
            return True
            
        # 3. 编辑距离匹配
        similarity = SequenceMatcher(None, pattern, text).ratio()
        if similarity > 0.6:  # 降低相似度阈值
            return True
            
        # 4. 关键词匹配
        pattern_keywords = set(word for word in pattern.split() if len(word) > 1)
        text_keywords = set(word for word in text.split() if len(word) > 1)
        if len(pattern_keywords) > 0 and pattern_keywords.issubset(text_keywords):
            return True
            
        # 5. 语义匹配
        if self._semantic_match(pattern, text):
            return True
            
        return False
    
    def _semantic_match(self, pattern: str, text: str) -> bool:
        """使用语义相似度进行匹配
        
        Args:
            pattern: 要匹配的模式
            text: 要搜索的文本
            
        Returns:
            是否匹配成功
        """
        # 扩展同义词词典
        synonyms = {
            # Web应用领域
            "网站": ["web", "网站", "网页", "门户", "站点", "平台", "系统", "商城", "商店", "商务"],
            "电商": ["电商", "商城", "购物", "商店", "网店", "在线商城", "网上商城"],
            "商品": ["商品", "产品", "货物", "物品", "商品", "货品", "商品"],
            "会员": ["会员", "用户", "客户", "消费者", "买家", "顾客", "访客"],
            "订单": ["订单", "交易", "购买", "下单", "结算", "支付"],
            
            # 数据处理领域
            "数据": ["数据", "信息", "资料", "记录", "内容", "资源", "资产"],
            "分析": ["分析", "统计", "计算", "评估", "研究", "挖掘", "处理"],
            "处理": ["处理", "加工", "转换", "清洗", "整理", "过滤", "提取"],
            "报表": ["报表", "报告", "图表", "统计表", "分析表", "数据表"],
            "挖掘": ["挖掘", "发现", "提取", "分析", "研究", "探索"],
            
            # API服务领域
            "接口": ["接口", "api", "服务", "endpoint", "服务端点", "调用点"],
            "服务": ["服务", "微服务", "接口", "功能", "能力", "组件"],
            "认证": ["认证", "鉴权", "验证", "授权", "登录", "身份验证"],
            "安全": ["安全", "加密", "保护", "防护", "防御", "保障"],
            "监控": ["监控", "观察", "追踪", "检测", "诊断", "分析"]
        }
        
        # 将模式转换为同义词集合
        pattern_synonyms = set()
        for word in pattern.split():
            word = word.lower()
            if word in synonyms:
                pattern_synonyms.update(synonyms[word])
            else:
                pattern_synonyms.add(word)
        
        # 检查文本中是否包含任何同义词
        text_words = set(text.split())
        return bool(pattern_synonyms & text_words)  # 使用集合交集
    
    def _calculate_match_score(self, pattern: str, text: str) -> float:
        """计算匹配得分
        
        Args:
            pattern: 匹配模式
            text: 目标文本
            
        Returns:
            匹配得分
        """
        # 1. 完全匹配
        if pattern in text:
            return self.match_strategy_weights["exact_match"]
            
        # 2. 分词匹配
        pattern_words = set(pattern.split())
        text_words = set(text.split())
        if len(pattern_words) > 0 and pattern_words.issubset(text_words):
            return self.match_strategy_weights["word_match"]
            
        # 3. 编辑距离匹配
        similarity = SequenceMatcher(None, pattern, text).ratio()
        if similarity > 0.6:  # 降低相似度阈值
            return self.match_strategy_weights["edit_distance"]
            
        # 4. 关键词匹配
        pattern_keywords = set(word for word in pattern.split() if len(word) > 1)
        text_keywords = set(word for word in text.split() if len(word) > 1)
        if len(pattern_keywords) > 0 and pattern_keywords.issubset(text_keywords):
            return self.match_strategy_weights["keyword_match"]
            
        # 5. 语义匹配
        if self._semantic_match(pattern, text):
            return self.match_strategy_weights["semantic_match"]
            
        return 0.0
    
    def _calculate_coverage_score(self, feature_counts: Dict[str, int], domain: str) -> float:
        """计算特征覆盖率得分
        
        Args:
            feature_counts: 每个类别的特征匹配数
            domain: 当前计算的领域
            
        Returns:
            覆盖率得分
        """
        if not feature_counts:
            return 0.0
            
        # 计算每个类别的覆盖率
        coverage_scores = []
        domain_features = self.feature_patterns.get(domain, {})
        
        for category, count in feature_counts.items():
            if category in domain_features:
                total_features = len(domain_features[category])
                if total_features > 0:
                    coverage = count / total_features
                    coverage_scores.append(coverage)
        
        # 计算平均覆盖率
        if coverage_scores:
            return sum(coverage_scores) / len(coverage_scores)
        
        return 0.0
    
    def _extract_key_features(self, text: str, domains: List[str]) -> List[str]:
        """根据领域提取需求中的关键特征
        
        Args:
            text: 需求文本
            domains: 识别出的领域列表
            
        Returns:
            提取出的关键特征列表
        """
        features = []
        text_lower = text.lower()
        
        # 1. 提取领域特定特征
        for domain in domains:
            if domain in self.feature_patterns:
                domain_patterns = self.feature_patterns[domain]
                for category, patterns in domain_patterns.items():
                    category_features = []
                    for pattern in patterns:
                        pattern_lower = pattern.lower()
                        if pattern_lower in text_lower or self._fuzzy_match(pattern_lower, text_lower):
                            category_features.append(pattern)
                    if category_features:
                        # 对于数据处理领域，特别处理分析功能和可视化
                        if domain == "数据处理":
                            if category == "基础特征":
                                # 处理分析功能
                                analysis_features = [f for f in category_features if "分析" in f.lower()]
                                if analysis_features:
                                    features.append(f"{domain}-分析功能:{','.join(analysis_features)}")
                                    category_features = [f for f in category_features if "分析" not in f.lower()]
                                # 处理可视化功能
                                visual_features = [f for f in category_features if any(kw in f.lower() for kw in ["可视化", "展示", "报表"])]
                                if visual_features:
                                    features.append(f"{domain}-可视化功能:{','.join(visual_features)}")
                                    category_features = [f for f in category_features if not any(kw in f.lower() for kw in ["可视化", "展示", "报表"])]
                        if category_features:  # 确保还有其他特征
                            features.append(f"{domain}-{category}:{','.join(category_features)}")
        
        # 2. 提取通用特征
        for category, patterns in self.general_features.items():
            category_features = []
            for pattern in patterns:
                pattern_lower = pattern.lower()
                if pattern_lower in text_lower or self._fuzzy_match(pattern_lower, text_lower):
                    category_features.append(pattern)
            if category_features:
                features.append(f"通用-{category}:{','.join(category_features)}")
        
        # 3. 提取数字相关的特征（如版本号、数量级等）
        number_patterns = {
            r"(\d+\.?\d*)\s*(ms|毫秒)": "响应时间要求",
            r"(\d+\.?\d*)\s*(分钟|小时)": "时间要求",
            r"(\d+\.?\d*)\s*(MB|GB|TB)": "数据量要求",
            r"(\d+\.?\d*)\s*(用户|并发)": "用户量要求",
            r"(\d+\.?\d*)%": "百分比指标",
            r"版本\s*(\d+\.?\d*\.?\d*)": "版本要求",
            r"(\d+\.?\d*)\s*(条|个|项)": "数量要求"
        }
        
        for pattern, feature_name in number_patterns.items():
            matches = re.findall(pattern, text_lower)
            if matches:
                for match in matches:
                    value = match[0] if isinstance(match, tuple) else match
                    # 根据特征名称和上下文判断领域
                    if feature_name in ["数据量要求", "响应时间要求"] or "数据" in text_lower:
                        features.append(f"数据处理-{feature_name}:{value}")
                    else:
                        features.append(f"指标-{feature_name}:{value}")
        
        # 4. 提取时间相关的特征
        time_patterns = {
            r"每(天|周|月|年)": "周期性要求",
            r"实时": "实时性要求",
            r"(\d+)秒内": "时间限制",
            r"(\d+)(分钟|小时)内": "时间限制"
        }
        
        for pattern, feature_name in time_patterns.items():
            matches = re.findall(pattern, text_lower)
            if matches:
                features.append(f"时间-{feature_name}")
        
        return list(set(features))  # 去重


class QuestionGeneratorTool:
    """基于当前对话上下文和领域分类，生成下一步应该提问的问题"""
    
    description = "基于已有的需求信息和对话历史，生成下一步应该询问的问题，以深化需求理解"
    parameters = [{
        'name': 'requirement_text',
        'type': 'string',
        'description': '用户的初始需求描述文本',
        'required': True
    }]
    
    def __init__(self):
        """初始化问题生成器"""
        self.question_bank = QuestionBankManager()
        self._initialize_question_bank()
    
    def _initialize_question_bank(self):
        """初始化问题库"""
        # 添加一些基础问题
        base_questions = [
            Question(
                id=str(uuid.uuid4()),
                type=QuestionType.FUNCTIONAL,
                difficulty=QuestionDifficulty.MEDIUM,
                content="这个功能的主要用户是谁？",
                answer="需要明确目标用户群体，包括用户角色、使用场景等",
                tags=["用户分析", "需求分析"],
                domain="通用",
                dependencies=[],
                created_at=datetime.now(),
                updated_at=datetime.now(),
                version=1,
                metadata={"stage": "initial"}
            ),
            Question(
                id=str(uuid.uuid4()),
                type=QuestionType.TECHNICAL,
                difficulty=QuestionDifficulty.MEDIUM,
                content="系统需要处理的数据量大概是多少？",
                answer="需要评估数据规模，包括用户数量、数据量、并发量等",
                tags=["性能", "架构"],
                domain="通用",
                dependencies=[],
                created_at=datetime.now(),
                updated_at=datetime.now(),
                version=1,
                metadata={"stage": "initial"}
            ),
            # 添加更多基础问题...
        ]
        
        for question in base_questions:
            self.question_bank.add_question(question)
    
    def call(self, params: str, **kwargs) -> str:
        """
        生成下一个问题
        
        Args:
            params: 参数JSON字符串
            **kwargs: 其他参数
            
        Returns:
            生成的问题JSON字符串
        """
        try:
            # 解析参数
            params_dict = json.loads(params)
            requirement_text = params_dict.get('requirement_text', '')
            
            # 获取领域分类
            domain_classifier = DomainClassifierTool()
            domain_result = json.loads(domain_classifier.call(json.dumps({
                'requirement_text': requirement_text
            })))
            domains = domain_result.get('domains', [])
            
            # 根据领域和当前理解生成问题
            questions = self._generate_questions_for_stage(
                domains=domains,
                current_understanding=requirement_text,
                stage=self._determine_discussion_stage(requirement_text)
            )
            
            # 从问题库中获取相关问题
            bank_questions = self._get_relevant_questions(domains, requirement_text)
            
            # 合并生成的问题和问题库中的问题
            all_questions = questions + bank_questions
            
            # 返回结果
            return json.dumps({
                'questions': all_questions,
                'stage': self._determine_discussion_stage(requirement_text),
                'domains': domains
            })
            
        except Exception as e:
            return json.dumps({
                'error': str(e),
                'questions': []
            })
    
    def _get_relevant_questions(self, domains: List[str], requirement_text: str) -> List[str]:
        """
        从问题库中获取相关问题
        
        Args:
            domains: 领域列表
            requirement_text: 需求文本
            
        Returns:
            相关问题列表
        """
        questions = []
        
        # 按领域获取问题
        for domain in domains:
            domain_questions = self.question_bank.get_questions_by_domain(domain)
            questions.extend(domain_questions)
        
        # 按关键词搜索问题
        keywords = self._extract_keywords(requirement_text)
        for keyword in keywords:
            keyword_questions = self.question_bank.search_questions(keyword)
            questions.extend(keyword_questions)
        
        # 去重并转换为文本
        unique_questions = list(set(q.content for q in questions))
        return unique_questions
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        从文本中提取关键词
        
        Args:
            text: 输入文本
            
        Returns:
            关键词列表
        """
        # 简单的关键词提取实现
        words = text.split()
        # 过滤停用词和短词
        keywords = [w for w in words if len(w) > 2]
        return list(set(keywords))  # 去重
    
    def _determine_discussion_stage(self, requirement_text: str) -> str:
        """根据需求文本确定当前讨论阶段"""
        # 简单的文本长度判断，实际应用中可能需要更复杂的逻辑
        if len(requirement_text) < 100:
            return "initial"
        elif len(requirement_text) < 500:
            return "detailed"
        else:
            return "final"
    
    def _generate_questions_for_stage(
        self, domains: List[str], current_understanding: str, stage: str
    ) -> List[str]:
        """根据当前阶段生成适当的问题"""
        # 根据阶段从问题库中获取相关问题
        stage_questions = self.question_bank.search_questions(
            query="",
            question_type=QuestionType.FUNCTIONAL if stage == "initial" else QuestionType.TECHNICAL
        )
        
        # 过滤掉不相关的问题
        relevant_questions = []
        for question in stage_questions:
            # 检查问题是否与当前领域相关
            if any(domain in question.domain for domain in domains):
                relevant_questions.append(question.content)
        
        return relevant_questions


class TechDecisionAnalyzerTool:
    """分析需求并提供技术决策建议，包括技术栈选择和实现方案"""
    
    description = "基于需求分析结果，提供技术栈选择建议和实现方案，包括优缺点分析和备选方案"
    parameters = [{
        'name': 'domain',
        'type': 'string',
        'description': '需求所属的主要领域',
        'required': True
    }, {
        'name': 'requirements_summary',
        'type': 'string',
        'description': '需求的详细摘要描述',
        'required': True
    }, {
        'name': 'technical_constraints',
        'type': 'string',
        'description': '已知的技术约束条件',
        'required': True
    }]
    
    def call(self, params: str, **kwargs) -> str:
        """提供技术决策建议"""
        try:
            params_dict = json.loads(params)
            domain = params_dict.get('domain', '')
            requirements_summary = params_dict.get('requirements_summary', '')
            technical_constraints = params_dict.get('technical_constraints', '')
            
            # 分析技术决策点
            decision_points = self._analyze_decision_points(domain, requirements_summary)
            
            # 生成技术建议
            tech_recommendations = self._generate_tech_recommendations(decision_points, technical_constraints)
            
            return json.dumps({
                'decision_points': decision_points,
                'tech_recommendations': tech_recommendations,
                'architecture_recommendation': self._suggest_architecture(domain, requirements_summary, technical_constraints)
            }, ensure_ascii=False)
            
        except Exception as e:
            return f"技术决策分析过程出错: {str(e)}"
    
    def _analyze_decision_points(self, domain: str, requirements_summary: str) -> List[Dict[str, Any]]:
        """分析需求，识别关键技术决策点"""
        decision_points = []
        
        # 根据领域识别关键决策点
        if "web应用" in domain:
            decision_points.append({
                "name": "前端框架选择",
                "description": "选择合适的前端框架或库",
                "importance": "高"
            })
            decision_points.append({
                "name": "后端框架选择",
                "description": "选择合适的后端框架或库",
                "importance": "高"
            })
            decision_points.append({
                "name": "数据库选择",
                "description": "选择适合需求的数据库系统",
                "importance": "高"
            })
        elif "数据处理" in domain:
            decision_points.append({
                "name": "数据处理框架",
                "description": "选择适合的数据处理框架或库",
                "importance": "高"
            })
            decision_points.append({
                "name": "数据存储方案",
                "description": "选择适合数据量和查询模式的存储方案",
                "importance": "高"
            })
        
        # 通用决策点
        decision_points.append({
            "name": "部署方案",
            "description": "选择合适的部署和运维方案",
            "importance": "中"
        })
        decision_points.append({
            "name": "安全策略",
            "description": "确定系统的安全策略和实现方案",
            "importance": "高"
        })
        
        return decision_points
    
    def _generate_tech_recommendations(self, decision_points: List[Dict[str, Any]], 
                                      technical_constraints: str) -> Dict[str, Dict[str, Any]]:
        """为每个决策点生成技术建议"""
        recommendations = {}
        
        tech_options = {
            "前端框架选择": {
                "推荐选项": "React",
                "理由": "React具有强大的组件模型和广泛的社区支持，适合构建复杂交互的现代Web应用",
                "备选方案": ["Vue.js", "Angular", "Svelte"],
                "备选方案分析": "Vue.js更易上手但生态略小；Angular功能全面但学习曲线陡峭；Svelte性能优异但社区较小。"
            },
            "后端框架选择": {
                "推荐选项": "Flask",
                "理由": "Flask轻量灵活，适合快速开发API服务，与各种数据库和扩展良好集成",
                "备选方案": ["Django", "FastAPI", "Express.js"],
                "备选方案分析": "Django功能更全面但较重；FastAPI性能更好且支持异步；Express.js需要使用Node.js生态。"
            },
            "数据库选择": {
                "推荐选项": "PostgreSQL",
                "理由": "PostgreSQL功能全面，支持关系型和JSON数据，性能优秀且有良好扩展性",
                "备选方案": ["MySQL", "MongoDB", "SQLite"],
                "备选方案分析": "MySQL更适合简单的关系型数据；MongoDB适合非结构化数据；SQLite适合嵌入式或小型应用。"
            },
            "数据处理框架": {
                "推荐选项": "Pandas",
                "理由": "Pandas操作简便，适合中小规模数据处理，与Python科学计算生态良好集成",
                "备选方案": ["Spark", "Dask", "NumPy"],
                "备选方案分析": "Spark适合大规模分布式处理；Dask适合并行计算；NumPy适合纯数值计算。"
            },
            "数据存储方案": {
                "推荐选项": "PostgreSQL + TimescaleDB",
                "理由": "组合支持关系数据和时序数据，适合多种查询模式且性能良好",
                "备选方案": ["InfluxDB", "MongoDB + GridFS", "ElasticSearch"],
                "备选方案分析": "InfluxDB专注时序数据；MongoDB适合文档存储；ElasticSearch适合全文搜索。"
            },
            "部署方案": {
                "推荐选项": "Docker + Kubernetes",
                "理由": "提供良好的容器化和编排能力，适合复杂系统的可扩展部署",
                "备选方案": ["传统VM部署", "Serverless", "PaaS平台"],
                "备选方案分析": "传统VM部署管理复杂；Serverless适合低负载高波动场景；PaaS平台便捷但灵活性较低。"
            },
            "安全策略": {
                "推荐选项": "OAuth2 + HTTPS + WAF",
                "理由": "组合提供认证、传输加密和攻击防护，覆盖主要安全风险",
                "备选方案": ["JWT + SSL", "API Key + TLS", "SAML + VPN"],
                "备选方案分析": "不同组合适合不同安全需求和集成场景，需根据具体情况选择。"
            }
        }
        
        # 根据决策点生成建议
        for point in decision_points:
            point_name = point["name"]
            if point_name in tech_options:
                recommendations[point_name] = tech_options[point_name]
        
        return recommendations
    
    def _suggest_architecture(self, domain: str, requirements_summary: str, 
                             technical_constraints: str) -> Dict[str, Any]:
        """根据需求和约束条件推荐系统架构"""
        architecture = {
            "web应用": {
                "架构类型": "三层架构",
                "组件": [
                    {"名称": "前端层", "技术": "React + Redux", "职责": "用户界面和交互逻辑"},
                    {"名称": "API服务层", "技术": "Flask + SQLAlchemy", "职责": "业务逻辑和数据访问"},
                    {"名称": "数据存储层", "技术": "PostgreSQL", "职责": "数据持久化"}
                ],
                "关键接口": [
                    {"名称": "REST API", "描述": "前端与后端通信的RESTful接口"},
                    {"名称": "数据库接口", "描述": "通过ORM访问数据库"}
                ]
            },
            "数据处理": {
                "架构类型": "流处理架构",
                "组件": [
                    {"名称": "数据收集层", "技术": "Kafka", "职责": "数据摄入和缓冲"},
                    {"名称": "处理层", "技术": "Spark Streaming", "职责": "实时数据处理"},
                    {"名称": "存储层", "技术": "HDFS + Hive", "职责": "原始数据和结果存储"},
                    {"名称": "展示层", "技术": "Dash + Plotly", "职责": "数据可视化"}
                ],
                "关键接口": [
                    {"名称": "数据接入API", "描述": "外部系统写入数据的接口"},
                    {"名称": "查询API", "描述": "获取处理结果的接口"}
                ]
            },
            "通用应用": {
                "架构类型": "分层架构",
                "组件": [
                    {"名称": "表示层", "技术": "取决于具体需求", "职责": "用户界面和交互"},
                    {"名称": "业务层", "技术": "取决于具体需求", "职责": "业务逻辑实现"},
                    {"名称": "数据层", "技术": "取决于具体需求", "职责": "数据访问和存储"}
                ],
                "关键接口": [
                    {"名称": "API接口", "描述": "系统对外提供的功能接口"},
                    {"名称": "数据访问接口", "描述": "业务逻辑访问数据的接口"}
                ]
            }
        }
        
        # 根据领域返回对应架构
        for key in domain.split(","):
            key = key.strip()
            if key in architecture:
                return architecture[key]
        
        # 默认返回通用架构
        return architecture["通用应用"]


class RequirementSpecGeneratorTool:
    """生成完整的需求规范文档，整合所有分析结果"""
    
    description = "根据对话历史和分析结果，生成结构化的需求规范文档"
    parameters = [{
        'name': 'domain',
        'type': 'string',
        'description': '需求所属的主要领域',
        'required': True
    }, {
        'name': 'discussion_summary',
        'type': 'string',
        'description': '需求讨论的摘要内容',
        'required': True
    }, {
        'name': 'tech_decisions',
        'type': 'string',
        'description': '技术决策和架构建议',
        'required': True
    }]
    
    def __init__(self):
        """初始化需求规范生成器"""
        # 定义完整性检查项
        self.completeness_checks = {
            "需求完整性": {
                "功能需求": [
                    "是否明确定义了所有核心功能?",
                    "是否包含了功能的优先级?",
                    "是否定义了功能的验收标准?",
                    "是否考虑了异常处理流程?",
                    "是否定义了用户角色和权限?"
                ],
                "非功能需求": [
                    "是否定义了性能指标?",
                    "是否定义了安全要求?",
                    "是否定义了可用性要求?",
                    "是否定义了可扩展性要求?",
                    "是否定义了兼容性要求?"
                ],
                "业务规则": [
                    "是否定义了业务约束?",
                    "是否定义了业务流程?",
                    "是否定义了数据规则?",
                    "是否定义了计算逻辑?",
                    "是否定义了报表要求?"
                ]
            },
            "技术完整性": {
                "架构设计": [
                    "是否明确了系统架构?",
                    "是否定义了技术栈选择?",
                    "是否考虑了系统集成?",
                    "是否定义了部署方案?",
                    "是否考虑了可扩展性?"
                ],
                "数据设计": [
                    "是否定义了数据模型?",
                    "是否定义了数据流?",
                    "是否考虑了数据量?",
                    "是否定义了备份策略?",
                    "是否考虑了数据安全?"
                ],
                "接口设计": [
                    "是否定义了接口规范?",
                    "是否定义了认证方式?",
                    "是否定义了接口格式?",
                    "是否考虑了版本控制?",
                    "是否定义了错误处理?"
                ]
            },
            "实现完整性": {
                "开发规范": [
                    "是否定义了编码规范?",
                    "是否定义了测试要求?",
                    "是否定义了文档要求?",
                    "是否定义了版本控制?",
                    "是否定义了CI/CD流程?"
                ],
                "运维规范": [
                    "是否定义了部署流程?",
                    "是否定义了监控方案?",
                    "是否定义了告警策略?",
                    "是否定义了备份策略?",
                    "是否定义了应急预案?"
                ],
                "安全规范": [
                    "是否定义了安全策略?",
                    "是否定义了加密方案?",
                    "是否定义了审计要求?",
                    "是否定义了权限模型?",
                    "是否考虑了合规要求?"
                ]
            }
        }
    
    def call(self, params: str, **kwargs) -> str:
        """生成需求规范文档"""
        try:
            params_dict = json.loads(params)
            domain = params_dict.get('domain', '')
            discussion_summary = params_dict.get('discussion_summary', '')
            tech_decisions = params_dict.get('tech_decisions', '')
            
            # 生成需求规范
            spec = self._generate_requirement_spec(domain, discussion_summary, tech_decisions)
            
            # 进行完整性检查
            completeness_analysis = self._analyze_completeness(spec)
            
            # 合并结果
            result = {
                "需求规范": spec,
                "完整性分析": completeness_analysis
            }
            
            return json.dumps(result, ensure_ascii=False, indent=2)
            
        except Exception as e:
            return f"需求规范生成过程出错: {str(e)}"
    
    def _generate_requirement_spec(self, domain: str, discussion_summary: str, 
                                  tech_decisions: str) -> Dict[str, Any]:
        """生成完整的需求规范文档"""
        spec = {
            "需求规范文档": {
                "文档信息": {
                    "版本": "1.0",
                    "日期": "2023-04-15",
                    "状态": "初稿"
                },
                "项目概述": {
                    "项目名称": f"{domain}系统",
                    "项目背景": "基于用户需求的初步描述",
                    "项目目标": "从讨论中提取的主要目标",
                    "关键干系人": "待确定"
                },
                "功能需求": [
                    {
                        "ID": "FR-001",
                        "名称": "示例功能1",
                        "描述": "示例功能1的详细描述",
                        "优先级": "高",
                        "验收标准": "功能验收的具体标准"
                    },
                    {
                        "ID": "FR-002",
                        "名称": "示例功能2",
                        "描述": "示例功能2的详细描述",
                        "优先级": "中",
                        "验收标准": "功能验收的具体标准"
                    }
                ],
                "非功能需求": [
                    {
                        "ID": "NFR-001",
                        "类型": "性能",
                        "描述": "系统性能要求描述",
                        "衡量标准": "性能衡量的具体标准"
                    },
                    {
                        "ID": "NFR-002",
                        "类型": "安全",
                        "描述": "系统安全要求描述",
                        "衡量标准": "安全衡量的具体标准"
                    }
                ],
                "技术架构": {
                    "架构类型": "基于讨论确定的架构类型",
                    "技术栈": "基于技术决策的技术栈选择",
                    "组件图": "组件关系的文字描述",
                    "部署图": "部署结构的文字描述"
                },
                "接口定义": [
                    {
                        "ID": "API-001",
                        "名称": "示例接口1",
                        "描述": "接口功能描述",
                        "请求方法": "GET/POST/etc",
                        "请求参数": "参数描述",
                        "返回格式": "返回格式描述"
                    }
                ],
                "数据模型": [
                    {
                        "实体名称": "示例实体1",
                        "描述": "实体描述",
                        "属性": [
                            {"名称": "id", "类型": "整数", "描述": "唯一标识"},
                            {"名称": "name", "类型": "字符串", "描述": "名称"}
                        ]
                    }
                ],
                "开发计划": {
                    "阶段划分": "开发阶段的初步规划",
                    "里程碑": "主要里程碑设定",
                    "资源需求": "人力和技术资源需求"
                },
                "风险评估": [
                    {
                        "风险描述": "潜在风险描述",
                        "影响程度": "高/中/低",
                        "缓解策略": "风险缓解措施"
                    }
                ]
            }
        }
        
        return spec 

    def _analyze_completeness(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """分析需求规范的完整性"""
        analysis_result = {
            "总体完整性": 0,
            "详细分析": {},
            "缺失项": [],
            "建议": []
        }
        
        total_checks = 0
        passed_checks = 0
        
        # 遍历所有完整性检查项
        for category, subcategories in self.completeness_checks.items():
            category_result = {
                "完整性得分": 0,
                "检查项": {},
                "缺失项": []
            }
            
            category_total = 0
            category_passed = 0
            
            for subcategory, checks in subcategories.items():
                subcategory_result = {
                    "通过项": [],
                    "未通过项": []
                }
                
                for check in checks:
                    total_checks += 1
                    category_total += 1
                    
                    # 检查需求规范中是否包含相关内容
                    if self._check_requirement_content(spec, check):
                        passed_checks += 1
                        category_passed += 1
                        subcategory_result["通过项"].append(check)
                    else:
                        subcategory_result["未通过项"].append(check)
                        analysis_result["缺失项"].append(f"{subcategory}: {check}")
                
                category_result["检查项"][subcategory] = subcategory_result
            
            # 计算分类完整性得分
            category_score = (category_passed / category_total * 100) if category_total > 0 else 0
            category_result["完整性得分"] = round(category_score, 2)
            
            analysis_result["详细分析"][category] = category_result
        
        # 计算总体完整性得分
        total_score = (passed_checks / total_checks * 100) if total_checks > 0 else 0
        analysis_result["总体完整性"] = round(total_score, 2)
        
        # 生成建议
        analysis_result["建议"] = self._generate_recommendations(analysis_result["缺失项"])
        
        return analysis_result
    
    def _check_requirement_content(self, spec: Dict[str, Any], check: str) -> bool:
        """检查需求规范中是否包含特定内容"""
        # 将检查项转换为关键词
        keywords = check.lower().replace("是否", "").replace("?", "").replace("？", "").split()
        
        # 将规范转换为文本进行搜索
        spec_text = json.dumps(spec, ensure_ascii=False).lower()
        
        # 检查所有关键词是否都存在
        return all(keyword in spec_text for keyword in keywords)
    
    def _generate_recommendations(self, missing_items: List[str]) -> List[str]:
        """根据缺失项生成改进建议"""
        recommendations = []
        
        # 对缺失项进行分类
        categorized_missing = {}
        for item in missing_items:
            category, check = item.split(": ", 1)
            if category not in categorized_missing:
                categorized_missing[category] = []
            categorized_missing[category].append(check)
        
        # 生成针对性建议
        for category, checks in categorized_missing.items():
            if len(checks) > 3:
                recommendations.append(f"建议优先完善 {category} 相关内容，特别是：" + 
                                    "、".join(checks[:3]) + " 等方面")
            else:
                recommendations.append(f"需要补充 {category} 中的：" + 
                                    "、".join(checks))
        
        # 添加一般性建议
        if len(missing_items) > 10:
            recommendations.append("建议召开需求评审会议，系统性地补充完善需求文档")
        elif len(missing_items) > 5:
            recommendations.append("建议与相关方进行进一步沟通，完善关键缺失内容")
        
        return recommendations 