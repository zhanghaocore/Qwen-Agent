"""
需求分析核心模块的单元测试
"""

import unittest
from auto_programming_system.requirement_analysis.core import RequirementAnalyzer


class RequirementAnalyzerOutputTest(unittest.TestCase):
    """需求分析器输出测试类"""
    
    def setUp(self):
        """初始化测试环境"""
        self.analyzer = RequirementAnalyzer()
    
    def test_function_description_preservation(self):
        """测试函数描述是否保留关键词"""
        text = "创建一个函数，接收一个整数列表，返回所有偶数的和"
        
        result = self.analyzer.parse(text)
        
        # 打印完整规范便于调试
        print("生成的规范:")
        print(result)
        
        # 验证函数描述保留了关键词
        self.assertIn("description", result)
        
        # 检查关键词是否保留（注意中文词汇）
        description = result["description"].lower()
        self.assertTrue("list" in description or "列表" in description, 
                       f"description中应包含'list'或'列表': {description}")
        self.assertTrue("sum" in description or "和" in description,
                       f"description中应包含'sum'或'和': {description}")
        self.assertTrue("even" in description or "偶数" in description,
                       f"description中应包含'even'或'偶数': {description}")


if __name__ == "__main__":
    unittest.main() 