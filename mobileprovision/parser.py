#!/usr/bin/env python
# _*_ coding:UTF-8 _*_
"""
__author__ = 'shede333'
"""

import plistlib
import re

from pathlib import Path


def content(file_path):
    """
    从mobileprovision文件里提取出plist部分的字符串内容
    :param file_path: mobileprovision文件路径
    :return: plist部分的字符串内容
    """
    p_start = re.escape("<?xml")
    p_end = re.escape("</plist>")
    pattern_str = "{}.+{}".format(p_start, p_end)
    file_content = Path(file_path).read_text(encoding="ascii", errors="ignore")
    result = re.search(pattern_str, file_content, flags=re.DOTALL)
    xml_content = result.group()
    return xml_content


def plist_obj(file_path):
    """
    从mobileprovision文件里提取出plist对象
    :param file_path: mobileprovision文件路径
    :return: plist对象
    """
    xml_content = content(file_path)
    return plistlib.loads(bytes(xml_content, encoding="ascii"))


def convert_plist_file(mp_file_path, dst_file_path):
    """
    转换为plist文件
    :param mp_file_path: mobileprovision文件路径
    :param dst_file_path: 转换后得到的plist文件路径
    :return:
    """
    xml_content = content(mp_file_path)
    Path(dst_file_path).open("w").write(xml_content)
