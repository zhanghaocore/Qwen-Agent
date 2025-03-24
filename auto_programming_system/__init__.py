"""
全自动Python后端编程系统
将自然语言需求转换为可执行Python代码
"""

__version__ = "0.1.0"

from auto_programming_system.requirement_analysis.core import RequirementAnalyzer
from auto_programming_system.code_generation.core import CodeGenerator
from auto_programming_system.execution_validation.core import CodeValidator
from auto_programming_system.optimization.core import CodeOptimizer


class AutoProgrammingSystem:
    """
    全自动编程系统，整合所有模块提供完整功能
    """
    
    def __init__(self, security_level: str = "standard"):
        """
        初始化自动编程系统
        
        Args:
            security_level: 代码执行安全级别 ("relaxed", "standard", "strict")
        """
        self.analyzer = RequirementAnalyzer()
        self.generator = CodeGenerator()
        self.validator = CodeValidator(security_level=security_level)
        self.optimizer = CodeOptimizer()
    
    def process(self, text: str, constraints: list = None) -> dict:
        """
        处理自然语言需求，生成代码
        
        Args:
            text: 自然语言需求描述
            constraints: 额外的约束条件列表
            
        Returns:
            包含生成代码和验证报告的字典
        """
        # 1. 需求分析
        spec = self.analyzer.parse(text)
        
        # 添加额外约束
        if constraints:
            spec["constraints"] = spec.get("constraints", []) + constraints
        
        # 2. 代码生成
        code = self.generator.generate(spec)
        
        # 3. 执行验证
        validation_report = self.validator.validate(code)
        
        # 4. 如果需要，进行代码优化
        if not validation_report["validation_summary"]["all_passed"]:
            code = self.optimizer.optimize(code, validation_report)
            validation_report = self.validator.validate(code)
        
        return {
            "code": code,
            "validation_report": validation_report,
            "specification": spec
        }
