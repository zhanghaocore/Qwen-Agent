"""
语义分析器模块的单元测试
设计全面的测试用例提高代码覆盖率
"""

import unittest
from src.requirement_analysis.semantic_analyzer.analyzer import SemanticAnalyzer


class SemanticAnalyzerTest(unittest.TestCase):
    """语义分析器测试类"""
    
    def setUp(self):
        """初始化测试环境"""
        self.analyzer = SemanticAnalyzer()
    
    def test_analyze_basic(self):
        """测试基本分析功能"""
        text = "创建一个函数，接收一个整数列表，返回所有偶数的和"
        
        result = self.analyzer.analyze(text)
        
        # 验证基本结构
        self.assertEqual(result["function_type"], "function")
        self.assertEqual(result["description"], text)
        self.assertIsInstance(result["parameters"], list)
        self.assertEqual(result["return_type"], "Any")
        self.assertEqual(result["return_description"], "函数返回值")
    
    def test_analyze_with_original_text(self):
        """测试使用原始文本作为描述"""
        text = "接收整数列表，返回偶数和"
        original_text = "创建一个处理数字的函数，接收整数列表，返回偶数和"
        
        result = self.analyzer.analyze(text, original_text)
        
        # 验证使用了原始文本作为描述
        self.assertEqual(result["description"], original_text)
    
    def test_analyze_no_parameters(self):
        """测试没有参数的情况"""
        text = "创建一个函数，返回当前时间"
        
        result = self.analyzer.analyze(text)
        
        # 验证参数为空列表（因为没有"接收"关键词）
        self.assertEqual(result["parameters"], [])
    
    def test_analyze_single_parameter(self):
        """测试单个参数的情况"""
        text = "创建一个函数，接收整数，返回其平方"
        
        result = self.analyzer.analyze(text)
        
        # 验证单个参数
        self.assertEqual(len(result["parameters"]), 1)
        self.assertEqual(result["parameters"][0]["name"], "param1")
        self.assertEqual(result["parameters"][0]["type"], "int")
        self.assertEqual(result["parameters"][0]["description"], "整数")
    
    def test_analyze_multiple_parameters(self):
        """测试多个参数的情况"""
        text = "创建一个函数，接收整数，字符串，返回组合结果"
        
        result = self.analyzer.analyze(text)
        
        # 验证两个参数
        self.assertEqual(len(result["parameters"]), 2)
        self.assertEqual(result["parameters"][0]["name"], "param1")
        self.assertEqual(result["parameters"][0]["type"], "int")
        self.assertEqual(result["parameters"][0]["description"], "整数")
        self.assertEqual(result["parameters"][1]["name"], "param2")
        self.assertEqual(result["parameters"][1]["type"], "str")
        self.assertEqual(result["parameters"][1]["description"], "字符串")
    
    def test_analyze_parameter_types(self):
        """测试各种参数类型的识别"""
        # 测试整数类型
        text = "创建一个函数，接收整数返回结果"
        result = self.analyzer.analyze(text)
        self.assertEqual(result["parameters"][0]["type"], "int")
        
        # 测试数字类型
        text = "创建一个函数，接收数字返回结果"
        result = self.analyzer.analyze(text)
        self.assertEqual(result["parameters"][0]["type"], "int")
        
        # 测试列表类型
        text = "创建一个函数，接收列表返回结果"
        result = self.analyzer.analyze(text)
        self.assertEqual(result["parameters"][0]["type"], "List")
        
        # 测试数组类型
        text = "创建一个函数，接收数组返回结果"
        result = self.analyzer.analyze(text)
        self.assertEqual(result["parameters"][0]["type"], "List")
        
        # 测试默认字符串类型
        text = "创建一个函数，接收名称返回结果"
        result = self.analyzer.analyze(text)
        self.assertEqual(result["parameters"][0]["type"], "str")
    
    def test_analyze_complex_case(self):
        """测试复杂需求的分析"""
        text = """创建一个函数，接收用户ID和商品ID列表，返回购物车对象"""
        
        result = self.analyzer.analyze(text)
        
        # 目前的实现会将"接收用户ID和商品ID列表"作为一个整体参数
        # 验证至少能提取基本信息而不崩溃
        self.assertEqual(result["function_type"], "function")
        self.assertEqual(result["description"], text)
        # 验证参数解析
        self.assertGreaterEqual(len(result["parameters"]), 1)
    
    def test_analyze_chinese_comma(self):
        """测试中文逗号分隔的参数"""
        text = "创建一个函数，接收整数，字符串，布尔值，返回组合结果"
        
        result = self.analyzer.analyze(text)
        
        # 当前实现会解析中文逗号分隔的参数
        self.assertEqual(len(result["parameters"]), 3)  # 修正为3个参数
        self.assertEqual(result["parameters"][0]["type"], "int")
        self.assertEqual(result["parameters"][0]["description"], "整数")
        self.assertEqual(result["parameters"][1]["type"], "str")
        self.assertEqual(result["parameters"][1]["description"], "字符串")
        self.assertEqual(result["parameters"][2]["type"], "bool")  # 修正为bool类型
        self.assertEqual(result["parameters"][2]["description"], "布尔值")


if __name__ == "__main__":
    unittest.main() 