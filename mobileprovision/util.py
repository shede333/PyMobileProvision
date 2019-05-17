#!/usr/bin/env python2.7
# _*_ coding:UTF-8 _*_
"""
__author__ = 'wangshaowei'
"""

import os
import subprocess

from . import parser


def mp_path_in_dir(dir_path):
    """
    查找dir_path目录下所有的mobileprovision文件
    :param dir_path: 目录路径
    :return: mobileprovision文件路径列表
    """
    mp_ext_name = parser.mp_ext_name
    path_list = []
    for file_name in os.listdir(dir_path):
        if file_name.endswith(mp_ext_name):
            file_path = os.path.join(dir_path, file_name)
            path_list.append(file_path)
    return path_list


def import_mobileprovision(mp_file_path, is_replace=False):
    """
    导入新的mobileprovision文件
    :param mp_file_path: mobileprovision文件路径
    :param is_replace: 是否删除相同"Name"属性的文件，默认False
    :return:
    """
    mp_home_dir = parser.mp_home_dir
    current_mp = parser.plist_obj(mp_file_path)
    current_name = current_mp["Name"]

    # 删除同name的mp文件
    has_same_name = False  # 是否有同Name的文件
    for file_path in mp_path_in_dir(mp_home_dir):
        tmp_mp = parser.plist_obj(file_path)
        tmp_name = tmp_mp["Name"]
        if is_replace and (current_name == tmp_name):
            has_same_name = True
            os.remove(file_path)
            print("- 删除文件:", file_path)
    if is_replace and (not has_same_name):
        print("* 没有同Name({})的mobileprovision文件".format(current_name))

    # 导入新的 mobileprovision 文件
    command = "open '{}'".format(mp_file_path)
    subprocess.call(command, shell=True)
    print("+ 导入mobileprovision: {}\n".format(command))
