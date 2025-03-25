from typing import Any, Dict, List, Optional
from .base_agent import BaseAgent

class SpecificationAgent(BaseAgent):
    """规范优化代理，负责优化和验证规范"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化规范优化代理
        
        Args:
            config: 代理配置信息
        """
        super().__init__(config)
        self.specifications = []
        self.optimizations = []
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理需求和技术决策，生成和优化规范
        
        Args:
            input_data: 包含需求和技术决策的输入数据
            
        Returns:
            优化后的规范
        """
        # 1. 分析输入
        requirements = input_data.get("requirements", [])
        decisions = input_data.get("decisions", [])
        
        # 2. 生成初始规范
        specifications = await self._generate_specifications(requirements, decisions)
        
        # 3. 优化规范
        optimized_specs = await self._optimize_specifications(specifications)
        
        # 4. 验证规范
        validated_specs = await self._validate_specifications(optimized_specs)
        
        # 5. 更新上下文
        self.specifications = validated_specs
        self.optimizations = self._get_optimization_history()
        
        return {
            "specifications": validated_specs,
            "optimizations": self.optimizations,
            "context": self.get_context()
        }
    
    async def update_context(self, new_context: Dict[str, Any]) -> None:
        """
        更新代理上下文
        
        Args:
            new_context: 新的上下文信息
        """
        self.context.update(new_context)
        
    async def _generate_specifications(self, requirements: List[str], decisions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        生成初始规范
        
        Args:
            requirements: 需求列表
            decisions: 技术决策列表
            
        Returns:
            初始规范列表
        """
        specifications = []
        
        # 获取规范配置
        spec_config = self.config.get("specification", {})
        max_iterations = spec_config.get("max_iterations", 3)
        min_improvement = spec_config.get("min_improvement", 0.1)
        
        # 为每个需求生成规范
        for req in requirements:
            # 找到相关的技术决策
            relevant_decisions = self._find_relevant_decisions(req, decisions)
            
            # 生成规范
            spec = {
                "requirement": req,
                "type": self._determine_spec_type(req),
                "content": self._generate_spec_content(req, relevant_decisions),
                "constraints": self._extract_constraints(req),
                "dependencies": self._get_dependencies(relevant_decisions),
                "validation_rules": self._generate_validation_rules(req, relevant_decisions)
            }
            specifications.append(spec)
        
        return specifications
    
    async def _optimize_specifications(self, specifications: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        优化规范
        
        Args:
            specifications: 初始规范列表
            
        Returns:
            优化后的规范列表
        """
        optimized_specs = []
        
        for spec in specifications:
            # 获取优化配置
            optimization_config = self.config.get("optimization", {})
            max_iterations = optimization_config.get("max_iterations", 3)
            min_improvement = optimization_config.get("min_improvement", 0.1)
            
            # 优化规范
            optimized_spec = await self._optimize_single_specification(spec, max_iterations, min_improvement)
            optimized_specs.append(optimized_spec)
        
        return optimized_specs
    
    async def _validate_specifications(self, specifications: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        验证规范
        
        Args:
            specifications: 规范列表
            
        Returns:
            验证后的规范列表
        """
        validated_specs = []
        
        for spec in specifications:
            validation_result = await self._validate_single_specification(spec)
            if not validation_result["is_valid"]:
                spec["validation_errors"] = validation_result["errors"]
            validated_specs.append(spec)
        
        return validated_specs
    
    def _find_relevant_decisions(self, requirement: str, decisions: List[Dict]) -> List[Dict]:
        """查找相关的技术决策"""
        relevant_decisions = []
        requirement_lower = requirement.lower()
        
        for decision in decisions:
            # 检查决策选项名称是否在需求中
            if decision["option"].lower() in requirement_lower:
                relevant_decisions.append(decision)
                continue
                
            # 检查决策描述中的关键词
            description = decision["description"].lower()
            if "csv" in description and "csv" in requirement_lower:
                relevant_decisions.append(decision)
                continue
                
            # 检查决策理由中的关键词
            reasoning = decision["reasoning"].lower()
            if "csv" in reasoning and "csv" in requirement_lower:
                relevant_decisions.append(decision)
                continue
                
            # 检查决策的优缺点中的关键词
            pros = [pro.lower() for pro in decision.get("pros", [])]
            cons = [con.lower() for con in decision.get("cons", [])]
            if any(keyword in requirement_lower for keyword in pros + cons):
                relevant_decisions.append(decision)
                
        return relevant_decisions
    
    def _determine_spec_type(self, requirement: str) -> str:
        """
        确定规范类型
        
        Args:
            requirement: 需求文本
            
        Returns:
            规范类型
        """
        if any(keyword in requirement.lower() for keyword in ["函数", "方法", "类"]):
            return "function"
        elif any(keyword in requirement.lower() for keyword in ["模块", "包", "库"]):
            return "module"
        else:
            return "general"
    
    def _generate_spec_content(self, requirement: str, decisions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成规范内容
        
        Args:
            requirement: 需求文本
            decisions: 相关的技术决策列表
            
        Returns:
            规范内容
        """
        content = {
            "description": requirement,
            "implementation_notes": [],
            "technical_details": {}
        }
        
        # 添加技术决策相关的实现说明
        for decision in decisions:
            content["implementation_notes"].append(decision["reasoning"])
            content["technical_details"][decision["option"]] = {
                "description": decision.get("description", ""),
                "pros": decision.get("pros", []),
                "cons": decision.get("cons", [])
            }
        
        return content
    
    def _extract_constraints(self, requirement: str) -> List[str]:
        """
        从需求中提取约束条件
        
        Args:
            requirement: 需求文本
            
        Returns:
            约束条件列表
        """
        constraints = []
        # 提取性能约束
        if "性能" in requirement:
            constraints.append("performance")
        # 提取安全约束
        if "安全" in requirement:
            constraints.append("security")
        # 提取可维护性约束
        if "维护" in requirement:
            constraints.append("maintainability")
        return constraints
    
    def _get_dependencies(self, decisions: List[Dict[str, Any]]) -> List[str]:
        """
        获取依赖项
        
        Args:
            decisions: 技术决策列表
            
        Returns:
            依赖项列表
        """
        dependencies = []
        for decision in decisions:
            dependencies.append(decision["option"])
        return dependencies
    
    def _generate_validation_rules(self, requirement: str, decisions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        生成验证规则
        
        Args:
            requirement: 需求文本
            decisions: 技术决策列表
            
        Returns:
            验证规则列表
        """
        rules = []
        
        # 添加基本验证规则
        rules.append({
            "type": "completeness",
            "description": "检查是否满足所有需求",
            "severity": "high"
        })
        
        # 添加性能验证规则
        if "性能" in requirement:
            rules.append({
                "type": "performance",
                "description": "检查性能指标",
                "severity": "medium"
            })
        
        # 添加技术决策相关的验证规则
        for decision in decisions:
            rules.append({
                "type": "implementation",
                "description": f"检查{decision['option']}的实现",
                "severity": "high"
            })
        
        return rules
    
    async def _optimize_single_specification(self, spec: Dict[str, Any], 
                                          max_iterations: int, 
                                          min_improvement: float) -> Dict[str, Any]:
        """
        优化单个规范
        
        Args:
            spec: 规范
            max_iterations: 最大迭代次数
            min_improvement: 最小改进阈值
            
        Returns:
            优化后的规范
        """
        optimized_spec = spec.copy()
        improvement_history = []
        
        for i in range(max_iterations):
            # 优化规范内容
            improved_content = await self._optimize_content(optimized_spec["content"])
            
            # 计算改进程度
            improvement = self._calculate_improvement(optimized_spec["content"], improved_content)
            improvement_history.append(improvement)
            
            # 如果改进程度足够，更新规范
            if improvement >= min_improvement:
                optimized_spec["content"] = improved_content
            else:
                break
        
        # 记录优化历史
        optimized_spec["optimization_history"] = improvement_history
        return optimized_spec
    
    async def _validate_single_specification(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证单个规范
        
        Args:
            spec: 规范
            
        Returns:
            验证结果
        """
        validation_result = {
            "is_valid": True,
            "errors": []
        }
        
        # 检查完整性
        if not spec.get("content"):
            validation_result["is_valid"] = False
            validation_result["errors"].append("规范内容为空")
        
        # 检查依赖项
        if not spec.get("dependencies"):
            validation_result["is_valid"] = False
            validation_result["errors"].append("缺少依赖项")
        
        # 检查验证规则
        if not spec.get("validation_rules"):
            validation_result["is_valid"] = False
            validation_result["errors"].append("缺少验证规则")
        
        return validation_result
    
    async def _optimize_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        优化规范内容
        
        Args:
            content: 规范内容
            
        Returns:
            优化后的内容
        """
        optimized_content = content.copy()
        
        # 优化实现说明
        optimized_content["implementation_notes"] = [
            note for note in content["implementation_notes"]
            if len(note) > 10  # 移除过短的说明
        ]
        
        # 优化技术细节
        for tech, details in content["technical_details"].items():
            if details.get("pros") and details.get("cons"):
                optimized_content["technical_details"][tech] = details
        
        return optimized_content
    
    def _calculate_improvement(self, old_content: Dict[str, Any], new_content: Dict[str, Any]) -> float:
        """
        计算改进程度
        
        Args:
            old_content: 旧的内容
            new_content: 新的内容
            
        Returns:
            改进程度（0-1）
        """
        # 简单的改进度计算
        old_notes_count = len(old_content.get("implementation_notes", []))
        new_notes_count = len(new_content.get("implementation_notes", []))
        
        if old_notes_count == 0:
            return 1.0
        
        return min(1.0, new_notes_count / old_notes_count)
    
    def _get_optimization_history(self) -> List[Dict[str, Any]]:
        """
        获取优化历史
        
        Returns:
            优化历史列表
        """
        history = []
        for spec in self.specifications:
            if "optimization_history" in spec:
                history.append({
                    "spec_id": id(spec),
                    "improvements": spec["optimization_history"]
                })
        return history 