"""
全自动编程系统集成测试
"""

import unittest
import json
from auto_programming_system import AutoProgrammingSystem


class IntegrationTest(unittest.TestCase):
    """集成测试用例"""
    
    def setUp(self):
        """初始化测试环境"""
        self.system = AutoProgrammingSystem()
    
    def test_basic_function_generation(self):
        """测试基本函数生成"""
        requirement = "创建一个函数，接收一个整数列表，返回所有偶数的和"
        
        result = self.system.process(requirement)
        
        # 验证结果包含代码
        self.assertIn("code", result)
        self.assertIsInstance(result["code"], str)
        
        # 验证代码中包含函数定义
        self.assertIn("def", result["code"])
        
        # 验证代码中包含偶数判断
        self.assertIn("%", result["code"])
        
        # 验证代码中包含求和操作
        self.assertIn("sum", result["code"])
    
    def test_with_constraints(self):
        """测试带约束条件的代码生成"""
        requirement = "创建一个函数，转换温度从摄氏度到华氏度"
        constraints = ["使用内置math模块", "添加类型注解"]
        
        result = self.system.process(requirement, constraints)
        
        # 验证结果包含代码
        self.assertIn("code", result)
        
        # 验证代码中包含math模块导入
        self.assertIn("import math", result["code"])
        
        # 验证代码中包含类型注解
        self.assertIn(":", result["code"])
        self.assertIn("->", result["code"])


if __name__ == "__main__":
    unittest.main() 