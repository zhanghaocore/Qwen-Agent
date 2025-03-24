"""
Benchmark tests for the semantic analyzer module.

This module contains performance tests for the semantic analyzer components,
focusing on parameter extraction, type inference, and requirement analysis.
"""

import pytest
from pathlib import Path
from typing import List, Dict, Any

from auto_programming_system.requirement_analysis.semantic_analyzer.analyzer import SemanticAnalyzer
from auto_programming_system.requirement_analysis.semantic_analyzer.parameter_extractor import ParameterExtractor
from auto_programming_system.requirement_analysis.semantic_analyzer.type_inference import TypeInferenceSystem
from auto_programming_system.requirement_analysis.semantic_analyzer.requirement_analyzer import RequirementAnalyzer

from . import (
    PerformanceMetrics,
    SMALL_CASES_DIR,
    MEDIUM_CASES_DIR,
    LARGE_CASES_DIR
)
from .performance_metrics import PerformanceAnalyzer, MetricsCollector

# Initialize performance analyzer
analyzer = PerformanceAnalyzer(output_dir="performance_reports/semantic_analyzer")
collector = MetricsCollector(analyzer)

@pytest.fixture
def semantic_analyzer():
    """Create a SemanticAnalyzer instance for testing."""
    return SemanticAnalyzer()

def load_test_data(data_dir: Path) -> List[str]:
    """Load test data from the specified directory."""
    test_data = []
    for file in data_dir.glob("*.txt"):
        with open(file, 'r', encoding='utf-8') as f:
            test_data.append(f.read())
    return test_data

@pytest.mark.benchmark
class TestSemanticAnalyzerPerformance:
    """Performance tests for the semantic analyzer module."""

    def test_small_cases(self, semantic_analyzer):
        """Test semantic analyzer performance with small input texts."""
        test_data = load_test_data(SMALL_CASES_DIR)
        
        collector.start_collection("semantic_analyzer_small_cases")
        for text in test_data:
            semantic_analyzer.analyze(text)
        collector.end_collection({
            'num_cases': len(test_data),
            'avg_text_length': sum(len(t) for t in test_data) / len(test_data)
        })

    def test_medium_cases(self, semantic_analyzer):
        """Test semantic analyzer performance with medium-sized input texts."""
        test_data = load_test_data(MEDIUM_CASES_DIR)
        
        collector.start_collection("semantic_analyzer_medium_cases")
        for text in test_data:
            semantic_analyzer.analyze(text)
        collector.end_collection({
            'num_cases': len(test_data),
            'avg_text_length': sum(len(t) for t in test_data) / len(test_data)
        })

    def test_large_cases(self, semantic_analyzer):
        """Test semantic analyzer performance with large input texts."""
        test_data = load_test_data(LARGE_CASES_DIR)
        
        collector.start_collection("semantic_analyzer_large_cases")
        for text in test_data:
            semantic_analyzer.analyze(text)
        collector.end_collection({
            'num_cases': len(test_data),
            'avg_text_length': sum(len(t) for t in test_data) / len(test_data)
        })

    def test_component_performance(self, semantic_analyzer):
        """Test individual component performance."""
        test_data = load_test_data(MEDIUM_CASES_DIR)
        components = {
            'parameter_extractor': ParameterExtractor(),
            'type_inference': TypeInferenceSystem(),
            'requirement_analyzer': RequirementAnalyzer()
        }

        for name, component in components.items():
            collector.start_collection(f"component_{name}")
            for text in test_data:
                if hasattr(component, 'analyze'):
                    component.analyze(text)
                elif hasattr(component, 'extract'):
                    component.extract(text)
                elif hasattr(component, 'infer'):
                    component.infer(text)
            collector.end_collection({
                'component': name,
                'num_cases': len(test_data)
            })

    def test_chinese_text_processing(self, semantic_analyzer):
        """Test performance with Chinese text processing."""
        test_data = [
            "创建一个函数，接收一个整数列表，返回所有偶数的和。",
            "实现一个API端点，用于处理用户登录请求，需要验证用户名和密码。",
            "开发一个数据处理函数，将CSV文件转换为JSON格式，要处理中文字符。"
        ]

        collector.start_collection("chinese_text_processing")
        for text in test_data:
            semantic_analyzer.analyze(text)
        collector.end_collection({
            'num_cases': len(test_data),
            'language': 'Chinese'
        })

    def test_mixed_language_processing(self, semantic_analyzer):
        """Test performance with mixed language text processing."""
        test_data = [
            "Create a function to process数据，返回JSON格式的结果。",
            "Implement an API endpoint处理用户请求，support分页查询。",
            "开发一个machine learning模型训练函数，使用TensorFlow框架。"
        ]

        collector.start_collection("mixed_language_processing")
        for text in test_data:
            semantic_analyzer.analyze(text)
        collector.end_collection({
            'num_cases': len(test_data),
            'language': 'Mixed'
        })

    def test_concurrent_analysis(self, semantic_analyzer):
        """Test semantic analyzer performance with concurrent processing."""
        import concurrent.futures
        import multiprocessing

        test_data = load_test_data(MEDIUM_CASES_DIR)
        num_workers = multiprocessing.cpu_count()

        collector.start_collection("semantic_analyzer_concurrent")
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(semantic_analyzer.analyze, text) for text in test_data]
            concurrent.futures.wait(futures)
        collector.end_collection({
            'num_workers': num_workers,
            'num_cases': len(test_data)
        })

    def test_type_inference_performance(self, semantic_analyzer):
        """Test type inference system performance."""
        test_cases = [
            "一个整数列表",
            "包含字符串的数组",
            "List[Dict[str, Any]]类型的参数",
            "返回Optional[float]类型",
            "接收一个Callable[[int, str], bool]参数"
        ]

        collector.start_collection("type_inference_performance")
        for case in test_cases:
            semantic_analyzer.infer_type(case)
        collector.end_collection({
            'num_cases': len(test_cases),
            'test_type': 'type_inference'
        })

    @classmethod
    def teardown_class(cls):
        """Generate performance report after all tests are complete."""
        analyzer.generate_report("semantic_analyzer_benchmark_report.json")

if __name__ == '__main__':
    pytest.main(['-v', __file__]) 