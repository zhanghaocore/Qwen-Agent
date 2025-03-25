from typing import Any, Dict, List, Optional, Tuple, Set
from datetime import datetime
from .base_agent import BaseAgent
import re

class TechnicalDecisionAgent(BaseAgent):
    """渐进式技术决策代理，负责技术选型和决策的渐进式处理。
    
    该类实现了渐进式的技术决策流程，包括：
    1. 决策点识别：从需求中识别需要做出技术决策的点
    2. 选项生成：为每个决策点生成可行的技术选项
    3. 选项评估：根据需求和约束评估各个选项
    4. 决策记录：记录决策过程和结果
    5. 依赖分析：分析决策点之间的依赖关系
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """初始化渐进式技术决策代理。
        
        Args:
            config: 代理配置信息，包含决策相关的配置参数
        """
        super().__init__(config)
        self.decision_history: List[Dict[str, Any]] = []
        self.current_decision_point: Optional[Dict[str, Any]] = None
        self.decision_context: Dict[str, Any] = {}
        
        # 确保配置不为空
        if not hasattr(self, 'config') or self.config is None:
            self.config = {
                "decision_making": {
                    "max_alternatives": 5,
                    "min_confidence": 0.5,
                    "feature_weights": {
                        "keyword": 2,
                        "pattern": 3,
                        "context": 1
                    }
                }
            }
        
    async def update_context(self, new_context: Dict[str, Any]) -> Dict[str, Any]:
        """更新代理上下文。
        
        Args:
            new_context: 新的上下文信息
            
        Returns:
            更新后的完整上下文信息
        """
        self.decision_context.update(new_context)
        return self.decision_context
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理需求并做出渐进式技术决策。
        
        Args:
            input_data: 包含需求和约束的输入数据，格式为：
                {
                    "requirements": List[str],  # 需求列表
                    "constraints": List[str]    # 约束条件列表
                }
            
        Returns:
            技术决策结果，包含：
            - current_decision: 当前决策记录
            - decision_history: 决策历史
            - context: 决策上下文
            - next_steps: 下一步决策点列表
        """
        # 1. 分析需求
        requirements = input_data.get("requirements", [])
        constraints = input_data.get("constraints", [])
        
        # 2. 识别决策点
        decision_points = await self._identify_decision_points(requirements, constraints)
        
        # 3. 选择当前决策点
        self.current_decision_point = await self._select_current_decision_point(decision_points)
        
        # 4. 生成选项
        alternatives = await self._generate_alternatives(self.current_decision_point)
        
        # 5. 评估选项
        evaluation = await self._evaluate_alternatives(alternatives, requirements, constraints)
        
        # 6. 记录决策
        decision_record = await self._record_decision(evaluation)
        
        # 7. 更新上下文
        self.decision_history.append(decision_record)
        self.decision_context.update(self._extract_context(decision_record))
        
        return {
            "current_decision": decision_record,
            "decision_history": self.decision_history,
            "context": self.decision_context,
            "next_steps": await self._determine_next_steps(decision_points)
        }
    
    async def _identify_decision_points(self, requirements: List[str], constraints: List[str]) -> List[Dict[str, Any]]:
        """识别需要做出技术决策的点。
        
        Args:
            requirements: 需求列表
            constraints: 约束条件列表
            
        Returns:
            决策点列表，每个决策点包含：
            - type: 决策点类型
            - content: 决策点内容
            - confidence: 置信度
            - dependencies: 依赖关系
            - constraints: 相关约束
        """
        decision_points = []
        
        # 获取决策配置
        decision_config = self.config.get("decision_making", {})
        max_alternatives = decision_config.get("max_alternatives", 5)
        min_confidence = decision_config.get("min_confidence", 0.3)  # 进一步降低最小置信度阈值
        
        # 定义决策点类型和特征
        decision_features = {
            "data_processing": {
                "keywords": ["处理", "分析", "转换", "清洗", "过滤", "聚合", "计算", "统计", "CSV", "文件"],
                "patterns": [
                    r"数据.*处理",
                    r"数据.*分析",
                    r"数据.*转换",
                    r"数据.*清洗",
                    r"数据.*过滤",
                    r"数据.*聚合",
                    r"计算.*平均值",
                    r"统计.*数据",
                    r"CSV.*文件",
                    r"文件.*处理"
                ],
                "context_words": ["数据", "信息", "记录", "日志", "指标", "CSV", "表格", "文件", "计算", "统计"]
            },
            "storage": {
                "keywords": ["存储", "保存", "数据库", "缓存", "持久化", "写入", "记录", "DB"],
                "patterns": [
                    r"数据.*存储",
                    r"数据.*保存",
                    r"使用.*数据库",
                    r"数据.*缓存",
                    r"数据.*持久化",
                    r"保存.*数据",
                    r"写入.*数据",
                    r"数据库.*保存"
                ],
                "context_words": ["数据", "文件", "记录", "配置", "状态", "数据库", "存储", "DB", "持久化"]
            },
            "performance": {
                "keywords": ["性能", "速度", "效率", "优化", "并发", "响应", "提升", "改进", "快速"],
                "patterns": [
                    r"性能.*优化",
                    r"提高.*速度",
                    r"提升.*效率",
                    r"并发.*处理",
                    r"响应.*时间",
                    r"优化.*性能",
                    r"改进.*效率",
                    r"优化.*处理"
                ],
                "context_words": ["性能", "速度", "效率", "时间", "资源", "优化", "提升", "快速", "改进"]
            }
        }
        
        # 分析需求中的技术决策点
        for req in requirements:
            req_lower = req.lower()
            for decision_type, features in decision_features.items():
                # 计算特征匹配分数
                feature_score = 0
                total_features = 0
                
                # 关键词匹配（增加权重）
                keyword_matches = sum(1 for keyword in features["keywords"] if keyword in req_lower)
                feature_score += keyword_matches * 3  # 增加关键词权重
                total_features += len(features["keywords"]) * 3
                
                # 模式匹配（增加权重）
                pattern_matches = sum(1 for pattern in features["patterns"] if re.search(pattern, req_lower))
                feature_score += pattern_matches * 4  # 增加模式匹配权重
                total_features += len(features["patterns"]) * 4
                
                # 上下文匹配（增加权重）
                context_matches = sum(1 for word in features["context_words"] if word in req_lower)
                feature_score += context_matches * 2  # 增加上下文匹配权重
                total_features += len(features["context_words"]) * 2
                
                # 计算置信度
                if total_features > 0:
                    confidence = feature_score / total_features
                    # 添加额外的置信度提升
                    if pattern_matches > 0:  # 如果有模式匹配，增加置信度
                        confidence += 0.1
                    if keyword_matches >= 2:  # 如果有多个关键词匹配，增加置信度
                        confidence += 0.1
                    if context_matches >= 3:  # 如果有多个上下文词匹配，增加置信度
                        confidence += 0.1
                    
                    # 确保置信度不超过1.0
                    confidence = min(confidence, 1.0)
                    
                    if confidence >= min_confidence:
                        decision_point = {
                            "type": decision_type,
                            "content": req,
                            "confidence": confidence,
                            "dependencies": [],
                            "constraints": self._extract_constraints(req, constraints),
                            "features": {
                                "keyword_matches": keyword_matches,
                                "pattern_matches": pattern_matches,
                                "context_matches": context_matches
                            }
                        }
                        decision_points.append(decision_point)
        
        # 分析决策点之间的依赖关系
        decision_points = await self._analyze_dependencies(decision_points)
        
        # 按置信度和依赖关系排序
        decision_points.sort(key=lambda x: (x["confidence"], -len(x["dependencies"])), reverse=True)
        return decision_points[:max_alternatives]
    
    async def _select_current_decision_point(self, decision_points: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """选择当前需要处理的决策点。
        
        Args:
            decision_points: 决策点列表
            
        Returns:
            当前决策点，如果没有可用的决策点则返回 None
        """
        if not decision_points:
            return None
            
        # 选择置信度最高且依赖已满足的决策点
        for point in decision_points:
            if self._are_dependencies_satisfied(point):
                return point
                
        # 如果没有完全满足依赖的决策点，选择置信度最高的
        return decision_points[0]
    
    async def _generate_alternatives(self, decision_point: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """为决策点生成技术选项。
        
        Args:
            decision_point: 决策点信息，如果为 None 则返回空列表
            
        Returns:
            技术选项列表，每个选项包含：
            - decision_point: 关联的决策点
            - option: 选项名称
            - description: 选项描述
            - pros: 优点列表
            - cons: 缺点列表
            - implementation_complexity: 实现复杂度
        """
        if not decision_point:
            return []
            
        # 定义技术选项配置
        alternatives_config = {
            "data_processing": [
                {
                    "option": "pandas",
                    "description": "使用pandas库进行数据处理",
                    "pros": ["功能强大", "性能好", "社区活跃"],
                    "cons": ["依赖较多", "学习曲线较陡"],
                    "implementation_complexity": "medium"
                },
                {
                    "option": "numpy",
                    "description": "使用numpy库进行数据处理",
                    "pros": ["性能极好", "内存效率高"],
                    "cons": ["功能相对简单", "需要自己实现一些功能"],
                    "implementation_complexity": "low"
                }
            ],
            "storage": [
                {
                    "option": "sqlite",
                    "description": "使用SQLite数据库存储数据",
                    "pros": ["轻量级", "无需安装", "适合小型应用"],
                    "cons": ["并发性能有限", "不适合大规模数据"],
                    "implementation_complexity": "low"
                },
                {
                    "option": "json",
                    "description": "使用JSON文件存储数据",
                    "pros": ["简单", "可读性好", "无需额外依赖"],
                    "cons": ["不适合频繁读写", "不支持复杂查询"],
                    "implementation_complexity": "very_low"
                }
            ],
            "performance": [
                {
                    "option": "multiprocessing",
                    "description": "使用多进程提高性能",
                    "pros": ["充分利用多核CPU", "适合CPU密集型任务"],
                    "cons": ["内存开销大", "进程间通信复杂"],
                    "implementation_complexity": "high"
                },
                {
                    "option": "asyncio",
                    "description": "使用异步IO提高性能",
                    "pros": ["适合IO密集型任务", "资源消耗小"],
                    "cons": ["代码复杂度增加", "需要重构同步代码"],
                    "implementation_complexity": "medium"
                }
            ]
        }
        
        # 根据决策点类型生成选项
        alternatives = []
        if decision_point["type"] in alternatives_config:
            for alt_config in alternatives_config[decision_point["type"]]:
                alternative = alt_config.copy()
                alternative["decision_point"] = decision_point
                alternatives.append(alternative)
        
        return alternatives
    
    async def _evaluate_alternatives(self, alternatives: List[Dict[str, Any]], 
                                  requirements: List[str], 
                                  constraints: List[str]) -> Dict[str, Any]:
        """评估技术选项。
        
        Args:
            alternatives: 技术选项列表
            requirements: 需求列表
            constraints: 约束条件列表
            
        Returns:
            评估结果，包含：
            - best_option: 最佳选项
            - all_options: 所有选项的评估结果
            - context: 评估上下文
        """
        if not alternatives:
            return {}
            
        evaluations = []
        for alt in alternatives:
            # 计算选项的得分
            score = self._calculate_option_score(alt, requirements, constraints)
            
            # 生成评估结果
            evaluation = {
                "option": alt["option"],
                "description": alt["description"],
                "pros": alt["pros"],
                "cons": alt["cons"],
                "score": score,
                "implementation_complexity": alt["implementation_complexity"],
                "reasoning": self._generate_decision_reasoning(alt, score)
            }
            evaluations.append(evaluation)
        
        # 按得分排序
        evaluations.sort(key=lambda x: x["score"], reverse=True)
        
        return {
            "best_option": evaluations[0],
            "all_options": evaluations,
            "context": self.decision_context
        }
    
    async def _record_decision(self, evaluation: Dict[str, Any]) -> Dict[str, Any]:
        """记录决策结果。
        
        Args:
            evaluation: 评估结果
            
        Returns:
            决策记录，包含：
            - timestamp: 决策时间戳
            - decision_point: 决策点信息
            - selected_option: 选中的选项
            - context: 决策上下文
            - reasoning: 决策理由
        """
        if not evaluation or not evaluation.get("best_option"):
            return {}
            
        decision_record = {
            "timestamp": self._get_current_timestamp(),
            "decision_point": self.current_decision_point,
            "selected_option": evaluation["best_option"],
            "context": self.decision_context,
            "reasoning": evaluation["best_option"]["reasoning"]
        }
        
        return decision_record
    
    async def _determine_next_steps(self, decision_points: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """确定下一步决策点。
        
        Args:
            decision_points: 决策点列表
            
        Returns:
            下一步决策点列表，按依赖关系和置信度排序
        """
        # 过滤掉已处理的决策点
        remaining_points = [p for p in decision_points if p != self.current_decision_point]
        
        # 按依赖关系和置信度排序
        remaining_points.sort(key=lambda x: (x["confidence"], -len(x["dependencies"])), reverse=True)
        
        # 选择下一个要处理的决策点
        return [point for point in remaining_points if self._are_dependencies_satisfied(point)]
    
    def _are_dependencies_satisfied(self, decision_point: Dict[str, Any]) -> bool:
        """检查决策点的依赖是否已满足。
        
        Args:
            decision_point: 决策点信息
            
        Returns:
            依赖是否满足
        """
        if not decision_point.get("dependencies"):
            return True
            
        return all(
            any(d["decision_point"]["type"] == dep for d in self.decision_history)
            for dep in decision_point["dependencies"]
        )
    
    def _extract_constraints(self, requirement: str, constraints: List[str]) -> List[str]:
        """从约束列表中提取与需求相关的约束。
        
        Args:
            requirement: 需求描述
            constraints: 约束条件列表
            
        Returns:
            与需求相关的约束列表
        """
        relevant_constraints = []
        requirement_lower = requirement.lower()
        
        # 定义约束类型和关键词
        constraint_keywords = {
            "performance": ["性能", "速度", "效率", "时间", "资源"],
            "memory": ["内存", "存储", "空间"],
            "dependency": ["依赖", "库", "包", "模块"],
            "compatibility": ["兼容", "支持", "版本"]
        }
        
        # 遍历每个约束
        for constraint in constraints:
            constraint_lower = constraint.lower()
            
            # 检查约束是否与需求相关
            is_relevant = False
            
            # 1. 直接关键词匹配
            for keywords in constraint_keywords.values():
                if any(keyword in requirement_lower and keyword in constraint_lower for keyword in keywords):
                    is_relevant = True
                    break
            
            # 2. 上下文相关性检查
            if not is_relevant:
                if "性能" in requirement_lower and any(word in constraint_lower for word in ["时间", "速度", "效率"]):
                    is_relevant = True
                elif "数据" in requirement_lower and any(word in constraint_lower for word in ["存储", "内存", "空间"]):
                    is_relevant = True
                elif "处理" in requirement_lower and any(word in constraint_lower for word in ["库", "依赖", "模块"]):
                    is_relevant = True
            
            # 3. 通用约束总是相关
            if any(word in constraint_lower for word in ["使用", "必须", "不能", "应该"]):
                is_relevant = True
            
            if is_relevant:
                relevant_constraints.append(constraint)
        
        return relevant_constraints
    
    def _calculate_option_score(self, option: Dict[str, Any], 
                              requirements: List[str], 
                              constraints: List[str]) -> float:
        """计算技术选项的得分。
        
        Args:
            option: 技术选项
            requirements: 需求列表
            constraints: 约束条件列表
            
        Returns:
            选项得分，范围在0-1之间
        """
        # 定义复杂度得分映射
        complexity_scores = {
            "very_low": 0.2,
            "low": 0.15,
            "medium": 0.1,
            "high": 0.05
        }
        
        # 计算基础分数
        score = 0.3  # 基础分
        
        # 实现复杂度评分
        complexity = option.get("implementation_complexity", "medium")
        score += complexity_scores.get(complexity, 0.1)
        
        # 优点评分
        pros = option.get("pros", [])
        score += min(len(pros) * 0.1, 0.4)  # 最多加0.4分
        
        # 缺点评分
        cons = option.get("cons", [])
        score -= min(len(cons) * 0.05, 0.3)  # 最多减0.3分
        
        # 约束满足度评分
        constraint_score = 0
        for constraint in constraints:
            if any(keyword in option["description"].lower() for keyword in constraint.lower().split()):
                constraint_score += 0.1
        score += min(constraint_score, 0.2)  # 最多加0.2分
        
        # 技术栈兼容性评分
        if "dependencies" in option:
            compatibility_score = 1 - (len(option["dependencies"]) * 0.1)
            score += max(compatibility_score, 0) * 0.2  # 最多加0.2分
        
        # 集成成本评分
        if "integration_cost" in option:
            cost_score = 1 - option["integration_cost"]
            score += cost_score * 0.1  # 最多加0.1分
        
        # 确保分数在0-1之间
        return max(0.0, min(1.0, score))
    
    def _generate_decision_reasoning(self, option: Dict[str, Any], score: float) -> str:
        """生成决策理由。
        
        Args:
            option: 技术选项
            score: 选项得分
            
        Returns:
            决策理由文本
        """
        reasoning = f"选择 {option['option']} 作为解决方案，"
        reasoning += f"实现复杂度为 {option['implementation_complexity']}，"
        reasoning += f"得分 {score:.2f}。"
        reasoning += f"主要优点：{', '.join(option['pros'])}。"
        reasoning += f"主要缺点：{', '.join(option['cons'])}。"
        return reasoning
    
    def _extract_context(self, decision_record: Dict[str, Any]) -> Dict[str, Any]:
        """从决策记录中提取上下文信息。
        
        Args:
            decision_record: 决策记录
            
        Returns:
            上下文信息，包含决策类型和选中的选项
        """
        context = {}
        if decision_record and "selected_option" in decision_record:
            option = decision_record["selected_option"]
            if isinstance(option, dict) and "decision_point" in option and "type" in option["decision_point"]:
                context[option["decision_point"]["type"]] = option["option"]
        return context
    
    def _get_current_timestamp(self) -> str:
        """获取当前时间戳。
        
        Returns:
            ISO格式的时间戳字符串
        """
        return datetime.now().isoformat()
    
    async def _analyze_dependencies(self, decision_points: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """分析决策点之间的依赖关系。
        
        Args:
            decision_points: 决策点列表
            
        Returns:
            添加了依赖关系的决策点列表
        """
        # 定义依赖规则
        dependency_rules = {
            "data_processing": {
                "depends_on": [],
                "required_by": ["storage", "performance"]
            },
            "storage": {
                "depends_on": ["data_processing"],
                "required_by": ["performance"]
            },
            "performance": {
                "depends_on": ["data_processing", "storage"],
                "required_by": []
            }
        }
        
        # 为每个决策点分析依赖
        for i, point in enumerate(decision_points):
            point_type = point["type"]
            if point_type in dependency_rules:
                # 添加依赖
                for dep_type in dependency_rules[point_type]["depends_on"]:
                    for j, other_point in enumerate(decision_points):
                        if other_point["type"] == dep_type and j != i:
                            if j not in point["dependencies"]:
                                point["dependencies"].append(j)
                
                # 添加被依赖
                for req_type in dependency_rules[point_type]["required_by"]:
                    for j, other_point in enumerate(decision_points):
                        if other_point["type"] == req_type and j != i:
                            if i not in other_point["dependencies"]:
                                other_point["dependencies"].append(i)
        
        return decision_points 