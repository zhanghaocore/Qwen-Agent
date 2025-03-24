"""
规范验证器模块
负责验证生成的规范是否符合要求
"""

from typing import Dict, Any, List, Optional


class SpecificationValidator:
    """规范验证器，验证规范是否完整有效"""
    
    def __init__(self):
        """初始化规范验证器"""
        self.errors = []
        
    def validate(self, specification: Dict[str, Any]) -> bool:
        """
        验证规范是否有效
        
        Args:
            specification: 要验证的规范
            
        Returns:
            规范是否有效
        """
        self.errors = []
        
        # 检查必要字段
        required_fields = [
            "function_type", 
            "function_name", 
            "description",
            "parameters"
        ]
        
        for field in required_fields:
            if field not in specification:
                self.errors.append(f"缺少必要字段: {field}")
        
        # 如果缺少必要字段，验证失败
        if self.errors:
            return False
        
        # 检查函数名是否有效
        if not self._is_valid_function_name(specification["function_name"]):
            self.errors.append(f"函数名无效: {specification['function_name']}")
        
        # 检查参数是否有效
        for i, param in enumerate(specification.get("parameters", [])):
            if "name" not in param:
                self.errors.append(f"参数 {i+1} 缺少名称")
            elif not self._is_valid_parameter_name(param["name"]):
                self.errors.append(f"参数名无效: {param['name']}")
        
        # 返回验证结果
        return len(self.errors) == 0
    
    def get_errors(self) -> List[str]:
        """
        获取验证错误信息
        
        Returns:
            错误信息列表
        """
        return self.errors
    
    def _is_valid_function_name(self, name: str) -> bool:
        """
        检查函数名是否有效
        
        Args:
            name: 函数名
            
        Returns:
            是否有效
        """
        # 简单实现 - 检查函数名是否为非空字符串
        return bool(name and isinstance(name, str) and name.isalnum() or "_" in name)
    
    def _is_valid_parameter_name(self, name: str) -> bool:
        """
        检查参数名是否有效
        
        Args:
            name: 参数名
            
        Returns:
            是否有效
        """
        # 简单实现 - 检查参数名是否为非空字符串
        return bool(name and isinstance(name, str) and name.isalnum() or "_" in name) 