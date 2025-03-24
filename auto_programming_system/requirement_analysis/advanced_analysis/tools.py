"""
高级需求分析工具
实现多层次需求挖掘所需的各种工具
"""

from typing import Dict, List, Any, Optional
import json
import re


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
                    "响应式", "单页面", "多页面", "网站", "门户"
                ],
                "功能特征": [
                    "认证", "授权", "登录", "注册", "表单", "搜索",
                    "上传", "下载", "评论", "分享", "支付"
                ],
                "技术特征": [
                    "SEO", "CDN", "缓存", "会话", "Cookie", "HTTPS",
                    "API", "WebSocket", "前后端分离"
                ],
                "展示特征": [
                    "数据展示", "图表", "仪表盘", "列表", "表格",
                    "菜单", "导航", "轮播", "布局"
                ],
                "用户体验": [
                    "交互", "动画", "主题", "多语言", "国际化",
                    "本地化", "自适应", "移动优先"
                ]
            },
            "数据处理": {
                "基础特征": [
                    "数据", "分析", "处理", "统计", "报表", "图表",
                    "excel", "计算", "汇总"
                ],
                "处理类型": [
                    "数据清洗", "ETL", "转换", "过滤", "聚合",
                    "归一化", "标准化", "去重", "合并"
                ],
                "分析功能": [
                    "数据挖掘", "预测分析", "统计分析", "相关性分析",
                    "趋势分析", "异常检测", "模式识别"
                ],
                "可视化": [
                    "数据可视化", "报表生成", "图表展示", "仪表板",
                    "实时监控", "趋势图", "散点图", "热力图"
                ],
                "数据特征": [
                    "实时数据", "历史数据", "结构化数据", "非结构化数据",
                    "时序数据", "流数据", "批量数据"
                ]
            },
            "API服务": {
                "基础特征": [
                    "API", "接口", "服务", "微服务", "端点", "REST",
                    "HTTP", "RPC", "WebService"
                ],
                "服务特性": [
                    "认证", "授权", "限流", "熔断", "降级", "负载均衡",
                    "服务发现", "配置中心"
                ],
                "接口特征": [
                    "RESTful", "GraphQL", "SOAP", "gRPC", "WebSocket",
                    "异步", "实时", "批量"
                ],
                "安全特征": [
                    "加密", "签名", "令牌", "OAuth", "JWT", "HTTPS",
                    "SSL", "TLS"
                ],
                "管理特征": [
                    "监控", "日志", "追踪", "文档", "测试", "版本",
                    "部署", "网关"
                ]
            },
            "人工智能": {
                "基础特征": [
                    "AI", "机器学习", "深度学习", "神经网络", "智能",
                    "算法", "模型"
                ],
                "应用场景": [
                    "分类", "预测", "识别", "生成", "推荐", "优化",
                    "决策", "规划"
                ],
                "技术特征": [
                    "训练", "推理", "特征工程", "模型评估", "调优",
                    "验证", "部署"
                ],
                "数据特征": [
                    "标注数据", "训练集", "测试集", "验证集", "样本",
                    "特征", "标签"
                ],
                "领域特征": [
                    "计算机视觉", "自然语言处理", "语音识别", "推荐系统",
                    "强化学习", "知识图谱"
                ]
            },
            "移动应用": {
                "基础特征": [
                    "APP", "移动", "iOS", "Android", "手机", "平板",
                    "客户端"
                ],
                "功能特征": [
                    "离线存储", "推送通知", "定位服务", "传感器",
                    "相机", "扫码", "分享"
                ],
                "用户体验": [
                    "手势", "动画", "主题", "暗黑模式", "自适应",
                    "响应式", "原生体验"
                ],
                "技术特征": [
                    "混合开发", "原生开发", "跨平台", "热更新",
                    "性能优化", "安全加密"
                ],
                "集成特征": [
                    "社交集成", "支付集成", "地图集成", "云服务",
                    "第三方登录", "分享"
                ]
            }
        }
        
        # 定义通用应用特征
        self.general_features = {
            "性能需求": [
                "高性能", "低延迟", "高并发", "实时", "响应时间",
                "吞吐量", "负载", "性能指标"
            ],
            "安全需求": [
                "安全", "加密", "认证", "授权", "审计", "防攻击",
                "数据安全", "访问控制"
            ],
            "可靠性": [
                "高可用", "容错", "备份", "恢复", "监控", "告警",
                "日志", "追踪"
            ],
            "扩展性": [
                "可扩展", "模块化", "插件", "微服务", "分布式",
                "集群", "水平扩展", "垂直扩展"
            ],
            "维护性": [
                "易维护", "文档", "测试", "部署", "版本控制",
                "持续集成", "持续部署"
            ]
        }
    
    def call(self, params: str, **kwargs) -> str:
        """执行领域分类"""
        try:
            params_dict = json.loads(params)
            requirement_text = params_dict.get('requirement_text', '')
            
            domains = self._classify_domain(requirement_text)
            
            return json.dumps({
                'primary_domain': domains[0],
                'secondary_domains': domains[1:],
                'key_features': self._extract_key_features(requirement_text, domains[0])
            }, ensure_ascii=False)
            
        except Exception as e:
            return f"领域分类过程出错: {str(e)}"
    
    def _classify_domain(self, text: str) -> List[str]:
        """分析文本并返回领域分类结果"""
        domains = []
        
        keywords = {
            "web应用": ["网站", "前端", "后端", "页面", "UI", "网页", "浏览器"],
            "数据处理": ["数据", "分析", "处理", "统计", "报表", "图表", "excel"],
            "API服务": ["API", "接口", "服务", "微服务", "端点", "REST", "HTTP"],
            "移动应用": ["APP", "移动", "iOS", "Android", "手机", "平板"],
            "人工智能": ["AI", "机器学习", "深度学习", "模型", "训练", "预测", "智能"],
            "数据库": ["数据库", "存储", "SQL", "NoSQL", "表", "查询"],
            "爬虫": ["爬虫", "抓取", "采集", "提取", "网页数据"]
        }
        
        text_lower = text.lower()
        for domain, words in keywords.items():
            for word in words:
                if word.lower() in text_lower:
                    if domain not in domains:
                        domains.append(domain)
        
        # 如果没有匹配到任何领域，返回通用应用
        if not domains:
            domains = ["通用应用"]
            
        return domains
    
    def _extract_key_features(self, text: str, domain: str) -> List[str]:
        """根据领域提取需求中的关键特征
        
        Args:
            text: 需求文本
            domain: 识别出的主要领域
            
        Returns:
            提取出的关键特征列表
        """
        features = []
        text_lower = text.lower()
        
        # 1. 提取领域特定特征
        if domain in self.feature_patterns:
            domain_patterns = self.feature_patterns[domain]
            for category, patterns in domain_patterns.items():
                for pattern in patterns:
                    if pattern.lower() in text_lower:
                        features.append(f"{category}:{pattern}")
        
        # 2. 提取通用特征
        for category, patterns in self.general_features.items():
            for pattern in patterns:
                if pattern.lower() in text_lower:
                    features.append(f"通用-{category}:{pattern}")
        
        # 3. 提取数字相关的特征（如版本号、数量级等）
        number_patterns = {
            r"(\d+\.?\d*)\s*(ms|毫秒)": "响应时间要求",
            r"(\d+\.?\d*)\s*(分钟|小时)": "时间要求",
            r"(\d+\.?\d*)\s*(MB|GB|TB)": "数据量要求",
            r"(\d+\.?\d*)\s*(用户|并发)": "用户量要求",
            r"(\d+\.?\d*)%": "百分比指标",
            r"版本\s*(\d+\.?\d*\.?\d*)": "版本要求"
        }
        
        for pattern, feature_name in number_patterns.items():
            matches = re.findall(pattern, text_lower)
            if matches:
                for match in matches:
                    value = match[0] if isinstance(match, tuple) else match
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
        'name': 'domain',
        'type': 'string',
        'description': '需求所属的主要领域',
        'required': True
    }, {
        'name': 'current_understanding',
        'type': 'string',
        'description': '当前对需求的理解摘要',
        'required': True
    }, {
        'name': 'discussion_history',
        'type': 'string',
        'description': '已讨论过的问题和答案',
        'required': True
    }]
    
    def __init__(self):
        """初始化问题生成器"""
        # 定义领域特定的问题模板
        self.domain_questions = {
            "web应用": {
                "需求概述": [
                    "网站需要支持哪些主要功能模块？",
                    "是否需要用户认证和权限管理？",
                    "是否需要支持多语言？",
                    "有特殊的浏览器兼容性要求吗？",
                    "网站的目标用户群体是谁？"
                ],
                "功能详述": [
                    "每个功能模块的具体操作流程是什么？",
                    "需要哪些数据表单和展示页面？",
                    "是否需要实时数据更新？",
                    "是否需要集成第三方服务？",
                    "用户权限需要划分为哪些层级？"
                ],
                "技术约束": [
                    "前端框架是否有特定要求？",
                    "后端技术栈是否有限制？",
                    "数据库选型有什么偏好？",
                    "是否需要支持移动端访问？",
                    "对响应时间有什么要求？"
                ],
                "架构设计": [
                    "预计的并发用户数是多少？",
                    "数据库的数据量预估？",
                    "是否需要考虑分布式部署？",
                    "是否需要CDN加速？",
                    "是否需要负载均衡？"
                ],
                "实现细节": [
                    "页面布局的风格要求？",
                    "是否需要响应式设计？",
                    "表单验证的规则？",
                    "数据缓存策略？",
                    "错误处理和日志记录要求？"
                ]
            },
            "数据处理": {
                "需求概述": [
                    "数据的主要来源是什么？",
                    "数据处理的频率和时效性要求是什么？",
                    "需要哪些类型的数据分析？",
                    "数据量级和增长趋势如何？",
                    "最终数据的使用场景是什么？"
                ],
                "功能详述": [
                    "需要哪些数据清洗规则？",
                    "需要生成哪些类型的报表？",
                    "是否需要数据可视化？",
                    "数据存储的时间跨度是多少？",
                    "是否需要历史数据追溯？"
                ],
                "技术约束": [
                    "对数据处理性能有什么要求？",
                    "是否需要支持实时处理？",
                    "数据安全性要求是什么？",
                    "是否需要分布式处理？",
                    "数据备份策略要求？"
                ],
                "架构设计": [
                    "是否需要流处理架构？",
                    "数据存储选型偏好？",
                    "计算资源需求评估？",
                    "是否需要任务调度系统？",
                    "监控告警要求？"
                ],
                "实现细节": [
                    "数据清洗的具体规则？",
                    "数据质量的验证标准？",
                    "异常数据的处理策略？",
                    "数据导入导出格式？",
                    "报表更新频率？"
                ]
            },
            "API服务": {
                "需求概述": [
                    "API服务的主要用途是什么？",
                    "预期的调用方有哪些？",
                    "是否需要支持跨平台访问？",
                    "对接口安全性有什么要求？",
                    "服务可用性要求是什么？"
                ],
                "功能详述": [
                    "需要提供哪些具体接口？",
                    "每个接口的输入输出定义？",
                    "是否需要版本控制？",
                    "是否需要接口文档？",
                    "错误处理策略是什么？"
                ],
                "技术约束": [
                    "接口协议选择(REST/GraphQL/gRPC)？",
                    "认证方式要求？",
                    "并发处理能力要求？",
                    "响应时间要求？",
                    "是否需要支持异步调用？"
                ],
                "架构设计": [
                    "是否采用微服务架构？",
                    "服务发现机制选择？",
                    "负载均衡策略？",
                    "限流降级方案？",
                    "监控方案选择？"
                ],
                "实现细节": [
                    "接口参数验证规则？",
                    "缓存策略设计？",
                    "日志记录要求？",
                    "测试覆盖率要求？",
                    "部署环境要求？"
                ]
            }
        }
        
        # 定义通用问题
        self.general_questions = {
            "需求概述": [
                "这个系统的主要目标是什么？",
                "目标用户群体是谁？",
                "系统需要解决什么核心问题？",
                "有哪些现有系统可以参考？",
                "项目的时间节点要求是什么？"
            ],
            "功能详述": [
                "系统需要哪些核心功能？",
                "功能的优先级排序是什么？",
                "是否有可选的扩展功能？",
                "用户操作流程是什么？",
                "需要什么样的用户界面？"
            ],
            "技术约束": [
                "是否有特定的技术栈要求？",
                "性能要求是什么？",
                "安全性要求是什么？",
                "可用性要求是什么？",
                "可维护性要求是什么？"
            ],
            "架构设计": [
                "系统的使用规模是多大？",
                "是否需要考虑扩展性？",
                "是否有特殊的部署要求？",
                "是否需要与其他系统集成？",
                "数据备份恢复要求是什么？"
            ],
            "实现细节": [
                "开发规范要求是什么？",
                "测试要求是什么？",
                "文档要求是什么？",
                "部署环境是什么？",
                "运维要求是什么？"
            ]
        }
    
    def call(self, params: str, **kwargs) -> str:
        """生成推进需求理解的问题"""
        try:
            params_dict = json.loads(params)
            domain = params_dict.get('domain', '')
            current_understanding = params_dict.get('current_understanding', '')
            discussion_history = params_dict.get('discussion_history', '')
            
            # 获取当前对话阶段
            stage = self._determine_discussion_stage(discussion_history)
            
            # 生成下一步问题
            next_questions = self._generate_questions_for_stage(
                domain, current_understanding, stage, discussion_history
            )
            
            return json.dumps({
                'current_stage': stage,
                'next_questions': next_questions,
                'explanation': self._get_stage_explanation(stage)
            }, ensure_ascii=False)
            
        except Exception as e:
            return f"问题生成过程出错: {str(e)}"
    
    def _determine_discussion_stage(self, discussion_history: str) -> str:
        """根据讨论历史确定当前处于哪个阶段"""
        stages = ["需求概述", "功能详述", "技术约束", "架构设计", "实现细节"]
        
        try:
            history = json.loads(discussion_history)
            # 计算讨论轮数
            rounds = len([msg for msg in history if msg.get("role") == "user"])
            
            # 根据讨论轮数和内容特征判断阶段
            if rounds < 2:
                return stages[0]
            elif rounds < 5:
                return stages[1]
            elif rounds < 8:
                return stages[2]
            elif rounds < 12:
                return stages[3]
            else:
                return stages[4]
        except:
            # 如果解析失败，使用简单的字符串匹配
            rounds = discussion_history.count("问题:")
            if rounds < 2:
                return stages[0]
            elif rounds < 5:
                return stages[1]
            elif rounds < 8:
                return stages[2]
            elif rounds < 12:
                return stages[3]
            else:
                return stages[4]
    
    def _generate_questions_for_stage(
        self, domain: str, current_understanding: str,
        stage: str, discussion_history: str
    ) -> List[str]:
        """根据当前阶段生成适当的问题"""
        # 获取已经问过的问题
        asked_questions = self._extract_asked_questions(discussion_history)
        
        # 获取领域特定问题
        domain_specific_questions = self.domain_questions.get(domain, {}).get(stage, [])
        
        # 获取通用问题
        general_questions = self.general_questions.get(stage, [])
        
        # 合并问题并去除已问过的
        all_questions = domain_specific_questions + general_questions
        new_questions = [q for q in all_questions if q not in asked_questions]
        
        # 如果没有新问题，使用下一阶段的问题
        if not new_questions:
            stages = ["需求概述", "功能详述", "技术约束", "架构设计", "实现细节"]
            current_index = stages.index(stage)
            if current_index < len(stages) - 1:
                next_stage = stages[current_index + 1]
                domain_specific_questions = self.domain_questions.get(domain, {}).get(next_stage, [])
                general_questions = self.general_questions.get(next_stage, [])
                new_questions = domain_specific_questions + general_questions
        
        # 返回前5个问题
        return new_questions[:5]
    
    def _extract_asked_questions(self, discussion_history: str) -> List[str]:
        """从讨论历史中提取已经问过的问题"""
        asked_questions = []
        try:
            history = json.loads(discussion_history)
            for msg in history:
                if msg.get("role") == "assistant":
                    content = msg.get("content", "")
                    # 提取问题（假设问题以问号结尾）
                    questions = [
                        q.strip() for q in content.split("\n")
                        if "?" in q or "？" in q
                    ]
                    asked_questions.extend(questions)
        except:
            # 如果解析失败，使用简单的文本匹配
            questions = [
                q.strip() for q in discussion_history.split("\n")
                if "?" in q or "？" in q
            ]
            asked_questions.extend(questions)
        
        return asked_questions
    
    def _get_stage_explanation(self, stage: str) -> str:
        """获取当前阶段的说明"""
        explanations = {
            "需求概述": "我们正处于需求理解的初始阶段，需要了解系统的基本目标和用户场景。",
            "功能详述": "现在我们需要深入了解系统的具体功能和优先级，确保不遗漏关键需求。",
            "技术约束": "在这个阶段，我们需要明确系统的技术约束和性能要求，为架构设计奠定基础。",
            "架构设计": "基于已了解的功能和约束，我们需要确定合适的技术架构和框架选择。",
            "实现细节": "最后，我们需要细化实现细节，确保系统的各个组件能够顺利开发和集成。"
        }
        
        return explanations.get(stage, "让我们继续深入了解您的需求。")


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