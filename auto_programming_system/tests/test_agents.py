import pytest
import os
from typing import Dict, Any
from auto_programming_system.agents import (
    BaseAgent,
    RequirementAgent,
    TechnicalAgent,
    SpecificationAgent,
    KnowledgeManager
)
from auto_programming_system.agents.config import (
    REQUIREMENT_AGENT_CONFIG,
    TECHNICAL_AGENT_CONFIG,
    SPECIFICATION_AGENT_CONFIG,
    KNOWLEDGE_BASE_CONFIG
)

class TestAgent(BaseAgent):
    """用于测试的具体代理类"""
    
    async def process(self, input_data: Any) -> Any:
        return {"result": input_data}
    
    async def update_context(self, new_context: Dict[str, Any]) -> None:
        self.context.update(new_context)

@pytest.fixture
def knowledge_manager():
    """创建知识库管理器实例"""
    test_kb_path = "test_knowledge_base.json"
    manager = KnowledgeManager(test_kb_path)
    yield manager
    # 清理测试文件
    if os.path.exists(test_kb_path):
        os.remove(test_kb_path)

@pytest.fixture
def requirement_agent():
    """创建需求理解代理实例"""
    return RequirementAgent(REQUIREMENT_AGENT_CONFIG)

@pytest.fixture
def technical_agent():
    """创建技术决策代理实例"""
    return TechnicalAgent(TECHNICAL_AGENT_CONFIG)

@pytest.fixture
def specification_agent():
    """创建规范优化代理实例"""
    return SpecificationAgent(SPECIFICATION_AGENT_CONFIG)

@pytest.fixture
def test_agent():
    """创建测试代理实例"""
    return TestAgent()

class TestBaseAgent:
    """测试基础代理类"""
    
    def test_base_agent_initialization(self, test_agent):
        """测试基础代理初始化"""
        assert test_agent.config == {}
        assert test_agent.context == {}
        
    def test_base_agent_with_config(self, test_agent):
        """测试带配置的基础代理初始化"""
        config = {"test": "config"}
        test_agent.config = config
        assert test_agent.config == config
        assert test_agent.context == {}
        
    def test_base_agent_context(self, test_agent):
        """测试基础代理上下文管理"""
        new_context = {"key": "value"}
        test_agent.context = new_context
        assert test_agent.get_context() == new_context
        test_agent.clear_context()
        assert test_agent.get_context() == {}

class TestRequirementAgent:
    """测试需求理解代理"""
    
    @pytest.mark.asyncio
    async def test_requirement_agent_initialization(self, requirement_agent):
        """测试需求理解代理初始化"""
        assert requirement_agent.config == REQUIREMENT_AGENT_CONFIG
        assert requirement_agent.requirements == []
        assert requirement_agent.questions == []
        
    @pytest.mark.asyncio
    async def test_requirement_agent_process(self, requirement_agent):
        """测试需求理解代理处理"""
        input_data = "创建一个处理CSV文件的函数"
        result = await requirement_agent.process(input_data)
        assert isinstance(result, dict)
        assert "requirements" in result
        assert "questions" in result
        assert "context" in result
        
    @pytest.mark.asyncio
    async def test_preprocess_text(self, requirement_agent):
        """测试文本预处理功能"""
        text = "创建一个处理CSV文件的函数！性能要好。"
        processed = await requirement_agent._preprocess_text(text)
        assert "创建一个处理CSV文件的函数" in processed
        assert "性能要好" in processed
        
    @pytest.mark.asyncio
    async def test_analyze_requirements(self, requirement_agent):
        """测试需求分析功能"""
        text = "创建一个处理CSV文件的函数。性能要好。"
        requirements = await requirement_agent._analyze_requirements(text)
        assert len(requirements) > 0
        assert any(r["type"] == "functional" for r in requirements)
        assert any(r["type"] == "non_functional" for r in requirements)
        
    @pytest.mark.asyncio
    async def test_generate_questions(self, requirement_agent):
        """测试问题生成功能"""
        requirements = [
            {
                "type": "functional",
                "content": "创建一个处理CSV文件的函数",
                "confidence": 0.9,
                "keywords": ["创建", "处理", "CSV", "文件", "函数"]
            },
            {
                "type": "non_functional",
                "content": "性能要好",
                "confidence": 0.85,
                "keywords": ["性能", "好"]
            }
        ]
        questions = await requirement_agent._generate_questions(requirements)
        assert len(questions) > 0
        assert any("异常处理" in q for q in questions)
        assert any("性能要求" in q for q in questions)

class TestTechnicalAgent:
    """测试技术决策代理"""
    
    @pytest.mark.asyncio
    async def test_technical_agent_initialization(self, technical_agent):
        """测试技术决策代理初始化"""
        assert technical_agent.config == TECHNICAL_AGENT_CONFIG
        assert technical_agent.decisions == []
        assert technical_agent.alternatives == []
        
    @pytest.mark.asyncio
    async def test_technical_agent_process(self, technical_agent):
        """测试技术决策代理处理"""
        input_data = {
            "requirements": ["处理CSV文件", "性能要好"],
            "constraints": ["使用Python标准库"]
        }
        result = await technical_agent.process(input_data)
        assert isinstance(result, dict)
        assert "decisions" in result
        assert "alternatives" in result
        assert "context" in result
        
    @pytest.mark.asyncio
    async def test_identify_decision_points(self, technical_agent):
        """测试决策点识别功能"""
        requirements = ["处理CSV文件", "性能要好"]
        constraints = ["使用Python标准库"]
        decision_points = await technical_agent._identify_decision_points(requirements, constraints)
        assert len(decision_points) > 0
        assert any(point["type"] == "data_processing" for point in decision_points)
        assert any(point["type"] == "performance" for point in decision_points)
        
    @pytest.mark.asyncio
    async def test_generate_alternatives(self, technical_agent):
        """测试选项生成功能"""
        decision_points = [
            {
                "type": "data_processing",
                "content": "处理CSV文件",
                "confidence": 0.9,
                "constraints": ["使用Python标准库"]
            }
        ]
        alternatives = await technical_agent._generate_alternatives(decision_points)
        assert len(alternatives) > 0
        assert any(alt["option"] == "pandas" for alt in alternatives)
        assert any(alt["option"] == "numpy" for alt in alternatives)
        
    @pytest.mark.asyncio
    async def test_evaluate_alternatives(self, technical_agent):
        """测试选项评估功能"""
        alternatives = [
            {
                "decision_point": {
                    "type": "data_processing",
                    "content": "处理CSV文件",
                    "confidence": 0.9,
                    "constraints": ["使用Python标准库"]
                },
                "option": "pandas",
                "description": "使用pandas库进行数据处理",
                "pros": ["功能强大", "性能好", "社区活跃"],
                "cons": ["依赖较多", "学习曲线较陡"]
            }
        ]
        requirements = ["处理CSV文件"]
        constraints = ["使用Python标准库"]
        decisions = await technical_agent._evaluate_alternatives(alternatives, requirements, constraints)
        assert len(decisions) > 0
        assert decisions[0]["option"] == "pandas"
        assert "score" in decisions[0]
        assert "reasoning" in decisions[0]

class TestSpecificationAgent:
    """测试规范优化代理"""
    
    @pytest.mark.asyncio
    async def test_specification_agent_initialization(self, specification_agent):
        """测试规范优化代理初始化"""
        assert specification_agent.config == SPECIFICATION_AGENT_CONFIG
        assert specification_agent.specifications == []
        assert specification_agent.optimizations == []
        
    @pytest.mark.asyncio
    async def test_specification_agent_process(self, specification_agent):
        """测试规范优化代理处理"""
        input_data = {
            "requirements": ["创建一个处理CSV文件的函数", "性能要好"],
            "decisions": [
                {
                    "option": "pandas",
                    "description": "使用pandas库进行数据处理",
                    "pros": ["功能强大", "性能好"],
                    "cons": ["依赖较多"],
                    "reasoning": "pandas是最适合处理CSV文件的库"
                }
            ]
        }
        result = await specification_agent.process(input_data)
        assert isinstance(result, dict)
        assert "specifications" in result
        assert "optimizations" in result
        assert "context" in result
        
    @pytest.mark.asyncio
    async def test_generate_specifications(self, specification_agent):
        """测试规范生成功能"""
        requirements = ["创建一个处理CSV文件的函数"]
        decisions = [
            {
                "option": "pandas",
                "description": "使用pandas库进行数据处理",
                "pros": ["功能强大", "性能好"],
                "cons": ["依赖较多"],
                "reasoning": "pandas是最适合处理CSV文件的库"
            }
        ]
        specifications = await specification_agent._generate_specifications(requirements, decisions)
        assert len(specifications) > 0
        assert specifications[0]["type"] == "function"
        assert "content" in specifications[0]
        assert "constraints" in specifications[0]
        assert "dependencies" in specifications[0]
        assert "validation_rules" in specifications[0]
        
    @pytest.mark.asyncio
    async def test_optimize_specifications(self, specification_agent):
        """测试规范优化功能"""
        specifications = [
            {
                "requirement": "创建一个处理CSV文件的函数",
                "type": "function",
                "content": {
                    "description": "处理CSV文件",
                    "implementation_notes": ["使用pandas"],
                    "technical_details": {
                        "pandas": {
                            "description": "数据处理库",
                            "pros": ["功能强大"],
                            "cons": ["依赖多"]
                        }
                    }
                },
                "constraints": ["performance"],
                "dependencies": ["pandas"],
                "validation_rules": []
            }
        ]
        optimized_specs = await specification_agent._optimize_specifications(specifications)
        assert len(optimized_specs) > 0
        assert "optimization_history" in optimized_specs[0]
        
    @pytest.mark.asyncio
    async def test_validate_specifications(self, specification_agent):
        """测试规范验证功能"""
        specifications = [
            {
                "requirement": "创建一个处理CSV文件的函数",
                "type": "function",
                "content": {
                    "description": "处理CSV文件",
                    "implementation_notes": ["使用pandas"],
                    "technical_details": {
                        "pandas": {
                            "description": "数据处理库",
                            "pros": ["功能强大"],
                            "cons": ["依赖多"]
                        }
                    }
                },
                "constraints": ["performance"],
                "dependencies": ["pandas"],
                "validation_rules": [
                    {
                        "type": "completeness",
                        "description": "检查是否满足所有需求",
                        "severity": "high"
                    }
                ]
            }
        ]
        validated_specs = await specification_agent._validate_specifications(specifications)
        assert len(validated_specs) > 0
        assert "validation_errors" not in validated_specs[0]
        
    @pytest.mark.asyncio
    async def test_validate_specifications_with_errors(self, specification_agent):
        """测试规范验证错误处理"""
        specifications = [
            {
                "requirement": "创建一个处理CSV文件的函数",
                "type": "function",
                "content": {},  # 空内容
                "constraints": [],  # 无约束
                "dependencies": [],  # 无依赖
                "validation_rules": []  # 无验证规则
            }
        ]
        validated_specs = await specification_agent._validate_specifications(specifications)
        assert len(validated_specs) > 0
        assert "validation_errors" in validated_specs[0]
        assert len(validated_specs[0]["validation_errors"]) > 0
        
    def test_find_relevant_decisions(self, specification_agent):
        """测试相关决策查找功能"""
        requirement = "创建一个处理CSV文件的函数"
        decisions = [
            {
                "option": "pandas",
                "description": "使用pandas库进行数据处理",
                "pros": ["功能强大", "性能好"],
                "cons": ["依赖较多"],
                "reasoning": "pandas是最适合处理CSV文件的库"
            }
        ]
        relevant_decisions = specification_agent._find_relevant_decisions(requirement, decisions)
        assert len(relevant_decisions) > 0
        assert relevant_decisions[0]["option"] == "pandas"
        
    def test_determine_spec_type(self, specification_agent):
        """测试规范类型确定功能"""
        assert specification_agent._determine_spec_type("创建一个函数") == "function"
        assert specification_agent._determine_spec_type("创建一个模块") == "module"
        assert specification_agent._determine_spec_type("其他需求") == "general"
        
    def test_generate_spec_content(self, specification_agent):
        """测试规范内容生成功能"""
        requirement = "创建一个处理CSV文件的函数"
        decisions = [
            {
                "option": "pandas",
                "description": "使用pandas库进行数据处理",
                "pros": ["功能强大", "性能好"],
                "cons": ["依赖较多"],
                "reasoning": "pandas是最适合处理CSV文件的库"
            }
        ]
        content = specification_agent._generate_spec_content(requirement, decisions)
        assert "description" in content
        assert "implementation_notes" in content
        assert "technical_details" in content
        assert "pandas" in content["technical_details"]
        
    def test_extract_constraints(self, specification_agent):
        """测试约束提取功能"""
        requirement = "创建一个性能好且安全的函数"
        constraints = specification_agent._extract_constraints(requirement)
        assert "performance" in constraints
        assert "security" in constraints
        
    def test_get_dependencies(self, specification_agent):
        """测试依赖项获取功能"""
        decisions = [
            {
                "option": "pandas",
                "description": "使用pandas库进行数据处理",
                "pros": ["功能强大", "性能好"],
                "cons": ["依赖较多"],
                "reasoning": "pandas是最适合处理CSV文件的库"
            }
        ]
        dependencies = specification_agent._get_dependencies(decisions)
        assert len(dependencies) > 0
        assert "pandas" in dependencies
        
    def test_generate_validation_rules(self, specification_agent):
        """测试验证规则生成功能"""
        requirement = "创建一个性能好的函数"
        decisions = [
            {
                "option": "pandas",
                "description": "使用pandas库进行数据处理",
                "pros": ["功能强大", "性能好"],
                "cons": ["依赖较多"],
                "reasoning": "pandas是最适合处理CSV文件的库"
            }
        ]
        rules = specification_agent._generate_validation_rules(requirement, decisions)
        assert len(rules) > 0
        assert any(rule["type"] == "completeness" for rule in rules)
        assert any(rule["type"] == "performance" for rule in rules)
        assert any(rule["type"] == "implementation" for rule in rules)

class TestKnowledgeManager:
    """测试知识库管理器"""
    
    def test_knowledge_manager_initialization(self, knowledge_manager):
        """测试知识库管理器初始化"""
        assert knowledge_manager.knowledge_base_path == "test_knowledge_base.json"
        assert isinstance(knowledge_manager.knowledge_base, dict)
        assert "domain_knowledge" in knowledge_manager.knowledge_base
        assert "technical_patterns" in knowledge_manager.knowledge_base
        assert "best_practices" in knowledge_manager.knowledge_base
        assert "metadata" in knowledge_manager.knowledge_base
        
    def test_add_domain_knowledge(self, knowledge_manager):
        """测试添加领域知识"""
        domain = "data_processing"
        knowledge = {"type": "csv", "operations": ["read", "write"]}
        knowledge_manager.add_domain_knowledge(domain, knowledge)
        domain_knowledge = knowledge_manager.get_domain_knowledge(domain)
        assert len(domain_knowledge) == 1
        assert domain_knowledge[0]["content"] == knowledge
        
    def test_add_technical_pattern(self, knowledge_manager):
        """测试添加技术模式"""
        pattern_type = "data_processing"
        pattern = {"name": "csv_processor", "description": "CSV文件处理模式"}
        knowledge_manager.add_technical_pattern(pattern_type, pattern)
        patterns = knowledge_manager.get_technical_patterns(pattern_type)
        assert len(patterns) == 1
        assert patterns[0]["content"] == pattern
        
    def test_add_best_practice(self, knowledge_manager):
        """测试添加最佳实践"""
        practice_type = "error_handling"
        practice = {"name": "graceful_failure", "description": "优雅处理错误"}
        knowledge_manager.add_best_practice(practice_type, practice)
        practices = knowledge_manager.get_best_practices(practice_type)
        assert len(practices) == 1
        assert practices[0]["content"] == practice 