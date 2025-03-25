"""
参数提取器

负责从文本中提取函数或方法的参数信息。
"""

import re
from typing import Dict, List, Any, Optional


class ParameterExtractor:
    """
    参数提取器类，用于提取函数或方法的参数信息。
    
    功能包括：
    - 从文本中提取参数列表
    - 识别参数名称
    - 提取参数描述
    - 确定参数是否必需
    - 提取默认值
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化参数提取器。
        
        参数:
            config: 可选的配置参数字典
        """
        self.config = config or {}
        self._init_patterns()
    
    def _init_patterns(self):
        """初始化正则表达式模式。"""
        # 参数列表匹配模式（中英文逗号混合）
        self.param_list_pattern = re.compile(r'参数[：:]\s*(.+?)(?:，|,|返回|$)', re.DOTALL)
        self.alt_param_list_pattern = re.compile(r'接[收纳](一个|一|\s+)*(?:参数|列表|数组|字典|对象)?[：:]*\s*(.+?)(?:，|,|、|和|与|返回|为|；|。|$)', re.DOTALL)
        
        # 参数分隔符匹配模式（支持中英文逗号、顿号、和、与等）
        self.param_separator = re.compile(r'[,，、]\s*|(?:\s+和\s+|\s+与\s+)')
        
        # 参数名称匹配模式
        self.param_name_pattern = re.compile(r'^([a-zA-Z_]\w*)(?:\s+|\:)')
        
        # 可选参数匹配模式
        self.optional_pattern = re.compile(r'可选|optional', re.IGNORECASE)
        
        # 默认值匹配模式
        self.default_pattern = re.compile(r'默认(?:值|为|是)[\:：]?\s*(\S+)')
    
    def extract(self, text: str) -> List[Dict[str, Any]]:
        """
        从文本中提取参数信息。
        
        参数:
            text: 输入文本
            
        返回:
            参数信息列表
        """
        if not text:
            return []
        
        # 尝试提取参数列表
        param_list_match = self.param_list_pattern.search(text)
        if not param_list_match:
            param_list_match = self.alt_param_list_pattern.search(text)
        
        parameters = []
        if param_list_match:
            param_text = param_list_match.group(1)
            # 使用各种分隔符分割参数
            param_parts = self.param_separator.split(param_text)
            
            for i, part in enumerate(param_parts):
                if not part.strip():
                    continue
                
                # 提取参数详细信息
                param_info = self._extract_param_info(part.strip(), i)
                parameters.append(param_info)
        
        return parameters
    
    def _extract_param_info(self, param_text: str, index: int) -> Dict[str, Any]:
        """
        从参数文本中提取详细信息。
        
        参数:
            param_text: 参数描述文本
            index: 参数索引
            
        返回:
            参数信息字典
        """
        # 默认参数信息
        param_info = {
            'name': f'param{index+1}',
            'description': param_text,
            'type': 'Any',
            'required': True,
            'default': None
        }
        
        # 尝试提取参数名称
        name_match = self.param_name_pattern.search(param_text)
        if name_match:
            param_info['name'] = name_match.group(1)
        
        # 判断参数是否可选
        if self.optional_pattern.search(param_text):
            param_info['required'] = False
        
        # 提取默认值
        default_match = self.default_pattern.search(param_text)
        if default_match:
            param_info['default'] = default_match.group(1)
            param_info['required'] = False
        
        # 委托类型推断给SemanticAnalyzer，此处使用简单标识
        param_info['needs_type_inference'] = True
        
        return param_info 