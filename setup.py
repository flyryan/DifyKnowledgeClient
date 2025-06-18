#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="dify-knowledge-client",
    version="1.0.0",
    description="Interactive client for Dify Knowledge API",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "rich>=13.7.0",
        "click>=8.1.7",
        "python-dotenv>=1.0.0",
        "tabulate>=0.9.0",
        "prompt-toolkit>=3.0.43",
    ],
    entry_points={
        "console_scripts": [
            "dify-client=cli:main",
        ],
    },
    python_requires=">=3.7",
)