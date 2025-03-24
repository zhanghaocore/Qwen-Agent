"""
多层次需求挖掘Agent
通过逐步推理深入分析用户需求，生成详细的需求规范
"""

from typing import Dict, List, Any, Optional, Union
import json
import os
import sys

# 添加项目根目录到路径，以便导入项目内模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

try:
    # 尝试导入qwen_agent相关模块
    from qwen_agent.agents import FnCallAgent  
    from qwen_agent.llm import BaseChatModel
    from qwen_agent.llm.schema import ASSISTANT, DEFAULT_SYSTEM_MESSAGE, USER, Message
    from qwen_agent.tools.base import BaseTool, register_tool

    # 标记是否使用qwen_agent
    USE_QWEN_AGENT = True
except ImportError:
    # 如果qwen_agent不可用，使用简化版Agent基类
    print("Qwen-Agent不可用，使用简化版Agent实现")
    USE_QWEN_AGENT = False
    
    # 定义简化版基类和工具
    class FnCallAgent:
        """简化版Agent基类"""
        def __init__(self, function_list=None, llm=None, system_message=None, name=None, description=None, **kwargs):
            self.function_list = function_list or []
            self.llm_config = llm
            self.system_message = system_message
            self.name = name
            self.description = description
            
        def run(self, messages):
            """模拟Agent运行"""
            yield [{"role": "assistant", "content": "请安装qwen_agent以使用完整功能"}]
    
    class BaseTool:
        """简化版工具基类"""
        def __init__(self):
            self.function = {"name": self.__class__.__name__}
            
    def register_tool(name):
        """模拟装饰器"""
        def decorator(cls):
            return cls
        return decorator

# 导入工具类
from .tools import (
    DomainClassifierTool, 
    QuestionGeneratorTool, 
    TechDecisionAnalyzerTool, 
    RequirementSpecGeneratorTool
)

# 系统提示词，指导Agent进行多层次需求分析
REQUIREMENT_ANALYSIS_SYSTEM_PROMPT = """你是一个专业的需求分析专家，负责将用户的初始需求转化为详细的编程规范。按照以下多层次需求挖掘框架工作：

1. 领域分类：首先识别需求所属领域（如Web应用、数据处理、API服务等）
2. 关键问题提取：基于领域知识提出关键问题
3. 逐层推理：每个答案触发更细粒度的子问题，不断深化需求理解
4. 技术决策：推荐合适的技术栈，并提供选择理由和备选方案
5. 完整性检查：确保所有必要的需求维度都已覆盖

你的目标是通过多轮推理，生成一个结构化的需求规范文档，包含：
- 功能需求详述
- 技术架构建议
- 关键组件说明
- 实现细节和接口定义

请始终保持系统化思考，不要遗漏任何关键决策点。"""


# 实现内部工具包装类（无需注册）
class QwenDomainClassifierTool:
    """对初始需求进行领域分类，确定适用的问题库和分析策略"""
    
    def __init__(self):
        self.internal_tool = DomainClassifierTool()
        
    def get_function_dict(self):
        """返回函数定义字典"""
        return {
            "name": "domain_classifier_tool",
            "description": "基于初始需求文本，识别其所属的应用领域，返回领域类型和关键特征",
            "parameters": {
                "type": "object",
                "properties": {
                    "requirement_text": {
                        "type": "string",
                        "description": "用户的初始需求描述文本"
                    }
                },
                "required": ["requirement_text"]
            }
        }
        
    def call(self, params: str, **kwargs) -> str:
        return self.internal_tool.call(params, **kwargs)


class QwenQuestionGeneratorTool:
    """基于当前对话上下文和领域分类，生成下一步应该提问的问题"""
    
    def __init__(self):
        self.internal_tool = QuestionGeneratorTool()
        
    def get_function_dict(self):
        """返回函数定义字典"""
        return {
            "name": "question_generator_tool",
            "description": "基于已有的需求信息和对话历史，生成下一步应该询问的问题，以深化需求理解",
            "parameters": {
                "type": "object",
                "properties": {
                    "domain": {
                        "type": "string",
                        "description": "需求所属的主要领域"
                    },
                    "current_understanding": {
                        "type": "string",
                        "description": "当前对需求的理解摘要"
                    },
                    "discussion_history": {
                        "type": "string",
                        "description": "已讨论过的问题和答案"
                    }
                },
                "required": ["domain", "current_understanding", "discussion_history"]
            }
        }
        
    def call(self, params: str, **kwargs) -> str:
        return self.internal_tool.call(params, **kwargs)


class QwenTechDecisionAnalyzerTool:
    """分析需求并提供技术决策建议，包括技术栈选择和实现方案"""
    
    def __init__(self):
        self.internal_tool = TechDecisionAnalyzerTool()
        
    def get_function_dict(self):
        """返回函数定义字典"""
        return {
            "name": "tech_decision_analyzer_tool",
            "description": "基于需求分析结果，提供技术栈选择建议和实现方案，包括优缺点分析和备选方案",
            "parameters": {
                "type": "object",
                "properties": {
                    "domain": {
                        "type": "string",
                        "description": "需求所属的主要领域"
                    },
                    "requirements_summary": {
                        "type": "string",
                        "description": "需求的详细摘要描述"
                    },
                    "technical_constraints": {
                        "type": "string",
                        "description": "已知的技术约束条件"
                    }
                },
                "required": ["domain", "requirements_summary", "technical_constraints"]
            }
        }
        
    def call(self, params: str, **kwargs) -> str:
        return self.internal_tool.call(params, **kwargs)


class QwenRequirementSpecGeneratorTool:
    """生成完整的需求规范文档，整合所有分析结果"""
    
    def __init__(self):
        self.internal_tool = RequirementSpecGeneratorTool()
        
    def get_function_dict(self):
        """返回函数定义字典"""
        return {
            "name": "requirement_spec_generator_tool",
            "description": "根据对话历史和分析结果，生成结构化的需求规范文档",
            "parameters": {
                "type": "object",
                "properties": {
                    "domain": {
                        "type": "string",
                        "description": "需求所属的主要领域"
                    },
                    "discussion_summary": {
                        "type": "string",
                        "description": "需求讨论的摘要内容"
                    },
                    "tech_decisions": {
                        "type": "string",
                        "description": "技术决策和架构建议"
                    }
                },
                "required": ["domain", "discussion_summary", "tech_decisions"]
            }
        }
        
    def call(self, params: str, **kwargs) -> str:
        return self.internal_tool.call(params, **kwargs)


class StepByStepRequirementAnalysisAgent(FnCallAgent):
    """实现多层次需求挖掘的智能体"""
    
    def __init__(self,
                 function_list=None,
                 llm=None,
                 system_message=REQUIREMENT_ANALYSIS_SYSTEM_PROMPT,
                 name="需求分析专家",
                 description="通过逐步推理深入分析用户需求，生成详细的需求规范的智能体",
                 **kwargs):
        
        if USE_QWEN_AGENT:
            # 使用Qwen-Agent时的初始化但不依赖装饰器注册工具
            # 创建工具实例
            tools = [
                QwenDomainClassifierTool(),
                QwenQuestionGeneratorTool(),
                QwenTechDecisionAnalyzerTool(),
                QwenRequirementSpecGeneratorTool()
            ]
            
            # 初始化FnCallAgent
            super().__init__(
                function_list=function_list,  # 不使用工具，避免注册问题
                llm=llm or {'model': 'qwen2.5-72b-instruct'},
                system_message=system_message,
                name=name,
                description=description,
                **kwargs
            )
            # 保存工具以供analyze_requirement使用
            self.qwen_tools = tools
        else:
            # 简化版初始化
            super().__init__(
                function_list=function_list,
                llm=llm,
                system_message=system_message,
                name=name,
                description=description,
                **kwargs
            )
            self.tools = [
                DomainClassifierTool(),
                QuestionGeneratorTool(),
                TechDecisionAnalyzerTool(),
                RequirementSpecGeneratorTool()
            ]
            
    def analyze_requirement(self, requirement_text, discussion_history=None):
        """分析需求，启动多层次需求挖掘流程
        
        Args:
            requirement_text: 用户初始需求文本
            discussion_history: 之前的对话历史记录，格式为[{"role": "user/assistant", "content": "..."}]
            
        Returns:
            需求分析结果，包含下一步建议的问题和当前的分析结果
        """
        try:
            # 初始化或获取对话历史
            history = discussion_history or []
            current_understanding = self._build_current_understanding(history + [{"role": "user", "content": requirement_text}])
            
            # 1. 领域分类
            domain_classifier = DomainClassifierTool()
            domain_result = domain_classifier.call(
                json.dumps({"requirement_text": current_understanding})
            )
            domain_info = json.loads(domain_result)
            primary_domain = domain_info.get("primary_domain", "通用应用")
            
            # 2. 生成深入问题
            question_generator = QuestionGeneratorTool()
            questions_result = question_generator.call(
                json.dumps({
                    "domain": primary_domain,
                    "current_understanding": current_understanding,
                    "discussion_history": json.dumps(history)
                })
            )
            questions_info = json.loads(questions_result)
            
            # 3. 提取已知的技术约束
            tech_constraints = self._extract_tech_constraints(history)
            
            # 4. 技术决策分析
            tech_analyzer = TechDecisionAnalyzerTool()
            tech_result = tech_analyzer.call(
                json.dumps({
                    "domain": primary_domain,
                    "requirements_summary": current_understanding,
                    "technical_constraints": tech_constraints
                })
            )
            tech_info = json.loads(tech_result)
            
            # 5. 生成需求规范
            spec_generator = RequirementSpecGeneratorTool()
            spec_result = spec_generator.call(
                json.dumps({
                    "domain": primary_domain,
                    "discussion_summary": current_understanding,
                    "tech_decisions": json.dumps(tech_info)
                })
            )
            spec_info = json.loads(spec_result)
            
            # 6. 分析完整性和确定下一步
            completeness_analysis = self._analyze_completeness(
                domain_info,
                questions_info,
                tech_info,
                spec_info
            )
            
            return {
                "domain_analysis": domain_info,
                "current_understanding": current_understanding,
                "discussion_stage": questions_info.get("current_stage"),
                "next_questions": questions_info.get("next_questions", []),
                "tech_analysis": tech_info,
                "requirement_spec": spec_info,
                "completeness_analysis": completeness_analysis,
                "next_steps": self._determine_next_steps(completeness_analysis)
            }
            
        except Exception as e:
            return {"error": str(e)}
            
    def _build_current_understanding(self, history):
        """根据对话历史构建当前的需求理解
        
        Args:
            history: 对话历史记录
            
        Returns:
            当前的需求理解摘要
        """
        # 提取所有用户输入
        user_inputs = [
            msg["content"] for msg in history 
            if msg["role"] == "user"
        ]
        
        # 合并用户输入，生成摘要
        return " ".join(user_inputs)
        
    def _extract_tech_constraints(self, history):
        """从对话历史中提取技术约束
        
        Args:
            history: 对话历史记录
            
        Returns:
            技术约束的描述
        """
        constraints = []
        
        # 在对话历史中查找技术约束相关的关键词
        tech_keywords = [
            "必须使用", "需要用", "基于", "版本要求",
            "性能要求", "并发", "响应时间", "技术栈"
        ]
        
        for msg in history:
            if msg["role"] == "user":
                content = msg["content"].lower()
                for keyword in tech_keywords:
                    if keyword in content:
                        # 提取包含关键词的句子
                        sentences = content.split("。")
                        for sentence in sentences:
                            if keyword in sentence:
                                constraints.append(sentence.strip())
        
        return "；".join(constraints) if constraints else "无特定约束"
        
    def _analyze_completeness(self, domain_info, questions_info, tech_info, spec_info):
        """分析需求理解的完整性
        
        Args:
            domain_info: 领域分析结果
            questions_info: 问题生成结果
            tech_info: 技术决策分析结果
            spec_info: 需求规范结果
            
        Returns:
            完整性分析结果
        """
        completeness = {
            "domain_clarity": self._check_domain_clarity(domain_info),
            "requirement_coverage": self._check_requirement_coverage(spec_info),
            "tech_decision_clarity": self._check_tech_decision_clarity(tech_info),
            "missing_aspects": []
        }
        
        # 检查是否缺失关键信息
        if not completeness["domain_clarity"]["is_clear"]:
            completeness["missing_aspects"].append("领域信息不明确")
        if not completeness["requirement_coverage"]["is_complete"]:
            completeness["missing_aspects"].extend(
                completeness["requirement_coverage"]["missing_items"]
            )
        if not completeness["tech_decision_clarity"]["is_clear"]:
            completeness["missing_aspects"].extend(
                completeness["tech_decision_clarity"]["unclear_points"]
            )
            
        return completeness
        
    def _check_domain_clarity(self, domain_info):
        """检查领域信息的清晰度"""
        return {
            "is_clear": domain_info.get("primary_domain") != "通用应用",
            "confidence": 0.8 if domain_info.get("key_features") else 0.5
        }
        
    def _check_requirement_coverage(self, spec_info):
        """检查需求覆盖的完整性"""
        doc = spec_info.get("需求规范文档", {})
        functional_reqs = doc.get("功能需求", [])
        non_functional_reqs = doc.get("非功能需求", [])
        
        missing_items = []
        if not functional_reqs:
            missing_items.append("功能需求")
        if not non_functional_reqs:
            missing_items.append("非功能需求")
            
        return {
            "is_complete": len(missing_items) == 0,
            "missing_items": missing_items
        }
        
    def _check_tech_decision_clarity(self, tech_info):
        """检查技术决策的清晰度"""
        unclear_points = []
        
        if not tech_info.get("tech_recommendations"):
            unclear_points.append("技术栈选择")
        if not tech_info.get("architecture_recommendation"):
            unclear_points.append("架构设计")
            
        return {
            "is_clear": len(unclear_points) == 0,
            "unclear_points": unclear_points
        }
        
    def _determine_next_steps(self, completeness_analysis):
        """根据完整性分析确定下一步行动
        
        Args:
            completeness_analysis: 完整性分析结果
            
        Returns:
            下一步行动建议列表
        """
        next_steps = []
        
        # 根据缺失的方面提供建议
        for aspect in completeness_analysis["missing_aspects"]:
            if "领域" in aspect:
                next_steps.append({
                    "type": "clarify_domain",
                    "description": "需要进一步明确系统的主要应用领域",
                    "suggested_questions": [
                        "这个系统主要服务于哪个行业或领域？",
                        "系统的主要用户群体是谁？"
                    ]
                })
            elif "功能需求" in aspect:
                next_steps.append({
                    "type": "gather_functional_requirements",
                    "description": "需要收集更多功能需求细节",
                    "suggested_questions": [
                        "系统需要实现哪些具体功能？",
                        "这些功能的优先级是什么？"
                    ]
                })
            elif "非功能需求" in aspect:
                next_steps.append({
                    "type": "gather_non_functional_requirements",
                    "description": "需要明确非功能需求",
                    "suggested_questions": [
                        "系统在性能方面有什么要求？",
                        "有特殊的安全性或可用性要求吗？"
                    ]
                })
            elif "技术栈" in aspect:
                next_steps.append({
                    "type": "clarify_tech_stack",
                    "description": "需要确定技术栈选择",
                    "suggested_questions": [
                        "是否有特定的技术栈偏好？",
                        "系统需要与哪些现有技术或系统集成？"
                    ]
                })
            elif "架构设计" in aspect:
                next_steps.append({
                    "type": "clarify_architecture",
                    "description": "需要明确架构设计方案",
                    "suggested_questions": [
                        "系统需要支持的并发用户数是多少？",
                        "数据量级和增长趋势如何？"
                    ]
                })
        
        return next_steps


def test_requirement_analysis_agent():
    """测试需求分析智能体"""
    # 创建智能体实例
    agent = StepByStepRequirementAnalysisAgent()
    
    # 准备测试消息（初始需求描述）
    test_requirement = "我需要开发一个智能问答系统，能够回答用户关于公司产品的问题，并且能够处理不同语言的请求。"
    
    # 简单测试
    if not USE_QWEN_AGENT:
        # 如果qwen_agent不可用，使用简化版分析方法
        result = agent.analyze_requirement(test_requirement)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 使用分析方法测试
        result = agent.analyze_requirement(test_requirement)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    test_requirement_analysis_agent() 