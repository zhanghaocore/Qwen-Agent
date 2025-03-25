"""
全自动编程系统集成测试
"""

import unittest
import json
from src import AutoProgrammingSystem


class IntegrationTest(unittest.TestCase):
    """集成测试用例"""
    
    def setUp(self):
        """初始化测试环境"""
        self.system = AutoProgrammingSystem()
    
    def test_basic_function_generation(self):
        """测试基本函数生成"""
        requirement = "创建一个函数，接收一个整数列表，返回所有偶数的和"
        
        result = self.system.process(requirement)
        
        # 验证结果包含代码和其他必要字段
        self.assertIn("code", result)
        self.assertIn("validation_report", result)
        self.assertIn("specification", result)
        self.assertIsInstance(result["code"], str)
        
        # 打印实际生成的代码，便于调试
        print("\n实际生成的代码:")
        print(result["code"])
        
        # 基本代码结构验证
        self.assertIn("def", result["code"])  # 确保包含函数定义
        
        # 从规范中获取函数名
        function_name = result["specification"]["function_name"]
        self.assertIn(function_name, result["code"])  # 验证函数名被正确使用
        
        # 验证代码逻辑 - 检测包含最基本的功能约束
        # 注意：这种验证比检查特定操作符更加灵活
        lowered_code = result["code"].lower()
        
        # 偶数判断可能会用不同方式实现
        self.assertTrue(
            "% 2 == 0" in lowered_code or 
            "is_even" in lowered_code or 
            "iseven" in lowered_code or
            "偶数" in lowered_code,
            "代码中应包含偶数判断逻辑"
        )
        
        # 求和操作可能有多种实现方式
        self.assertTrue(
            "sum" in lowered_code or 
            "+=" in lowered_code or 
            "total" in lowered_code or
            "result" in lowered_code,
            "代码中应包含求和操作"
        )
        
        # 检查所需的参数类型
        self.assertIn("list", lowered_code)  # 应该提到列表参数
    
    def test_with_constraints(self):
        """测试带约束条件的代码生成"""
        requirement = "创建一个函数，转换温度从摄氏度到华氏度"
        constraints = ["使用内置math模块", "添加类型注解"]
        
        result = self.system.process(requirement, constraints)
        
        # 打印实际生成的代码，便于调试
        print("\n实际生成的代码:")
        print(result["code"])
        
        # 验证结果包含代码
        self.assertIn("code", result)
        
        # 验证代码中包含math模块导入
        self.assertIn("import math", result["code"])
        
        # 验证代码中包含类型注解
        self.assertIn(":", result["code"])
        self.assertIn("->", result["code"])
        
        # 验证代码中包含转换公式
        lowered_code = result["code"].lower()
        self.assertTrue(
            "* 9/5 + 32" in lowered_code or 
            "× 9/5 + 32" in lowered_code or
            "celsius * 1.8 + 32" in lowered_code,
            "代码中应包含摄氏度到华氏度的转换公式"
        )


if __name__ == "__main__":
    unittest.main() 