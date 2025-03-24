#!/usr/bin/env python3
"""
全自动Python后端编程系统 - 主入口点
用于处理命令行参数和执行主流程
"""

import argparse
import sys
import json
from typing import Dict, Any, List, Optional

try:
    from auto_programming_system.requirement_analysis.core import RequirementAnalyzer
    from auto_programming_system.code_generation.core import CodeGenerator
    from auto_programming_system.execution_validation.core import CodeValidator
    from auto_programming_system.optimization.core import CodeOptimizer
except ImportError:
    print("无法导入核心模块。请确保已安装依赖项。")
    sys.exit(1)


def parse_arguments() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="全自动Python后端编程系统 - 将自然语言需求转换为Python代码"
    )
    
    parser.add_argument(
        "--input", "-i", type=str, required=True,
        help="自然语言需求描述"
    )
    
    parser.add_argument(
        "--constraints", "-c", type=str, default="",
        help="代码生成约束，多个约束用逗号分隔"
    )
    
    parser.add_argument(
        "--output", "-o", type=str, default="",
        help="输出文件路径，默认打印到标准输出"
    )
    
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="启用详细输出模式"
    )
    
    parser.add_argument(
        "--security", "-s", choices=["relaxed", "standard", "strict"], default="standard",
        help="代码执行安全级别"
    )
    
    return parser.parse_args()


def process_input(args: argparse.Namespace) -> Dict[str, Any]:
    """处理输入并执行完整流程"""
    if args.verbose:
        print(f"正在处理需求: {args.input}")
        print(f"约束条件: {args.constraints}")
    
    # 1. 需求分析
    analyzer = RequirementAnalyzer()
    requirement_spec = analyzer.parse(args.input)
    
    if args.constraints:
        constraint_list = [c.strip() for c in args.constraints.split(",")]
        requirement_spec["constraints"] = constraint_list
    
    if args.verbose:
        print("\n=== 需求分析结果 ===")
        print(json.dumps(requirement_spec, indent=2, ensure_ascii=False))
    
    # 2. 代码生成
    generator = CodeGenerator()
    code = generator.generate(requirement_spec)
    
    if args.verbose:
        print("\n=== 生成的代码 ===")
        print(code)
    
    # 3. 执行验证
    validator = CodeValidator(security_level=args.security)
    validation_report = validator.validate(code)
    
    if args.verbose:
        print("\n=== 验证结果 ===")
        print(json.dumps(validation_report, indent=2, ensure_ascii=False))
    
    # 4. 迭代优化（如果验证未通过）
    if not validation_report["validation_summary"]["all_passed"]:
        if args.verbose:
            print("\n=== 进行代码优化 ===")
        
        optimizer = CodeOptimizer()
        code = optimizer.optimize(code, validation_report)
        
        if args.verbose:
            print("\n=== 优化后的代码 ===")
            print(code)
        
        # 再次验证
        validation_report = validator.validate(code)
        
        if args.verbose:
            print("\n=== 再次验证结果 ===")
            print(json.dumps(validation_report, indent=2, ensure_ascii=False))
    
    # 返回结果
    return {
        "code": code,
        "validation_report": validation_report
    }


def main() -> None:
    """主函数"""
    args = parse_arguments()
    
    try:
        result = process_input(args)
        
        # 输出结果
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(result["code"])
            print(f"代码已保存到: {args.output}")
        else:
            print(result["code"])
        
        # 检查验证结果
        if not result["validation_report"]["validation_summary"]["all_passed"]:
            print("\n警告: 生成的代码可能存在问题, 请查看验证报告了解详情。", file=sys.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
