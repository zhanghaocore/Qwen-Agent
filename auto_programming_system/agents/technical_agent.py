from typing import Any, Dict, List, Optional
from .base_agent import BaseAgent

class TechnicalAgent(BaseAgent):
    """技术决策代理，负责技术选型和决策"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化技术决策代理
        
        Args:
            config: 代理配置信息
        """
        super().__init__(config)
        self.decisions = []
        self.alternatives = []
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理需求并做出技术决策
        
        Args:
            input_data: 包含需求和约束的输入数据
            
        Returns:
            技术决策结果
        """
        # 1. 分析需求
        requirements = input_data.get("requirements", [])
        constraints = input_data.get("constraints", [])
        
        # 2. 识别决策点
        decision_points = await self._identify_decision_points(requirements, constraints)
        
        # 3. 生成选项
        alternatives = await self._generate_alternatives(decision_points)
        
        # 4. 评估选项
        decisions = await self._evaluate_alternatives(alternatives, requirements, constraints)
        
        # 5. 更新上下文
        self.decisions = decisions
        self.alternatives = alternatives
        
        return {
            "decisions": decisions,
            "alternatives": alternatives,
            "context": self.get_context()
        }
    
    async def update_context(self, new_context: Dict[str, Any]) -> None:
        """
        更新代理上下文
        
        Args:
            new_context: 新的上下文信息
        """
        self.context.update(new_context)
        
    async def _identify_decision_points(self, requirements: List[str], constraints: List[str]) -> List[Dict[str, Any]]:
        """
        识别需要做出技术决策的点
        
        Args:
            requirements: 需求列表
            constraints: 约束条件列表
            
        Returns:
            决策点列表
        """
        decision_points = []
        
        # 获取决策配置
        decision_config = self.config.get("decision_making", {})
        max_alternatives = decision_config.get("max_alternatives", 5)
        min_confidence = decision_config.get("min_confidence", 0.7)
        
        # 分析需求中的技术决策点
        for req in requirements:
            # 识别数据处理相关的决策点
            if any(keyword in req.lower() for keyword in ["处理", "分析", "转换"]):
                decision_point = {
                    "type": "data_processing",
                    "content": req,
                    "confidence": 0.9,
                    "constraints": self._extract_constraints(req, constraints)
                }
                decision_points.append(decision_point)
            
            # 识别存储相关的决策点
            elif any(keyword in req.lower() for keyword in ["存储", "保存", "数据库"]):
                decision_point = {
                    "type": "storage",
                    "content": req,
                    "confidence": 0.85,
                    "constraints": self._extract_constraints(req, constraints)
                }
                decision_points.append(decision_point)
            
            # 识别性能相关的决策点
            elif any(keyword in req.lower() for keyword in ["性能", "速度", "效率"]):
                decision_point = {
                    "type": "performance",
                    "content": req,
                    "confidence": 0.8,
                    "constraints": self._extract_constraints(req, constraints)
                }
                decision_points.append(decision_point)
        
        # 按置信度排序并限制数量
        decision_points.sort(key=lambda x: x["confidence"], reverse=True)
        return decision_points[:max_alternatives]
    
    async def _generate_alternatives(self, decision_points: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        为每个决策点生成技术选项
        
        Args:
            decision_points: 决策点列表
            
        Returns:
            技术选项列表
        """
        alternatives = []
        
        for point in decision_points:
            # 根据决策点类型生成不同的技术选项
            if point["type"] == "data_processing":
                alternatives.extend([
                    {
                        "decision_point": point,
                        "option": "pandas",
                        "description": "使用pandas库进行数据处理",
                        "pros": ["功能强大", "性能好", "社区活跃"],
                        "cons": ["依赖较多", "学习曲线较陡"]
                    },
                    {
                        "decision_point": point,
                        "option": "numpy",
                        "description": "使用numpy库进行数据处理",
                        "pros": ["性能极好", "内存效率高"],
                        "cons": ["功能相对简单", "需要自己实现一些功能"]
                    }
                ])
            elif point["type"] == "storage":
                alternatives.extend([
                    {
                        "decision_point": point,
                        "option": "sqlite",
                        "description": "使用SQLite数据库存储数据",
                        "pros": ["轻量级", "无需安装", "适合小型应用"],
                        "cons": ["并发性能有限", "不适合大规模数据"]
                    },
                    {
                        "decision_point": point,
                        "option": "json",
                        "description": "使用JSON文件存储数据",
                        "pros": ["简单", "可读性好", "无需额外依赖"],
                        "cons": ["不适合频繁读写", "不支持复杂查询"]
                    }
                ])
            elif point["type"] == "performance":
                alternatives.extend([
                    {
                        "decision_point": point,
                        "option": "multiprocessing",
                        "description": "使用多进程提高性能",
                        "pros": ["充分利用多核CPU", "适合CPU密集型任务"],
                        "cons": ["内存开销大", "进程间通信复杂"]
                    },
                    {
                        "decision_point": point,
                        "option": "asyncio",
                        "description": "使用异步IO提高性能",
                        "pros": ["适合IO密集型任务", "资源消耗小"],
                        "cons": ["代码复杂度增加", "需要重构同步代码"]
                    }
                ])
        
        return alternatives
    
    async def _evaluate_alternatives(self, alternatives: List[Dict[str, Any]], 
                                  requirements: List[str], 
                                  constraints: List[str]) -> List[Dict[str, Any]]:
        """
        评估技术选项
        
        Args:
            alternatives: 技术选项列表
            requirements: 需求列表
            constraints: 约束条件列表
            
        Returns:
            评估后的决策列表
        """
        decisions = []
        
        for alt in alternatives:
            # 计算选项的得分
            score = self._calculate_option_score(alt, requirements, constraints)
            
            # 生成决策
            decision = {
                "option": alt["option"],
                "description": alt["description"],
                "pros": alt["pros"],
                "cons": alt["cons"],
                "score": score,
                "reasoning": self._generate_decision_reasoning(alt, score)
            }
            decisions.append(decision)
        
        # 按得分排序
        decisions.sort(key=lambda x: x["score"], reverse=True)
        return decisions
    
    def _extract_constraints(self, requirement: str, constraints: List[str]) -> List[str]:
        """
        从需求和约束中提取相关约束
        
        Args:
            requirement: 需求文本
            constraints: 约束条件列表
            
        Returns:
            相关约束列表
        """
        relevant_constraints = []
        for constraint in constraints:
            if any(keyword in constraint.lower() for keyword in requirement.lower().split()):
                relevant_constraints.append(constraint)
        return relevant_constraints
    
    def _calculate_option_score(self, option: Dict[str, Any], 
                              requirements: List[str], 
                              constraints: List[str]) -> float:
        """
        计算技术选项的得分
        
        Args:
            option: 技术选项
            requirements: 需求列表
            constraints: 约束条件列表
            
        Returns:
            选项得分
        """
        score = 0.0
        
        # 基础分数
        score += 0.3
        
        # 根据优点加分
        score += len(option["pros"]) * 0.1
        
        # 根据缺点减分
        score -= len(option["cons"]) * 0.05
        
        # 检查是否满足约束
        for constraint in constraints:
            if any(keyword in option["description"].lower() for keyword in constraint.lower().split()):
                score += 0.2
        
        # 确保分数在0-1之间
        return max(0.0, min(1.0, score))
    
    def _generate_decision_reasoning(self, option: Dict[str, Any], score: float) -> str:
        """
        生成决策理由
        
        Args:
            option: 技术选项
            score: 选项得分
            
        Returns:
            决策理由
        """
        reasoning = f"选择{option['option']}的原因是：\n"
        reasoning += f"1. {option['description']}\n"
        reasoning += "2. 优点：\n"
        for pro in option["pros"]:
            reasoning += f"   - {pro}\n"
        reasoning += "3. 缺点：\n"
        for con in option["cons"]:
            reasoning += f"   - {con}\n"
        reasoning += f"4. 总体评分：{score:.2f}"
        return reasoning 