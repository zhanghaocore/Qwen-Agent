"""
需求分析模块

该模块负责将自然语言需求转换为结构化的编程任务描述。
"""

from .preprocessor import TextPreprocessor, PreprocessedText

__version__ = "0.1.0"

__all__ = [
    'TextPreprocessor',
    'PreprocessedText'
]
