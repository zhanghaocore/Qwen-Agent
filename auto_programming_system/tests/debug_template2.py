"""
详细调试脚本：直接使用Jinja2渲染模板
"""

import os
import sys
import jinja2

# 将项目根目录添加到sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def debug_jinja_template():
    """直接使用Jinja2渲染模板"""
    # 获取模板目录路径
    templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../templates'))
    
    # 创建Jinja2环境
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(templates_dir),
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    # 定义测试上下文
    context = {
        "function_name": "test_function",
        "parameters": [{"name": "numbers", "type": "List[int]", "description": "整数列表"}],
        "return_type": "int",
        "function_description": "创建一个函数，接收一个整数列表，返回所有偶数的和",
        "implementation": "",  # 空实现，让模板条件判断生效
        "imports": ["from typing import Any, List, Dict, Optional"]
    }
    
    # 准备一个简单的测试模板字符串
    test_template_str = """
    {% if 'list' in function_description and 'sum' in function_description %}
    上下文中同时包含'list'和'sum'
    {% endif %}
    
    {% if '列表' in function_description and '和' in function_description %}
    上下文中同时包含'列表'和'和'
    {% endif %}
    """
    
    # 渲染测试模板
    test_template = jinja_env.from_string(test_template_str)
    test_result = test_template.render(**context)
    
    print("测试模板渲染结果:")
    print(test_result)
    
    # 尝试加载并渲染实际模板
    try:
        template = jinja_env.get_template("functions/basic_function.py.jinja")
        
        # 提取模板源码中的条件判断部分
        template_source = jinja_env.loader.get_source(jinja_env, "functions/basic_function.py.jinja")[0]
        
        # 查找关键条件判断
        key_condition = "{% if 'list' in function_description and 'sum' in function_description %}"
        condition_index = template_source.find(key_condition)
        
        if condition_index >= 0:
            print(f"\n找到关键条件判断，位于位置: {condition_index}")
            # 提取上下文相关部分，约50个字符
            context_before = template_source[max(0, condition_index-50):condition_index]
            context_after = template_source[condition_index:condition_index+len(key_condition)+50]
            print(f"条件前文本: {context_before}")
            print(f"条件及后文本: {context_after}")
        else:
            print("\n未找到关键条件判断，检查完整条件:")
            # 打印所有if语句
            import re
            if_conditions = re.findall(r'{%\s*if\s+.*?%}', template_source)
            print("模板中的所有if条件:")
            for i, cond in enumerate(if_conditions):
                print(f"{i+1}. {cond}")
        
        # 渲染完整模板
        result = template.render(**context)
        
        print("\n完整模板渲染结果:")
        print(result)
        
    except Exception as e:
        print(f"模板渲染出错: {e}")


if __name__ == "__main__":
    debug_jinja_template() 