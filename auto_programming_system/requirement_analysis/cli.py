"""
命令行接口模块
提供简单的命令行界面来执行文本预处理
"""
import argparse
import json
import sys
import os
from typing import Dict, Any, Optional

from auto_programming_system.requirement_analysis.preprocessor.preprocessor import TextPreprocessor


def convert_to_serializable(obj: Any) -> Any:
    """
    将对象转换为可序列化的格式，适用于JSON输出
    
    Args:
        obj: 要转换的对象
        
    Returns:
        可JSON序列化的对象
    """
    if isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    elif isinstance(obj, tuple):
        return list(obj)
    elif hasattr(obj, '__dict__'):
        return convert_to_serializable(obj.__dict__)
    else:
        return obj


def preprocess_text(args: argparse.Namespace) -> Optional[Any]:
    """
    执行文本预处理
    
    Args:
        args: 命令行参数
        
    Returns:
        处理结果
    """
    # 创建预处理器
    preprocessor = TextPreprocessor(args.dictionary)
    
    # 读取输入文本
    if args.input_file:
        try:
            with open(args.input_file, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading input file: {e}", file=sys.stderr)
            return None
    else:
        text = args.text
    
    # 处理文本
    try:
        result = preprocessor.preprocess(text)
        return result
    except Exception as e:
        print(f"Error during preprocessing: {e}", file=sys.stderr)
        return None


def main() -> None:
    """命令行入口点"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='文本预处理工具')
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--text', type=str, help='要处理的文本')
    input_group.add_argument('--input-file', type=str, help='包含输入文本的文件路径')
    
    parser.add_argument('--dictionary', type=str, help='技术术语词典文件路径（可选）')
    parser.add_argument('--output', type=str, help='输出文件路径（如未指定则输出到标准输出）')
    parser.add_argument('--format', choices=['json', 'text'], default='json', 
                        help='输出格式，可选json或text（默认：json）')
    parser.add_argument('--details', action='store_true', help='显示详细信息，包括技术术语和元数据')
    
    args = parser.parse_args()
    
    # 执行预处理
    result = preprocess_text(args)
    if not result:
        sys.exit(1)
    
    # 准备输出
    if args.format == 'json':
        # 使用内置方法输出JSON
        output = result.to_json()
    else:
        # 文本格式输出，根据用户选择显示不同级别的详细信息
        sentences = '\n'.join([f"  - {s}" for s in result.sentences])
        
        # 技术术语展示
        if args.details:
            tech_terms = '\n'.join([
                f"  - {t['term']} (类型: {t.get('type', '未知')}, 置信度: {t.get('confidence', '未知'):.2f})" 
                for t in result.technical_terms
            ])
            metadata_str = json.dumps(result.metadata, ensure_ascii=False, indent=2)
        else:
            # 简化输出，只显示最重要的术语
            top_terms = sorted(result.technical_terms, key=lambda t: t.get('confidence', 0), reverse=True)[:5]
            tech_terms = '\n'.join([f"  - {t['term']}" for t in top_terms])
            metadata_str = json.dumps({k: v for k, v in result.metadata.items() 
                                     if k in ['sentence_count', 'term_count']}, 
                                   ensure_ascii=False, indent=2)
        
        output = f"""
预处理结果:
-----------
原始文本:
{result.original_text}

清洗后文本:
{result.cleaned_text}

句子分割:
{sentences}

识别到的技术术语:
{tech_terms}

规范化文本:
{result.normalized_text}

元数据:
{metadata_str}
"""
    
    # 输出结果
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"结果已保存到 {args.output}")
        except Exception as e:
            print(f"Error writing output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output)


if __name__ == '__main__':
    main() 