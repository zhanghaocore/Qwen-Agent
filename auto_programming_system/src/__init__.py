"""
全自动Python后端编程系统
"""

from src.requirement_analysis.core import RequirementAnalyzer
from src.code_generation.core import CodeGenerator
from src.execution_validation.core import CodeValidator
from src.optimization.core import CodeOptimizer
from src.core import AutoProgrammingSystem

__version__ = "0.1.0"

__all__ = [
    "AutoProgrammingSystem",
    "RequirementAnalyzer",
    "CodeGenerator",
    "CodeValidator",
    "CodeOptimizer",
] 