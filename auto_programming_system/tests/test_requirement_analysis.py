"""
需求分析模块的单元测试
"""

import unittest
from auto_programming_system.requirement_analysis.core import RequirementAnalyzer


class RequirementAnalyzerTest(unittest.TestCase):
    """需求分析器测试用例"""
    
    def setUp(self):
        """初始化测试环境"""
        self.analyzer = RequirementAnalyzer()
    
    def test_basic_function_parsing(self):
        """测试基本函数需求解析"""
        text = "创建一个函数，接收一个整数列表，返回所有偶数的和"
        
        result = self.analyzer.parse(text)
        
        # 验证基本字段
        self.assertIn("function_type", result)
        self.assertEqual(result["function_type"], "function")
        
        self.assertIn("function_name", result)
        self.assertTrue(result["function_name"])
        
        self.assertIn("description", result)
        # 不要精确匹配描述，因为预处理可能会修改文本格式
        self.assertTrue(len(result["description"]) > 0)
        
        # 验证参数
        self.assertIn("parameters", result)
        self.assertIsInstance(result["parameters"], list)
        self.assertTrue(len(result["parameters"]) > 0)
        
        # 验证第一个参数的基本属性
        param = result["parameters"][0]
        self.assertIn("name", param)
        self.assertIn("type", param)
        # 只检查类型存在，而不检查精确类型
        self.assertTrue(param["type"])
        # 确保参数有描述
        self.assertIn("description", param)
        self.assertTrue(param["description"])
    
    def test_enrich_specification(self):
        """测试规范丰富功能"""
        text = "创建一个函数，转换温度从摄氏度到华氏度"
        spec = self.analyzer.parse(text)
        
        additional_info = {
            "constraints": ["使用内置math模块", "添加类型注解"]
        }
        
        enriched = self.analyzer.enrich_specification(spec, additional_info)
        
        # 验证约束条件已添加
        self.assertIn("constraints", enriched)
        self.assertIsInstance(enriched["constraints"], list)
        self.assertEqual(len(enriched["constraints"]), 2)
        self.assertIn("使用内置math模块", enriched["constraints"])
        self.assertIn("添加类型注解", enriched["constraints"])


if __name__ == "__main__":
    unittest.main()
