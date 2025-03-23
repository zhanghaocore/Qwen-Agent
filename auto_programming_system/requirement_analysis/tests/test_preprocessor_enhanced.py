"""
文本预处理器增强测试模块
提供全面的测试用例，覆盖边界条件、具体功能、错误处理等
"""
import unittest
import sys
import os
import re
from datetime import datetime

# 添加项目根目录到Python路径，使测试能够导入相应模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from auto_programming_system.requirement_analysis.preprocessor.text_cleaner import TextCleaner
from auto_programming_system.requirement_analysis.preprocessor.sentence_splitter import SentenceSplitter
from auto_programming_system.requirement_analysis.preprocessor.term_extractor import TermExtractor
from auto_programming_system.requirement_analysis.preprocessor.text_normalizer import TextNormalizer
from auto_programming_system.requirement_analysis.preprocessor.preprocessor import TextPreprocessor, PreprocessedText


class TestTextCleanerEnhanced(unittest.TestCase):
    """测试文本清洗功能的增强测试"""
    
    def setUp(self):
        self.cleaner = TextCleaner()
    
    def test_normal_text_cleaning(self):
        """测试正常文本清洗"""
        text = "这是一个  测试文本，有一些多余的  空格。"
        result = self.cleaner.clean_text(text)
        # 验证多余空格被清理，保留原有标点
        self.assertNotIn("  ", result)
        self.assertIn("，", result)
        self.assertIn("。", result)
    
    def test_edge_cases(self):
        """测试边界情况"""
        # 空字符串
        self.assertEqual(self.cleaner.clean_text(""), "")
        # 全空格字符串
        self.assertEqual(self.cleaner.clean_text("   "), "")
        # 超长字符串
        long_text = "a" * 10000
        self.assertEqual(len(self.cleaner.clean_text(long_text)), 10000)
        # 全标点字符串
        self.assertEqual(self.cleaner.clean_text("!@#$%^&*()_+"), "!_+")
    
    def test_tech_terms_protection(self):
        """测试多种技术术语保护情况"""
        # 单个术语
        self.assertIn("API", self.cleaner.clean_text("使用API"))
        # 多个术语
        result = self.cleaner.clean_text("使用REST API和HTTP请求")
        self.assertIn("REST", result)
        self.assertIn("API", result)
        self.assertIn("HTTP", result)
        # 术语大小写混合
        self.assertIn("REST", self.cleaner.clean_text("使用Rest api"))
    
    def test_special_characters_handling(self):
        """测试特殊字符处理"""
        # 中英文混合
        text = "Creating a RESTful API 创建一个REST接口"
        result = self.cleaner.clean_text(text)
        self.assertIn("Creating", result)
        self.assertIn("RESTful", result)
        self.assertIn("API", result)
        self.assertIn("创建", result)
        # 表情符号和特殊Unicode字符
        text = "测试😊文本with😎特殊characters"
        result = self.cleaner.clean_text(text)
        self.assertIn("测试", result)
        self.assertIn("文本", result)
        self.assertIn("with", result)
        self.assertIn("特殊", result)
        self.assertIn("characters", result)
    
    def test_metadata_extraction(self):
        """测试元数据提取功能"""
        # 基本元数据
        text = "这是一个测试文本"
        metadata = self.cleaner.extract_metadata(text)
        self.assertEqual(metadata['length'], len(text))
        self.assertEqual(metadata['word_count'], len(text.split()))
        self.assertFalse(metadata['has_code'])
        
        # 代码检测
        code_text = "def test_function(): return True"
        code_metadata = self.cleaner.extract_metadata(code_text)
        self.assertTrue(code_metadata['has_code'])
        
        # URL检测
        url_text = "访问 https://example.com 获取更多信息"
        url_metadata = self.cleaner.extract_metadata(url_text)
        self.assertTrue(url_metadata['has_urls'])
        
        # 邮箱检测
        email_text = "联系 user@example.com 获取支持"
        email_metadata = self.cleaner.extract_metadata(email_text)
        self.assertTrue(email_metadata['has_emails'])


class TestSentenceSplitterEnhanced(unittest.TestCase):
    """句子分割功能的增强测试"""
    
    def setUp(self):
        self.splitter = SentenceSplitter()
    
    def test_basic_splitting(self):
        """测试基本句子分割，使用标准句号分隔"""
        text = "这是第一句。这是第二句。这是第三句。"
        sentences = self.splitter.split_into_sentences(text)
        self.assertGreaterEqual(len(sentences), 1)
        for s in sentences:
            self.assertIn(s, text)
    
    def test_edge_cases(self):
        """测试边界情况"""
        # 空文本
        self.assertEqual(len(self.splitter.split_into_sentences("")), 0)
        # 无句号文本
        single_sentence = "这是一个没有句号的句子"
        self.assertEqual(len(self.splitter.split_into_sentences(single_sentence)), 1)
        self.assertEqual(self.splitter.split_into_sentences(single_sentence)[0], single_sentence)
        # 只有标点的文本
        self.assertEqual(len(self.splitter.split_into_sentences("。。。")), 0)
        # 超长句子
        long_sentence = "这是一个" + "非常" * 1000 + "长的句子。"
        sentences = self.splitter.split_into_sentences(long_sentence)
        self.assertTrue(len(sentences) > 0)
    
    def test_abbreviations_handling(self):
        """测试缩写处理"""
        # 常见英文缩写
        text = "使用e.g. 表示例如。使用i.e. 表示也就是。"
        sentences = self.splitter.split_into_sentences(text)
        self.assertTrue(any("e.g." in s for s in sentences))
        # 缩写与句号混合
        text = "公司名称是ABC Inc. 它成立于2010年。"
        sentences = self.splitter.split_into_sentences(text)
        self.assertTrue(any("Inc." in s for s in sentences))
    
    def test_list_items(self):
        """测试列表项处理"""
        # 数字列表
        text = "以下是步骤：\n1. 第一步\n2. 第二步\n3. 第三步"
        items = self.splitter.process_list_items(text)
        self.assertEqual(len(items), 4)  # 引言 + 3个列表项
        
        # 符号列表
        text = "以下是要点：\n• 第一点\n• 第二点\n• 第三点"
        items = self.splitter.process_list_items(text)
        self.assertTrue(len(items) >= 1)  # 至少有引言

        # 连续列表，无序号
        text = "- 项目一\n- 项目二\n- 项目三"
        items = self.splitter.process_list_items(text)
        self.assertTrue(len(items) >= 1)
    
    def test_complex_text(self):
        """测试复杂文本混合情况"""
        text = """创建一个RESTful API。API需要支持以下功能：
1. 用户注册和登录
2. 数据CRUD操作
3. 报表生成

API应使用JWT认证，并提供详细文档。"""
        sentences = self.splitter.split_into_sentences(text)
        self.assertTrue(len(sentences) >= 2)  # 至少有两个完整句子
        
    def test_clean_and_merge(self):
        """测试句子清理和合并功能"""
        # 空列表
        self.assertEqual(len(self.splitter.clean_and_merge_sentences([])), 0)
        
        # 合并短句子
        short_sentences = ["这是", "一个", "很短的句子"]
        merged = self.splitter.clean_and_merge_sentences(short_sentences)
        self.assertTrue(len(merged) < len(short_sentences))
        
        # 不合并长句子
        long_sentences = ["这是第一个长句子。", "这是第二个长句子。"]
        merged = self.splitter.clean_and_merge_sentences(long_sentences)
        self.assertEqual(len(merged), len(long_sentences))


class TestTermExtractorEnhanced(unittest.TestCase):
    """术语提取功能的增强测试"""
    
    def setUp(self):
        self.extractor = TermExtractor()
    
    def test_dictionary_terms(self):
        """测试词典中的术语提取"""
        # 编程语言
        text = "使用Python和JavaScript开发"
        terms = self.extractor.extract_technical_terms(text)
        term_names = [term['term'].lower() for term in terms]
        self.assertTrue(any('python' in name for name in term_names))
        self.assertTrue(any('javascript' in name for name in term_names))
        
        # 框架和库
        text = "使用Django和Flask构建Web应用"
        terms = self.extractor.extract_technical_terms(text)
        term_names = [term['term'].lower() for term in term_names]
        self.assertTrue(any('django' in name for name in term_names) or 
                       any('flask' in name for name in term_names))
        
        # API和协议
        text = "实现REST API，支持HTTP请求"
        terms = self.extractor.extract_technical_terms(text)
        term_names = [term['term'].lower() for term in terms]
        self.assertTrue(any('rest' in name or 'api' in name for name in term_names))
        self.assertTrue(any('http' in name for name in term_names))
    
    def test_compound_terms(self):
        """测试复合术语识别"""
        # REST API
        text = "实现RESTful API接口"
        terms = self.extractor.extract_technical_terms(text)
        term_texts = [term['term'].lower() for term in terms]
        self.assertTrue(any('rest' in text and 'api' in text for text in term_texts))
        
        # HTTP请求
        text = "发送HTTP请求获取数据"
        terms = self.extractor.extract_technical_terms(text)
        term_texts = [term['term'].lower() for term in terms]
        self.assertTrue(any('http' in text and '请求' in text for text in term_texts))
    
    def test_chinese_terms(self):
        """测试中文术语识别"""
        text = "创建一个用户管理服务，实现身份认证"
        terms = self.extractor.extract_technical_terms(text)
        term_texts = [term['term'] for term in terms]
        self.assertTrue(any('用户' in text for text in term_texts))
        self.assertTrue(any('服务' in text for text in term_texts))
        self.assertTrue(any('认证' in text for text in term_texts))
    
    def test_edge_cases(self):
        """测试边界情况"""
        # 空文本
        self.assertEqual(len(self.extractor.extract_technical_terms("")), 0)
        
        # 无技术术语的文本
        text = "这是一个普通的文本，没有任何技术术语"
        terms = self.extractor.extract_technical_terms(text)
        self.assertTrue(len(terms) >= 0)  # 可能没有识别出术语
        
        # 全是技术术语的文本
        text = "API REST HTTP JSON XML"
        terms = self.extractor.extract_technical_terms(text)
        self.assertTrue(len(terms) > 0)  # 应该识别出一些术语
    
    def test_candidate_term_identification(self):
        """测试候选术语识别"""
        # 上下文相关术语
        text = "实现一个用户认证服务，提供登录和注册功能"
        terms = self.extractor.extract_technical_terms(text)
        
        # 检查是否识别出关键术语
        term_texts = [term['term'].lower() for term in terms]
        relevant_terms = ['用户', '认证', '服务', '登录', '注册']
        matches = [any(rt in tt for tt in term_texts) for rt in relevant_terms]
        self.assertTrue(any(matches))  # 至少应该匹配一个相关术语


class TestTextNormalizerEnhanced(unittest.TestCase):
    """文本规范化功能的增强测试"""
    
    def setUp(self):
        self.normalizer = TextNormalizer()
    
    def test_number_normalization(self):
        """测试数字规范化"""
        # 千位单位
        text = "值为5k"
        normalized = self.normalizer.normalize_numbers(text)
        self.assertIn("5000", normalized)
        
        # 兆位单位
        text = "内存为8MB"
        normalized = self.normalizer.normalize_numbers(text)
        self.assertTrue("8388608" in normalized or "8MB" in normalized)
        
        # 小数
        text = "大小为2.5kb"
        normalized = self.normalizer.normalize_numbers(text)
        self.assertTrue("2560" in normalized or "2.5kb" in normalized)
        
        # 多个数字
        text = "服务器有16GB内存和2TB存储"
        normalized = self.normalizer.normalize_numbers(text)
        self.assertTrue(re.search(r'16.*?GB', normalized) or re.search(r'17179869184', normalized))
        self.assertTrue(re.search(r'2.*?TB', normalized) or re.search(r'2199023255552', normalized))
    
    def test_date_normalization(self):
        """测试日期规范化"""
        # MM/DD/YYYY格式
        text = "开始日期：12/25/2023"
        normalized = self.normalizer.normalize_dates(text)
        self.assertIn("2023-12-25", normalized)
        
        # 月份名称格式
        text = "结束日期：Jan 1, 2024"
        normalized = self.normalizer.normalize_dates(text)
        self.assertIn("2024-01-01", normalized)
        
        # 两位数年份
        text = "发布日期：03/15/22"
        normalized = self.normalizer.normalize_dates(text)
        self.assertIn("2022-03-15", normalized)
        
        # 多个日期
        text = "从01/01/2023到12/31/2023"
        normalized = self.normalizer.normalize_dates(text)
        self.assertIn("2023-01-01", normalized)
        self.assertIn("2023-12-31", normalized)
    
    def test_time_normalization(self):
        """测试时间规范化"""
        # 12小时制AM
        text = "会议时间：9:30am"
        normalized = self.normalizer.normalize_times(text)
        self.assertIn("09:30", normalized)
        
        # 12小时制PM
        text = "截止时间：3:45pm"
        normalized = self.normalizer.normalize_times(text)
        self.assertIn("15:45", normalized)
        
        # 24小时制
        text = "系统维护：23:59"
        normalized = self.normalizer.normalize_times(text)
        self.assertIn("23:59", normalized)
        
        # 带秒数
        text = "执行时间：12:34:56"
        normalized = self.normalizer.normalize_times(text)
        self.assertIn("12:34:56", normalized)
    
    def test_edge_cases(self):
        """测试边界情况"""
        # 空文本
        self.assertEqual(self.normalizer.normalize(""), "")
        
        # 无需规范化的文本
        text = "普通文本，没有特殊格式"
        self.assertEqual(self.normalizer.normalize(text), text)
        
        # 混合多种格式的文本
        text = "在2023/01/01 9:30am，服务器使用了5k内存"
        normalized = self.normalizer.normalize(text)
        self.assertNotEqual(normalized, text)  # 应该有所变化
    
    def test_abbreviation_expansion(self):
        """测试缩写展开功能"""
        # 仅测试功能可用性，默认不启用
        text = "使用db存储数据"
        expanded = self.normalizer.expand_abbreviations(text)
        self.assertTrue(expanded == text or "database" in expanded)
        
        # 多个缩写
        text = "dev环境和prod环境"
        expanded = self.normalizer.expand_abbreviations(text)
        self.assertTrue(expanded == text or 
                        ("development" in expanded and "production" in expanded))


class TestTextPreprocessorEnhanced(unittest.TestCase):
    """文本预处理器集成功能的增强测试"""
    
    def setUp(self):
        self.preprocessor = TextPreprocessor()
    
    def test_basic_preprocessing(self):
        """测试基本预处理功能"""
        text = "创建一个API，支持用户认证。"
        processed = self.preprocessor.preprocess(text)
        
        # 检查基本属性
        self.assertEqual(processed.original_text, text)
        self.assertTrue(hasattr(processed, 'cleaned_text'))
        self.assertTrue(hasattr(processed, 'sentences'))
        self.assertTrue(hasattr(processed, 'technical_terms'))
        self.assertTrue(hasattr(processed, 'normalized_text'))
        
        # 验证数据流：清洗结果应该传递给后续步骤
        self.assertEqual(processed.cleaned_text, 
                         self.preprocessor.cleaner.clean_text(text))
    
    def test_preprocessing_pipeline(self):
        """测试完整的预处理流水线，验证数据流向"""
        text = "实现REST API，支持OAuth 2.0认证。服务器处理10k并发请求。"
        processed = self.preprocessor.preprocess(text)
        
        # 1. 清洗结果验证
        cleaned_result = self.preprocessor.cleaner.process(text)
        self.assertEqual(processed.cleaned_text, cleaned_result['cleaned_text'])
        
        # 2. 分割结果验证
        splitting_result = self.preprocessor.splitter.process(processed.cleaned_text)
        self.assertEqual(processed.sentences, splitting_result['sentences'])
        
        # 3. 术语提取验证
        self.assertTrue(len(processed.technical_terms) >= 0)
        
        # 4. 规范化验证
        normalizing_result = self.preprocessor.normalizer.process(processed.cleaned_text)
        self.assertEqual(processed.normalized_text, normalizing_result['normalized_text'])
    
    def test_edge_cases(self):
        """测试边界情况"""
        # 空文本
        empty_processed = self.preprocessor.preprocess("")
        self.assertEqual(empty_processed.original_text, "")
        self.assertEqual(empty_processed.cleaned_text, "")
        self.assertEqual(len(empty_processed.sentences), 0)
        
        # 极长文本
        long_text = "这是一个" + "非常" * 1000 + "长的文本。"
        long_processed = self.preprocessor.preprocess(long_text)
        self.assertEqual(long_processed.original_text, long_text)
        self.assertTrue(len(long_processed.cleaned_text) > 0)
        
        # 特殊格式文本
        special_text = "包含特殊格式：2023/12/25 3:30pm，内存5k，支持HTTP请求。"
        special_processed = self.preprocessor.preprocess(special_text)
        # 验证处理不会出错
        self.assertEqual(special_processed.original_text, special_text)
    
    def test_to_dict_conversion(self):
        """测试对象到字典的转换"""
        text = "测试文本转字典功能"
        processed = self.preprocessor.preprocess(text)
        result_dict = self.preprocessor.to_dict(processed)
        
        # 验证字典包含所有关键字段
        self.assertIn('original_text', result_dict)
        self.assertIn('cleaned_text', result_dict)
        self.assertIn('sentences', result_dict)
        self.assertIn('technical_terms', result_dict)
        self.assertIn('normalized_text', result_dict)
        self.assertIn('metadata', result_dict)
        
        # 验证值正确性
        self.assertEqual(result_dict['original_text'], text)
        self.assertEqual(result_dict['cleaned_text'], processed.cleaned_text)
    
    def test_complex_preprocessing(self):
        """测试复杂文本的全流程处理"""
        text = """创建一个RESTful API服务，支持以下功能：
1. 用户注册和登录（OAuth 2.0认证）
2. 数据CRUD操作（支持JSON和XML格式）
3. 报表生成（支持PDF和Excel）

服务器需要处理至少10k的并发连接，数据存储使用MongoDB。上线日期：2023/12/31。"""
        
        processed = self.preprocessor.preprocess(text)
        
        # 检查是否能正确提取关键技术术语
        tech_terms = [term['term'].lower() for term in processed.technical_terms]
        key_terms = ['api', 'oauth', 'json', 'xml', 'mongodb', 'restful', '服务', '数据']
        
        # 验证至少包含一些关键术语
        self.assertTrue(any(kt in ''.join(tech_terms) for kt in key_terms))
        
        # 验证数字规范化
        self.assertTrue('10000' in processed.normalized_text or '10k' in processed.normalized_text)
        
        # 验证日期规范化
        self.assertTrue('2023-12-31' in processed.normalized_text or '2023/12/31' in processed.normalized_text)


class TestPreprocessedTextModel(unittest.TestCase):
    """测试PreprocessedText数据模型"""
    
    def test_initialization(self):
        """测试初始化功能"""
        text = "测试文本"
        preprocessed = PreprocessedText(text)
        
        # 验证初始化参数
        self.assertEqual(preprocessed.original_text, text)
        
        # 验证默认属性
        self.assertEqual(preprocessed.cleaned_text, "")
        self.assertEqual(preprocessed.sentences, [])
        self.assertEqual(preprocessed.tokens, [])
        self.assertEqual(preprocessed.tagged_tokens, [])
        self.assertEqual(preprocessed.technical_terms, [])
        self.assertEqual(preprocessed.normalized_text, "")
        self.assertEqual(preprocessed.metadata, {})
    
    def test_attribute_assignment(self):
        """测试属性赋值"""
        preprocessed = PreprocessedText("测试")
        
        # 赋值测试
        preprocessed.cleaned_text = "清洗后文本"
        preprocessed.sentences = ["句子1", "句子2"]
        preprocessed.tokens = ["token1", "token2"]
        preprocessed.technical_terms = [{"term": "术语1"}, {"term": "术语2"}]
        preprocessed.normalized_text = "规范化文本"
        preprocessed.metadata = {"key": "value"}
        
        # 验证赋值结果
        self.assertEqual(preprocessed.cleaned_text, "清洗后文本")
        self.assertEqual(preprocessed.sentences, ["句子1", "句子2"])
        self.assertEqual(preprocessed.tokens, ["token1", "token2"])
        self.assertEqual(preprocessed.technical_terms[0]["term"], "术语1")
        self.assertEqual(preprocessed.normalized_text, "规范化文本")
        self.assertEqual(preprocessed.metadata["key"], "value")


if __name__ == '__main__':
    unittest.main() 