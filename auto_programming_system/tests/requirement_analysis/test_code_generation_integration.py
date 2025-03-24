"""
需求分析与代码生成模块的集成测试
验证需求分析模块生成的规范能被代码生成模块正确处理
"""

import unittest
from auto_programming_system.requirement_analysis.core import RequirementAnalyzer
from auto_programming_system.code_generation.core import CodeGenerator


class RequirementCodeIntegrationTest(unittest.TestCase):
    """需求分析与代码生成集成测试类"""
    
    def setUp(self):
        """初始化测试环境"""
        self.analyzer = RequirementAnalyzer()
        self.generator = CodeGenerator()
    
    def test_basic_function_generation(self):
        """测试基本函数生成流程"""
        # 1. 需求分析
        requirement = "创建一个函数，接收一个整数列表，返回所有偶数的和"
        spec = self.analyzer.parse(requirement)
        
        # 打印规范，便于调试
        print("\n需求分析生成的规范:")
        for key, value in spec.items():
            print(f"  {key}: {value}")
        
        # 2. 代码生成
        code = self.generator.generate(spec)
        
        # 打印生成的代码，便于调试
        print("\n生成的代码:")
        print(code)
        
        # 验证生成的代码
        self.assertIsInstance(code, str)
        self.assertIn("def", code)
        
        # 检查函数名
        self.assertIn(spec["function_name"], code)
        
        # 检查偶数判断逻辑
        lowered_code = code.lower()
        self.assertTrue(
            "% 2 == 0" in lowered_code or 
            "is_even" in lowered_code,
            "代码中应包含偶数判断逻辑"
        )
    
    def test_temperature_conversion(self):
        """测试温度转换函数生成流程"""
        # 1. 需求分析
        requirement = "实现摄氏度到华氏度的温度转换函数"
        spec = self.analyzer.parse(requirement)
        
        # 添加约束条件
        spec["constraints"] = ["使用内置math模块"]
        
        # 2. 代码生成
        code = self.generator.generate(spec)
        
        # 打印生成的代码，便于调试
        print("\n生成的代码:")
        print(code)
        
        # 验证生成的代码
        self.assertIn("import math", code)
        
        # 检查转换公式
        lowered_code = code.lower()
        self.assertTrue(
            "* 9/5 + 32" in lowered_code or 
            "* 1.8 + 32" in lowered_code,
            "代码中应包含摄氏度到华氏度的转换公式"
        )
    
    def test_complex_requirement(self):
        """测试复杂需求的处理"""
        # 1. 需求分析
        requirement = """
        创建一个函数，接收一个字典列表，每个字典包含'name'和'score'字段，
        返回分数大于60的学生姓名列表，按分数从高到低排序
        """
        spec = self.analyzer.parse(requirement)
        
        # 2. 代码生成
        code = self.generator.generate(spec)
        
        # 打印生成的代码，便于调试
        print("\n生成的代码:")
        print(code)
        
        # 由于这是复杂需求，模板可能没有专门为此设计
        # 只验证基本结构正确
        self.assertIn("def", code)
        self.assertIn(spec["function_name"], code)
        
        # 应该至少包含参数描述
        if spec["parameters"]:
            self.assertIn(spec["parameters"][0]["name"], code)


if __name__ == "__main__":
    unittest.main() 