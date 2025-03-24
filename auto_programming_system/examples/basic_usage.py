#!/usr/bin/env python3
"""
基本使用示例 - 全自动Python后端编程系统

本示例展示了系统的基本使用方法，包括：
1. 初始化系统
2. 生成简单函数
3. 验证生成的代码
4. 优化代码
"""

import json
from auto_programming_system import AutoProgrammingSystem, RequirementAnalyzer, CodeGenerator, CodeValidator, CodeOptimizer

def basic_code_generation():
    """展示基本的代码生成功能"""
    # 初始化系统
    system = AutoProgrammingSystem()
    
    # 处理自然语言需求
    requirement = "创建一个函数，接收一个整数列表，返回所有偶数的和"
    result = system.process(requirement)
    
    print("=== 生成的代码 ===")
    print(result["code"])
    
    print("\n=== 验证结果 ===")
    print(f"全部通过: {result['validation_report']['validation_summary']['all_passed']}")
    print(f"通过测试: {result['validation_report']['validation_summary']['passed_tests']}")
    print(f"失败测试: {result['validation_report']['validation_summary']['failed_tests']}")


def manual_pipeline_usage():
    """展示手动使用各个模块的功能"""
    # 初始化需求分析器
    analyzer = RequirementAnalyzer()
    
    # 分析自然语言需求
    requirement = "创建一个函数，接收一个整数列表，返回所有偶数的和"
    spec = analyzer.parse(requirement)
    
    print("=== 需求分析结果 ===")
    print(json.dumps(spec, indent=2, ensure_ascii=False))
    
    # 使用代码生成器生成代码
    generator = CodeGenerator()
    code = generator.generate(spec)
    
    print("\n=== 生成的代码 ===")
    print(code)
    
    # 验证生成的代码
    validator = CodeValidator()
    test_cases = [
        {"inputs": {"numbers": [1, 2, 3, 4, 5]}, "expected": 6},  # 2 + 4 = 6
        {"inputs": {"numbers": [2, 4, 6, 8]}, "expected": 20},    # 全部是偶数
        {"inputs": {"numbers": [1, 3, 5]}, "expected": 0},        # 没有偶数
        {"inputs": {"numbers": []}, "expected": 0}                # 空列表
    ]
    
    validation_report = validator.validate(code, test_cases)
    
    print("\n=== 验证结果 ===")
    print(f"通过测试: {validation_report['validation_summary']['passed_tests']}/{len(test_cases)}")
    
    # 如果有失败的测试，尝试修复代码
    if validation_report['validation_summary']['failed_tests'] > 0:
        print("\n发现问题，尝试修复...")
        optimizer = CodeOptimizer()
        improved_code = optimizer.optimize(code, validation_report)
        
        print("\n=== 改进后的代码 ===")
        print(improved_code)
        
        # 再次验证
        new_validation = validator.validate(improved_code, test_cases)
        print("\n=== 再次验证 ===")
        print(f"通过测试: {new_validation['validation_summary']['passed_tests']}/{len(test_cases)}")


if __name__ == "__main__":
    print("示例1: 使用整合系统")
    print("-" * 50)
    basic_code_generation()
    
    print("\n\n示例2: 手动使用各模块")
    print("-" * 50)
    manual_pipeline_usage()
