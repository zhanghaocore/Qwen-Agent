from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
from .base_agent import BaseAgent

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
        min_confidence = decision_config.get("min_confidence", 0.7)
        
        # 定义决策点类型和关键词映射
        decision_types = {
            "data_processing": ["处理", "分析", "转换"],
            "storage": ["存储", "保存", "数据库"],
            "performance": ["性能", "速度", "效率"]
        }
        
        # 分析需求中的技术决策点
        for req in requirements:
            for decision_type, keywords in decision_types.items():
                if any(keyword in req.lower() for keyword in keywords):
                    decision_point = {
                        "type": decision_type,
                        "content": req,
                        "confidence": 0.9 - (0.05 * list(decision_types.keys()).index(decision_type)),
                        "dependencies": [],
                        "constraints": self._extract_constraints(req, constraints)
                    }
                    decision_points.append(decision_point)
                    break
        
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
        """从需求和约束中提取相关约束。
        
        Args:
            requirement: 需求文本
            constraints: 约束条件列表
            
        Returns:
            相关约束列表
        """
        requirement_keywords = requirement.lower().split()
        return [
            constraint for constraint in constraints
            if any(keyword in constraint.lower() for keyword in requirement_keywords)
        ]
    
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
        score += complexity_scores.get(option["implementation_complexity"], 0.1)
        score += len(option["pros"]) * 0.1
        score -= len(option["cons"]) * 0.05
        
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
            包含依赖关系的决策点列表
        """
        # 定义依赖关系规则
        dependency_rules = {
            "storage": ["data_processing"],
            "performance": ["data_processing", "storage"]
        }
        
        for point in decision_points:
            dependencies = []
            if point["type"] in dependency_rules:
                for other_point in decision_points:
                    if other_point["type"] in dependency_rules[point["type"]]:
                        dependencies.append(other_point["type"])
            point["dependencies"] = dependencies
            
        return decision_points 