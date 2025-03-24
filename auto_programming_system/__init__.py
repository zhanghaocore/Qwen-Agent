"""
全自动Python后端编程系统
将自然语言需求转换为可执行Python代码
"""

__version__ = "0.1.0"

from typing import Dict, Any, List, Optional
from auto_programming_system.requirement_analysis.core import RequirementAnalyzer
from auto_programming_system.code_generation.core import CodeGenerator
from auto_programming_system.execution_validation.core import CodeValidator
from auto_programming_system.optimization.core import CodeOptimizer


class AutoProgrammingSystem:
    """
    全自动编程系统，整合所有模块提供完整功能
    """
    
    def __init__(self, 
                 security_level: str = "standard",
                 optimization_config: Optional[Dict[str, Any]] = None,
                 execution_sandbox: Optional[Dict[str, Any]] = None):
        """
        初始化自动编程系统
        
        Args:
            security_level: 代码执行安全级别 ("relaxed", "standard", "strict")
            optimization_config: 优化配置参数
            execution_sandbox: 执行沙箱配置
        """
        self.analyzer = RequirementAnalyzer()
        self.generator = CodeGenerator()
        self.validator = CodeValidator(security_level=security_level)
        self.optimizer = CodeOptimizer(max_optimization_rounds=optimization_config.get("max_rounds", 3)) if optimization_config else CodeOptimizer()
        self.sandbox = execution_sandbox
    
    def process(self, text: str, constraints: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        处理自然语言需求，生成代码
        
        Args:
            text: 自然语言需求描述
            constraints: 额外的约束条件列表
            
        Returns:
            包含生成代码和验证报告的字典
        """
        constraints = constraints or []
        
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
    
    def build(self, user_input: str, max_iter: int = 3, constraints: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        一站式构建代码，包含多轮优化
        
        Args:
            user_input: 用户输入的需求描述
            max_iter: 最大优化迭代次数
            constraints: 代码约束条件
            
        Returns:
            包含最终代码和优化历史的字典
        """
        optimization_history = []
        current_result = self.process(user_input, constraints)
        optimization_history.append({
            'code': current_result['code'],
            'metrics': current_result['validation_report']
        })
        
        # 进行多轮优化
        for i in range(max_iter - 1):
            if current_result['validation_report']['validation_summary']['all_passed']:
                break
                
            current_result = self.process(user_input, constraints)
            optimization_history.append({
                'code': current_result['code'],
                'metrics': current_result['validation_report']
            })
        
        return {
            'final_code': current_result['code'],
            'validation_report': current_result['validation_report'],
            'optimization_history': optimization_history
        }
    
    def build_from_document(self, doc_path: str) -> Dict[str, Any]:
        """
        从文档生成代码
        
        Args:
            doc_path: 需求文档路径
            
        Returns:
            包含生成的代码文件的字典
        """
        with open(doc_path, 'r', encoding='utf-8') as f:
            doc_content = f.read()
            
        # 解析文档内容
        spec = self.analyzer.parse(doc_content)  # 使用普通的 parse 方法，不再使用 parse_document
        
        # 生成代码
        code = self.generator.generate(spec)  # 使用普通的 generate 方法，不再使用 generate_project
        
        # 验证生成的代码
        validation_result = self.validator.validate(code)
        
        return {
            'generated_code': code,
            'validation_result': validation_result,
            'specification': spec
        }
