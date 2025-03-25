"""
需求分析模块的核心类
负责将自然语言需求转换为结构化的编程任务描述
"""

import json
from typing import Dict, Any, List, Optional

from .preprocessor import TextPreprocessor, PreprocessedText
from src.requirement_analysis.semantic_analyzer.analyzer import SemanticAnalyzer
from src.requirement_analysis.dsl_converter.converter import DSLConverter
from src.requirement_analysis.validator.validator import SpecificationValidator


class RequirementAnalyzer:
    """需求分析器的主类，协调各个组件完成需求分析。"""
    
    def __init__(self):
        """初始化需求分析器及其组件。"""
        self.preprocessor = TextPreprocessor()
        self.semantic_analyzer = SemanticAnalyzer()
        self.dsl_converter = DSLConverter()
        self.validator = SpecificationValidator()
    
    def parse(self, text: str) -> Dict[str, Any]:
        """
        解析自然语言需求文本。
        
        Args:
            text: 需求文本
            
        Returns:
            包含结构化需求规范的字典
            
        Raises:
            ValueError: 如果无法解析需求或结果不符合规范
        """
        # 1. 预处理文本
        preprocessed: PreprocessedText = self.preprocessor.preprocess(text)
        
        # 2. 语义分析
        semantic_result = self.semantic_analyzer.analyze(preprocessed.normalized_text)
        
        # 3. 转换为DSL
        specification = self.dsl_converter.convert(semantic_result)
        
        # 4. 验证规范
        if not self.validator.validate(specification):
            raise ValueError("Generated specification does not meet the requirements")
            
        return specification
    
    def enrich_specification(self, spec: Dict[str, Any], additional_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        使用附加信息丰富规范
        
        Args:
            spec: 原始规范
            additional_info: 附加信息
            
        Returns:
            丰富后的规范
        """
        enriched = spec.copy()
        
        # 合并约束条件
        if "constraints" in additional_info and "constraints" in enriched:
            enriched["constraints"].extend(additional_info["constraints"])
        elif "constraints" in additional_info:
            enriched["constraints"] = additional_info["constraints"]
        
        # 验证丰富后的规范
        if not self.validator.validate(enriched):
            errors = self.validator.get_errors()
            raise ValueError(f"丰富规范验证失败: {errors}")
        
        return enriched
