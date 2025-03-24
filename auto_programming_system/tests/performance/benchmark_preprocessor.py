"""
Benchmark tests for the preprocessor module.

This module contains performance tests for the text preprocessor components,
including the TextCleaner, SentenceSplitter, TermExtractor, and TextNormalizer.
"""

import pytest
from pathlib import Path
from typing import List, Dict, Any

from auto_programming_system.requirement_analysis.preprocessor import (
    TextPreprocessor,
    TextCleaner,
    SentenceSplitter,
    TermExtractor,
    TextNormalizer
)

from . import (
    PerformanceMetrics,
    SMALL_CASES_DIR,
    MEDIUM_CASES_DIR,
    LARGE_CASES_DIR
)
from .performance_metrics import PerformanceAnalyzer, MetricsCollector

# Initialize performance analyzer
analyzer = PerformanceAnalyzer(output_dir="performance_reports/preprocessor")
collector = MetricsCollector(analyzer)

@pytest.fixture
def preprocessor():
    """Create a TextPreprocessor instance for testing."""
    return TextPreprocessor()

def load_test_data(data_dir: Path) -> List[str]:
    """Load test data from the specified directory."""
    test_data = []
    for file in data_dir.glob("*.txt"):
        with open(file, 'r', encoding='utf-8') as f:
            test_data.append(f.read())
    return test_data

@pytest.mark.benchmark
class TestPreprocessorPerformance:
    """Performance tests for the preprocessor module."""

    def test_small_cases(self, preprocessor):
        """Test preprocessor performance with small input texts."""
        test_data = load_test_data(SMALL_CASES_DIR)
        
        collector.start_collection("preprocessor_small_cases")
        for text in test_data:
            preprocessor.process(text)
        collector.end_collection({
            'num_cases': len(test_data),
            'avg_text_length': sum(len(t) for t in test_data) / len(test_data)
        })

    def test_medium_cases(self, preprocessor):
        """Test preprocessor performance with medium-sized input texts."""
        test_data = load_test_data(MEDIUM_CASES_DIR)
        
        collector.start_collection("preprocessor_medium_cases")
        for text in test_data:
            preprocessor.process(text)
        collector.end_collection({
            'num_cases': len(test_data),
            'avg_text_length': sum(len(t) for t in test_data) / len(test_data)
        })

    def test_large_cases(self, preprocessor):
        """Test preprocessor performance with large input texts."""
        test_data = load_test_data(LARGE_CASES_DIR)
        
        collector.start_collection("preprocessor_large_cases")
        for text in test_data:
            preprocessor.process(text)
        collector.end_collection({
            'num_cases': len(test_data),
            'avg_text_length': sum(len(t) for t in test_data) / len(test_data)
        })

    def test_component_performance(self, preprocessor):
        """Test individual component performance."""
        test_data = load_test_data(MEDIUM_CASES_DIR)
        components = {
            'cleaner': TextCleaner(),
            'splitter': SentenceSplitter(),
            'extractor': TermExtractor(),
            'normalizer': TextNormalizer()
        }

        for name, component in components.items():
            collector.start_collection(f"component_{name}")
            for text in test_data:
                if hasattr(component, 'process'):
                    component.process(text)
                elif hasattr(component, 'clean'):
                    component.clean(text)
                elif hasattr(component, 'split'):
                    component.split(text)
                elif hasattr(component, 'extract'):
                    component.extract(text)
                elif hasattr(component, 'normalize'):
                    component.normalize(text)
            collector.end_collection({
                'component': name,
                'num_cases': len(test_data)
            })

    def test_concurrent_processing(self, preprocessor):
        """Test preprocessor performance with concurrent processing."""
        import concurrent.futures
        import multiprocessing

        test_data = load_test_data(MEDIUM_CASES_DIR)
        num_workers = multiprocessing.cpu_count()

        collector.start_collection("preprocessor_concurrent")
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(preprocessor.process, text) for text in test_data]
            concurrent.futures.wait(futures)
        collector.end_collection({
            'num_workers': num_workers,
            'num_cases': len(test_data)
        })

    @classmethod
    def teardown_class(cls):
        """Generate performance report after all tests are complete."""
        analyzer.generate_report("preprocessor_benchmark_report.json")

if __name__ == '__main__':
    pytest.main(['-v', __file__]) 