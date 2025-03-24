#!/usr/bin/env python3
"""
全自动Python后端编程系统 - 安装配置
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="auto_programming_system",
    version="0.1.0",
    author="AutoProgramming Team",
    author_email="contact@autoprogramming.example",
    description="自然语言到可执行Python代码的自动转换系统",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/autoprogramming/auto_programming_system",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "auto_programming_system": ["templates/**/*.jinja"],
    },
    entry_points={
        "console_scripts": [
            "auto-program=auto_programming_system.__main__:main",
        ],
    },
)
