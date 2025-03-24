#!/usr/bin/env python3
"""
Test Report Generator

This script generates a comprehensive test report by combining results from
unit tests, performance tests, and coverage reports.
"""

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

def parse_junit_xml(junit_path: Path) -> Dict[str, Any]:
    """Parse JUnit XML report and extract test statistics."""
    tree = ET.parse(junit_path)
    root = tree.getroot()
    
    total = int(root.attrib.get('tests', 0))
    failures = int(root.attrib.get('failures', 0))
    errors = int(root.attrib.get('errors', 0))
    skipped = int(root.attrib.get('skipped', 0))
    time = float(root.attrib.get('time', 0))
    
    return {
        'total': total,
        'passed': total - failures - errors - skipped,
        'failures': failures,
        'errors': errors,
        'skipped': skipped,
        'time': time
    }

def parse_coverage_xml(coverage_path: Path) -> Dict[str, Any]:
    """Parse coverage XML report and extract coverage statistics."""
    tree = ET.parse(coverage_path)
    root = tree.getroot()
    
    coverage = root.find('coverage')
    if coverage is not None:
        line_rate = float(coverage.attrib.get('line-rate', 0)) * 100
        branch_rate = float(coverage.attrib.get('branch-rate', 0)) * 100
        
        return {
            'line_coverage': line_rate,
            'branch_coverage': branch_rate
        }
    return {'line_coverage': 0, 'branch_coverage': 0}

def parse_performance_results(performance_dir: Path) -> List[Dict[str, Any]]:
    """Parse performance test results from JSON reports."""
    results = []
    for report_file in performance_dir.glob('*.json'):
        with open(report_file) as f:
            data = json.load(f)
            results.append(data)
    return results

def generate_markdown_report(
    unit_results: Dict[str, Any],
    coverage_results: Dict[str, Any],
    performance_results: List[Dict[str, Any]]
) -> str:
    """Generate a markdown format test report."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    report = [
        f"# 测试执行报告",
        f"\n生成时间: {timestamp}\n",
        
        "## 1. 单元测试结果",
        "| 指标 | 数值 |",
        "|------|------|",
        f"| 总用例数 | {unit_results['total']} |",
        f"| 通过数 | {unit_results['passed']} |",
        f"| 失败数 | {unit_results['failures']} |",
        f"| 错误数 | {unit_results['errors']} |",
        f"| 跳过数 | {unit_results['skipped']} |",
        f"| 执行时间 | {unit_results['time']:.2f}秒 |",
        
        "\n## 2. 代码覆盖率",
        "| 指标 | 比率 |",
        "|------|------|",
        f"| 行覆盖率 | {coverage_results['line_coverage']:.2f}% |",
        f"| 分支覆盖率 | {coverage_results['branch_coverage']:.2f}% |",
        
        "\n## 3. 性能测试结果"
    ]
    
    # 添加每个性能测试的结果
    for perf_result in performance_results:
        report.extend([
            f"\n### {perf_result.get('test_name', 'Unknown Test')}",
            "| 指标 | 数值 |",
            "|------|------|",
            f"| 平均执行时间 | {perf_result.get('mean_time', 0):.3f}秒 |",
            f"| 最大执行时间 | {perf_result.get('max_time', 0):.3f}秒 |",
            f"| 最小执行时间 | {perf_result.get('min_time', 0):.3f}秒 |",
            f"| 内存使用 | {perf_result.get('memory_usage', 0):.2f}MB |"
        ])
    
    # 添加总结
    total_pass_rate = (unit_results['passed'] / unit_results['total']) * 100
    report.extend([
        "\n## 4. 测试总结",
        f"- 单元测试通过率: {total_pass_rate:.2f}%",
        f"- 代码覆盖率: {coverage_results['line_coverage']:.2f}%",
        "- 性能测试: " + ("✅ 所有测试通过" if all(r.get('passed', False) for r in performance_results) else "❌ 部分测试未通过")
    ])
    
    return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description="Generate comprehensive test report")
    parser.add_argument('--unit-results', type=Path, required=True, help="Directory containing unit test results")
    parser.add_argument('--performance-results', type=Path, required=True, help="Directory containing performance test results")
    parser.add_argument('--coverage-results', type=Path, required=True, help="Directory containing coverage results")
    parser.add_argument('--output', type=Path, required=True, help="Output markdown file path")
    
    args = parser.parse_args()
    
    # Parse test results
    unit_results = parse_junit_xml(args.unit_results / 'junit.xml')
    coverage_results = parse_coverage_xml(args.coverage_results / 'coverage.xml')
    performance_results = parse_performance_results(args.performance_results)
    
    # Generate report
    report = generate_markdown_report(unit_results, coverage_results, performance_results)
    
    # Write report
    args.output.write_text(report, encoding='utf-8')
    print(f"Report generated: {args.output}")

if __name__ == '__main__':
    main() 