#!/usr/bin/env python2.7
# _*_ coding:UTF-8 _*_
"""
__author__ = 'shede333'
"""

import os
import shutil
import stat

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


def import_mobileprovision(mp_file_path, replace_at_attr=None):
    """
    导入新的mobileprovision文件
    :param mp_file_path: mobileprovision文件路径
    :param replace_at_attr: 删除属性相同的文件，这里代表需要对比的属性列表，属性间为"或"的关系
    :return:
    """
    mp_ext_name = parser.mp_ext_name
    mp_home_dir = parser.mp_home_dir
    current_mp = parser.plist_obj(mp_file_path)
    current_uuid = current_mp["UUID"]
    replace_at_attr = set(replace_at_attr) if replace_at_attr else None
    print("开始导入mobileprovision 文件：")

    # 删除同name的mp文件
    has_same_name = False  # 是否有同Name的文件
    for file_path in mp_path_in_dir(mp_home_dir):
        tmp_mp = parser.plist_obj(file_path)
        if not replace_at_attr:
            continue
        for tmp_key in replace_at_attr:
            tmp_value = tmp_mp.get(tmp_key, None)
            current_value = current_mp.get(tmp_key, None)
            if tmp_value and current_value and (tmp_value == current_value):
                has_same_name = True
                os.remove(file_path)
                print("\t- 删除文件:", file_path)

    if replace_at_attr and (not has_same_name):
        print("\t* 没有相同属性({})的mobileprovision文件".format(replace_at_attr))

    # 导入新的 mobileprovision 文件
    if not os.path.isdir(mp_home_dir):
        os.makedirs(mp_home_dir)
    file_name = "{}{}".format(current_uuid, mp_ext_name)
    dst_path = os.path.join(mp_home_dir, file_name)
    shutil.copy(mp_file_path, dst_path)
    # 修改文件权限"-rw-r--r-- "
    os.chmod(dst_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    print("+ 成功导入mobileprovision: \n\tfrom: {}\n\tto: {}".format(mp_file_path, dst_path))
