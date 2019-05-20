#!/usr/bin/env python2.7
# _*_ coding:UTF-8 _*_
"""
__author__ = 'wangshaowei'
"""

import os

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

setup(
    name='PyMobileProvision',  # 包名字
    version='0.2.1',  # 包版本
    author='shede333',  # 作者
    author_email='333wshw@163.com',  # 作者邮箱
    keywords='mobileprovision mobile provision MobileProvision',
    description='parse ".mobileprovision" file in MacOS System;',  # 简单描述
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/shede333/PyMobileProvision',  # 包的主页
    packages=find_packages(),  # 包
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: Chinese (Simplified)",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
