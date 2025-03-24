"""
Performance Testing Module for Auto Programming System.

This module contains performance testing utilities and configurations for the
auto programming system, including benchmarking tools and metrics collection.
"""

import time
import psutil
import statistics
from typing import Callable, Any, List, Dict, Optional, Union
from dataclasses import dataclass
from pathlib import Path

@dataclass
class PerformanceMetrics:
    """Data class for storing performance test results."""
    execution_time: float  # in seconds
    memory_usage: float   # in MB
    cpu_usage: float      # percentage
    test_name: str
    timestamp: float
    additional_metrics: Optional[Dict[str, Any]] = None

def measure_execution_time(func: Callable) -> Callable:
    """Decorator to measure function execution time."""
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        return result, execution_time
    return wrapper

def measure_memory_usage(func: Callable) -> Callable:
    """Decorator to measure memory usage of a function."""
    def wrapper(*args, **kwargs) -> Any:
        process = psutil.Process()
        start_memory = process.memory_info().rss / 1024 / 1024  # Convert to MB
        result = func(*args, **kwargs)
        end_memory = process.memory_info().rss / 1024 / 1024
        memory_used = end_memory - start_memory
        return result, memory_used
    return wrapper

def calculate_statistics(metrics: List[float]) -> Dict[str, float]:
    """Calculate basic statistics for a list of metrics."""
    return {
        'mean': statistics.mean(metrics),
        'median': statistics.median(metrics),
        'std_dev': statistics.stdev(metrics) if len(metrics) > 1 else 0,
        'min': min(metrics),
        'max': max(metrics)
    }

# Test data paths
TEST_DATA_DIR = Path(__file__).parent / 'test_data'
SMALL_CASES_DIR = TEST_DATA_DIR / 'small_cases'
MEDIUM_CASES_DIR = TEST_DATA_DIR / 'medium_cases'
LARGE_CASES_DIR = TEST_DATA_DIR / 'large_cases'

# Performance thresholds
EXECUTION_TIME_THRESHOLD = 1.0  # seconds
MEMORY_USAGE_THRESHOLD = 100    # MB
CPU_USAGE_THRESHOLD = 80        # percentage 