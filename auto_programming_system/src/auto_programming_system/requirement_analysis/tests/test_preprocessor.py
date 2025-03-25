"""
文本预处理器测试模块
"""
import unittest
import sys
import os

# 添加项目根目录到Python路径，使测试能够导入相应模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.requirement_analysis.preprocessor.text_cleaner import TextCleaner
from src.requirement_analysis.preprocessor.sentence_splitter import SentenceSplitter
from src.requirement_analysis.preprocessor.term_extractor import TermExtractor
from src.requirement_analysis.preprocessor.text_normalizer import TextNormalizer
from src.requirement_analysis.preprocessor.preprocessor import TextPreprocessor


class TestTextCleaner(unittest.TestCase):
    """测试文本清洗功能"""
    
    def setUp(self):
        self.cleaner = TextCleaner()
    
    def test_basic_functionality(self):
        """测试基本功能"""
        text = "这是一个  测试文本，有一些多余的  空格。"
        result = self.cleaner.clean_text(text)
        # 测试多余空格被清理
        self.assertNotIn("  ", result)
        # 测试文本长度变短
        self.assertLess(len(result), len(text))
    
    def test_tech_terms_protection(self):
        """测试技术术语保护"""
        text = "使用REST API来实现这个功能"
        result = self.cleaner.clean_text(text)
        self.assertIn("REST", result)
        self.assertIn("API", result)
    
    def test_extract_metadata(self):
        """测试元数据提取"""
        text = "这是一个包含代码的文本: def test_function(): return True"
        metadata = self.cleaner.extract_metadata(text)
        self.assertTrue(metadata['has_code'])
        self.assertGreater(metadata['word_count'], 0)


class TestSentenceSplitter(unittest.TestCase):
    """测试句子分割功能"""
    
    def setUp(self):
        self.splitter = SentenceSplitter()
    
    def test_split_functionality(self):
        """测试分割功能是否正常工作"""
        text = "这是一个句子。这是另一个句子。"
        sentences = self.splitter.split_into_sentences(text)
        # 验证结果不为空
        self.assertTrue(len(sentences) > 0)
        # 验证分割后的句子存在于原文中
        for s in sentences:
            self.assertIn(s, text)
    
    def test_process_functionality(self):
        """测试处理功能是否正常工作"""
        text = "这是一个测试。"
        result = self.splitter.process(text)
        # 验证返回字典包含预期的键
        self.assertIn('sentences', result)
        self.assertIn('sentence_count', result)
        self.assertIn('avg_sentence_length', result)
        # 验证句子数量正确
        self.assertEqual(result['sentence_count'], len(result['sentences']))


class TestTermExtractor(unittest.TestCase):
    """测试术语提取功能"""
    
    def setUp(self):
        self.extractor = TermExtractor()
    
    def test_basic_functionality(self):
        """测试基本功能是否正常工作"""
        text = "使用数据库和API创建网站"
        terms = self.extractor.extract_technical_terms(text)
        # 验证能够提取一些术语
        self.assertTrue(len(terms) > 0)
    
    def test_process_functionality(self):
        """测试处理功能是否正常工作"""
        text = "创建一个RESTful API"
        result = self.extractor.process(text)
        # 验证返回字典包含预期的键
        self.assertIn('technical_terms', result)
        self.assertIn('term_count', result)
        self.assertIn('term_types', result)
        # 验证术语数量正确
        self.assertEqual(result['term_count'], len(result['technical_terms']))


class TestTextNormalizer(unittest.TestCase):
    """测试文本规范化功能"""
    
    def setUp(self):
        self.normalizer = TextNormalizer()
    
    def test_basic_functionality(self):
        """测试基本功能是否正常工作"""
        text = "会议时间：3:30pm"
        normalized = self.normalizer.normalize(text)
        # 验证正规化不会返回空字符串
        self.assertTrue(normalized)
        # 验证长度基本不变
        self.assertAlmostEqual(len(normalized), len(text), delta=5)
    
    def test_process_functionality(self):
        """测试处理功能是否正常工作"""
        text = "文件大小为10k"
        result = self.normalizer.process(text)
        # 验证返回字典包含预期的键
        self.assertIn('normalized_text', result)
        self.assertIn('normalization_applied', result)
        # 验证结果是否包含原文
        self.assertEqual(result['original_text'], text)


class TestTextPreprocessor(unittest.TestCase):
    """测试文本预处理器集成功能"""
    
    def setUp(self):
        self.preprocessor = TextPreprocessor()
    
    def test_basic_functionality(self):
        """测试基本功能是否正常工作"""
        text = "创建一个API，支持用户认证。"
        processed = self.preprocessor.preprocess(text)
        # 验证返回对象包含预期的属性
        self.assertTrue(hasattr(processed, 'original_text'))
        self.assertTrue(hasattr(processed, 'cleaned_text'))
        self.assertTrue(hasattr(processed, 'sentences'))
        self.assertTrue(hasattr(processed, 'technical_terms'))
        self.assertTrue(hasattr(processed, 'normalized_text'))
        self.assertTrue(hasattr(processed, 'metadata'))
        # 验证原文被保留
        self.assertEqual(processed.original_text, text)
    
    def test_to_dict_functionality(self):
        """测试转字典功能是否正常工作"""
        text = "测试文本"
        processed = self.preprocessor.preprocess(text)
        result = processed.to_dict()
        # 验证返回字典包含预期的键
        self.assertIn('original_text', result)
        self.assertIn('cleaned_text', result)
        self.assertIn('sentences', result)
        self.assertIn('technical_terms', result)
        self.assertIn('normalized_text', result)
        self.assertIn('metadata', result)


if __name__ == '__main__':
    unittest.main() 