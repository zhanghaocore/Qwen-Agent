#!/usr/bin/env python3
"""
全自动Python后端编程系统 - 安装配置
"""

from setuptools import setup, find_packages

setup(
    name="auto_programming_system",
    version="0.1.0",
    description="An AI-powered automatic Python backend programming system",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "openai>=0.27.0",
        "fastapi>=0.68.0",
        "pydantic>=1.8.2",
        "pytest>=6.2.5",
        "black>=21.9b0",
        "isort>=5.9.3",
        "mypy>=0.910",
        "pylint>=2.11.1",
        "python-dotenv>=0.19.0",
        "requests>=2.26.0",
        "SQLAlchemy>=1.4.23",
        "uvicorn>=0.15.0",
        "jinja2>=3.0.1",
        "numpy>=1.21.2",
        "pandas>=1.3.3",
    ],
    extras_require={
        "dev": [
            "pytest-cov>=2.12.1",
            "pytest-mock>=3.6.1",
            "pytest-asyncio>=0.15.1",
            "black>=21.9b0",
            "isort>=5.9.3",
            "mypy>=0.910",
            "pylint>=2.11.1",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "console_scripts": [
            "auto-programming=src.__main__:main",
        ],
    },
)
