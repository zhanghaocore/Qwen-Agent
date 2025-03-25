#!/usr/bin/env python3
"""
多层次需求挖掘Agent测试脚本
验证逐步推理过程和输出质量
"""

import json
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
sys.path.append(str(project_root))

from src.requirement_analysis.advanced_analysis import (
    StepByStepRequirementAnalysisAgent,
    DomainClassifierTool,
    QuestionGeneratorTool,
    TechDecisionAnalyzerTool,
    RequirementSpecGeneratorTool
)

# 测试案例 - 不同复杂度的需求描述
TEST_CASES = [
    {
        "name": "简单Web应用",
        "requirement": "我需要开发一个简单的网站，用于展示公司的产品信息，包括产品介绍、价格和图片。"
    },
    {
        "name": "智能问答系统",
        "requirement": "我需要开发一个智能问答系统，能够回答用户关于公司产品的问题，并且能够处理不同语言的请求。"
    },
    {
        "name": "数据分析平台",
        "requirement": "我需要一个数据分析平台，可以接入多种数据源，对数据进行清洗、分析和可视化，并支持导出报表。同时需要有权限管理功能，不同角色可以查看不同的数据。"
    }
]

def test_domain_classifier():
    """测试领域分类工具"""
    print("\n=== 测试领域分类工具 ===")
    
    domain_classifier = DomainClassifierTool()
    
    for case in TEST_CASES:
        print(f"\n测试用例: {case['name']}")
        result = domain_classifier.call(json.dumps({"requirement_text": case["requirement"]}))
        print(f"领域分类结果: {result}")

def test_question_generator():
    """测试问题生成工具"""
    print("\n=== 测试问题生成工具 ===")
    
    domain_classifier = DomainClassifierTool()
    question_generator = QuestionGeneratorTool()
    
    for case in TEST_CASES:
        print(f"\n测试用例: {case['name']}")
        
        # 先进行领域分类
        domain_result = domain_classifier.call(json.dumps({"requirement_text": case["requirement"]}))
        domain_info = json.loads(domain_result)
        primary_domain = domain_info.get("primary_domain", "通用应用")
        
        # 根据领域生成问题
        questions_result = question_generator.call(
            json.dumps({
                "domain": primary_domain,
                "current_understanding": case["requirement"],
                "discussion_history": ""
            })
        )
        
        print(f"问题生成结果: {questions_result}")

def test_tech_decision_analyzer():
    """测试技术决策分析工具"""
    print("\n=== 测试技术决策分析工具 ===")
    
    domain_classifier = DomainClassifierTool()
    tech_analyzer = TechDecisionAnalyzerTool()
    
    for case in TEST_CASES:
        print(f"\n测试用例: {case['name']}")
        
        # 先进行领域分类
        domain_result = domain_classifier.call(json.dumps({"requirement_text": case["requirement"]}))
        domain_info = json.loads(domain_result)
        primary_domain = domain_info.get("primary_domain", "通用应用")
        
        # 生成技术决策建议
        tech_result = tech_analyzer.call(
            json.dumps({
                "domain": primary_domain,
                "requirements_summary": case["requirement"],
                "technical_constraints": "无特定约束"
            })
        )
        
        print(f"技术决策分析结果摘要:")
        tech_data = json.loads(tech_result)
        print(f"- 决策点数量: {len(tech_data.get('decision_points', []))}")
        print(f"- 推荐技术数量: {len(tech_data.get('tech_recommendations', {}))}")
        print(f"- 架构类型: {tech_data.get('architecture_recommendation', {}).get('架构类型', '未指定')}")

def test_requirement_spec_generator():
    """测试需求规范生成工具"""
    print("\n=== 测试需求规范生成工具 ===")
    
    domain_classifier = DomainClassifierTool()
    tech_analyzer = TechDecisionAnalyzerTool()
    spec_generator = RequirementSpecGeneratorTool()
    
    # 仅测试第一个案例以节省输出
    case = TEST_CASES[0]
    print(f"\n测试用例: {case['name']}")
    
    # 先进行领域分类
    domain_result = domain_classifier.call(json.dumps({"requirement_text": case["requirement"]}))
    domain_info = json.loads(domain_result)
    primary_domain = domain_info.get("primary_domain", "通用应用")
    
    # 生成技术决策建议
    tech_result = tech_analyzer.call(
        json.dumps({
            "domain": primary_domain,
            "requirements_summary": case["requirement"],
            "technical_constraints": "无特定约束"
        })
    )
    
    # 生成需求规范
    spec_result = spec_generator.call(
        json.dumps({
            "domain": primary_domain,
            "discussion_summary": case["requirement"],
            "tech_decisions": tech_result
        })
    )
    
    print(f"需求规范生成结果摘要:")
    spec_data = json.loads(spec_result)
    doc = spec_data.get("需求规范文档", {})
    print(f"- 文档版本: {doc.get('文档信息', {}).get('版本', '未指定')}")
    print(f"- 项目名称: {doc.get('项目概述', {}).get('项目名称', '未指定')}")
    print(f"- 功能需求数量: {len(doc.get('功能需求', []))}")
    print(f"- 非功能需求数量: {len(doc.get('非功能需求', []))}")

def test_full_agent():
    """测试完整的智能体流程"""
    print("\n=== 测试完整的智能体流程 ===")
    
    try:
        # 创建智能体实例
        agent = StepByStepRequirementAnalysisAgent()
        
        # 测试用例1：初始需求分析
        case = TEST_CASES[0]
        print(f"\n测试用例1 - 初始需求: {case['name']}")
        
        result = agent.analyze_requirement(case["requirement"])
        
        print("\n初始需求分析结果摘要:")
        domain_analysis = result.get('domain_analysis') if isinstance(result, dict) else {}
        if isinstance(domain_analysis, dict):
            print(f"- 识别的领域: {domain_analysis.get('primary_domain', '未知')}")
        else:
            print("- 识别的领域: 未知")
            
        print(f"- 当前对话阶段: {result.get('discussion_stage', '未知') if isinstance(result, dict) else '未知'}")
        print(f"- 下一步问题数量: {len(result.get('next_questions', [])) if isinstance(result, dict) else 0}")
        
        completeness_analysis = result.get('completeness_analysis') if isinstance(result, dict) else {}
        missing_aspects = completeness_analysis.get('missing_aspects', []) if isinstance(completeness_analysis, dict) else []
        print(f"- 缺失的方面: {', '.join(missing_aspects)}")
        
        # 测试用例2：多轮对话
        print("\n测试用例2 - 多轮对话")
        discussion_history = [
            {"role": "user", "content": case["requirement"]},
            {"role": "assistant", "content": "这个项目听起来是一个企业展示网站。我需要了解一些具体细节：1. 产品信息需要多久更新一次？2. 是否需要多语言支持？"},
            {"role": "user", "content": "产品信息每周更新一次，需要支持中英文。必须使用React框架开发前端，后端性能要求是并发用户1000以上。"}
        ]
        
        result = agent.analyze_requirement(
            "另外，我们需要一个产品搜索功能，可以按照价格区间和类别筛选。",
            discussion_history
        )
        
        print("\n多轮对话分析结果摘要:")
        if isinstance(result, dict):
            current_understanding = result.get('current_understanding', '')
            print(f"- 当前理解的需求长度: {len(current_understanding)}")
            
            tech_analysis = result.get('tech_analysis', {})
            if isinstance(tech_analysis, dict):
                tech_recommendations = tech_analysis.get('tech_recommendations', {})
                if isinstance(tech_recommendations, dict):
                    print(f"- 识别的技术约束: {list(tech_recommendations.keys())}")
                else:
                    print("- 识别的技术约束: []")
            
            print(f"- 下一步建议:")
            next_steps = result.get('next_steps', [])
            if isinstance(next_steps, list):
                for step in next_steps:
                    if isinstance(step, dict):
                        print(f"  * {step.get('description', '')}")
            
        # 测试用例3：完整性检查
        print("\n测试用例3 - 完整性检查")
        if isinstance(result, dict):
            completeness = result.get('completeness_analysis', {})
            if isinstance(completeness, dict):
                domain_clarity = completeness.get('domain_clarity', {})
                requirement_coverage = completeness.get('requirement_coverage', {})
                tech_decision_clarity = completeness.get('tech_decision_clarity', {})
                
                print("\n完整性分析结果:")
                if isinstance(domain_clarity, dict):
                    print(f"- 领域清晰度: {'清晰' if domain_clarity.get('is_clear') else '不清晰'}")
                if isinstance(requirement_coverage, dict):
                    print(f"- 需求覆盖度: {'完整' if requirement_coverage.get('is_complete') else '不完整'}")
                if isinstance(tech_decision_clarity, dict):
                    print(f"- 技术决策清晰度: {'清晰' if tech_decision_clarity.get('is_clear') else '不清晰'}")
        
    except Exception as e:
        print(f"测试失败: {str(e)}")

if __name__ == "__main__":
    # 按照工具链顺序测试各个组件
    test_domain_classifier()
    test_question_generator()
    test_tech_decision_analyzer()
    test_requirement_spec_generator()
    test_full_agent() 