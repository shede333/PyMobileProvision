#!/usr/bin/env python
# _*_ coding:UTF-8 _*_
"""
__author__ = 'shede333'
"""

from pathlib import Path

from setuptools import find_packages
from setuptools import setup

README = Path(__file__).resolve().with_name("README.md").read_text()

print("{} - {}".format("*" * 10, find_packages()))

setup(
    name='PyMobileProvision',  # 包名字
    version='0.4',  # 包版本
    author='shede333',  # 作者
    author_email='333wshw@163.com',  # 作者邮箱
    keywords='mobileprovision mobile provision MobileProvision',
    description='Python3, parse ".mobileprovision" file in MacOS System;',  # 简单描述
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/shede333/PyMobileProvision',  # 包的主页
    packages=find_packages(),  # 包
    include_package_data=True,
    # package_data={'': ["**/*.mobileprovision", "*.txt"]},
    python_requires="~=3.4",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Natural Language :: Chinese (Simplified)",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
