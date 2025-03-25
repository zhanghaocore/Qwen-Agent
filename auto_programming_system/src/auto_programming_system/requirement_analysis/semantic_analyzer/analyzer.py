"""
语义分析器模块
负责分析预处理后的需求文本，提取关键概念和关系
"""

from typing import Dict, Any, List, Optional, Tuple, Set
import re


class SemanticAnalyzer:
    """语义分析器，将预处理文本转换为语义表示"""
    
    def __init__(self):
        """初始化语义分析器"""
        # 定义关键操作匹配模式
        self.operation_patterns = {
            "创建": {"action": "create", "confidence": 1.0},
            "生成": {"action": "create", "confidence": 1.0},
            "制作": {"action": "create", "confidence": 0.9},
            "开发": {"action": "create", "confidence": 0.9},
            "实现": {"action": "create", "confidence": 0.9},
            "编写": {"action": "create", "confidence": 0.9},
            "构建": {"action": "create", "confidence": 0.9},
            "查询": {"action": "query", "confidence": 1.0},
            "搜索": {"action": "query", "confidence": 1.0},
            "读取": {"action": "read", "confidence": 1.0},
            "获取": {"action": "read", "confidence": 1.0},
            "提取": {"action": "read", "confidence": 0.9},
            "修改": {"action": "update", "confidence": 1.0},
            "更新": {"action": "update", "confidence": 1.0},
            "编辑": {"action": "update", "confidence": 1.0},
            "删除": {"action": "delete", "confidence": 1.0},
            "移除": {"action": "delete", "confidence": 1.0},
            "清除": {"action": "delete", "confidence": 0.9},
            "验证": {"action": "validate", "confidence": 1.0},
            "校验": {"action": "validate", "confidence": 1.0},
            "检查": {"action": "validate", "confidence": 0.9},
            "转换": {"action": "transform", "confidence": 1.0},
            "处理": {"action": "process", "confidence": 0.9},
            "计算": {"action": "calculate", "confidence": 1.0},
            "分析": {"action": "analyze", "confidence": 1.0},
            "发送": {"action": "send", "confidence": 1.0},
            "接收": {"action": "receive", "confidence": 1.0},
            "过滤": {"action": "filter", "confidence": 1.0},
            "排序": {"action": "sort", "confidence": 1.0},
            "分组": {"action": "group", "confidence": 1.0},
            "合并": {"action": "merge", "confidence": 1.0},
        }
        
        # 定义数据类型匹配模式
        self.data_type_patterns = {
            "整数": "int",
            "数字": "int",
            "int": "int",
            "integer": "int",
            "浮点数": "float",
            "小数": "float",
            "float": "float",
            "字符串": "str",
            "文本": "str",
            "str": "str",
            "string": "str",
            "布尔": "bool",
            "布尔值": "bool",
            "bool": "bool",
            "boolean": "bool",
            "列表": "List",
            "数组": "List",
            "list": "List",
            "array": "List",
            "字典": "Dict",
            "映射": "Dict",
            "dict": "Dict",
            "map": "Dict",
            "dictionary": "Dict",
            "集合": "Set",
            "set": "Set",
            "元组": "Tuple",
            "tuple": "Tuple",
            "日期": "datetime.date",
            "date": "datetime.date",
            "时间": "datetime.time",
            "time": "datetime.time",
            "日期时间": "datetime.datetime",
            "datetime": "datetime.datetime",
            "文件": "file",
            "file": "file",
            "对象": "object",
            "object": "object",
            "json": "JSON",
            "xml": "XML",
            "yaml": "YAML",
            "csv": "CSV",
        }
        
        # 复合数据类型模式
        self.complex_type_patterns = {
            r'(列表|数组|List)[\s]*[的]?[\s]*(整数|数字|int)': "List[int]",
            r'(整数|数字|int)[\s]*[的]?[\s]*(列表|数组|List)': "List[int]",
            r'(列表|数组|List)[\s]*[的]?[\s]*(字符串|文本|str)': "List[str]",
            r'(字符串|文本|str)[\s]*[的]?[\s]*(列表|数组|List)': "List[str]",
            r'(列表|数组|List)[\s]*[的]?[\s]*(浮点数|小数|float)': "List[float]",
            r'(浮点数|小数|float)[\s]*[的]?[\s]*(列表|数组|List)': "List[float]",
            r'(列表|数组|List)[\s]*[的]?[\s]*(字典|映射|dict)': "List[Dict]",
            r'(字典|映射|dict)[\s]*[的]?[\s]*(列表|数组|List)': "List[Dict]",
            r'(字典|映射|dict)[\s]*[的]?[\s]*(字符串|文本|str)': "Dict[str, Any]",
            r'(字典|映射|dict)[\s]*[的]?[\s]*(整数|数字|int)': "Dict[int, Any]",
        }
        
        # 条件和逻辑操作匹配模式
        self.condition_patterns = {
            r'\b(如果|若|当|if)\b': "if_condition",
            r'\b(否则|else)\b': "else_condition",
            r'\b(否则如果|elif|else if)\b': "elif_condition",
            r'\b(所有|全部|all)\b': "all_qualifier",
            r'\b(任何|任意|any)\b': "any_qualifier",
            r'\b(每个|each)\b': "each_qualifier",
            r'\b(大于|>|多于|more than)\b': "greater_than",
            r'\b(小于|<|少于|less than)\b': "less_than",
            r'\b(等于|==|=|equals)\b': "equals",
            r'\b(不等于|!=|不同于|not equals)\b': "not_equals",
            r'\b(大于等于|>=)\b': "greater_than_or_equals",
            r'\b(小于等于|<=)\b': "less_than_or_equals",
            r'\b(包含|contains|包括)\b': "contains",
            r'\b(不包含|不含有|excludes)\b': "not_contains",
            r'\b(存在|exists)\b': "exists",
            r'\b(不存在|not exists)\b': "not_exists",
            r'\b(和|且|与|and)\b': "and_operator",
            r'\b(或|或者|or)\b': "or_operator",
            r'\b(不|非|not)\b': "not_operator",
        }
    
    def analyze(self, text: str, original_text: Optional[str] = None) -> Dict[str, Any]:
        """
        分析预处理后的文本，提取语义信息
        
        Args:
            text: 预处理后的需求文本
            original_text: 原始需求文本（如果None则使用预处理文本）
            
        Returns:
            包含语义信息的字典
        """
        # 使用原始文本作为描述，如果未提供则使用预处理文本
        description = original_text if original_text is not None else text
        
        # 识别操作类型
        operation_type, function_type = self._identify_operation_type(text)
        
        # 基于操作类型创建基本结构
        result = {
            "function_type": function_type,
            "operation_type": operation_type,
            "description": description,
            "parameters": [],
            "return_type": "Any",
            "return_description": "函数返回值",  # 使用固定的返回值描述
            "constraints": [],
            "examples": []
        }
        
        # 提取参数和返回值
        result = self._extract_parameters_and_return(text, result)
        
        # 提取约束条件和业务规则
        result = self._extract_constraints(text, result)
        
        # 提取步骤和逻辑路径
        result = self._extract_logic_paths(text, result)
        
        # 尝试推断函数名
        result["function_name"] = self._generate_function_name(result)
        
        return result
    
    def _identify_operation_type(self, text: str) -> Tuple[str, str]:
        """识别操作类型和函数类型"""
        operation_type = "process"  # 默认操作类型
        function_type = "function"  # 默认是函数
        
        # 检查是否包含类的指示词
        if re.search(r'\b(类|class|对象|object)\b', text):
            function_type = "class"
        # 检查是否包含API的指示词
        elif re.search(r'\b(API|接口|端点|endpoint|服务|微服务)\b', text):
            function_type = "api"
        
        # 查找主要操作类型
        max_confidence = 0
        for keyword, info in self.operation_patterns.items():
            if keyword in text:
                if info["confidence"] > max_confidence:
                    max_confidence = info["confidence"]
                    operation_type = info["action"]
        
        return operation_type, function_type
    
    def _extract_parameters_and_return(self, text: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """提取参数和返回值信息"""
        # 如果有"接收"关键词，提取其后到"返回"之前的所有内容作为参数
        if "接收" in text:
            param_text = text.split("接收")[1]
            if "返回" in param_text:
                param_text = param_text.split("返回")[0]
            self._extract_parameters_from_text(param_text.strip(), result)
        
        # 尝试提取返回值类型
        return_patterns = [
            r'返回(?:一个|1个|一|1)?(\S+)',
            r'输出(?:一个|1个|一|1)?(\S+)',
            r'生成(?:一个|1个|一|1)?(\S+)',
        ]
        
        for pattern in return_patterns:
            match = re.search(pattern, text)
            if match:
                return_type_text = match.group(1)
                return_type = self._infer_data_type(return_type_text)
                result["return_type"] = return_type
                break
        
        return result
    
    def _process_param_match(self, match: re.Match, result: Dict[str, Any]) -> None:
        """处理单个参数匹配"""
        param_text = match.group(1)
        self._add_parameter(param_text, result)
    
    def _process_param_list(self, match: re.Match, result: Dict[str, Any]) -> None:
        """处理参数列表匹配"""
        param_text = match.group(1)
        self._extract_parameters_from_text(param_text, result)
    
    def _extract_parameters_from_text(self, param_text: str, result: Dict[str, Any]) -> None:
        """从文本中提取参数列表"""
        # 替换所有可能的分隔符为英文逗号
        separators = ["，", "、", "和", "与", "以及", "还有"]
        processed_text = param_text
        
        # 处理"返回"之前的文本
        if "返回" in processed_text:
            processed_text = processed_text.split("返回")[0]
        
        # 替换分隔符
        for sep in separators:
            processed_text = processed_text.replace(sep, ",")
        
        # 分割参数并过滤空值
        params = [p.strip() for p in processed_text.split(",") if p.strip()]
        
        # 处理可能的参数组合，比如"整数和字符串"
        expanded_params = []
        merged_params = []  # 初始化 merged_params 列表
        current_param = None
        
        for param in params:
            if any(type_text in param for type_text in self.data_type_patterns.keys()):
                if current_param:
                    merged_params.append(current_param)
                current_param = param
            else:
                if current_param:
                    current_param += param
                else:
                    current_param = param
        
        if current_param:
            merged_params.append(current_param)
        
        # 处理每个参数
        for param in merged_params:
            self._add_parameter(param, result)
    
    def _add_parameter(self, param_text: str, result: Dict[str, Any]) -> None:
        """添加单个参数到结果字典"""
        # 检查是否已经添加该参数
        for existing_param in result["parameters"]:
            if param_text.strip() in existing_param["description"]:
                return
        
        param_type = self._infer_data_type(param_text)
        param_name = self._generate_param_name(param_text, len(result["parameters"]))
        
        # 使用完整的参数文本作为描述
        result["parameters"].append({
            "name": param_name,
            "type": param_type,
            "description": param_text.strip()
        })
    
    def _infer_data_type(self, text: str) -> str:
        """推断数据类型"""
        # 先检查复合类型
        for pattern, type_str in self.complex_type_patterns.items():
            if re.search(pattern, text):
                return type_str
        
        # 检查直接类型匹配
        for type_text, type_str in self.data_type_patterns.items():
            if type_text in text:
                return type_str
        
        # 基于关键词推断
        if any(word in text for word in ["文件", "file", "路径", "path"]):
            return "str"  # 假定文件路径是字符串
        elif any(word in text for word in ["url", "链接", "网址"]):
            return "str"
        elif any(word in text for word in ["日期", "时间", "date", "time"]):
            return "datetime.datetime"
        elif any(word in text for word in ["配置", "设置", "参数", "选项"]):
            return "Dict"
        elif any(word in text for word in ["列表", "数组", "集合", "list", "array"]):
            return "List"
        elif any(word in text for word in ["布尔", "布尔值", "标志", "开关", "boolean", "flag"]):
            return "bool"
        elif any(word in text for word in ["数字", "整数", "数值", "int", "number"]):
            return "int"
        elif any(word in text for word in ["名称", "名字", "标题", "描述", "内容", "文本", "信息", "消息", "备注"]):
            return "str"
        
        # 如果参数名看起来像是字符串类型
        string_patterns = [
            r'name$',
            r'title$',
            r'desc$',
            r'description$',
            r'text$',
            r'content$',
            r'message$',
            r'msg$',
            r'note$',
            r'comment$',
            r'label$',
            r'tag$',
            r'key$',
            r'code$',
            r'status$'
        ]
        if any(re.search(pattern, text.lower()) for pattern in string_patterns):
            return "str"
        
        return "Any"  # 默认类型
    
    def _generate_param_name(self, param_text: str, index: int) -> str:
        """生成参数名称"""
        # 尝试从参数描述中提取有意义的名称
        name_hints = {
            "文件": "file",
            "路径": "path",
            "名称": "name",
            "列表": "items",
            "数组": "array",
            "字典": "dict",
            "映射": "mapping",
            "日期": "date",
            "时间": "time",
            "配置": "config",
            "选项": "options",
            "设置": "settings",
            "用户": "user",
            "客户": "customer",
            "数据": "data",
            "值": "value",
            "键": "key",
            "地址": "address",
            "url": "url",
            "链接": "link",
            "查询": "query",
            "过滤": "filter",
            "条件": "condition",
        }
        
        for hint, name in name_hints.items():
            if hint in param_text:
                return name
        
        # 如果没有找到匹配的，使用默认命名
        return f"param{index + 1}"
    
    def _extract_constraints(self, text: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """提取约束条件和业务规则"""
        constraint_patterns = [
            # "必须/应该..."模式
            r'(必须|应该|需要|要求)(\S+)',
            # "确保..."模式
            r'确保(\S+)',
            # "限制..."模式
            r'(限制|约束)(\S+)',
            # "不允许..."模式
            r'不(允许|能|可以)(\S+)',
            # "如果...则..."模式
            r'如果(\S+)则(\S+)',
        ]
        
        for pattern in constraint_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                if len(match.groups()) >= 1:
                    constraint = match.group(0)
                    if constraint and not any(c == constraint for c in result["constraints"]):
                        result["constraints"].append(constraint)
        
        # 特定类型的约束
        if "性能" in text or "效率" in text:
            result["constraints"].append("优化性能和效率")
        
        if "安全" in text:
            result["constraints"].append("确保安全性")
        
        if "并发" in text or "多线程" in text:
            result["constraints"].append("支持并发处理")
        
        return result
    
    def _extract_logic_paths(self, text: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """提取逻辑路径和处理步骤"""
        # 如果没有逻辑路径字段，添加一个
        if "logic_paths" not in result:
            result["logic_paths"] = []
        
        # 查找条件结构
        for pattern_text, pattern_type in self.condition_patterns.items():
            matches = re.finditer(pattern_text, text)
            for match in matches:
                condition = match.group(0)
                context = self._get_surrounding_context(text, match.start(), 50)
                if condition and context:
                    result["logic_paths"].append({
                        "type": pattern_type,
                        "condition": condition,
                        "context": context
                    })
        
        # 查找处理步骤
        steps = self._extract_processing_steps(text)
        if steps:
            if "processing_steps" not in result:
                result["processing_steps"] = []
            result["processing_steps"].extend(steps)
        
        return result
    
    def _get_surrounding_context(self, text: str, position: int, window_size: int) -> str:
        """获取上下文文本片段"""
        start = max(0, position - window_size)
        end = min(len(text), position + window_size)
        return text[start:end]
    
    def _extract_processing_steps(self, text: str) -> List[Dict[str, Any]]:
        """提取处理步骤"""
        steps = []
        
        # 查找数字编号的步骤，如 "1. xxx 2. yyy"
        numbered_steps = re.finditer(r'\b(\d+)[.、]([\s\S]+?)(?=\b\d+[.、]|$)', text)
        for match in numbered_steps:
            step_num = match.group(1)
            step_text = match.group(2).strip()
            steps.append({
                "step_number": int(step_num),
                "description": step_text
            })
        
        # 查找关键词引导的步骤
        step_keywords = ["首先", "然后", "接着", "之后", "最后", "同时", "首次", "随后", "下一步", "先", "后"]
        for keyword in step_keywords:
            pattern = f'({keyword})([^。；！？]*[。；！？])'
            matches = re.finditer(pattern, text)
            for match in matches:
                step_text = match.group(0).strip()
                if step_text:
                    steps.append({
                        "keyword": match.group(1),
                        "description": step_text
                    })
        
        # 排序步骤
        if steps:
            # 如果有编号的步骤，按编号排序
            numbered = [s for s in steps if "step_number" in s]
            if numbered:
                numbered.sort(key=lambda x: x["step_number"])
            
            # 其他步骤按出现顺序保持不变
            return steps
        
        return []
    
    def _generate_function_name(self, result: Dict[str, Any]) -> str:
        """根据需求内容生成函数名"""
        # 基于操作类型创建前缀
        operation_prefixes = {
            "create": "create",
            "query": "find",
            "read": "get",
            "update": "update",
            "delete": "delete",
            "validate": "validate",
            "transform": "convert",
            "process": "process",
            "calculate": "calculate",
            "analyze": "analyze",
            "send": "send",
            "receive": "receive",
            "filter": "filter",
            "sort": "sort",
            "group": "group",
            "merge": "merge",
        }
        
        prefix = operation_prefixes.get(result["operation_type"], "process")
        
        # 查找主要操作对象
        object_name = "data"  # 默认对象名
        
        # 从参数描述中提取对象名称
        if result["parameters"]:
            param_desc = result["parameters"][0]["description"]
            for keyword in ["文件", "列表", "数组", "字典", "数据", "记录", "配置", "设置", "用户", "客户"]:
                if keyword in param_desc:
                    object_name = keyword
                    break
        
        # 英文关键词映射
        object_name_mapping = {
            "文件": "file",
            "列表": "list",
            "数组": "array",
            "字典": "dict",
            "数据": "data",
            "记录": "records",
            "配置": "config",
            "设置": "settings",
            "用户": "user",
            "客户": "customer",
        }
        
        # 转换为英文
        if object_name in object_name_mapping:
            object_name = object_name_mapping[object_name]
        
        # 生成最终函数名
        return f"{prefix}_{object_name}" 