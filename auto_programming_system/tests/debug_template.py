"""
调试脚本：检查模板渲染过程
"""

import os
import sys
import jinja2

# 将项目根目录添加到sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from auto_programming_system.code_generation.context_builder.builder import ContextBuilder
from auto_programming_system.code_generation.template_engine.engine import SmartTemplateEngine


def debug_rendering():
    """调试模板渲染过程"""
    # 创建一个测试规范
    specification = {
        "function_type": "function",
        "function_name": "calculate_sum_of_even_numbers",
        "description": "创建一个函数，接收一个整数列表，返回所有偶数的和",
        "parameters": [
            {
                "name": "numbers",
                "type": "List[int]",
                "description": "整数列表"
            }
        ],
        "return_type": "int",
        "return_description": "所有偶数的和",
        "constraints": [],
        "examples": []
    }
    
    # 获取模板目录路径
    templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../templates'))
    
    # 构建上下文
    context_builder = ContextBuilder()
    context = context_builder.build(specification)
    
    # 打印上下文，检查变量是否正确
    print("模板上下文:")
    for key, value in context.items():
        print(f"  {key}: {value}")
    
    # 加载模板
    template_engine = SmartTemplateEngine(templates_dir)
    template_name = "functions/basic_function"
    
    # 直接操作Jinja2环境以检查问题
    try:
        # 获取原始模板文本
        template_loader = jinja2.FileSystemLoader(templates_dir)
        jinja_env = jinja2.Environment(loader=template_loader)
        if jinja_env.loader is None:
            raise ValueError("Template loader is not initialized")
        template_source = jinja_env.loader.get_source(jinja_env, f"{template_name}.py.jinja")[0]
        
        print("\n原始模板内容片段:")
        # 只打印前100个字符和后100个字符，避免输出过多
        print(f"前100个字符: {template_source[:100]}")
        print(f"后100个字符: {template_source[-100:]}")
        
        # 检查关键条件判断
        if "{% if 'list' in function_description and 'sum' in function_description %}" in template_source:
            print("\n模板中包含'list'和'sum'的条件判断")
            
            # 检查上下文中是否有这些关键词
            if "function_description" in context:
                fd = context["function_description"].lower()
                list_in_fd = "list" in fd or "列表" in fd
                sum_in_fd = "sum" in fd or "和" in fd
                print(f"上下文中function_description是否包含'list': {list_in_fd}")
                print(f"上下文中function_description是否包含'sum': {sum_in_fd}")
                print(f"两者是否都包含: {list_in_fd and sum_in_fd}")
            else:
                print("上下文中缺少function_description变量")
        
        # 生成代码并输出
        code = template_engine.generate(template_name, context)
        print("\n生成的代码:")
        print(code)
        
    except Exception as e:
        print(f"模板渲染出错: {e}")


if __name__ == "__main__":
    debug_rendering() 