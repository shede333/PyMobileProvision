#!/usr/bin/env python2.7
# _*_ coding:UTF-8 _*_
"""
__author__ = 'shede333'
"""

import os

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

print("{} - {}".format("*" * 10, find_packages()))

setup(
    name='Py2MobileProvision',  # 包名字
    version='0.3.2',  # 包版本
    author='shede333',  # 作者
    author_email='333wshw@163.com',  # 作者邮箱
    keywords='mobileprovision mobile provision MobileProvision',
    description='Python2, parse ".mobileprovision" file in MacOS System;',  # 简单描述
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/shede333/Py2MobileProvision',  # 包的主页
    packages=find_packages(),  # 包
    include_package_data=True,
    # package_data={'': ["**/*.mobileprovision", "*.txt"]},
    python_requires="~=2.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Natural Language :: Chinese (Simplified)",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
)
