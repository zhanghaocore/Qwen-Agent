"""
Performance Metrics Collection and Analysis Tool.

This module provides tools for collecting, analyzing, and reporting performance metrics
for the auto programming system components.
"""

import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from . import (
    PerformanceMetrics,
    calculate_statistics,
    EXECUTION_TIME_THRESHOLD,
    MEMORY_USAGE_THRESHOLD,
    CPU_USAGE_THRESHOLD
)

class PerformanceAnalyzer:
    """Analyzes and reports performance metrics."""
    
    def __init__(self, output_dir: str = "performance_reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metrics: List[PerformanceMetrics] = []
        self._setup_logging()

    def _setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.output_dir / 'performance.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def add_metric(self, metric: PerformanceMetrics):
        """Add a performance metric to the analyzer."""
        self.metrics.append(metric)
        self._log_metric(metric)

    def _log_metric(self, metric: PerformanceMetrics):
        """Log a single performance metric."""
        self.logger.info(
            f"Performance metric recorded - Test: {metric.test_name}, "
            f"Time: {metric.execution_time:.3f}s, "
            f"Memory: {metric.memory_usage:.2f}MB, "
            f"CPU: {metric.cpu_usage:.1f}%"
        )

    def analyze_metrics(self) -> Dict[str, Any]:
        """Analyze collected metrics and generate statistics."""
        if not self.metrics:
            return {}

        # Group metrics by test name
        metrics_by_test = {}
        for metric in self.metrics:
            if metric.test_name not in metrics_by_test:
                metrics_by_test[metric.test_name] = []
            metrics_by_test[metric.test_name].append(metric)

        # Calculate statistics for each test
        analysis = {}
        for test_name, test_metrics in metrics_by_test.items():
            execution_times = [m.execution_time for m in test_metrics]
            memory_usages = [m.memory_usage for m in test_metrics]
            cpu_usages = [m.cpu_usage for m in test_metrics]

            analysis[test_name] = {
                'execution_time': calculate_statistics(execution_times),
                'memory_usage': calculate_statistics(memory_usages),
                'cpu_usage': calculate_statistics(cpu_usages),
                'samples': len(test_metrics),
                'thresholds_exceeded': self._check_thresholds(test_metrics)
            }

        return analysis

    def _check_thresholds(self, metrics: List[PerformanceMetrics]) -> Dict[str, int]:
        """Check how many times each threshold was exceeded."""
        return {
            'execution_time': sum(1 for m in metrics if m.execution_time > EXECUTION_TIME_THRESHOLD),
            'memory_usage': sum(1 for m in metrics if m.memory_usage > MEMORY_USAGE_THRESHOLD),
            'cpu_usage': sum(1 for m in metrics if m.cpu_usage > CPU_USAGE_THRESHOLD)
        }

    def generate_report(self, report_name: Optional[str] = None) -> str:
        """Generate a performance report and save it to a file."""
        if not report_name:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_name = f"performance_report_{timestamp}.json"

        report_path = self.output_dir / report_name
        analysis = self.analyze_metrics()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': len(self.metrics),
            'unique_tests': len({m.test_name for m in self.metrics}),
            'analysis': analysis,
            'thresholds': {
                'execution_time': EXECUTION_TIME_THRESHOLD,
                'memory_usage': MEMORY_USAGE_THRESHOLD,
                'cpu_usage': CPU_USAGE_THRESHOLD
            }
        }

        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        self.logger.info(f"Performance report generated: {report_path}")
        return str(report_path)

    def clear_metrics(self):
        """Clear all collected metrics."""
        self.metrics.clear()

class MetricsCollector:
    """Collects performance metrics during test execution."""

    def __init__(self, analyzer: PerformanceAnalyzer):
        self.analyzer = analyzer
        self.start_time: float = 0
        self.start_memory: float = 0
        self.test_name: str = ""

    def start_collection(self, test_name: str):
        """Start collecting metrics for a test."""
        self.test_name = test_name
        self.start_time = time.time()
        self.start_memory = self._get_current_memory()

    def end_collection(self, additional_metrics: Optional[Dict[str, Any]] = None):
        """End metrics collection and record results."""
        end_time = time.time()
        end_memory = self._get_current_memory()

        metric = PerformanceMetrics(
            execution_time=end_time - self.start_time,
            memory_usage=end_memory - self.start_memory,
            cpu_usage=self._get_cpu_usage(),
            test_name=self.test_name,
            timestamp=end_time,
            additional_metrics=additional_metrics
        )

        self.analyzer.add_metric(metric)

    @staticmethod
    def _get_current_memory() -> float:
        """Get current memory usage in MB."""
        import psutil
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024

    @staticmethod
    def _get_cpu_usage() -> float:
        """Get current CPU usage percentage."""
        import psutil
        return psutil.cpu_percent(interval=0.1) 