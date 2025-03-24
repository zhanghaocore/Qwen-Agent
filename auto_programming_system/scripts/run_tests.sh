#!/bin/bash

# 自动化测试执行脚本
# 用于运行单元测试、性能测试和生成测试报告

# 设置环境变量
export PYTHONPATH="$PYTHONPATH:$(pwd)"
export PYTEST_ADDOPTS="--color=yes"

# 创建测试结果目录
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
TEST_RESULTS_DIR="test_results_${TIMESTAMP}"
mkdir -p "${TEST_RESULTS_DIR}"/{unit,performance,coverage}

echo "开始执行测试..."

# 运行单元测试
echo "运行单元测试..."
python -m pytest tests/requirement_analysis/ \
    --verbose \
    --junitxml="${TEST_RESULTS_DIR}/unit/junit.xml" \
    --html="${TEST_RESULTS_DIR}/unit/report.html" \
    --self-contained-html

# 运行性能测试
echo "运行性能测试..."
python -m pytest tests/performance/ \
    --verbose \
    -m benchmark \
    --html="${TEST_RESULTS_DIR}/performance/report.html" \
    --self-contained-html

# 运行覆盖率测试
echo "运行覆盖率测试..."
python -m pytest tests/ \
    --cov=auto_programming_system \
    --cov-report=html:"${TEST_RESULTS_DIR}/coverage" \
    --cov-report=xml:"${TEST_RESULTS_DIR}/coverage/coverage.xml"

# 生成测试报告摘要
echo "生成测试报告摘要..."
python scripts/generate_report.py \
    --unit-results="${TEST_RESULTS_DIR}/unit" \
    --performance-results="${TEST_RESULTS_DIR}/performance" \
    --coverage-results="${TEST_RESULTS_DIR}/coverage" \
    --output="${TEST_RESULTS_DIR}/summary.md"

# 检查测试结果
UNIT_EXIT_CODE=$?
if [ $UNIT_EXIT_CODE -ne 0 ]; then
    echo "单元测试失败！"
    exit $UNIT_EXIT_CODE
fi

echo "测试执行完成。"
echo "测试报告位置: ${TEST_RESULTS_DIR}"
echo "- 单元测试报告: ${TEST_RESULTS_DIR}/unit/report.html"
echo "- 性能测试报告: ${TEST_RESULTS_DIR}/performance/report.html"
echo "- 覆盖率报告: ${TEST_RESULTS_DIR}/coverage/index.html"
echo "- 测试摘要: ${TEST_RESULTS_DIR}/summary.md" 