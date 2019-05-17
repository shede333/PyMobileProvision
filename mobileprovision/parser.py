#!/usr/bin/env python2.7
# _*_ coding:UTF-8 _*_
"""
__author__ = 'wangshaowei'
"""

import os
import plistlib
import re

mp_home_dir = os.path.expanduser("~/Library/MobileDevice/Provisioning Profiles")
mp_ext_name = ".mobileprovision"


def content(file_path):
    """
    从mobileprovision文件里提取出plist部分的字符串内容
    :param file_path: mobileprovision文件路径
    :return: plist部分的字符串内容
    """
    with open(file_path, "rb") as fp:
        file_content = fp.read()

    p_start = re.escape("<?xml")
    p_end = re.escape("</plist>")
    pattern_str = "{}.+{}".format(p_start, p_end)
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
    return plistlib.readPlistFromString(xml_content)
