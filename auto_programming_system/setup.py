#!/usr/bin/env python3
"""
全自动Python后端编程系统 - 安装配置
"""

from setuptools import find_packages, setup

setup(
    name="auto_programming_system",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pytest>=6.0.0",
        "jinja2>=3.0.0",
        "qwen-agent>=0.0.16",  # 更新为最新可用版本
    ],
    python_requires=">=3.8",
    author="Qinghao Hao",
    author_email="hao.qinghao@gmail.com",
    description="An automatic programming system based on LLM",
    keywords="llm, automatic programming, code generation",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
