"""
静态代码分析器模块
负责检查生成代码的质量和可能问题
"""

import re
from typing import Dict, Any, List, Optional


class StaticAnalyzer:
    """静态代码分析器，分析代码质量和潜在问题"""
    
    def __init__(self):
        """初始化静态代码分析器"""
        pass
    
    def analyze(self, code: str) -> List[str]:
        """
        分析代码
        
        Args:
            code: 要分析的代码
            
        Returns:
            问题列表
        """
        issues = []
        
        # 检查基本问题
        if "pass" in code and not self._is_in_docstring(code, "pass"):
            issues.append("代码中含有未实现的pass语句")
        
        # 检查缩进问题
        if self._has_indentation_issues(code):
            issues.append("代码可能存在缩进问题")
        
        # 检查未使用的导入
        unused_imports = self._find_unused_imports(code)
        for imp in unused_imports:
            issues.append(f"未使用的导入: {imp}")
        
        return issues
    
    def _is_in_docstring(self, code: str, text: str) -> bool:
        """
        检查文本是否在文档字符串中
        
        Args:
            code: 代码
            text: 要检查的文本
            
        Returns:
            文本是否在文档字符串中
        """
        # 简单实现，检查文本是否在三引号之间
        docstring_pattern = r'""".*?"""'
        docstrings = re.findall(docstring_pattern, code, re.DOTALL)
        
        for docstring in docstrings:
            if text in docstring:
                return True
                
        return False
    
    def _has_indentation_issues(self, code: str) -> bool:
        """
        检查代码是否有缩进问题
        
        Args:
            code: 代码
            
        Returns:
            是否有缩进问题
        """
        lines = code.split("\n")
        for i, line in enumerate(lines):
            # 跳过空行
            if not line.strip():
                continue
                
            # 检查缩进是否是4的倍数（简单检查）
            indent = len(line) - len(line.lstrip())
            if indent % 4 != 0:
                return True
                
        return False
    
    def _find_unused_imports(self, code: str) -> List[str]:
        """
        查找未使用的导入
        
        Args:
            code: 代码
            
        Returns:
            未使用的导入列表
        """
        # 简单实现，提取导入的模块名并检查是否在代码中使用
        imports = []
        unused = []
        
        # 匹配导入语句
        import_pattern = r'import\s+([a-zA-Z0-9_]+)'
        from_import_pattern = r'from\s+[a-zA-Z0-9_.]+\s+import\s+([a-zA-Z0-9_, ]+)'
        
        # 提取导入的模块
        for match in re.finditer(import_pattern, code):
            imports.append(match.group(1))
            
        # 提取from导入的对象
        for match in re.finditer(from_import_pattern, code):
            imported_items = match.group(1).split(',')
            for item in imported_items:
                item = item.strip()
                if item:
                    imports.append(item)
        
        # 检查每个导入是否在代码中使用
        for imp in imports:
            # 跳过typing模块，通常只用于类型注解
            if imp == "typing" or imp in ["Any", "List", "Dict", "Optional"]:
                continue
                
            # 在导入语句之后查找
            import_pos = code.find(f"import {imp}")
            if import_pos == -1:
                import_pos = code.find(f"import {imp},")
                
            if import_pos == -1:
                continue
                
            rest_of_code = code[import_pos + len(f"import {imp}"):]
            
            # 检查模块名是否在代码中使用
            if imp + "." not in rest_of_code and not re.search(r'\b' + re.escape(imp) + r'\b', rest_of_code):
                unused.append(imp)
                
        return unused 