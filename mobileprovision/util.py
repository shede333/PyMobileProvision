#!/usr/bin/env python
# _*_ coding:UTF-8 _*_
"""
__author__ = 'shede333'
"""

import shutil
import stat
from pathlib import Path

from . import parser

MP_ROOT_PATH = Path("~/Library/MobileDevice/Provisioning Profiles").expanduser()
MP_EXT_NAME = ".mobileprovision"


def mp_path_in_dir(dir_path):
    """
    查找dir_path目录下所有的mobileprovision文件
    :param dir_path: 目录路径
    :return: mobileprovision文件路径列表
    """
    path_list = []
    for file_path in Path(dir_path).iterdir():
        if file_path.suffix == MP_EXT_NAME:
            path_list.append(file_path)
    return path_list


def import_mobileprovision(mp_file_path, replace_at_attrs=None):
    """
    导入新的mobileprovision文件
    :param mp_file_path: mobileprovision文件路径
    :param replace_at_attrs: 删除属性相同的文件，这里代表需要对比的属性列表，属性间为"或"的关系
    :return:
    """
    current_mp = parser.plist_obj(mp_file_path)
    current_uuid = current_mp["UUID"]
    replace_at_attrs = set(replace_at_attrs) if replace_at_attrs else None
    print("开始导入mobileprovision 文件：")

    # 删除同name的mp文件
    has_same_name = False  # 是否有同Name的文件
    for file_path in mp_path_in_dir(MP_ROOT_PATH):
        tmp_mp = parser.plist_obj(file_path)
        if not replace_at_attrs:
            continue
        for tmp_key in replace_at_attrs:
            tmp_value = tmp_mp.get(tmp_key, None)
            current_value = current_mp.get(tmp_key, None)
            if tmp_value and current_value and (tmp_value == current_value):
                has_same_name = True
                file_path.unlink()
                print("\t- 删除文件:", file_path)

    if replace_at_attrs and (not has_same_name):
        print("\t* 没有相同属性({})的mobileprovision文件".format(replace_at_attrs))

    # 导入新的 mobileprovision 文件
    MP_ROOT_PATH.mkdir(parents=True, exist_ok=True)
    file_name = "{}{}".format(current_uuid, MP_EXT_NAME)
    dst_path = MP_ROOT_PATH.joinpath(file_name)
    shutil.copy(mp_file_path, dst_path)
    # 修改文件权限"-rw-r--r-- "
    dst_path.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    print("+ 成功导入mobileprovision: \n\tfrom: {}\n\tto: {}".format(mp_file_path, dst_path))
