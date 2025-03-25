"""
语义分析器

负责从预处理文本中提取语义信息，包括意图分类、参数识别和类型推断。
"""

import re
from typing import Dict, List, Any, Optional, Tuple


class SemanticAnalyzer:
    """
    语义分析器类，用于提取文本中的语义信息。
    
    功能包括：
    - 参数提取
    - 类型推断
    - 函数名称生成
    - 返回值提取
    - 需求描述解析
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化语义分析器。
        
        参数:
            config: 可选的配置参数字典
        """
        self.config = config or {}
        self._init_patterns()
    
    def _init_patterns(self):
        """初始化正则表达式模式。"""
        # 函数描述匹配模式
        self.function_pattern = re.compile(r'(?:创建|实现|开发|编写)(一个|一|个)*\s*(\w+)?\s*(?:的)*\s*(?:函数|方法|代码|API|接口|程序)', re.IGNORECASE)
        
        # 参数列表匹配模式（中英文逗号混合）
        self.param_list_pattern = re.compile(r'接[收纳](一个|一|\s+)*(?:参数|列表|数组|字典|对象)?[：:]*\s*(.+?)(?:，|,|、|和|与|返回|为|；|。|$)', re.DOTALL)
        
        # 参数分隔符匹配模式（支持中英文逗号、顿号、和、与等）
        self.param_separator = re.compile(r'[,，、]\s*|(?:\s+和\s+|\s+与\s+)')
        
        # 类型匹配模式
        self.type_pattern = re.compile(r'(?:类型|type)[为是:：]\s*(\w+)|\(\s*(\w+)\s*(?:类型|type)\)')
        
        # 函数名匹配模式
        self.funcname_pattern = re.compile(r'函数名[为是:：]\s*(\w+)')
        
        # 返回值匹配模式
        self.return_pattern = re.compile(r'返回\s*(?:一个|一|\s+)*(?:参数|值|结果)?[：:]*\s*(.+?)(?:，|,|、|；|。|$)', re.DOTALL)
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        分析文本并提取语义信息。
        
        参数:
            text: 输入文本
            
        返回:
            包含语义分析结果的字典
        """
        if not text:
            return {}
        
        # 提取函数描述
        function_info = self._extract_function_info(text)
        
        # 提取参数信息
        parameters = self._extract_parameters(text)
        
        # 提取返回值信息
        return_info = self._extract_return_info(text)
        
        # 组合结果
        result = {
            'original_text': text,
            'function_info': function_info,
            'parameters': parameters,
            'return_info': return_info,
            'intent': self._determine_intent(text)
        }
        
        return result
    
    def _extract_function_info(self, text: str) -> Dict[str, Any]:
        """提取函数相关信息。"""
        function_info = {
            'function_name': '',
            'description': text.strip(),
            'purpose': ''
        }
        
        # 尝试提取函数名称
        funcname_match = self.funcname_pattern.search(text)
        if funcname_match:
            function_info['function_name'] = funcname_match.group(1)
        else:
            # 从函数描述中推断函数名
            function_match = self.function_pattern.search(text)
            if function_match and function_match.group(2):
                function_info['function_name'] = function_match.group(2) + '_function'
        
        # 提取函数目的（简单实现，实际应用中可能需要更复杂的逻辑）
        first_sentence = text.split('.')[0] if '.' in text else text
        function_info['purpose'] = first_sentence.strip()
        
        return function_info
    
    def _extract_parameters(self, text: str) -> List[Dict[str, Any]]:
        """提取参数信息。"""
        parameters = []
        
        # 尝试提取参数列表
        param_list_match = self.param_list_pattern.search(text)
        if param_list_match:
            param_text = param_list_match.group(2)
            # 使用各种分隔符分割参数
            param_parts = self.param_separator.split(param_text)
            
            for i, part in enumerate(param_parts):
                if not part.strip():
                    continue
                
                param = {
                    'name': f'param{i+1}',
                    'description': part.strip(),
                    'type': self._infer_type(part.strip()),
                    'required': True,
                    'default': None
                }
                
                parameters.append(param)
        
        return parameters
    
    def _extract_return_info(self, text: str) -> Dict[str, Any]:
        """提取返回值信息。"""
        return_info = {
            'type': 'None',
            'description': ''
        }
        
        # 尝试提取返回值描述
        return_match = self.return_pattern.search(text)
        if return_match:
            return_description = return_match.group(1).strip()
            return_info['description'] = return_description
            return_info['type'] = self._infer_type(return_description)
        
        return return_info
    
    def _infer_type(self, text: str) -> str:
        """从文本中推断类型。"""
        # 简单的类型推断规则
        if re.search(r'字符串|string|str|文本|text', text, re.IGNORECASE):
            return 'str'
        elif re.search(r'整数|integer|int|数字', text, re.IGNORECASE):
            return 'int'
        elif re.search(r'浮点|float|小数|decimal', text, re.IGNORECASE):
            return 'float'
        elif re.search(r'布尔|boolean|bool|真假', text, re.IGNORECASE):
            return 'bool'
        elif re.search(r'列表|list|数组|array', text, re.IGNORECASE):
            inner_type = self._infer_inner_type(text)
            return f'List[{inner_type}]'
        elif re.search(r'字典|dict|映射|map', text, re.IGNORECASE):
            key_type, value_type = self._infer_dict_types(text)
            return f'Dict[{key_type}, {value_type}]'
        elif re.search(r'元组|tuple', text, re.IGNORECASE):
            return 'tuple'
        elif re.search(r'集合|set', text, re.IGNORECASE):
            return 'set'
        elif re.search(r'无|none', text, re.IGNORECASE):
            return 'None'
        else:
            return 'Any'
    
    def _infer_inner_type(self, text: str) -> str:
        """推断列表内部类型。"""
        if re.search(r'字符串|string|str|文本|text', text, re.IGNORECASE):
            return 'str'
        elif re.search(r'整数|integer|int|数字', text, re.IGNORECASE):
            return 'int'
        elif re.search(r'浮点|float|小数|decimal', text, re.IGNORECASE):
            return 'float'
        else:
            return 'Any'
    
    def _infer_dict_types(self, text: str) -> Tuple[str, str]:
        """推断字典的键和值类型。"""
        key_type = 'str'  # 默认键类型
        value_type = 'Any'  # 默认值类型
        
        if re.search(r'整数|integer|int|数字.*?键|key', text, re.IGNORECASE):
            key_type = 'int'
        
        if re.search(r'字符串|string|str|文本|text.*?值|value', text, re.IGNORECASE):
            value_type = 'str'
        elif re.search(r'整数|integer|int|数字.*?值|value', text, re.IGNORECASE):
            value_type = 'int'
        elif re.search(r'浮点|float|小数|decimal.*?值|value', text, re.IGNORECASE):
            value_type = 'float'
        
        return key_type, value_type
    
    def _determine_intent(self, text: str) -> str:
        """确定文本的主要意图。"""
        if re.search(r'函数|方法|method|function', text, re.IGNORECASE):
            return 'function_creation'
        elif re.search(r'类|class|对象|object', text, re.IGNORECASE):
            return 'class_creation'
        elif re.search(r'API|端点|endpoint|接口|interface', text, re.IGNORECASE):
            return 'api_creation'
        elif re.search(r'数据库|database|表|table|存储|storage', text, re.IGNORECASE):
            return 'database_operation'
        elif re.search(r'配置|config|设置|setting', text, re.IGNORECASE):
            return 'configuration'
        else:
            return 'general_task' 