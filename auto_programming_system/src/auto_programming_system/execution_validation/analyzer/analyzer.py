"""
代码分析器模块
负责分析代码质量和特性
"""

import ast
import re
from typing import Dict, Any, List, Optional


class CodeAnalyzer:
    """代码分析器，分析代码的质量和特性"""
    
    def __init__(self):
        """初始化代码分析器"""
        pass
    
    def analyze(self, code: str) -> Dict[str, Any]:
        """
        分析代码
        
        Args:
            code: 要分析的代码
            
        Returns:
            分析结果字典
        """
        results = {
            "code_metrics": self._calculate_metrics(code),
            "code_quality": self._assess_quality(code),
            "code_features": self._extract_features(code)
        }
        
        return results
    
    def _calculate_metrics(self, code: str) -> Dict[str, Any]:
        """
        计算代码度量
        
        Args:
            code: 要分析的代码
            
        Returns:
            度量结果
        """
        lines = code.split("\n")
        non_empty_lines = [line for line in lines if line.strip()]
        
        # 计算基本度量
        metrics = {
            "total_lines": len(lines),
            "code_lines": len(non_empty_lines),
            "blank_lines": len(lines) - len(non_empty_lines),
            "comment_lines": sum(1 for line in lines if line.strip().startswith("#")),
            "average_line_length": sum(len(line) for line in non_empty_lines) / len(non_empty_lines) if non_empty_lines else 0
        }
        
        # 分析代码结构
        try:
            tree = ast.parse(code)
            
            # 计算函数和类
            metrics["num_functions"] = sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
            metrics["num_classes"] = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
            
            # 计算分支和循环
            metrics["num_branches"] = sum(1 for node in ast.walk(tree) if isinstance(node, (ast.If, ast.IfExp)))
            metrics["num_loops"] = sum(1 for node in ast.walk(tree) if isinstance(node, (ast.For, ast.While)))
        except:
            # 如果代码无法解析，设置为0
            metrics.update({
                "num_functions": 0,
                "num_classes": 0,
                "num_branches": 0,
                "num_loops": 0
            })
        
        return metrics
    
    def _assess_quality(self, code: str) -> Dict[str, Any]:
        """
        评估代码质量
        
        Args:
            code: 要分析的代码
            
        Returns:
            质量评估结果
        """
        quality = {
            "has_docstrings": self._has_docstrings(code),
            "has_type_annotations": self._has_type_annotations(code),
            "has_error_handling": self._has_error_handling(code),
            "issues": self._identify_issues(code)
        }
        
        # 计算综合质量评分
        score_factors = [
            3 if quality["has_docstrings"] else 0,
            2 if quality["has_type_annotations"] else 0,
            2 if quality["has_error_handling"] else 0,
            3 if not quality["issues"] else max(0, 3 - len(quality["issues"]))
        ]
        
        quality["score"] = sum(score_factors) / 10.0  # 归一化到0-1
        
        return quality
    
    def _extract_features(self, code: str) -> Dict[str, Any]:
        """
        提取代码特性
        
        Args:
            code: 要分析的代码
            
        Returns:
            特性字典
        """
        features = {
            "imports": self._extract_imports(code),
            "functions": self._extract_function_names(code),
            "uses_classes": self._uses_classes(code),
            "uses_list_comprehension": self._uses_list_comprehension(code),
            "uses_generators": self._uses_generators(code),
        }
        
        return features
    
    def _has_docstrings(self, code: str) -> bool:
        """检查代码是否包含文档字符串"""
        return '"""' in code or "'''" in code
    
    def _has_type_annotations(self, code: str) -> bool:
        """检查代码是否使用类型注解"""
        return " -> " in code or re.search(r": *[A-Za-z\[\], ]+", code) is not None
    
    def _has_error_handling(self, code: str) -> bool:
        """检查代码是否使用异常处理"""
        return "try:" in code and "except" in code
    
    def _identify_issues(self, code: str) -> List[str]:
        """识别代码中的潜在问题"""
        issues = []
        
        # 检查长行
        for i, line in enumerate(code.split("\n")):
            if len(line.strip()) > 100:
                issues.append(f"第{i+1}行过长 ({len(line.strip())} 字符)")
        
        # 检查裸except
        if re.search(r"except *:", code):
            issues.append("使用了裸except语句")
        
        # 检查pass语句
        if re.search(r"[^#]pass", code):
            issues.append("包含未实现的pass语句")
        
        return issues
    
    def _extract_imports(self, code: str) -> List[str]:
        """提取代码中的导入语句"""
        imports = []
        import_pattern = r"(import|from) ([a-zA-Z0-9_\.]+)"
        
        for match in re.finditer(import_pattern, code):
            imports.append(match.group(2))
            
        return imports
    
    def _extract_function_names(self, code: str) -> List[str]:
        """提取代码中的函数名"""
        functions = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
        except:
            pass
            
        return functions
    
    def _uses_classes(self, code: str) -> bool:
        """检查代码是否使用类"""
        return "class " in code
    
    def _uses_list_comprehension(self, code: str) -> bool:
        """检查代码是否使用列表推导式"""
        return re.search(r"\[.+for.+in.+\]", code) is not None
    
    def _uses_generators(self, code: str) -> bool:
        """检查代码是否使用生成器"""
        return "yield " in code or re.search(r"\(.+for.+in.+\)", code) is not None 